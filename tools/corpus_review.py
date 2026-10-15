"""Check the explicitly reviewed corpus frames and bind approvals to inputs."""
import json
import re
import hashlib
from nebulith_data import ROOT, entry_hash, reference, FUNCTIONAL, CORRELATIVES


def analyze_unit(unit, vocab, rules):
    roots = {r['nrs']: r for r in vocab}
    by_id = {r['id']: r for r in vocab}
    clauses, errors = [], []
    for text in re.split(r'[.,:!?]+', unit['nrs']):
        tokens = re.findall(r"[a-z']+", text.lower())
        if not tokens:
            continue
        question = tokens[-1]=='ka'
        if question:tokens.pop()
        prefixes = []
        while tokens and tokens[0] in rules['prefixes']:
            prefixes.append(tokens.pop(0))
        if not tokens:
            errors.append('missing predicate')
            continue
        predicate = tokens.pop(0)
        ref = reference(predicate, roots)
        id_ = ref.get('lexiconId', ref.get('stemId'))
        frame = rules['frames'].get(str(id_))
        if not frame or '動' not in by_id.get(id_, {}).get('pos', ''):
            errors.append('unsupported predicate: '+predicate)
            continue
        groups, case = {}, None
        for token in tokens:
            if token in rules['cases']:
                if token in groups:
                    errors.append('duplicate case: '+token)
                case = token
                groups[case] = []
            elif case is None:
                errors.append('unmarked argument: '+token)
            else:
                groups[case].append(token)
        allowed = frame.get('passiveAllowed', []) if ref.get('prefix') == 're' else frame['allowed']
        if set(frame['required'])-groups.keys() or set(groups)-set(allowed):
            errors.append('argument frame mismatch: '+predicate)
        for case, words in groups.items():
            if not words:
                errors.append('empty case: '+case)
                continue
            head = words[0]
            head_ref = reference(head, roots)
            entry = by_id.get(head_ref.get('lexiconId', head_ref.get('stemId')))
            if entry and '名' not in entry['pos'] and not (case == 'ia' and id_ == 906 and '形' in entry['pos']):
                errors.append('non-nominal argument: '+head)
            elif not entry and head not in CORRELATIVES and head not in ['mi', 'ti', 'ri']:
                errors.append('unsupported argument head: '+head)
        clauses.append({'text': text.strip(), 'predicate': predicate, 'lexiconId': id_,
                        'question':question,
                        'sense': frame['sense'], 'prefixes': prefixes, 'voice': ref.get('prefix') or 'active',
                        'aspect': ref.get('suffix') or 'unmarked', 'arguments': groups})
    return {'clauses': clauses, 'errors': errors}


def dependency_hash(unit, vocab=None, rules=None):
    if vocab is None:
        vocab = json.loads((ROOT / 'data/lexicon.json').read_text(encoding='utf-8'))['vocabulary']
    if rules is None:
        rules = json.loads((ROOT / 'data/corpus_rules.json').read_text(encoding='utf-8'))
    ids = {t.get('lexiconId', t.get('stemId')) for t in unit['tokens']}
    entries = [r for r in vocab if r['id'] in ids]
    specification = (ROOT / 'docs/Project Requirements And Design.md').read_text(encoding='utf-8').split('<!-- BEGIN GENERATED CANON -->')[0]
    return entry_hash({'entries': entries, 'rules': rules, 'specification': specification,
                       'analyzerSha256':hashlib.sha256((ROOT/'tools/corpus_review.py').read_bytes()).hexdigest()})
