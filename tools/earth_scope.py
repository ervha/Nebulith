"""Evidence-derived full-sense coverage; partial links can never certify the scope."""
import re
from collections import defaultdict
from nebulith_data import entry_hash


def senses(entry):
    return {'en:'+x.strip().casefold() for x in entry['meaningEn'].split(',') if x.strip()} | {
            'ja:'+x.strip() for x in re.split('[、／]',entry['meaningJa']) if x.strip()}


def coverage(vocab,rows,links,policy,reviews):
    languages=set(policy['requiredLanguages'])
    available=defaultdict(set)
    for row in rows:available[row['conceptId']].add(row['language'])
    linked=defaultdict(dict)
    for row in links['entries']:
        if row.get('decision')=='approved':linked[row['lexiconId']][row['conceptId']]=row
    reviewed={r['lexiconId']:r for r in reviews.get('entries',[])}
    complete=[]
    for entry in vocab:
        r=reviewed.get(entry['id'],{})
        if (r.get('decision')!='approved' or r.get('entryHash')!=entry_hash(entry)
                or not r.get('reviewer') or not r.get('reason')):continue
        checked=set()
        for sense in r.get('senses',[]):
            concepts=sense.get('conceptIds',[])
            if concepts and all(c in linked[entry['id']] and languages<=available[c]
                    and sense['label'] in linked[entry['id']][c].get('reviewedSenses',[]) for c in concepts):
                checked.add(sense['label'])
        if senses(entry)<=checked:complete.append(entry['id'])
    unique_forms=len({(r['conceptId'],r['language'],r['comparisonForm']) for r in rows})
    return {'fullSenseEntries':len(complete),'unreviewedSenseEntryIds':sorted({r['id'] for r in vocab}-set(complete)),
            'uniqueForms':unique_forms,'minimumForms':policy['minimumComparisonForms'],
            'scopeComplete':len(complete)==len(vocab) and unique_forms>=policy['minimumComparisonForms']}
