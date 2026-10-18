"""Reject incomplete examples before they can become exact-match translations."""
import re


def validate_examples(rows, vocabulary):
    # Historical corpus forms documented by EXT-06/17/18/21.
    roots = {r['nrs'].lower() for r in vocabulary} | {'mia', 'keli', 'kelen'}
    seen = set()
    for row in rows:
        if not all(isinstance(row.get(k), str) and row[k].strip() for k in ['id', 'japanese', 'nebulith']):
            raise ValueError('Incomplete extended example: ' + str(row.get('id')))
        variants = row.get('japanese_variants')
        if not isinstance(variants, list) or not variants or any(not isinstance(v, str) or not v.strip() for v in variants):
            raise ValueError('Missing Japanese variants: ' + row['id'])
        if row['id'] in seen:
            raise ValueError('Duplicate extended example: ' + row['id'])
        seen.add(row['id'])
        unknown = set(re.findall(r"[a-z']+", row['nebulith'].lower())) - roots
        if unknown:
            raise ValueError('Undefined extended example tokens: ' + row['id'] + ': ' + ', '.join(sorted(unknown)))
