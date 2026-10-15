"""Verify the distributable Web app against its current source data."""
import hashlib
import json
import re
from pathlib import Path
from studio_dictionary import dictionary_entries

ROOT = Path(__file__).resolve().parents[1]


def verify():
    meta = json.loads((ROOT / 'web/build-manifest.json').read_text(encoding='utf-8'))
    for path, digest in meta['sha256'].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, 'Stale Web input/output: ' + path
    script = (ROOT / 'web/data.js').read_text(encoding='utf-8')
    def value(name):
        return json.loads(re.search(r'^const ' + name + r' = (.+);$', script, re.M)[1])
    vocab = dictionary_entries(json.loads((ROOT / 'data/lexicon.json').read_text(encoding='utf-8'))['vocabulary'])
    keys = dict(id='id', r='nrs', p='pos', m='meaningJa', i='ipa', en='meaningEn', c='category', n='notes')
    assert value('VOCAB') == [{k: e[v] for k, v in keys.items()} for e in vocab]
    assert value('GRAMMAR_FRAMES') == json.loads((ROOT / 'data/corpus_rules.json').read_text(encoding='utf-8'))['frames']
    assert value('INPUT_RULES') == json.loads((ROOT / 'data/translation_input_rules.json').read_text(encoding='utf-8'))
    extensions = json.loads((ROOT / 'data/translation_extensions.json').read_text(encoding='utf-8'))
    extensions['productive'] = json.loads((ROOT / 'data/translation_patterns.json').read_text(encoding='utf-8'))
    assert value('TRANSLATION_EXTENSIONS') == extensions
    usage = json.loads((ROOT / 'data/usage_examples.json').read_text(encoding='utf-8'))['examples']
    assert value('USAGE_EXAMPLES') == usage
    canon = json.loads((ROOT / 'data/canon_corpus.json').read_text(encoding='utf-8'))['units']
    assert value('CANON') == [dict(id=u['id'], neb=u['nrs'], ja=u['translationJa'], lit=u['title']) for u in canon]
    standalone = (ROOT / 'web/standalone.html').read_text(encoding='utf-8')
    for path in ['web/data.js', 'web/incremental.js', 'web/workspace.js', 'web/app.js']:
        assert (ROOT / path).read_text(encoding='utf-8') in standalone, 'Missing embedded script: ' + path
    assert not re.search(r'<script\b[^>]*\bsrc=', standalone), 'Standalone requires external scripts'
    assert (ROOT / 'fonts/font_b64.txt').read_text(encoding='utf-8').strip() in standalone
    return dict(entries=len(vocab), rootEntries=1008, examples=len(canon), sourceInputsMatch=True, standaloneEmbedded=True)


if __name__ == '__main__':
    print(verify())
