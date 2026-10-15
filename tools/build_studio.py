"""Build a Kotlin/JVM offline PoC with installed tooling; no downloads or global config changes."""
import argparse,base64,hashlib,json,os,subprocess,zipfile
from pathlib import Path
from nebulith_data import ROOT,dump,FIELDS,corpus_semantic_pending


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--jdk',default='C:/Program Files/Android/Android Studio/jbr')
    parser.add_argument('--kotlin',default='C:/Program Files/Android/Android Studio/plugins/Kotlin/kotlinc')
    args=parser.parse_args()
    java=Path(args.jdk)/'bin/java.exe';compiler=Path(args.kotlin)/'lib'
    if not java.is_file() or not (compiler/'kotlin-compiler.jar').is_file():raise SystemExit('Pass installed JDK and Kotlin directories using --jdk/--kotlin')
    out=ROOT/'studio/build';out.mkdir(parents=True,exist_ok=True)
    vocab=json.loads((ROOT/'data/lexicon.json').read_text(encoding='utf-8'))
    corpus=json.loads((ROOT/'data/canon_corpus.json').read_text(encoding='utf-8'))
    rules=json.loads((ROOT/'data/corpus_rules.json').read_text(encoding='utf-8'))
    if corpus_semantic_pending(corpus):raise ValueError('Cannot bundle unreviewed corpus')
    encode=lambda s:base64.b64encode(str(s).encode()).decode()
    resources={'lexicon.tsv':('\n'.join('\t'.join([str(r['id'])]+[encode(r[k]) for k in FIELDS[1:]]) for r in vocab['vocabulary'])+'\n').encode(),
      'translation-frames.tsv':('\n'.join('\t'.join([id_,','.join(frame['required']),','.join(frame['allowed']),','.join(frame.get('passiveAllowed',[]))]) for id_,frame in rules['frames'].items())+'\n').encode(),
      'corpus.tsv':('\n'.join('\t'.join(encode(x) for x in [u['id'],u['title'],u['nrs'],u['translationJa'],u['review']['note']]) for u in corpus['units'])+'\n').encode(),
      'Nebulith-Regular.ttf':(ROOT/'fonts/Nebulith-Regular.ttf').read_bytes(),
      'characters.txt':json.loads((ROOT/'fonts/inventory.json').read_text(encoding='utf-8'))['characters'].encode(),
      'version.txt':('lexicon '+vocab['version']+' / font '+json.loads((ROOT/'fonts/inventory.json').read_text(encoding='utf-8'))['fontVersion']).encode()}
    sources=sorted((ROOT/'studio/src').rglob('*.kt'))
    jar=out/'NebulithStudio.jar'
    command=[str(java),'-Dfile.encoding=UTF-8','-cp',str(compiler/'*'),'org.jetbrains.kotlin.cli.jvm.K2JVMCompiler',
      '-kotlin-home',args.kotlin,'-jvm-target','1.8','-include-runtime','-d',str(jar),*[str(p) for p in sources]]
    build=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
    (out/'build.log').write_text(build.stdout+build.stderr,encoding='utf-8')
    if build.returncode:raise RuntimeError(build.stdout+build.stderr)
    with zipfile.ZipFile(jar,'a',compression=zipfile.ZIP_DEFLATED) as archive:
        for name,value in resources.items():archive.writestr(name,value)
    test=subprocess.run([str(java),'-Dfile.encoding=UTF-8','-Djava.awt.headless=true','-jar',str(jar),'--self-test',str(out/'studio-preview.png')],capture_output=True,text=True,encoding='utf-8',errors='replace')
    (out/'self-test.log').write_text(test.stdout+test.stderr,encoding='utf-8')
    if test.returncode:raise RuntimeError(test.stdout+test.stderr)
    dump(out/'bundle-manifest.json',{'jarSha256':hashlib.sha256(jar.read_bytes()).hexdigest(),
      'sourceInputs':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ['data/lexicon.json','data/canon_corpus.json','data/corpus_rules.json','fonts/Nebulith-Regular.ttf','fonts/inventory.json','tools/build_studio.py']},
      'sourceSha256':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
      'resources':{name:hashlib.sha256(value).hexdigest() for name,value in resources.items()},
      'selfTest':test.stdout.strip(),'validation':'Headless JVM UI and logic; native IME, clipboard, Android and installer acceptance pending.'})
    print(test.stdout.strip());print(jar)


if __name__=='__main__':main()
