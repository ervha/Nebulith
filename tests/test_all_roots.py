import hashlib
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'tools'))
from compare_all_roots import RUN, LANGUAGES, english_senses, translation_rows
from nebulith_data import entry_hash


class AllRootsComparison(unittest.TestCase):
    def test_parser_preserves_sense_pos_and_source_romanization(self):
        text = '''==English==
===Noun===
====Translations====
{{trans-top|financial institution}}
* French: {{tt+|fr|banque|f}}
* Japanese: {{t|ja|銀行|tr=ginkō}}, {{t|ja|未出典}}
* Latin: {{t-check|la|unverified}}
{{trans-bottom}}
===Verb===
====Translations====
{{trans-top|to incline}}
* French: {{t|fr|incliner}}
{{trans-bottom}}
==French==
===Noun===
{{trans-top|wrong language section}}{{t|de|wrong}}{{trans-bottom}}
'''
        rows = translation_rows(text)
        self.assertEqual(['banque','ginkō','incliner'], [r['sourceForm'] for r in rows])
        self.assertEqual('ginko',rows[1]['comparisonForm'])
        self.assertEqual('financial institution',rows[1]['sourceSense'])
        self.assertEqual('Verb',rows[2]['sourcePos'])

    def test_current_inventory_invalidates_changed_historical_entries(self):
        from review_state import screening_state
        vocab = json.loads((ROOT/'data/lexicon.json').read_text(encoding='utf-8'))['vocabulary']
        result = json.loads((RUN/'comparison.json').read_text(encoding='utf-8'))
        state = screening_state(vocab, result)
        self.assertEqual({e['id'] for e in vocab}, {e['lexiconId'] for e in state['entries']})
        historical = {r['lexiconId']: r for r in result['entries']}
        pending = {e['id'] for e in vocab if e['id'] not in historical or entry_hash(e) != historical[e['id']]['entryHash']}
        self.assertEqual(pending, set(state['pendingIds']))
        self.assertTrue(pending)
        self.assertFalse(state['screeningFresh'])
        self.assertFalse(state['semanticCertification'])
        for row in state['entries']:
            if row['lexiconId'] in pending:
                self.assertEqual('needs-source-and-semantic-review', row['status'])
                self.assertTrue(row['uncoveredSenses'])
        witness = dict(vocab[0], meaningEn='new meaning requiring new sources')
        changed = screening_state([witness], result)
        self.assertEqual([witness['id']], changed['pendingIds'])
        self.assertFalse(changed['semanticCertification'])

    def test_every_external_candidate_is_traceable_to_saved_source(self):
        sources=json.loads((RUN/'sources.json').read_text(encoding='utf-8'))
        historical=json.loads((RUN/'comparison.json').read_text(encoding='utf-8'))['entries']
        self.assertEqual(sorted({s for e in historical for s in english_senses(e)}),
                         sorted(s for b in sources['batches'] for s in b['titles']))
        self.assertFalse(any('error' in b for b in sources['batches']))
        for source in sources['batches']:
            if 'error' not in source:
                self.assertEqual(source['sha256'],hashlib.sha256((ROOT/source['snapshot']).read_bytes()).hexdigest())
        pages=json.loads((RUN/'translations.json').read_text(encoding='utf-8'))['pages']
        indexed={p['url']:p for p in pages}
        result=json.loads((RUN/'comparison.json').read_text(encoding='utf-8'))
        for c in result['candidates']:
            if c['language']=='en':continue
            page=indexed[c['source']]
            self.assertTrue(any(all(row[k]==c[k] for k in row) for row in page['rows']))
            self.assertEqual('source-sense-review-required',c['semanticStatus'])


if __name__=='__main__':unittest.main()
