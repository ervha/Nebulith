import unittest
import json
import os
import sys
import copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from extended_corpus import validate_examples
from studio_dictionary import dictionary_entries

class ExtendedTranslationChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        corpus_path = os.path.join(base_dir, 'data', 'extended_corpus_v2.json')
        with open(corpus_path, 'r', encoding='utf-8') as f:
            cls.corpus = json.load(f)

    def test_corpus_structure(self):
        sentences = self.corpus.get('sentences', [])
        self.assertEqual(len(sentences), 23, "Should contain exactly 23 extended sentences")
        for s in sentences:
            self.assertTrue(s.get('id'), f"Sentence {s} must have an id")
            self.assertTrue(s.get('japanese'), f"Sentence {s} must have japanese text")
            self.assertTrue(s.get('nebulith'), f"Sentence {s} must have nebulith text")
            self.assertTrue(len(s.get('japanese_variants', [])) > 0, f"Sentence {s} must have variants")

    def test_invalid_additions_stay_held_and_cannot_be_bundled(self):
        held=json.loads((ROOT/'data/audit/held_extended_corpus.json').read_text(encoding='utf-8'))
        active={r['id'] for r in self.corpus['sentences']}
        self.assertEqual(5,len(held['sentences']))
        self.assertTrue(active.isdisjoint(r['id'] for r in held['sentences']))
        vocab=dictionary_entries(json.loads((ROOT/'data/lexicon.json').read_text(encoding='utf-8'))['vocabulary'])
        validate_examples(self.corpus['sentences'],vocab)
        for row in held['sentences']:
            with self.assertRaises(ValueError):validate_examples([row],vocab)
        corrupt=copy.deepcopy(self.corpus['sentences'][0]);corrupt['nebulith']+=' undefinedtoken'
        with self.assertRaisesRegex(ValueError,'Undefined'):validate_examples([corrupt],vocab)

    def test_vocabulary_consistency(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        lex_path = os.path.join(base_dir, 'data', 'lexicon.json')
        with open(lex_path, 'r', encoding='utf-8') as f:
            lex_data = json.load(f)
        
        vocab_nrs = {w.get('nrs', '').lower() for w in lex_data.get('vocabulary', [])}
        pronouns_and_grammar = {
            'el', 'ia', 'en', 'to', 'uo', 'de', 'ku', 'al', 'ni', 'va',
            'sen', 'hav', 'ne', 'ka', 'di', 'fe', 'se', 'lo', 'ze', 'na',
            'mi', 'ti', 'ri', 'mia', 'tia', 'ria',
            'celen', 'talen', 'kelen', 'keli', 'kauo', 'kano', 'sente'
        }
        
        for s in self.corpus.get('sentences', []):
            neb = s.get('nebulith', '').replace(',', '').replace('.', '').replace('!', '').replace('?', '').lower()
            words = neb.split()
            for w in words:
                self.assertTrue(
                    w in vocab_nrs or w in pronouns_and_grammar,
                    f"Word '{w}' in sentence {s['id']} must exist in lexicon or pronouns/grammar set"
                )

if __name__ == '__main__':
    unittest.main()
