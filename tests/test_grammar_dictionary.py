import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from nebulith_data import FUNCTIONAL, CORRELATIVES
from studio_dictionary import dictionary_entries


class GrammarDictionaryChecks(unittest.TestCase):
    def test_all_specified_functional_and_correlative_tokens_are_searchable(self):
        roots = json.loads((ROOT / 'data/lexicon.json').read_text(encoding='utf-8'))['vocabulary']
        entries = dictionary_entries(roots)
        self.assertTrue((FUNCTIONAL | CORRELATIVES) <= {e['nrs'] for e in entries})
        for root in ['mi', 'ti', 'ri', 'miel', 'tiel', 'riel', 'miin', 'tiin', 'riin']:
            self.assertEqual(1, sum(e['nrs'] == root for e in entries))
        self.assertEqual(len(entries), len({e['id'] for e in entries}))
        self.assertEqual(len(entries), len({e['nrs'] for e in entries}))

    def test_collision_merging_preserves_root_identity_and_input_data(self):
        roots = json.loads((ROOT / 'data/lexicon.json').read_text(encoding='utf-8'))['vocabulary']
        before = json.dumps(roots, ensure_ascii=False)
        merged = {e['nrs']: e for e in dictionary_entries(roots)}
        for root in ['zen', 'tor', 'hav']:
            original = next(e for e in roots if e['nrs'] == root)
            self.assertEqual(original['id'], merged[root]['id'])
            self.assertTrue(merged[root]['meaningJa'].startswith(original['meaningJa']))
            self.assertIn('出典', merged[root]['notes'])
        self.assertEqual(before, json.dumps(roots, ensure_ascii=False))

    def test_unsettled_particle_meanings_are_explicit(self):
        grammar = json.loads((ROOT / 'data/grammar_dictionary.json').read_text(encoding='utf-8'))['entries']
        for root in ['ze', 'na', 'lo']:
            self.assertIn('未整備', next(e for e in grammar if e['nrs'] == root)['notes'])
