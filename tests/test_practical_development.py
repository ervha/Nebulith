import subprocess
import unittest
from pathlib import Path


class PracticalDevelopmentChecks(unittest.TestCase):
    def test_catalog_roles_negatives_and_confirmation(self):
        root=Path(__file__).resolve().parents[1]
        result=subprocess.run(['node','tests/verify_practical_development.js'],cwd=root,capture_output=True,text=True,encoding='utf-8',timeout=30)
        self.assertEqual(0,result.returncode,result.stdout+result.stderr)


if __name__=='__main__':unittest.main()
