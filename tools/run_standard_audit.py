"""Read-only SOP audit evidence collector; does not repair or regenerate assets.

Run from the repository root with the fonttools version in requirements.txt.
The JSON is evidence, not an automatic linguistic/visual certification.
"""
import base64
import csv
import hashlib
import io
import json
import os
import platform
import re
import subprocess
import sys
import argparse
import uuid
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from fontTools import __version__ as fonttools_version
from fontTools.ttLib import TTFont

sys.path.append(str(Path(__file__).resolve().parent))
from false_friend_detector import EARTH_WORDS, levenshtein
from nebulith_data import expected_ipa, normalize_ipa, validate_corpus, corpus_markdown, corpus_semantic_pending
from audit_reviews import coda_review, glyph_review
from earth_comparison import load_and_compare

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', help='New evidence directory under audit; existing directories are refused')
args = parser.parse_args()
default = 'audit/runs/'+datetime.now(timezone.utc).strftime('%Y-%m-%d-%H%M%S')+'-'+uuid.uuid4().hex[:8]
OUT = (ROOT / (args.output or os.environ.get('AUDIT_OUT_DIR') or default)).resolve()
if ROOT / 'audit' not in OUT.parents:
    parser.error('Output must be a child directory of audit/')
OUT.mkdir(parents=True, exist_ok=False)


def read(path):
    return (ROOT / path).read_text(encoding='utf-8')


paths = ['audit/docs/Nebulith Standard Audit Report.md', 'docs/Nebulith Master Lexicon.md',
         'data/lexicon.json', 'data/lexicon.csv', 'data/StaticLexicon.kt',
         'docs/Project Requirements And Design.md', 'fonts/Nebulith-Regular.ttf',
         'fonts/font_b64.txt', 'fonts/preview.html', 'tools/num_specimen.html',
         'tools/comprehensive_audit_1008.py', 'tools/false_friend_detector.py',
         'tools/analyze_lexicon_roots.py', 'tools/run_standard_audit.py',
         'tools/nebulith_data.py', 'tools/audit_reviews.py', 'data/canon_corpus.json',
         'data/audit/coda_reviews.json', 'data/audit/glyph_reviews.json',
         'data/audit/earth_sources.json', 'audit/document-migration.json', 'tools/sync_web_fonts.py',
         'fonts/inventory.json', 'fonts/punctuation.html', 'tools/font_symbols.py']
manifest = {}
paths += ['data/corpus_rules.json', 'tools/corpus_review.py', 'tools/review_canon.py',
          'data/audit/earth_candidate_reviews.json', 'data/audit/flight_root_migration.json',
          'tools/resolve_reviewed_flight_collision.py',
          'audit/docs/Nebulith Lexical Change Policy 2026-10-15.md',
          'data/audit/corpus_review_batch_2026-10-15.json',
          'data/audit/earth_lexicon.jsonl', 'data/audit/earth_concept_links.json',
          'data/audit/earth_concepts.json', 'tools/earth_comparison.py',
          'tools/import_swadesh_comparison.py', 'data/audit/stone_root_migration.json',
          'data/audit/coda_repair_candidates.json', 'audit/comparisons/glyph-v'+json.loads(read('fonts/inventory.json'))['fontVersion']+'/inventory.json',
          'tools/build_font.py', 'tools/build_glyph_comparison.py', 'tools/font_letter_revision.py',
          'tools/review_glyphs_v24.py', 'data/audit/glyph_review_batch_v24.json', 'fonts/handwriting.html',
          'tools/font_pending_revision.py', 'tools/review_glyphs_v25.py', 'data/audit/glyph_review_batch_v25.json']
paths += ['README.md','docs/Nebulith Executive Summary.md','docs/NEXT_DEVELOPMENT_PLAN.md',
          'tools/earth_scope.py','data/audit/earth_scope_policy.json','data/audit/earth_scope_reviews.json',
          'data/audit/earth_research_batch_01.json','tools/research_earth_batch.py','data/audit/nebula_root_migration.json',
          'tools/fix_reviewed_nebula_collision.py','tools/expand_corpus.py','tools/review_corpus_30.py',
          'data/audit/corpus_review_batch_30.json','audit/maintenance/2026-10-15-cleanup.json',
          'tools/clean_workspace.ps1','tools/update_project_overview.py','tools/build_web_studio.py','tools/verify_web_bundle.py',
          'tools/studio_dictionary.py','data/usage_examples.json','data/feedback_resolutions.json','data/translation_extensions.json','data/translation_patterns.json','data/grammar_dictionary.json','data/translation_input_rules.json',
          'data/translation_input_fixtures.json','web/README.md','web/app.js','web/incremental.js','web/workspace.js','data/language_review_ledger.json',
          'web/data.js','web/index.html','web/standalone.html','web/build-manifest.json']
batch_dir = ROOT / 'audit/runs/2026-10-15-all-roots'
if (batch_dir / 'comparison.json').exists():
    paths += ['tools/compare_all_roots.py', 'tools/report_all_roots.py', 'tests/test_all_roots.py',
              'audit/docs/Nebulith All Roots Multilingual Comparison 2026-10-15.md']
    paths += [p.relative_to(ROOT).as_posix() for p in sorted(batch_dir.rglob('*'))
              if p.is_file() and 'check' not in p.relative_to(batch_dir).parts and p.suffix in ['.json','.csv']]
comparison_dir = ROOT / ('audit/comparisons/glyph-v'+json.loads(read('fonts/inventory.json'))['fontVersion'])
paths += [p.relative_to(ROOT).as_posix() for p in sorted(comparison_dir.glob('*.html'))]
for path in paths:
    raw = (ROOT / path).read_bytes()
    info = {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}
    if not path.endswith(('.ttf','.jar','.png')):
        text = raw.decode('utf-8', errors='strict')
        info.update(lines=len(text.splitlines()), bom=raw.startswith(b'\xef\xbb\xbf'),
                    crlf=raw.count(b'\r\n'), lf_only=raw.count(b'\n')-raw.count(b'\r\n'),
                    cr_only=raw.count(b'\r')-raw.count(b'\r\n'))
    manifest[path] = info
data = json.loads(read('data/lexicon.json'))
vocab = data['vocabulary']
fields = ['id', 'category', 'nrs', 'ipa', 'pos', 'meaningJa', 'meaningEn', 'notes']
csv_rows = list(csv.DictReader(io.StringIO(read('data/lexicon.csv'))))
for row in csv_rows:
    row['id'] = int(row['id'])
kt_rows = []
for line in read('data/StaticLexicon.kt').splitlines():
    match = re.fullmatch(r'\s*LexiconEntry\((\d+), (.*)\),', line)
    if match:
        values = json.loads('[' + match[2] + ']')
        assert len(values) == 7
        kt_rows.append(dict(zip(fields, [int(match[1]), *values])))
md_rows = []
category = None
for line in read('docs/Nebulith Master Lexicon.md').splitlines():
    match = re.match(r'^### (\d+\. .+?) \(\d+語\)\s*$', line)
    if match:
        category = match[1]
    cells = [c.strip() for c in line.strip().strip('|').split('|')]
    if len(cells) == 7 and cells[0].isdigit():
        assert category is not None
        values = [int(cells[0]), category, cells[1].strip('*'), cells[2].strip('`'), *cells[3:]]
        md_rows.append(dict(zip(fields, values)))
formats = {'json': vocab, 'csv': csv_rows, 'kotlin': kt_rows, 'markdown': md_rows}
diffs = []
for name, rows in formats.items():
    assert len(rows) == 1008, (name, len(rows))
    assert [r['id'] for r in rows] == list(range(1, 1009)), name
    for expected, actual in zip(vocab, rows):
        for field in fields:
            if expected[field] != actual[field]:
                diffs.append({'format': name, 'id': expected['id'], 'field': field,
                              'json': expected[field], 'actual': actual[field]})


def duplicates(field, transform=lambda s: s):
    groups = defaultdict(list)
    for row in vocab:
        groups[transform(row[field])].append(row['id'])
    return {key: ids for key, ids in groups.items() if len(ids) > 1}


suspects, comparisons, covered = [], 0, set()
for row in vocab:
    for concept, words in EARTH_WORDS.items():
        if not re.search(r'\b' + re.escape(concept) + r'\b', row['meaningEn'].lower()):
            continue
        covered.add(row['id'])
        for word in sorted(set(words)):
            comparisons += 1
            distance = levenshtein(row['nrs'], word)
            substring = word in row['nrs'] or row['nrs'] in word
            if distance <= 2 or substring:
                suspects.append({'id': row['id'], 'nrs': row['nrs'], 'meaningEn': row['meaningEn'],
                                 'concept': concept, 'earth_word': word,
                                 'distance': distance, 'substring': substring})
prefixes = Counter(row['nrs'][:3] for row in vocab if len(row['nrs']) >= 3)
marked = [row for row in vocab if row['nrs'][-1] not in 'aeiouylrnms']
directions = [row for row in vocab if row['category'].startswith('16.') and row['pos'] == '副'
              and re.search(r'\b(?:eastward|westward|northward|southward|upwards?|downwards?|forward|backward|inward|outward|leftward|rightward)\b', row['meaningEn'])]
by_root = {row['nrs']: row for row in vocab}
direction_results = [{'id': row['id'], 'nrs': row['nrs'], 'meaningEn': row['meaningEn'],
                      'base_exists': row['nrs'].endswith('u') and row['nrs'][:-1] in by_root,
                      'base': by_root.get(row['nrs'][:-1])} for row in directions]
spec = read('docs/Project Requirements And Design.md')
grid = spec.split('### 6.1 ')[1].split('### 6.2 ')[0]
actual_grid = []
for line in grid.splitlines():
    if line.startswith('| **'):
        actual_grid.extend(re.findall(r'\*\*`([a-z]+)`\*\*', line))
expected_grid = [p+s for s in ['te', 'as', 'uo', 'hav', 'ku', 'zen']
                 for p in ['hi', 'ta', 'va', 'ka', 'sen', 'ni']]
corpus = spec.split('### 6.5 ')[1]
functional = set('el ia al en uo de to va ku fe se di ne nila ka ze na lo i sen zen tor hav mi ti ri'.split())
grid_words = set(actual_grid)


def analyze_token(token):
    if token in by_root:
        return {'type': 'dictionary', 'id': by_root[token]['id'], 'pos': by_root[token]['pos'],
                'meaningJa': by_root[token]['meaningJa']}
    if token in functional:
        return {'type': 'grammar'}
    if token in grid_words:
        return {'type': 'correlative'}
    candidates = []
    for prefix in ['', 're', 'co']:
        for suffix in ['', 'ast', 'in', 'ol', 'cor', 'el', 'i', 'u', 'as', 'or', 'ar']:
            if not prefix and not suffix:
                continue
            if token.startswith(prefix) and token.endswith(suffix):
                stem = token[len(prefix):len(token)-len(suffix) if suffix else None]
                check_bases = [stem]
                if suffix == 'ol':
                    check_bases.extend([stem + 'an', stem + 'en'])
                for base in check_bases:
                    if base in by_root:
                        candidates.append({'prefix': prefix, 'suffix': suffix, 'base': base,
                                           'base_id': by_root[base]['id'], 'pos': by_root[base]['pos']})
    return {'type': 'derivation_candidate' if candidates else 'unresolved', 'candidates': candidates}


texts = []
for label, sentence in re.findall(r'> \*\*(NRS|A|B)\*\*: `([^`]+)`', corpus):
    tokens = re.findall(r"[a-z']+", sentence.lower())
    texts.append({'label': label, 'sentence': sentence,
                  'tokens': [{'token': token, **analyze_token(token)} for token in tokens]})
font = TTFont(ROOT / 'fonts/Nebulith-Regular.ttf', checkChecksums=2)
font.ensureDecompiled()
cmap = font.getBestCmap()
binary = (ROOT / 'fonts/Nebulith-Regular.ttf').read_bytes()
font_evidence = {'tables': list(font.keys()), 'glyph_count': len(font.getGlyphOrder()),
                 'mapped_characters': len(cmap), 'characters': ''.join(map(chr, sorted(cmap))),
                 'cmap_formats': [t.format for t in font['cmap'].tables],
                 'unitsPerEm': font['head'].unitsPerEm,
                 'names': {str(i): font['name'].getDebugName(i) for i in [1, 2, 3, 4, 5, 6]},
                 'base64_equal': base64.b64decode(read('fonts/font_b64.txt'), validate=True) == binary,
                 'embedded_fonts': {}}
for path in ['fonts/preview.html', 'tools/num_specimen.html', 'fonts/punctuation.html', 'fonts/handwriting.html']:
    embedded = re.findall(r'base64,([A-Za-z0-9+/=]+)', read(path))
    font_evidence['embedded_fonts'][path] = [base64.b64decode(s) == binary for s in embedded]
required = ['head', 'hhea', 'maxp', 'OS/2', 'hmtx', 'cmap', 'loca', 'glyf', 'name', 'post']
font_evidence['missing_tables'] = [t for t in required if t not in font]

reviews = coda_review(vocab, json.loads(read('data/audit/coda_reviews.json')))
sourced = load_and_compare(vocab)
glyphs = glyph_review(font, hashlib.sha256(binary).hexdigest(), json.loads(read('data/audit/glyph_reviews.json')))
canon = json.loads(read('data/canon_corpus.json'))
corpus_errors = validate_corpus(canon, vocab)
corpus_pending = corpus_semantic_pending(canon)
ipa_errors = [r for r in vocab if normalize_ipa(r['ipa']) != expected_ipa(r['nrs'])]
generated = corpus_markdown(canon, vocab)
canon_start = spec.index('<!-- BEGIN GENERATED CANON -->')
canon_end = spec.index('<!-- END GENERATED CANON -->', canon_start) + len('<!-- END GENERATED CANON -->')
spec_sync = spec[canon_start:canon_end].strip() == generated.strip()
web = read('fonts/preview.html')
web_sync = all(u['nrs'] in web and u['translationJa'] in web for u in canon['units'])
category_counts = Counter(r['category'] for r in vocab)
category_errors = [c for c in data['categories'] if c['wordsCount'] != category_counts[c['name']]]
if set(category_counts) != {c['name'] for c in data['categories']}:
    category_errors.append({'error': 'category membership mismatch'})

result = {'timestamp_utc': datetime.now(timezone.utc).isoformat(),
          'commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
          'python': platform.python_version(), 'fonttools': fonttools_version,
          'manifest': manifest, 'format_counts': {k: len(v) for k, v in formats.items()},\
          'field_differences': diffs, 'category_counts': dict(Counter(r['category'] for r in vocab)),
          'category_metadata': data['categories'], 'category_metadata_errors': category_errors,
          'declared_total': data['totalEntries'],
          'invalid_nrs': [r for r in vocab if not re.fullmatch(r"[a-pr-wyz']+", r['nrs'])],
          'duplicate_roots': duplicates('nrs'), 'duplicate_ipa_raw': duplicates('ipa'),
          'duplicate_ipa_normalized': duplicates('ipa', normalize_ipa),
          'ipa_delimiters': dict(Counter('slashes' if r['ipa'].startswith('/') else 'brackets'
                                         if r['ipa'].startswith('[') else 'other' for r in vocab)),
          'c_or_j_ipa_mismatches': [r for r in vocab if ('c' in r['nrs'] and 'ʃ' not in r['ipa'])
                                   or ('j' in r['nrs'] and 'ʒ' not in r['ipa'])],
          'earth_coverage': {'concepts': len(EARTH_WORDS), 'word_forms': sum(map(len, EARTH_WORDS.values())),
                             'covered_entries': len(covered), 'comparisons': comparisons,
                             'uncovered_ids': sorted(set(by_root[r]['id'] for r in by_root)-covered)},
          'earth_candidates': suspects, 'earth_sourced': sourced, 'prefix_counts': prefixes.most_common(),
          'marked_codas': marked,
          'unmarked_or_vowel_rate': (len(vocab)-len(marked))/len(vocab),
          'marked_coda_exceptions_approved': len(reviews['approved']),
          'total_coda_compliance_rate': reviews['complianceRate'],
          'coda_reviews': reviews, 'glyph_reviews': glyphs,
          'ipa_mapping_mismatches': ipa_errors,
          'canon_validation': {'errors': corpus_errors, 'semantic_pending': corpus_pending,
                              'spec_sync': spec_sync, 'web_sync': web_sync},
          'directions': direction_results, 'correlatives': {'actual': actual_grid,
                        'matches_expected': actual_grid == expected_grid,
                        'dictionary_present': sorted(grid_words & by_root.keys())},
          'corpus': texts,
          'unresolved_corpus_tokens': [t['token'] for c in texts for t in c['tokens'] if t['type'] == 'unresolved'],
          'font': font_evidence}
checks = {}
def check(id_, ok, reason, pending=False):
    checks[id_] = {'status': 'Warn' if pending else 'Pass' if ok else 'Fail', 'reason': reason}
check('CHK-01', not result['invalid_nrs'], 'NRS character validation')
check('CHK-02', not result['duplicate_roots'], 'NRS uniqueness')
check('CHK-03', not result['duplicate_ipa_normalized'] and not result['duplicate_ipa_raw'], 'IPA uniqueness')
earth_ok = not sourced['confirmed'] and not sourced['errors']
check('CHK-04', earth_ok, f"Source-backed basic senses: {sourced['reviewed_entry_count']}/{len(vocab)} entries, {sourced['comparisons']} comparisons; {len(sourced['confirmed'])} confirmed, {len(sourced['ignored'])} ignored, {len(sourced['pending'])} pending. Distance alone never confirms a change; full scope incomplete. Legacy candidates are unreviewed diagnostics.", pending=earth_ok and (not sourced['scope_complete'] or bool(sourced['pending']) or bool(suspects)))
check('CHK-05', all(len(rows) == 1008 for rows in formats.values()) and not category_errors and data['totalEntries'] == 1008,
      'Four formats contain 1008 entries and category metadata matches')
check('CHK-06', not diffs, 'All eight fields match')
check('CHK-07', prefixes.most_common(1)[0][1] < 80, 'Largest prefix family <80')
checks['CHK-08'] = {'status': 'Reference', 'reason': 'Historical coda diagnostic retained; excluded from acceptance and rename triggers under the current user policy.',
                    'historicalThreshold': .95, 'historicalDiagnostic': 'Pass' if reviews['complete'] and reviews['complianceRate'] >= .95 else 'Fail' if reviews['complete'] else 'Warn'}
check('CHK-09', len(direction_results) == 14 and all(r['base_exists'] for r in direction_results), '14 directional adverb bases')
check('CHK-10', actual_grid == expected_grid, '36 correlative cells')
grammar_ok = all(s in spec for s in ['`-ast`', '`-in`', '`-ol`', '`-cor`', '`re-`', '`co-`']) and '起格 **`al`**' not in spec
check('CHK-11', grammar_ok, 'Declared aspect/voice and corrected case rules; broader semantic review is separate')
check('CHK-12', glyphs['complete'] and not glyphs['rejected'], 'Tiered design review: critical restructuring, minor conventional-symbol refinement, and separate functional checks; no universal originality or human handwriting certification', pending=not glyphs['complete'] and not glyphs['rejected'] and not glyphs['errors'])
inventory = json.loads(read('fonts/inventory.json'))
inventory_ok = (len(font.getGlyphOrder()) == inventory['glyphCount'] and len(cmap) == inventory['mappedCharacterCount']
                and ''.join(chr(c) for c in sorted(cmap)) == inventory['characters']
                and font_evidence['names']['5'] == 'Version '+inventory['fontVersion'])
check('CHK-13', not font_evidence['missing_tables'] and inventory_ok, 'TTF structure and versioned character inventory')
check('CHK-14', font_evidence['base64_equal'] and all(v and all(v) for v in font_evidence['embedded_fonts'].values()), 'Embedded font byte equality; live browser check is separate')
check('CHK-15', not corpus_errors and spec_sync and web_sync, 'Corpus references, source sync and semantic review',
      pending=not corpus_errors and spec_sync and web_sync and bool(corpus_pending))
result['scorecard'] = checks
result['scorecard_counts'] = dict(Counter(c['status'] for c in checks.values()))
from verify_web_bundle import verify as verify_web
result['web_bundle'] = verify_web()
if (batch_dir / 'comparison.json').exists():
    all_roots = json.loads((batch_dir/'comparison.json').read_text(encoding='utf-8'))
    assert all_roots['summary']['dictionarySha256'] == hashlib.sha256((ROOT/'data/lexicon.json').read_bytes()).hexdigest(), 'Stale all-roots comparison'
    assert {r['lexiconId'] for r in all_roots['entries']} == {r['id'] for r in vocab}, 'Incomplete all-roots inventory'
    result['all_roots_screening'] = all_roots['summary']
    result['all_roots_screening_note'] = 'Supplementary automatic screening. Unreviewed source senses do not grant CHK-04 approval.'
result['git_status'] = subprocess.check_output(['git', 'status', '--short'], cwd=ROOT, text=True)
result['supplementary_failures'] = {'ipa_mapping': len(ipa_errors), 'corpus_references': len(corpus_errors),
                                    'source_integrity': len(sourced['errors']),
                                    'spec_sync': not spec_sync, 'web_sync': not web_sync}
(OUT / 'evidence.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({'format_counts': result['format_counts'], 'field_differences': len(diffs),
                  'earth_candidates': len(suspects), 'marked_codas': len(marked),
                  'unresolved_tokens': len(result['unresolved_corpus_tokens']),
                  'total_coda_compliance_rate': result['total_coda_compliance_rate'],
                  'font_version': font_evidence['names'].get('5'),
                  'direction_pairs': len(directions)}, ensure_ascii=False, indent=2))
print('Evidence saved to:', OUT / 'evidence.json')
print('Scorecard:', result['scorecard_counts'])
print('Note: automatic results do not attest glyph originality or release approval.')
sys.exit(1 if any(c['status'] == 'Fail' for c in checks.values()) or ipa_errors else
         2 if any(c['status'] == 'Warn' for c in checks.values()) else 0)
