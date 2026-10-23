"""Validate source-bound usage proposals without promoting them to canon."""
import json
from pathlib import Path

SOURCE_FIELDS = ('id', 'nrs', 'pos', 'meaningJa', 'meaningEn', 'morphemes',
                 'etymology', 'example_sentence', 'example_ja', 'scenario_id')


def validate_usage_reviews(document, compounds):
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
    return len(seen)


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    read = lambda name: json.loads((root / 'data' / name).read_text(encoding='utf-8'))
    count = validate_usage_reviews(read('lexical_usage_reviews.json'), read('verified_canonical_compounds.json'))
    print(f'{count} source-bound usage proposals validated; no approval granted')
