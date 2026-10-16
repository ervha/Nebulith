import subprocess
import hashlib
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from verify_web_bundle import verify


class WebStudioChecks(unittest.TestCase):
    def test_bundle_contains_current_dictionary_rules_and_offline_assets(self):
        result = verify()
        from studio_dictionary import dictionary_entries
        canonical=json.loads((ROOT/'data/lexicon.json').read_text(encoding='utf-8'))['vocabulary']
        self.assertEqual(len(dictionary_entries(canonical)), result['entries'])
        self.assertEqual(30, result['examples'])
        self.assertTrue(result['standaloneEmbedded'])

    def test_search_queue_and_exact_match_behaviors(self):
        result = subprocess.run(['node', 'tests/verify_studio.js'], cwd=ROOT,
                                capture_output=True, text=True, encoding='utf-8', timeout=20)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn('PASS: grammar dictionary search', result.stdout)

    def test_generated_grammar_and_rejection_cases(self):
        result = subprocess.run(['node', 'tests/verify_web_translation.js'], cwd=ROOT,
                                capture_output=True, text=True, encoding='utf-8', timeout=20)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_recovered_feedback_is_bound_to_original_requests(self):
        report = json.loads((ROOT / 'data/feedback_resolutions.json').read_text(encoding='utf-8'))
        requests = {}
        for source in report['sources']:
            raw = (ROOT / source['path']).read_bytes()
            self.assertEqual(source['sha256'], hashlib.sha256(raw).hexdigest())
            for r in json.loads(raw)['queue']:
                requests[(source['path'], r['id'])] = r['text']
        self.assertEqual(set(requests), {(r['source'], r['requestId']) for r in report['items']})
        for item in report['items']:
            self.assertEqual(requests[(item['source'],item['requestId'])], item['input'])

    def test_productive_inflections_and_argument_combinations(self):
        result = subprocess.run(['node', 'tests/verify_productive_translation.js'], cwd=ROOT,
                                capture_output=True, text=True, encoding='utf-8', timeout=45)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_storage_and_feedback_import_are_safe_and_repeatable(self):
        result = subprocess.run(['node', 'tests/verify_workspace.js'], cwd=ROOT,
                                capture_output=True, text=True, encoding='utf-8', timeout=20)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_workspace_ui_restart_and_import_workflow(self):
        result = subprocess.run(['node', 'tests/verify_workspace_ui.js'], cwd=ROOT,
                                capture_output=True, text=True, encoding='utf-8', timeout=20)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_shared_meaning_and_compositional_clauses(self):
        result = subprocess.run(['node', 'tests/verify_semantic_translation.js'], cwd=ROOT,
                                capture_output=True, text=True, encoding='utf-8', timeout=20)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_provisional_review_ledger_is_current_and_does_not_grant_approval(self):
        ledger=json.loads((ROOT/'data/language_review_ledger.json').read_text(encoding='utf-8'))
        self.assertEqual(ledger['sourceSha256'],hashlib.sha256((ROOT/'data/translation_extensions.json').read_bytes()).hexdigest())
        self.assertEqual(ledger['frameReview']['sha256'],hashlib.sha256((ROOT/'data/translation_patterns.json').read_bytes()).hexdigest())
        self.assertEqual(47,len(ledger['entries']))
        for entry in ledger['entries']:
            self.assertEqual('needs-independent-review',entry['status'])
            self.assertFalse(entry['adoptedIntoCanonical'])
