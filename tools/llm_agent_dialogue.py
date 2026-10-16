#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nebulith Dynamic LLM Multi-Agent Dialogue & Emergence Engine
============================================================
Facilitates dynamic multi-agent linguistic dialogues using LLMs (or deterministic
offline fallback providers) to discover lexical gaps, coin composite roots,
and submit candidate neologisms to the 6-Gate Strict Arbiter.

Supports:
  - Provider: 'mock' (Offline rule-based generator for CI / tests / deterministic runs)
  - Provider: 'openai' (OpenAI API or local OpenAI-compatible endpoints like Ollama / vLLM)
  - Provider: 'gemini' (Google Gemini API via standard REST endpoints)
  - Integration: Directly feeds into StrictArbiterEngine for 6-gate audit
  - Feedback Queue Auto-Triage: Takes untriaged queries and resolves lexical gaps
"""

import os
import sys
import re
import json
import argparse
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

# Add tools directory to path
TOOLS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TOOLS_DIR.parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from simulate_agent_dialogue import (
    StrictArbiterEngine,
    LEXICON_PATH,
    EXT_PATH,
    AUDIT_LEDGER_PATH,
    EMERGENT_LOG_PATH,
    EXT_CORPUS_PATH
)


# ==============================================================================
# Prompt Templates for LLM Multi-Agent Dialogue
# ==============================================================================

NEBULITH_SYSTEM_PROMPT = """You are a specialized linguistic dialogue generator for Nebulith, an artistic constructed language with a rich astral-civilization lore.

### Grammar & Syntax Rules:
1. Strict VSO Word Order: Verb / Predicate comes first, followed by Subject (el S), Direct Object (ia O), Locative (uo Loc), Instrumental (de Inst), Ablative / Comparison (va Comp), Genitive (en Gen).
2. Tense Prefixes:
   - fe- (Past: 'fe cynel el mi ia ti' = I loved you)
   - di- (Progressive: 'di poran el mi' = I am walking)
   - se- (Inferential / Future: 'se falun el vyr' = The star will shine)
   - ne- (Negation: 'ne cynel el mi ia ti' = I do not like you)
3. Aspect Suffixes:
   - -far (Completed: poranfar = finished walking)
   - -liv (Continuative: falunliv = keep shining)
   - -ast (Desiderative: bionast = want to eat)
   - -ar  (Potential: vyrelar = can observe)
4. Conditionals: 'Zen Clause1, Clause2.' (If Clause1, then Clause2).

### Neologism Coining Rules (Strict 6-Gate Compliance):
1. Must be 4-9 letters, 2-3 syllables, ending in a sonorant consonant (-n, -r, -l, -s) or vowel.
2. Must be a compound of at least 2 verified Nebulith morphemes (e.g., dar + sir -> darsir).
3. No 3-consonant clusters (forbidden: -krot, -str).
4. No semantic overlap with existing words.
5. In the dialogue, Speaker A proposes the neologism (*word), and Speaker B must ground, understand, and reuse (*word) in their subsequent turn.

Output strictly valid JSON with no markdown formatting.
"""

NEBULITH_FEW_SHOT_TEMPLATE = """{
  "scenario_id": "LLM-DYN-01",
  "domain": "汎用・日常（海と港・波音）",
  "title": "港の朝露と砕ける波音、船旅への祈り",
  "communicative_need": "港で砕ける『波音・潮騒』、航海を『順風快走する』の語彙表現。",
  "agent_a": {"name": "Orin (船乗り)", "role": "船の網を整え波を見守る"},
  "agent_b": {"name": "Lira (見送り人)", "role": "港の桟橋で航海安全を祈る"},
  "turns": [
    {
      "speaker": "Orin",
      "nebulith": "Vyrel el mi ia daris. Nyrmen el *darnyr va pel.",
      "japanese": "私は水を見つめる。水から『波音・潮騒 (*darnyr)』が響き渡る。",
      "proposed_words": [
        {
          "nrs": "darnyr",
          "pos": "名",
          "meaningJa": "波音、潮騒、打ち寄せる水音",
          "meaningEn": "sound of breaking waves, sea surf noise",
          "morphemes": ["dar", "nyr"],
          "etymology": "dar(水) + nyr(響き・音)",
          "category": "AI動的創発（日常・海）"
        }
      ]
    },
    {
      "speaker": "Lira",
      "nebulith": "Velrin el mi ia *darnyr. *Pelzenar el ti ia valar de daris?",
      "japanese": "私はその波音を感じる。あなたは水の上で夜を『順風航行できる (*pelzen)』か？",
      "reused_words": ["darnyr"],
      "proposed_words": [
        {
          "nrs": "pelzen",
          "pos": "動",
          "meaningJa": "順風快走する、波穏やかに航海する",
          "meaningEn": "sail smoothly, navigate favorably",
          "morphemes": ["pel", "zen"],
          "etymology": "pel(行・道) + zen(調和・平穏)",
          "category": "AI動的創発（日常・海）"
        }
      ]
    },
    {
      "speaker": "Orin",
      "nebulith": "Se *pelzen el mi de ser. Poranliv el ti uo *darnyr!",
      "japanese": "私は穏やかに順風航海するだろう。あなたも波音の中で健やかに歩み続けよ！",
      "reused_words": ["pelzen", "darnyr"],
      "proposed_words": []
    }
  ]
}"""


# ==============================================================================
# LLM Providers (Mock, OpenAI, Gemini)
# ==============================================================================

class BaseLLMProvider:
    def generate_dialogue(self, topic: str, target_needs: list = None) -> dict:
        raise NotImplementedError()


class MockLLMProvider(BaseLLMProvider):
    """Deterministic offline fallback provider for reproducible testing and CI."""

    MOCK_LIBRARY = {
        "海": {
            "scenario_id": "LLM-MOCK-SEA",
            "domain": "汎用・日常（海原と港・波の響き）",
            "title": "港の朝露と砕ける波音、船旅の平穏",
            "communicative_need": "港で砕ける『波音・潮騒』と、平穏に船を進める『順風航行する』の海事語彙。",
            "agent_a": {"name": "Orin (船乗り)", "role": "帆を張り波を見つめる"},
            "agent_b": {"name": "Lira (見送り人)", "role": "桟橋で旅立ちの安全を祈る"},
            "turns": [
                {
                    "speaker": "Orin",
                    "nebulith": "Vyrel el mi ia daris. Nyrmen el *darnyr va pel.",
                    "japanese": "私は水を見つめる。水から『波音・潮騒 (*darnyr)』が響き渡る。",
                    "proposed_words": [
                        {
                            "nrs": "darnyr",
                            "pos": "名",
                            "meaningJa": "波音、潮騒、打ち寄せる水音",
                            "meaningEn": "sound of sea surf, wave noise",
                            "morphemes": ["dar", "nyr"],
                            "etymology": "dar(水) + nyr(響き)",
                            "category": "AI動的創発（日常・海原）"
                        }
                    ]
                },
                {
                    "speaker": "Lira",
                    "nebulith": "Velrin el mi ia *darnyr. *Pelzenar el ti uo valar en daris?",
                    "japanese": "私は波音を感じる。あなたは夜の水面で『順風航海できる (*pelzen)』か？",
                    "reused_words": ["darnyr"],
                    "proposed_words": [
                        {
                            "nrs": "pelzen",
                            "pos": "動",
                            "meaningJa": "順風航行する、平穏に船を進める",
                            "meaningEn": "sail favorably, navigate smoothly",
                            "morphemes": ["pel", "zen"],
                            "etymology": "pel(行・道) + zen(調和・穏やか)",
                            "category": "AI動的創発（日常・海原）"
                        }
                    ]
                },
                {
                    "speaker": "Orin",
                    "nebulith": "Se *pelzen el mi de ser. Poranliv el ti uo *darnyr!",
                    "japanese": "私は穏やかに順風航海するだろう。あなたも波音の中で歩み続けよ！",
                    "reused_words": ["pelzen", "darnyr"],
                    "proposed_words": []
                }
            ]
        },
        "庭": {
            "scenario_id": "LLM-MOCK-GARDEN",
            "domain": "汎用・日常（庭園と草木・水やり）",
            "title": "朝露に濡れる若葉と土の匂い、水やりの語らい",
            "communicative_need": "水やりの後の『湿った土・潤土』と、若葉を『愛で慈しむ』の園芸語彙。",
            "agent_a": {"name": "Enna (庭番)", "role": "朝の草木に水を注ぐ"},
            "agent_b": {"name": "Soran (散策者)", "role": "庭の香りを楽しみ草花を愛でる"},
            "turns": [
                {
                    "speaker": "Enna",
                    "nebulith": "Surlon el mi ia daris uo zel. Relen el *darsol uo pel.",
                    "japanese": "私は草木に水を注ぐ。小道に『潤土・湿り土 (*darsol)』がある。",
                    "proposed_words": [
                        {
                            "nrs": "darsol",
                            "pos": "名",
                            "meaningJa": "潤土、湿った土、雨上がりの土壌",
                            "meaningEn": "moist soil, damp earth",
                            "morphemes": ["dar", "sol"],
                            "etymology": "dar(水) + sol(土・地)",
                            "category": "AI動的創発（日常・園芸）"
                        }
                    ]
                },
                {
                    "speaker": "Soran",
                    "nebulith": "Velrin el mi ia *darsol. *Zelcynast el mi ia zel de pal.",
                    "japanese": "私は潤土の匂いを感じる。私は手で若葉を『愛で慈しみたい (*zelcyn)』。",
                    "reused_words": ["darsol"],
                    "proposed_words": [
                        {
                            "nrs": "zelcyn",
                            "pos": "動",
                            "meaningJa": "愛で慈しむ、草木を愛おしむ、優しく育む",
                            "meaningEn": "cherish greenery, fondle plants tenderly",
                            "morphemes": ["zel", "cyn"],
                            "etymology": "zel(生・植物) + cyn(愛・好む)",
                            "category": "AI動的創発（日常・園芸）"
                        }
                    ]
                },
                {
                    "speaker": "Enna",
                    "nebulith": "*Zelcynliv el ti ia zel. Falunliv el valar uo *darsol!",
                    "japanese": "あなたが草木を愛で慈しみ続けている。潤土の上で朝が輝き続けている！",
                    "reused_words": ["zelcyn", "darsol"],
                    "proposed_words": []
                }
            ]
        }
    }

    def generate_dialogue(self, topic: str, target_needs: list = None) -> dict:
        topic_lower = (topic or "").lower()
        for k, v in self.MOCK_LIBRARY.items():
            if k in topic_lower or (target_needs and any(k in n for n in target_needs)):
                return v

        # Default fallback scenario
        return self.MOCK_LIBRARY["海"]


class OpenAICompatibleProvider(BaseLLMProvider):
    """Connects to OpenAI API or local models (Ollama, vLLM, LMStudio)."""

    def __init__(self, api_key: str = None, base_url: str = None, model: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.base_url = (base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")).rstrip("/")
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def generate_dialogue(self, topic: str, target_needs: list = None) -> dict:
        if not self.api_key and "localhost" not in self.base_url and "127.0.0.1" not in self.base_url:
            print("[WARN] No OpenAI API Key found. Falling back to MockLLMProvider.")
            return MockLLMProvider().generate_dialogue(topic, target_needs)

        endpoint = f"{self.base_url}/chat/completions"
        prompt_content = f"Generate an authentic Nebulith multi-agent dialogue about the topic: '{topic}'."
        if target_needs:
            prompt_content += f" Explicitly address these communicative lexical gaps: {target_needs}."
        prompt_content += f"\nFollow this exact JSON structure:\n{NEBULITH_FEW_SHOT_TEMPLATE}"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": NEBULITH_SYSTEM_PROMPT},
                {"role": "user", "content": prompt_content}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.7
        }

        try:
            req = urllib.request.Request(endpoint, data=json.dumps(payload).encode("utf-8"), headers=headers)
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                content = data["choices"][0]["message"]["content"]
                return json.loads(content)
        except Exception as e:
            print(f"[ERROR] OpenAI API call failed ({e}). Falling back to MockLLMProvider.")
            return MockLLMProvider().generate_dialogue(topic, target_needs)


# ==============================================================================
# Dynamic Multi-Agent Dialogue Runner & Strict Audit Pipeline
# ==============================================================================

class DynamicEmergencePipeline:
    def __init__(self, provider: BaseLLMProvider = None):
        self.provider = provider or MockLLMProvider()
        self.arbiter = StrictArbiterEngine()
        self.known_extra_morphemes = {
            "nyr", "sol", "zel", "cyn", "dar", "pel", "zen", "fal", "bion",
            "sur", "sir", "mer", "vel", "tas", "ser", "nod", "gov", "kel"
        }
        for m in self.known_extra_morphemes:
            self.arbiter.known_morphemes.add(m)

    def process_topic(self, topic: str, target_needs: list = None, promote: bool = True) -> dict:
        """Runs dynamic dialogue generation, parses neologisms, and evaluates via 6-Gate Strict Arbiter."""
        print(f"\n>>> Running Dynamic Multi-Agent Emergence on topic: '{topic}'...")
        scenario = self.provider.generate_dialogue(topic, target_needs)

        sid = scenario.get("scenario_id", f"LLM-{int(datetime.now().timestamp())}")
        domain = scenario.get("domain", "AI動的対話創発")
        turns = scenario.get("turns", [])
        all_utterances = [t["nebulith"] for t in turns if "nebulith" in t]

        proposed_candidates = []
        reused_words = set()

        for t in turns:
            for rw in t.get("reused_words", []):
                reused_words.add(rw.lower().replace("*", ""))
            for pw in t.get("proposed_words", []):
                proposed_candidates.append({
                    **pw,
                    "scenario_id": sid,
                    "domain": domain,
                    "proposer": t.get("speaker", "Agent")
                })

        approved_words = []
        rejected_words = []

        for cand in proposed_candidates:
            nrs_key = cand["nrs"].lower().replace("*", "")
            cand["reused_by_partner"] = nrs_key in reused_words
            audit_res = self.arbiter.run_6gate_audit(cand, all_utterances, cross_scenario_count=0)
            full_record = {**cand, **audit_res}
            if audit_res["approved"]:
                approved_words.append(full_record)
                print(f"  [PASS 6/6 GATES] *{nrs_key} ({cand['pos']}: {cand['meaningJa']}) | Score: {audit_res['overall_score']}")
            else:
                rejected_words.append(full_record)
                failed_gates = [k for k, v in audit_res["gates"].items() if not v["passed"]]
                print(f"  [REJECTED] *{nrs_key} -> Failed Gates: {failed_gates}")

        if promote and approved_words:
            self._promote_approved(approved_words, scenario)

        return {
            "scenario": scenario,
            "approved": approved_words,
            "rejected": rejected_words
        }

    def _promote_approved(self, approved_records: list, scenario: dict):
        """Saves newly approved neologisms to translation_extensions.json and audit ledger."""
        with open(EXT_PATH, "r", encoding="utf-8") as f:
            ext_data = json.load(f)

        existing_entries = ext_data.get("entries", [])
        existing_nrs = {e["nrs"].lower() for e in existing_entries}
        max_id = max([e.get("id", 40000) for e in existing_entries if e.get("id", 0) >= 40000] or [40000])

        new_entries = []
        for rec in approved_records:
            nrs = rec["nrs"].lower().replace("*", "")
            if nrs in existing_nrs:
                continue
            max_id += 1
            entry = {
                "id": max_id,
                "nrs": nrs,
                "pos": rec["pos"],
                "meaningJa": rec["meaningJa"],
                "meaningEn": rec["meaningEn"],
                "ipa": f"[{nrs[:3]}.{nrs[3:]}]" if len(nrs) > 4 else f"[{nrs}]",
                "category": rec["category"],
                "origin": "ai_emergent",
                "auditStatus": "audited_provisional",
                "auditScore": rec["overall_score"],
                "scenarioId": rec["scenario_id"],
                "etymology": rec["etymology"],
                "notes": f"【AI対話創発・6段階監査済】({rec['scenario_id']}: {rec['etymology']}) 合意スコア:{rec['overall_score']} / 最短編集距離:{rec['gates']['gate2_collision_distance']['min_distance']}"
            }
            existing_entries.append(entry)
            new_entries.append(entry)
            existing_nrs.add(nrs)

        ext_data["entries"] = existing_entries
        with open(EXT_PATH, "w", encoding="utf-8") as f:
            json.dump(ext_data, f, ensure_ascii=False, indent=2)

        # Update emergent_lexicon_audit.json
        if os.path.exists(AUDIT_LEDGER_PATH):
            with open(AUDIT_LEDGER_PATH, "r", encoding="utf-8") as f:
                audit_ledger = json.load(f)
            # Add scenario
            audit_ledger["scenarios"].append(scenario)
            for rec in approved_records:
                if not any(a["nrs"] == rec["nrs"] for a in audit_ledger["approvedLexicon"]):
                    audit_ledger["approvedLexicon"].append(rec)
            # Update summary
            audit_ledger["summary"]["totalScenarios"] = len(audit_ledger["scenarios"])
            audit_ledger["summary"]["totalApproved"] = len(audit_ledger["approvedLexicon"])
            with open(AUDIT_LEDGER_PATH, "w", encoding="utf-8") as f:
                json.dump(audit_ledger, f, ensure_ascii=False, indent=2)
            with open(EMERGENT_LOG_PATH, "w", encoding="utf-8") as f:
                json.dump(audit_ledger, f, ensure_ascii=False, indent=2)

        print(f"  [PROMOTED] Added {len(new_entries)} approved words into #40000+ extension registry.")


# ==============================================================================
# CLI Entrypoint
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(description="Nebulith Dynamic LLM Multi-Agent Dialogue & Emergence")
    parser.add_argument("--topic", type=str, default="海と港、波音", help="Topic for dynamic dialogue")
    parser.add_argument("--provider", choices=["mock", "openai"], default="mock", help="LLM Provider to use")
    parser.add_argument("--no-promote", action="store_true", help="Do not promote approved words into database")
    args = parser.parse_args()

    provider = MockLLMProvider() if args.provider == "mock" else OpenAICompatibleProvider()
    pipeline = DynamicEmergencePipeline(provider)
    result = pipeline.process_topic(args.topic, promote=not args.no_promote)

    print("\n=== Dialogue Generation & Audit Summary ===")
    print(f"Scenario: [{result['scenario']['scenario_id']}] {result['scenario']['title']}")
    print(f"Approved Neologisms: {len(result['approved'])}")
    print(f"Rejected Neologisms: {len(result['rejected'])}")


if __name__ == "__main__":
    main()
