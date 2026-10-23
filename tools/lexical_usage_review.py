"""Validate source-bound usage proposals without promoting them to canon."""
import json
from pathlib import Path

SOURCE_FIELDS = ('id', 'nrs', 'pos', 'meaningJa', 'meaningEn', 'morphemes',
                 'etymology', 'example_sentence', 'example_ja', 'scenario_id')


def validate_usage_reviews(document, compounds, constituents=None, rules=None):
    if document.get('schemaVersion') != 1:
        raise ValueError('Unsupported lexical usage review schema')
    by_id = {entry['id']: entry for entry in compounds['entries']}
    seen = set()
    for row in document['entries']:
        ident = row['id']
        if ident in seen or ident not in by_id:
            raise ValueError(f'Duplicate or unknown usage review ID: {ident}')
        seen.add(ident)
        source = {key: by_id[ident][key] for key in SOURCE_FIELDS}
        if row['source'] != source or row['root'] != source['nrs']:
            raise ValueError(f'Usage review source changed; re-review required: {ident}')
        if row['status'] != 'proposal' or row.get('approved') is not False:
            raise ValueError(f'Usage proposals cannot grant canon approval: {ident}')
        if row['usage'] not in ('held', 'attributive_only', 'frame_proposal'):
            raise ValueError(f'Unknown usage boundary: {ident}')
        if not all(row.get(key) for key in ('issue', 'proposal', 'acceptance', 'userNote')):
            raise ValueError(f'Incomplete usage review: {ident}')
        decision = row.get('decision', {})
        if (decision.get('outcome') not in ('held-for-reformation', 'app-frame-only')
                or decision.get('canonicalChange') is not False
                or decision.get('independentApproval') is not False
                or not decision.get('reason') or not decision.get('nextAction')):
            raise ValueError(f'Invalid application decision: {ident}')
        expected_usage = 'held' if decision['outcome'] == 'held-for-reformation' else 'frame_proposal'
        if row['usage'] != expected_usage:
            raise ValueError(f'Decision and usage boundary disagree: {ident}')
        if row['usage'] == 'held':
            reform = row.get('reformation', {})
            if (reform.get('status') != 'proposal' or reform.get('automaticReplacement') is not False
                    or not all(reform.get(key) for key in ('plan', 'unresolved', 'related'))):
                raise ValueError(f'Incomplete reformation proposal: {ident}')
            related = reform['related']
            if len({entry['root'] for entry in related}) != len(related) or any(not entry.get('difference') for entry in related):
                raise ValueError(f'Invalid related meaning boundaries: {ident}')
        if constituents is not None:
            by_root = {entry['nrs']: entry for entry in constituents}
            fields = ('id', 'nrs', 'pos', 'meaningJa', 'meaningEn')
            expected = [{key: by_root[m][key] for key in fields} for m in source['morphemes']]
            if row.get('constituents') != expected:
                raise ValueError(f'Constituent source changed; re-review required: {ident}')
            for entry in row.get('reformation', {}).get('related', []):
                current = by_root.get(entry['root'])
                if current is None or entry['source'] != {key: current[key] for key in fields}:
                    raise ValueError(f'Related word source changed; re-review required: {ident}')
    if rules is not None:
        held = {row['id'] for row in document['entries'] if row['usage'] == 'held'}
        if held != {row['id'] for row in rules['held']}:
            raise ValueError('Usage decisions and held translation rules disagree')
        if held.intersection(row['id'] for row in rules['adjectives']):
            raise ValueError('Held decisions cannot remain active adjective rules')
    return len(seen)


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    read = lambda name: json.loads((root / 'data' / name).read_text(encoding='utf-8'))
    count = validate_usage_reviews(read('lexical_usage_reviews.json'), read('verified_canonical_compounds.json'),
                                  read('lexicon.json')['vocabulary'], read('roadmap_lexical_rules.json'))
    print(f'{count} source-bound application decisions validated; no approval granted')
