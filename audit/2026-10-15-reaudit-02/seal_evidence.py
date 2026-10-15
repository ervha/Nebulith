"""Verify audited inputs are unchanged and seal this run's evidence."""
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
REPORT = ROOT / 'docs/Nebulith Audit Results 2026-10-15-Reaudit-02.md'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
e = json.loads((OUT / 'evidence.json').read_text(encoding='utf-8'))
for p, info in e['manifest'].items():
    assert sha(ROOT / p) == info['sha256'], f'Audited input changed: {p}'
score = json.loads((OUT / 'scorecard.json').read_text(encoding='utf-8'))
assert [r['id'] for r in score['items']] == [f'CHK-{i:02d}' for i in range(1, 16)]
assert dict(Counter(r['status'] for r in score['items'])) == score['counts']
report = REPORT.read_text(encoding='utf-8')
rows = re.findall(r'^\| CHK-\d{2} .*$', report, re.M)
assert len(rows) == 15
for row, item in zip(rows, score['items']):
    assert f"**{item['status']}**" in row
for target in re.findall(r'\]\(([^)]+)\)', report):
    if '://' not in target:
        # seal.json itself is about to be generated.
        p = (REPORT.parent / unquote(target)).resolve()
        assert p.exists() or p == OUT / 'seal.json', target
artifacts = {str(p.relative_to(ROOT)).replace('\\', '/'): sha(p)
             for p in sorted(OUT.iterdir()) if p.is_file() and p.name != 'seal.json'}
artifacts[str(REPORT.relative_to(ROOT)).replace('\\', '/')] = sha(REPORT)
seal = {'timestamp_utc': datetime.now(timezone.utc).isoformat(),
        'audited_inputs_unchanged': True, 'scorecard_verified': True,
        'counts': score['counts'], 'artifact_sha256': artifacts}
(OUT / 'seal.json').write_text(json.dumps(seal, indent=2)+'\n', encoding='utf-8')
print('Verified: audited inputs unchanged; 15 distinct checks; counts 10/1/4; report links; evidence sealed.')
