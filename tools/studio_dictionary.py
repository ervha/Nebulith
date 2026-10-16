"""Studio search dictionary: approved roots plus documented grammar entries."""
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def dictionary_entries(vocabulary):
    entries = copy.deepcopy(vocabulary)
    grammar = json.loads((ROOT / 'data/grammar_dictionary.json').read_text(encoding='utf-8'))['entries']
    grammar += json.loads((ROOT / 'data/translation_extensions.json').read_text(encoding='utf-8'))['entries']
    by_root = {e['nrs']: e for e in entries}
    ids = {e['id'] for e in entries}
    for row in grammar:
        if row['nrs'] in by_root:
            # Keep existing IDs/favorites and expose both senses in one card.
            entry = by_root[row['nrs']]
            for field in ('pos', 'meaningJa', 'meaningEn', 'notes'):
                entry[field] += (' / ' if field == 'pos' else '、' if field == 'meaningJa' else '; ') + row[field]
        else:
            if row['id'] in ids:
                raise ValueError(f"Duplicate dictionary ID: {row['id']}")
            entries.append(copy.deepcopy(row))
            by_root[row['nrs']] = entries[-1]
            ids.add(row['id'])
    patterns = json.loads((ROOT / 'data/translation_patterns.json').read_text(encoding='utf-8'))
    for alias, root in patterns.get('pronounAliases', {}).items():
        by_root[root]['notes'] += ' 日本語入力の表記：' + alias + '。'
    by_id = {e['id']: e for e in entries}
    for verb in patterns.get('verbs', []):
        entry = by_id[verb['id']]
        if verb['lemma'] not in entry['meaningJa']:
            entry['notes'] += ' 対応する日本語動詞：' + verb['lemma'] + '。'

    # Attach canonical scripture loci from Codex Astrolith
    loci_file = ROOT / 'data/lexicon_canonical_loci.json'
    if loci_file.exists():
        loci_map = json.loads(loci_file.read_text(encoding='utf-8'))
        for root, locus in loci_map.items():
            if root in by_root:
                by_root[root]['notes'] += f' 【聖典原典】{locus}。'

    return entries
