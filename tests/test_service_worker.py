import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from build_web_studio import update_service_worker


class ServiceWorkerVersionChecks(unittest.TestCase):
    def test_asset_changes_update_cache_name_and_identical_builds_are_stable(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            script = "const CACHE_NAME = 'nebulith-studio-old';\nconst PRECACHE_ASSETS = ['./', './app.js'];\n"
            (root / 'service-worker.js').write_text(script, encoding='utf-8')
            (root / 'index.html').write_text('index', encoding='utf-8')
            (root / 'app.js').write_text('first', encoding='utf-8')
            first = update_service_worker(root)
            self.assertEqual(first, update_service_worker(root))
            (root / 'app.js').write_text('second', encoding='utf-8')
            second = update_service_worker(root)
            self.assertNotEqual(first, second)
            self.assertIn(second, (root / 'service-worker.js').read_text(encoding='utf-8'))
            (root / 'index.html').write_text('new index', encoding='utf-8')
            self.assertNotEqual(second, update_service_worker(root))
