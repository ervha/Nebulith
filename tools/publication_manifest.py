"""Record current publication bytes while preserving dated historical manifests."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HISTORICAL = 'audit/maintenance/codex-build-20261016.json'
CURRENT = 'audit/maintenance/current-publication.json'


def build_manifest(root=ROOT):
    previous = json.loads((root / HISTORICAL).read_text(encoding='utf-8'))
    result = {k: v for k, v in previous.items() if k != 'sha256'}
    result.update(previousManifest=HISTORICAL, independentReviewGranted=False,
                  manifestPurpose='Current byte integrity; does not grant linguistic approval')
    paths = list(previous['sha256']) + ['tools/publication_manifest.py', 'tools/evidence_hash.py']
    result['sha256'] = {p: hashlib.sha256((root / p).read_bytes()).hexdigest() for p in paths}
    return result


if __name__ == '__main__':
    (ROOT / CURRENT).write_text(json.dumps(build_manifest(), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
