"""Capture IAU OAE terms for 50 reviewed entries, without inventing missing translations."""
import hashlib
import json
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
from html.parser import HTMLParser
from nebulith_data import ROOT,dump,entry_hash

MAPPINGS={3:['Molecular Cloud'],4:['Celestial Sphere'],7:['Planet'],9:['Luminosity'],
 10:['Aphelion','Apoapsis'],12:['Refraction'],14:['Spectrum'],15:['Reflection'],16:['Light'],
 17:['Zodiacal Light'],18:['Comet'],21:['Supernova Remnant'],25:['Eclipse','Occultation'],
 26:['Dark Matter'],27:['Penumbra'],28:['Event Horizon'],29:['Outer Space','Cosmos'],
 30:['Galaxy Cluster'],31:['Black Hole','Singularity'],32:['Comet Nucleus'],33:['Escape Velocity'],
 34:['Orbit'],35:['Orbital Inclination'],37:['Nebula','Dust Cloud'],38:['Protoplanetary Disk'],
 39:['Perihelion','Periapsis'],40:['Zenith'],42:['Escape Velocity'],43:['Semi-major Axis'],
 47:['Nadir'],50:['Gravity'],53:['Gravitational Waves','Tidal Force']}


class Anchors(HTMLParser):
    def __init__(self):super().__init__();self.rows=[];self.active=None;self.text=[]
    def handle_starttag(self,tag,attrs):
        if tag=='a':self.active=dict(attrs).get('href','');self.text=[]
    def handle_data(self,data):
        if self.active is not None:self.text.append(data)
    def handle_endtag(self,tag):
        if tag=='a' and self.active is not None:
            self.rows.append((self.active,re.sub(r'\s+',' ',''.join(self.text)).strip()));self.active=None


def capture(url,path):
    if path.exists():return path.read_text(encoding='utf-8')
    raw=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'NebulithResearch/1.0'}),timeout=25).read()
    text=raw.decode('utf-8');path.write_bytes(raw);return text


def main():
    out=ROOT/'audit/runs/2026-10-15-development/sources';out.mkdir(parents=True,exist_ok=True)
    index_url='https://astro4edu.org/resources/glossary/search/'
    index=capture(index_url,out/'iau-index.html');p=Anchors();p.feed(index)
    terms={text.casefold():href.replace('/term/','/term-detail/') for href,text in p.rows if re.fullmatch(r'/resources/glossary/term/\d+/',href)}
    vocab=json.loads((ROOT/'data/lexicon.json').read_text(encoding='utf-8'))['vocabulary']
    linked={r['lexiconId'] for r in json.loads((ROOT/'data/audit/earth_concept_links.json').read_text(encoding='utf-8'))['entries']}
    selected=[r for r in vocab if r['id'] not in linked][:50]
    requested={label for row in selected for label in MAPPINGS.get(row['id'],[]) if label.casefold() in terms}
    def fetch(label):
        url='https://astro4edu.org'+terms[label.casefold()];id_=url.rstrip('/').split('/')[-1]
        path=out/('iau-'+id_+'.html')
        try:
            text=capture(url,path);parser=Anchors();parser.feed(text)
            translations={}
            for href,word in parser.rows:
                match=re.fullmatch(r'/(?:(fr|de|es|ja)/)?resources/glossary/term/'+id_+'/',href)
                if match and word:translations[match[1] or 'en']=word
            # Japanese entries are external and do not provide an attested romanization.
            ja=next((word for href,word in parser.rows if 'astro-dic.jp' in href),None)
            source={'id':'iau-oae:'+id_,'url':url,'snapshot':path.relative_to(ROOT).as_posix(),
                    'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'attribution':'IAU OAE',
                    'license':'CC BY 4.0','licenseVerified':'creativecommons.org/licenses/by/4.0' in text,
                    'retrievedAt':datetime.fromtimestamp(path.stat().st_mtime,timezone.utc).isoformat()}
            return label,{'source':source,'translations':translations,'japaneseLabel':ja}
        except Exception as exc:return label,{'error':str(exc)}
    with ThreadPoolExecutor(max_workers=4) as pool:results=dict(pool.map(fetch,sorted(requested)))
    records=[]
    for row in selected:
        senses=[]
        for label in MAPPINGS.get(row['id'],[]):
            result=results.get(label)
            if not result or result.get('error'):
                senses.append({'label':label,'status':'source-missing','reason':result.get('error') if result else 'No exact glossary entry; do not substitute a broader concept.'})
            else:
                senses.append({'label':label,'status':'partial-source-backed',**result,
                               'mappingReview':'Codex AI review: basic or explicit secondary sense only; not all meanings.',
                               'missing':['la','ja-romanization'],'reason':'Latin translation and sourced Japanese reading/romanization are unavailable; six-language completeness is not claimed.'})
        records.append({'lexiconId':row['id'],'nrs':row['nrs'],'meaningJa':row['meaningJa'],'meaningEn':row['meaningEn'],
                        'category':row['category'],'pos':row['pos'],'entryHash':entry_hash(row),'reviewer':'Codex',
                        'status':'partial' if any(s['status']=='partial-source-backed' for s in senses) else 'source-needed',
                        'senses':senses,'reason':'Inspect each dictionary sense separately. No exact documented translation has been assigned to unresolved senses.'})
    dump(ROOT/'data/audit/earth_research_batch_01.json',{'scope':'50 previously unmapped entries; partial research, no full-sense approval',
          'indexSource':{'url':index_url,'snapshot':(out/'iau-index.html').relative_to(ROOT).as_posix(),'sha256':hashlib.sha256((out/'iau-index.html').read_bytes()).hexdigest()},
          'entries':records})
    print(json.dumps({'entries':len(records),'partial':sum(r['status']=='partial' for r in records),'sources':len(results),'fetchErrors':[k for k,v in results.items() if v.get('error')]}))


if __name__=='__main__':main()
