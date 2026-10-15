"""Independent read-only checks. Run with .venv-audit/Scripts/python.exe.
Writes only independent.json in this execution's directory.
"""
import hashlib
import io
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
raw = lambda p: (ROOT / p).read_bytes()
sha = lambda b: hashlib.sha256(b).hexdigest()
e = json.loads(raw('audit/2026-10-15-reaudit-02/evidence.json'))
vocab = json.loads(raw('data/lexicon.json'))['vocabulary']
by_id = {v['id']: v for v in vocab}
by_root = {v['nrs']: v for v in vocab}
spec = raw('docs/Project Requirements And Design.md').decode('utf-8')

def normalize(s):
    return re.sub(r'[\[\]/.\s]', '', s).replace('ɾ', 'r')

groups = {}
for v in vocab:
    groups.setdefault(normalize(v['ipa']), []).append(v['id'])
ipa_mismatches = []
for v in vocab:
    expected = v['nrs']
    for source, target in [('ai', 'aɪ'), ('ei', 'eɪ'), ('au', 'aʊ'), ('oi', 'ɔɪ'),
                           ('c', 'ʃ'), ('j', 'ʒ'), ("'", 'ʔ')]:
        expected = expected.replace(source, target)
    if normalize(v['ipa']) != expected:
        ipa_mismatches.append({'id': v['id'], 'nrs': v['nrs'], 'actual': v['ipa'],
                               'expected_without_syllable_breaks': expected})

corpus = spec.split('### 6.5 ')[1]
references = []
for number, line in enumerate(spec.splitlines(), 1):
    if number <= spec[:spec.index('### 6.5 ')].count('\n'):
        continue
    for match in re.finditer(r'`([^`]+)`\s*\(([^)]*)\)', line):
        token, gloss = match.groups()
        ids = [int(x) for x in re.findall(r'ID\s+(\d+)', gloss)]
        for id_ in ids:
            entry = by_id.get(id_)
            references.append({'line': number, 'token': token, 'gloss': gloss, 'id': id_,
                               'dictionary': entry,
                               'direct_token_matches_id': entry is not None and entry['nrs'] == token.lower()})

fonts = {'current': TTFont(ROOT / 'fonts/Nebulith-Regular.ttf'),
         'head_commit': TTFont(io.BytesIO(subprocess.check_output(
             ['git', 'show', 'HEAD:fonts/Nebulith-Regular.ttf'], cwd=ROOT)))}
font = fonts['current']
table_comparison = {}
for table in sorted(set(font.keys()) & set(fonts['head_commit'].keys()) - {'GlyphOrder'}):
    a, b = (f.getTableData(table) for f in fonts.values())
    table_comparison[table] = {'same': a == b, 'current_sha256': sha(a), 'head_sha256': sha(b)}
font_details = {'table_comparison_with_head': table_comparison,
                'space_metrics': font['hmtx']['space'],
                'notdef_contours': font['glyf']['.notdef'].numberOfContours,
                'notdef_coordinates': list(map(list, font['glyf']['.notdef'].coordinates)),
                'fontRevision': font['head'].fontRevision,
                'created': font['head'].created, 'modified': font['head'].modified}

old = json.loads(raw('audit/2026-10-15-reaudit/evidence.json'))
old_manifest_drift = [p for p, m in old['manifest'].items() if sha(raw(p)) != m['sha256']]
copied_artifacts = {}
for name in ['browser-evidence.json', 'font-preview.png', 'numeral-preview.png', 'all-glyphs.png']:
    a, b = (raw(f'audit/{folder}/{name}') for folder in ['2026-10-15', '2026-10-15-reaudit'])
    copied_artifacts[name] = {'byte_identical_to_initial_audit': a == b,
                              'initial_sha256': sha(a), 'previous_reaudit_sha256': sha(b)}

result = {'normalized_ipa_duplicates': {s: ids for s, ids in groups.items() if len(ids) > 1},
          'ipa_mapping_mismatches': ipa_mismatches, 'corpus_id_references': references,
          'corpus_token_count': sum(len(t['tokens']) for t in e['corpus']),
          'corpus_token_types': dict(Counter(t['type'] for c in e['corpus'] for t in c['tokens'])),
          'category_metadata_total': sum(c['wordsCount'] for c in e['category_metadata']),
          'category_metadata_mismatches': [c for c in e['category_metadata']
              if c['wordsCount'] != e['category_counts'].get(c['name'], 0)],
          'marked_coda_count': len(e['marked_codas']),
          'marked_coda_endings': dict(Counter(r['nrs'][-1] for r in e['marked_codas'])),
          'unmarked_rate': e['unmarked_or_vowel_rate'],
          'coda_approval_predicate': "category prefix is any integer 1..16; no semantic test",
          'previous_evidence_manifest_drift': old_manifest_drift,
          'previous_browser_artifact_comparison': copied_artifacts,
          'font': font_details}
(OUT / 'independent.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({k: v for k, v in result.items() if k not in ['corpus_id_references']},
                 ensure_ascii=False, indent=2))
