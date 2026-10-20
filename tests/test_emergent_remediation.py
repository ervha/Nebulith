import hashlib
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from evidence_hash import recorded_digest_matches


def load(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


class EmergentRemediationChecks(unittest.TestCase):
    def test_withdrawn_approvals_keep_exact_original_records(self):
        ledger = load('data/emergent_lexicon_audit.json')
        snapshot = load(ledger['remediation']['archive'])
        self.assertEqual(ledger['remediation']['archiveSha256'], hashlib.sha256((ROOT / ledger['remediation']['archive']).read_bytes()).hexdigest())
        self.assertEqual([], ledger['approvedLexicon'])
        self.assertEqual(1020, ledger['summary']['totalPendingReview'])
        original = {r['id']: r for r in snapshot['approvedLexicon']}
        self.assertEqual(set(original), {r['id'] for r in ledger['candidates']})
        for row in ledger['candidates']:
            self.assertFalse(row['approved'])
            self.assertFalse(row['bookEligible'])
            self.assertEqual(original[row['id']], row['previousAudit'])

    def test_learning_entries_use_existing_meanings_not_fallback_coins(self):
        learning = load('data/everyday_vocabulary_review.json')
        canon = {r['id']: r for r in load(learning['source'])['vocabulary']}
        self.assertTrue(recorded_digest_matches(ROOT / learning['source'], learning['sourceSha256']))
        self.assertEqual(500, len({r['id'] for r in learning['entries']}))
        self.assertEqual(0, learning['newRoots'])
        for row in learning['entries']:
            for key, value in row.items():
                self.assertEqual(canon[row['id']][key], value)

    def test_legacy_generator_cannot_certify_forged_evidence(self):
        from simulate_agent_dialogue import StrictArbiterEngine
        with self.assertRaisesRegex(RuntimeError, 'retired'):
            StrictArbiterEngine().run_6gate_audit({'nrs': 'kelvas', 'reused_by_partner': True}, ['nonsense el kelvas'], 1)

    def test_print_artifacts_are_current_and_exclude_unreviewed_templates(self):
        manifest = load('audit/maintenance/current-publication.json')
        self.assertFalse(manifest['independentReviewGranted'])
        self.assertEqual('audit/maintenance/codex-build-20261016.json',manifest['previousManifest'])
        self.assertEqual(0, manifest['emergentPromoted'])
        self.assertEqual(500, manifest['learningEntries'])
        self.assertEqual(30, manifest['corpusUnits'])
        for path, expected in manifest['sha256'].items():
            self.assertTrue(recorded_digest_matches(ROOT / path, expected), path)
        html = (ROOT / 'docs/Codex_Astrolith_Canon_Scripture.html').read_text(encoding='utf-8')
        self.assertNotIn('監査検証完了', html)
        self.assertNotIn('kelvas', html)
        self.assertNotIn('Vyrel el mi ia *', html)
        self.assertTrue((ROOT / 'docs/Codex_Astrolith_Canon_Scripture.pdf').read_bytes().startswith(b'%PDF'))


if __name__ == '__main__':
    unittest.main()
