"""Build a source-attributed comparison set from captured lexical tables.

Translation-table rows are source data, not proof that all Nebulith senses have
been mapped. Only explicitly reviewed concept links are used for conclusions.
"""
import json
import re
import unicodedata
from collections import Counter
from nebulith_data import ROOT, dump, entry_hash

LINKS = {'sun': [73], 'moon': [49], 'star': [62], 'water': [332], 'sea': [377],
         'stone': [285], 'sand': [308], 'cloud': [322], 'wind': [365], 'fire': [361],
         'tree': [391], 'leaf': [392], 'root': [419], 'flower': [398], 'bird': [456],
         'fish': [465], 'hand': [245], 'foot': [225], 'head': [235], 'eye': [261],
         'ear': [214], 'blood': [202], 'bone': [205], 'heart': [253], 'salt': [970],
         'walk': [902], 'eat': [972], 'sleep': [222], 'rain': [333], 'sky': [1]}

# Individually checked against Japanese meaning and part of speech, not regex matches.
# Excludes legal "right", numeric "float", nominal "sleep", verbal "tie",
# spatial "back", "dwell" as biological live, and receive as sustained hold.
LINKS.update({'thick': [827], 'heavy': [773], 'small': [821], 'narrow': [801],
              'thin': [806], 'animal': [428], 'forest': [404], 'fruit': [422],
              'seed': [387], 'bark': [393], 'grass': [397], 'rope': [670],
              'skin': [216], 'horn': [449], 'nose': [264], 'mouth': [211],
              'back': [426], 'drink': [959], 'breathe': [268], 'laugh': [907],
              'hear': [866], 'live': [267], 'dig': [926], 'swim': [958],
              'fly': [945], 'come': [930], 'fall': [930], 'give': [909],
              'wash': [911], 'sing': [845], 'freeze': [886], 'lake': [339],
              'dust': [282], 'earth': [277], 'snow': [356], 'ice': [353],
              'burn': [905], 'mountain': [275], 'red': [802], 'green': [828],
              'white': [760], 'black': [791], 'night': [22], 'cold': [788],
              'new': [810], 'old': [776], 'round': [805], 'sharp': [793],
              'smooth': [766], 'near': [849], 'far': [931], 'right': [898],
              'left': [890], 'and': [938], 'because': [957]})

# Additional sense links checked beyond exact English gloss tokens.
LINKS.update({'leg': [225], 'fog': [322], 'feather': [462], 'pull': [916], 'dry': [837]})
REVIEWED_GLOSSES = {('feather', 462): 'flight feather', ('pull', 916): 'pull cable',
                    ('dry', 837): 'crisp dry'}


def normalize_form(value):
    value = unicodedata.normalize('NFKC', value).casefold().replace('ß', 'ss').replace('œ', 'oe').replace('æ', 'ae')
    return ''.join(c for c in unicodedata.normalize('NFD', value) if not unicodedata.combining(c)).strip()


def forms(cell):
    cell = re.sub(r'\([^)]*\)', '', cell).replace('*', '').strip()
    result = []
    for piece in re.split(r'[,;/]', cell):
        word = re.sub(r'\s+', ' ', piece).strip(' .')
        if word.lower().startswith('to '):
            word = word[3:]
        if word and all(c.isalpha() or c in " -'’" for c in word):
            result.append(word)
    return list(dict.fromkeys(result))


def concept_name(value):
    return re.sub(r'\([^)]*\)', '', value).strip().removeprefix('to ').lower()


def main():
    path = ROOT / 'audit/runs/2026-10-15-reviewed/swadesh/sources.json'
    captured = json.loads(path.read_text(encoding='utf-8'))['sources']
    records, sources, concepts = [], [], {}
    for source in captured:
        if source['status'] != 'table-extracted-unreviewed':
            continue
        sources.append({k: v for k, v in source.items() if k != 'rows'})
        rows = [r for r in source['rows'] if r[0].isdigit()]
        if {int(r[0]) for r in rows} != set(range(1, 208)):
            raise ValueError('Unexpected Swadesh concept inventory')
        for row in rows:
            concept = 'swadesh-207:'+row[0]
            if source['language'] == 'la':
                concepts[concept] = {'conceptId': concept, 'englishGloss': row[1]}
            variants = [(source['language'], row[-1] if source['language'] == 'ja' else row[2])]
            if source['language'] == 'la':
                variants.append(('en', row[1]))
            for language, cell in variants:
                for word in forms(cell):
                    record = {'conceptId': concept, 'language': language, 'sourceForm': word,
                              'comparisonForm': normalize_form(word), 'sourceId': source['id'],
                              'row': int(row[0]), 'rawCell': cell}
                    records.append(record)
    records = list({(r['conceptId'], r['language'], r['sourceForm']): r for r in records}.values())
    by_name = {}
    for concept in concepts.values():
        by_name.setdefault(concept_name(concept['englishGloss']), []).append(concept['conceptId'])
    vocab = json.loads((ROOT / 'data/lexicon.json').read_text(encoding='utf-8'))['vocabulary']
    by_id = {r['id']: r for r in vocab}
    links = []
    for label, ids in LINKS.items():
        targets = by_name.get(label, [])
        if len(targets) != 1:
            raise ValueError(f'Concept must be unambiguous: {label} -> {targets}')
        for id_ in ids:
            entry = by_id[id_]
            reviewed_gloss = REVIEWED_GLOSSES.get((label, id_), label)
            if reviewed_gloss not in [s.strip() for s in entry['meaningEn'].lower().split(',')]:
                raise ValueError(f'Reviewed meaning drift: {id_}')
            links.append({'lexiconId': id_, 'conceptId': targets[0], 'decision': 'approved',
                          'reviewer': 'Codex', 'reviewedAgainstEntryHash': entry_hash(entry),
                          'reason': f"辞書の{entry['meaningJa']} / {reviewed_gloss}を、Swadeshの{label}の基本語義へ対応。"+
                          ({'feather': '飛翔羽という具体的な羽の語義に限定。', 'pull': '手で引き寄せる行為に限定。', 'dry': '乾いた性質の語義に限定。'}.get(label, ''))+
                          '複合・比喩の別語義まで網羅した承認ではない。'})
    out = ROOT / 'data/audit/earth_lexicon.jsonl'
    out.write_text(''.join(json.dumps(r, ensure_ascii=False)+'\n' for r in records), encoding='utf-8')
    dump(ROOT / 'data/audit/earth_concept_links.json', {'scope': 'source-attributed partial concept mapping', 'entries': links})
    dump(ROOT / 'data/audit/earth_concepts.json', {'concepts': list(concepts.values())})
    dump(ROOT / 'data/audit/earth_sources.json', {'status': 'partial-source-backed',
         'requiredLanguages': ['en', 'la', 'fr', 'es', 'de', 'ja'], 'sources': sources,
         'comparisonRows': len(records), 'languageRows': dict(Counter(r['language'] for r in records)),
         'normalization': 'NFKC, casefold, ligatures oe/ae/ss, remove combining marks; Japanese source Hepburn macrons lose length in ASCII comparison. Orthographic, not phonetic equivalence.',
         'scope': '207基本概念の出典付き比較資料。全1008語義の対応・約2000語の監査母集団の充足は未完了。',
         'pending': ['残るNebulith語義との意味対応', '全語義・言語別の比較母集団と用語辞書', '表記正規化の追加異形の検討'],
         'legacyComparison': {'path': 'tools/false_friend_detector.py', 'mayCertifyFullCoverage': False}})
    print(f'Imported {len(records)} sourced comparison forms across six languages; {len(links)} reviewed partial links.')


if __name__ == '__main__':
    main()
