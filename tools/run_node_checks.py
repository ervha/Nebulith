"""Run the same JavaScript checks on Windows and CI, preserving every exit code."""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def run_checks(paths, cwd=ROOT):
    failed = []
    for path in paths:
        print(f'RUN: {path.name}', flush=True)
        result = subprocess.run(['node', str(path)], cwd=cwd, check=False)
        if result.returncode:
            failed.append((path.name, result.returncode))
            print(f'FAIL: {path.name} (exit {result.returncode})', flush=True)
    return failed


def main():
    # The productive matrix is already run by test_web_studio.py in the Python suite.
    paths = [p for p in sorted((ROOT / 'tests').glob('verify*.js'))
             if p.name != 'verify_productive_translation.js']
    if not paths:
        raise SystemExit('No JavaScript checks were discovered')
    failed = run_checks(paths, cwd=ROOT)
    print(f'JavaScript suites: {len(paths) - len(failed)}/{len(paths)} passed', flush=True)
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
