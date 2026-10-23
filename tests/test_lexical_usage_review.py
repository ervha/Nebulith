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
        self.constituents = read('lexicon.json')['vocabulary']

    def test_source_and_usage_boundaries(self):
        self.assertEqual(10, validate_usage_reviews(self.reviews, self.compounds, self.constituents, self.rules))
        grouped = lambda usage: {row['id'] for row in self.reviews['entries'] if row['usage'] == usage}
        self.assertEqual({r['id'] for r in self.rules['held']}, grouped('held'))
        self.assertEqual({r['id'] for r in self.rules['adjectives'] if not r['predicative']}, grouped('attributive_only'))
        self.assertEqual({31866}, grouped('frame_proposal'))

    def test_constituent_meaning_drift_requires_review(self):
        for field in ('pos', 'meaningJa', 'meaningEn'):
            with self.subTest(field=field):
                changed = copy.deepcopy(self.constituents)
                next(row for row in changed if row['nrs'] == 'bion')[field] = 'changed'
                with self.assertRaisesRegex(ValueError, 'Constituent source changed'):
                    validate_usage_reviews(self.reviews, self.compounds, changed, self.rules)

    def test_decision_does_not_allow_unsupported_activation(self):
        rules = copy.deepcopy(self.rules)
        rules['held'] = [row for row in rules['held'] if row['id'] != 32000]
        with self.assertRaisesRegex(ValueError, 'held translation rules disagree'):
            validate_usage_reviews(self.reviews, self.compounds, self.constituents, rules)
        decisions = copy.deepcopy(self.reviews)
        next(row for row in decisions['entries'] if row['id'] == 32000)['usage'] = 'attributive_only'
        with self.assertRaisesRegex(ValueError, 'Decision and usage boundary disagree'):
            validate_usage_reviews(decisions, self.compounds)
        decisions = copy.deepcopy(self.reviews)
        decisions['entries'][0]['decision']['independentApproval'] = True
        with self.assertRaisesRegex(ValueError, 'Invalid application decision'):
            validate_usage_reviews(decisions, self.compounds)

    def test_changed_source_requires_review(self):
        for field in ('pos', 'meaningJa', 'meaningEn', 'example_sentence', 'example_ja', 'morphemes'):
            with self.subTest(field=field):
                changed = copy.deepcopy(self.compounds)
                row = next(r for r in changed['entries'] if r['id'] == 31939)
                row[field] = ['other'] if field == 'morphemes' else 'changed'
                with self.assertRaisesRegex(ValueError, 're-review required'):
                    validate_usage_reviews(self.reviews, changed)

    def test_related_source_drift_requires_review(self):
        for field in ('pos', 'meaningJa', 'meaningEn'):
            with self.subTest(field=field):
                changed = copy.deepcopy(self.constituents)
                next(row for row in changed if row['nrs'] == 'zyvil')[field] = 'changed'
                with self.assertRaisesRegex(ValueError, 'Related word source changed'):
                    validate_usage_reviews(self.reviews, self.compounds, changed, self.rules)

    def test_reformation_cannot_be_automatic_or_omit_meaning_boundary(self):
        for mutation, error in (
            (lambda r: r.update(automaticReplacement=True), 'Incomplete reformation'),
            (lambda r: r.update(unresolved=''), 'Incomplete reformation'),
            (lambda r: r['related'][0].update(difference=''), 'Invalid related meaning'),
            (lambda r: r['related'].append(copy.deepcopy(r['related'][0])), 'Invalid related meaning'),
        ):
            changed = copy.deepcopy(self.reviews)
            mutation(next(row for row in changed['entries'] if row['usage'] == 'held')['reformation'])
            with self.assertRaisesRegex(ValueError, error):
                validate_usage_reviews(changed, self.compounds, self.constituents, self.rules)

    def test_duplicate_or_approved_proposal_is_rejected(self):
        duplicate = copy.deepcopy(self.reviews)
        duplicate['entries'].append(duplicate['entries'][0])
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            validate_usage_reviews(duplicate, self.compounds)
        approved = copy.deepcopy(self.reviews)
        approved['entries'][0]['approved'] = True
        with self.assertRaisesRegex(ValueError, 'cannot grant canon approval'):
            validate_usage_reviews(approved, self.compounds)
