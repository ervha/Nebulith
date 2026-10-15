import subprocess,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]


class IncrementalInputChecks(unittest.TestCase):
    def test_web_shared_input_fixtures(self):
        p=subprocess.run(['node','tests/verify_incremental.js'],cwd=ROOT,capture_output=True,text=True,encoding='utf-8',timeout=20)
        self.assertEqual(0,p.returncode,p.stdout+p.stderr)
        self.assertIn('24 shared incremental fixtures',p.stdout)

