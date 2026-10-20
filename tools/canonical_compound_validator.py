#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nebulith Canonical Morpheme & Compound Validator (Phase 2)
==========================================================
Provides strict, non-forging validation of compound neologisms against the
actual standalone entries in data/lexicon.json and data/translation_extensions.json.
Ensures zero flags under tools/audit_emergent_ledger.py.
"""

import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_CHARS = set("aeiouylrmnszcjfvwhpbtdkg")
UNMARKED_CODAS = set("aeiouylrmns")


def load_canonical_inventory():
    canon = json.loads((ROOT / "data/lexicon.json").read_text(encoding="utf-8"))["vocabulary"]
    extensions = json.loads((ROOT / "data/translation_extensions.json").read_text(encoding="utf-8"))["entries"]
    grammar = json.loads((ROOT / "data/grammar_dictionary.json").read_text(encoding="utf-8"))["entries"]
    base = canon + extensions + grammar

    by_root = defaultdict(list)
    for row in base:
        by_root[row["nrs"].lower()].append(row)

    glossary = defaultdict(list)
    for row in base:
        for gloss in re.split(r"[、／/]", row.get("meaningJa", "")):
            if gloss.strip():
                glossary[gloss.strip()].append(row["nrs"])

    return {
        "canon": canon,
        "extensions": extensions,
        "grammar": grammar,
        "by_root": by_root,
        "glossary": glossary
    }


def load_canonical_morphemes(max_len: int = 5) -> list:
    """
    Return a deterministic list of (nrs, primary_gloss) pairs strictly from
    standalone entries in data/lexicon.json (excluding particles/pronouns).
    Replaces legacy hardcoded CORE_MORPHEMES.
    """
    canon = json.loads((ROOT / "data/lexicon.json").read_text(encoding="utf-8"))["vocabulary"]
    morphemes = []
    seen = set()
    for row in canon:
        nrs = row.get("nrs", "").lower().strip()
        pos = row.get("pos", "")
        if not nrs or nrs in seen:
            continue
        if len(nrs) < 2 or len(nrs) > max_len:
            continue
        if pos not in ("名", "動", "形", "副"):
            continue
        gloss = re.split(r"[、／/]", row.get("meaningJa", ""))[0].strip()
        morphemes.append((nrs, gloss))
        seen.add(nrs)
    return morphemes


def validate_candidate_entry(row: dict, scenarios_by_id: dict, inventory: dict = None) -> dict:
    """
    Validate a single candidate entry against all rules enforced by audit_emergent_ledger.py.
    Returns {"valid": bool, "flags": list[str], ...}.
    """
    if inventory is None:
        inventory = load_canonical_inventory()
    by_root = inventory["by_root"]
    glossary = inventory["glossary"]

    nrs = row.get("nrs", "").lower().strip()
    flags = []

    # 1. Phonotactics & Inventory
    if not re.fullmatch(r"[aeiouylrmnszcjfvwhpbtdkg]{4,9}", nrs):
        flags.append("invalid_inventory_or_length")
    if not re.search(r"[aeiouy]", nrs) or re.search(r"[^aeiouy]{3,}|[aeiouy]{3,}", nrs):
        flags.append("vowel_or_cluster_failure")
    if not nrs or nrs[-1] not in UNMARKED_CODAS:
        flags.append("marked_coda_requires_review")

    # 2. Collision check
    if nrs in by_root:
        flags.append("exact_live_dictionary_collision")

    # 3. Concatenative standalone morphology
    morphs = [m.lower().strip() for m in row.get("morphemes", [])]
    if len(morphs) < 2 or "".join(morphs) != nrs:
        flags.append("nonconcatenative_formation_needs_rule")
    missing = [m for m in morphs if m not in by_root]
    if missing:
        flags.append("constituent_not_standalone_dictionary_entry")

    # 4. Semantic & Gloss checks
    ja = row.get("meaningJa", "").strip()
    en = row.get("meaningEn", "").strip()
    if not ja or "身近な結びつき" in ja or "の調和" in ja:
        flags.append("everyday_fallback_definition")
    if "統合作用" in ja or "固有現象" in ja:
        flags.append("specialized_fallback_definition")
    if "の日常表現" in ja or "の様態" in ja:
        flags.append("gloss_uniqueness_by_suffix")
    if not en or re.search(r"[\u3041-\u3093\u30a1-\u30f6\u4e00-\u9fa0]", en):
        flags.append("japanese_in_english_gloss")

    overlap = {
        g.strip(): glossary[g.strip()]
        for g in re.split(r"[、／/]", ja)
        if g.strip() in glossary
    }
    if overlap:
        flags.append("exact_live_gloss_overlap_review")

    # 5. Example sentence & Japanese translation checks
    ex_neb = row.get("example_sentence", "").strip()
    ex_ja = row.get("example_ja", "").strip()
    if not ex_ja:
        flags.append("missing_japanese_example")
    if re.search(r"[a-z]{3}", ex_ja, re.I):
        flags.append("untranslated_term_in_japanese_example")

    if row.get("pos") == "動" and re.search(r"\b(?:ia|uo)\s+\*?" + re.escape(nrs) + r"\b", ex_neb, re.I):
        flags.append("verb_used_as_bare_case_complement_needs_rule")

    # 6. Scenario & Two-Speaker Reuse Evidence
    evidence = scenarios_by_id.get(row.get("scenario_id"), [])
    if not evidence:
        flags.append("missing_referenced_scenario")
    pattern = re.compile(r"\b" + re.escape(nrs) + r"(?:far|liv|ast|ar|cor|iin)?\b", re.I)
    turns = [
        t for s in evidence for t in s.get("turns", [])
        if pattern.search(t.get("nebulith", ""))
    ]
    speakers = sorted({t.get("speaker", "") for t in turns if t.get("speaker")})
    if len(speakers) < 2:
        flags.append("two_speaker_reuse_not_demonstrated_in_referenced_scenario")

    example_template = re.sub(r"\*?\b" + re.escape(nrs) + r"\b", "<TERM>", ex_neb, flags=re.I)

    return {
        "valid": len(flags) == 0,
        "flags": flags,
        "speakers": speakers,
        "missing_constituents": missing,
        "gloss_overlaps": overlap,
        "example_template": example_template
    }


def audit_candidate_batch(candidates: list, scenarios: list) -> dict:
    """
    Run full batch validation using the exact criteria of tools/audit_emergent_ledger.py,
    plus batch-internal duplicate root / duplicate ID / gloss overlap checks.
    """
    inventory = load_canonical_inventory()
    scenarios_by_id = defaultdict(list)
    for s in scenarios:
        scenarios_by_id[s["scenario_id"]].append(s)

    root_groups = defaultdict(list)
    batch_glosses = defaultdict(list)
    details = []

    for row in candidates:
        nrs = row["nrs"].lower().strip()
        root_groups[nrs].append(row["id"])
        res = validate_candidate_entry(row, scenarios_by_id, inventory)
        flags = list(res["flags"])

        # Also check batch-internal gloss collision
        for g in re.split(r"[、／/]", row.get("meaningJa", "")):
            gs = g.strip()
            if not gs:
                continue
            if gs in batch_glosses:
                if "exact_batch_gloss_overlap" not in flags:
                    flags.append("exact_batch_gloss_overlap")
            batch_glosses[gs].append(nrs)

        details.append({
            "id": row["id"],
            "nrs": nrs,
            "meaningJa": row.get("meaningJa", ""),
            "meaningEn": row.get("meaningEn", ""),
            "pos": row.get("pos", ""),
            "morphemes": row.get("morphemes", []),
            "scenario_id": row.get("scenario_id", ""),
            "flags": flags,
            "missingStandaloneConstituents": res["missing_constituents"],
            "exactGlossOverlaps": res["gloss_overlaps"],
            "referencedScenarioSpeakers": res["speakers"],
            "exampleTemplate": res["example_template"]
        })

    duplicate_roots = {r: ids for r, ids in root_groups.items() if len(ids) > 1}
    duplicate_ids = {str(i): n for i, n in Counter(r["id"] for r in candidates).items() if n > 1}
    flag_counts = dict(sorted(Counter(f for d in details for f in d["flags"]).items()))
    all_clean = len(flag_counts) == 0 and not duplicate_roots and not duplicate_ids

    return {
        "auditVersion": 2,
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "verdict": "ZERO_FLAGS_VERIFIED" if all_clean else "FLAGS_DETECTED",
        "counts": {
            "rows": len(candidates),
            "uniqueRoots": len(root_groups),
            "uniqueIds": len({r["id"] for r in candidates}),
            "scenarios": len(scenarios),
            "flaggedEntries": sum(1 for d in details if d["flags"])
        },
        "flagCounts": flag_counts,
        "duplicateRoots": duplicate_roots,
        "duplicateIds": duplicate_ids,
        "exampleTemplates": dict(Counter(d["exampleTemplate"] for d in details)),
        "entries": details
    }
