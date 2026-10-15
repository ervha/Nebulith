"""Collect attributed Swadesh comparison tables; never claim full coverage.

Stores immutable fetched HTML and extracted table cells in a new directory.
No comparison is made from unreviewed translations or scraped annotations.
"""
import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.request import Request, urlopen

from nebulith_data import ROOT, dump

PAGES = {'la': 'Latin', 'fr': 'French', 'de': 'German', 'es': 'Spanish', 'ja': 'Japanese'}


class Tables(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables, self.depth, self.rows, self.row, self.cell = [], 0, [], None, None
        self.sup = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            if self.depth == 0:
                self.rows = []
            self.depth += 1
        if not self.depth:
            return
        if tag == 'tr':
            self.row = []
        if tag in ['td', 'th']:
            self.cell = []
        if tag == 'sup':
            self.sup += 1
        if tag == 'br' and self.cell is not None:
            self.cell.append('; ')

    def handle_data(self, data):
        if self.depth and self.cell is not None and not self.sup:
            self.cell.append(data)

    def handle_endtag(self, tag):
        if tag == 'sup':
            self.sup = max(0, self.sup-1)
        if tag in ['td', 'th'] and self.cell is not None:
            if self.row is not None:
                self.row.append(re.sub(r'\s+', ' ', ''.join(self.cell)).strip())
            self.cell = None
        if tag == 'tr' and self.row is not None:
            self.rows.append(self.row)
            self.row = None
        if tag == 'table':
            self.depth -= 1
            if not self.depth:
                self.tables.append(self.rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('directory')
    args = parser.parse_args()
    out = (ROOT / args.directory).resolve()
    if ROOT / 'audit' not in out.parents:
        parser.error('Output must be below audit/')
    out.mkdir(parents=True, exist_ok=False)
    sources = []
    for language, name in PAGES.items():
        url = f'https://en.wiktionary.org/wiki/Appendix:{name}_Swadesh_list'
        request = Request(url, headers={'User-Agent': 'NebulithAudit/0.1 (local lexicon comparison; urllib)'})
        try:
            with urlopen(request, timeout=25) as response:
                raw = response.read()
            (out / f'{language}.html').write_bytes(raw)
            html = raw.decode('utf-8')
            tables = Tables()
            tables.feed(html)
            candidates = [t for t in tables.tables if sum(bool(r and re.fullmatch(r'\d+', r[0])) for r in t) >= 100]
            if len(candidates) != 1:
                raise ValueError(f'Expected one numbered Swadesh table, got {len(candidates)}')
            revision = re.search(r'"wgRevisionId"\s*:\s*(\d+)', html)
            record = {'id': f'wiktionary-swadesh-{language}', 'language': language, 'url': url,
                      'retrievedAt': datetime.now(timezone.utc).isoformat(),
                      'revisionId': revision[1] if revision else None,
                      'sha256': hashlib.sha256(raw).hexdigest(), 'snapshot': (out / f'{language}.html').relative_to(ROOT).as_posix(),
                      'attribution': f'Wiktionary contributors, Appendix:{name} Swadesh list; see source page history',
                      'license': 'CC BY-SA 4.0 (page footer); individual lexical facts extracted',
                      'licenseUrl': 'https://creativecommons.org/licenses/by-sa/4.0/',
                      'status': 'table-extracted-unreviewed', 'rows': candidates[0]}
            sources.append(record)
            print(language, len(candidates[0]), 'rows extracted')
        except Exception as error:
            sources.append({'language': language, 'url': url, 'status': 'unavailable', 'error': str(error)})
            print(language, type(error).__name__, str(error))
        dump(out / 'sources.json', {'sources': sources, 'scope': 'Source acquisition only. No automatic semantic approval.'})


if __name__ == '__main__':
    main()
