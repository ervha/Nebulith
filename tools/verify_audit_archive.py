"""Verify original document bytes and historical sealed artifacts after relocation."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def verify():
    migration = json.loads((ROOT / 'audit/document-migration.json').read_text(encoding='utf-8'))
    originals = {r['oldPath']: r for r in migration['documents']}
    count = 0
    for r in originals.values():
        assert hashlib.sha256((ROOT / r['originalPath']).read_bytes()).hexdigest() == r['originalSha256']
        assert (ROOT / r['currentPath']).is_file()
        assert not (ROOT / r['oldPath']).exists()
    for seal_path in (ROOT / 'audit').glob('2026-*/seal.json'):
        seal = json.loads(seal_path.read_text(encoding='utf-8'))
        for old, expected in seal['artifact_sha256'].items():
            path = ROOT / (originals[old]['originalPath'] if old in originals else old)
            assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, old
            count += 1
    return {'originalDocuments': len(originals), 'historicalSealedArtifacts': count}


if __name__ == '__main__':
    print(verify())
