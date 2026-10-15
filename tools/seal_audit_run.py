"""Validate a completed evidence run and save test output and hashes."""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote

from nebulith_data import ROOT, dump
from verify_audit_archive import verify


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('directory')
    args = parser.parse_args()
    out = (ROOT / args.directory).resolve()
    if ROOT / 'audit/runs' not in out.parents:
        parser.error('Expected a run under audit/runs')
    if (out / 'seal.json').exists():
        parser.error('Refusing to overwrite an existing seal')
    evidence = json.loads((out / 'evidence.json').read_text(encoding='utf-8'))
    sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
    for path, info in evidence['manifest'].items():
        assert sha(ROOT / path) == info['sha256'], f'Audited input changed: {path}'
    archive = verify()
    docs = list((ROOT / 'audit/docs').glob('*.md')) + [ROOT / 'audit/README.md']
    for path in docs:
        for href in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
            if '://' not in href and not href.startswith('#'):
                assert (path.parent / unquote(href).split('#')[0]).exists(), (path, href)
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    test = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'],
                          cwd=ROOT, env=env, capture_output=True, text=True, encoding='utf-8')
    (out / 'unittest.log').write_text(test.stdout+test.stderr, encoding='utf-8')
    assert test.returncode == 0, test.stdout+test.stderr
    tests_run = int(re.search(r'Ran (\d+) tests?', test.stdout+test.stderr)[1])
    browser_path = out / 'browser-evidence.json'
    if browser_path.exists():
        browser = json.loads(browser_path.read_text(encoding='utf-8'))
        browser['fontSha256'] = evidence['manifest']['fonts/Nebulith-Regular.ttf']['sha256']
        browser['corpusSha256'] = evidence['manifest']['data/canon_corpus.json']['sha256']
        dump(browser_path, browser)
    summary = {'timestamp_utc': datetime.now(timezone.utc).isoformat(), 'audited_inputs_unchanged': True,
               'archive': archive, 'tests_run': tests_run, 'test_exit_code': test.returncode,
               'document_links_valid': True, 'scorecard_counts': evidence['scorecard_counts'],
               'scope': 'Automatic checks and reference integrity; no release approval.'}
    dump(out / 'validation.json', summary)
    artifacts = {p.relative_to(ROOT).as_posix(): sha(p) for p in out.iterdir() if p.is_file()}
    artifacts.update({p.relative_to(ROOT).as_posix(): sha(p) for p in docs})
    artifacts['tools/seal_audit_run.py'] = sha(Path(__file__))
    artifacts.update({p.relative_to(ROOT).as_posix(): sha(p) for p in (ROOT / 'tests').glob('test_*.py')})
    dump(out / 'seal.json', {'timestamp_utc': summary['timestamp_utc'], 'artifact_sha256': artifacts,
                             'counts': evidence['scorecard_counts']})
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
