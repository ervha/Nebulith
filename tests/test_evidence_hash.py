import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from evidence_hash import recorded_digest_matches


class EvidenceHashChecks(unittest.TestCase):
    def test_only_legacy_line_endings_can_match_text(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'record.json'
            original = b'{"meaning": "sky"}\r\n'
            expected = hashlib.sha256(original).hexdigest()
            path.write_bytes(original.replace(b'\r\n', b'\n'))
            self.assertTrue(recorded_digest_matches(path, expected))
            for changed in [b'{"meaning": "sea"}\n', b'{ "meaning": "sky"}\n', b'{"meaning": "sky"}']:
                path.write_bytes(changed)
                self.assertFalse(recorded_digest_matches(path, expected))
            binary = Path(folder) / 'record.pdf'
            binary.write_bytes(original.replace(b'\r\n', b'\n'))
            self.assertFalse(recorded_digest_matches(binary, expected))
