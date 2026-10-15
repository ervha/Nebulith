"""Audit source-backed concept links without turning partial coverage into Pass."""
import hashlib
import json
from collections import defaultdict
from nebulith_data import ROOT, entry_hash
from false_friend_detector import levenshtein
from import_swadesh_comparison import normalize_form
from earth_scope import coverage


def candidate_key(row):
    return '|'.join(str(row[k]) for k in ['lexiconId', 'nrs', 'conceptId', 'language', 'sourceForm'])


def compare(vocab, registry, rows, links, reviews=None, scope_policy=None, scope_reviews=None):
    by_id = {r['id']: r for r in vocab}
    indexed = defaultdict(list)
    errors, suspects, covered = [], [], set()
    sources = {r['id']: r for r in registry['sources']}
    for source in sources.values():
        path = ROOT / source['snapshot']
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != source['sha256']:
            errors.append('source snapshot hash mismatch: '+source['id'])
    for row in rows:
        if row['sourceId'] not in sources or row['comparisonForm'] != normalize_form(row['sourceForm']):
            errors.append('invalid source form: '+row['conceptId'])
        indexed[(row['conceptId'], row['language'])].append(row)
    comparisons = 0
    partially_covered = set()
    for link in links['entries']:
        entry = by_id.get(link['lexiconId'])
        if link['decision'] != 'approved':
            continue
        if entry is None or link['reviewedAgainstEntryHash'] != entry_hash(entry) or not link.get('reviewer') or not link.get('reason'):
            errors.append('stale or unsubstantiated concept link: '+str(link['lexiconId']))
            continue
        languages = 0
        for language in registry['requiredLanguages']:
            matching = indexed[(link['conceptId'], language)]
            if matching:
                languages += 1
            for row in matching:
                a, b = entry['nrs'], row['comparisonForm']
                distance = levenshtein(a, b)
                substring = a in b or b in a
                comparisons += 1
                if distance <= 2 or substring:
                    suspects.append({'lexiconId': entry['id'], 'nrs': a, 'conceptId': link['conceptId'],
                                     'language': language, 'sourceForm': row['sourceForm'], 'comparisonForm': b,
                                     'sourceId': row['sourceId'], 'distance': distance, 'substring': substring})
        if languages == len(registry['requiredLanguages']):
            covered.add(entry['id'])
        if languages:partially_covered.add(entry['id'])
    decisions = {}
    for review in (reviews or {}).get('entries', []):
        key = review['candidateKey']
        if key in decisions:
            errors.append('duplicate candidate review: '+key)
        decisions[key] = review
    confirmed, ignored, pending = [], [], []
    for candidate in suspects:
        review = decisions.get(candidate_key(candidate))
        if not review:
            pending.append(candidate)
            continue
        entry = by_id[candidate['lexiconId']]
        if review.get('entryHash') != entry_hash(entry) or not review.get('reviewer') or not review.get('reason'):
            errors.append('stale or unsubstantiated candidate review: '+candidate_key(candidate))
            pending.append(candidate)
        elif review.get('decision') == 'change' and review.get('meaningSimilar') is True and review.get('formSimilar') is True:
            confirmed.append(candidate)
        elif review.get('decision') == 'ignore' and (review.get('meaningSimilar') is False or review.get('formSimilar') is False):
            ignored.append(candidate)
        else:
            errors.append('decision does not satisfy both-meaning-and-form policy: '+candidate_key(candidate))
            pending.append(candidate)
    full=coverage(vocab,rows,links,scope_policy or {'requiredLanguages':registry['requiredLanguages'],'minimumComparisonForms':2000},scope_reviews or {'entries':[]})
    return {'comparison_forms': len(rows), 'reviewed_entry_count': len(covered),'partially_reviewed_entry_count':len(partially_covered),
            'unmapped_ids': sorted(by_id.keys()-covered), 'comparisons': comparisons,
            'candidates': suspects, 'confirmed': confirmed, 'ignored': ignored, 'pending': pending,
            'errors': errors, 'scope_complete': full['scopeComplete'] and not errors, 'full_sense_coverage':full,
            'scope_note': '出典付きの基本語義の限定照合。全語義・監査母集団の充足を保証しない。'}


def load_and_compare(vocab):
    registry = json.loads((ROOT / 'data/audit/earth_sources.json').read_text(encoding='utf-8'))
    rows = [json.loads(s) for s in (ROOT / 'data/audit/earth_lexicon.jsonl').read_text(encoding='utf-8').splitlines()]
    links = json.loads((ROOT / 'data/audit/earth_concept_links.json').read_text(encoding='utf-8'))
    path = ROOT / 'data/audit/earth_candidate_reviews.json'
    reviews = json.loads(path.read_text(encoding='utf-8')) if path.exists() else None
    batch_path=ROOT/'data/audit/earth_research_batch_01.json'
    if batch_path.exists():
        batch=json.loads(batch_path.read_text(encoding='utf-8'))
        sources={r['id']:r for r in registry['sources']}
        for entry in batch['entries']:
            for sense in entry['senses']:
                if sense['status']!='partial-source-backed':continue
                source=sense['source'];sources[source['id']]=source
                concept=source['id']
                for language,form in sense['translations'].items():
                    rows.append({'conceptId':concept,'language':language,'sourceId':source['id'],
                                 'sourceForm':form,'comparisonForm':normalize_form(form)})
                links['entries'].append({'lexiconId':entry['lexiconId'],'conceptId':concept,'decision':'approved',
                   'reviewedAgainstEntryHash':entry['entryHash'],'reviewer':entry['reviewer'],'reason':sense['mappingReview']})
        registry['sources']=list(sources.values())
        rows=list({(r['conceptId'],r['language'],r['comparisonForm']):r for r in rows}.values())
    policy=json.loads((ROOT/'data/audit/earth_scope_policy.json').read_text(encoding='utf-8'))
    scope_reviews=json.loads((ROOT/'data/audit/earth_scope_reviews.json').read_text(encoding='utf-8'))
    return compare(vocab, registry, rows, links, reviews,policy,scope_reviews)
