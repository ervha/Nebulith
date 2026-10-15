"""Apply the reviewed fly/volar collision only; retain independently used vol roots."""
import json
from nebulith_data import ROOT, dump, export_lexicon, expected_ipa, entry_hash


def main():
    path = ROOT / 'data/lexicon.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    vocab = data['vocabulary']
    row = next(r for r in vocab if r['id'] == 945)
    if row['nrs'] == 'veiran':
        print('Flight collision already repaired; migration record retained.')
        return
    if row['nrs'] != 'volan' or any(r['nrs'] == 'veiran' for r in vocab):
        raise ValueError('Unexpected source or duplicate target')
    before = dict(row)
    row['nrs'], row['ipa'] = 'veiran', '['+expected_ipa('veiran')+']'
    notes = []
    for entry in vocab:
        old = entry['notes']
        entry['notes'] = old.replace('volan (飛ぶ)', 'veiran (飛ぶ)')
        if old != entry['notes']:
            notes.append({'lexiconId': entry['id'], 'before': old, 'after': entry['notes']})
    export_lexicon(data)
    dump(ROOT / 'data/audit/flight_root_migration.json', {
        'reviewer': 'Codex', 'reviewType': 'AI meaning and form review',
        'before': before, 'after': row, 'beforeHash': entry_hash(before), 'afterHash': entry_hash(row),
        'reason': '飛ぶの語義が一致し、volan/volarは末尾1文字のみ異なる。voler/volōとも近い。語形全体と意味の両条件で変更。',
        'noteUpdates': notes,
        'preserved': '別語義のfervolan、意味と語形の両条件を満たさない他のvol系語は改名しない。'})


if __name__ == '__main__':
    main()
