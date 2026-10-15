import copy
import hashlib
import json
import os
import re
import subprocess
import sys
import unittest
import shutil
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from nebulith_data import corpus_semantic_pending, entry_hash, expected_ipa, normalize_ipa, validate_corpus
from audit_reviews import coda_review, glyph_review
from false_friend_detector import check_false_friends
from verify_audit_archive import verify
from fontTools.ttLib import TTFont


class RemediationChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.vocab = json.loads((ROOT / 'data/lexicon.json').read_text(encoding='utf-8'))['vocabulary']
        cls.corpus = json.loads((ROOT / 'data/canon_corpus.json').read_text(encoding='utf-8'))
        cls.codas = json.loads((ROOT / 'data/audit/coda_reviews.json').read_text(encoding='utf-8'))

    def test_all_ipa_matches_declared_sound_rules(self):
        self.assertEqual([], [r['id'] for r in self.vocab if normalize_ipa(r['ipa']) != expected_ipa(r['nrs'])])
        self.assertEqual(len(self.vocab), len({normalize_ipa(r['ipa']) for r in self.vocab}))

    def test_corpus_references_and_changed_id_detection(self):
        self.assertEqual([], validate_corpus(self.corpus, self.vocab))
        bad = copy.deepcopy(self.corpus)
        token = next(t for t in bad['units'][0]['tokens'] if t.get('lexiconId') == 754)
        token['lexiconId'] = 172
        self.assertTrue(validate_corpus(bad, self.vocab))

    def test_corpus_surface_drift_is_detected(self):
        bad = copy.deepcopy(self.corpus)
        bad['units'][0]['nrs'] += ' dolin'
        self.assertTrue(validate_corpus(bad, self.vocab))

    def test_unsupported_nominal_passive_is_rejected(self):
        bad = copy.deepcopy(self.corpus)
        bad['units'][0]['nrs'] = 'Revyr'
        bad['units'][0]['tokens'] = [{'id': 'bad', 'surface': 'revyr', 'kind': 'derivation',
                                     'stemId': 62, 'prefix': 're', 'suffix': ''}]
        self.assertTrue(validate_corpus(bad, self.vocab))

    def test_unattested_semantic_approval_is_pending(self):
        bad = copy.deepcopy(self.corpus)
        for u in bad['units']:
            u['review']['status'] = 'approved'
            u['review'].pop('reviewedAgainstDependenciesHash', None)
        self.assertEqual(len(bad['units']), len(corpus_semantic_pending(bad)))

    def test_coda_categories_are_not_automatic_approval(self):
        records = copy.deepcopy(self.codas)
        for row in records['entries']:
            row['decision'] = 'pending'
        result = coda_review(self.vocab, records)
        self.assertEqual(160, len(result['pending']))
        self.assertEqual([], result['approved'])
        self.assertIsNone(result['complianceRate'])
        self.assertFalse(result['complete'])

    def test_coda_missing_stale_and_unsubstantiated_reviews(self):
        for kind in ['missing', 'stale', 'unsubstantiated', 'duplicate']:
            bad = copy.deepcopy(self.codas)
            if kind == 'missing':
                bad['entries'].pop()
            elif kind == 'stale':
                bad['entries'][0]['reviewedAgainstEntryHash'] = 'old'
            elif kind == 'duplicate':
                bad['entries'].append(bad['entries'][0])
            else:
                bad['entries'][0]['decision'] = 'approved'
            result = coda_review(self.vocab, bad)
            self.assertFalse(result['complete'], kind)
            self.assertTrue(result['errors'] or result['missing'], kind)

    def test_coda_review_bound_to_meaning(self):
        changed = copy.deepcopy(self.vocab)
        row = next(r for r in changed if r['id'] == self.codas['entries'][0]['lexiconId'])
        row['meaningJa'] = 'changed concept'
        self.assertTrue(coda_review(changed, self.codas)['errors'])

    def test_earth_distance_two_short_word_and_substrings(self):
        # Same-meaning examples that the old detector missed.
        cases = [('ser', 'hand'), ('sunnyzz', 'sun'), ('breadzz', 'bread')]
        for nrs, concept in cases:
            result = check_false_friends([{'id': 1, 'nrs': nrs, 'meaningEn': concept, 'meaningJa': 'fixture'}])
            self.assertTrue(result, nrs)
        self.assertFalse(check_false_friends([{'id': 1, 'nrs': 'breadzz', 'meaningEn': 'unrelated concept', 'meaningJa': 'fixture'}]))

    def test_glyph_review_requires_real_comparison(self):
        font = TTFont(ROOT / 'fonts/Nebulith-Regular.ttf')
        digest = hashlib.sha256((ROOT / 'fonts/Nebulith-Regular.ttf').read_bytes()).hexdigest()
        reviews = json.loads((ROOT / 'data/audit/glyph_reviews.json').read_text(encoding='utf-8'))
        result = glyph_review(font, digest, reviews)
        self.assertEqual(0, len(result['pending']))
        self.assertEqual(85, len(result['approved']))
        self.assertEqual({'space','.notdef'},set(result['functional']))
        self.assertTrue({'A', 'a', 'S', 's', 'U', 'u', 'J', 'j'} <= set(result['approved']))
        self.assertEqual([], result['rejected'])
        for r in reviews['entries']:
            r['decision'] = 'approved'
        self.assertFalse(glyph_review(font, digest, reviews)['complete'])
        self.assertTrue(glyph_review(font, 'new-font', reviews)['errors'])

    def test_original_documents_and_seals_preserved(self):
        self.assertEqual(5, verify()['originalDocuments'])

    def test_relocated_document_links(self):
        for path in (ROOT / 'audit/docs').glob('*.md'):
            for href in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
                if '://' not in href and not href.startswith('#'):
                    self.assertTrue((path.parent / unquote(href).split('#')[0]).exists(), (path.name, href))

    def test_cli_refuses_existing_evidence_directory(self):
        path = ROOT / 'audit/2026-10-15-reaudit-02/evidence.json'
        before = path.read_bytes()
        result = subprocess.run([sys.executable, 'tools/run_standard_audit.py', '--output',
                                 'audit/2026-10-15-reaudit-02'], cwd=ROOT, capture_output=True)
        self.assertNotEqual(0, result.returncode)
        self.assertEqual(before, path.read_bytes())

    def test_cli_rejects_output_outside_audit(self):
        result = subprocess.run([sys.executable, 'tools/run_standard_audit.py', '--output',
                                 'docs/should-not-exist'], cwd=ROOT, capture_output=True)
        self.assertEqual(2, result.returncode)
        self.assertFalse((ROOT / 'docs/should-not-exist').exists())

    def test_live_collector_reports_incomplete_reviews_instead_of_success(self):
        env = dict(os.environ, PYTHONIOENCODING='utf-8')
        env.pop('AUDIT_OUT_DIR', None)
        result = subprocess.run([sys.executable, 'tools/run_standard_audit.py'], cwd=ROOT,
                                env=env, text=True, encoding='utf-8', capture_output=True)
        self.assertEqual(2, result.returncode, result.stdout+result.stderr)
        output = Path(re.search(r'Evidence saved to: (.+)', result.stdout)[1].strip())
        generated_run = output.parent.resolve()
        self.assertEqual(ROOT / 'audit/runs', generated_run.parent)
        self.assertRegex(generated_run.name,r'^\d{4}-\d{2}-\d{2}-\d{6}-[a-f0-9]{8}$')
        self.addCleanup(shutil.rmtree, generated_run)
        evidence = json.loads(output.read_text(encoding='utf-8'))
        self.assertEqual('Warn', evidence['scorecard']['CHK-04']['status'])
        self.assertEqual('Reference', evidence['scorecard']['CHK-08']['status'])
        self.assertEqual('Fail', evidence['scorecard']['CHK-08']['historicalDiagnostic'])
        self.assertEqual('Pass', evidence['scorecard']['CHK-12']['status'])
        self.assertEqual('Pass', evidence['scorecard']['CHK-15']['status'])
        self.assertEqual([], evidence['field_differences'])
        self.assertEqual([], evidence['ipa_mapping_mismatches'])
        self.assertEqual([], evidence['category_metadata_errors'])
        self.assertTrue(evidence['canon_validation']['spec_sync'])
        self.assertTrue(evidence['canon_validation']['web_sync'])

    def test_corpus_review_is_bound_to_meaning_and_frames(self):
        self.assertEqual([], corpus_semantic_pending(self.corpus))
        changed = copy.deepcopy(self.vocab)
        next(r for r in changed if r['id'] == 906)['meaningJa'] = '別の語義'
        self.assertTrue(corpus_semantic_pending(self.corpus, changed))
        rules = json.loads((ROOT / 'data/corpus_rules.json').read_text(encoding='utf-8'))
        rules['version'] = 'changed'
        self.assertEqual(len(self.corpus['units']), len(corpus_semantic_pending(self.corpus, self.vocab, rules)))

    def test_individual_codas_and_sourced_collision_repair(self):
        from earth_comparison import load_and_compare
        result = coda_review(self.vocab, self.codas)
        self.assertTrue(result['complete'])
        self.assertEqual((33, 127), (len(result['approved']), len(result['rejected'])))
        self.assertAlmostEqual(881/1008, result['complianceRate'])
        sourced = load_and_compare(self.vocab)
        self.assertEqual([], sourced['errors'])
        self.assertEqual([], sourced['confirmed'])
        self.assertEqual([], sourced['pending'])
        self.assertEqual(7, len(sourced['ignored']))
        self.assertEqual(87, sourced['reviewed_entry_count'])
        old = copy.deepcopy(self.vocab)
        stone = next(r for r in old if r['id'] == 285)
        stone['nrs'] = 'talis'
        # A changed root cannot inherit the approval of its source-concept link.
        self.assertTrue(load_and_compare(old)['errors'])
        self.assertEqual('talisum', next(r for r in self.vocab if r['id'] == 119)['nrs'])

    def test_distance_candidates_need_individual_both_condition_review(self):
        from earth_comparison import compare
        registry = json.loads((ROOT / 'data/audit/earth_sources.json').read_text(encoding='utf-8'))
        rows = [json.loads(s) for s in (ROOT / 'data/audit/earth_lexicon.jsonl').read_text(encoding='utf-8').splitlines()]
        links = json.loads((ROOT / 'data/audit/earth_concept_links.json').read_text(encoding='utf-8'))
        reviews = json.loads((ROOT / 'data/audit/earth_candidate_reviews.json').read_text(encoding='utf-8'))
        unreviewed = compare(self.vocab, registry, rows, links)
        self.assertEqual(7, len(unreviewed['pending']))
        self.assertEqual([], unreviewed['confirmed'])
        bad = copy.deepcopy(reviews)
        bad['entries'][0]['decision'] = 'change'
        self.assertTrue(compare(self.vocab, registry, rows, links, bad)['errors'])
        bad['entries'][0]['formSimilar'] = True
        self.assertEqual(1, len(compare(self.vocab, registry, rows, links, bad)['confirmed']))
        bad['entries'][0]['entryHash'] = 'stale'
        self.assertTrue(compare(self.vocab, registry, rows, links, bad)['errors'])

    def test_source_mapping_avoids_homograph_and_part_of_speech_false_matches(self):
        links = json.loads((ROOT / 'data/audit/earth_concept_links.json').read_text(encoding='utf-8'))['entries']
        pairs = {(r['lexiconId'], r['conceptId']) for r in links}
        for pair in [(519, 'swadesh-207:199'), (82, 'swadesh-207:143'),
                     (251, 'swadesh-207:107'), (670, 'swadesh-207:137')]:
            self.assertNotIn(pair, pairs)
        self.assertIn((898, 'swadesh-207:199'), pairs)
        self.assertEqual('veiran', next(r for r in self.vocab if r['id'] == 945)['nrs'])
        self.assertEqual('fervolan', next(r for r in self.vocab if r['id'] == 439)['nrs'])

    def test_glyph_approval_rejects_missing_or_changed_comparison_evidence(self):
        font = TTFont(ROOT / 'fonts/Nebulith-Regular.ttf')
        digest = hashlib.sha256((ROOT / 'fonts/Nebulith-Regular.ttf').read_bytes()).hexdigest()
        data = json.loads((ROOT / 'data/audit/glyph_reviews.json').read_text(encoding='utf-8'))
        for key, value in [('outlineSha256', 'changed'), ('comparisonReference', 'audit/comparisons/missing.html#glyph-u')]:
            bad = copy.deepcopy(data)
            next(r for r in bad['entries'] if r['glyph'] == 'u')[key] = value
            self.assertTrue(glyph_review(font, digest, bad)['errors'])

    def test_glyph_review_scope_and_full_investigation(self):
        font = TTFont(ROOT / 'fonts/Nebulith-Regular.ttf')
        digest = hashlib.sha256((ROOT / 'fonts/Nebulith-Regular.ttf').read_bytes()).hexdigest()
        data = json.loads((ROOT / 'data/audit/glyph_reviews.json').read_text(encoding='utf-8'))
        self.assertTrue(all(r['investigated'] and r['reason'] and r['styleInspection'] for r in data['entries']))
        data['comparisonScope'] = 'cross-script'
        self.assertTrue(glyph_review(font, digest, data)['errors'])

    def test_functional_verdict_cannot_exempt_a_letter(self):
        font = TTFont(ROOT / 'fonts/Nebulith-Regular.ttf')
        digest = hashlib.sha256((ROOT / 'fonts/Nebulith-Regular.ttf').read_bytes()).hexdigest()
        data = json.loads((ROOT / 'data/audit/glyph_reviews.json').read_text(encoding='utf-8'))
        row=next(r for r in data['entries'] if r['glyph']=='i')
        row['decision']='functional'
        row['functionalEvidence']={'fontSha256':digest,'positiveAdvance':True}
        self.assertTrue(glyph_review(font,digest,data)['errors'])


if __name__ == '__main__':
    unittest.main()
