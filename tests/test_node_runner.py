import contextlib
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from run_node_checks import run_checks


class NodeRunnerChecks(unittest.TestCase):
    def test_nonzero_child_is_recorded_and_later_checks_still_run(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'tests').mkdir()
            bad, good = root / 'tests/verify_bad.js', root / 'tests/verify_good.js'
            bad.write_text('process.exit(9);', encoding='utf-8')
            good.write_text("require('fs').writeFileSync('ran.txt', 'yes');", encoding='utf-8')
            result = subprocess.run(
                [sys.executable, '-c',
                 'import sys; from pathlib import Path; sys.path.insert(0, sys.argv[1]); '
                 'import run_node_checks as runner; runner.ROOT = Path(sys.argv[2]); '
                 'raise SystemExit(runner.main())',
                 str(Path(__file__).resolve().parents[1] / 'tools'), str(root)],
                capture_output=True, text=True, encoding='utf-8', timeout=20)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn('FAIL: verify_bad.js (exit 9)', result.stdout)
            self.assertIn('JavaScript suites: 1/2 passed', result.stdout)
            self.assertEqual('yes', (root / 'ran.txt').read_text())

    def test_successful_child_does_not_report_failure(self):
        with tempfile.TemporaryDirectory() as folder:
            script = Path(folder) / 'pass.js'
            script.write_text('process.exit(0);', encoding='utf-8')
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual([], run_checks([script]))
