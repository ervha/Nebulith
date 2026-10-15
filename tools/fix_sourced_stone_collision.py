"""Resolve the attested talis/lapis collision without renaming talisum (theorem)."""
import json
from nebulith_data import ROOT, dump, export_lexicon


def main():
    path = ROOT / 'data/lexicon.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    fixes = {285: ('talis', 'talyr', '[ta.lyr]'), 286: ('talisar', 'talyrar', '[ta.ly.rar]'),
             814: ('taliski', 'talyrki', '[ta.lyr.ki]')}
    changes = []
    for row in data['vocabulary']:
        if row['id'] not in fixes:
            continue
        old, new, ipa = fixes[row['id']]
        if row['nrs'] not in [old, new]:
            raise ValueError('Unexpected source root: '+str(row['id']))
        if any(r['nrs'] == new and r['id'] != row['id'] for r in data['vocabulary']):
            raise ValueError('Duplicate target: '+new)
        changes.append({'lexiconId': row['id'], 'oldNrs': old, 'newNrs': new,
                        'reason': '石のtalyr語幹へ統一。talis/lapisの出典付き距離2を是正。'})
        row['nrs'], row['ipa'] = new, ipa
        row['notes'] = row['notes'].replace('talis (石)', 'talyr (石)')
    data['version'] = '23.3'
    data['status'] = '監査中。コーパスと限定比較の是正を実施。全項目適合・リリース承認は未実施。'
    export_lexicon(data)
    dump(ROOT / 'data/audit/stone_root_migration.json', {'changes': changes,
          'preservedIndependentRoots': [{'lexiconId': 119, 'nrs': 'talisum', 'reason': '数学的定理の独立語。石の語源参照がないため変更しない。'}]})
    print('Updated stone and its two attested derivatives; independent theorem root preserved.')


if __name__ == '__main__':
    main()
