"""Exhaustive ID inventory and source-backed, sense-labelled translation screening.

No automatic semantic approvals: an English lookup is a retrieval key, not proof
that every translation sense is the intended Japanese/Nebulith meaning.
Uses only stdlib; snapshots allow an offline, deterministic replay.
"""
import argparse
import csv
import hashlib
import json
import re
import time
import urllib.parse
import urllib.request
from collections import Counter

from nebulith_data import ROOT, dump, entry_hash
from import_swadesh_comparison import normalize_form
from false_friend_detector import levenshtein
from earth_comparison import load_and_compare

LANGUAGES = ['en', 'la', 'fr', 'es', 'de', 'ja']
RUN = ROOT / 'audit/runs/2026-10-15-all-roots'
API = 'https://en.wiktionary.org/w/api.php'


def english_senses(entry):
    return list(dict.fromkeys(s.strip().lower() for s in entry['meaningEn'].split(',') if s.strip()))


def clean(value):
    value = re.sub(r'\[\[(?:[^]|]+\|)?([^]]+)\]\]', r'\1', value)
    return value.replace("''", '').strip()


def translation_rows(text):
    """Keep English section, translation-table sense and POS; never other languages.

    Deliberately exclude translation-check templates and unexpanded nested terms.
    Japanese comparison uses only explicitly supplied Latin-script tr= variants.
    """
    section = re.search(r'^==English==\s*$(.*?)(?=^==[^=]|\Z)', text, re.M | re.S)
    if not section:
        return []
    body = section[1]
    rows = []
    for block in re.finditer(r'\{\{trans-top(?:-also|-see)?\|([^{}]*?)\}\}(.*?)\{\{trans-bottom\}\}', body, re.S):
        gloss = clean(block[1].split('|')[0])
        headings = re.findall(r'^={3,5}([^=\n]+)={3,5}\s*$', body[:block.start()], re.M)
        pos = next((h for h in reversed(headings) if h in ['Noun','Verb','Adjective','Adverb','Pronoun','Preposition','Conjunction','Interjection','Numeral','Determiner','Proper noun']), 'unknown')
        for match in re.finditer(r'\{\{(tt?\+?)\|(la|fr|es|de|ja)\|([^{}]+?)\}\}', block[2]):
            parts = match[3].split('|')
            native = clean(parts[0])
            params = dict(p.split('=', 1) for p in parts[1:] if '=' in p)
            forms = [clean(params.get('alt', native))]
            if match[2] == 'ja':
                forms = [clean(x) for x in re.split('[,;]', params.get('tr', ''))]
            for form in forms:
                if not form or not re.fullmatch(r"[\w\s'’\-]+", form, re.UNICODE):
                    continue
                if not all(ord(c) < 0x250 or not c.isalpha() for c in form):
                    continue
                rows.append({'language':match[2], 'sourceForm':form, 'nativeForm':native,
                             'comparisonForm':normalize_form(form), 'sourceSense':gloss, 'sourcePos':pos})
    return list({tuple(sorted(r.items())):r for r in rows}.values())


def fetch_batch(item):
    number, titles = item
    target = RUN / 'sources' / f'batch-{number:03d}.json'
    params = {'action':'query','prop':'revisions','rvprop':'ids|timestamp|content',
              'rvslots':'main','titles':'|'.join(titles),'redirects':'1',
              'format':'json','formatversion':'2','maxlag':'5'}
    url = API + '?' + urllib.parse.urlencode(params)
    if not target.exists():
        time.sleep(3)
        for attempt in range(3):
            try:
                request = urllib.request.Request(url, headers={'User-Agent':'NebulithLexicalAudit/1.0 (source-attributed local linguistic research)'})
                raw = urllib.request.urlopen(request, timeout=45).read()
                payload = json.loads(raw)
                if 'error' in payload:
                    raise ValueError(str(payload['error']))
                target.write_bytes(raw)
                break
            except Exception as exc:
                # Respect the server's rate limit. Do not continue a blocked
                # batch by hammering the remaining titles.
                if getattr(exc, 'code', None) == 429:
                    retry = exc.headers.get('Retry-After','')
                    if retry.isdigit() and int(retry) <= 55 and attempt < 2:
                        print('Server rate limit; waiting '+retry+' seconds before retry', flush=True)
                        time.sleep(int(retry) + 2)
                        continue
                    return {'batch':number, 'titles':titles, 'url':url, 'error':str(exc),
                            'retryAfter':retry or 'unspecified'}
                if attempt == 2:
                    return {'batch':number, 'titles':titles, 'url':url, 'error':str(exc)}
                time.sleep(2 * (attempt + 1))
    return {'batch':number,'titles':titles,'url':url,'snapshot':target.relative_to(ROOT).as_posix(),
            'sha256':hashlib.sha256(target.read_bytes()).hexdigest()}


def near(a, b):
    d = levenshtein(a, b)
    substring = a in b or b in a
    return d <= 2 or substring, d, substring


def analyze(vocab, sources):
    pages, lookup = {}, {}
    for source in sources:
        if 'error' in source:
            continue
        path = ROOT / source['snapshot']
        if hashlib.sha256(path.read_bytes()).hexdigest() != source['sha256']:
            raise ValueError('Snapshot hash mismatch: '+str(path))
        payload = json.loads(path.read_text(encoding='utf-8'))['query']
        aliases = {r['from']:r['to'] for key in ['normalized','redirects'] for r in payload.get(key,[])}
        batch_pages = {p['title']:p for p in payload['pages']}
        for title in source['titles']:
            resolved, visited = title, set()
            while resolved in aliases and resolved not in visited:
                visited.add(resolved); resolved = aliases[resolved]
            p = batch_pages.get(resolved, {})
            lookup[title] = resolved if p.get('revisions') else None
        for title, page in batch_pages.items():
            if not page.get('revisions'):
                continue
            rev = page['revisions'][0]
            pages[title] = {'title':title,'revisionId':rev['revid'], 'timestamp':rev['timestamp'],
                            'url':'https://en.wiktionary.org/w/index.php?oldid='+str(rev['revid']),
                            'snapshot':source['snapshot'], 'rows':translation_rows(rev['slots']['main']['content'])}
    entries, candidates = [], []
    for entry in vocab:
        comparisons = Counter(); sense_records = []
        for sense in english_senses(entry):
            found, distance, substring = near(normalize_form(entry['nrs']), normalize_form(sense))
            comparisons['en'] += 1
            if found:
                candidates.append({'lexiconId':entry['id'],'nrs':entry['nrs'],'meaningJa':entry['meaningJa'],
                    'querySense':sense,'language':'en','sourceForm':sense,'sourceSense':sense,'sourcePos':'dictionary gloss',
                    'source':'data/lexicon.json','distance':distance,'substring':substring,'semanticStatus':'dictionary-gloss-correspondence'})
            title = lookup.get(sense)
            page = pages.get(title, {})
            rows = page.get('rows', [])
            counts = Counter(r['language'] for r in rows)
            for row in rows:
                comparisons[row['language']] += 1
                found, distance, substring = near(normalize_form(entry['nrs']), row['comparisonForm'])
                if found:
                    candidates.append({'lexiconId':entry['id'],'nrs':entry['nrs'],'meaningJa':entry['meaningJa'],
                        'querySense':sense,**row,'source':page['url'],'distance':distance,'substring':substring,
                        'semanticStatus':'source-sense-review-required'})
            sense_records.append({'label':'en:'+sense,'page':title,'source':page.get('url'),
                'status':'translation-tables-retrieved' if rows else 'page-without-extracted-tables' if page else 'page-unavailable',
                'translationCounts':dict(counts),'missingLanguages':[l for l in LANGUAGES[1:] if not counts[l]]})
        entries.append({'lexiconId':entry['id'],'nrs':entry['nrs'],'entryHash':entry_hash(entry),
                        'meaningJa':entry['meaningJa'],'meaningEn':entry['meaningEn'],
                        'comparisonCounts':{l:comparisons[l] for l in LANGUAGES},'senses':sense_records,
                        'japaneseGlossReview':'Japanese-only listed senses still require individual semantic mapping',
                        'status':'screened-not-semantically-certified'})
    candidates = list({json.dumps(c,sort_keys=True,ensure_ascii=False):c for c in candidates}.values())
    return entries, candidates, pages


def main():
    parser = argparse.ArgumentParser();parser.add_argument('--offline', action='store_true');args=parser.parse_args()
    vocab = json.loads((ROOT/'data/lexicon.json').read_text(encoding='utf-8'))['vocabulary']
    RUN.mkdir(parents=True,exist_ok=True);(RUN/'sources').mkdir(exist_ok=True)
    titles = sorted({s for entry in vocab for s in english_senses(entry)})
    if args.offline:
        sources = json.loads((RUN/'sources.json').read_text(encoding='utf-8'))['batches']
        if sorted(s for b in sources for s in b['titles']) != titles:
            raise ValueError('Source lookup inventory differs from current dictionary')
    else:
        batches = [(i//50+1,titles[i:i+50]) for i in range(0,len(titles),50)]
        sources = []
        blocked = None
        for batch in batches:
            if blocked and not (RUN/'sources'/f'batch-{batch[0]:03d}.json').exists():
                source = {'batch':batch[0],'titles':batch[1],'error':'not-requested-after-server-rate-limit','retryAfter':blocked}
            else:
                source = fetch_batch(batch)
                if source.get('retryAfter'):
                    blocked = source['retryAfter']
            sources.append(source)
            print(f"Captured {len(sources)}/{len(batches)} batches; batch {source['batch']} {source.get('error','OK')}",flush=True)
        sources.sort(key=lambda s:s['batch'])
        dump(RUN/'sources.json',{'provider':'English Wiktionary contributors','license':'CC BY-SA 4.0; additional terms and possible GFDL availability: see licenseUrl. Retain attribution and share-alike for adaptations.',
            'licenseUrl':'https://en.wiktionary.org/wiki/Wiktionary:Copyrights','batches':sources})
    entries,candidates,pages = analyze(vocab,sources)
    totals = {l:sum(e['comparisonCounts'][l] for e in entries) for l in LANGUAGES}
    summary = {'dictionaryVersion':json.loads((ROOT/'data/lexicon.json').read_text(encoding='utf-8'))['version'],
        'dictionarySha256':hashlib.sha256((ROOT/'data/lexicon.json').read_bytes()).hexdigest(),
        'processedEntries':len(entries),'uniqueEnglishLookups':len(titles),'retrievedPages':len(pages),
        'sourceErrors':[s for s in sources if 'error' in s], 'comparisonCounts':totals,
        'entriesWithExternalTranslations':sum(any(e['comparisonCounts'][l] for l in LANGUAGES[1:]) for e in entries),
        'entriesWithAllSixLanguageForms':sum(all(e['comparisonCounts'][l] for l in LANGUAGES) for e in entries),
        'screeningCandidates':len(candidates),'candidateEntryCount':len({c['lexiconId'] for c in candidates}),
        'candidateLanguageCounts':dict(Counter(c['language'] for c in candidates)),
        'semanticCertification':False,'policy':'Only confirmed similarity of BOTH meaning and whole form warrants change. Distance <=2 / substring is retrieval only.',
        'limitations':['English gloss comparison uses internal labels, not independent English semantic validation.',
          'All retrieved senses are screened; homonyms and parts of speech require candidate review.',
          'Japanese forms require an explicit source tr= Latin-script romanization; no generated readings.',
          'Redirect-only translation references, nested templates, absent tables and Japanese-only extra senses are not certified.',
          'All 1008 IDs processed does not certify all senses in all six languages.'],
        'previousReviewedComparison':load_and_compare(vocab)}
    dump(RUN/'comparison.json',{'summary':summary,'entries':entries,'candidates':candidates})
    dump(RUN/'translations.json',{'pages':list(pages.values())})
    with (RUN/'entries.csv').open('w',encoding='utf-8-sig',newline='') as stream:
        writer=csv.writer(stream);writer.writerow(['id','nrs','meaningJa','meaningEn',*LANGUAGES,'candidateCount','missingLanguages'])
        for e in entries:
            writer.writerow([e['lexiconId'],e['nrs'],e['meaningJa'],e['meaningEn'],*[e['comparisonCounts'][l] for l in LANGUAGES],
                sum(c['lexiconId']==e['lexiconId'] for c in candidates),','.join(l for l in LANGUAGES if not e['comparisonCounts'][l])])
    with (RUN/'candidates.csv').open('w',encoding='utf-8-sig',newline='') as stream:
        fields=['lexiconId','nrs','meaningJa','querySense','language','sourceForm','sourceSense','sourcePos','distance','substring','source','semanticStatus']
        writer=csv.DictWriter(stream,fieldnames=fields,extrasaction='ignore');writer.writeheader();writer.writerows(candidates)
    print(json.dumps({k:v for k,v in summary.items() if k not in ['previousReviewedComparison','sourceErrors']},ensure_ascii=False,indent=2))
    print('Source error batches:',len(summary['sourceErrors']))


if __name__ == '__main__':main()
