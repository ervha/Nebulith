#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nebulith Dynamic LLM Multi-Agent Dialogue & Emergence Engine
============================================================
Facilitates dynamic multi-agent linguistic dialogues using LLMs (e.g. Google Colab
vLLM inference server, OpenAI API, Ollama) or deterministic offline fallback providers.
Automatically generates creative topics/communicative gaps, coins candidate neologisms,
submits them to the 6-Gate Strict Arbiter, and records approved candidates in the
emergent audit ledger (pending human verification).
"""

import os
import sys
import re
import json
import random
import argparse
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

# Fix Windows console encoding if needed
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

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
from llm_endpoint import LlmEndpointError, authorization_headers, resolve_api_key, resolve_base_url


# ==============================================================================
# Prompt Templates for LLM Multi-Agent Dialogue & Topic Generation
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
   - -ol (Perfective: poran -> porol = finish walking; fe porol = finished walking. Replace final an/en or final vowel with ol; otherwise append ol. Do not guess when roots collapse to the same form.)
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
}"""

TOPIC_GENERATION_PROMPT = """You are a creative linguist designing novel communicative situations for Nebulith, an astral-civilization constructed language.
Generate ONE novel dialogue topic and lexical gap where speakers need new compound words.
Themes can span:
- Celestial navigation (astrolabes, star occultations, orbital maps, solar lenses)
- Nature & elements (mountain mist, thermal springs, desert wind, aurora storms, forest soil)
- Crafts & materials (stone carving, lantern tuning, herbal distillation, loom weaving, crystal mirrors)
- Daily life & emotions (hearth cooking, market bargaining, twilight parting, shared relief, travel lodging)

Output strictly valid JSON with this exact schema:
{
  "domain": "Domain Name (e.g. 天文・観測工学, 日常・料理と火加減, 自然・気象現象, 旅・街道見送り)",
  "topic": "Concise Scenario Title (e.g. 早朝の港で霧が晴れる情景と出航の合図)",
  "communicative_need": "Specific lexical gap / concepts to coin (e.g. 朝霧が消え去る瞬間、船出の合図笛)"
}
"""


# ==============================================================================
# LLM Providers (Mock, OpenAI / Colab)
# ==============================================================================

class BaseLLMProvider:
    def generate_dialogue(self, topic: str, target_needs: list = None) -> dict:
        raise NotImplementedError()

    def generate_topic(self) -> dict:
        raise NotImplementedError()


class MockLLMProvider(BaseLLMProvider):
    """Deterministic offline fallback provider for reproducible testing and CI."""

    MOCK_TOPICS = [
        {"domain": "自然・海原と港", "topic": "港の朝露と砕ける波音、船旅への祈り", "communicative_need": "港で砕ける『波音・潮騒』、航海を『順風快走する』"},
        {"domain": "日常・園芸と草木", "topic": "朝露に濡れる若葉と土の匂い、水やりの語らい", "communicative_need": "水やりの後の『潤土・湿り土』、若葉を『愛で慈しむ』"},
        {"domain": "日常・台所と料理", "topic": "出汁の煮立ちと具材の炒め、味見の分かち合い", "communicative_need": "鍋で煮出す『出汁・煮汁』、弱火で『炒める』、仕上がりを『味見する』"},
        {"domain": "工芸・光学調律", "topic": "星石ランタンの波長調律と微光減衰の防止", "communicative_need": "古びた光石の『光曇り・波長濁り』、それを再び澄ませる『光調律する』"},
        {"domain": "医療・薬草手当て", "topic": "冷えた手足のさすり手当てと薬草湿布、滋養粥", "communicative_need": "痛む手足を『優しく撫でる・さする』、練り上げた『薬草湿布』、快復のための『滋養粥』"},
        {"domain": "天測・天体航海", "topic": "連星食における二重光条と重力レンズの観測", "communicative_need": "恒星食の『屈折光環・二重光条』、観測値を『軌道演算する』"},
        {"domain": "街道・旅立ち", "topic": "街道の分かれ道と夕暮れの宿り場、見送りの抱擁", "communicative_need": "旅の『携行荷物・背負い袋』、無事を祈り『見送る』、街道の『野営宿り場』"},
        {"domain": "市場・物々交換", "topic": "織布の肌触りと温もりの吟味、手頃な商い", "communicative_need": "布の『手触り・質感』、肌に馴染む『滑らかさ』、適正価格で『譲る・商う』"}
    ]

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
            "communicative_need": "水やりの後の『潤土・湿り土』と、若葉を『愛で慈しむ』の園芸語彙。",
            "agent_a": {"name": "Enna (庭番)", "role": "朝の草木に水を注ぐ"},
            "agent_b": {"name": "Soran (散策者)", "role": "庭の香りを楽しみに草花を愛でる"},
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
                            "meaningJa": "草木を愛でる、慈しみ育てる、優しく撫でる",
                            "meaningEn": "cherish flora, tend lovingly",
                            "morphemes": ["zel", "cyn"],
                            "etymology": "zel(草木・生) + cyn(愛・好)",
                            "category": "AI動的創発（日常・園芸）"
                        }
                    ]
                },
                {
                    "speaker": "Enna",
                    "nebulith": "Cylani el sola en *zelcyn! Falunst el sola de *darsol.",
                    "japanese": "愛で慈しむ太陽は美しい！太陽が潤土を照らしてほしい。",
                    "reused_words": ["zelcyn", "darsol"],
                    "proposed_words": []
                }
            ]
        }
    }

    def __init__(self):
        self._counter = 0

    def generate_topic(self) -> dict:
        topic = self.MOCK_TOPICS[self._counter % len(self.MOCK_TOPICS)]
        self._counter += 1
        return topic

    def generate_dialogue(self, topic: str, target_needs: list = None) -> dict:
        for k, sc in self.MOCK_LIBRARY.items():
            if k in topic:
                return sc
        # Default mock
        return self.MOCK_LIBRARY["海"]


class OpenAICompatibleProvider(BaseLLMProvider):
    """Connects to Google Colab vLLM server (via Cloudflare), OpenAI API, Ollama, etc."""

    def __init__(self, api_key: str = None, base_url: str = None, model: str = None, provider: str = None):
        self.base_url = resolve_base_url(base_url, provider=provider)
        self.api_key = resolve_api_key(self.base_url, api_key)
        self.model = model or os.getenv("OPENAI_MODEL", "Qwen/Qwen2.5-7B-Instruct")

    def _headers(self):
        headers = {"Content-Type": "application/json"}
        headers.update(authorization_headers(self.base_url, self.api_key or None))
        return headers

    def health_check(self) -> bool:
        """Checks if the remote/Colab inference endpoint is alive."""
        try:
            url = f"{self.base_url}/models"
            req = urllib.request.Request(url, headers=self._headers())
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                models = [m.get("id") for m in data.get("data", [])]
                print(f"[HEALTH-CHECK SUCCESS] Connected to {self.base_url} (Available models: {models or 'OK'})")
                return True
        except Exception as e:
            print(f"[HEALTH-CHECK WARN] Could not reach {self.base_url}/models: {e}")
            return False

    def generate_topic(self) -> dict:
        """Generates a novel situation and lexical gap using the LLM."""
        endpoint = f"{self.base_url}/chat/completions"
        headers = self._headers()
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a creative linguist. Output JSON only."},
                {"role": "user", "content": TOPIC_GENERATION_PROMPT}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.85,
            "max_tokens": 300
        }

        try:
            req = urllib.request.Request(endpoint, data=json.dumps(payload).encode("utf-8"), headers=headers)
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                raw = data["choices"][0]["message"]["content"]
                raw = re.sub(r"^```(?:json)?\s*", "", raw.strip(), flags=re.MULTILINE)
                raw = re.sub(r"\s*```$", "", raw.strip(), flags=re.MULTILINE)
                topic_data = json.loads(raw)
                return {
                    "domain": topic_data.get("domain", "日常・生活情景"),
                    "topic": topic_data.get("topic", "未知の情景と伝達課題"),
                    "communicative_need": topic_data.get("communicative_need", "表現したい新しい語彙概念")
                }
        except Exception as e:
            print(f"[WARN] Topic generation via LLM failed ({e}). Falling back to procedural topic.")
            return MockLLMProvider().generate_topic()

    def generate_dialogue(self, topic: str, target_needs: list = None) -> dict:
        endpoint = f"{self.base_url}/chat/completions"
        prompt_content = f"Generate an authentic Nebulith multi-agent dialogue about the topic: '{topic}'."
        if target_needs:
            prompt_content += f" Explicitly address these communicative lexical gaps: {target_needs}."
        prompt_content += f"\nFollow this exact JSON structure:\n{NEBULITH_FEW_SHOT_TEMPLATE}"

        headers = self._headers()
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": NEBULITH_SYSTEM_PROMPT},
                {"role": "user", "content": prompt_content}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.7,
            "max_tokens": 900
        }

        try:
            req = urllib.request.Request(endpoint, data=json.dumps(payload).encode("utf-8"), headers=headers)
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                content = data["choices"][0]["message"]["content"]
                content = re.sub(r"^```(?:json)?\s*", "", content.strip(), flags=re.MULTILINE)
                content = re.sub(r"\s*```$", "", content.strip(), flags=re.MULTILINE)
                return json.loads(content)
        except Exception as e:
            print(f"[ERROR] LLM dialogue generation failed ({e}). Falling back to MockLLMProvider.")
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
            "sur", "sir", "mer", "vel", "tas", "ser", "nod", "gov", "kel",
            "mor", "jyl", "puk", "pels", "kels", "vyrkels"
        }
        for m in self.known_extra_morphemes:
            self.arbiter.known_morphemes.add(m)

    def process_topic(self, topic: str, target_needs: list = None, promote: bool = False) -> dict:
        """Runs dynamic dialogue generation, parses neologisms, and evaluates via 6-Gate Strict Arbiter."""
        print(f"\n>>> Running Dynamic Multi-Agent Emergence on topic: '{topic}'...")
        scenario = self.provider.generate_dialogue(topic, target_needs)

        sid = scenario.get("scenario_id", f"LLM-{int(datetime.now().timestamp())}")
        domain = scenario.get("domain", "AI動的対話創発")
        title = scenario.get("title", topic)
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

        # Always record in the audit candidate ledger (data/emergent_lexicon_audit.json)
        # Note: We do NOT promote directly into actual dictionary (translation_extensions.json) without human audit.
        self._record_in_audit_ledger(approved_words, rejected_words, scenario)

        return {
            "scenario": scenario,
            "approved": approved_words,
            "rejected": rejected_words
        }

    def _record_in_audit_ledger(self, approved_records: list, rejected_records: list, scenario: dict):
        """Records scenarios and coined candidates into emergent_lexicon_audit.json as pending human review."""
        if not os.path.exists(AUDIT_LEDGER_PATH):
            return

        try:
            with open(AUDIT_LEDGER_PATH, "r", encoding="utf-8") as f:
                audit_ledger = json.load(f)

            # Record scenario
            if "scenarios" not in audit_ledger:
                audit_ledger["scenarios"] = []
            audit_ledger["scenarios"].append(scenario)

            # Record approved candidates (marked with human_audit_status: pending)
            if "approvedLexicon" not in audit_ledger:
                audit_ledger["approvedLexicon"] = []

            for rec in approved_records:
                nrs = rec.get("nrs", "").lower().replace("*", "")
                if not any(a.get("nrs") == nrs for a in audit_ledger["approvedLexicon"]):
                    rec["human_audit_status"] = "pending_review"
                    audit_ledger["approvedLexicon"].append(rec)

            # Record rejected candidates
            if "rejectedLog" not in audit_ledger:
                audit_ledger["rejectedLog"] = []
            for rej in rejected_records:
                audit_ledger["rejectedLog"].append(rej)

            # Update summary
            audit_ledger.setdefault("summary", {})
            audit_ledger["summary"]["totalScenarios"] = len(audit_ledger["scenarios"])
            audit_ledger["summary"]["totalApproved"] = len(audit_ledger["approvedLexicon"])
            audit_ledger["summary"]["totalRejected"] = len(audit_ledger["rejectedLog"])
            audit_ledger["summary"]["lastUpdatedAt"] = datetime.now().isoformat()

            with open(AUDIT_LEDGER_PATH, "w", encoding="utf-8") as f:
                json.dump(audit_ledger, f, ensure_ascii=False, indent=2)
            with open(EMERGENT_LOG_PATH, "w", encoding="utf-8") as f:
                json.dump(audit_ledger, f, ensure_ascii=False, indent=2)

            print(f"  [AUDIT LEDGER] Recorded {len(approved_records)} candidate(s) in emergent_lexicon_audit.json (Pending Human Audit)")
        except Exception as e:
            print(f"  [AUDIT LEDGER WARN] Failed to update ledger: {e}")

    def run_rounds(self, rounds: int = 1, base_topic: str = None) -> list:
        """Executes multiple automated rounds of dynamic topic generation and neologism coining."""
        print(f"\n=================================================================")
        print(f"  Starting Nebulith Autonomous Word Generation ({rounds} Rounds)")
        print(f"  Provider: {type(self.provider).__name__}")
        print(f"  Rule: Real dictionary inclusion requires human audit approval")
        print(f"=================================================================\n")

        all_results = []
        for r in range(1, rounds + 1):
            print(f"\n-------------------------------------------------------------")
            print(f"  [Round {r}/{rounds}] Generating Topic & Dialogue...")
            print(f"-------------------------------------------------------------")

            if base_topic and rounds == 1:
                topic_info = {
                    "domain": "指定トピック",
                    "topic": base_topic,
                    "communicative_need": base_topic
                }
            else:
                topic_info = self.provider.generate_topic()

            domain = topic_info.get("domain", "日常・情景")
            topic = topic_info.get("topic", "未知の対話")
            need = topic_info.get("communicative_need", "")
            print(f"  Domain: {domain}")
            print(f"  Topic : {topic}")
            print(f"  Need  : {need}")

            result = self.process_topic(f"[{domain}] {topic}", target_needs=[need] if need else None, promote=False)
            all_results.append({
                "round": r,
                "topic_info": topic_info,
                "result": result
            })

        # Summary report
        total_approved = sum(len(res["result"]["approved"]) for res in all_results)
        total_rejected = sum(len(res["result"]["rejected"]) for res in all_results)

        print(f"\n=================================================================")
        print(f"  Autonomous Emergence Complete ({rounds} Rounds Finished)")
        print(f"  Total Candidates Evaluated : {total_approved + total_rejected}")
        print(f"  Passed 6-Gate Strict Arbiter: {total_approved} (Held for Human Audit)")
        print(f"  Rejected by Strict Arbiter  : {total_rejected}")
        print(f"=================================================================")
        for res in all_results:
            r = res["round"]
            t = res["topic_info"]["topic"]
            app = [f"*{w['nrs']} ({w['meaningJa']})" for w in res["result"]["approved"]]
            print(f"  Round {r}: '{t}' -> Approved: {app or 'None'}")

        return all_results


# ==============================================================================
# CLI Entrypoint
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(description="Nebulith Dynamic LLM Multi-Agent Dialogue & Emergence")
    parser.add_argument("--rounds", "--count", "-n", dest="rounds", type=int, default=1, help="Number of automated generation rounds to execute")
    parser.add_argument("--topic", type=str, default=None, help="Explicit topic (if omitted, topic will be auto-generated)")
    parser.add_argument("--auto-topic", action="store_true", help="Explicitly enable automatic topic generation")
    parser.add_argument("--provider", choices=["mock", "openai", "colab"], default="colab", help="LLM Provider (default: colab)")
    parser.add_argument("--endpoint", type=str, default=None, help="LLM endpoint (or NEBULITH_LLM_ENDPOINT). Required for colab/self-hosted; no public default.")
    parser.add_argument("--model", type=str, default="Qwen/Qwen2.5-7B-Instruct", help="Model name (default: Qwen/Qwen2.5-7B-Instruct)")
    parser.add_argument("--api-key", type=str, default=None, help="API key. Self-hosted endpoints use NEBULITH_LLM_API_KEY; OPENAI_API_KEY is sent only to api.openai.com.")
    parser.add_argument("--health-check", action="store_true", help="Check remote LLM endpoint connectivity")
    args = parser.parse_args()

    # Determine provider
    if args.provider == "mock" and not args.endpoint:
        provider = MockLLMProvider()
    else:
        try:
            provider = OpenAICompatibleProvider(api_key=args.api_key, base_url=args.endpoint, model=args.model, provider=args.provider)
        except LlmEndpointError as exc:
            parser.error(str(exc))
        if args.health_check:
            provider.health_check()
            return

    pipeline = DynamicEmergencePipeline(provider)

    # Execute rounds
    pipeline.run_rounds(rounds=args.rounds, base_topic=args.topic)


if __name__ == "__main__":
    main()
