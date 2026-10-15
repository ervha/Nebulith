"""Relocate audit documents, retaining exact originals for historical seals."""
import hashlib
import json
import os
import re
from pathlib import Path
from urllib.parse import quote, unquote

ROOT = Path(__file__).resolve().parents[1]
NAMES = ['Nebulith Standard Audit Report.md', 'Nebulith Audit Results 2026-10-15.md',
         'Nebulith Audit Results 2026-10-15-Reaudit.md',
         'Nebulith Audit Results 2026-10-15-Reaudit-02.md',
         'Nebulith Remediation Proposal 2026-10-15.md']


def main():
    target = ROOT / 'audit/docs'
    archive = ROOT / 'audit/archive/original-documents'
    target.mkdir(parents=True, exist_ok=True)
    archive.mkdir(parents=True, exist_ok=True)
    mapping = {(ROOT / 'docs' / n).resolve(): target / n for n in NAMES}
    manifest_path = ROOT / 'audit/document-migration.json'
    if manifest_path.exists():
        print('Migration already recorded; no files changed.')
        return
    records = []
    for old, new in mapping.items():
        original = old.read_bytes()
        saved = archive / old.name
        if new.exists() or saved.exists():
            raise FileExistsError(f'Refusing to overwrite {new} or {saved}')
        saved.write_bytes(original)

        def relocate(match):
            href = match[1]
            if '://' in href or href.startswith('#'):
                return match[0]
            path, sep, fragment = unquote(href).partition('#')
            resolved = (old.parent / path).resolve()
            destination = mapping.get(resolved, resolved)
            relative = os.path.relpath(destination, new.parent).replace('\\', '/')
            return '](' + quote(relative, safe='/') + (sep + fragment if sep else '') + ')'

        text = re.sub(r'\]\(([^)]+)\)', relocate, original.decode('utf-8'))
        # Match the source's newline convention when changing navigational links.
        moved = text.encode('utf-8')
        new.write_bytes(moved)
        if ROOT not in old.parents or ROOT not in new.resolve().parents:
            raise ValueError('Migration path escaped workspace')
        old.unlink()
        records.append({'oldPath': old.relative_to(ROOT).as_posix(),
                        'currentPath': new.relative_to(ROOT).as_posix(),
                        'originalPath': saved.relative_to(ROOT).as_posix(),
                        'originalSha256': hashlib.sha256(original).hexdigest(),
                        'relocatedSha256': hashlib.sha256(moved).hexdigest()})
    manifest_path.write_text(json.dumps({'note': 'Original bytes retained; relocated copies have updated relative links.',
                                         'documents': records}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(f'Moved {len(records)} audit documents; exact original bytes archived.')


if __name__ == '__main__':
    main()
