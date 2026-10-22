import subprocess
import unittest
from pathlib import Path

class RoadmapV4Checks(unittest.TestCase):
    def test_lexical_meaning_roles_choices_and_failures(self):
        result=subprocess.run(['node','tests/verify_roadmap_v4.js'],cwd=Path(__file__).resolve().parents[1],capture_output=True,text=True,encoding='utf-8',timeout=60)
        self.assertEqual(0,result.returncode,result.stdout+result.stderr)
