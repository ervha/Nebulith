"""Publish one Windows x64 EXE with a checksummed Temurin JRE and offline JAR."""
import argparse,hashlib,json,os,shutil,subprocess,urllib.request,zipfile
from pathlib import Path
from nebulith_data import ROOT,dump
from verify_studio_bundle import verify


def fetch(url,path):
    if not path.exists():
        request=urllib.request.Request(url,headers={'User-Agent':'NebulithStudioBuild/1.0'})
        with urllib.request.urlopen(request,timeout=90) as response,path.open('wb') as out:
            shutil.copyfileobj(response,out)
    return path


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--skip-test',action='store_true');args=parser.parse_args()
    verify()
    build=ROOT/'studio/build';work=build/'package';work.mkdir(exist_ok=True)
    project=ROOT/'studio/launcher/NebulithStudio.csproj'
    dotnet_env=dict(os.environ,DOTNET_CLI_TELEMETRY_OPTOUT='1',DOTNET_NOLOGO='1',DOTNET_GENERATE_ASPNET_CERTIFICATE='false')
    intermediate='-p:BaseIntermediateOutputPath='+str(work/'obj')+os.sep
    restore=subprocess.run(['dotnet','restore',str(project),intermediate,'--nologo'],cwd=ROOT,env=dotnet_env,capture_output=True,text=True,encoding='utf-8',errors='replace')
    (work/'restore.log').write_text(restore.stdout+restore.stderr,encoding='utf-8')
    if restore.returncode:raise RuntimeError(restore.stdout+restore.stderr)
    metadata=fetch('https://api.github.com/repos/adoptium/temurin21-binaries/releases/latest',work/'temurin-release.json')
    release=json.loads(metadata.read_text(encoding='utf-8'))
    asset=next(a for a in release['assets'] if a['name'].startswith('OpenJDK21U-jre_x64_windows_hotspot_') and a['name'].endswith('.zip'))
    checksum_asset=next(a for a in release['assets'] if a['name']==asset['name']+'.sha256.txt')
    runtime=fetch(asset['browser_download_url'],work/asset['name'])
    checksum=fetch(checksum_asset['browser_download_url'],work/checksum_asset['name']).read_text().split()[0]
    sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
    if sha(runtime)!=checksum:raise ValueError('Runtime SHA256 mismatch')
    print('Runtime verified:',asset['name'],flush=True)
    payload=work/'payload.zip';hashes={}
    with zipfile.ZipFile(payload,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as target:
        with zipfile.ZipFile(runtime) as source:
            for name in source.namelist():
                if name.endswith('/'):continue
                relative='runtime/'+name.split('/',1)[1]
                if '..' in Path(relative).parts:raise ValueError('Invalid runtime archive path')
                value=source.read(name);target.writestr(relative,value);hashes[relative]=hashlib.sha256(value).hexdigest()
        jar=build/'NebulithStudio.jar';value=jar.read_bytes();target.writestr(jar.name,value);hashes[jar.name]=sha(jar)
        source_asset=next((a['browser_download_url'] for a in release['assets'] if 'sources_' in a['name'] and a['name'].endswith('.tar.gz')),release['html_url'])
        notices=('Nebulith Studio bundles Eclipse Temurin OpenJDK. Runtime license and third-party notices: runtime/legal/.\n'
                 'Runtime binary: '+asset['browser_download_url']+'\nCorresponding sources: '+source_asset+'\n'
                 'The .NET launcher uses Microsoft .NET under the MIT license.\n'
                 'https://github.com/dotnet/runtime/blob/main/LICENSE.TXT\n'
                 'https://github.com/dotnet/runtime/blob/main/THIRD-PARTY-NOTICES.TXT\n').encode()
        target.writestr('THIRD-PARTY.txt',notices);hashes['THIRD-PARTY.txt']=hashlib.sha256(notices).hexdigest()
        # Include actual installed runtime/compiler notices, not only web links.
        asset_metadata=json.loads((work/'obj/project.assets.json').read_text(encoding='utf-8'))
        downloads=[d for f in asset_metadata['project']['frameworks'].values() for d in f.get('downloadDependencies',[])
                   if d['name'].lower()=='microsoft.netcore.app.runtime.win-x64']
        if not downloads:raise ValueError('Runtime dependency version is missing from restore metadata')
        version=downloads[0]['version'].strip('[]').split(',')[0]
        runtime_pack=next(Path(folder)/'microsoft.netcore.app.runtime.win-x64'/version for folder in asset_metadata['packageFolders']
            if (Path(folder)/'microsoft.netcore.app.runtime.win-x64'/version).is_dir())
        licenses=[(runtime_pack/name,'licenses/dotnet/'+name) for name in ['LICENSE.TXT','THIRD-PARTY-NOTICES.TXT']]
        kotlin_licenses=Path('C:/Program Files/Android/Android Studio/plugins/Kotlin/kotlinc/license')
        licenses += [(p,'licenses/kotlin/'+p.relative_to(kotlin_licenses).as_posix()) for p in kotlin_licenses.rglob('*') if p.is_file()]
        for path,name in licenses:
            value=path.read_bytes();target.writestr(name,value);hashes[name]=hashlib.sha256(value).hexdigest()
        target.writestr('files.json',json.dumps(hashes,indent=2))
    dist=build/'dist';dist.mkdir(exist_ok=True)
    command=['dotnet','publish',str(project),'-c','Release','-o',str(dist),
        '-p:BaseIntermediateOutputPath='+str(work/'obj')+os.sep,
        '-p:BaseOutputPath='+str(work/'bin')+os.sep,'--nologo']
    result=subprocess.run(command,cwd=ROOT,env=dotnet_env,capture_output=True,text=True,encoding='utf-8',errors='replace')
    (work/'publish.log').write_text(result.stdout+result.stderr,encoding='utf-8')
    if result.returncode:raise RuntimeError(result.stdout+result.stderr)
    exe=dist/'NebulithStudio.exe'
    if sorted(p.name for p in dist.iterdir())!=['NebulithStudio.exe']:raise ValueError('Distribution must contain exactly one EXE')
    evidence=None; window_evidence=None
    if not args.skip_test:
        # Invoke the EXE with Java absent from PATH and a foreign, Unicode working directory.
        testdir=work/'配布テスト space';testdir.mkdir(exist_ok=True)
        report=(testdir/'launcher-report.json').resolve()
        env=dict(os.environ,PATH=str(Path(os.environ['SystemRoot'])/'System32'),JAVA_HOME='')
        test=subprocess.run([str(exe),'--launcher-self-test',str(report)],cwd=testdir,env=env,timeout=180)
        evidence=json.loads(report.read_text(encoding='utf-8'))
        if test.returncode or evidence.get('javaExitCode')!=0:raise RuntimeError(str(evidence))
        window_report=(testdir/'window-launcher-report.json').resolve()
        test=subprocess.run([str(exe),'--launcher-window-self-test',str(window_report)],cwd=testdir,env=env,timeout=180)
        window_evidence=json.loads(window_report.read_text(encoding='utf-8'))
        if test.returncode or window_evidence.get('javaExitCode')!=0:raise RuntimeError(str(window_evidence))
    dump(work/'package-manifest.json',{'exe':exe.relative_to(ROOT).as_posix(),'exeSha256':sha(exe),'bytes':exe.stat().st_size,
        'jarSha256':sha(jar),'payloadSha256':sha(payload),'runtimeUrl':asset['browser_download_url'],
        'runtimeSha256':checksum,'runtimeSourceUrl':source_asset,'target':'Windows x64',
        'launcherSources':{p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'studio/launcher').glob('*') if p.is_file()},
        'selfTest':evidence,'windowSelfTest':window_evidence,'dotnetRuntimeVersion':version,
        'packageToolSha256':sha(Path(__file__)),'signed':False})
    print('Single EXE:',exe,'bytes:',exe.stat().st_size)


if __name__=='__main__':main()
