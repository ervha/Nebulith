import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from canonical_compound_validator import (
    load_canonical_inventory,
    load_canonical_morphemes,
    validate_candidate_entry,
)
from canonical_promotion_gateway import (
    REMEDIATION_SUMMARY_PATH,
    evaluate_promotion_readiness,
    simulate_promotion,
)
from curated_canonical_compounds import (
    BATCH_AUDIT_REPORT_PATH,
    VERIFIED_COMPOUNDS_PATH,
    build_and_verify_canonical_compounds,
)
from simulate_agent_dialogue import StrictArbiterEngine
from verify_web_bundle import verify as verify_web_bundle


class CanonicalCompoundValidatorTests(unittest.TestCase):
    def test_canonical_morphemes_are_strictly_standalone_lexicon_entries(self):
        canon = json.loads((ROOT / "data/lexicon.json").read_text(encoding="utf-8"))["vocabulary"]
        canon_roots = {r["nrs"].lower() for r in canon}
        morphemes = load_canonical_morphemes()
        self.assertGreater(len(morphemes), 200)
        for nrs, gloss in morphemes:
            self.assertIn(nrs, canon_roots)
            self.assertTrue(gloss)
        fake_bound_roots = {"kel", "vas", "pel", "nel", "sel", "mol", "tan"}
        loaded_set = {m[0] for m in morphemes}
        self.assertTrue(fake_bound_roots.isdisjoint(loaded_set - canon_roots))

    def test_strict_arbiter_known_morphemes_exclude_truncated_prefixes_and_fake_roots(self):
        arbiter = StrictArbiterEngine()
        self.assertEqual(arbiter.existing_roots, arbiter.known_morphemes)
        self.assertNotIn("kel", arbiter.known_morphemes)
        self.assertNotIn("pel", arbiter.known_morphemes)

    def test_verified_canonical_compounds_batches_1_to_81_have_zero_audit_flags(self):
        self.assertTrue(VERIFIED_COMPOUNDS_PATH.exists())
        self.assertTrue(BATCH_AUDIT_REPORT_PATH.exists())
        self.assertTrue(REMEDIATION_SUMMARY_PATH.exists())

        saved_dataset = json.loads(VERIFIED_COMPOUNDS_PATH.read_text(encoding="utf-8"))
        saved_report = json.loads(BATCH_AUDIT_REPORT_PATH.read_text(encoding="utf-8"))
        live = build_and_verify_canonical_compounds(write_files=False)

        self.assertEqual("ZERO_FLAGS_VERIFIED", saved_report["verdict"])
        self.assertEqual({}, saved_report["flagCounts"])
        self.assertEqual(883, saved_dataset["summary"]["totalEntries"])
        self.assertEqual(295, saved_dataset["summary"]["totalScenarios"])
        self.assertEqual(0, saved_dataset["summary"]["auditFlagCount"])
        self.assertEqual(883, saved_dataset["summary"]["remediatedLegacyCount"])
        self.assertEqual(saved_dataset["entries"], live["dataset"]["entries"])
        self.assertEqual(saved_report["entries"], live["auditReport"]["entries"])

        canon_by_nrs = {
            r["nrs"].lower(): r
            for r in json.loads((ROOT / "data/lexicon.json").read_text(encoding="utf-8"))["vocabulary"]
        }
        for entry in saved_dataset["entries"]:
            self.assertEqual([], entry["auditFlags"])
            self.assertGreaterEqual(len(entry["speakers"]), 2)
            self.assertEqual("".join(entry["morphemes"]), entry["nrs"])
            for m in entry["morphemes"]:
                self.assertIn(m, canon_by_nrs)

    def test_validator_rejects_non_standalone_and_fallback_defects(self):
        inventory = load_canonical_inventory()
        bad_candidate = {
            "id": 99999,
            "nrs": "kelvas",
            "pos": "動",
            "meaningJa": "日常の挨拶、木と広の身近な結びつき",
            "meaningEn": "everyday 挨拶 (kel-vas)",
            "morphemes": ["kel", "vas"],
            "scenario_id": "MISSING-SCEN",
            "example_sentence": "Poran el mi uo *kelvas de zen.",
            "example_ja": "私は穏やかに*kelvasへと歩む。",
        }
        res = validate_candidate_entry(bad_candidate, {}, inventory)
        self.assertFalse(res["valid"])
        expected_flags = {
            "constituent_not_standalone_dictionary_entry",
            "everyday_fallback_definition",
            "japanese_in_english_gloss",
            "untranslated_term_in_japanese_example",
            "verb_used_as_bare_case_complement_needs_rule",
            "missing_referenced_scenario",
            "two_speaker_reuse_not_demonstrated_in_referenced_scenario",
        }
        self.assertTrue(expected_flags.issubset(set(res["flags"])))

    def test_web_studio_and_valnes_dialogues_pdf_integration(self):
        bundle_res = verify_web_bundle()
        self.assertEqual(883, bundle_res["verifiedCompounds"])
        self.assertTrue(bundle_res["sourceInputsMatch"])

        html_path = ROOT / "docs/Valnes_dialogues.html"
        pdf_path = ROOT / "docs/Valnes_dialogues.pdf"
        md_path = ROOT / "docs/VALNES_DIALOGUES_COMPANION.md"
        self.assertTrue(html_path.exists())
        self.assertTrue(pdf_path.exists())
        self.assertTrue(md_path.exists())
        self.assertTrue(pdf_path.read_bytes().startswith(b"%PDF"))

        html_text = html_path.read_text(encoding="utf-8")
        self.assertIn("darfalun", html_text)
        self.assertIn("klorcalor", html_text)
        self.assertIn("alinzevil", html_text)
        self.assertIn("CANON-CONV-167", html_text)
        self.assertIn("CANON-COLAB-10", html_text)
        self.assertIn("CANON-COLAB-20", html_text)
        self.assertIn("CANON-COLAB-30", html_text)
        self.assertIn("CANON-COLAB-40", html_text)
        self.assertIn("CANON-COLAB-50", html_text)
        self.assertIn("CANON-COLAB-60", html_text)
        self.assertIn("CANON-COLAB-70", html_text)
        self.assertIn("CANON-COLAB-80", html_text)
        self.assertIn("CANON-COLAB-90", html_text)
        self.assertIn("CANON-COLAB-100", html_text)
        self.assertIn("CANON-COLAB-110", html_text)
        self.assertIn("CANON-COLAB-119", html_text)
        self.assertIn("CANON-UNIV-09", html_text)
        self.assertIn("domain-category-index", html_text)
        self.assertIn("constituent-root-index", html_text)

    def test_enhanced_translator_engines_handle_verified_compounds_and_clauses(self):
        proc = subprocess.run(
            ["node", "tests/verify_canonical_compound_translation.js"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=20,
        )
        self.assertEqual(0, proc.returncode, proc.stdout + proc.stderr)
        out = json.loads(proc.stdout.strip())
        self.assertTrue(out["r1"]["success"])
        self.assertIn("露光", out["r1"]["text"])
        self.assertIn("雫茶", out["r1"]["text"])
        self.assertIn("ので", out["r1"]["text"])
        self.assertTrue(out["r2"]["success"])
        self.assertIn("with you", out["r2"]["text"])
        self.assertIn("darfalun", out["r3Neb"].lower())
        self.assertTrue(out["r4"]["success"])
        self.assertIn("vyrcelar", out["r4"]["text"].lower())
        self.assertTrue(out.get("r5", {}).get("success", False))
        self.assertIn("vyrelast", out["r5"]["text"].lower())
        self.assertTrue(out.get("r6", {}).get("success", False))
        self.assertTrue(out.get("r7", {}).get("success", False))
        self.assertTrue(out.get("r8", {}).get("success", False))
        # Verify interrogative 'ro' and relative clause 'that'
        self.assertTrue(out.get("r9Ja", {}).get("success", False))
        self.assertIn("か？", out["r9Ja"]["text"])
        self.assertTrue(out.get("r9En", {}).get("success", False))
        self.assertIn("Do you", out["r9En"]["text"])
        self.assertTrue(out.get("r10", {}).get("success", False))
        self.assertIn("ro?", out["r10"]["text"])
        self.assertTrue(out.get("r11Ja", {}).get("success", False))
        self.assertTrue(out.get("r11En", {}).get("success", False))
        self.assertIn("that", out["r11En"]["text"])
        # Verify conditional clause 'if ... then ...'
        self.assertTrue(out.get("r12", {}).get("success", False))
        self.assertIn("Zen", out["r12"]["text"])
        # Verify concessive clause 'even if ...'
        self.assertTrue(out.get("r13", {}).get("success", False))
        self.assertIn("Tor", out["r13"]["text"])
        self.assertTrue(out.get("r13Ja", {}).get("success", False))
        self.assertIn("けれど", out["r13Ja"]["text"])
        self.assertTrue(out.get("r13En", {}).get("success", False))
        self.assertIn("Although", out["r13En"]["text"])
        # Verify temporal clause 'when / while ...'
        self.assertTrue(out.get("r14", {}).get("success", False))
        self.assertIn("Hav", out["r14"]["text"])
        self.assertTrue(out.get("r14While", {}).get("success", False))
        self.assertIn("Hav", out["r14While"]["text"])
        self.assertTrue(out.get("r14Ja", {}).get("success", False))
        self.assertIn("とき", out["r14Ja"]["text"])
        self.assertTrue(out.get("r14En", {}).get("success", False))
        self.assertIn("When", out["r14En"]["text"])
        # Verify purposive clause 'so that / in order that ...'
        self.assertTrue(out.get("r15", {}).get("success", False))
        self.assertIn("Sol", out["r15"]["text"])
        self.assertTrue(out.get("r15InOrder", {}).get("success", False))
        self.assertIn("Sol", out["r15InOrder"]["text"])
        self.assertTrue(out.get("r15Ja", {}).get("success", False))
        self.assertIn("ために", out["r15Ja"]["text"])
        self.assertTrue(out.get("r15En", {}).get("success", False))
        self.assertIn("So that", out["r15En"]["text"])
        # Verify comparative clause 'Poran el mi va ti' / 'Falani el zohar va vyr'
        self.assertTrue(out.get("r16Ja", {}).get("success", False))
        self.assertIn("より", out["r16Ja"]["text"])
        self.assertTrue(out.get("r16En", {}).get("success", False))
        self.assertIn("more than", out["r16En"]["text"])
        self.assertTrue(out.get("r16", {}).get("success", False))
        self.assertIn("va ti", out["r16"]["text"])
        self.assertTrue(out.get("r17", {}).get("success", False))
        self.assertIn("va vyr", out["r17"]["text"])
        # Verify reported speech / thought clause 'that ...' / 'ia ...'
        self.assertTrue(out.get("r18", {}).get("success", False))
        self.assertIn("ia", out["r18"]["text"])
        self.assertTrue(out.get("r18Ja", {}).get("success", False))
        self.assertIn("と", out["r18Ja"]["text"])
        self.assertTrue(out.get("r18En", {}).get("success", False))
        self.assertIn("that", out["r18En"]["text"])
        # Verify indirect question / Wh-clause 'where ...' / 'ia kauo ...'
        self.assertTrue(out.get("r19", {}).get("success", False))
        self.assertIn("ia kauo", out["r19"]["text"])
        self.assertTrue(out.get("r19Ja", {}).get("success", False))
        self.assertIn("どこへ", out["r19Ja"]["text"])
        self.assertIn("か", out["r19Ja"]["text"])
        self.assertTrue(out.get("r19En", {}).get("success", False))
        self.assertIn("where", out["r19En"]["text"])

    def test_promotion_gateway_requires_explicit_council_signoff(self):
        status = evaluate_promotion_readiness()
        self.assertTrue(status["mechanicallyReady"])
        self.assertEqual(883, status["candidateCount"])
        self.assertEqual(295, status["scenarioCount"])
        self.assertFalse(status["councilSignoffGranted"])
        self.assertEqual("HOLD_FOR_COUNCIL_SIGNOFF", status["status"])

        with self.assertRaises(PermissionError):
            evaluate_promotion_readiness(apply_promotion=True)

        approved = evaluate_promotion_readiness(council_signoff="COUNCIL-APPROVE-20261019")
        self.assertTrue(approved["councilSignoffGranted"])
        self.assertEqual("READY_FOR_PROMOTION", approved["status"])

        # Test official promotion application to staging ledger
        applied = evaluate_promotion_readiness(
            council_signoff="COUNCIL-APPROVE-20261020",
            apply_promotion=True,
        )
        self.assertEqual("PROMOTION_APPLIED_SUCCESSFULLY", applied["status"])
        self.assertEqual(883, applied["promotedCount"])
        self.assertEqual(1255, applied["totalExtensionsCount"])
        self.assertTrue((ROOT / applied["stagingFile"]).exists())

    def test_promotion_simulation_passes_without_disk_mutation(self):
        sim = simulate_promotion()
        self.assertTrue(sim["simulationPassed"])
        self.assertEqual(372, sim["existingExtensionsCount"])
        self.assertEqual(883, sim["promotedCandidateCount"])
        self.assertEqual(1255, sim["totalSimulatedExtensionsCount"])
        self.assertEqual(0, sim["idCollisions"])
        self.assertEqual(0, sim["rootCollisions"])
        self.assertEqual("PROMOTION_SIMULATION_SUCCESSFUL", sim["verdict"])


if __name__ == "__main__":
    unittest.main()
