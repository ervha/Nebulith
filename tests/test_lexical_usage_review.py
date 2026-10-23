import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from lexical_usage_review import validate_usage_reviews


class LexicalUsageReviewChecks(unittest.TestCase):
    def setUp(self):
        read = lambda name: json.loads((ROOT / 'data' / name).read_text(encoding='utf-8'))
        self.reviews = read('lexical_usage_reviews.json')
        self.compounds = read('verified_canonical_compounds.json')
        self.rules = read('roadmap_lexical_rules.json')

    def test_source_and_usage_boundaries(self):
        self.assertEqual(10, validate_usage_reviews(self.reviews, self.compounds))
        grouped = lambda usage: {row['id'] for row in self.reviews['entries'] if row['usage'] == usage}
        self.assertEqual({r['id'] for r in self.rules['held']}, grouped('held'))
        self.assertEqual({r['id'] for r in self.rules['adjectives'] if not r['predicative']}, grouped('attributive_only'))
        self.assertEqual({31866}, grouped('frame_proposal'))

    def test_changed_source_requires_review(self):
        for field in ('pos', 'meaningJa', 'meaningEn', 'example_sentence', 'example_ja', 'morphemes'):
            with self.subTest(field=field):
                changed = copy.deepcopy(self.compounds)
                row = next(r for r in changed['entries'] if r['id'] == 31939)
                row[field] = ['other'] if field == 'morphemes' else 'changed'
                with self.assertRaisesRegex(ValueError, 're-review required'):
                    validate_usage_reviews(self.reviews, changed)

    def test_duplicate_or_approved_proposal_is_rejected(self):
        duplicate = copy.deepcopy(self.reviews)
        duplicate['entries'].append(duplicate['entries'][0])
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            validate_usage_reviews(duplicate, self.compounds)
        approved = copy.deepcopy(self.reviews)
        approved['entries'][0]['approved'] = True
        with self.assertRaisesRegex(ValueError, 'cannot grant canon approval'):
            validate_usage_reviews(approved, self.compounds)
