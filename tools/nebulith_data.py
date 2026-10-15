"""Shared deterministic exports and explicit corpus-reference validation."""
import csv
import io
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ['id', 'category', 'nrs', 'ipa', 'pos', 'meaningJa', 'meaningEn', 'notes']
FUNCTIONAL = set('el ia al en uo de to va ku fe se di ne nila ka ze na lo i sen zen tor hav mi ti ri'.split())
CORRELATIVES = {p+s for p in ['hi', 'ta', 'va', 'ka', 'sen', 'ni']
                for s in ['te', 'as', 'uo', 'hav', 'ku', 'zen']}


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def normalize_ipa(value):
    return re.sub(r'[\[\]/.\s]', '', value).replace('ɾ', 'r')


def expected_ipa(nrs):
    for a, b in [('ai', 'aɪ'), ('ei', 'eɪ'), ('au', 'aʊ'), ('oi', 'ɔɪ'),
                 ('c', 'ʃ'), ('j', 'ʒ'), ("'", 'ʔ')]:
        nrs = nrs.replace(a, b)
    return nrs


def entry_hash(entry):
    import hashlib
    return hashlib.sha256(json.dumps(entry, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def corpus_semantic_pending(corpus, vocab=None, rules=None):
    """An approval must identify its reviewer and the exact reviewed unit."""
    pending = []
    from corpus_review import dependency_hash, analyze_unit
    if vocab is None:
        vocab = json.loads((ROOT / 'data/lexicon.json').read_text(encoding='utf-8'))['vocabulary']
    if rules is None:
        rules = json.loads((ROOT / 'data/corpus_rules.json').read_text(encoding='utf-8'))
    for unit in corpus['units']:
        review = unit.get('review', {})
        unit_content = {k: v for k, v in unit.items() if k != 'review'}
        if (review.get('status') != 'approved' or not review.get('reviewer') or not review.get('note')
                or review.get('reviewedAgainstUnitHash') != entry_hash(unit_content)
                or review.get('reviewedAgainstDependenciesHash') != dependency_hash(unit, vocab, rules)
                or analyze_unit(unit, vocab, rules)['errors']):
            pending.append(unit['id'])
    return pending


def export_lexicon(data):
    """Generate the other three formats from JSON without changing IDs or meanings."""
    vocab = data['vocabulary']
    counts = Counter(r['category'] for r in vocab)
    for category in data['categories']:
        category['wordsCount'] = counts[category['name']]
    data['totalEntries'] = len(vocab)
    dump(ROOT / 'data/lexicon.json', data)
    buf = io.StringIO(newline='')
    writer = csv.DictWriter(buf, fieldnames=FIELDS, lineterminator='\n')
    writer.writeheader()
    writer.writerows({k: row[k] for k in FIELDS} for row in vocab)
    (ROOT / 'data/lexicon.csv').write_bytes(buf.getvalue().encode())
    version = data['version']
    kt = ['package com.nebulith.data', '', '/** Generated from lexicon.json; audit status is recorded separately. */',
          'data class LexiconEntry(', *[f'    val {key}: {"Int" if key == "id" else "String"},' for key in FIELDS],
          ')', '', 'object StaticLexicon {', f'    const val VERSION = "{version}"',
          f'    const val TOTAL_ENTRIES = {len(vocab)}', '    val entries: List<LexiconEntry> = listOf(']
    for row in vocab:
        values = [str(row['id'])]+[json.dumps(row[k], ensure_ascii=False).replace('$', '\\$') for k in FIELDS[1:]]
        kt.append('        LexiconEntry(' + ', '.join(values) + '),')
    (ROOT / 'data/StaticLexicon.kt').write_text('\n'.join(kt+['    )', '}'])+'\n', encoding='utf-8')
    md = ['# Nebulith Master Lexicon (星石語 統御語彙大系)', '',
          f'> **Version**: {version} (1,008 Master Roots across 16 Categories)',
          '> **Audit status**: 修正中。監査記録は [audit/README.md](../audit/README.md) を参照。', '',
          '## 16-Domain Category Overview (全16領域構成)', '',
          '| ID | カテゴリー名 (Domain) | 語彙数 (Words) | 構成比 | 概要 |', '|---|---|---|---|---|']
    for c in data['categories']:
        md.append(f"| {c['id']} | **{c['name']}** | {c['wordsCount']}語 | {c['wordsCount']/len(vocab):.1%} | {c['description']} |")
    md += ['', '## 語彙目録 (Master Vocabulary Entries - 1,008 Roots)', '']
    current = None
    for row in vocab:
        if row['category'] != current:
            current = row['category']
            md += [f'### {current} ({counts[current]}語)', '',
                   '| ID | 語根 (NRS) | IPA | 品詞 | 日本語意味 | 英語意味 | 語源・備考 |', '|---|---|---|---|---|---|---|']
        md.append(f"| {row['id']} | **{row['nrs']}** | `{row['ipa']}` | {row['pos']} | {row['meaningJa']} | {row['meaningEn']} | {row['notes']} |")
    (ROOT / 'docs/Nebulith Master Lexicon.md').write_text('\n'.join(md)+'\n', encoding='utf-8')


def apply_recipe(stem, prefix, suffix):
    if suffix == 'ol':
        if stem.endswith(('an', 'en')):
            stem = stem[:-2]
        elif stem[-1] in 'aeiouy':
            stem = stem[:-1]
    return prefix + stem + suffix


def reference(token, by_root):
    if token in by_root:
        return {'kind': 'dictionary', 'lexiconId': by_root[token]['id']}
    if token in FUNCTIONAL:
        return {'kind': 'grammar', 'rule': token}
    if token in CORRELATIVES:
        return {'kind': 'correlative', 'rule': token}
    for prefix in ['', 're', 'co']:
        for suffix in ['', 'ast', 'in', 'ol', 'cor', 'el', 'i', 'u', 'as', 'or', 'ar']:
            if not prefix and not suffix:
                continue
            for stem in by_root:
                if apply_recipe(stem, prefix, suffix) == token:
                    return {'kind': 'derivation', 'stemId': by_root[stem]['id'], 'prefix': prefix, 'suffix': suffix}
    return {'kind': 'unresolved'}


def validate_corpus(corpus, vocab):
    by_id = {r['id']: r for r in vocab}
    errors = []
    for unit in corpus['units']:
        surface = re.findall(r"[a-z']+", unit['nrs'].lower())
        if surface != [t['surface'] for t in unit['tokens']]:
            errors.append({'unit': unit['id'], 'error': 'token text mismatch'})
        if len({t['id'] for t in unit['tokens']}) != len(unit['tokens']):
            errors.append({'unit': unit['id'], 'error': 'duplicate token ID'})
        for t in unit['tokens']:
            kind = t.get('kind')
            if kind == 'dictionary':
                valid = by_id.get(t.get('lexiconId'), {}).get('nrs') == t['surface']
            elif kind == 'derivation':
                stem = by_id.get(t.get('stemId'), {}).get('nrs')
                valid = stem is not None and apply_recipe(stem, t['prefix'], t['suffix']) == t['surface']
                if t['prefix'] or t['suffix'] in ['ast', 'ol', 'cor']:
                    valid = valid and '動' in by_id.get(t.get('stemId'), {}).get('pos', '')
            elif kind == 'grammar':
                valid = t.get('rule') == t['surface'] and t['surface'] in FUNCTIONAL
            elif kind == 'correlative':
                valid = t.get('rule') == t['surface'] and t['surface'] in CORRELATIVES
            else:
                valid = False
            if not valid:
                errors.append({'unit': unit['id'], 'token': t['id'], 'error': 'invalid reference or derivation'})
    return errors


def corpus_markdown(corpus, vocab):
    by_id = {r['id']: r for r in vocab}
    lines = ['<!-- BEGIN GENERATED CANON -->', '### 6.5 公式規範コーパス集（Nebulith Canon Corpus）', '',
             '本文・和訳・参照は `data/canon_corpus.json` から生成。字句整合と意味・統語の審査を区別し、未審査を適合済みとしない。', '']
    for unit in corpus['units']:
        lines += [f"#### {unit['title']}", f"> **{unit['label']}**: `{unit['nrs']}`", f"> **日本語訳**: {unit['translationJa']}",
                  f"> **意味・統語審査**: {unit['review']['status']} — {unit['review']['note']}", '> **逐語参照**:']
        for t in unit['tokens']:
            if t['kind'] == 'dictionary':
                r = by_id[t['lexiconId']]
                desc = f"ID {r['id']} / {r['pos']} / {r['meaningJa']}"
            elif t['kind'] == 'derivation':
                r = by_id[t['stemId']]
                desc = f"語幹ID {r['id']} {r['nrs']} + prefix={t['prefix'] or '∅'}, suffix={t['suffix'] or '∅'}"
            else:
                desc = f"{t['kind']} / 規則 {t.get('rule', '未解決')}"
            lines.append(f"> - `{t['surface']}` ({desc})")
        lines.append('')
    return '\n'.join(lines+['<!-- END GENERATED CANON -->', ''])
