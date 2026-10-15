"""Verify packaged resources against canonical inputs without launching a JVM."""
import base64,hashlib,json,zipfile
from nebulith_data import ROOT,FIELDS


def verify():
    out=ROOT/'studio/build';jar=out/'NebulithStudio.jar'
    meta=json.loads((out/'bundle-manifest.json').read_text(encoding='utf-8'))
    assert hashlib.sha256(jar.read_bytes()).hexdigest()==meta['jarSha256'],'JAR changed'
    for path,digest in {**meta['sourceSha256'],**meta['sourceInputs']}.items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,'Stale app input: '+path
    with zipfile.ZipFile(jar) as z:
        assert 'Main-Class:' in z.read('META-INF/MANIFEST.MF').decode()
        for name,digest in meta['resources'].items():
            assert z.namelist().count(name)==1,'Duplicate resource: '+name
            assert hashlib.sha256(z.read(name)).hexdigest()==digest,name
        data=json.loads((ROOT/'data/lexicon.json').read_text(encoding='utf-8'))
        decoded=[]
        for line in z.read('lexicon.tsv').decode().splitlines():
            cells=line.split('\t');decoded.append([int(cells[0])]+[base64.b64decode(x).decode() for x in cells[1:]])
        assert decoded==[[r[k] for k in FIELDS] for r in data['vocabulary']]
        corpus=json.loads((ROOT/'data/canon_corpus.json').read_text(encoding='utf-8'))
        examples=[[base64.b64decode(x).decode() for x in line.split('\t')] for line in z.read('corpus.tsv').decode().splitlines()]
        assert examples==[[u['id'],u['title'],u['nrs'],u['translationJa'],u['review']['note']] for u in corpus['units']]
        assert z.read('Nebulith-Regular.ttf')==(ROOT/'fonts/Nebulith-Regular.ttf').read_bytes()
    return {'entries':len(decoded),'examples':len(examples),'fontMatches':True,'sourceInputsMatch':True,'jarSha256':meta['jarSha256']}


if __name__=='__main__':print(verify())
