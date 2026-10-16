#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nebulith Feedback Queue Auto-Triage Pipeline (Sprint 7)
=======================================================
Reads user feedback queue files exported from Nebulith Studio Web (or live
queue entries), classifies the lexical/syntactic gaps, executes dynamic AI
multi-agent dialogue to coin candidate neologisms, audits them via the 6-Gate
Strict Arbiter, promotes approved words into the #40001+ registry, and updates
the triage status of each queued item.
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TOOLS_DIR.parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from llm_agent_dialogue import DynamicEmergencePipeline, MockLLMProvider, OpenAICompatibleProvider
from simulate_agent_dialogue import StrictArbiterEngine, EXT_PATH, AUDIT_LEDGER_PATH


def triage_queue_file(queue_file_path: str, provider_name: str = "mock", promote: bool = True) -> dict:
    queue_path = Path(queue_file_path)
    if not queue_path.exists():
        raise FileNotFoundError(f"Feedback queue file not found: {queue_path}")

    with open(queue_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    items = data.get("queue", []) if isinstance(data, dict) and "queue" in data else data
    if not isinstance(items, list):
        items = [items]

    provider = MockLLMProvider() if provider_name == "mock" else OpenAICompatibleProvider()
    pipeline = DynamicEmergencePipeline(provider)

    triaged_results = []
    print(f"=== Starting Auto-Triage on {len(items)} Feedback Requests ===")

    for item in items:
        req_id = item.get("id", "req_unknown")
        req_type = item.get("type", "word")
        text = item.get("text", "")
        status = item.get("status", "untriaged")

        print(f"\n[Processing #{req_id}] Type: {req_type} | Text: '{text}' | Status: {status}")

        if status == "implemented":
            print("  -> Already implemented. Skipping.")
            triaged_results.append({**item, "triage_action": "already_implemented"})
            continue

        # Formulate communicative need & topic
        topic = f"{text}（生活・自然・情景の語彙）"
        target_needs = [text]

        emergence_res = pipeline.process_topic(topic, target_needs=target_needs, promote=promote)
        approved = emergence_res.get("approved", [])

        if approved:
            best_word = approved[0]
            print(f"  -> SUCCESS: Coined & Audited *{best_word['nrs']} (#{best_word.get('id', '40001+')})")
            triaged_results.append({
                **item,
                "status": "implemented",
                "cause": "vocabulary",
                "resolvedWith": {
                    "nrs": best_word["nrs"],
                    "pos": best_word["pos"],
                    "meaningJa": best_word["meaningJa"],
                    "meaningEn": best_word["meaningEn"],
                    "score": best_word["overall_score"],
                    "scenarioId": best_word["scenario_id"]
                },
                "triagedAt": datetime.now().isoformat()
            })
        else:
            print("  -> REVIEW NEEDED: No candidate passed 6-gate audit.")
            triaged_results.append({
                **item,
                "status": "review",
                "cause": "vocabulary",
                "rejectionDetails": emergence_res.get("rejected", []),
                "triagedAt": datetime.now().isoformat()
            })

    output_payload = {
        "schemaVersion": 2,
        "triagedAt": datetime.now().isoformat(),
        "source": str(queue_path),
        "totalItems": len(triaged_results),
        "implementedCount": sum(1 for i in triaged_results if i.get("status") == "implemented"),
        "reviewCount": sum(1 for i in triaged_results if i.get("status") == "review"),
        "queue": triaged_results
    }

    out_file = queue_path.with_name(f"{queue_path.stem}_triaged.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(output_payload, f, ensure_ascii=False, indent=2)

    print(f"\n=== Auto-Triage Complete ===")
    print(f"Total: {len(triaged_results)} | Implemented: {output_payload['implementedCount']} | Review: {output_payload['reviewCount']}")
    print(f"Output saved to: {out_file}")

    return output_payload


def main():
    parser = argparse.ArgumentParser(description="Nebulith Feedback Queue Auto-Triage Pipeline")
    parser.add_argument("queue_file", type=str, help="Path to exported feedback queue JSON file")
    parser.add_argument("--provider", choices=["mock", "openai"], default="mock", help="LLM Provider to use")
    parser.add_argument("--no-promote", action="store_true", help="Do not promote approved words into database")
    args = parser.parse_args()

    triage_queue_file(args.queue_file, provider_name=args.provider, promote=not args.no_promote)


if __name__ == "__main__":
    main()
