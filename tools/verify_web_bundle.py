"""Verify the distributable Web app against its current source data."""
import json
import re
from pathlib import Path
from evidence_hash import recorded_digest_matches
from studio_dictionary import dictionary_entries

ROOT = Path(__file__).resolve().parents[1]


def verify():
    meta = json.loads((ROOT / 'web/build-manifest.json').read_text(encoding='utf-8'))
    for path, digest in meta['sha256'].items():
        assert recorded_digest_matches(ROOT / path, digest), 'Stale Web input/output: ' + path
    script = (ROOT / 'web/data.js').read_text(encoding='utf-8')
    def value(name):
        return json.loads(re.search(r'^const ' + name + r' = (.+);$', script, re.M)[1])
    vocab = dictionary_entries(json.loads((ROOT / 'data/lexicon.json').read_text(encoding='utf-8'))['vocabulary'])
    keys = dict(id='id', r='nrs', p='pos', m='meaningJa', i='ipa', en='meaningEn', c='category', n='notes')
    expected=[]
    for entry in vocab:
        row={k: entry[v] for k,v in keys.items()}
        wid=entry['id']
        row.update(o=entry.get('origin') or ('canon' if wid<=1008 else 'curated_ext'),
                   **{'as':entry.get('auditStatus','canon_verified' if wid<=1008 else 'curated')},\
                   sc=entry.get('auditScore',1.0),sid=entry.get('scenarioId',''),et=entry.get('etymology',''))
        expected.append(row)
    assert value('VOCAB') == expected
    assert value('GRAMMAR_FRAMES') == json.loads((ROOT / 'data/corpus_rules.json').read_text(encoding='utf-8'))['frames']
    assert value('INPUT_RULES') == json.loads((ROOT / 'data/translation_input_rules.json').read_text(encoding='utf-8'))
    extensions = json.loads((ROOT / 'data/translation_extensions.json').read_text(encoding='utf-8'))
    extensions['productive'] = json.loads((ROOT / 'data/translation_patterns.json').read_text(encoding='utf-8'))
    extensions['compoundProductive'] = json.loads((ROOT/'data/compound_translation_patterns.json').read_text(encoding='utf-8'))
    extensions['roadmapProductive'] = json.loads((ROOT/'data/roadmap_lexical_rules.json').read_text(encoding='utf-8'))
    extensions['catalogCategories'] = json.loads((ROOT/'data/studio_categories.json').read_text(encoding='utf-8'))
    assert value('TRANSLATION_EXTENSIONS') == extensions
    usage = json.loads((ROOT / 'data/usage_examples.json').read_text(encoding='utf-8'))['examples']
    assert value('USAGE_EXAMPLES') == usage
    verified_compounds = json.loads((ROOT / 'data/verified_canonical_compounds.json').read_text(encoding='utf-8'))
    assert value('VERIFIED_CANONICAL_COMPOUNDS') == verified_compounds
    canon = json.loads((ROOT / 'data/canon_corpus.json').read_text(encoding='utf-8'))['units']
    assert value('CANON') == [dict(id=u['id'], neb=u['nrs'], ja=u['translationJa'], lit=u['title']) for u in canon]
    literary=json.loads((ROOT/'data/literary_sourcebook.json').read_text(encoding='utf-8'))
    bundled=value('LITERARY_BOOK')
    assert set(bundled['entries'])=={e['nrs'] for e in vocab}
    library=(ROOT/'web/library.html').read_text(encoding='utf-8')
    for entry in literary['entries']:
        assert bundled['entries'][entry['root']]['quote']==entry['quote']
        assert 'id="'+entry['anchor']+'"' in library
    standalone = (ROOT / 'web/standalone.html').read_text(encoding='utf-8')
    for path in ['web/data.js', 'web/incremental.js', 'web/workspace.js', 'web/app.js']:
        assert (ROOT / path).read_text(encoding='utf-8') in standalone, 'Missing embedded script: ' + path
    assert not re.search(r'<script\b[^>]*\bsrc=', standalone), 'Standalone requires external scripts'
    assert (ROOT / 'fonts/font_b64.txt').read_text(encoding='utf-8').strip() in standalone
    return dict(entries=len(vocab), rootEntries=1008, examples=len(canon), verifiedCompounds=len(verified_compounds['entries']), sourceInputsMatch=True, standaloneEmbedded=True)


if __name__ == '__main__':
    print(verify())
