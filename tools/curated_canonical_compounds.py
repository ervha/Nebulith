#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 3 & Phase 5: Curated Canonical Compound Batch Generator & Ledger Evaluator
================================================================================
Constructs 60 strictly verified everyday and specialized compound words across
20 multi-turn two-speaker dialogue scenarios (Batches 1-5) using ONLY standalone
canonical roots from data/lexicon.json, with explicit traceability remapping
from legacy pending candidates in data/emergent_lexicon_audit.json.
Verifies 0 flags via canonical_compound_validator.py and records them cleanly.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from canonical_compound_validator import (
    audit_candidate_batch,
    load_canonical_inventory,
    validate_candidate_entry,
)

VERIFIED_COMPOUNDS_PATH = ROOT / "data/verified_canonical_compounds.json"
BATCH_AUDIT_REPORT_PATH = ROOT / "audit/maintenance/canonical-compounds-batch1-20261019.json"

# 20 Authentic Two-Speaker Scenarios (3 words each = 60 words across Batches 1-5)
CURATED_SCENARIOS = [
    {
        "scenario_id": "CANON-CONV-01",
        "batch": "Batch 1",
        "domain": "日常・朝の目覚めと茶の支度",
        "title": "朝露の窓辺と薬草茶の湯気",
        "communicative_need": "朝露の輝き、朝の白湯・煎じ茶、朝の平穏なひとときを語り合う。",
        "agent_a": {
            "name": "Yura",
            "role": "朝の窓を開ける写字生"
        },
        "agent_b": {
            "name": "Sev",
            "role": "炉で茶を淹れる灯守"
        },
        "turns": [
            {
                "speaker": "Yura",
                "nebulith": "Leras el mi ia lerel uo valar. Falun el darfalun uo velas.",
                "japanese": "私は朝に扉を開ける。葉の上で露光（朝露の煌めき）が光る。"
            },
            {
                "speaker": "Sev",
                "nebulith": "Vyrel el mi ia darfalun. Bion el miel ia darterin uo vorn. Relen el havsirin al miel.",
                "japanese": "私も朝露の煌めきを見つめる。私たちは部屋で雫茶（澄んだ朝茶）を飲もう。私たちに静かなひとときがある。"
            },
            {
                "speaker": "Yura",
                "nebulith": "Bionast el mi ia darterin. Cynel el mi ia havsirin en valar.",
                "japanese": "私は澄んだ朝茶を飲みたい。私は朝の静かなひとときを愛する。"
            }
        ],
        "words": [
            {
                "nrs": "darfalun",
                "pos": "名",
                "meaningJa": "露光、朝露の煌めき、光る水滴",
                "meaningEn": "dew-gleam, glistening morning dewdrop, luminous droplet",
                "morphemes": [
                    "dar",
                    "falun"
                ],
                "etymology": "dar(しずく・朝露) + falun(光・輝き)",
                "category": "16. 日常・自然・気象",
                "example_sentence": "Falun el darfalun uo velas.",
                "example_ja": "葉の上で朝露の煌めきが光る。"
            },
            {
                "nrs": "darterin",
                "pos": "名",
                "meaningJa": "雫茶、澄んだ朝茶、湧き水の煎じ茶",
                "meaningEn": "clear morning tea, spring-water herbal brew",
                "morphemes": [
                    "dar",
                    "terin"
                ],
                "etymology": "dar(しずく・水滴) + terin(温かい煎じ茶)",
                "category": "12. 食文化・料理・飲食",
                "example_sentence": "Bion el miel ia darterin uo vorn.",
                "example_ja": "私たち二人は部屋で澄んだ朝茶を飲む。"
            },
            {
                "nrs": "havsirin",
                "pos": "名",
                "meaningJa": "静かなひととき、安らぎの刻、平穏な時間",
                "meaningEn": "peaceful moment, quiet hour, tranquil time",
                "morphemes": [
                    "hav",
                    "sirin"
                ],
                "etymology": "hav(時・瞬間) + sirin(平穏・安らぎ)",
                "category": "13. 精神・感情・内省",
                "example_sentence": "Relen el havsirin al miel.",
                "example_ja": "私たち二人に静かなひとときがある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-02",
        "batch": "Batch 1",
        "domain": "日常・食卓と温かい食事",
        "title": "共同炊事場の滋養汁と果実の糧",
        "communicative_need": "滋養のある温かいスープ、栄養豊かな木の実、食卓の歓びを表現する。",
        "agent_a": {
            "name": "Sev",
            "role": "共同炊事場の料理番"
        },
        "agent_b": {
            "name": "Toa",
            "role": "港から戻った舟守"
        },
        "turns": [
            {
                "speaker": "Sev",
                "nebulith": "Toren el ti va larar. Neran el ti ia nerdarel ul nervorin uo nerom.",
                "japanese": "あなたは港から戻ってきたね。調理室で滋養スープと滋養果実を食べなさい。"
            },
            {
                "speaker": "Toa",
                "nebulith": "Neran el mi ia nerdarel ul nervorin de cynur. Toren el nerelir al sylim en mi.",
                "japanese": "私は感謝とともに滋養スープと滋養果実を食べる。私の心に食の歓びが満ちてくる。"
            },
            {
                "speaker": "Sev",
                "nebulith": "Saren el mi. Relen el nerelir uo govan en miin.",
                "japanese": "私は微笑む。私たちの家に食の歓びがある。"
            }
        ],
        "words": [
            {
                "nrs": "nerdarel",
                "pos": "名",
                "meaningJa": "滋養スープ、具だくさんの温汁、栄養煮込み汁",
                "meaningEn": "nourishing soup, hearty broth, rich stew",
                "morphemes": [
                    "ner",
                    "darel"
                ],
                "etymology": "ner(滋養・食材) + darel(スープ・温煮汁)",
                "category": "12. 食文化・料理・飲食",
                "example_sentence": "Neran el ti ia nerdarel uo nerom.",
                "example_ja": "あなたは調理室で滋養スープを食べる。"
            },
            {
                "nrs": "nervorin",
                "pos": "名",
                "meaningJa": "滋養果実、熟した保存果、食卓の木の実",
                "meaningEn": "nourishing fruit, ripe table berry, wholesome orchard fruit",
                "morphemes": [
                    "ner",
                    "vorin"
                ],
                "etymology": "ner(滋養・食材) + vorin(果実・木の実)",
                "category": "12. 食文化・料理・飲食",
                "example_sentence": "Neran el mi ia nervorin de cynur.",
                "example_ja": "私は感謝とともに滋養果実を食べる。"
            },
            {
                "nrs": "nerelir",
                "pos": "名",
                "meaningJa": "食の歓び、団欒の満腹感、食事の幸せ",
                "meaningEn": "joy of dining, satisfaction of a shared meal",
                "morphemes": [
                    "ner",
                    "elir"
                ],
                "etymology": "ner(滋養・食物) + elir(喜び・多幸感)",
                "category": "12. 食文化・料理・飲食",
                "example_sentence": "Toren el nerelir al sylim en mi.",
                "example_ja": "私の心に食の歓びが訪れる。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-03",
        "batch": "Batch 1",
        "domain": "日常・住まいと木工家具",
        "title": "木組みの椅子と小部屋の休息",
        "communicative_need": "木製の腰掛け椅子、木造の住まい、夜の寝室での休息を語る。",
        "agent_a": {
            "name": "Neri",
            "role": "標本を整理する採集師"
        },
        "agent_b": {
            "name": "Yura",
            "role": "帳面を綴じる写字生"
        },
        "turns": [
            {
                "speaker": "Neri",
                "nebulith": "Soran el ti ia pamel uo veltasel. Sirin el velgovan uo kym.",
                "japanese": "あなたは木の腰掛け椅子で冊子を書き留めているね。木造の住まいは夜に静まり返っている。"
            },
            {
                "speaker": "Yura",
                "nebulith": "Cynel el mi ia veltasel ul velgovan. Tymisast el mi uo kymvorn.",
                "japanese": "私は木の腰掛け椅子と木造の住まいが気に入っている。私は寝室で眠りたい。"
            },
            {
                "speaker": "Neri",
                "nebulith": "Poran el ti to kymvorn. Se tymis el ti de sirin.",
                "japanese": "あなたは寝室へ行きなさい。穏やかに眠れるだろう。"
            }
        ],
        "words": [
            {
                "nrs": "veltasel",
                "pos": "名",
                "meaningJa": "木の腰掛け椅子、木製スツール、木組みの座席",
                "meaningEn": "wooden chair, timber stool, wooden seat",
                "morphemes": [
                    "vel",
                    "tasel"
                ],
                "etymology": "vel(木・樹木) + tasel(椅子・座席)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Soran el ti ia pamel uo veltasel.",
                "example_ja": "あなたは木の腰掛け椅子で冊子を書き留める。"
            },
            {
                "nrs": "velgovan",
                "pos": "名",
                "meaningJa": "木造の住まい、木の家屋、林間の家",
                "meaningEn": "wooden house, timber dwelling, woodland home",
                "morphemes": [
                    "vel",
                    "govan"
                ],
                "etymology": "vel(木・樹木) + govan(家・住まい)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Sirin el velgovan uo kym.",
                "example_ja": "木造の住まいは夜に静かだ。"
            },
            {
                "nrs": "kymvorn",
                "pos": "名",
                "meaningJa": "寝室、夜の私室、休息の間",
                "meaningEn": "bedroom, night chamber, sleeping room",
                "morphemes": [
                    "kym",
                    "vorn"
                ],
                "etymology": "kym(夜・闇) + vorn(部屋・私室)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Tymisast el mi uo kymvorn.",
                "example_ja": "私は寝室で眠りたい。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-04",
        "batch": "Batch 1",
        "domain": "日常・街歩きと庭の散策",
        "title": "土の歩道と木陰の庭",
        "communicative_need": "土の散歩道、木陰の広場、白い小花について話す。",
        "agent_a": {
            "name": "Toa",
            "role": "街を歩く舟守"
        },
        "agent_b": {
            "name": "Neri",
            "role": "庭の手入れをする採集師"
        },
        "turns": [
            {
                "speaker": "Toa",
                "nebulith": "Poran el mi uo talporan to velar. Vyrel el mi ia alinvelin uo veltalom.",
                "japanese": "私は土の歩道を通って庭へ歩く。私は木立の広場で白花を見つめる。"
            },
            {
                "speaker": "Neri",
                "nebulith": "Toren el ti uo talporan. Falun el alinvelin uo veltalom de dar.",
                "japanese": "あなたは土の歩道を通って来たね。木立の広場で白花がしずくによって輝く。"
            }
        ],
        "words": [
            {
                "nrs": "talporan",
                "pos": "名",
                "meaningJa": "土の歩道、踏み固めた小道、野の散歩道",
                "meaningEn": "earthen walkway, unpaved footpath, country trail",
                "morphemes": [
                    "tal",
                    "poran"
                ],
                "etymology": "tal(大地・土) + poran(歩く・進む)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Poran el mi uo talporan to velar.",
                "example_ja": "私は土の歩道を通って庭へ歩く。"
            },
            {
                "nrs": "alinvelin",
                "pos": "名",
                "meaningJa": "白花、純白の草花、白い小花",
                "meaningEn": "white blossom, pure white flower",
                "morphemes": [
                    "alin",
                    "velin"
                ],
                "etymology": "alin(白い・純白の) + velin(花)",
                "category": "8. 植物・森林・菌類",
                "example_sentence": "Vyrel el mi ia alinvelin uo veltalom.",
                "example_ja": "私は木立の広場で白花を見つめる。"
            },
            {
                "nrs": "veltalom",
                "pos": "名",
                "meaningJa": "木立の広場、並木原、木陰の平地",
                "meaningEn": "tree-lined meadow, shaded clearing, grove plain",
                "morphemes": [
                    "vel",
                    "talom"
                ],
                "etymology": "vel(木・樹木) + talom(平原・大地)",
                "category": "6. 地球自然・地形・地質",
                "example_sentence": "Falun el alinvelin uo veltalom de dar.",
                "example_ja": "木立の広場で白花がしずくによって輝く。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-05",
        "batch": "Batch 1",
        "domain": "日常・手仕事と文具・道具",
        "title": "木箱の整理と今日の日記",
        "communicative_need": "木製の小箱、今日の手記帳、木組みの扉について会話する。",
        "agent_a": {
            "name": "Yura",
            "role": "記録を整理する写字生"
        },
        "agent_b": {
            "name": "Sev",
            "role": "道具を点検する灯守"
        },
        "turns": [
            {
                "speaker": "Yura",
                "nebulith": "Leras el mi ia vellerel ul velkypal. Soran el mi ia hanopamel de kirel.",
                "japanese": "私は木の扉と木箱を開ける。私は筆で今日の手記帳を書き留める。"
            },
            {
                "speaker": "Sev",
                "nebulith": "Vyrel el mi ia velkypal ul hanopamel. Vymin el vellerel ia vorn en miel.",
                "japanese": "私は木箱と今日の手記帳を見る。木の扉が私たちの部屋を守っている。"
            }
        ],
        "words": [
            {
                "nrs": "velkypal",
                "pos": "名",
                "meaningJa": "木箱、木製の小箱、木組みの収納匣",
                "meaningEn": "wooden box, timber casket, wooden storage chest",
                "morphemes": [
                    "vel",
                    "kypal"
                ],
                "etymology": "vel(木・樹木) + kypal(箱・小箱)",
                "category": "15. 工芸・道具・物質",
                "example_sentence": "Leras el mi ia vellerel ul velkypal.",
                "example_ja": "私は木の扉と木箱を開ける。"
            },
            {
                "nrs": "hanopamel",
                "pos": "名",
                "meaningJa": "今日の手記帳、当日の日誌、本日の控え帳",
                "meaningEn": "today's journal, daily logbook, current day notebook",
                "morphemes": [
                    "hano",
                    "pamel"
                ],
                "etymology": "hano(今日・現在) + pamel(本・手記ノート)",
                "category": "15. 工芸・道具・物質",
                "example_sentence": "Soran el mi ia hanopamel de kirel.",
                "example_ja": "私は筆で今日の手記帳を書き留める。"
            },
            {
                "nrs": "vellerel",
                "pos": "名",
                "meaningJa": "木の扉、木戸、木組みの戸口",
                "meaningEn": "wooden door, timber gate, wooden doorway",
                "morphemes": [
                    "vel",
                    "lerel"
                ],
                "etymology": "vel(木・樹木) + lerel(扉・ドア)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Vymin el vellerel ia vorn en miel.",
                "example_ja": "木の扉が私たち二人の部屋を守る。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-06",
        "batch": "Batch 1",
        "domain": "日常・夜空の観察と語らい",
        "title": "銀色の月光と夜の対話",
        "communicative_need": "夜の空、銀色の星明かり、夜の静かな語らいを表現する。",
        "agent_a": {
            "name": "Yura",
            "role": "観測院の写字生"
        },
        "agent_b": {
            "name": "Toa",
            "role": "夜番の舟守"
        },
        "turns": [
            {
                "speaker": "Yura",
                "nebulith": "Celan el miel ia kymcelen. Falun el tynivyr uo novar.",
                "japanese": "私たちは夜空を見上げる。天頂で銀星が輝いている。"
            },
            {
                "speaker": "Toa",
                "nebulith": "Vyrel el mi ia kymcelen ul tynivyr. Calun el miel ia kymfenor uo larar.",
                "japanese": "私は夜空と銀星を見つめる。私たちは港で夜語り（静かな夜の話し声）を交わす。"
            },
            {
                "speaker": "Yura",
                "nebulith": "Cynel el mi ia kymfenor ku ti.",
                "japanese": "私はあなたとの夜語りを愛おしく思う。"
            }
        ],
        "words": [
            {
                "nrs": "kymcelen",
                "pos": "名",
                "meaningJa": "夜空、夜の天蓋、闇の蒼穹",
                "meaningEn": "night sky, nocturnal firmament, dark heavens",
                "morphemes": [
                    "kym",
                    "celen"
                ],
                "etymology": "kym(夜・闇) + celen(空・天蓋)",
                "category": "1. 天体・宇宙・天文",
                "example_sentence": "Celan el miel ia kymcelen.",
                "example_ja": "私たち二人は夜空を見上げる。"
            },
            {
                "nrs": "tynivyr",
                "pos": "名",
                "meaningJa": "銀星、白銀の星明かり、銀色に輝く星",
                "meaningEn": "silver star, silvery starlight, gleaming orb",
                "morphemes": [
                    "tyni",
                    "vyr"
                ],
                "etymology": "tyni(銀色の・白銀の) + vyr(星・光点)",
                "category": "1. 天体・宇宙・天文",
                "example_sentence": "Falun el tynivyr uo novar.",
                "example_ja": "天頂で銀星が輝く。"
            },
            {
                "nrs": "kymfenor",
                "pos": "名",
                "meaningJa": "夜語り、夜のひそやかな語らい、夜更けの話し声",
                "meaningEn": "night talk, quiet evening discourse, late-night conversation",
                "morphemes": [
                    "kym",
                    "fenor"
                ],
                "etymology": "kym(夜・闇) + fenor(話す・語る)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Calun el miel ia kymfenor uo larar.",
                "example_ja": "私たち二人は港で夜語りを交わす。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-07",
        "batch": "Batch 1",
        "domain": "日常・健康と休息の気遣い",
        "title": "生薬のしずくと安眠の配慮",
        "communicative_need": "大地の活力、薬草の雫薬、心地よい夜の眠りを気遣う。",
        "agent_a": {
            "name": "Neri",
            "role": "薬草を調合する採集師"
        },
        "agent_b": {
            "name": "Sev",
            "role": "疲れを癒やす灯守"
        },
        "turns": [
            {
                "speaker": "Neri",
                "nebulith": "Zyvan el mi ia kylat en ti de talzyvas. Bion el ti ia darzyvil.",
                "japanese": "私は大地の生気によってあなたの疲れを癒やす。水薬（薬草雫）を飲みなさい。"
            },
            {
                "speaker": "Sev",
                "nebulith": "Bion el mi ia darzyvil. Toren el kymtymis al mi de talzyvas.",
                "japanese": "私は水薬を飲む。大地の生気のおかげで私に夜眠り（深い安眠）が訪れる。"
            },
            {
                "speaker": "Neri",
                "nebulith": "Sirin el kymtymis. Revir el ti uo seno.",
                "japanese": "夜眠りは穏やかだ。あなたは明日に回復して目覚める。"
            }
        ],
        "words": [
            {
                "nrs": "talzyvas",
                "pos": "名",
                "meaningJa": "大地の生気、土の養生力、自然の健やかさ",
                "meaningEn": "earth vitality, natural restorative vigor, grounding health",
                "morphemes": [
                    "tal",
                    "zyvas"
                ],
                "etymology": "tal(大地・土壌) + zyvas(健康・活力)",
                "category": "4. 人体・生理・医療",
                "example_sentence": "Zyvan el mi ia kylat en ti de talzyvas.",
                "example_ja": "私は大地の生気によってあなたの疲労を癒やす。"
            },
            {
                "nrs": "darzyvil",
                "pos": "名",
                "meaningJa": "水薬、薬草の雫、煎じ薬液",
                "meaningEn": "liquid medicine, herbal drops, healing tincture",
                "morphemes": [
                    "dar",
                    "zyvil"
                ],
                "etymology": "dar(しずく・水滴) + zyvil(薬・処方生薬)",
                "category": "4. 人体・生理・医療",
                "example_sentence": "Bion el ti ia darzyvil.",
                "example_ja": "あなたは水薬を飲む。"
            },
            {
                "nrs": "kymtymis",
                "pos": "名",
                "meaningJa": "夜眠り、深い安眠、夜の熟睡",
                "meaningEn": "night slumber, deep nocturnal sleep, restful sleep",
                "morphemes": [
                    "kym",
                    "tymis"
                ],
                "etymology": "kym(夜・闇) + tymis(眠り・睡眠)",
                "category": "4. 人体・生理・医療",
                "example_sentence": "Toren el kymtymis al mi de talzyvas.",
                "example_ja": "大地の生気によって私に深い安眠が訪れる。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-08",
        "batch": "Batch 1",
        "domain": "日常・市場と共同体の約束",
        "title": "広場の商いと今日の相談",
        "communicative_need": "今日の商い、今日の相談、確かな事実の記録を確認し合う。",
        "agent_a": {
            "name": "Toa",
            "role": "市場へ荷を運ぶ舟守"
        },
        "agent_b": {
            "name": "Yura",
            "role": "帳面を確認する写字生"
        },
        "turns": [
            {
                "speaker": "Toa",
                "nebulith": "Soran el ti ia hanorenan uo renar. Vyrel el mi ia hanocalun ul zydsoras.",
                "japanese": "あなたは市場で今日の商いを書き留める。私は今日の相談と事実記録を確認する。"
            },
            {
                "speaker": "Yura",
                "nebulith": "Ve, relen el hanocalun uo pamel. Dirin el hanorenan de zydsoras.",
                "japanese": "はい、冊子に今日の相談がある。事実記録によって今日の商いは公正になる。"
            }
        ],
        "words": [
            {
                "nrs": "hanorenan",
                "pos": "名",
                "meaningJa": "今日の商い、本日の取引、当日の物々交換",
                "meaningEn": "today's trade, daily commerce, day's market exchange",
                "morphemes": [
                    "hano",
                    "renan"
                ],
                "etymology": "hano(今日・現在) + renan(交易・物々交換)",
                "category": "10. 経済・交易・資源",
                "example_sentence": "Soran el ti ia hanorenan uo renar.",
                "example_ja": "あなたは市場で今日の商いを書き留める。"
            },
            {
                "nrs": "hanocalun",
                "pos": "名",
                "meaningJa": "今日の相談、本日の語らい、当日の打ち合わせ",
                "meaningEn": "today's discussion, daily consultation, day's talk",
                "morphemes": [
                    "hano",
                    "calun"
                ],
                "etymology": "hano(今日・現在) + calun(対話する・相談する)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Relen el hanocalun uo pamel.",
                "example_ja": "冊子に今日の相談が記されている。"
            },
            {
                "nrs": "zydsoras",
                "pos": "名",
                "meaningJa": "事実記録、実相の記憶、確かな控え",
                "meaningEn": "factual record, verified memory, authentic log",
                "morphemes": [
                    "zyd",
                    "soras"
                ],
                "etymology": "zyd(事実・実相) + soras(記憶・刻印)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Vyrel el mi ia hanocalun ul zydsoras.",
                "example_ja": "私は今日の相談と事実記録を確認する。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-09",
        "batch": "Batch 1",
        "domain": "日常・水辺と自然の風景",
        "title": "谷の湧き水と木立の風",
        "communicative_need": "大地の湧き水、樹木の葉風、水面の星影を描写する。",
        "agent_a": {
            "name": "Neri",
            "role": "水辺を歩く採集師"
        },
        "agent_b": {
            "name": "Toa",
            "role": "錨を下ろす舟守"
        },
        "turns": [
            {
                "speaker": "Neri",
                "nebulith": "Toren el taldaris va talik. Vyrel el mi ia velwylas uo daron.",
                "japanese": "谷から湧き水（大地水）が流れてくる。私は湖で木立のそよ風を見つめる。"
            },
            {
                "speaker": "Toa",
                "nebulith": "Alin el taldaris. Falun el vyrdaron uo velwylas.",
                "japanese": "湧き水は清らかだ。木立のそよ風のなかで星湖（星を映す水面）が輝く。"
            },
            {
                "speaker": "Neri",
                "nebulith": "Vyrel el mi ia vyrdaron de elir.",
                "japanese": "私は喜びをもって星を映す水面を見つめる。"
            }
        ],
        "words": [
            {
                "nrs": "taldaris",
                "pos": "名",
                "meaningJa": "湧き水、地下水脈、大地の清流",
                "meaningEn": "groundwater spring, earthen stream, natural wellspring",
                "morphemes": [
                    "tal",
                    "daris"
                ],
                "etymology": "tal(大地・土壌) + daris(水・清流)",
                "category": "6. 地球自然・地形・地質",
                "example_sentence": "Toren el taldaris va talik.",
                "example_ja": "谷から湧き水が流れてくる。"
            },
            {
                "nrs": "velwylas",
                "pos": "名",
                "meaningJa": "木立のそよ風、樹間を渡る風、木漏れ日の風",
                "meaningEn": "forest breeze, wind through trees, woodland air",
                "morphemes": [
                    "vel",
                    "wylas"
                ],
                "etymology": "vel(木・樹木) + wylas(風・そよぐ)",
                "category": "6. 地球自然・地形・地質",
                "example_sentence": "Falun el vyrdaron uo velwylas.",
                "example_ja": "木立のそよ風のなかで星を映す水面が輝く。"
            },
            {
                "nrs": "vyrdaron",
                "pos": "名",
                "meaningJa": "星を映す湖、星影の水面、星見池",
                "meaningEn": "starlit lake, star-reflecting pond, astral basin",
                "morphemes": [
                    "vyr",
                    "daron"
                ],
                "etymology": "vyr(星・光点) + daron(湖・静水面)",
                "category": "6. 地球自然・地形・地質",
                "example_sentence": "Vyrel el mi ia vyrdaron de elir.",
                "example_ja": "私は喜びをもって星を映す湖を見つめる。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-10",
        "batch": "Batch 1",
        "domain": "日常・明日への希望と旅立ち",
        "title": "明日の航路と心の灯火",
        "communicative_need": "明日の希望、星の道しるべ、仲間との心の輪を語り合う。",
        "agent_a": {
            "name": "Sev",
            "role": "灯台を守る灯守"
        },
        "agent_b": {
            "name": "Yura",
            "role": "記録を継ぐ写字生"
        },
        "turns": [
            {
                "speaker": "Sev",
                "nebulith": "Falun el vyrlaris uo celen. Relen el senowelin uo klorsylim en miin.",
                "japanese": "空に星の道しるべが輝く。私たちの心の輪のなかに明日の希望がある。"
            },
            {
                "speaker": "Yura",
                "nebulith": "Poran el miin uo vyrlaris. Vymin el miin ia senowelin ul klorsylim.",
                "japanese": "私たちは星の道しるべを進む。私たちは明日の希望と心の輪を守り抜く。"
            }
        ],
        "words": [
            {
                "nrs": "vyrlaris",
                "pos": "名",
                "meaningJa": "星の道しるべ、星見の航路、夜空の導き道",
                "meaningEn": "starlit pathway, stellar route, celestial guideway",
                "morphemes": [
                    "vyr",
                    "laris"
                ],
                "etymology": "vyr(星・光点) + laris(軌道・航路・天の路)",
                "category": "1. 天体・宇宙・天文",
                "example_sentence": "Falun el vyrlaris uo celen.",
                "example_ja": "空に星の道しるべが輝く。"
            },
            {
                "nrs": "senowelin",
                "pos": "名",
                "meaningJa": "明日の希望、未来への願い、明日への期待",
                "meaningEn": "hope for tomorrow, future aspiration, morrow's wish",
                "morphemes": [
                    "seno",
                    "welin"
                ],
                "etymology": "seno(明日・来たるべき日) + welin(希望・願い)",
                "category": "13. 精神・感情・内省",
                "example_sentence": "Relen el senowelin uo klorsylim en miin.",
                "example_ja": "私たちの心の輪のなかに明日の希望がある。"
            },
            {
                "nrs": "klorsylim",
                "pos": "名",
                "meaningJa": "心の輪、魂の結びつき、円居の共感",
                "meaningEn": "circle of minds, bond of spirits, fellowship ring",
                "morphemes": [
                    "klor",
                    "sylim"
                ],
                "etymology": "klor(円・環) + sylim(心・魂・精神)",
                "category": "13. 精神・感情・内省",
                "example_sentence": "Vymin el miin ia senowelin ul klorsylim.",
                "example_ja": "私たちは明日の希望と心の輪を守る。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-11",
        "batch": "Batch 2",
        "domain": "日常・衣服と身支度・寝具",
        "title": "白い布衣と木組みの寝台",
        "communicative_need": "純白の布衣、銀糸の装束、木組みの寝台を整える。",
        "agent_a": {
            "name": "Yura",
            "role": "身支度を整える写字生"
        },
        "agent_b": {
            "name": "Neri",
            "role": "布地を畳む採集師"
        },
        "turns": [
            {
                "speaker": "Yura",
                "nebulith": "Vyrel el mi ia alinvalis ul tynivalis uo velkymel.",
                "japanese": "私は木の寝台の上で白衣と銀衣を見つめる。"
            },
            {
                "speaker": "Neri",
                "nebulith": "Alin el alinvalis, ul falun el tynivalis. Sirin el velkymel uo vorn.",
                "japanese": "白衣は清らかで、銀衣は輝く。部屋で木の寝台が静かに佇んでいる。"
            }
        ],
        "words": [
            {
                "nrs": "alinvalis",
                "pos": "名",
                "meaningJa": "白衣、純白の布衣、白い装束",
                "meaningEn": "white garment, pure white robe, linen tunic",
                "morphemes": [
                    "alin",
                    "valis"
                ],
                "etymology": "alin(白い・純白の) + valis(衣服・布地)",
                "category": "15. 工芸・道具・物質",
                "example_sentence": "Vyrel el mi ia alinvalis uo velkymel.",
                "example_ja": "私は木の寝台の上で白衣を見つめる。"
            },
            {
                "nrs": "tynivalis",
                "pos": "名",
                "meaningJa": "銀衣、白銀の装い、銀糸の衣",
                "meaningEn": "silver robe, silvery attire, silver-threaded cloak",
                "morphemes": [
                    "tyni",
                    "valis"
                ],
                "etymology": "tyni(銀色の・白銀の) + valis(衣服・装束)",
                "category": "15. 工芸・道具・物質",
                "example_sentence": "Falun el tynivalis uo vorn.",
                "example_ja": "部屋で銀衣が輝く。"
            },
            {
                "nrs": "velkymel",
                "pos": "名",
                "meaningJa": "木の寝台、木組みのベッド、木製寝床",
                "meaningEn": "wooden bedstead, timber cot, wooden sleeping frame",
                "morphemes": [
                    "vel",
                    "kymel"
                ],
                "etymology": "vel(木・樹木) + kymel(寝台・ベッド)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Sirin el velkymel uo vorn.",
                "example_ja": "部屋で木の寝台が静かに佇む。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-12",
        "batch": "Batch 2",
        "domain": "日常・舟運と港の往来",
        "title": "星見港の渡し舟と今日の航路",
        "communicative_need": "水路の渡し舟、星見の船着き場、今日の巡行路を確認する。",
        "agent_a": {
            "name": "Toa",
            "role": "舟を整える舟守"
        },
        "agent_b": {
            "name": "Sev",
            "role": "灯火を掲げる灯守"
        },
        "turns": [
            {
                "speaker": "Toa",
                "nebulith": "Toren el darlaros to vyrlarar. Vyrel el mi ia hanolaris.",
                "japanese": "水上舟が星見港へ到着する。私は今日の航路を確かめる。"
            },
            {
                "speaker": "Sev",
                "nebulith": "Vymin el mi ia darlaros uo vyrlarar. Dirin el hanolaris uo daron.",
                "japanese": "私は星見港で水上舟を守る。湖の上で今日の航路は穏やかだ。"
            }
        ],
        "words": [
            {
                "nrs": "darlaros",
                "pos": "名",
                "meaningJa": "水上舟、水路の乗り物、渡し舟",
                "meaningEn": "watercraft, canal ferry, river skiff",
                "morphemes": [
                    "dar",
                    "laros"
                ],
                "etymology": "dar(しずく・水) + laros(乗り物・船)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Toren el darlaros to vyrlarar.",
                "example_ja": "水上舟が星見港へ到着する。"
            },
            {
                "nrs": "vyrlarar",
                "pos": "名",
                "meaningJa": "星見港、星影の船着き場、夜間停泊所",
                "meaningEn": "starlit harbor, astral pier, night anchorage",
                "morphemes": [
                    "vyr",
                    "larar"
                ],
                "etymology": "vyr(星・光点) + larar(港・停留所)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Vymin el mi ia darlaros uo vyrlarar.",
                "example_ja": "私は星見港で水上舟を守る。"
            },
            {
                "nrs": "hanolaris",
                "pos": "名",
                "meaningJa": "今日の航路、本日の道筋、当日の巡行路",
                "meaningEn": "today's route, daily course, day's itinerary",
                "morphemes": [
                    "hano",
                    "laris"
                ],
                "etymology": "hano(今日・現在) + laris(軌道・航路)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Dirin el hanolaris uo daron.",
                "example_ja": "湖の上で今日の航路は整っている。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-13",
        "batch": "Batch 3",
        "domain": "日常・感謝と友情・礼節",
        "title": "誠の謝意と微笑みの刻",
        "communicative_need": "偽りなき感謝、揺るぎない友情、笑顔のひとときを分かち合う。",
        "agent_a": {
            "name": "Sev",
            "role": "客人を迎える灯守"
        },
        "agent_b": {
            "name": "Toa",
            "role": "贈り物を届ける舟守"
        },
        "turns": [
            {
                "speaker": "Sev",
                "nebulith": "Fenor el mi ia zydcynur to ti. Relen el zydcynas ul havsaren al miel.",
                "japanese": "私はあなたへ心からの感謝を伝える。私たち二人に真の友情と微笑みの瞬間がある。"
            },
            {
                "speaker": "Toa",
                "nebulith": "Cynel el mi ia zydcynur ul zydcynas. Falun el havsaren uo govan.",
                "japanese": "私は心からの感謝と真の友情を愛する。家の中で微笑みの瞬間が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "zydcynur",
                "pos": "名",
                "meaningJa": "心からの感謝、偽りなき謝意、誠実な返礼",
                "meaningEn": "sincere gratitude, heartfelt thanks, earnest appreciation",
                "morphemes": [
                    "zyd",
                    "cynur"
                ],
                "etymology": "zyd(事実・誠) + cynur(感謝・謝意)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Fenor el mi ia zydcynur to ti.",
                "example_ja": "私はあなたへ心からの感謝を伝える。"
            },
            {
                "nrs": "zydcynas",
                "pos": "名",
                "meaningJa": "真の友情、揺るぎない親愛、誠の絆",
                "meaningEn": "true friendship, steadfast amity, genuine bond",
                "morphemes": [
                    "zyd",
                    "cynas"
                ],
                "etymology": "zyd(事実・誠) + cynas(友情・親愛)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Cynel el mi ia zydcynur ul zydcynas.",
                "example_ja": "私は心からの感謝と真の友情を愛する。"
            },
            {
                "nrs": "havsaren",
                "pos": "名",
                "meaningJa": "微笑みの瞬間、笑顔のひととき、和やかな刻",
                "meaningEn": "moment of smiling, cheerful instant, warm interlude",
                "morphemes": [
                    "hav",
                    "saren"
                ],
                "etymology": "hav(時・瞬間) + saren(微笑む・笑顔になる)",
                "category": "13. 精神・感情・内省",
                "example_sentence": "Falun el havsaren uo govan.",
                "example_ja": "家の中で微笑みの瞬間が輝く。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-14",
        "batch": "Batch 3",
        "domain": "日常・音楽と詩歌・夕べの調べ",
        "title": "水辺の詩と夜想の調べ",
        "communicative_need": "夜の詩歌、せせらぎの歌、木々の調べを楽しむ。",
        "agent_a": {
            "name": "Neri",
            "role": "竪琴を爪弾く採集師"
        },
        "agent_b": {
            "name": "Yura",
            "role": "詩を口ずさむ写字生"
        },
        "turns": [
            {
                "speaker": "Neri",
                "nebulith": "Cival el mi ia kymlyren ul darlyren. Toren el velcival va velom.",
                "japanese": "私は夜想歌と水辺の歌を奏でる。森から木笛の奏楽が響いてくる。"
            },
            {
                "speaker": "Yura",
                "nebulith": "Cynel el mi ia kymlyren ul darlyren. Sirin el sylim de velcival.",
                "japanese": "私は夜想歌と水辺の歌を好む。木笛の奏楽によって心が静まる。"
            }
        ],
        "words": [
            {
                "nrs": "kymlyren",
                "pos": "名",
                "meaningJa": "夜想歌、夜の詩歌、宵の調べ",
                "meaningEn": "nocturne, night song, evening ballad",
                "morphemes": [
                    "kym",
                    "lyren"
                ],
                "etymology": "kym(夜・闇) + lyren(歌・詩)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Cival el mi ia kymlyren ul darlyren.",
                "example_ja": "私は夜想歌と水辺の歌を奏でる。"
            },
            {
                "nrs": "darlyren",
                "pos": "名",
                "meaningJa": "水辺の歌、せせらぎの詩、清流の調べ",
                "meaningEn": "waterside song, brook melody, stream lyric",
                "morphemes": [
                    "dar",
                    "lyren"
                ],
                "etymology": "dar(しずく・水) + lyren(歌・詩)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Cynel el mi ia kymlyren ul darlyren.",
                "example_ja": "私は夜想歌と水辺の歌を好む。"
            },
            {
                "nrs": "velcival",
                "pos": "名",
                "meaningJa": "木笛の奏楽、樹間の調べ、木々の合奏",
                "meaningEn": "woodwind music, sylvan melody, timber resonance",
                "morphemes": [
                    "vel",
                    "cival"
                ],
                "etymology": "vel(木・樹木) + cival(奏でる・歌う)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Toren el velcival va velom.",
                "example_ja": "森から木笛の奏楽が響いてくる。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-15",
        "batch": "Batch 4",
        "domain": "学芸・書斎と観測記録",
        "title": "銀筆と星見帳の思索",
        "communicative_need": "天体観測の冊子、銀軸の筆、事実に基づく深い思索を語る。",
        "agent_a": {
            "name": "Yura",
            "role": "星図を写す写字生"
        },
        "agent_b": {
            "name": "Sev",
            "role": "観測機器を整える灯守"
        },
        "turns": [
            {
                "speaker": "Yura",
                "nebulith": "Soran el mi ia vyrpamel de tynikirel. Relen el zydmemar uo sylim.",
                "japanese": "私は銀筆で星見帳を書き留める。心の中に実相の思索がある。"
            },
            {
                "speaker": "Sev",
                "nebulith": "Vyrel el mi ia vyrpamel ul tynikirel. Dirin el zydmemar en ti.",
                "japanese": "私は星見帳と銀筆を見つめる。あなたの実相の思索は確かだ。"
            }
        ],
        "words": [
            {
                "nrs": "vyrpamel",
                "pos": "名",
                "meaningJa": "星見帳、天体観測記、星図の冊子",
                "meaningEn": "star atlas, astronomical logbook, celestial codex",
                "morphemes": [
                    "vyr",
                    "pamel"
                ],
                "etymology": "vyr(星・光点) + pamel(本・手記ノート)",
                "category": "1. 天体・宇宙・天文",
                "example_sentence": "Soran el mi ia vyrpamel de tynikirel.",
                "example_ja": "私は銀筆で星見帳を書き留める。"
            },
            {
                "nrs": "tynikirel",
                "pos": "名",
                "meaningJa": "銀筆、白銀の鉄筆、銀軸のペン",
                "meaningEn": "silver stylus, silver-barreled pen, gleaming quill",
                "morphemes": [
                    "tyni",
                    "kirel"
                ],
                "etymology": "tyni(銀色の・白銀の) + kirel(筆・ペン・鉄筆)",
                "category": "15. 工芸・道具・物質",
                "example_sentence": "Vyrel el mi ia vyrpamel ul tynikirel.",
                "example_ja": "私は星見帳と銀筆を見つめる。"
            },
            {
                "nrs": "zydmemar",
                "pos": "名",
                "meaningJa": "実相の思索、事実の熟考、真理の黙想",
                "meaningEn": "factual contemplation, grounded reflection, earnest meditation",
                "morphemes": [
                    "zyd",
                    "memar"
                ],
                "etymology": "zyd(事実・実相) + memar(思考・熟考)",
                "category": "13. 精神・感情・内省",
                "example_sentence": "Relen el zydmemar uo sylim.",
                "example_ja": "心の中に実相の思索がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-16",
        "batch": "Batch 4",
        "domain": "日常・菜園と保存食の恵み",
        "title": "大地の庭園と露葉の収穫",
        "communicative_need": "土の菜園、水滴を宿す若葉、熟成させた滋養食について話す。",
        "agent_a": {
            "name": "Neri",
            "role": "若葉を摘む採集師"
        },
        "agent_b": {
            "name": "Sev",
            "role": "保存食を仕込む灯守"
        },
        "turns": [
            {
                "speaker": "Neri",
                "nebulith": "Poran el mi to talvelar. Vyrel el mi ia darvelas uo velil.",
                "japanese": "私は大地の庭園へ歩く。私は草木の上で露葉を見つめる。"
            },
            {
                "speaker": "Sev",
                "nebulith": "Kiras el mi ia nervoril va darvelas uo talvelar.",
                "japanese": "私は大地の庭園で露葉から滋養発酵食を仕込む。"
            },
            {
                "speaker": "Neri",
                "nebulith": "Neranast el mi ia nervoril.",
                "japanese": "私はその滋養発酵食を味わいたい。"
            }
        ],
        "words": [
            {
                "nrs": "talvelar",
                "pos": "名",
                "meaningJa": "大地の庭園、土の菜園、里の緑地",
                "meaningEn": "earthen garden, kitchen plot, cultivated green",
                "morphemes": [
                    "tal",
                    "velar"
                ],
                "etymology": "tal(大地・土壌) + velar(庭・庭園)",
                "category": "8. 植物・森林・菌類",
                "example_sentence": "Poran el mi to talvelar.",
                "example_ja": "私は大地の庭園へ歩く。"
            },
            {
                "nrs": "darvelas",
                "pos": "名",
                "meaningJa": "露葉、水滴を宿す若葉、濡れ葉",
                "meaningEn": "dewy leaf, moisture-laden foliage, wet frond",
                "morphemes": [
                    "dar",
                    "velas"
                ],
                "etymology": "dar(しずく・水滴) + velas(葉・緑葉)",
                "category": "8. 植物・森林・菌類",
                "example_sentence": "Vyrel el mi ia darvelas uo velil.",
                "example_ja": "私は草木の上で露葉を見つめる。"
            },
            {
                "nrs": "nervoril",
                "pos": "名",
                "meaningJa": "滋養発酵食、熟成保存糧、発酵滋養食",
                "meaningEn": "nourishing fermented fare, cultured preserve, aged provisions",
                "morphemes": [
                    "ner",
                    "voril"
                ],
                "etymology": "ner(滋養・食材) + voril(発酵食・熟成食)",
                "category": "12. 食文化・料理・飲食",
                "example_sentence": "Neranast el mi ia nervoril.",
                "example_ja": "私は滋養発酵食を味わいたい。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-17",
        "batch": "Batch 4",
        "domain": "工芸・手仕事と日々の勤労",
        "title": "銀の小刀と木工・土仕事",
        "communicative_need": "銀細工の小刀、木工の手仕事、大地の土仕事を語り合う。",
        "agent_a": {
            "name": "Toa",
            "role": "木材を削る舟守"
        },
        "agent_b": {
            "name": "Neri",
            "role": "畑を整える採集師"
        },
        "turns": [
            {
                "speaker": "Toa",
                "nebulith": "Kiras el mi ia veldolar de tyniserel. Vyrel el mi ia taldolar en ti.",
                "japanese": "私は銀の小刀で木工仕事を行う。私はあなたの土仕事を見つめる。"
            },
            {
                "speaker": "Neri",
                "nebulith": "Cynel el mi ia taldolar ul veldolar. Falun el tyniserel uo morpal.",
                "japanese": "私は土仕事と木工仕事を愛する。手のひらで銀の小刀が光る。"
            }
        ],
        "words": [
            {
                "nrs": "tyniserel",
                "pos": "名",
                "meaningJa": "銀の小刀、白銀の刃物、銀細工ナイフ",
                "meaningEn": "silver knife, gleaming craft blade, silver carving knife",
                "morphemes": [
                    "tyni",
                    "serel"
                ],
                "etymology": "tyni(銀色の・白銀の) + serel(小刀・ナイフ)",
                "category": "15. 工芸・道具・物質",
                "example_sentence": "Falun el tyniserel uo morpal.",
                "example_ja": "手のひらで銀の小刀が光る。"
            },
            {
                "nrs": "veldolar",
                "pos": "名",
                "meaningJa": "木工仕事、木彫りの勤労、木材加工",
                "meaningEn": "woodworking, carpentry craft, timber labor",
                "morphemes": [
                    "vel",
                    "dolar"
                ],
                "etymology": "vel(木・樹木) + dolar(労働・勤労)",
                "category": "15. 工芸・道具・物質",
                "example_sentence": "Kiras el mi ia veldolar de tyniserel.",
                "example_ja": "私は銀の小刀で木工仕事を行う。"
            },
            {
                "nrs": "taldolar",
                "pos": "名",
                "meaningJa": "土仕事、農作業、大地の勤労",
                "meaningEn": "earthwork, tilling labor, soil cultivation",
                "morphemes": [
                    "tal",
                    "dolar"
                ],
                "etymology": "tal(大地・土) + dolar(労働・勤労)",
                "category": "10. 経済・交易・資源",
                "example_sentence": "Cynel el mi ia taldolar ul veldolar.",
                "example_ja": "私は土仕事と木工仕事を愛する。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-18",
        "batch": "Batch 4",
        "domain": "日常・通信と遠方からの便り",
        "title": "星便りと今日の確報",
        "communicative_need": "星間通信の便り、本日の伝言、実証された確報を伝え合う。",
        "agent_a": {
            "name": "Sev",
            "role": "信号塔を守る灯守"
        },
        "agent_b": {
            "name": "Yura",
            "role": "通信文を記録する写字生"
        },
        "turns": [
            {
                "speaker": "Sev",
                "nebulith": "Toren el vyrtolas ul hanotolas to tolom. Relen el zydtolas uo pamel.",
                "japanese": "交信院へ星便りと今日の便りが届く。冊子の中に確報がある。"
            },
            {
                "speaker": "Yura",
                "nebulith": "Soran el mi ia vyrtolas ul hanotolas. Vymin el mi ia zydtolas.",
                "japanese": "私は星便りと今日の便りを書き留める。私は確報を守り抜く。"
            }
        ],
        "words": [
            {
                "nrs": "vyrtolas",
                "pos": "名",
                "meaningJa": "星便り、星間通信文、光信号の便り",
                "meaningEn": "stellar message, astral dispatch, starlight tidings",
                "morphemes": [
                    "vyr",
                    "tolas"
                ],
                "etymology": "vyr(星・光点) + tolas(メッセージ・便り)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Toren el vyrtolas ul hanotolas to tolom.",
                "example_ja": "交信院へ星便りと今日の便りが届く。"
            },
            {
                "nrs": "hanotolas",
                "pos": "名",
                "meaningJa": "今日の便り、本日の知らせ、当日の伝言",
                "meaningEn": "today's tidings, daily message, current dispatch",
                "morphemes": [
                    "hano",
                    "tolas"
                ],
                "etymology": "hano(今日・現在) + tolas(メッセージ・便り)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Soran el mi ia vyrtolas ul hanotolas.",
                "example_ja": "私は星便りと今日の便りを書き留める。"
            },
            {
                "nrs": "zydtolas",
                "pos": "名",
                "meaningJa": "確報、事実の知らせ、実証された便り",
                "meaningEn": "verified dispatch, confirmed report, factual tidings",
                "morphemes": [
                    "zyd",
                    "tolas"
                ],
                "etymology": "zyd(事実・実相) + tolas(メッセージ・便り)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Relen el zydtolas uo pamel.",
                "example_ja": "冊子の中に確報がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-19",
        "batch": "Batch 5",
        "domain": "医療・草木薬と心身の回復",
        "title": "木皮薬と覚醒の刻",
        "communicative_need": "樹木の生薬、清水の養生力、心身が回復して目覚める瞬間を語る。",
        "agent_a": {
            "name": "Neri",
            "role": "草木薬を煎じる採集師"
        },
        "agent_b": {
            "name": "Toa",
            "role": "休息から目覚める舟守"
        },
        "turns": [
            {
                "speaker": "Neri",
                "nebulith": "Zyvan el mi ia ti de velzyvil ul darzyvas. Toren el havrevir al ti.",
                "japanese": "私は木皮薬と潤いの活力によってあなたを癒やす。あなたに覚醒の刻が訪れる。"
            },
            {
                "speaker": "Toa",
                "nebulith": "Bion el mi ia velzyvil. Velrin el mi ia darzyvas uo havrevir.",
                "japanese": "私は木皮薬を飲む。私は覚醒の刻のなかで潤いの活力を感じる。"
            }
        ],
        "words": [
            {
                "nrs": "velzyvil",
                "pos": "名",
                "meaningJa": "木皮薬、樹木の生薬、草木薬",
                "meaningEn": "bark medicine, botanical remedy, herbal sylvan cure",
                "morphemes": [
                    "vel",
                    "zyvil"
                ],
                "etymology": "vel(木・樹木) + zyvil(薬・処方薬)",
                "category": "4. 人体・生理・医療",
                "example_sentence": "Bion el mi ia velzyvil.",
                "example_ja": "私は木皮薬を飲む。"
            },
            {
                "nrs": "darzyvas",
                "pos": "名",
                "meaningJa": "潤いの活力、清水の養生、水気の健やかさ",
                "meaningEn": "hydrating vigor, spring-water vitality, refreshing health",
                "morphemes": [
                    "dar",
                    "zyvas"
                ],
                "etymology": "dar(しずく・水) + zyvas(健康・活力)",
                "category": "4. 人体・生理・医療",
                "example_sentence": "Velrin el mi ia darzyvas uo havrevir.",
                "example_ja": "私は覚醒の刻のなかで潤いの活力を感じる。"
            },
            {
                "nrs": "havrevir",
                "pos": "名",
                "meaningJa": "覚醒の刻、回復の瞬間、目覚めの時",
                "meaningEn": "hour of awakening, moment of recovery, revival instant",
                "morphemes": [
                    "hav",
                    "revir"
                ],
                "etymology": "hav(時・瞬間) + revir(目覚める・回復する)",
                "category": "4. 人体・生理・医療",
                "example_sentence": "Toren el havrevir al ti.",
                "example_ja": "あなたに覚醒の刻が訪れる。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-20",
        "batch": "Batch 5",
        "domain": "社会・円卓評議と平和の誓い",
        "title": "円卓の対話と真の平和",
        "communicative_need": "円居の融和、揺るぎない平和、車座の対話集会を讃える。",
        "agent_a": {
            "name": "Yura",
            "role": "評議を記録する写字生"
        },
        "agent_b": {
            "name": "Sev",
            "role": "議場の灯を守る灯守"
        },
        "turns": [
            {
                "speaker": "Yura",
                "nebulith": "Calun el miin uo klorcalor. Vymin el miin ia klorsilan ul zydsilan.",
                "japanese": "私たちは円卓評議で語り合う。私たちは和の輪と真の平和を守り抜く。"
            },
            {
                "speaker": "Sev",
                "nebulith": "Falun el klorcalor de klorsilan. Relen el zydsilan uo domom en miin.",
                "japanese": "和の輪によって円卓評議が輝く。私たちの街に真の平和がある。"
            }
        ],
        "words": [
            {
                "nrs": "klorsilan",
                "pos": "名",
                "meaningJa": "和の輪、円居の平和、共同体の融和",
                "meaningEn": "circle of peace, harmonious fellowship, ring of concord",
                "morphemes": [
                    "klor",
                    "silan"
                ],
                "etymology": "klor(円・環) + silan(平和・融和)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Vymin el miin ia klorsilan ul zydsilan.",
                "example_ja": "私たちは和の輪と真の平和を守り抜く。"
            },
            {
                "nrs": "zydsilan",
                "pos": "名",
                "meaningJa": "真の平和、実相の安寧、揺るぎない和合",
                "meaningEn": "true peace, enduring tranquility, authentic concord",
                "morphemes": [
                    "zyd",
                    "silan"
                ],
                "etymology": "zyd(事実・実相) + silan(平和・安寧)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Relen el zydsilan uo domom en miin.",
                "example_ja": "私たちの街に真の平和がある。"
            },
            {
                "nrs": "klorcalor",
                "pos": "名",
                "meaningJa": "円卓評議、車座の会議、輪の対話集会",
                "meaningEn": "roundtable council, circle assembly, deliberative ring",
                "morphemes": [
                    "klor",
                    "calor"
                ],
                "etymology": "klor(円・環) + calor(評議会・対話の座)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Calun el miin uo klorcalor.",
                "example_ja": "私たちは円卓評議で語り合う。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-21",
        "batch": "Batch 6",
        "domain": "自然・風向きと夜空の気配",
        "title": "湖面を渡る湿り風と星見の風",
        "communicative_need": "水辺の湿り風、宵闇の夜風、星見の晴風を観測し合う。",
        "agent_a": {
            "name": "Toa",
            "role": "帆綱を確かめる舟守"
        },
        "agent_b": {
            "name": "Sev",
            "role": "風見を掲げる灯守"
        },
        "turns": [
            {
                "speaker": "Toa",
                "nebulith": "Toren el darwylas ul kymwylas va daron. Vyrel el mi ia vyrwylas uo celen.",
                "japanese": "湖から湿り風と夜風が吹いてくる。私は空に星見の風を見つめる。"
            },
            {
                "speaker": "Sev",
                "nebulith": "Velrin el mi ia darwylas ul kymwylas. Dirin el vyrwylas al laros.",
                "japanese": "私は湿り風と夜風を感じる。船にとって星見の風は穏やかだ。"
            }
        ],
        "words": [
            {
                "nrs": "darwylas",
                "pos": "名",
                "meaningJa": "湿り風、水辺の風、湖面を渡る涼風",
                "meaningEn": "moist breeze, waterside wind, lake-air current",
                "morphemes": [
                    "dar",
                    "wylas"
                ],
                "etymology": "dar(しずく・水) + wylas(風・大気の流れ)",
                "category": "7. 気象・天候・季節",
                "example_sentence": "Toren el darwylas ul kymwylas va daron.",
                "example_ja": "湖から湿り風と夜風が吹いてくる。"
            },
            {
                "nrs": "kymwylas",
                "pos": "名",
                "meaningJa": "夜風、宵闇の風、静夜の涼風",
                "meaningEn": "night breeze, evening wind, nocturnal draft",
                "morphemes": [
                    "kym",
                    "wylas"
                ],
                "etymology": "kym(夜・闇) + wylas(風・大気の流れ)",
                "category": "7. 気象・天候・季節",
                "example_sentence": "Velrin el mi ia darwylas ul kymwylas.",
                "example_ja": "私は湿り風と夜風を感じる。"
            },
            {
                "nrs": "vyrwylas",
                "pos": "名",
                "meaningJa": "星見の風、星夜の晴風、高空の清風",
                "meaningEn": "starlit breeze, clear night wind, astral current",
                "morphemes": [
                    "vyr",
                    "wylas"
                ],
                "etymology": "vyr(星・光点) + wylas(風・大気の流れ)",
                "category": "7. 気象・天候・季節",
                "example_sentence": "Dirin el vyrwylas al laros.",
                "example_ja": "船にとって星見の風は穏やかだ。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-22",
        "batch": "Batch 6",
        "domain": "自然・季節のほころびと水面のきらめき",
        "title": "大地のほころびと若葉の微笑み",
        "communicative_need": "春めく大地のほころび、木々の芽吹き、水面のきらめきを喜ぶ。",
        "agent_a": {
            "name": "Neri",
            "role": "芽吹きを調べる採集師"
        },
        "agent_b": {
            "name": "Yura",
            "role": "季節の暦を記す写字生"
        },
        "turns": [
            {
                "speaker": "Neri",
                "nebulith": "Vyrel el mi ia talsaren ul velsaren uo talom. Falun el darsaren uo daris.",
                "japanese": "私は野原で大地のほころびと木々の芽吹きを見つめる。清流で水面のきらめきが輝く。"
            },
            {
                "speaker": "Yura",
                "nebulith": "Soran el mi ia talsaren ul velsaren. Cynel el mi ia darsaren.",
                "japanese": "私は大地のほころびと木々の芽吹きを書き留める。私は水面のきらめきを愛する。"
            }
        ],
        "words": [
            {
                "nrs": "talsaren",
                "pos": "名",
                "meaningJa": "大地のほころび、土の芽吹き、春の野の微笑み",
                "meaningEn": "blossoming earth, vernal thawing soil, smiling meadow",
                "morphemes": [
                    "tal",
                    "saren"
                ],
                "etymology": "tal(大地・土) + saren(微笑む・ほころぶ)",
                "category": "7. 気象・天候・季節",
                "example_sentence": "Vyrel el mi ia talsaren ul velsaren uo talom.",
                "example_ja": "私は野原で大地のほころびと木々の芽吹きを見つめる。"
            },
            {
                "nrs": "velsaren",
                "pos": "名",
                "meaningJa": "木々の芽吹き、樹木のほころび、新緑の歓び",
                "meaningEn": "budding foliage, sylvan blooming, woodland awakening",
                "morphemes": [
                    "vel",
                    "saren"
                ],
                "etymology": "vel(木・樹木) + saren(微笑む・ほころぶ)",
                "category": "8. 植物・森林・菌類",
                "example_sentence": "Soran el mi ia talsaren ul velsaren.",
                "example_ja": "私は大地のほころびと木々の芽吹きを書き留める。"
            },
            {
                "nrs": "darsaren",
                "pos": "名",
                "meaningJa": "水面のきらめき、さざ波の微笑み、清流の照り映え",
                "meaningEn": "sparkling ripple, smiling water surface, stream glint",
                "morphemes": [
                    "dar",
                    "saren"
                ],
                "etymology": "dar(しずく・水) + saren(微笑む・きらめく)",
                "category": "6. 地球自然・地形・地質",
                "example_sentence": "Falun el darsaren uo daris.",
                "example_ja": "清流で水面のきらめきが輝く。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-23",
        "batch": "Batch 6",
        "domain": "天文・天蓋の観測と今日の空模様",
        "title": "星天の広がりと地平の空",
        "communicative_need": "満天の星空、地平に接する空、今日の空模様を見上げて語り合う。",
        "agent_a": {
            "name": "Sev",
            "role": "観測台に立つ灯守"
        },
        "agent_b": {
            "name": "Yura",
            "role": "天候記録をつける写字生"
        },
        "turns": [
            {
                "speaker": "Sev",
                "nebulith": "Falun el vyrcelen ul talcelen. Alin el hanocelen uo domom.",
                "japanese": "星天と地平の空が輝く。街の上で今日の空は澄み渡っている。"
            },
            {
                "speaker": "Yura",
                "nebulith": "Vyrel el mi ia vyrcelen ul talcelen. Soran el mi ia hanocelen uo pamel.",
                "japanese": "私は星天と地平の空を見つめる。私は冊子に今日の空模様を書き留める。"
            }
        ],
        "words": [
            {
                "nrs": "vyrcelen",
                "pos": "名",
                "meaningJa": "星天、満天の星空、星々の天蓋",
                "meaningEn": "starry firmament, astral vault, star-filled sky",
                "morphemes": [
                    "vyr",
                    "celen"
                ],
                "etymology": "vyr(星・天体) + celen(空・天蓋)",
                "category": "1. 天体・宇宙・天文",
                "example_sentence": "Falun el vyrcelen ul talcelen.",
                "example_ja": "星天と地平の空が輝く。"
            },
            {
                "nrs": "talcelen",
                "pos": "名",
                "meaningJa": "地平の空、大地と接する空、低い空の広がり",
                "meaningEn": "horizon sky, low earthward sky, terrestrial firmament",
                "morphemes": [
                    "tal",
                    "celen"
                ],
                "etymology": "tal(大地・地上) + celen(空・天蓋)",
                "category": "7. 気象・天候・季節",
                "example_sentence": "Vyrel el mi ia vyrcelen ul talcelen.",
                "example_ja": "私は星天と地平の空を見つめる。"
            },
            {
                "nrs": "hanocelen",
                "pos": "名",
                "meaningJa": "今日の空、本日の空模様、当日の天候",
                "meaningEn": "today's sky, current weather sky, day's firmament",
                "morphemes": [
                    "hano",
                    "celen"
                ],
                "etymology": "hano(今日・現在) + celen(空・天蓋)",
                "category": "7. 気象・天候・季節",
                "example_sentence": "Soran el mi ia hanocelen uo pamel.",
                "example_ja": "私は冊子に今日の空模様を書き留める。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-24",
        "batch": "Batch 6",
        "domain": "移動・陸路と林道・夜道の巡回",
        "title": "陸の街道と木立の小径",
        "communicative_need": "大地の街道、森林の並木道、夜間の巡回路を確認する。",
        "agent_a": {
            "name": "Toa",
            "role": "荷を運ぶ舟守"
        },
        "agent_b": {
            "name": "Neri",
            "role": "森の道案内をする採集師"
        },
        "turns": [
            {
                "speaker": "Toa",
                "nebulith": "Poran el miin uo tallaris ul vellaris. Vymin el miin ia kymlaris.",
                "japanese": "私たちは陸の街道と林道を進む。私たちは夜道の巡回路を守る。"
            },
            {
                "speaker": "Neri",
                "nebulith": "Dirin el tallaris ul vellaris. Falun el zohar uo kymlaris.",
                "japanese": "陸の街道と林道は整っている。夜道の巡回路に灯りが輝く。"
            }
        ],
        "words": [
            {
                "nrs": "tallaris",
                "pos": "名",
                "meaningJa": "陸の街道、大地の道筋、陸路",
                "meaningEn": "overland route, earthen highway, terrestrial path",
                "morphemes": [
                    "tal",
                    "laris"
                ],
                "etymology": "tal(大地・陸) + laris(軌道・道筋)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Poran el miin uo tallaris ul vellaris.",
                "example_ja": "私たちは陸の街道と林道を進む。"
            },
            {
                "nrs": "vellaris",
                "pos": "名",
                "meaningJa": "木立の小径、森の巡回路、樹間の道筋",
                "meaningEn": "woodland trail, forest path, tree-lined avenue",
                "morphemes": [
                    "vel",
                    "laris"
                ],
                "etymology": "vel(木・樹木) + laris(軌道・道筋)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Dirin el tallaris ul vellaris.",
                "example_ja": "陸の街道と林道は整っている。"
            },
            {
                "nrs": "kymlaris",
                "pos": "名",
                "meaningJa": "夜道、夜間の巡回路、宵の道筋",
                "meaningEn": "night path, nocturnal watch route, evening trail",
                "morphemes": [
                    "kym",
                    "laris"
                ],
                "etymology": "kym(夜・闇) + laris(軌道・道筋)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Falun el zohar uo kymlaris.",
                "example_ja": "夜道の巡回路に灯りが輝く。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-25",
        "batch": "Batch 7",
        "domain": "食文化・水辺の果実と木の実の収穫",
        "title": "みずみずしい水辺の実と今日の収穫実",
        "communicative_need": "水分豊かな水辺の果実、森の木の実、今日採れたばかりの果実を分け合う。",
        "agent_a": {
            "name": "Neri",
            "role": "果実を籠に集める採集師"
        },
        "agent_b": {
            "name": "Sev",
            "role": "食卓を整える灯守"
        },
        "turns": [
            {
                "speaker": "Neri",
                "nebulith": "Toren el mi ia darvorin ul velvorin. Relen el hanovorin uo kypal.",
                "japanese": "私は水辺の果実と森の木の実を運ぶ。箱の中に今日採れた果実がある。"
            },
            {
                "speaker": "Sev",
                "nebulith": "Neran el miin ia darvorin ul velvorin. Cynel el mi ia hanovorin.",
                "japanese": "私たちは水辺の果実と森の木の実を食べる。私は今日採れた果実を好む。"
            }
        ],
        "words": [
            {
                "nrs": "darvorin",
                "pos": "名",
                "meaningJa": "水辺の果実、果汁豊かな実、みずみずしい果物",
                "meaningEn": "juicy berry, waterside fruit, succulent pome",
                "morphemes": [
                    "dar",
                    "vorin"
                ],
                "etymology": "dar(しずく・水分) + vorin(果実・果物)",
                "category": "12. 食文化・料理・飲食",
                "example_sentence": "Toren el mi ia darvorin ul velvorin.",
                "example_ja": "私は水辺の果実と森の木の実を運ぶ。"
            },
            {
                "nrs": "velvorin",
                "pos": "名",
                "meaningJa": "森の木の実、樹上の果実、堅果",
                "meaningEn": "tree nut, woodland fruit, orchard harvest",
                "morphemes": [
                    "vel",
                    "vorin"
                ],
                "etymology": "vel(木・樹木) + vorin(果実・木の実)",
                "category": "12. 食文化・料理・飲食",
                "example_sentence": "Neran el miin ia darvorin ul velvorin.",
                "example_ja": "私たちは水辺の果実と森の木の実を食べる。"
            },
            {
                "nrs": "hanovorin",
                "pos": "名",
                "meaningJa": "今日採れた果実、本日の収穫果、朝摘みの実",
                "meaningEn": "today's picked fruit, fresh daily harvest, day's berry",
                "morphemes": [
                    "hano",
                    "vorin"
                ],
                "etymology": "hano(今日・当日) + vorin(果実・果物)",
                "category": "12. 食文化・料理・飲食",
                "example_sentence": "Relen el hanovorin uo kypal.",
                "example_ja": "箱の中に今日採れた果実がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-26",
        "batch": "Batch 7",
        "domain": "工芸・収納箱と器の整理",
        "title": "銀細工の小箱と素焼きの収納匣",
        "communicative_need": "銀細工の小箱、土器の保存箱、白い磁器の器箱を棚に並べる。",
        "agent_a": {
            "name": "Yura",
            "role": "書斎の道具を整理する写字生"
        },
        "agent_b": {
            "name": "Toa",
            "role": "荷箱を運ぶ舟守"
        },
        "turns": [
            {
                "speaker": "Yura",
                "nebulith": "Vyrel el mi ia tynikypal ul talkypal. Relen el alinkypal uo vorn.",
                "japanese": "私は銀の小箱と土器の保存箱を見つめる。部屋に白磁の器箱がある。"
            },
            {
                "speaker": "Toa",
                "nebulith": "Vymin el mi ia tynikypal ul talkypal. Falun el alinkypal uo zohar.",
                "japanese": "私は銀の小箱と土器の保存箱を守る。灯りの下で白磁の器箱が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "tynikypal",
                "pos": "名",
                "meaningJa": "銀の小箱、白銀の匣、銀細工ケース",
                "meaningEn": "silver casket, silver-trimmed box, metal coffer",
                "morphemes": [
                    "tyni",
                    "kypal"
                ],
                "etymology": "tyni(銀色の・白銀の) + kypal(箱・ケース)",
                "category": "15. 工芸・道具・物質",
                "example_sentence": "Vyrel el mi ia tynikypal ul talkypal.",
                "example_ja": "私は銀の小箱と土器の保存箱を見つめる。"
            },
            {
                "nrs": "talkypal",
                "pos": "名",
                "meaningJa": "土器の保存箱、陶器の匣、素焼きの収納容器",
                "meaningEn": "earthenware chest, terracotta storage box, clay vessel",
                "morphemes": [
                    "tal",
                    "kypal"
                ],
                "etymology": "tal(大地・粘土) + kypal(箱・容器)",
                "category": "15. 工芸・道具・物質",
                "example_sentence": "Vymin el mi ia tynikypal ul talkypal.",
                "example_ja": "私は銀の小箱と土器の保存箱を守る。"
            },
            {
                "nrs": "alinkypal",
                "pos": "名",
                "meaningJa": "白磁の器箱、純白の小匣、白い収納箱",
                "meaningEn": "white porcelain box, pure white chest, ivory casket",
                "morphemes": [
                    "alin",
                    "kypal"
                ],
                "etymology": "alin(白い・純白の) + kypal(箱・ケース)",
                "category": "15. 工芸・道具・物質",
                "example_sentence": "Falun el alinkypal uo zohar.",
                "example_ja": "灯りの下で白磁の器箱が輝く。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-27",
        "batch": "Batch 7",
        "domain": "食文化・発酵食と果実酒の仕込み",
        "title": "土蔵の熟成食と木樽の発酵酒",
        "communicative_need": "土蔵の熟成食、清水で仕込んだ発酵飲料、木樽の果実酒を点検する。",
        "agent_a": {
            "name": "Sev",
            "role": "貯蔵庫を見回る灯守"
        },
        "agent_b": {
            "name": "Neri",
            "role": "酵母を管理する採集師"
        },
        "turns": [
            {
                "speaker": "Sev",
                "nebulith": "Vyrel el mi ia talvoril ul darvoril. Relen el velvoril uo govan.",
                "japanese": "私は土蔵の熟成食と清水の発酵飲料を見つめる。家の中に木樽の果実酒がある。"
            },
            {
                "speaker": "Neri",
                "nebulith": "Kiras el mi ia talvoril ul darvoril. Bion el miin ia velvoril.",
                "japanese": "私は土蔵の熟成食と清水の発酵飲料を仕込む。私たちは木樽の果実酒を飲む。"
            }
        ],
        "words": [
            {
                "nrs": "talvoril",
                "pos": "名",
                "meaningJa": "土蔵の熟成食、地室の発酵食、根菜の漬け物",
                "meaningEn": "cellar-aged preserve, earthen-crock ferment, pickled root",
                "morphemes": [
                    "tal",
                    "voril"
                ],
                "etymology": "tal(大地・土室) + voril(発酵食・熟成食)",
                "category": "12. 食文化・料理・飲食",
                "example_sentence": "Vyrel el mi ia talvoril ul darvoril.",
                "example_ja": "私は土蔵の熟成食と清水の発酵飲料を見つめる。"
            },
            {
                "nrs": "darvoril",
                "pos": "名",
                "meaningJa": "清水の発酵飲料、澄んだ醸造酒、水仕込みの果実酒",
                "meaningEn": "spring-brewed beverage, clear fermented drink, liquid tonic",
                "morphemes": [
                    "dar",
                    "voril"
                ],
                "etymology": "dar(しずく・清水) + voril(発酵食・醸造酒)",
                "category": "12. 食文化・料理・飲食",
                "example_sentence": "Kiras el mi ia talvoril ul darvoril.",
                "example_ja": "私は土蔵の熟成食と清水の発酵飲料を仕込む。"
            },
            {
                "nrs": "velvoril",
                "pos": "名",
                "meaningJa": "木樽の果実酒、木の実の熟成酒、樹液の発酵酒",
                "meaningEn": "cask-aged cider, wooden-barrel vintage, sylvan brew",
                "morphemes": [
                    "vel",
                    "voril"
                ],
                "etymology": "vel(木・木樽) + voril(発酵食・果実酒)",
                "category": "12. 食文化・料理・飲食",
                "example_sentence": "Bion el miin ia velvoril.",
                "example_ja": "私たちは木樽の果実酒を飲む。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-28",
        "batch": "Batch 7",
        "domain": "食文化・温かい煮込みと今日の汁物",
        "title": "今日の滋養汁と木の実の煮込み",
        "communicative_need": "本日の日替わりスープ、木の実の煮込み汁、根菜の大地汁を振る舞う。",
        "agent_a": {
            "name": "Sev",
            "role": "大鍋をかき混ぜる灯守"
        },
        "agent_b": {
            "name": "Toa",
            "role": "冷えた体を温める舟守"
        },
        "turns": [
            {
                "speaker": "Sev",
                "nebulith": "Kiras el mi ia hanodarel ul veldarel. Relen el taldarel uo govan.",
                "japanese": "私は本日の滋養汁と木の実の煮込みを作る。家の中に根菜の大地汁がある。"
            },
            {
                "speaker": "Toa",
                "nebulith": "Neran el mi ia hanodarel ul veldarel. Cynel el mi ia taldarel.",
                "japanese": "私は本日の滋養汁と木の実の煮込みを味わう。私は根菜の大地汁を好む。"
            }
        ],
        "words": [
            {
                "nrs": "hanodarel",
                "pos": "名",
                "meaningJa": "本日の滋養汁、今日のスープ、当日の温かい煮汁",
                "meaningEn": "soup of the day, today's broth, daily warm potage",
                "morphemes": [
                    "hano",
                    "darel"
                ],
                "etymology": "hano(今日・本日) + darel(スープ・煮汁)",
                "category": "12. 食文化・料理・飲食",
                "example_sentence": "Kiras el mi ia hanodarel ul veldarel.",
                "example_ja": "私は本日の滋養汁と木の実の煮込みを作る。"
            },
            {
                "nrs": "veldarel",
                "pos": "名",
                "meaningJa": "木の実の煮込み、森の茸汁、草木の滋味スープ",
                "meaningEn": "woodland nut stew, herbal forest broth, sylvan soup",
                "morphemes": [
                    "vel",
                    "darel"
                ],
                "etymology": "vel(木・草木) + darel(スープ・煮汁)",
                "category": "12. 食文化・料理・飲食",
                "example_sentence": "Neran el mi ia hanodarel ul veldarel.",
                "example_ja": "私は本日の滋養汁と木の実の煮込みを味わう。"
            },
            {
                "nrs": "taldarel",
                "pos": "名",
                "meaningJa": "根菜の大地汁、土の恵みのポタージュ、滋味深い根菜スープ",
                "meaningEn": "root-vegetable potage, earthen harvest broth, hearty stew",
                "morphemes": [
                    "tal",
                    "darel"
                ],
                "etymology": "tal(大地・根菜) + darel(スープ・煮汁)",
                "category": "12. 食文化・料理・飲食",
                "example_sentence": "Cynel el mi ia taldarel.",
                "example_ja": "私は根菜の大地汁を好む。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-29",
        "batch": "Batch 8",
        "domain": "建築・住居の佇まいと星見の館",
        "title": "土壁の家と白壁の住まい",
        "communicative_need": "温かな土壁の家、星見の館、清らかな白壁の住まいを訪ねる。",
        "agent_a": {
            "name": "Toa",
            "role": "街を歩く舟守"
        },
        "agent_b": {
            "name": "Yura",
            "role": "建物を案内する写字生"
        },
        "turns": [
            {
                "speaker": "Toa",
                "nebulith": "Vyrel el mi ia talgovan ul vyrgovan. Falun el alingovan uo domom.",
                "japanese": "私は土壁の家と星見の館を見つめる。街の中で白壁の住まいが輝く。"
            },
            {
                "speaker": "Yura",
                "nebulith": "Sirin el talgovan ul vyrgovan. Poran el miin to alingovan.",
                "japanese": "土壁の家と星見の館は静かに佇む。私たちは白壁の住まいへ歩む。"
            }
        ],
        "words": [
            {
                "nrs": "talgovan",
                "pos": "名",
                "meaningJa": "土壁の家、大地の住まい、石造りの住居",
                "meaningEn": "earthen house, masonry dwelling, grounded homestead",
                "morphemes": [
                    "tal",
                    "govan"
                ],
                "etymology": "tal(大地・土石) + govan(家・住居)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Vyrel el mi ia talgovan ul vyrgovan.",
                "example_ja": "私は土壁の家と星見の館を見つめる。"
            },
            {
                "nrs": "vyrgovan",
                "pos": "名",
                "meaningJa": "星見の館、天体観測の家、星影の邸宅",
                "meaningEn": "star-watching lodge, astral manor, observatory house",
                "morphemes": [
                    "vyr",
                    "govan"
                ],
                "etymology": "vyr(星・天体) + govan(家・館)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Sirin el talgovan ul vyrgovan.",
                "example_ja": "土壁の家と星見の館は静かに佇む。"
            },
            {
                "nrs": "alingovan",
                "pos": "名",
                "meaningJa": "白壁の住まい、純白の家屋、白い漆喰の館",
                "meaningEn": "whitewashed house, white-walled home, bright residence",
                "morphemes": [
                    "alin",
                    "govan"
                ],
                "etymology": "alin(白い・純白の) + govan(家・住居)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Falun el alingovan uo domom.",
                "example_ja": "街の中で白壁の住まいが輝く。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-30",
        "batch": "Batch 8",
        "domain": "建築・門戸と扉の守り",
        "title": "銀飾りの扉と石造りの門",
        "communicative_need": "銀細工の扉、重厚な石門、白い出入口の扉を開閉し守る。",
        "agent_a": {
            "name": "Sev",
            "role": "門の鍵を預かる灯守"
        },
        "agent_b": {
            "name": "Toa",
            "role": "朝の見回りをする舟守"
        },
        "turns": [
            {
                "speaker": "Sev",
                "nebulith": "Vymin el mi ia tynilerel ul tallerel. Vyrel el mi ia alinlerel.",
                "japanese": "私は銀飾りの扉と石造りの門を守る。私は白い扉を見つめる。"
            },
            {
                "speaker": "Toa",
                "nebulith": "Falun el tynilerel ul alinlerel. Dirin el tallerel uo domom.",
                "japanese": "銀飾りの扉と白い扉が輝く。街の中で石造りの門は堅固だ。"
            }
        ],
        "words": [
            {
                "nrs": "tynilerel",
                "pos": "名",
                "meaningJa": "銀飾りの扉、白銀の門扉、銀細工のゲート",
                "meaningEn": "silver-mounted door, silver portal, gleaming gate",
                "morphemes": [
                    "tyni",
                    "lerel"
                ],
                "etymology": "tyni(銀色の・白銀の) + lerel(扉・門)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Vymin el mi ia tynilerel ul tallerel.",
                "example_ja": "私は銀飾りの扉と石造りの門を守る。"
            },
            {
                "nrs": "tallerel",
                "pos": "名",
                "meaningJa": "石造りの門、大地の城門、重厚な石扉",
                "meaningEn": "stone archway, earthen gate, masonry portal",
                "morphemes": [
                    "tal",
                    "lerel"
                ],
                "etymology": "tal(大地・石) + lerel(扉・門)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Dirin el tallerel uo domom.",
                "example_ja": "街の中で石造りの門は堅固だ。"
            },
            {
                "nrs": "alinlerel",
                "pos": "名",
                "meaningJa": "白い扉、白木の戸口、純白の門扉",
                "meaningEn": "white doorway, pale timber door, bright entrance",
                "morphemes": [
                    "alin",
                    "lerel"
                ],
                "etymology": "alin(白い・純白の) + lerel(扉・出入口)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Falun el tynilerel ul alinlerel.",
                "example_ja": "銀飾りの扉と白い扉が輝く。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-31",
        "batch": "Batch 8",
        "domain": "住空間・水庭と星見の中庭",
        "title": "泉のある水庭と夜の庭園",
        "communicative_need": "水を湛えた水庭、星を見上げる中庭、静かな夜の庭園を散策する。",
        "agent_a": {
            "name": "Neri",
            "role": "水草を手入れする採集師"
        },
        "agent_b": {
            "name": "Yura",
            "role": "夕涼みをする写字生"
        },
        "turns": [
            {
                "speaker": "Neri",
                "nebulith": "Poran el mi uo darvelar ul vyrvelar. Sirin el kymvelar uo govan.",
                "japanese": "私は水庭と星見の庭を歩く。家のそばで夜の庭園が静まり返る。"
            },
            {
                "speaker": "Yura",
                "nebulith": "Cynel el mi ia darvelar ul vyrvelar. Vyrel el mi ia kymvelar.",
                "japanese": "私は水庭と星見の庭を愛する。私は夜の庭園を見つめる。"
            }
        ],
        "words": [
            {
                "nrs": "darvelar",
                "pos": "名",
                "meaningJa": "水庭、泉のある中庭、水辺の庭園",
                "meaningEn": "water garden, fountain courtyard, aquatic patio",
                "morphemes": [
                    "dar",
                    "velar"
                ],
                "etymology": "dar(しずく・水) + velar(庭・庭園)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Poran el mi uo darvelar ul vyrvelar.",
                "example_ja": "私は水庭と星見の庭を歩く。"
            },
            {
                "nrs": "vyrvelar",
                "pos": "名",
                "meaningJa": "星見の庭、天体観測の中庭、星空のテラス",
                "meaningEn": "stargazing courtyard, astral garden, skyward terrace",
                "morphemes": [
                    "vyr",
                    "velar"
                ],
                "etymology": "vyr(星・天体) + velar(庭・庭園)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Cynel el mi ia darvelar ul vyrvelar.",
                "example_ja": "私は水庭と星見の庭を愛する。"
            },
            {
                "nrs": "kymvelar",
                "pos": "名",
                "meaningJa": "夜の庭園、宵闇の中庭、静夜の庭",
                "meaningEn": "night garden, evening courtyard, nocturnal grove",
                "morphemes": [
                    "kym",
                    "velar"
                ],
                "etymology": "kym(夜・闇) + velar(庭・庭園)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Sirin el kymvelar uo govan.",
                "example_ja": "家のそばで夜の庭園が静まり返る。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-32",
        "batch": "Batch 8",
        "domain": "住空間・地下室と天窓の部屋・円形広間",
        "title": "地階の貯蔵室と円形の談話室",
        "communicative_need": "涼しい地階の小部屋、星見の天窓部屋、円形の談話室を使い分ける。",
        "agent_a": {
            "name": "Sev",
            "role": "館の灯りを管理する灯守"
        },
        "agent_b": {
            "name": "Yura",
            "role": "読書室を探す写字生"
        },
        "turns": [
            {
                "speaker": "Sev",
                "nebulith": "Relen el talvorn ul vyrvorn uo govan. Falun el zohar uo klorvorn.",
                "japanese": "家の中に地階室と天窓の部屋がある。円形広間に灯りが輝く。"
            },
            {
                "speaker": "Yura",
                "nebulith": "Vyrel el mi ia talvorn ul vyrvorn. Calun el miin uo klorvorn.",
                "japanese": "私は地階室と天窓の部屋を見つめる。私たちは円形広間で語り合う。"
            }
        ],
        "words": [
            {
                "nrs": "talvorn",
                "pos": "名",
                "meaningJa": "地階室、土室の部屋、涼しい地下貯蔵室",
                "meaningEn": "ground-level chamber, earthen cellar room, cool vault",
                "morphemes": [
                    "tal",
                    "vorn"
                ],
                "etymology": "tal(大地・地下) + vorn(部屋・室内)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Relen el talvorn ul vyrvorn uo govan.",
                "example_ja": "家の中に地階室と天窓の部屋がある。"
            },
            {
                "nrs": "vyrvorn",
                "pos": "名",
                "meaningJa": "天窓の部屋、星見の小部屋、展望室",
                "meaningEn": "skylight room, star-viewing chamber, upper observatory",
                "morphemes": [
                    "vyr",
                    "vorn"
                ],
                "etymology": "vyr(星・光点) + vorn(部屋・室内)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Vyrel el mi ia talvorn ul vyrvorn.",
                "example_ja": "私は地階室と天窓の部屋を見つめる。"
            },
            {
                "nrs": "klorvorn",
                "pos": "名",
                "meaningJa": "円形広間、車座の談話室、環状の部屋",
                "meaningEn": "rotunda parlor, circular hall, round chamber",
                "morphemes": [
                    "klor",
                    "vorn"
                ],
                "etymology": "klor(円・環) + vorn(部屋・広間)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Calun el miin uo klorvorn.",
                "example_ja": "私たちは円形広間で語り合う。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-33",
        "batch": "Batch 9",
        "domain": "学芸・地理誌と植物図鑑・白紙の帳面",
        "title": "大地の地理誌と草木図鑑の編纂",
        "communicative_need": "大地の地理誌、草木の植物図鑑、新しい白紙の帳面を揃える。",
        "agent_a": {
            "name": "Yura",
            "role": "書物を編む写字生"
        },
        "agent_b": {
            "name": "Neri",
            "role": "標本を届ける採集師"
        },
        "turns": [
            {
                "speaker": "Yura",
                "nebulith": "Soran el mi ia talpamel ul velpamel. Relen el alinpamel uo vorn.",
                "japanese": "私は地理誌と草木図鑑を書き留める。部屋に白紙の帳面がある。"
            },
            {
                "speaker": "Neri",
                "nebulith": "Vyrel el mi ia talpamel ul velpamel. Toren el mi ia alinpamel to ti.",
                "japanese": "私は地理誌と草木図鑑を見つめる。私はあなたへ白紙の帳面を届ける。"
            }
        ],
        "words": [
            {
                "nrs": "talpamel",
                "pos": "名",
                "meaningJa": "地理誌、大地の記録帳、地形図鑑",
                "meaningEn": "geographical codex, terrestrial survey book, land chronicle",
                "morphemes": [
                    "tal",
                    "pamel"
                ],
                "etymology": "tal(大地・地形) + pamel(本・冊子)",
                "category": "9. 学問・科学・技術",
                "example_sentence": "Soran el mi ia talpamel ul velpamel.",
                "example_ja": "私は地理誌と草木図鑑を書き留める。"
            },
            {
                "nrs": "velpamel",
                "pos": "名",
                "meaningJa": "草木図鑑、植物誌、森林の手記",
                "meaningEn": "botanical compendium, herbal codex, flora notebook",
                "morphemes": [
                    "vel",
                    "pamel"
                ],
                "etymology": "vel(木・植物) + pamel(本・手記ノート)",
                "category": "8. 植物・森林・菌類",
                "example_sentence": "Vyrel el mi ia talpamel ul velpamel.",
                "example_ja": "私は地理誌と草木図鑑を見つめる。"
            },
            {
                "nrs": "alinpamel",
                "pos": "名",
                "meaningJa": "白紙の帳面、未使用の冊子、純白の手記帳",
                "meaningEn": "blank notebook, uninscribed ledger, white vellum codex",
                "morphemes": [
                    "alin",
                    "pamel"
                ],
                "etymology": "alin(白い・無垢の) + pamel(本・手記ノート)",
                "category": "15. 工芸・道具・物質",
                "example_sentence": "Toren el mi ia alinpamel to ti.",
                "example_ja": "私はあなたへ白紙の帳面を届ける。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-34",
        "batch": "Batch 9",
        "domain": "歴史・星の記憶と土地の伝承・今日の思い出",
        "title": "星の古記録と土地の記憶",
        "communicative_need": "星々の古い記憶、土地に刻まれた伝承、今日の思い出を語り継ぐ。",
        "agent_a": {
            "name": "Sev",
            "role": "伝承を語る灯守"
        },
        "agent_b": {
            "name": "Yura",
            "role": "歴史を記録する写字生"
        },
        "turns": [
            {
                "speaker": "Sev",
                "nebulith": "Vymin el miin ia vyrsoras ul talsoras. Relen el hanosoras uo sylim.",
                "japanese": "私たちは星の記憶と土地の伝承を守り抜く。心の中に今日の思い出がある。"
            },
            {
                "speaker": "Yura",
                "nebulith": "Soran el mi ia vyrsoras ul talsoras. Cynel el mi ia hanosoras.",
                "japanese": "私は星の記憶と土地の伝承を書き留める。私は今日の思い出を愛する。"
            }
        ],
        "words": [
            {
                "nrs": "vyrsoras",
                "pos": "名",
                "meaningJa": "星の記憶、天体の古記録、星辰の刻印",
                "meaningEn": "stellar memory, astral chronicle, celestial imprint",
                "morphemes": [
                    "vyr",
                    "soras"
                ],
                "etymology": "vyr(星・天体) + soras(記憶・刻印)",
                "category": "1. 天体・宇宙・天文",
                "example_sentence": "Vymin el miin ia vyrsoras ul talsoras.",
                "example_ja": "私たちは星の記憶と土地の伝承を守り抜く。"
            },
            {
                "nrs": "talsoras",
                "pos": "名",
                "meaningJa": "土地の伝承、大地の記憶、郷土の由緒",
                "meaningEn": "memory of the land, earthen heritage, local lore",
                "morphemes": [
                    "tal",
                    "soras"
                ],
                "etymology": "tal(大地・土地) + soras(記憶・思い出)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Soran el mi ia vyrsoras ul talsoras.",
                "example_ja": "私は星の記憶と土地の伝承を書き留める。"
            },
            {
                "nrs": "hanosoras",
                "pos": "名",
                "meaningJa": "今日の思い出、本日の記憶、その日の銘記",
                "meaningEn": "today's memory, recollection of the day, daily remembrance",
                "morphemes": [
                    "hano",
                    "soras"
                ],
                "etymology": "hano(今日・当日) + soras(記憶・思い出)",
                "category": "13. 精神・感情・内省",
                "example_sentence": "Relen el hanosoras uo sylim.",
                "example_ja": "心の中に今日の思い出がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-35",
        "batch": "Batch 9",
        "domain": "芸術・星の讃歌と大地の民謡・今日の詩",
        "title": "星見の讃歌と収穫の民謡",
        "communicative_need": "星を讃える詩歌、大地の労働歌、今日紡いだばかりの詩を披露し合う。",
        "agent_a": {
            "name": "Neri",
            "role": "野の歌を口ずさむ採集師"
        },
        "agent_b": {
            "name": "Toa",
            "role": "舟歌を合わせる舟守"
        },
        "turns": [
            {
                "speaker": "Neri",
                "nebulith": "Cival el mi ia vyrlyren ul tallyren. Fenor el mi ia hanolyren to ti.",
                "japanese": "私は星の讃歌と大地の民謡を歌う。私はあなたへ今日の詩を伝える。"
            },
            {
                "speaker": "Toa",
                "nebulith": "Cynel el mi ia vyrlyren ul tallyren. Falun el hanolyren uo klorcalor.",
                "japanese": "私は星の讃歌と大地の民謡を好む。円卓評議で今日の詩が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "vyrlyren",
                "pos": "名",
                "meaningJa": "星の讃歌、星辰の詩、夜空の頌歌",
                "meaningEn": "starlight hymn, astral ode, celestial lyric",
                "morphemes": [
                    "vyr",
                    "lyren"
                ],
                "etymology": "vyr(星・光点) + lyren(歌・詩)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Cival el mi ia vyrlyren ul tallyren.",
                "example_ja": "私は星の讃歌と大地の民謡を歌う。"
            },
            {
                "nrs": "tallyren",
                "pos": "名",
                "meaningJa": "大地の民謡、里の労働歌、郷土の詩歌",
                "meaningEn": "folk song of the land, earthen ballad, pastoral chant",
                "morphemes": [
                    "tal",
                    "lyren"
                ],
                "etymology": "tal(大地・郷土) + lyren(歌・詩)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Cynel el mi ia vyrlyren ul tallyren.",
                "example_ja": "私は星の讃歌と大地の民謡を好む。"
            },
            {
                "nrs": "hanolyren",
                "pos": "名",
                "meaningJa": "今日の詩、本日の歌、当日の即興詩",
                "meaningEn": "today's poem, verse of the day, daily lyric",
                "morphemes": [
                    "hano",
                    "lyren"
                ],
                "etymology": "hano(今日・本日) + lyren(歌・詩)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Fenor el mi ia hanolyren to ti.",
                "example_ja": "私はあなたへ今日の詩を伝える。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-36",
        "batch": "Batch 9",
        "domain": "芸術・水琴の調べと夜の合奏",
        "title": "水辺の奏楽と星夜の合奏",
        "communicative_need": "水の響きを生かした水辺の奏楽、星夜の演奏、静夜の調べを聴き合う。",
        "agent_a": {
            "name": "Yura",
            "role": "音律を記録する写字生"
        },
        "agent_b": {
            "name": "Sev",
            "role": "鐘琴を鳴らす灯守"
        },
        "turns": [
            {
                "speaker": "Yura",
                "nebulith": "Velrin el mi ia darcival ul vyrcival. Toren el kymcival va darvelar.",
                "japanese": "私は水辺の奏楽と星夜の合奏を感じる。水庭から夜想の調べが響いてくる。"
            },
            {
                "speaker": "Sev",
                "nebulith": "Cival el miin ia darcival ul vyrcival. Sirin el sylim de kymcival.",
                "japanese": "私たちは水辺の奏楽と星夜の合奏を奏でる。夜想の調べによって心が静まる。"
            }
        ],
        "words": [
            {
                "nrs": "darcival",
                "pos": "名",
                "meaningJa": "水辺の奏楽、水琴の調べ、せせらぎの合奏",
                "meaningEn": "waterside music, water-chime harmony, stream concert",
                "morphemes": [
                    "dar",
                    "cival"
                ],
                "etymology": "dar(しずく・水) + cival(奏でる・和音)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Velrin el mi ia darcival ul vyrcival.",
                "example_ja": "私は水辺の奏楽と星夜の合奏を感じる。"
            },
            {
                "nrs": "vyrcival",
                "pos": "名",
                "meaningJa": "星夜の合奏、天体の調べ、星見の音楽",
                "meaningEn": "starlight ensemble, astral harmony, celestial concert",
                "morphemes": [
                    "vyr",
                    "cival"
                ],
                "etymology": "vyr(星・天体) + cival(奏でる・和音)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Cival el miin ia darcival ul vyrcival.",
                "example_ja": "私たちは水辺の奏楽と星夜の合奏を奏でる。"
            },
            {
                "nrs": "kymcival",
                "pos": "名",
                "meaningJa": "夜想の調べ、静夜の奏楽、宵の音楽",
                "meaningEn": "nocturnal music, evening serenade, night harmony",
                "morphemes": [
                    "kym",
                    "cival"
                ],
                "etymology": "kym(夜・闇) + cival(奏でる・音楽)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Toren el kymcival va darvelar.",
                "example_ja": "水庭から夜想の調べが響いてくる。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-37",
        "batch": "Batch 10",
        "domain": "医療・鉱物薬と今日の処方薬",
        "title": "大地の鉱物薬と純白の塗薬",
        "communicative_need": "大地の鉱物薬、今日調合した処方薬、清らかな白い軟膏を整える。",
        "agent_a": {
            "name": "Neri",
            "role": "薬を調合する採集師"
        },
        "agent_b": {
            "name": "Sev",
            "role": "救護箱を管理する灯守"
        },
        "turns": [
            {
                "speaker": "Neri",
                "nebulith": "Kiras el mi ia talzyvil ul hanozyvil. Relen el alinzyvil uo alinkypal.",
                "japanese": "私は大地の鉱物薬と今日の処方薬を調合する。白磁の器箱の中に純白の軟膏がある。"
            },
            {
                "speaker": "Sev",
                "nebulith": "Vymin el mi ia talzyvil ul hanozyvil. Zyvan el mi ia ti de alinzyvil.",
                "japanese": "私は大地の鉱物薬と今日の処方薬を守る。私は純白の軟膏によってあなたを癒やす。"
            }
        ],
        "words": [
            {
                "nrs": "talzyvil",
                "pos": "名",
                "meaningJa": "大地の鉱物薬、薬土の湿布、根茎の生薬",
                "meaningEn": "mineral poultice, earthen medicinal clay, root remedy",
                "morphemes": [
                    "tal",
                    "zyvil"
                ],
                "etymology": "tal(大地・薬土) + zyvil(薬・治療薬)",
                "category": "4. 人体・生理・医療",
                "example_sentence": "Kiras el mi ia talzyvil ul hanozyvil.",
                "example_ja": "私は大地の鉱物薬と今日の処方薬を調合する。"
            },
            {
                "nrs": "hanozyvil",
                "pos": "名",
                "meaningJa": "今日の処方薬、本日の調合薬、当日の服薬",
                "meaningEn": "today's remedy, daily dose, freshly compounded medicine",
                "morphemes": [
                    "hano",
                    "zyvil"
                ],
                "etymology": "hano(今日・当日) + zyvil(薬・処方薬)",
                "category": "4. 人体・生理・医療",
                "example_sentence": "Vymin el mi ia talzyvil ul hanozyvil.",
                "example_ja": "私は大地の鉱物薬と今日の処方薬を守る。"
            },
            {
                "nrs": "alinzyvil",
                "pos": "名",
                "meaningJa": "純白の軟膏、白い清浄薬、浄化の塗り薬",
                "meaningEn": "white salve, purifying ointment, clean balm",
                "morphemes": [
                    "alin",
                    "zyvil"
                ],
                "etymology": "alin(白い・清らかな) + zyvil(薬・治療薬)",
                "category": "4. 人体・生理・医療",
                "example_sentence": "Zyvan el mi ia ti de alinzyvil.",
                "example_ja": "私は純白の軟膏によってあなたを癒やす。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-38",
        "batch": "Batch 10",
        "domain": "精神・星への願いと共同体の希望",
        "title": "星への祈願と車座の願い",
        "communicative_need": "星々への願い、偽りなき切なる願い、共同体の共通の希望を分かち合う。",
        "agent_a": {
            "name": "Yura",
            "role": "祈願文を記す写字生"
        },
        "agent_b": {
            "name": "Toa",
            "role": "航海の無事を願う舟守"
        },
        "turns": [
            {
                "speaker": "Yura",
                "nebulith": "Relen el vyrwelin ul zydwelin uo sylim. Falun el klorwelin uo domom.",
                "japanese": "心の中に星への願いと切なる願いがある。街の中で共同体の希望が輝く。"
            },
            {
                "speaker": "Toa",
                "nebulith": "Vymin el miin ia vyrwelin ul zydwelin. Cynel el miin ia klorwelin.",
                "japanese": "私たちは星への願いと切なる願いを守り抜く。私たちは共同体の希望を愛する。"
            }
        ],
        "words": [
            {
                "nrs": "vyrwelin",
                "pos": "名",
                "meaningJa": "星への願い、星辰への祈願、天への希望",
                "meaningEn": "wish upon the stars, astral aspiration, celestial hope",
                "morphemes": [
                    "vyr",
                    "welin"
                ],
                "etymology": "vyr(星・天体) + welin(希望・願い)",
                "category": "13. 精神・感情・内省",
                "example_sentence": "Relen el vyrwelin ul zydwelin uo sylim.",
                "example_ja": "心の中に星への願いと切なる願いがある。"
            },
            {
                "nrs": "zydwelin",
                "pos": "名",
                "meaningJa": "切なる願い、真の希望、偽りなき希求",
                "meaningEn": "earnest wish, true hope, sincere aspiration",
                "morphemes": [
                    "zyd",
                    "welin"
                ],
                "etymology": "zyd(事実・誠) + welin(希望・願い)",
                "category": "13. 精神・感情・内省",
                "example_sentence": "Vymin el miin ia vyrwelin ul zydwelin.",
                "example_ja": "私たちは星への願いと切なる願いを守り抜く。"
            },
            {
                "nrs": "klorwelin",
                "pos": "名",
                "meaningJa": "共同体の希望、輪の願い、皆の共通の望み",
                "meaningEn": "shared communal hope, circle's aspiration, collective wish",
                "morphemes": [
                    "klor",
                    "welin"
                ],
                "etymology": "klor(円・共同体の輪) + welin(希望・願い)",
                "category": "13. 精神・感情・内省",
                "example_sentence": "Falun el klorwelin uo domom.",
                "example_ja": "街の中で共同体の希望が輝く。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-39",
        "batch": "Batch 10",
        "domain": "経済・農産物と水上交易・木材の商い",
        "title": "大地の収穫交易と水路の商い",
        "communicative_need": "農産物の陸上交易、水路の舟運交易、木材や林産物の取引を記録する。",
        "agent_a": {
            "name": "Toa",
            "role": "交易舟を操る舟守"
        },
        "agent_b": {
            "name": "Neri",
            "role": "林産物を出荷する採集師"
        },
        "turns": [
            {
                "speaker": "Toa",
                "nebulith": "Toren el talrenan ul darrenan to renar. Vyrel el mi ia velrenan.",
                "japanese": "農産物交易と水上交易が市場へ集まる。私は林産物取引を見つめる。"
            },
            {
                "speaker": "Neri",
                "nebulith": "Dirin el talrenan ul darrenan. Soran el mi ia velrenan uo pamel.",
                "japanese": "農産物交易と水上交易は順調だ。私は冊子に林産物取引を書き留める。"
            }
        ],
        "words": [
            {
                "nrs": "talrenan",
                "pos": "名",
                "meaningJa": "農産物交易、大地の恵みの取引、陸上交易",
                "meaningEn": "agricultural trade, overland commerce, produce exchange",
                "morphemes": [
                    "tal",
                    "renan"
                ],
                "etymology": "tal(大地・農産) + renan(交易・取引)",
                "category": "10. 経済・交易・資源",
                "example_sentence": "Toren el talrenan ul darrenan to renar.",
                "example_ja": "農産物交易と水上交易が市場へ集まる。"
            },
            {
                "nrs": "darrenan",
                "pos": "名",
                "meaningJa": "水上交易、舟運の商い、水路の物々交換",
                "meaningEn": "waterborne trade, canal commerce, maritime exchange",
                "morphemes": [
                    "dar",
                    "renan"
                ],
                "etymology": "dar(しずく・水路) + renan(交易・取引)",
                "category": "10. 経済・交易・資源",
                "example_sentence": "Dirin el talrenan ul darrenan.",
                "example_ja": "農産物交易と水上交易は順調だ。"
            },
            {
                "nrs": "velrenan",
                "pos": "名",
                "meaningJa": "林産物取引、木材の商い、森の恵みの交換",
                "meaningEn": "timber trade, forestry commerce, woodland barter",
                "morphemes": [
                    "vel",
                    "renan"
                ],
                "etymology": "vel(木・木材) + renan(交易・取引)",
                "category": "10. 経済・交易・資源",
                "example_sentence": "Soran el mi ia velrenan uo pamel.",
                "example_ja": "私は冊子に林産物取引を書き留める。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-40",
        "batch": "Batch 10",
        "domain": "社会・今日の平穏と天地の平和",
        "title": "今日の安寧と星降る大地の平和",
        "communicative_need": "今日の平穏、星空の下の平和、大地に根差した安寧を感謝し合う。",
        "agent_a": {
            "name": "Sev",
            "role": "夜の灯台から街を見守る灯守"
        },
        "agent_b": {
            "name": "Yura",
            "role": "対話篇の結語を記す写字生"
        },
        "turns": [
            {
                "speaker": "Sev",
                "nebulith": "Relen el hanosilan ul vyrsilan uo domom. Vymin el miin ia talsilan.",
                "japanese": "街の中に今日の平穏と星夜の平和がある。私たちは大地の安寧を守り抜く。"
            },
            {
                "speaker": "Yura",
                "nebulith": "Soran el mi ia hanosilan ul vyrsilan. Falun el talsilan al miin.",
                "japanese": "私は今日の平穏と星夜の平和を書き留める。私たちに大地の安寧が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "hanosilan",
                "pos": "名",
                "meaningJa": "今日の平穏、本日の安寧、日々の静かな平和",
                "meaningEn": "today's peace, daily tranquility, present concord",
                "morphemes": [
                    "hano",
                    "silan"
                ],
                "etymology": "hano(今日・現在) + silan(平和・安寧)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Relen el hanosilan ul vyrsilan uo domom.",
                "example_ja": "街の中に今日の平穏と星夜の平和がある。"
            },
            {
                "nrs": "vyrsilan",
                "pos": "名",
                "meaningJa": "星夜の平和、天の安寧、星空の下の融和",
                "meaningEn": "starlit peace, celestial harmony, astral serenity",
                "morphemes": [
                    "vyr",
                    "silan"
                ],
                "etymology": "vyr(星・天) + silan(平和・融和)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Soran el mi ia hanosilan ul vyrsilan.",
                "example_ja": "私は今日の平穏と星夜の平和を書き留める。"
            },
            {
                "nrs": "talsilan",
                "pos": "名",
                "meaningJa": "大地の安寧、国土の平和、地に根差した融和",
                "meaningEn": "peace of the land, terrestrial concord, grounded serenity",
                "morphemes": [
                    "tal",
                    "silan"
                ],
                "etymology": "tal(大地・国土) + silan(平和・安寧)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Vymin el miin ia talsilan.",
                "example_ja": "私たちは大地の安寧を守り抜く。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-41",
        "batch": "Batch 11",
        "domain": "工芸・装束と布地の仕立て",
        "title": "星模様の装束と水辺の衣",
        "communicative_need": "星紋の礼装、大地の作業衣、水辺の外套を仕立てて確認し合う。",
        "agent_a": {
            "name": "Yura",
            "role": "衣装帳を記す写字生"
        },
        "agent_b": {
            "name": "Neri",
            "role": "染料を整える採集師"
        },
        "turns": [
            {
                "speaker": "Yura",
                "nebulith": "Vyrel el mi ia vyrvalis ul talvalis uo vorn. Relen el darvalis uo vorn.",
                "japanese": "私は部屋で星紋の礼装と大地の作業衣を見つめる。部屋で水辺の外套がある。"
            },
            {
                "speaker": "Neri",
                "nebulith": "Vymin el miin ia vyrvalis ul talvalis. Falun el darvalis al miin.",
                "japanese": "私たちは星紋の礼装と大地の作業衣を大切に守る。私たちに水辺の外套が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "vyrvalis",
                "pos": "名",
                "meaningJa": "星紋の礼装、星空模様の衣、天測の装束",
                "meaningEn": "star-patterned robe, astral vestment, stargazer's cloak",
                "morphemes": [
                    "vyr",
                    "valis"
                ],
                "etymology": "vyr(星・天体) + valis(衣服・装い)",
                "category": "15. 工芸・道具・物質",
                "example_sentence": "Vyrel el mi ia vyrvalis ul talvalis uo vorn.",
                "example_ja": "私は部屋で星紋の礼装と大地の作業衣を見つめる。"
            },
            {
                "nrs": "talvalis",
                "pos": "名",
                "meaningJa": "大地の作業衣、野良着、土色の外衣",
                "meaningEn": "earth-toned workwear, field tunic, rustic garment",
                "morphemes": [
                    "tal",
                    "valis"
                ],
                "etymology": "tal(大地・野) + valis(衣服・装い)",
                "category": "15. 工芸・道具・物質",
                "example_sentence": "Vyrel el mi ia vyrvalis ul talvalis uo vorn.",
                "example_ja": "私は部屋で星紋の礼装と大地の作業衣を見つめる。"
            },
            {
                "nrs": "darvalis",
                "pos": "名",
                "meaningJa": "水辺の外套、雨除けの衣、防水の装束",
                "meaningEn": "waterside cloak, rain cape, moisture-resistant robe",
                "morphemes": [
                    "dar",
                    "valis"
                ],
                "etymology": "dar(しずく・水) + valis(衣服・装い)",
                "category": "15. 工芸・道具・物質",
                "example_sentence": "Relen el darvalis uo vorn.",
                "example_ja": "部屋で水辺の外套がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-42",
        "batch": "Batch 11",
        "domain": "工芸・標本箱と丸匣の整理",
        "title": "星図の小箱と円形の収納匣",
        "communicative_need": "星石の標本箱、水辺の採取箱、円形の小匣を整理する。",
        "agent_a": {
            "name": "Sev",
            "role": "器具庫を整える灯守"
        },
        "agent_b": {
            "name": "Yura",
            "role": "目録を作る写字生"
        },
        "turns": [
            {
                "speaker": "Sev",
                "nebulith": "Vyrel el mi ia vyrkypal ul darkypal uo govan. Relen el klorkypal uo govan.",
                "japanese": "私は家の中で星石の小箱と水辺の採取箱を確かめる。家の中で円形の小匣がある。"
            },
            {
                "speaker": "Yura",
                "nebulith": "Vymin el miin ia vyrkypal ul darkypal. Falun el klorkypal al miin.",
                "japanese": "私たちは星石の小箱と水辺の採取箱を保管する。私たちに円形の小匣が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "vyrkypal",
                "pos": "名",
                "meaningJa": "星石の小箱、天測器具ケース、星紋の匣",
                "meaningEn": "star-instrument case, astral coffer, starlight box",
                "morphemes": [
                    "vyr",
                    "kypal"
                ],
                "etymology": "vyr(星・天体) + kypal(箱・ケース)",
                "category": "15. 工芸・道具・物質",
                "example_sentence": "Vyrel el mi ia vyrkypal ul darkypal uo govan.",
                "example_ja": "私は家の中で星石の小箱と水辺の採取箱を確かめる。"
            },
            {
                "nrs": "darkypal",
                "pos": "名",
                "meaningJa": "水辺の採取箱、保水ケース、水草の小匣",
                "meaningEn": "moisture-keeping box, aquatic specimen case, water casket",
                "morphemes": [
                    "dar",
                    "kypal"
                ],
                "etymology": "dar(しずく・水) + kypal(箱・ケース)",
                "category": "15. 工芸・道具・物質",
                "example_sentence": "Vyrel el mi ia vyrkypal ul darkypal uo govan.",
                "example_ja": "私は家の中で星石の小箱と水辺の採取箱を確かめる。"
            },
            {
                "nrs": "klorkypal",
                "pos": "名",
                "meaningJa": "円形の小匣、丸箱、環状の収納ケース",
                "meaningEn": "round casket, circular box, ring-shaped container",
                "morphemes": [
                    "klor",
                    "kypal"
                ],
                "etymology": "klor(円・真円) + kypal(箱・ケース)",
                "category": "15. 工芸・道具・物質",
                "example_sentence": "Relen el klorkypal uo govan.",
                "example_ja": "家の中で円形の小匣がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-43",
        "batch": "Batch 11",
        "domain": "学芸・筆記具の選定と手入れ",
        "title": "星見の鉄筆と木軸のペン",
        "communicative_need": "天測用の鉄筆、木軸のペン、石筆を机に並べて手入れする。",
        "agent_a": {
            "name": "Yura",
            "role": "筆先を整える写字生"
        },
        "agent_b": {
            "name": "Toa",
            "role": "木軸を削る舟守"
        },
        "turns": [
            {
                "speaker": "Yura",
                "nebulith": "Vyrel el mi ia vyrkirel ul velkirel uo dovik. Relen el talkirel uo dovik.",
                "japanese": "私は机の上で天測の鉄筆と木軸のペンを見つめる。机の上で石筆がある。"
            },
            {
                "speaker": "Toa",
                "nebulith": "Cynel el miin ia vyrkirel ul velkirel. Falun el talkirel al miin.",
                "japanese": "私たちは天測の鉄筆と木軸のペンを愛用する。私たちに石筆が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "vyrkirel",
                "pos": "名",
                "meaningJa": "天測の鉄筆、星図用のペン、星見のスタイラス",
                "meaningEn": "astronomical stylus, star-chart pen, celestial graver",
                "morphemes": [
                    "vyr",
                    "kirel"
                ],
                "etymology": "vyr(星・天体) + kirel(筆・ペン)",
                "category": "15. 工芸・道具・物質",
                "example_sentence": "Vyrel el mi ia vyrkirel ul velkirel uo dovik.",
                "example_ja": "私は机の上で天測の鉄筆と木軸のペンを見つめる。"
            },
            {
                "nrs": "velkirel",
                "pos": "名",
                "meaningJa": "木軸のペン、樹木の筆、木製スタイラス",
                "meaningEn": "wooden-shafted pen, timber stylus, sylvan brush",
                "morphemes": [
                    "vel",
                    "kirel"
                ],
                "etymology": "vel(木・樹木) + kirel(筆・ペン)",
                "category": "15. 工芸・道具・物質",
                "example_sentence": "Vyrel el mi ia vyrkirel ul velkirel uo dovik.",
                "example_ja": "私は机の上で天測の鉄筆と木軸のペンを見つめる。"
            },
            {
                "nrs": "talkirel",
                "pos": "名",
                "meaningJa": "石筆、鉱石の鉄筆、粘土板のスタイラス",
                "meaningEn": "slate pencil, mineral stylus, earthen graver",
                "morphemes": [
                    "tal",
                    "kirel"
                ],
                "etymology": "tal(大地・石) + kirel(筆・鉄筆)",
                "category": "15. 工芸・道具・物質",
                "example_sentence": "Relen el talkirel uo dovik.",
                "example_ja": "机の上で石筆がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-44",
        "batch": "Batch 11",
        "domain": "建築・天文台の扉と水門の扉",
        "title": "星見台の門扉と円拱のゲート",
        "communicative_need": "星見台の扉、水路の水門扉、円形のアーチ門を見回る。",
        "agent_a": {
            "name": "Sev",
            "role": "鍵束を持つ灯守"
        },
        "agent_b": {
            "name": "Toa",
            "role": "水門を点検する舟守"
        },
        "turns": [
            {
                "speaker": "Sev",
                "nebulith": "Vymin el mi ia vyrlerel ul darlerel uo domom. Relen el klorlerel uo domom.",
                "japanese": "私は街の中で星見台の扉と水門の扉を守る。街の中で円拱の門がある。"
            },
            {
                "speaker": "Toa",
                "nebulith": "Vyrel el miin ia vyrlerel ul darlerel. Falun el klorlerel al miin.",
                "japanese": "私たちは星見台の扉と水門の扉を点検する。私たちに円拱の門が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "vyrlerel",
                "pos": "名",
                "meaningJa": "星見台の扉、天測室の門、星紋のゲート",
                "meaningEn": "observatory door, astral gate, star-crested portal",
                "morphemes": [
                    "vyr",
                    "lerel"
                ],
                "etymology": "vyr(星・天体) + lerel(扉・ゲート)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Vymin el mi ia vyrlerel ul darlerel uo domom.",
                "example_ja": "私は街の中で星見台の扉と水門の扉を守る。"
            },
            {
                "nrs": "darlerel",
                "pos": "名",
                "meaningJa": "水門の扉、水路のゲート、船着き場の門",
                "meaningEn": "sluice gate, canal lock door, waterside portal",
                "morphemes": [
                    "dar",
                    "lerel"
                ],
                "etymology": "dar(しずく・水路) + lerel(扉・ゲート)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Vymin el mi ia vyrlerel ul darlerel uo domom.",
                "example_ja": "私は街の中で星見台の扉と水門の扉を守る。"
            },
            {
                "nrs": "klorlerel",
                "pos": "名",
                "meaningJa": "円拱の門、アーチ扉、円形のゲート",
                "meaningEn": "circular archway, round portal, ring gate",
                "morphemes": [
                    "klor",
                    "lerel"
                ],
                "etymology": "klor(円・環) + lerel(扉・ゲート)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Relen el klorlerel uo domom.",
                "example_ja": "街の中で円拱の門がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-45",
        "batch": "Batch 12",
        "domain": "住空間・石の腰掛けと銀飾りの椅子",
        "title": "庭の石椅子と白木の座席",
        "communicative_need": "中庭の石の腰掛け、銀飾りの椅子、白い座席を整える。",
        "agent_a": {
            "name": "Toa",
            "role": "家具を運ぶ舟守"
        },
        "agent_b": {
            "name": "Yura",
            "role": "席を設ける写字生"
        },
        "turns": [
            {
                "speaker": "Toa",
                "nebulith": "Vyrel el mi ia taltasel ul tynitasel uo velar. Relen el alintasel uo velar.",
                "japanese": "私は中庭で石の腰掛けと銀飾りの椅子を見つめる。中庭で白木の椅子がある。"
            },
            {
                "speaker": "Yura",
                "nebulith": "Cynel el miin ia taltasel ul tynitasel. Falun el alintasel al miin.",
                "japanese": "私たちは石の腰掛けと銀飾りの椅子を好む。私たちに白木の椅子が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "taltasel",
                "pos": "名",
                "meaningJa": "石の腰掛け、大地のベンチ、岩の座席",
                "meaningEn": "stone bench, earthen seat, masonry stool",
                "morphemes": [
                    "tal",
                    "tasel"
                ],
                "etymology": "tal(大地・石) + tasel(椅子・座席)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Vyrel el mi ia taltasel ul tynitasel uo velar.",
                "example_ja": "私は中庭で石の腰掛けと銀飾りの椅子を見つめる。"
            },
            {
                "nrs": "tynitasel",
                "pos": "名",
                "meaningJa": "銀飾りの椅子、白銀の座席、銀細工の腰掛け",
                "meaningEn": "silver-trimmed chair, gleaming seat, silver stool",
                "morphemes": [
                    "tyni",
                    "tasel"
                ],
                "etymology": "tyni(銀色の・白銀の) + tasel(椅子・座席)",
                "category": "15. 工芸・道具・物質",
                "example_sentence": "Vyrel el mi ia taltasel ul tynitasel uo velar.",
                "example_ja": "私は中庭で石の腰掛けと銀飾りの椅子を見つめる。"
            },
            {
                "nrs": "alintasel",
                "pos": "名",
                "meaningJa": "白木の椅子、純白の座席、白い腰掛け",
                "meaningEn": "white chair, pale timber seat, ivory bench",
                "morphemes": [
                    "alin",
                    "tasel"
                ],
                "etymology": "alin(白い・純白の) + tasel(椅子・座席)",
                "category": "15. 工芸・道具・物質",
                "example_sentence": "Relen el alintasel uo velar.",
                "example_ja": "中庭で白木の椅子がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-46",
        "batch": "Batch 12",
        "domain": "食文化・里の食堂と水辺の茶屋",
        "title": "水辺の喫茶店と星見の食堂",
        "communicative_need": "大地の里の食堂、水辺の茶屋、星見のテラス食堂を訪ねる。",
        "agent_a": {
            "name": "Neri",
            "role": "食材を届ける採集師"
        },
        "agent_b": {
            "name": "Toa",
            "role": "昼食をとる舟守"
        },
        "turns": [
            {
                "speaker": "Neri",
                "nebulith": "Vyrel el mi ia talnerar ul darnerar uo domom. Relen el vyrnerar uo domom.",
                "japanese": "私は街の中で里の食堂と水辺の茶屋を見つめる。街の中で星見の食堂がある。"
            },
            {
                "speaker": "Toa",
                "nebulith": "Cynel el miin ia talnerar ul darnerar. Falun el vyrnerar al miin.",
                "japanese": "私たちは里の食堂と水辺の茶屋を愛する。私たちに星見の食堂が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "talnerar",
                "pos": "名",
                "meaningJa": "里の食堂、大地の食事処、郷土料理店",
                "meaningEn": "countryside dining hall, earthen tavern, local eatery",
                "morphemes": [
                    "tal",
                    "nerar"
                ],
                "etymology": "tal(大地・里) + nerar(食堂・カフェ)",
                "category": "12. 食文化・料理・飲食",
                "example_sentence": "Vyrel el mi ia talnerar ul darnerar uo domom.",
                "example_ja": "私は街の中で里の食堂と水辺の茶屋を見つめる。"
            },
            {
                "nrs": "darnerar",
                "pos": "名",
                "meaningJa": "水辺の茶屋、湖畔のカフェ、運河の食堂",
                "meaningEn": "waterside cafe, lakeside teahouse, canal bistro",
                "morphemes": [
                    "dar",
                    "nerar"
                ],
                "etymology": "dar(しずく・水辺) + nerar(カフェ・食堂)",
                "category": "12. 食文化・料理・飲食",
                "example_sentence": "Vyrel el mi ia talnerar ul darnerar uo domom.",
                "example_ja": "私は街の中で里の食堂と水辺の茶屋を見つめる。"
            },
            {
                "nrs": "vyrnerar",
                "pos": "名",
                "meaningJa": "星見の食堂、夜間カフェ、星空テラスの茶屋",
                "meaningEn": "starlight cafe, night bistro, observatory dining room",
                "morphemes": [
                    "vyr",
                    "nerar"
                ],
                "etymology": "vyr(星・天体) + nerar(カフェ・食堂)",
                "category": "12. 食文化・料理・飲食",
                "example_sentence": "Relen el vyrnerar uo domom.",
                "example_ja": "街の中で星見の食堂がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-47",
        "batch": "Batch 12",
        "domain": "食文化・土竈の厨房と白い配膳室",
        "title": "石造りの調理場と木の厨房",
        "communicative_need": "土竈のある調理場、木組みの厨房、清潔な白い配膳室を整える。",
        "agent_a": {
            "name": "Sev",
            "role": "火種を配る灯守"
        },
        "agent_b": {
            "name": "Neri",
            "role": "香草を並べる採集師"
        },
        "turns": [
            {
                "speaker": "Sev",
                "nebulith": "Vymin el mi ia talnerom ul velnerom uo govan. Relen el alinnerom uo govan.",
                "japanese": "私は家の中で土竈の調理場と木組みの厨房を清潔に守る。家の中で白壁の配膳室がある。"
            },
            {
                "speaker": "Neri",
                "nebulith": "Vyrel el miin ia talnerom ul velnerom. Falun el alinnerom al miin.",
                "japanese": "私たちは土竈の調理場と木組みの厨房を確かめる。私たちに白壁の配膳室が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "talnerom",
                "pos": "名",
                "meaningJa": "土竈の調理場、石造りの厨房、地階の炊事室",
                "meaningEn": "earthen-hearth kitchen, stone galley, ground scullery",
                "morphemes": [
                    "tal",
                    "nerom"
                ],
                "etymology": "tal(大地・土石) + nerom(厨房・調理室)",
                "category": "12. 食文化・料理・飲食",
                "example_sentence": "Vymin el mi ia talnerom ul velnerom uo govan.",
                "example_ja": "私は家の中で土竈の調理場と木組みの厨房を清潔に守る。"
            },
            {
                "nrs": "velnerom",
                "pos": "名",
                "meaningJa": "木組みの厨房、森の炊事場、木造の調理室",
                "meaningEn": "timber kitchen, woodland cookhouse, wooden galley",
                "morphemes": [
                    "vel",
                    "nerom"
                ],
                "etymology": "vel(木・樹木) + nerom(厨房・調理室)",
                "category": "12. 食文化・料理・飲食",
                "example_sentence": "Vymin el mi ia talnerom ul velnerom uo govan.",
                "example_ja": "私は家の中で土竈の調理場と木組みの厨房を清潔に守る。"
            },
            {
                "nrs": "alinnerom",
                "pos": "名",
                "meaningJa": "白壁の配膳室、清潔な白い厨房、純白の調理室",
                "meaningEn": "whitewashed kitchen, clean bright pantry, white galley",
                "morphemes": [
                    "alin",
                    "nerom"
                ],
                "etymology": "alin(白い・清潔な) + nerom(厨房・配膳所)",
                "category": "12. 食文化・料理・飲食",
                "example_sentence": "Relen el alinnerom uo govan.",
                "example_ja": "家の中で白壁の配膳室がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-48",
        "batch": "Batch 12",
        "domain": "食文化・今日の献立と山の幸・川の幸",
        "title": "本日の温かい食事と森の料理",
        "communicative_need": "今日の温かい料理、森の草木料理、水辺の魚菜料理を味わう。",
        "agent_a": {
            "name": "Neri",
            "role": "料理を盛り付ける採集師"
        },
        "agent_b": {
            "name": "Yura",
            "role": "献立を記す写字生"
        },
        "turns": [
            {
                "speaker": "Neri",
                "nebulith": "Kiras el mi ia hanonerel ul velnerel uo nerar. Relen el darnerel uo nerar.",
                "japanese": "私は食堂で今日の料理と森の料理を調理する。食堂で水辺の料理がある。"
            },
            {
                "speaker": "Yura",
                "nebulith": "Neran el miin ia hanonerel ul velnerel. Falun el darnerel al miin.",
                "japanese": "私たちは今日の料理と森の料理を味わう。私たちに水辺の料理が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "hanonerel",
                "pos": "名",
                "meaningJa": "今日の料理、本日の献立、当日の温かいごはん",
                "meaningEn": "today's meal, daily dish, fare of the day",
                "morphemes": [
                    "hano",
                    "nerel"
                ],
                "etymology": "hano(今日・本日) + nerel(料理・ごはん)",
                "category": "12. 食文化・料理・飲食",
                "example_sentence": "Kiras el mi ia hanonerel ul velnerel uo nerar.",
                "example_ja": "私は食堂で今日の料理と森の料理を調理する。"
            },
            {
                "nrs": "velnerel",
                "pos": "名",
                "meaningJa": "森の料理、木の実と山菜の食事、草木料理",
                "meaningEn": "woodland cuisine, forest-harvest meal, herbal dish",
                "morphemes": [
                    "vel",
                    "nerel"
                ],
                "etymology": "vel(木・草木) + nerel(料理・食事)",
                "category": "12. 食文化・料理・飲食",
                "example_sentence": "Kiras el mi ia hanonerel ul velnerel uo nerar.",
                "example_ja": "私は食堂で今日の料理と森の料理を調理する。"
            },
            {
                "nrs": "darnerel",
                "pos": "名",
                "meaningJa": "水辺の料理、清流の恵みの食事、瑞々しい料理",
                "meaningEn": "waterside dish, freshwater meal, brookside fare",
                "morphemes": [
                    "dar",
                    "nerel"
                ],
                "etymology": "dar(しずく・水辺) + nerel(料理・食事)",
                "category": "12. 食文化・料理・飲食",
                "example_sentence": "Relen el darnerel uo nerar.",
                "example_ja": "食堂で水辺の料理がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-49",
        "batch": "Batch 13",
        "domain": "食文化・樹皮の薬草茶と白茶の振る舞い",
        "title": "木々の煎じ茶と今日の温茶",
        "communicative_need": "木々の香る煎じ茶、今日淹れた薬草茶、澄んだ白茶を振る舞う。",
        "agent_a": {
            "name": "Neri",
            "role": "茶葉を煎じる採集師"
        },
        "agent_b": {
            "name": "Sev",
            "role": "湯を沸かす灯守"
        },
        "turns": [
            {
                "speaker": "Neri",
                "nebulith": "Bion el mi ia velterin ul hanoterin uo govan. Relen el alinterin uo govan.",
                "japanese": "私は家の中で木々の煎じ茶と今日の煎じ茶を飲む。家の中で白茶がある。"
            },
            {
                "speaker": "Sev",
                "nebulith": "Cynel el miin ia velterin ul hanoterin. Falun el alinterin al miin.",
                "japanese": "私たちは木々の煎じ茶と今日の煎じ茶を好む。私たちに白茶が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "velterin",
                "pos": "名",
                "meaningJa": "木々の煎じ茶、樹皮と若葉の茶、森の薬草茶",
                "meaningEn": "woodland herbal tea, bark infusion, forest tisane",
                "morphemes": [
                    "vel",
                    "terin"
                ],
                "etymology": "vel(木・樹木) + terin(煎じ茶・薬草茶)",
                "category": "12. 食文化・料理・飲食",
                "example_sentence": "Bion el mi ia velterin ul hanoterin uo govan.",
                "example_ja": "私は家の中で木々の煎じ茶と今日の煎じ茶を飲む。"
            },
            {
                "nrs": "hanoterin",
                "pos": "名",
                "meaningJa": "今日の煎じ茶、本日の薬草茶、淹れたての温茶",
                "meaningEn": "today's tea, daily herbal infusion, fresh warm brew",
                "morphemes": [
                    "hano",
                    "terin"
                ],
                "etymology": "hano(今日・本日) + terin(煎じ茶・薬草茶)",
                "category": "12. 食文化・料理・飲食",
                "example_sentence": "Bion el mi ia velterin ul hanoterin uo govan.",
                "example_ja": "私は家の中で木々の煎じ茶と今日の煎じ茶を飲む。"
            },
            {
                "nrs": "alinterin",
                "pos": "名",
                "meaningJa": "白茶、澄んだ煎じ茶、純白の花茶",
                "meaningEn": "white tea, clear herbal infusion, pale blossom tisane",
                "morphemes": [
                    "alin",
                    "terin"
                ],
                "etymology": "alin(白い・澄んだ) + terin(煎じ茶・薬草茶)",
                "category": "12. 食文化・料理・飲食",
                "example_sentence": "Relen el alinterin uo govan.",
                "example_ja": "家の中で白茶がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-50",
        "batch": "Batch 13",
        "domain": "自然・星見の高嶺と夜の連峰",
        "title": "星を頂く山嶺と大地の連峰",
        "communicative_need": "星に近い高嶺、どっしりとした大地の山並み、夜闇に浮かぶ山を見上げる。",
        "agent_a": {
            "name": "Sev",
            "role": "高台から山を望む灯守"
        },
        "agent_b": {
            "name": "Toa",
            "role": "山影を目印にする舟守"
        },
        "turns": [
            {
                "speaker": "Sev",
                "nebulith": "Vyrel el mi ia vyrnovan ul talnovan uo talom. Relen el kymnovan uo talom.",
                "japanese": "私は平原で星見の高嶺と大地の連峰を観測する。平原で夜の山嶺がある。"
            },
            {
                "speaker": "Toa",
                "nebulith": "Soran el miin ia vyrnovan ul talnovan. Falun el kymnovan al miin.",
                "japanese": "私たちは星見の高嶺と大地の連峰を記録する。私たちに夜の山嶺が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "vyrnovan",
                "pos": "名",
                "meaningJa": "星見の高嶺、星を頂く山、天測の峰",
                "meaningEn": "starlit peak, astral mountain, observatory summit",
                "morphemes": [
                    "vyr",
                    "novan"
                ],
                "etymology": "vyr(星・天体) + novan(山・連峰)",
                "category": "6. 地球自然・地形・地質",
                "example_sentence": "Vyrel el mi ia vyrnovan ul talnovan uo talom.",
                "example_ja": "私は平原で星見の高嶺と大地の連峰を観測する。"
            },
            {
                "nrs": "talnovan",
                "pos": "名",
                "meaningJa": "大地の連峰、岩山、堂々たる山岳",
                "meaningEn": "earthen mountain range, rocky massif, terrestrial peak",
                "morphemes": [
                    "tal",
                    "novan"
                ],
                "etymology": "tal(大地・岩) + novan(山・連峰)",
                "category": "6. 地球自然・地形・地質",
                "example_sentence": "Vyrel el mi ia vyrnovan ul talnovan uo talom.",
                "example_ja": "私は平原で星見の高嶺と大地の連峰を観測する。"
            },
            {
                "nrs": "kymnovan",
                "pos": "名",
                "meaningJa": "夜の山嶺、宵闇の連峰、夜影の山",
                "meaningEn": "night mountain, dark silhouette peak, nocturnal ridge",
                "morphemes": [
                    "kym",
                    "novan"
                ],
                "etymology": "kym(夜・闇) + novan(山・連峰)",
                "category": "6. 地球自然・地形・地質",
                "example_sentence": "Relen el kymnovan uo talom.",
                "example_ja": "平原で夜の山嶺がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-51",
        "batch": "Batch 13",
        "domain": "自然・湖上の浮島と緑の木島",
        "title": "水辺の環礁と星見の小島",
        "communicative_need": "湖に浮かぶ水辺の島、木々の茂る緑島、星を観測する孤島を巡る。",
        "agent_a": {
            "name": "Toa",
            "role": "島へ舟を漕ぐ舟守"
        },
        "agent_b": {
            "name": "Neri",
            "role": "島の植物を調べる採集師"
        },
        "turns": [
            {
                "speaker": "Toa",
                "nebulith": "Vyrel el mi ia dartalon ul veltalon uo daron. Relen el vyrtalon uo daron.",
                "japanese": "私は湖の上で水辺の浮島と木々の茂る島を見つめる。湖の上で星見の孤島がある。"
            },
            {
                "speaker": "Neri",
                "nebulith": "Vymin el miin ia dartalon ul veltalon. Falun el vyrtalon al miin.",
                "japanese": "私たちは水辺の浮島と木々の茂る島を守る。私たちに星見の孤島が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "dartalon",
                "pos": "名",
                "meaningJa": "水辺の浮島、湖上の小島、水の環礁",
                "meaningEn": "water island, lake islet, aquatic atoll",
                "morphemes": [
                    "dar",
                    "talon"
                ],
                "etymology": "dar(しずく・水) + talon(島・環礁)",
                "category": "6. 地球自然・地形・地質",
                "example_sentence": "Vyrel el mi ia dartalon ul veltalon uo daron.",
                "example_ja": "私は湖の上で水辺の浮島と木々の茂る島を見つめる。"
            },
            {
                "nrs": "veltalon",
                "pos": "名",
                "meaningJa": "木々の茂る島、森の小島、緑の浮島",
                "meaningEn": "wooded island, forested islet, sylvan cay",
                "morphemes": [
                    "vel",
                    "talon"
                ],
                "etymology": "vel(木・森林) + talon(島・孤立陸地)",
                "category": "6. 地球自然・地形・地質",
                "example_sentence": "Vyrel el mi ia dartalon ul veltalon uo daron.",
                "example_ja": "私は湖の上で水辺の浮島と木々の茂る島を見つめる。"
            },
            {
                "nrs": "vyrtalon",
                "pos": "名",
                "meaningJa": "星見の孤島、天測の島、星影の環礁",
                "meaningEn": "starlit island, astral atoll, stargazer's isle",
                "morphemes": [
                    "vyr",
                    "talon"
                ],
                "etymology": "vyr(星・天体) + talon(島・環礁)",
                "category": "6. 地球自然・地形・地質",
                "example_sentence": "Relen el vyrtalon uo daron.",
                "example_ja": "湖の上で星見の孤島がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-52",
        "batch": "Batch 13",
        "domain": "自然・水辺の林と星降る樹海",
        "title": "清流の森と静かな夜の森",
        "communicative_need": "水を湛えた水辺の森、星降る樹海、静寂に包まれた夜の森を歩く。",
        "agent_a": {
            "name": "Neri",
            "role": "森の奥へ進む採集師"
        },
        "agent_b": {
            "name": "Yura",
            "role": "森林の地図を描く写字生"
        },
        "turns": [
            {
                "speaker": "Neri",
                "nebulith": "Vyrel el mi ia darvelom ul vyrvelom uo talom. Relen el kymvelom uo talom.",
                "japanese": "私は原野で水辺の森と星降る森を見つめる。原野で夜の森がある。"
            },
            {
                "speaker": "Yura",
                "nebulith": "Cynel el miin ia darvelom ul vyrvelom. Falun el kymvelom al miin.",
                "japanese": "私たちは水辺の森と星降る森を愛する。私たちに夜の森が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "darvelom",
                "pos": "名",
                "meaningJa": "水辺の森、渓流の森林、潤いの樹林",
                "meaningEn": "waterside forest, riparian woodland, stream grove",
                "morphemes": [
                    "dar",
                    "velom"
                ],
                "etymology": "dar(しずく・水) + velom(森・森林)",
                "category": "8. 植物・森林・菌類",
                "example_sentence": "Vyrel el mi ia darvelom ul vyrvelom uo talom.",
                "example_ja": "私は原野で水辺の森と星降る森を見つめる。"
            },
            {
                "nrs": "vyrvelom",
                "pos": "名",
                "meaningJa": "星降る森、星見の樹海、星影の林",
                "meaningEn": "starlit forest, astral woodland, starry grove",
                "morphemes": [
                    "vyr",
                    "velom"
                ],
                "etymology": "vyr(星・光点) + velom(森・樹海)",
                "category": "8. 植物・森林・菌類",
                "example_sentence": "Vyrel el mi ia darvelom ul vyrvelom uo talom.",
                "example_ja": "私は原野で水辺の森と星降る森を見つめる。"
            },
            {
                "nrs": "kymvelom",
                "pos": "名",
                "meaningJa": "夜の森、宵闇の樹海、静夜の森林",
                "meaningEn": "night forest, nocturnal woods, dark sylvan grove",
                "morphemes": [
                    "kym",
                    "velom"
                ],
                "etymology": "kym(夜・闇) + velom(森・森林)",
                "category": "8. 植物・森林・菌類",
                "example_sentence": "Relen el kymvelom uo talom.",
                "example_ja": "原野で夜の森がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-53",
        "batch": "Batch 14",
        "domain": "植物・朝露の若芽と大地の薬草",
        "title": "水滴を宿す新芽と星見草",
        "communicative_need": "朝露を宿す若芽、大地から芽吹く薬草、星のように開く新芽を観察する。",
        "agent_a": {
            "name": "Neri",
            "role": "薬草を摘む採集師"
        },
        "agent_b": {
            "name": "Sev",
            "role": "薬草園を照らす灯守"
        },
        "turns": [
            {
                "speaker": "Neri",
                "nebulith": "Vyrel el mi ia darvelil ul talvelil uo velar. Relen el vyrvelil uo velar.",
                "japanese": "私は庭園で朝露の若芽と大地の若草を観察する。庭園で星見草がある。"
            },
            {
                "speaker": "Sev",
                "nebulith": "Vymin el miin ia darvelil ul talvelil. Falun el vyrvelil al miin.",
                "japanese": "私たちは朝露の若芽と大地の若草を育てる。私たちに星見草が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "darvelil",
                "pos": "名",
                "meaningJa": "朝露の若芽、水辺の薬草、瑞々しい新芽",
                "meaningEn": "dewy sprout, waterside herb, moist seedling",
                "morphemes": [
                    "dar",
                    "velil"
                ],
                "etymology": "dar(しずく・朝露) + velil(新芽・薬草)",
                "category": "8. 植物・森林・菌類",
                "example_sentence": "Vyrel el mi ia darvelil ul talvelil uo velar.",
                "example_ja": "私は庭園で朝露の若芽と大地の若草を観察する。"
            },
            {
                "nrs": "talvelil",
                "pos": "名",
                "meaningJa": "大地の若草、土から出る新芽、根生薬草",
                "meaningEn": "earthen shoot, ground herb, sprouting seedling",
                "morphemes": [
                    "tal",
                    "velil"
                ],
                "etymology": "tal(大地・土壌) + velil(新芽・薬草)",
                "category": "8. 植物・森林・菌類",
                "example_sentence": "Vyrel el mi ia darvelil ul talvelil uo velar.",
                "example_ja": "私は庭園で朝露の若芽と大地の若草を観察する。"
            },
            {
                "nrs": "vyrvelil",
                "pos": "名",
                "meaningJa": "星見草、星形の新芽、夜に香る薬草",
                "meaningEn": "star-sprout, astral herb, night-blooming seedling",
                "morphemes": [
                    "vyr",
                    "velil"
                ],
                "etymology": "vyr(星・光点) + velil(新芽・薬草)",
                "category": "8. 植物・森林・菌類",
                "example_sentence": "Relen el vyrvelil uo velar.",
                "example_ja": "庭園で星見草がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-54",
        "batch": "Batch 14",
        "domain": "物質・星石の結晶と川底の白石",
        "title": "星の鉱石と水辺の丸石",
        "communicative_need": "星光を宿す結晶石、清流の川石、純白の石英を集める。",
        "agent_a": {
            "name": "Toa",
            "role": "河原で石を拾う舟守"
        },
        "agent_b": {
            "name": "Yura",
            "role": "鉱物標本を記す写字生"
        },
        "turns": [
            {
                "speaker": "Toa",
                "nebulith": "Vyrel el mi ia vyrtalyr ul dartalyr uo daris. Relen el alintalyr uo daris.",
                "japanese": "私は清流で星石の結晶と水辺の丸石を見つめる。清流で白石がある。"
            },
            {
                "speaker": "Yura",
                "nebulith": "Soran el miin ia vyrtalyr ul dartalyr. Falun el alintalyr al miin.",
                "japanese": "私たちは星石の結晶と水辺の丸石を記録する。私たちに白石が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "vyrtalyr",
                "pos": "名",
                "meaningJa": "星石の結晶、星光を帯びた鉱石、天測石",
                "meaningEn": "star-crystal, astral ore, starlight mineral",
                "morphemes": [
                    "vyr",
                    "talyr"
                ],
                "etymology": "vyr(星・光点) + talyr(石・結晶)",
                "category": "6. 地球自然・地形・地質",
                "example_sentence": "Vyrel el mi ia vyrtalyr ul dartalyr uo daris.",
                "example_ja": "私は清流で星石の結晶と水辺の丸石を見つめる。"
            },
            {
                "nrs": "dartalyr",
                "pos": "名",
                "meaningJa": "水辺の丸石、川底の清石、水に磨かれた石",
                "meaningEn": "river stone, water-smoothed pebble, stream rock",
                "morphemes": [
                    "dar",
                    "talyr"
                ],
                "etymology": "dar(しずく・水) + talyr(石・岩)",
                "category": "6. 地球自然・地形・地質",
                "example_sentence": "Vyrel el mi ia vyrtalyr ul dartalyr uo daris.",
                "example_ja": "私は清流で星石の結晶と水辺の丸石を見つめる。"
            },
            {
                "nrs": "alintalyr",
                "pos": "名",
                "meaningJa": "白石、純白の石英、白い結晶石",
                "meaningEn": "white quartz, pure white stone, alabaster crystal",
                "morphemes": [
                    "alin",
                    "talyr"
                ],
                "etymology": "alin(白い・純白の) + talyr(石・結晶)",
                "category": "6. 地球自然・地形・地質",
                "example_sentence": "Relen el alintalyr uo daris.",
                "example_ja": "清流で白石がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-55",
        "batch": "Batch 14",
        "domain": "工芸・白銀の合金と地金の精錬",
        "title": "銀色の金属資材と白い軽合金",
        "communicative_need": "銀色の精錬合金、白い軽金属、大地から採れた地金を点検する。",
        "agent_a": {
            "name": "Sev",
            "role": "炉の火を守る灯守"
        },
        "agent_b": {
            "name": "Toa",
            "role": "金具を鍛える舟守"
        },
        "turns": [
            {
                "speaker": "Sev",
                "nebulith": "Vyrel el mi ia tynitalur ul alintalur uo vorn. Relen el taltalur uo vorn.",
                "japanese": "私は工房の部屋で白銀の合金と白色合金を確かめる。工房の部屋で大地の地金がある。"
            },
            {
                "speaker": "Toa",
                "nebulith": "Kiras el miin ia tynitalur ul alintalur. Falun el taltalur al miin.",
                "japanese": "私たちは白銀の合金と白色合金を鍛える。私たちに大地の地金が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "tynitalur",
                "pos": "名",
                "meaningJa": "白銀の合金、銀色の金属、光沢ある精錬材",
                "meaningEn": "silver alloy, silvery metal, gleaming ingot",
                "morphemes": [
                    "tyni",
                    "talur"
                ],
                "etymology": "tyni(銀色の・白銀の) + talur(金属・合金)",
                "category": "15. 工芸・道具・物質",
                "example_sentence": "Vyrel el mi ia tynitalur ul alintalur uo vorn.",
                "example_ja": "私は工房の部屋で白銀の合金と白色合金を確かめる。"
            },
            {
                "nrs": "alintalur",
                "pos": "名",
                "meaningJa": "白色合金、純白の軽金属、白い精錬資材",
                "meaningEn": "white metal, bright light alloy, pale ingot",
                "morphemes": [
                    "alin",
                    "talur"
                ],
                "etymology": "alin(白い・純白の) + talur(金属・合金)",
                "category": "15. 工芸・道具・物質",
                "example_sentence": "Vyrel el mi ia tynitalur ul alintalur uo vorn.",
                "example_ja": "私は工房の部屋で白銀の合金と白色合金を確かめる。"
            },
            {
                "nrs": "taltalur",
                "pos": "名",
                "meaningJa": "大地の地金、粗金属、鉱山の金属資材",
                "meaningEn": "raw earthen metal, base ore ingot, terrestrial alloy",
                "morphemes": [
                    "tal",
                    "talur"
                ],
                "etymology": "tal(大地・鉱山) + talur(金属・資材)",
                "category": "15. 工芸・道具・物質",
                "example_sentence": "Relen el taltalur uo vorn.",
                "example_ja": "工房の部屋で大地の地金がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-56",
        "batch": "Batch 14",
        "domain": "工芸・石刃の小刀と木柄のナイフ",
        "title": "大地の石小刀と白い骨刀",
        "communicative_need": "硬い石刃の小刀、木柄の工作ナイフ、白い細工小刀を使い分ける。",
        "agent_a": {
            "name": "Neri",
            "role": "茎を切り分ける採集師"
        },
        "agent_b": {
            "name": "Toa",
            "role": "綱を切る舟守"
        },
        "turns": [
            {
                "speaker": "Neri",
                "nebulith": "Vyrel el mi ia talserel ul velserel uo govan. Relen el alinserel uo govan.",
                "japanese": "私は家の中で石刃の小刀と木柄の小刀を点検する。家の中で白い細工小刀がある。"
            },
            {
                "speaker": "Toa",
                "nebulith": "Vymin el miin ia talserel ul velserel. Falun el alinserel al miin.",
                "japanese": "私たちは石刃の小刀と木柄の小刀を手入れする。私たちに白い細工小刀が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "talserel",
                "pos": "名",
                "meaningJa": "石刃の小刀、黒曜のナイフ、鉱石の刃物",
                "meaningEn": "stone-bladed knife, obsidian cutter, mineral blade",
                "morphemes": [
                    "tal",
                    "serel"
                ],
                "etymology": "tal(大地・石) + serel(小刀・ナイフ)",
                "category": "15. 工芸・道具・物質",
                "example_sentence": "Vyrel el mi ia talserel ul velserel uo govan.",
                "example_ja": "私は家の中で石刃の小刀と木柄の小刀を点検する。"
            },
            {
                "nrs": "velserel",
                "pos": "名",
                "meaningJa": "木柄の小刀、接ぎ木ナイフ、木工用の刃物",
                "meaningEn": "wood-handled knife, grafting blade, whittling knife",
                "morphemes": [
                    "vel",
                    "serel"
                ],
                "etymology": "vel(木・樹木) + serel(小刀・ナイフ)",
                "category": "15. 工芸・道具・物質",
                "example_sentence": "Vyrel el mi ia talserel ul velserel uo govan.",
                "example_ja": "私は家の中で石刃の小刀と木柄の小刀を点検する。"
            },
            {
                "nrs": "alinserel",
                "pos": "名",
                "meaningJa": "白い細工小刀、白磁の刃、清浄な調理ナイフ",
                "meaningEn": "white craft knife, pale ceramic blade, clean paring knife",
                "morphemes": [
                    "alin",
                    "serel"
                ],
                "etymology": "alin(白い・清らかな) + serel(小刀・調理刃)",
                "category": "15. 工芸・道具・物質",
                "example_sentence": "Relen el alinserel uo govan.",
                "example_ja": "家の中で白い細工小刀がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-57",
        "batch": "Batch 15",
        "domain": "天文・星と並ぶ月と白夜の月",
        "title": "星伴う月と宵闇の月影",
        "communicative_need": "星々と並ぶ月、闇夜に浮かぶ月、白く澄んだ月を観測する。",
        "agent_a": {
            "name": "Sev",
            "role": "月齢を測る灯守"
        },
        "agent_b": {
            "name": "Yura",
            "role": "月運行表を記す写字生"
        },
        "turns": [
            {
                "speaker": "Sev",
                "nebulith": "Vyrel el mi ia vyrtynes ul kymtynes uo celen. Relen el alintynes uo celen.",
                "japanese": "私は空で星伴う月と宵闇の月を観測する。空で白月がある。"
            },
            {
                "speaker": "Yura",
                "nebulith": "Soran el miin ia vyrtynes ul kymtynes. Falun el alintynes al miin.",
                "japanese": "私たちは星伴う月と宵闇の月を書き留める。私たちに白月が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "vyrtynes",
                "pos": "名",
                "meaningJa": "星伴う月、星辰と並ぶ衛星、星見の月",
                "meaningEn": "star-accompanied moon, astral satellite, starry orb",
                "morphemes": [
                    "vyr",
                    "tynes"
                ],
                "etymology": "vyr(星・天体) + tynes(月・衛星)",
                "category": "1. 天体・宇宙・天文",
                "example_sentence": "Vyrel el mi ia vyrtynes ul kymtynes uo celen.",
                "example_ja": "私は空で星伴う月と宵闇の月を観測する。"
            },
            {
                "nrs": "kymtynes",
                "pos": "名",
                "meaningJa": "宵闇の月、夜空の光球、深夜の月",
                "meaningEn": "night moon, nocturnal lunar orb, midnight satellite",
                "morphemes": [
                    "kym",
                    "tynes"
                ],
                "etymology": "kym(夜・闇) + tynes(月・夜の光球)",
                "category": "1. 天体・宇宙・天文",
                "example_sentence": "Vyrel el mi ia vyrtynes ul kymtynes uo celen.",
                "example_ja": "私は空で星伴う月と宵闇の月を観測する。"
            },
            {
                "nrs": "alintynes",
                "pos": "名",
                "meaningJa": "白月、純白の満月、澄み切った白い月",
                "meaningEn": "white moon, pale full moon, luminous ivory orb",
                "morphemes": [
                    "alin",
                    "tynes"
                ],
                "etymology": "alin(白い・純白の) + tynes(月・光球)",
                "category": "1. 天体・宇宙・天文",
                "example_sentence": "Relen el alintynes uo celen.",
                "example_ja": "空で白月がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-58",
        "batch": "Batch 15",
        "domain": "日常・朝露の夜明けと森の朝",
        "title": "水辺の曙光と今日の夜明け",
        "communicative_need": "水辺に霧立つ朝、森の夜明け、今日という新しい朝を迎え入れる。",
        "agent_a": {
            "name": "Toa",
            "role": "早朝の舟を出す舟守"
        },
        "agent_b": {
            "name": "Neri",
            "role": "朝の森へ入る採集師"
        },
        "turns": [
            {
                "speaker": "Toa",
                "nebulith": "Vyrel el mi ia darvalar ul velvalar uo daron. Relen el hanovalar uo daron.",
                "japanese": "私は湖のほとりで朝露の夜明けと森の朝を見つめる。湖のほとりで今日の朝がある。"
            },
            {
                "speaker": "Neri",
                "nebulith": "Cynel el miin ia darvalar ul velvalar. Falun el hanovalar al miin.",
                "japanese": "私たちは朝露の夜明けと森の朝を愛する。私たちに今日の朝が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "darvalar",
                "pos": "名",
                "meaningJa": "朝露の夜明け、水辺の朝、瑞々しい曙光",
                "meaningEn": "dewy dawn, waterside morning, misty daybreak",
                "morphemes": [
                    "dar",
                    "valar"
                ],
                "etymology": "dar(しずく・朝露) + valar(朝・夜明け)",
                "category": "7. 気象・天候・季節",
                "example_sentence": "Vyrel el mi ia darvalar ul velvalar uo daron.",
                "example_ja": "私は湖のほとりで朝露の夜明けと森の朝を見つめる。"
            },
            {
                "nrs": "velvalar",
                "pos": "名",
                "meaningJa": "森の朝、木立の夜明け、小鳥鳴く曙光",
                "meaningEn": "woodland morning, forest dawn, sylvan daybreak",
                "morphemes": [
                    "vel",
                    "valar"
                ],
                "etymology": "vel(木・森林) + valar(朝・夜明け)",
                "category": "7. 気象・天候・季節",
                "example_sentence": "Vyrel el mi ia darvalar ul velvalar uo daron.",
                "example_ja": "私は湖のほとりで朝露の夜明けと森の朝を見つめる。"
            },
            {
                "nrs": "hanovalar",
                "pos": "名",
                "meaningJa": "今日の朝、今朝、本日の夜明け",
                "meaningEn": "this morning, today's dawn, present daybreak",
                "morphemes": [
                    "hano",
                    "valar"
                ],
                "etymology": "hano(今日・本日) + valar(朝・夜明け)",
                "category": "7. 気象・天候・季節",
                "example_sentence": "Relen el hanovalar uo daron.",
                "example_ja": "湖のほとりで今日の朝がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-59",
        "batch": "Batch 15",
        "domain": "日常・一番星の夕暮れと水辺の黄昏",
        "title": "星見の薄暮と今日の夕べ",
        "communicative_need": "一番星が光る夕暮れ、水面に映る黄昏、今日の穏やかな夕べを語り合う。",
        "agent_a": {
            "name": "Sev",
            "role": "夕べの灯をともす灯守"
        },
        "agent_b": {
            "name": "Yura",
            "role": "日誌を閉じる写字生"
        },
        "turns": [
            {
                "speaker": "Sev",
                "nebulith": "Vyrel el mi ia vyrkylas ul darkylas uo domom. Relen el hanokylas uo domom.",
                "japanese": "私は街の中で一番星の夕暮れと水辺の黄昏を見つめる。街の中で今日の夕暮れがある。"
            },
            {
                "speaker": "Yura",
                "nebulith": "Cynel el miin ia vyrkylas ul darkylas. Falun el hanokylas al miin.",
                "japanese": "私たちは一番星の夕暮れと水辺の黄昏をいつくしむ。私たちに今日の夕暮れが輝く。"
            }
        ],
        "words": [
            {
                "nrs": "vyrkylas",
                "pos": "名",
                "meaningJa": "一番星の夕暮れ、星見の薄暮、星影の黄昏",
                "meaningEn": "starlit dusk, evening of the first star, astral twilight",
                "morphemes": [
                    "vyr",
                    "kylas"
                ],
                "etymology": "vyr(星・光点) + kylas(夕・薄暮)",
                "category": "7. 気象・天候・季節",
                "example_sentence": "Vyrel el mi ia vyrkylas ul darkylas uo domom.",
                "example_ja": "私は街の中で一番星の夕暮れと水辺の黄昏を見つめる。"
            },
            {
                "nrs": "darkylas",
                "pos": "名",
                "meaningJa": "水辺の黄昏、湖面の夕暮れ、水影の薄暮",
                "meaningEn": "waterside twilight, lakeside dusk, rippling evening",
                "morphemes": [
                    "dar",
                    "kylas"
                ],
                "etymology": "dar(しずく・水辺) + kylas(夕・黄昏)",
                "category": "7. 気象・天候・季節",
                "example_sentence": "Vyrel el mi ia vyrkylas ul darkylas uo domom.",
                "example_ja": "私は街の中で一番星の夕暮れと水辺の黄昏を見つめる。"
            },
            {
                "nrs": "hanokylas",
                "pos": "名",
                "meaningJa": "今日の夕暮れ、今夕、本日の黄昏",
                "meaningEn": "this evening, today's dusk, present twilight",
                "morphemes": [
                    "hano",
                    "kylas"
                ],
                "etymology": "hano(今日・本日) + kylas(夕・黄昏)",
                "category": "7. 気象・天候・季節",
                "example_sentence": "Relen el hanokylas uo domom.",
                "example_ja": "街の中で今日の夕暮れがある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-60",
        "batch": "Batch 15",
        "domain": "日常・水辺の昼下がりと木陰の正午",
        "title": "清流の日中と今日の昼",
        "communicative_need": "水辺の明るい昼、木陰の涼しい日中、今日の穏やかな正午を過ごす。",
        "agent_a": {
            "name": "Neri",
            "role": "木陰で休む採集師"
        },
        "agent_b": {
            "name": "Toa",
            "role": "昼の荷を下ろす舟守"
        },
        "turns": [
            {
                "speaker": "Neri",
                "nebulith": "Vyrel el mi ia darsovil ul velsovil uo velar. Relen el hanosovil uo velar.",
                "japanese": "私は庭の中で水辺の昼と木陰の昼を感じる。庭の中で今日の昼がある。"
            },
            {
                "speaker": "Toa",
                "nebulith": "Cynel el miin ia darsovil ul velsovil. Falun el hanosovil al miin.",
                "japanese": "私たちは水辺の昼と木陰の昼を好む。私たちに今日の昼が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "darsovil",
                "pos": "名",
                "meaningJa": "水辺の昼、水面きらめく正午、清流の日中",
                "meaningEn": "waterside noon, bright midday by the water, stream daytime",
                "morphemes": [
                    "dar",
                    "sovil"
                ],
                "etymology": "dar(しずく・水辺) + sovil(昼・正午)",
                "category": "7. 気象・天候・季節",
                "example_sentence": "Vyrel el mi ia darsovil ul velsovil uo velar.",
                "example_ja": "私は庭の中で水辺の昼と木陰の昼を感じる。"
            },
            {
                "nrs": "velsovil",
                "pos": "名",
                "meaningJa": "木陰の昼、森の日中、緑陰の正午",
                "meaningEn": "woodland midday, forest noon, shaded daytime",
                "morphemes": [
                    "vel",
                    "sovil"
                ],
                "etymology": "vel(木・木陰) + sovil(昼・日中)",
                "category": "7. 気象・天候・季節",
                "example_sentence": "Vyrel el mi ia darsovil ul velsovil uo velar.",
                "example_ja": "私は庭の中で水辺の昼と木陰の昼を感じる。"
            },
            {
                "nrs": "hanosovil",
                "pos": "名",
                "meaningJa": "今日の昼、本日の正午、当日の日中",
                "meaningEn": "today's noon, midday today, present daytime",
                "morphemes": [
                    "hano",
                    "sovil"
                ],
                "etymology": "hano(今日・本日) + sovil(昼・正午)",
                "category": "7. 気象・天候・季節",
                "example_sentence": "Relen el hanosovil uo velar.",
                "example_ja": "庭の中で今日の昼がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-61",
        "batch": "Batch 16",
        "domain": "学芸・星辰書庫と円環の記録庫",
        "title": "天測の宝庫と大地の公文書館",
        "communicative_need": "星図を収める天測書庫、土地記録の書庫、円環状に並ぶ書庫を管理する。",
        "agent_a": {
            "name": "Yura",
            "role": "書庫の目録を編む写字生"
        },
        "agent_b": {
            "name": "Sev",
            "role": "書庫の灯を守る灯守"
        },
        "turns": [
            {
                "speaker": "Yura",
                "nebulith": "Vymin el mi ia vyrlivar ul tallivar uo domom. Relen el klorlivar uo domom.",
                "japanese": "私は街の中で天測の書庫と大地の記録庫を守る。街の中で円環書庫がある。"
            },
            {
                "speaker": "Sev",
                "nebulith": "Vyrel el miin ia vyrlivar ul tallivar. Falun el klorlivar al miin.",
                "japanese": "私たちは天測の書庫と大地の記録庫を点検する。私たちに円環書庫が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "vyrlivar",
                "pos": "名",
                "meaningJa": "天測の書庫、星図の保管座、星辰アーカイブ",
                "meaningEn": "astronomical archive, star-chart repository, celestial library",
                "morphemes": [
                    "vyr",
                    "livar"
                ],
                "etymology": "vyr(星・天体) + livar(星辰書庫・記録保管座)",
                "category": "9. 学問・科学・技術",
                "example_sentence": "Vymin el mi ia vyrlivar ul tallivar uo domom.",
                "example_ja": "私は街の中で天測の書庫と大地の記録庫を守る。"
            },
            {
                "nrs": "tallivar",
                "pos": "名",
                "meaningJa": "大地の記録庫、地理公文書館、郷土資料館",
                "meaningEn": "terrestrial archive, land registry vault, geographical library",
                "morphemes": [
                    "tal",
                    "livar"
                ],
                "etymology": "tal(大地・土地) + livar(書庫・記録保管座)",
                "category": "9. 学問・科学・技術",
                "example_sentence": "Vymin el mi ia vyrlivar ul tallivar uo domom.",
                "example_ja": "私は街の中で天測の書庫と大地の記録庫を守る。"
            },
            {
                "nrs": "klorlivar",
                "pos": "名",
                "meaningJa": "円環書庫、車座の閲覧庫、環状の記録館",
                "meaningEn": "rotunda library, circular archive, ring repository",
                "morphemes": [
                    "klor",
                    "livar"
                ],
                "etymology": "klor(円・環) + livar(書庫・記録保管座)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Relen el klorlivar uo domom.",
                "example_ja": "街の中で円環書庫がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-62",
        "batch": "Batch 16",
        "domain": "科学・天測計算機と銀の演算盤",
        "title": "星軌道の演算儀と今日の算定盤",
        "communicative_need": "星軌道を計算する演算儀、銀細工の計算盤、今日の算定結果を照合する。",
        "agent_a": {
            "name": "Sev",
            "role": "軌道を算出する灯守"
        },
        "agent_b": {
            "name": "Yura",
            "role": "数値を検算する写字生"
        },
        "turns": [
            {
                "speaker": "Sev",
                "nebulith": "Vyrel el mi ia vyrmator ul tynimator uo vorn. Relen el hanomator uo vorn.",
                "japanese": "私は観測室で軌道演算儀と銀の計算盤を確かめる。観測室で今日の算定盤がある。"
            },
            {
                "speaker": "Yura",
                "nebulith": "Vymin el miin ia vyrmator ul tynimator. Falun el hanomator al miin.",
                "japanese": "私たちは軌道演算儀と銀の計算盤を整備する。私たちに今日の算定盤が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "vyrmator",
                "pos": "名",
                "meaningJa": "軌道演算儀、星辰の天測計算機、恒星算定盤",
                "meaningEn": "orbital calculator, astral astrolabe, star-reckoning engine",
                "morphemes": [
                    "vyr",
                    "mator"
                ],
                "etymology": "vyr(星・天体) + mator(星辰演算儀・天測計算機)",
                "category": "3. 数理・情報・計算機",
                "example_sentence": "Vyrel el mi ia vyrmator ul tynimator uo vorn.",
                "example_ja": "私は観測室で軌道演算儀と銀の計算盤を確かめる。"
            },
            {
                "nrs": "tynimator",
                "pos": "名",
                "meaningJa": "銀の計算盤、白銀の天測儀、精密演算器",
                "meaningEn": "silver abacus, silver-framed calculator, precision reckoning plate",
                "morphemes": [
                    "tyni",
                    "mator"
                ],
                "etymology": "tyni(銀色の・白銀の) + mator(演算儀・計算機)",
                "category": "3. 数理・情報・計算機",
                "example_sentence": "Vyrel el mi ia vyrmator ul tynimator uo vorn.",
                "example_ja": "私は観測室で軌道演算儀と銀の計算盤を確かめる。"
            },
            {
                "nrs": "hanomator",
                "pos": "名",
                "meaningJa": "今日の算定盤、本日の演算記録機、当日の計算儀",
                "meaningEn": "today's reckoning slate, daily computation board, current calculator",
                "morphemes": [
                    "hano",
                    "mator"
                ],
                "etymology": "hano(今日・本日) + mator(演算儀・計算機)",
                "category": "3. 数理・情報・計算機",
                "example_sentence": "Relen el hanomator uo vorn.",
                "example_ja": "観測室で今日の算定盤がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-63",
        "batch": "Batch 16",
        "domain": "情報・星石の記憶器と実証メモリ",
        "title": "天測の記憶素と銀の記録核",
        "communicative_need": "星光を蓄える記憶素、事実を刻んだ実証記憶器、銀枠の記憶板を保管する。",
        "agent_a": {
            "name": "Yura",
            "role": "記憶素を分類する写字生"
        },
        "agent_b": {
            "name": "Sev",
            "role": "記録核を封じる灯守"
        },
        "turns": [
            {
                "speaker": "Yura",
                "nebulith": "Vymin el mi ia vyrsoril ul zydsoril uo kypal. Relen el tynisoril uo kypal.",
                "japanese": "私は収納箱で天測の記憶素と実証記憶器を保管する。収納箱で銀枠の記憶器がある。"
            },
            {
                "speaker": "Sev",
                "nebulith": "Vyrel el miin ia vyrsoril ul zydsoril. Falun el tynisoril al miin.",
                "japanese": "私たちは天測の記憶素と実証記憶器を確認する。私たちに銀枠の記憶器が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "vyrsoril",
                "pos": "名",
                "meaningJa": "天測の記憶素、星光の記録結晶、星辰メモリ",
                "meaningEn": "starlight memory crystal, astral storage core, celestial record unit",
                "morphemes": [
                    "vyr",
                    "soril"
                ],
                "etymology": "vyr(星・光点) + soril(星石記憶素・記憶器)",
                "category": "3. 数理・情報・計算機",
                "example_sentence": "Vymin el mi ia vyrsoril ul zydsoril uo kypal.",
                "example_ja": "私は収納箱で天測の記憶素と実証記憶器を保管する。"
            },
            {
                "nrs": "zydsoril",
                "pos": "名",
                "meaningJa": "実証記憶器、不変の証憑メモリ、事実保持座",
                "meaningEn": "verified memory core, factual storage unit, authentic record crystal",
                "morphemes": [
                    "zyd",
                    "soril"
                ],
                "etymology": "zyd(事実・実相) + soril(記憶素・記憶器)",
                "category": "3. 数理・情報・計算機",
                "example_sentence": "Vymin el mi ia vyrsoril ul zydsoril uo kypal.",
                "example_ja": "私は収納箱で天測の記憶素と実証記憶器を保管する。"
            },
            {
                "nrs": "tynisoril",
                "pos": "名",
                "meaningJa": "銀枠の記憶器、白銀の記憶盤、金属記憶素",
                "meaningEn": "silver-cased memory unit, silver storage plate, metallic core",
                "morphemes": [
                    "tyni",
                    "soril"
                ],
                "etymology": "tyni(銀色の・白銀の) + soril(記憶素・記憶器)",
                "category": "3. 数理・情報・計算機",
                "example_sentence": "Relen el tynisoril uo kypal.",
                "example_ja": "収納箱で銀枠の記憶器がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-64",
        "batch": "Batch 16",
        "domain": "数理・天体運行譜と今日の数理記述",
        "title": "星辰の記述譜と実証言辞",
        "communicative_need": "天体運行の数理譜、検証済みの論理記述文、今日の観測記述譜を読み合わせる。",
        "agent_a": {
            "name": "Yura",
            "role": "数理譜を清書する写字生"
        },
        "agent_b": {
            "name": "Sev",
            "role": "運行律を照合する灯守"
        },
        "turns": [
            {
                "speaker": "Yura",
                "nebulith": "Soran el mi ia vyrzevil ul zydzevil uo pamel. Relen el hanozevil uo pamel.",
                "japanese": "私は冊子の中で天体運行譜と実証記述文を記す。冊子の中で今日の観測譜がある。"
            },
            {
                "speaker": "Sev",
                "nebulith": "Vyrel el miin ia vyrzevil ul zydzevil. Falun el hanozevil al miin.",
                "japanese": "私たちは天体運行譜と実証記述文を照合する。私たちに今日の観測譜が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "vyrzevil",
                "pos": "名",
                "meaningJa": "天体運行譜、星辰の数理記述文、天文言辞",
                "meaningEn": "celestial equation scroll, astral notation, star-motion script",
                "morphemes": [
                    "vyr",
                    "zevil"
                ],
                "etymology": "vyr(星・天体) + zevil(星辰記述文・数理言辞)",
                "category": "3. 数理・情報・計算機",
                "example_sentence": "Soran el mi ia vyrzevil ul zydzevil uo pamel.",
                "example_ja": "私は冊子の中で天体運行譜と実証記述文を記す。"
            },
            {
                "nrs": "zydzevil",
                "pos": "名",
                "meaningJa": "実証記述文、検証済みの数理譜、事実命題文",
                "meaningEn": "verified logical statement, factual notation, proven formula",
                "morphemes": [
                    "zyd",
                    "zevil"
                ],
                "etymology": "zyd(事実・実相) + zevil(記述文・数理言辞)",
                "category": "3. 数理・情報・計算機",
                "example_sentence": "Soran el mi ia vyrzevil ul zydzevil uo pamel.",
                "example_ja": "私は冊子の中で天体運行譜と実証記述文を記す。"
            },
            {
                "nrs": "hanozevil",
                "pos": "名",
                "meaningJa": "今日の観測譜、本日の数理記述、当日の記録文",
                "meaningEn": "today's observation script, daily notation, current log formula",
                "morphemes": [
                    "hano",
                    "zevil"
                ],
                "etymology": "hano(今日・本日) + zevil(記述文・星符譜)",
                "category": "3. 数理・情報・計算機",
                "example_sentence": "Relen el hanozevil uo pamel.",
                "example_ja": "冊子の中で今日の観測譜がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-65",
        "batch": "Batch 17",
        "domain": "身体・星を映す瞳と澄んだまなざし",
        "title": "星見の瞳と潤んだ瞳",
        "communicative_need": "星を映す瞳、澄み切った白いまなざし、涙や露に潤む瞳を表現する。",
        "agent_a": {
            "name": "Neri",
            "role": "夜空を見上げる採集師"
        },
        "agent_b": {
            "name": "Yura",
            "role": "詩句を紡ぐ写字生"
        },
        "turns": [
            {
                "speaker": "Neri",
                "nebulith": "Vyrel el mi ia vyrvylan ul alinvylan uo govan. Relen el darvylan uo govan.",
                "japanese": "私は家の中で星を映す瞳と澄んだ瞳を見つめる。家の中で潤んだ瞳がある。"
            },
            {
                "speaker": "Yura",
                "nebulith": "Cynel el miin ia vyrvylan ul alinvylan. Falun el darvylan al miin.",
                "japanese": "私たちは星を映す瞳と澄んだ瞳を愛する。私たちに潤んだ瞳が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "vyrvylan",
                "pos": "名",
                "meaningJa": "星を映す瞳、星見の目、輝くまなざし",
                "meaningEn": "star-reflecting eyes, stargazer's gaze, luminous pupils",
                "morphemes": [
                    "vyr",
                    "vylan"
                ],
                "etymology": "vyr(星・光点) + vylan(目・瞳)",
                "category": "4. 人体・生理・医療",
                "example_sentence": "Vyrel el mi ia vyrvylan ul alinvylan uo govan.",
                "example_ja": "私は家の中で星を映す瞳と澄んだ瞳を見つめる。"
            },
            {
                "nrs": "alinvylan",
                "pos": "名",
                "meaningJa": "澄んだ瞳、純真なまなざし、曇りなき目",
                "meaningEn": "clear eyes, pure gaze, unclouded vision",
                "morphemes": [
                    "alin",
                    "vylan"
                ],
                "etymology": "alin(白い・純白の) + vylan(目・瞳)",
                "category": "4. 人体・生理・医療",
                "example_sentence": "Vyrel el mi ia vyrvylan ul alinvylan uo govan.",
                "example_ja": "私は家の中で星を映す瞳と澄んだ瞳を見つめる。"
            },
            {
                "nrs": "darvylan",
                "pos": "名",
                "meaningJa": "潤んだ瞳、露を宿す目、慈しみのまなざし",
                "meaningEn": "dewy eyes, moistened gaze, tender tearful eyes",
                "morphemes": [
                    "dar",
                    "vylan"
                ],
                "etymology": "dar(しずく・露) + vylan(目・瞳)",
                "category": "4. 人体・生理・医療",
                "example_sentence": "Relen el darvylan uo govan.",
                "example_ja": "家の中で潤んだ瞳がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-66",
        "batch": "Batch 17",
        "domain": "身体・せせらぎを聴く耳と夜の聴覚",
        "title": "水音に澄ます耳と森の聴覚",
        "communicative_need": "水音を聴き分ける耳、森の葉擦れを聴く耳、夜の静寂を聴く耳を語り合う。",
        "agent_a": {
            "name": "Toa",
            "role": "水音で浅瀬を知る舟守"
        },
        "agent_b": {
            "name": "Neri",
            "role": "森の音を聴く採集師"
        },
        "turns": [
            {
                "speaker": "Toa",
                "nebulith": "Vymin el mi ia darharel ul velharel uo daron. Relen el kymharel uo daron.",
                "japanese": "私は湖の上で水音を聴く耳と森を聴く耳を研ぎ澄ます。湖の上で夜を聴く耳がある。"
            },
            {
                "speaker": "Neri",
                "nebulith": "Vyrel el miin ia darharel ul velharel. Falun el kymharel al miin.",
                "japanese": "私たちは水音を聴く耳と森を聴く耳を確かめる。私たちに夜を聴く耳が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "darharel",
                "pos": "名",
                "meaningJa": "水音を聴く耳、せせらぎの聴覚、水辺の耳敏さ",
                "meaningEn": "ear attuned to water, stream-listening hearing, ripple sense",
                "morphemes": [
                    "dar",
                    "harel"
                ],
                "etymology": "dar(しずく・水) + harel(耳・聴覚)",
                "category": "4. 人体・生理・医療",
                "example_sentence": "Vymin el mi ia darharel ul velharel uo daron.",
                "example_ja": "私は湖の上で水音を聴く耳と森を聴く耳を研ぎ澄ます。"
            },
            {
                "nrs": "velharel",
                "pos": "名",
                "meaningJa": "森を聴く耳、葉擦れの聴覚、樹林の耳敏さ",
                "meaningEn": "forest-attuned ear, woodland hearing, sylvan listening",
                "morphemes": [
                    "vel",
                    "harel"
                ],
                "etymology": "vel(木・森林) + harel(耳・聴覚)",
                "category": "4. 人体・生理・医療",
                "example_sentence": "Vymin el mi ia darharel ul velharel uo daron.",
                "example_ja": "私は湖の上で水音を聴く耳と森を聴く耳を研ぎ澄ます。"
            },
            {
                "nrs": "kymharel",
                "pos": "名",
                "meaningJa": "夜を聴く耳、暗闇の聴覚、静夜の耳敏さ",
                "meaningEn": "night-keen ear, nocturnal hearing, darkness listening",
                "morphemes": [
                    "kym",
                    "harel"
                ],
                "etymology": "kym(夜・闇) + harel(耳・聴覚)",
                "category": "4. 人体・生理・医療",
                "example_sentence": "Relen el kymharel uo daron.",
                "example_ja": "湖の上で夜を聴く耳がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-67",
        "batch": "Batch 17",
        "domain": "医療・大地の精力と今日の気力",
        "title": "地に足ついたスタミナと潤いの精力",
        "communicative_need": "大地のように揺るぎない精力、水分による気力の充実、今日の活力を確かめる。",
        "agent_a": {
            "name": "Toa",
            "role": "櫂を漕ぐ舟守"
        },
        "agent_b": {
            "name": "Neri",
            "role": "滋養食を配る採集師"
        },
        "turns": [
            {
                "speaker": "Toa",
                "nebulith": "Vymin el mi ia talzyvor ul darzyvor uo laros. Relen el hanozyvor uo laros.",
                "japanese": "私は船の上で大地の精力と潤いの精力を保つ。船の上で今日の気力がある。"
            },
            {
                "speaker": "Neri",
                "nebulith": "Velrin el miin ia talzyvor ul darzyvor. Falun el hanozyvor al miin.",
                "japanese": "私たちは大地の精力と潤いの精力を実感する。私たちに今日の気力が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "talzyvor",
                "pos": "名",
                "meaningJa": "大地の精力、強靭な足腰のスタミナ、持久力",
                "meaningEn": "grounded stamina, earthen endurance, steadfast vigor",
                "morphemes": [
                    "tal",
                    "zyvor"
                ],
                "etymology": "tal(大地・足元) + zyvor(活力・スタミナ)",
                "category": "4. 人体・生理・医療",
                "example_sentence": "Vymin el mi ia talzyvor ul darzyvor uo laros.",
                "example_ja": "私は船の上で大地の精力と潤いの精力を保つ。"
            },
            {
                "nrs": "darzyvor",
                "pos": "名",
                "meaningJa": "潤いの精力、水分補給による気力、瑞々しい活力",
                "meaningEn": "hydrated stamina, refreshed vigor, fluid vitality",
                "morphemes": [
                    "dar",
                    "zyvor"
                ],
                "etymology": "dar(しずく・水) + zyvor(活力・スタミナ)",
                "category": "4. 人体・生理・医療",
                "example_sentence": "Vymin el mi ia talzyvor ul darzyvor uo laros.",
                "example_ja": "私は船の上で大地の精力と潤いの精力を保つ。"
            },
            {
                "nrs": "hanozyvor",
                "pos": "名",
                "meaningJa": "今日の気力、本日のスタミナ、当日の充実した精力",
                "meaningEn": "today's stamina, daily energy, current vigor",
                "morphemes": [
                    "hano",
                    "zyvor"
                ],
                "etymology": "hano(今日・本日) + zyvor(活力・精力)",
                "category": "4. 人体・生理・医療",
                "example_sentence": "Relen el hanozyvor uo laros.",
                "example_ja": "船の上で今日の気力がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-68",
        "batch": "Batch 17",
        "domain": "医療・森の養生と今日の健やかさ",
        "title": "草木の生命力と星夜の健康",
        "communicative_need": "森林浴による健やかさ、星夜に整う生命力、今日の良好な体調を喜ぶ。",
        "agent_a": {
            "name": "Neri",
            "role": "体調を尋ねる採集師"
        },
        "agent_b": {
            "name": "Sev",
            "role": "夜勤明けの灯守"
        },
        "turns": [
            {
                "speaker": "Neri",
                "nebulith": "Vymin el mi ia velzyvas ul vyrzyvas uo velar. Relen el hanozyvas uo velar.",
                "japanese": "私は庭の中で森の養生力と星夜の健やかさを守る。庭の中で今日の体調がある。"
            },
            {
                "speaker": "Sev",
                "nebulith": "Cynel el miin ia velzyvas ul vyrzyvas. Falun el hanozyvas al miin.",
                "japanese": "私たちは森の養生力と星夜の健やかさを喜ぶ。私たちに今日の体調が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "velzyvas",
                "pos": "名",
                "meaningJa": "森の養生力、草木の健やかさ、緑の生命力",
                "meaningEn": "woodland vitality, botanical health, forest wellness",
                "morphemes": [
                    "vel",
                    "zyvas"
                ],
                "etymology": "vel(木・森林) + zyvas(健康・生命力)",
                "category": "4. 人体・生理・医療",
                "example_sentence": "Vymin el mi ia velzyvas ul vyrzyvas uo velar.",
                "example_ja": "私は庭の中で森の養生力と星夜の健やかさを守る。"
            },
            {
                "nrs": "vyrzyvas",
                "pos": "名",
                "meaningJa": "星夜の健やかさ、澄んだ生命力、天測の気력",
                "meaningEn": "starlit vitality, clear nocturnal wellness, astral health",
                "morphemes": [
                    "vyr",
                    "zyvas"
                ],
                "etymology": "vyr(星・光点) + zyvas(健康・生命力)",
                "category": "4. 人体・生理・医療",
                "example_sentence": "Vymin el mi ia velzyvas ul vyrzyvas uo velar.",
                "example_ja": "私は庭の中で森の養生力と星夜の健やかさを守る。"
            },
            {
                "nrs": "hanozyvas",
                "pos": "名",
                "meaningJa": "今日の体調、本日の健やかさ、日々の健康",
                "meaningEn": "today's health, daily wellness, present good condition",
                "morphemes": [
                    "hano",
                    "zyvas"
                ],
                "etymology": "hano(今日・本日) + zyvas(健康・活力)",
                "category": "4. 人体・生理・医療",
                "example_sentence": "Relen el hanozyvas uo velar.",
                "example_ja": "庭の中で今日の体調がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-69",
        "batch": "Batch 18",
        "domain": "精神・星の夢と水面の幻視",
        "title": "星空のビジョンと静夜の夢",
        "communicative_need": "星々を巡る夢、深い夜の夢、水面に映るような淡い夢を語り合う。",
        "agent_a": {
            "name": "Yura",
            "role": "夢日記をつける写字生"
        },
        "agent_b": {
            "name": "Neri",
            "role": "朝の茶を淹れる採集師"
        },
        "turns": [
            {
                "speaker": "Yura",
                "nebulith": "Soran el mi ia vyrsonir ul kymsonir uo pamel. Relen el darsonir uo pamel.",
                "japanese": "私は手記ノートで星の夢と夜の夢を書き留める。手記ノートで水面の夢がある。"
            },
            {
                "speaker": "Neri",
                "nebulith": "Vyrel el miin ia vyrsonir ul kymsonir. Falun el darsonir al miin.",
                "japanese": "私たちは星の夢と夜の夢を思い返す。私たちに水面の夢が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "vyrsonir",
                "pos": "名",
                "meaningJa": "星の夢、天界のビジョン、星空の幻視",
                "meaningEn": "starry dream, astral vision, celestial reverie",
                "morphemes": [
                    "vyr",
                    "sonir"
                ],
                "etymology": "vyr(星・天体) + sonir(夢・ビジョン)",
                "category": "13. 精神・感情・内省",
                "example_sentence": "Soran el mi ia vyrsonir ul kymsonir uo pamel.",
                "example_ja": "私は手記ノートで星の夢と夜の夢を書き留める。"
            },
            {
                "nrs": "kymsonir",
                "pos": "名",
                "meaningJa": "夜の夢、深夜のまどろみ、宵闇の夢見",
                "meaningEn": "night dream, nocturnal slumber vision, midnight reverie",
                "morphemes": [
                    "kym",
                    "sonir"
                ],
                "etymology": "kym(夜・闇) + sonir(夢・幻視)",
                "category": "13. 精神・感情・内省",
                "example_sentence": "Soran el mi ia vyrsonir ul kymsonir uo pamel.",
                "example_ja": "私は手記ノートで星の夢と夜の夢を書き留める。"
            },
            {
                "nrs": "darsonir",
                "pos": "名",
                "meaningJa": "水面の夢、露のように淡い夢、水辺のまどろみ",
                "meaningEn": "rippling dream, dewy reverie, waterside vision",
                "morphemes": [
                    "dar",
                    "sonir"
                ],
                "etymology": "dar(しずく・水) + sonir(夢・幻視)",
                "category": "13. 精神・感情・内省",
                "example_sentence": "Relen el darsonir uo pamel.",
                "example_ja": "手記ノートで水面の夢がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-70",
        "batch": "Batch 18",
        "domain": "哲学・星辰の理と大地の摂理",
        "title": "普遍の真理と実証された道理",
        "communicative_need": "星々の運行の理、検証された事実の真理、大地の揺るぎない摂理を探究する。",
        "agent_a": {
            "name": "Sev",
            "role": "天球儀を回す灯守"
        },
        "agent_b": {
            "name": "Yura",
            "role": "哲学論考を記す写字生"
        },
        "turns": [
            {
                "speaker": "Sev",
                "nebulith": "Vyrel el mi ia vyrvyran ul zydvyran uo vorn. Relen el talvyran uo vorn.",
                "japanese": "私は書斎で星辰の理と実証の真理を探究する。書斎で大地の摂理がある。"
            },
            {
                "speaker": "Yura",
                "nebulith": "Soran el miin ia vyrvyran ul zydvyran. Falun el talvyran al miin.",
                "japanese": "私たちは星辰の理と実証の真理を記す。私たちに大地の摂理が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "vyrvyran",
                "pos": "名",
                "meaningJa": "星辰の理、天体運行の法則、宇宙の真理",
                "meaningEn": "cosmic law, astral truth, celestial logos",
                "morphemes": [
                    "vyr",
                    "vyran"
                ],
                "etymology": "vyr(星・天体) + vyran(真理・不変の理)",
                "category": "9. 学問・科学・技術",
                "example_sentence": "Vyrel el mi ia vyrvyran ul zydvyran uo vorn.",
                "example_ja": "私は書斎で星辰の理と実証の真理を探究する。"
            },
            {
                "nrs": "zydvyran",
                "pos": "名",
                "meaningJa": "実証の真理、事実に基づく道理、確証された理",
                "meaningEn": "verified truth, empirical principle, factual logos",
                "morphemes": [
                    "zyd",
                    "vyran"
                ],
                "etymology": "zyd(事実・実相) + vyran(真理・理)",
                "category": "9. 学問・科学・技術",
                "example_sentence": "Vyrel el mi ia vyrvyran ul zydvyran uo vorn.",
                "example_ja": "私は書斎で星辰の理と実証の真理を探究する。"
            },
            {
                "nrs": "talvyran",
                "pos": "名",
                "meaningJa": "大地の摂理、自然の法則、地の道理",
                "meaningEn": "law of the earth, natural order, terrestrial principle",
                "morphemes": [
                    "tal",
                    "vyran"
                ],
                "etymology": "tal(大地・自然) + vyran(真理・理)",
                "category": "9. 学問・科学・技術",
                "example_sentence": "Relen el talvyran uo vorn.",
                "example_ja": "書斎で大地の摂理がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-71",
        "batch": "Batch 18",
        "domain": "精神・星の閃きと今日の直感",
        "title": "澄んだ直観と湧き水のような着想",
        "communicative_need": "星光のような鋭い閃き、清水のように湧き出る着想、今日の直感を書き留める。",
        "agent_a": {
            "name": "Yura",
            "role": "着想をメモする写字生"
        },
        "agent_b": {
            "name": "Toa",
            "role": "風向きを読む舟守"
        },
        "turns": [
            {
                "speaker": "Yura",
                "nebulith": "Velrin el mi ia vyrfelyn ul darfelyn uo sylim. Relen el hanofelyn uo sylim.",
                "japanese": "私は心の中で星の閃きと湧き出る着想を感じる。心の中で今日の直感がある。"
            },
            {
                "speaker": "Toa",
                "nebulith": "Soran el miin ia vyrfelyn ul darfelyn. Falun el hanofelyn al miin.",
                "japanese": "私たちは星の閃きと湧き出る着想を書き留める。私たちに今日の直感が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "vyrfelyn",
                "pos": "名",
                "meaningJa": "星の閃き、天啓のような直観、鋭い洞察",
                "meaningEn": "starlight flash of insight, astral intuition, sudden inspiration",
                "morphemes": [
                    "vyr",
                    "felyn"
                ],
                "etymology": "vyr(星・光点) + felyn(直感・閃き)",
                "category": "13. 精神・感情・内省",
                "example_sentence": "Velrin el mi ia vyrfelyn ul darfelyn uo sylim.",
                "example_ja": "私は心の中で星の閃きと湧き出る着想を感じる。"
            },
            {
                "nrs": "darfelyn",
                "pos": "名",
                "meaningJa": "湧き出る着想、澄んだ直感、瑞々しい感性",
                "meaningEn": "welling inspiration, clear intuition, flowing insight",
                "morphemes": [
                    "dar",
                    "felyn"
                ],
                "etymology": "dar(しずく・湧水) + felyn(直感・閃き)",
                "category": "13. 精神・感情・内省",
                "example_sentence": "Velrin el mi ia vyrfelyn ul darfelyn uo sylim.",
                "example_ja": "私は心の中で星の閃きと湧き出る着想を感じる。"
            },
            {
                "nrs": "hanofelyn",
                "pos": "名",
                "meaningJa": "今日の直感、本日の着想、その場の閃き",
                "meaningEn": "today's intuition, daily inspiration, immediate hunch",
                "morphemes": [
                    "hano",
                    "felyn"
                ],
                "etymology": "hano(今日・現在) + felyn(直感・閃き)",
                "category": "13. 精神・感情・内省",
                "example_sentence": "Relen el hanofelyn uo sylim.",
                "example_ja": "心の中で今日の直感がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-72",
        "batch": "Batch 18",
        "domain": "精神・星見の心と純白の精神",
        "title": "澄み切った魂と水のように静かな心",
        "communicative_need": "星を仰ぐ高潔な心、水鏡のように静かな心、純白で曇りない精神を讃える。",
        "agent_a": {
            "name": "Sev",
            "role": "静かに瞑想する灯守"
        },
        "agent_b": {
            "name": "Neri",
            "role": "香を焚く採集師"
        },
        "turns": [
            {
                "speaker": "Sev",
                "nebulith": "Vymin el mi ia vyrsylim ul darsylim uo govan. Relen el alinsylim uo govan.",
                "japanese": "私は家の中で星見の心と水鏡の心を守る。家の中で純白の心がある。"
            },
            {
                "speaker": "Neri",
                "nebulith": "Cynel el miin ia vyrsylim ul darsylim. Falun el alinsylim al miin.",
                "japanese": "私たちは星見の心と水鏡の心を尊ぶ。私たちに純白の心が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "vyrsylim",
                "pos": "名",
                "meaningJa": "星見の心、天を仰ぐ魂、気高い精神",
                "meaningEn": "stargazer's spirit, astral soul, aspiring mind",
                "morphemes": [
                    "vyr",
                    "sylim"
                ],
                "etymology": "vyr(星・天体) + sylim(心・精神)",
                "category": "13. 精神・感情・内省",
                "example_sentence": "Vymin el mi ia vyrsylim ul darsylim uo govan.",
                "example_ja": "私は家の中で星見の心と水鏡の心を守る。"
            },
            {
                "nrs": "darsylim",
                "pos": "名",
                "meaningJa": "水鏡の心、静水のような精神、澄んだ魂",
                "meaningEn": "tranquil water-like mind, clear spirit, calm soul",
                "morphemes": [
                    "dar",
                    "sylim"
                ],
                "etymology": "dar(しずく・清水) + sylim(心・精神)",
                "category": "13. 精神・感情・内省",
                "example_sentence": "Vymin el mi ia vyrsylim ul darsylim uo govan.",
                "example_ja": "私は家の中で星見の心と水鏡の心を守る。"
            },
            {
                "nrs": "alinsylim",
                "pos": "名",
                "meaningJa": "純白の心、無垢な精神、曇りなき魂",
                "meaningEn": "pure heart, unblemished spirit, innocent soul",
                "morphemes": [
                    "alin",
                    "sylim"
                ],
                "etymology": "alin(白い・無垢な) + sylim(心・魂)",
                "category": "13. 精神・感情・内省",
                "example_sentence": "Relen el alinsylim uo govan.",
                "example_ja": "家の中で純白の心がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-73",
        "batch": "Batch 19",
        "domain": "社会・大地の住人と円環の共同体員",
        "title": "里の市民と天測の住人",
        "communicative_need": "大地に暮らす市民、天文台街区の住人、円環共同体の仲間を歓迎する。",
        "agent_a": {
            "name": "Toa",
            "role": "連絡船で人々を迎える舟守"
        },
        "agent_b": {
            "name": "Yura",
            "role": "住民台帳を記す写字生"
        },
        "turns": [
            {
                "speaker": "Toa",
                "nebulith": "Cynel el mi ia talpolor ul vyrpolor uo domom. Relen el klorpolor uo domom.",
                "japanese": "私は街の中で里の住人と星見街の住人を歓迎する。街の中で円環共同体の住人がある。"
            },
            {
                "speaker": "Yura",
                "nebulith": "Vymin el miin ia talpolor ul vyrpolor. Falun el klorpolor al miin.",
                "japanese": "私たちは里の住人と星見街の住人を守る。私たちに円環共同体の住人が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "talpolor",
                "pos": "名",
                "meaningJa": "里の住人、大地の市民、定住の民",
                "meaningEn": "land dweller, terrestrial citizen, local resident",
                "morphemes": [
                    "tal",
                    "polor"
                ],
                "etymology": "tal(大地・里) + polor(市民・住人)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Cynel el mi ia talpolor ul vyrpolor uo domom.",
                "example_ja": "私は街の中で里の住人と星見街の住人を歓迎する。"
            },
            {
                "nrs": "vyrpolor",
                "pos": "名",
                "meaningJa": "星見街の住人、天測都市の市民、観測所の民",
                "meaningEn": "observatory citizen, astral-quarter resident, star-city folk",
                "morphemes": [
                    "vyr",
                    "polor"
                ],
                "etymology": "vyr(星・天体) + polor(市民・住人)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Cynel el mi ia talpolor ul vyrpolor uo domom.",
                "example_ja": "私は街の中で里の住人と星見街の住人を歓迎する。"
            },
            {
                "nrs": "klorpolor",
                "pos": "名",
                "meaningJa": "円環共同体の住人、輪の仲間、同胞市民",
                "meaningEn": "circle fellow, communal citizen, member of the ring",
                "morphemes": [
                    "klor",
                    "polor"
                ],
                "etymology": "klor(円・環) + polor(市民・共同体員)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Relen el klorpolor uo domom.",
                "example_ja": "街の中で円環共同体の住人がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-74",
        "batch": "Batch 19",
        "domain": "社会・誠の盟友と車座の同志",
        "title": "揺るぎない親友と星見の伴走者",
        "communicative_need": "偽りなき真の親友、共に星を仰ぐ盟友、車座の仲間との絆を確かめる。",
        "agent_a": {
            "name": "Sev",
            "role": "長年の友と語る灯守"
        },
        "agent_b": {
            "name": "Toa",
            "role": "杯を交わす舟守"
        },
        "turns": [
            {
                "speaker": "Sev",
                "nebulith": "Cynel el mi ia zydcynor ul vyrcynor uo klorcalor. Relen el klorcynor uo klorcalor.",
                "japanese": "私は円卓評議で真の親友と星見の盟友を信頼する。円卓評議で車座の同志がある。"
            },
            {
                "speaker": "Toa",
                "nebulith": "Vymin el miin ia zydcynor ul vyrcynor. Falun el klorcynor al miin.",
                "japanese": "私たちは真の親友と星見の盟友を大切にする。私たちに車座の同志が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "zydcynor",
                "pos": "名",
                "meaningJa": "真の親友、誠の盟友、揺るぎない相棒",
                "meaningEn": "true confidant, steadfast ally, faithful companion",
                "morphemes": [
                    "zyd",
                    "cynor"
                ],
                "etymology": "zyd(事実・誠) + cynor(親友・盟友)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Cynel el mi ia zydcynor ul vyrcynor uo klorcalor.",
                "example_ja": "私は円卓評議で真の親友と星見の盟友を信頼する。"
            },
            {
                "nrs": "vyrcynor",
                "pos": "名",
                "meaningJa": "星見の盟友、天測の伴走者、志を同じくする友",
                "meaningEn": "stargazing companion, astral comrade, fellow seeker",
                "morphemes": [
                    "vyr",
                    "cynor"
                ],
                "etymology": "vyr(星・天体) + cynor(親友・伴走者)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Cynel el mi ia zydcynor ul vyrcynor uo klorcalor.",
                "example_ja": "私は円卓評議で真の親友と星見の盟友を信頼する。"
            },
            {
                "nrs": "klorcynor",
                "pos": "名",
                "meaningJa": "車座の同志、円卓の盟友、共同体の親友",
                "meaningEn": "circle comrade, roundtable friend, fellowship ally",
                "morphemes": [
                    "klor",
                    "cynor"
                ],
                "etymology": "klor(円・環) + cynor(親友・盟友)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Relen el klorcynor uo klorcalor.",
                "example_ja": "円卓評議で車座の同志がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-75",
        "batch": "Batch 19",
        "domain": "社会・実証の法と円卓の規約",
        "title": "公正な掟と天体運行の規律",
        "communicative_need": "事実に基づく公正な法、星々の運行にならう規律、円卓評議の規約を確認する。",
        "agent_a": {
            "name": "Yura",
            "role": "法典を紐解く写字生"
        },
        "agent_b": {
            "name": "Sev",
            "role": "評議の秩序を守る灯守"
        },
        "turns": [
            {
                "speaker": "Yura",
                "nebulith": "Vymin el mi ia zydtaros ul vyrtaros uo pamel. Relen el klortaros uo pamel.",
                "japanese": "私は法典冊子で公正な法と軌道規律を遵守する。法典冊子で円卓の規約がある。"
            },
            {
                "speaker": "Sev",
                "nebulith": "Soran el miin ia zydtaros ul vyrtaros. Falun el klortaros al miin.",
                "japanese": "私たちは公正な法と軌道規律を記録する。私たちに円卓の規約が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "zydtaros",
                "pos": "名",
                "meaningJa": "公正な法、事実に基づく掟、実証法典",
                "meaningEn": "empirical law, just statute, verified code",
                "morphemes": [
                    "zyd",
                    "taros"
                ],
                "etymology": "zyd(事実・公正) + taros(法・掟)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Vymin el mi ia zydtaros ul vyrtaros uo pamel.",
                "example_ja": "私は法典冊子で公正な法と軌道規律を遵守する。"
            },
            {
                "nrs": "vyrtaros",
                "pos": "名",
                "meaningJa": "軌道規律、星辰の運行法、天文の規範",
                "meaningEn": "orbital regulation, celestial statute, astral canon law",
                "morphemes": [
                    "vyr",
                    "taros"
                ],
                "etymology": "vyr(星・天体) + taros(法・軌道規則)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Vymin el mi ia zydtaros ul vyrtaros uo pamel.",
                "example_ja": "私は法典冊子で公正な法と軌道規律を遵守する。"
            },
            {
                "nrs": "klortaros",
                "pos": "名",
                "meaningJa": "円卓の規約、共同体の掟、合議の法",
                "meaningEn": "council charter, communal bylaw, rule of the circle",
                "morphemes": [
                    "klor",
                    "taros"
                ],
                "etymology": "klor(円・共同体) + taros(法・掟)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Relen el klortaros uo pamel.",
                "example_ja": "法典冊子で円卓の規約がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-76",
        "batch": "Batch 19",
        "domain": "経済・陸の青空市と水上の定期市",
        "title": "大地の市場と円形広場の市",
        "communicative_need": "農産物が集まる陸の市場、舟が集まる水上市場、円形広場の定期市を巡る。",
        "agent_a": {
            "name": "Neri",
            "role": "薬草を出品する採集師"
        },
        "agent_b": {
            "name": "Toa",
            "role": "舟荷を並べる舟守"
        },
        "turns": [
            {
                "speaker": "Neri",
                "nebulith": "Vyrel el mi ia talrenar ul darrenar uo domom. Relen el klorrenar uo domom.",
                "japanese": "私は街の中で陸の市場と水上市場を見て回る。街の中で円形広場の市がある。"
            },
            {
                "speaker": "Toa",
                "nebulith": "Cynel el miin ia talrenar ul darrenar. Falun el klorrenar al miin.",
                "japanese": "私たちは陸の市場と水上市場で賑わう。私たちに円形広場の市が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "talrenar",
                "pos": "名",
                "meaningJa": "陸の市場、大地の青空市、農産物取引所",
                "meaningEn": "overland market, country bazaar, produce marketplace",
                "morphemes": [
                    "tal",
                    "renar"
                ],
                "etymology": "tal(大地・陸) + renar(市場・取引所)",
                "category": "10. 経済・交易・資源",
                "example_sentence": "Vyrel el mi ia talrenar ul darrenar uo domom.",
                "example_ja": "私は街の中で陸の市場と水上市場を見て回る。"
            },
            {
                "nrs": "darrenar",
                "pos": "名",
                "meaningJa": "水上市場、船着き場の市、運河の取引所",
                "meaningEn": "floating market, waterside bazaar, canal exchange",
                "morphemes": [
                    "dar",
                    "renar"
                ],
                "etymology": "dar(しずく・水路) + renar(市場・店)",
                "category": "10. 経済・交易・資源",
                "example_sentence": "Vyrel el mi ia talrenar ul darrenar uo domom.",
                "example_ja": "私は街の中で陸の市場と水上市場を見て回る。"
            },
            {
                "nrs": "klorrenar",
                "pos": "名",
                "meaningJa": "円形広場の市、環状市場、車座の取引所",
                "meaningEn": "rotunda market, circular plaza bazaar, ring exchange",
                "morphemes": [
                    "klor",
                    "renar"
                ],
                "etymology": "klor(円・環) + renar(市場・取引所)",
                "category": "10. 経済・交易・資源",
                "example_sentence": "Relen el klorrenar uo domom.",
                "example_ja": "街の中で円形広場の市がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-77",
        "batch": "Batch 20",
        "domain": "経済・銀貨と白磁貨・地金通貨",
        "title": "白銀の貨幣と取引の決済",
        "communicative_need": "銀色の硬貨、白い証票通貨、大地の鉱物貨幣を数えて帳面に記す。",
        "agent_a": {
            "name": "Yura",
            "role": "出納帳をつける写字生"
        },
        "agent_b": {
            "name": "Toa",
            "role": "運賃を受け取る舟守"
        },
        "turns": [
            {
                "speaker": "Yura",
                "nebulith": "Vyrel el mi ia tynirenis ul alinrenis uo renar. Relen el talrenis uo renar.",
                "japanese": "私は市場で銀貨と白磁貨を数える。市場で鉱石貨幣がある。"
            },
            {
                "speaker": "Toa",
                "nebulith": "Soran el miin ia tynirenis ul alinrenis. Falun el talrenis al miin.",
                "japanese": "私たちは銀貨と白磁貨を帳面に記す。私たちに鉱石貨幣が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "tynirenis",
                "pos": "名",
                "meaningJa": "銀貨、白銀の硬貨、銀の通貨",
                "meaningEn": "silver coin, argent currency, silver piece",
                "morphemes": [
                    "tyni",
                    "renis"
                ],
                "etymology": "tyni(銀色の・白銀の) + renis(貨幣・通貨)",
                "category": "10. 経済・交易・資源",
                "example_sentence": "Vyrel el mi ia tynirenis ul alinrenis uo renar.",
                "example_ja": "私は市場で銀貨と白磁貨を数える。"
            },
            {
                "nrs": "alinrenis",
                "pos": "名",
                "meaningJa": "白磁貨、純白の証票貨、白い通貨トークン",
                "meaningEn": "white porcelain token, ivory coin, bright trade chit",
                "morphemes": [
                    "alin",
                    "renis"
                ],
                "etymology": "alin(白い・純白の) + renis(貨幣・通貨)",
                "category": "10. 経済・交易・資源",
                "example_sentence": "Vyrel el mi ia tynirenis ul alinrenis uo renar.",
                "example_ja": "私は市場で銀貨と白磁貨を数える。"
            },
            {
                "nrs": "talrenis",
                "pos": "名",
                "meaningJa": "鉱石貨幣、地金コイン、大地の通貨",
                "meaningEn": "mineral coin, base-metal currency, earthen trade token",
                "morphemes": [
                    "tal",
                    "renis"
                ],
                "etymology": "tal(大地・鉱石) + renis(貨幣・お金)",
                "category": "10. 経済・交易・資源",
                "example_sentence": "Relen el talrenis uo renar.",
                "example_ja": "市場で鉱石貨幣がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-78",
        "batch": "Batch 20",
        "domain": "経済・土地の資産と森林資源・共有財産",
        "title": "大地の財産と共同体の共有富",
        "communicative_need": "土地と農地の資産、森林の資源資産、共同体全体の共有財産を管理する。",
        "agent_a": {
            "name": "Sev",
            "role": "備蓄を管理する灯守"
        },
        "agent_b": {
            "name": "Neri",
            "role": "森林資源を調査する採集師"
        },
        "turns": [
            {
                "speaker": "Sev",
                "nebulith": "Vymin el mi ia talrenon ul velrenon uo domom. Relen el klorrenon uo domom.",
                "japanese": "私は街の中で土地資産と森林資産を保全する。街の中で共有財産がある。"
            },
            {
                "speaker": "Neri",
                "nebulith": "Soran el miin ia talrenon ul velrenon. Falun el klorrenon al miin.",
                "japanese": "私たちは土地資産と森林資産を記録する。私たちに共有財産が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "talrenon",
                "pos": "名",
                "meaningJa": "土地資産、大地の財産、不動産の富",
                "meaningEn": "landed estate, terrestrial asset, soil wealth",
                "morphemes": [
                    "tal",
                    "renon"
                ],
                "etymology": "tal(大地・土地) + renon(財産・資産)",
                "category": "10. 経済・交易・資源",
                "example_sentence": "Vymin el mi ia talrenon ul velrenon uo domom.",
                "example_ja": "私は街の中で土地資産と森林資産を保全する。"
            },
            {
                "nrs": "velrenon",
                "pos": "名",
                "meaningJa": "森林資産、木材資源の富、樹林の財産",
                "meaningEn": "forestry asset, timber wealth, woodland resource",
                "morphemes": [
                    "vel",
                    "renon"
                ],
                "etymology": "vel(木・森林) + renon(財産・資産)",
                "category": "10. 経済・交易・資源",
                "example_sentence": "Vymin el mi ia talrenon ul velrenon uo domom.",
                "example_ja": "私は街の中で土地資産と森林資産を保全する。"
            },
            {
                "nrs": "klorrenon",
                "pos": "名",
                "meaningJa": "共有財産、共同体の資産、輪の共通富",
                "meaningEn": "commonwealth, communal asset, shared treasury",
                "morphemes": [
                    "klor",
                    "renon"
                ],
                "etymology": "klor(円・共同体) + renon(財産・資産)",
                "category": "10. 経済・交易・資源",
                "example_sentence": "Relen el klorrenon uo domom.",
                "example_ja": "街の中で共有財産がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-79",
        "batch": "Batch 20",
        "domain": "都市・陸の城塞街と水辺の運河都市",
        "title": "大地の街区と環状の都",
        "communicative_need": "大地に広がる街、水路が巡る水辺の都市、環状に築かれた円形都市を描写する。",
        "agent_a": {
            "name": "Toa",
            "role": "水路から街を見る舟守"
        },
        "agent_b": {
            "name": "Yura",
            "role": "都市図を描く写字生"
        },
        "turns": [
            {
                "speaker": "Toa",
                "nebulith": "Vyrel el mi ia taldomom ul dardomom uo celen. Relen el klordomom uo celen.",
                "japanese": "私は空の下で内陸の街と水辺の都市を見渡す。空の下で環状都市がある。"
            },
            {
                "speaker": "Yura",
                "nebulith": "Cynel el miin ia taldomom ul dardomom. Falun el klordomom al miin.",
                "japanese": "私たちは内陸の街と水辺の都市を誇りに思う。私たちに環状都市が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "taldomom",
                "pos": "名",
                "meaningJa": "内陸の街、大地の都市、石造りの街区",
                "meaningEn": "inland city, earthen metropolis, stone-built town",
                "morphemes": [
                    "tal",
                    "domom"
                ],
                "etymology": "tal(大地・陸) + domom(都市・街)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Vyrel el mi ia taldomom ul dardomom uo celen.",
                "example_ja": "私は空の下で内陸の街と水辺の都市を見渡す。"
            },
            {
                "nrs": "dardomom",
                "pos": "名",
                "meaningJa": "水辺の都市、運河の街、湖畔の街区",
                "meaningEn": "canal city, waterside town, aquatic district",
                "morphemes": [
                    "dar",
                    "domom"
                ],
                "etymology": "dar(しずく・水路) + domom(都市・街)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Vyrel el mi ia taldomom ul dardomom uo celen.",
                "example_ja": "私は空の下で内陸の街と水辺の都市を見渡す。"
            },
            {
                "nrs": "klordomom",
                "pos": "名",
                "meaningJa": "環状都市、円形の街区、灰環の都",
                "meaningEn": "ring city, circular district, concentric town",
                "morphemes": [
                    "klor",
                    "domom"
                ],
                "etymology": "klor(円・環) + domom(都市・街区)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Relen el klordomom uo celen.",
                "example_ja": "空の下で環状都市がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-80",
        "batch": "Batch 20",
        "domain": "社会・真の講和と星下の盟約・円卓の安寧",
        "title": "恒久の講和と灰環の平和条約",
        "communicative_need": "偽りなき講和、星々の下で結ぶ平和、円卓の恒久安寧を宣言して全80話を結ぶ。",
        "agent_a": {
            "name": "Yura",
            "role": "講和証書を朗読する写字生"
        },
        "agent_b": {
            "name": "Sev",
            "role": "平和の灯を高く掲げる灯守"
        },
        "turns": [
            {
                "speaker": "Yura",
                "nebulith": "Vymin el mi ia zydsirar ul vyrsirar uo klorcalor. Relen el klorsirar uo klorcalor.",
                "japanese": "私は円卓評議で真の講和と星下の講和を守り抜く。円卓評議で円卓の講和がある。"
            },
            {
                "speaker": "Sev",
                "nebulith": "Soran el miin ia zydsirar ul vyrsirar. Falun el klorsirar al miin.",
                "japanese": "私たちは真の講和と星下の講和を永遠に刻む。私たちに円卓の講和が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "zydsirar",
                "pos": "名",
                "meaningJa": "真の講和、誠実な平和条約、揺るぎない和睦",
                "meaningEn": "authentic peace treaty, genuine accord, lasting reconciliation",
                "morphemes": [
                    "zyd",
                    "sirar"
                ],
                "etymology": "zyd(事実・誠) + sirar(安寧・講和条約)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Vymin el mi ia zydsirar ul vyrsirar uo klorcalor.",
                "example_ja": "私は円卓評議で真の講和と星下の講和を守り抜く。"
            },
            {
                "nrs": "vyrsirar",
                "pos": "名",
                "meaningJa": "星下の講和、星辰の盟約、星空の和睦",
                "meaningEn": "starlit accord, celestial peace, astral covenant of calm",
                "morphemes": [
                    "vyr",
                    "sirar"
                ],
                "etymology": "vyr(星・天) + sirar(安寧・平和)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Vymin el mi ia zydsirar ul vyrsirar uo klorcalor.",
                "example_ja": "私は円卓評議で真の講和と星下の講和を守り抜く。"
            },
            {
                "nrs": "klorsirar",
                "pos": "名",
                "meaningJa": "円卓の講和、共同体の和睦、環の恒久平和",
                "meaningEn": "roundtable peace, communal accord, concord of the circle",
                "morphemes": [
                    "klor",
                    "sirar"
                ],
                "etymology": "klor(円・環) + sirar(安寧・講和条約)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Relen el klorsirar uo klorcalor.",
                "example_ja": "円卓評議で円卓の講和がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-81",
        "batch": "Batch 21",
        "domain": "天文・極光と彩雲・天頂の輝き",
        "title": "北天の極光と白雲の天蓋",
        "communicative_need": "北天に揺れる星色の極光、白く輝く高層の雲、澄み渡る天頂の輝きを観測記録に残す。",
        "agent_a": {
            "name": "Yura",
            "role": "観測日誌を記す写字生"
        },
        "agent_b": {
            "name": "Sev",
            "role": "天頂鏡を合わせる灯守"
        },
        "turns": [
            {
                "speaker": "Yura",
                "nebulith": "Vyrel el mi ia vyrcelar ul alincelis uo celen. Relen el vyrnovar uo celen.",
                "japanese": "私は空の下で星彩の極光と白銀の彩雲を見渡す。空の下で星辰の天頂がある。"
            },
            {
                "speaker": "Sev",
                "nebulith": "Soran el miin ia vyrcelar ul alincelis. Falun el vyrnovar al miin.",
                "japanese": "私たちは星彩の極光と白銀の彩雲を記録する。私たちに星辰の天頂が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "vyrcelar",
                "pos": "名",
                "meaningJa": "星彩の極光、星明かりのオーロラ、天の極光帯",
                "meaningEn": "starlit aurora, astral polar light, shimmering sky curtain",
                "morphemes": [
                    "vyr",
                    "celar"
                ],
                "etymology": "vyr(星) + celar(極光)",
                "category": "1. 天文・宇宙・時空",
                "example_sentence": "Vyrel el mi ia vyrcelar ul alincelis uo celen.",
                "example_ja": "私は空の下で星彩の極光と白銀の彩雲を見渡す。"
            },
            {
                "nrs": "alincelis",
                "pos": "名",
                "meaningJa": "白銀の彩雲、純白の高層雲、白雲の帯",
                "meaningEn": "pure white cloud, silvery cirrus, luminous cloudbank",
                "morphemes": [
                    "alin",
                    "celis"
                ],
                "etymology": "alin(白い) + celis(雲)",
                "category": "1. 天文・宇宙・時空",
                "example_sentence": "Vyrel el mi ia vyrcelar ul alincelis uo celen.",
                "example_ja": "私は空の下で星彩の極光と白銀の彩雲を見渡す。"
            },
            {
                "nrs": "vyrnovar",
                "pos": "名",
                "meaningJa": "星辰の天頂、星が集う天頂点、天頂の星座",
                "meaningEn": "astral zenith, starlit celestial crown, zenithal star point",
                "morphemes": [
                    "vyr",
                    "novar"
                ],
                "etymology": "vyr(星) + novar(天頂)",
                "category": "1. 天文・宇宙・時空",
                "example_sentence": "Relen el vyrnovar uo celen.",
                "example_ja": "空の下で星辰の天頂がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-82",
        "batch": "Batch 21",
        "domain": "天文・日食の影と天底の静寂",
        "title": "金環の食と天底の星座",
        "communicative_need": "太陽と月が重なる環食、大地の下に巡る天底、海に映る星座の姿を語り合う。",
        "agent_a": {
            "name": "Sev",
            "role": "日食盤を読む灯守"
        },
        "agent_b": {
            "name": "Toa",
            "role": "水面の星影を見る舟守"
        },
        "turns": [
            {
                "speaker": "Sev",
                "nebulith": "Vyrel el mi ia klorkymos ul taltulos uo daron. Relen el darvyrom uo daron.",
                "japanese": "私は湖の上で金環食と大地の天底を観測する。湖の上で水鏡の星座がある。"
            },
            {
                "speaker": "Toa",
                "nebulith": "Cynel el miin ia klorkymos ul taltulos. Falun el darvyrom al miin.",
                "japanese": "私たちは金環食と大地の天底を敬愛する。私たちに水鏡の星座が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "klorkymos",
                "pos": "名",
                "meaningJa": "金環食、環状の日食、円環の食影",
                "meaningEn": "annular eclipse, ring eclipse, coronal shadow ring",
                "morphemes": [
                    "klor",
                    "kymos"
                ],
                "etymology": "klor(円) + kymos(日食)",
                "category": "1. 天文・宇宙・時空",
                "example_sentence": "Vyrel el mi ia klorkymos ul taltulos uo daron.",
                "example_ja": "私は湖の上で金環食と大地の天底を観測する。"
            },
            {
                "nrs": "taltulos",
                "pos": "名",
                "meaningJa": "大地の天底、地底側の天球点、深き天底",
                "meaningEn": "terrestrial nadir, subterranean sky pole, deep nadir point",
                "morphemes": [
                    "tal",
                    "tulos"
                ],
                "etymology": "tal(大地) + tulos(天底)",
                "category": "1. 天文・宇宙・時空",
                "example_sentence": "Vyrel el mi ia klorkymos ul taltulos uo daron.",
                "example_ja": "私は湖の上で金環食と大地の天底を観測する。"
            },
            {
                "nrs": "darvyrom",
                "pos": "名",
                "meaningJa": "水鏡の星座、水面に映る星座、湖面の星宿",
                "meaningEn": "water-reflected constellation, mirrored star pattern, aquatic asterism",
                "morphemes": [
                    "dar",
                    "vyrom"
                ],
                "etymology": "dar(しずく) + vyrom(星座)",
                "category": "1. 天文・宇宙・時空",
                "example_sentence": "Relen el darvyrom uo daron.",
                "example_ja": "湖の上で水鏡の星座がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-83",
        "batch": "Batch 21",
        "domain": "天文・惑星の公転と天体脈動",
        "title": "水の惑星と銀の公転周期",
        "communicative_need": "水を湛える惑星、円環を描く公転周期、星々の規則正しい脈動を数理盤で確かめる。",
        "agent_a": {
            "name": "Yura",
            "role": "公転表を引く写字生"
        },
        "agent_b": {
            "name": "Neri",
            "role": "季節の移ろいを読む採集師"
        },
        "turns": [
            {
                "speaker": "Yura",
                "nebulith": "Vyrel el mi ia dardoran ul klorvoris uo livar. Relen el vyrvalur uo livar.",
                "japanese": "私は星辰書庫で水の惑星と円環公転を照合する。星辰書庫で恒星脈動がある。"
            },
            {
                "speaker": "Neri",
                "nebulith": "Soran el miin ia dardoran ul klorvoris. Falun el vyrvalur al miin.",
                "japanese": "私たちは水の惑星と円環公転を書き留める。私たちに恒星脈動が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "dardoran",
                "pos": "名",
                "meaningJa": "水の惑星、海洋を湛える遊星、蒼き水惑星",
                "meaningEn": "water planet, oceanic world, aquatic celestial body",
                "morphemes": [
                    "dar",
                    "doran"
                ],
                "etymology": "dar(しずく) + doran(惑星)",
                "category": "1. 天文・宇宙・時空",
                "example_sentence": "Vyrel el mi ia dardoran ul klorvoris uo livar.",
                "example_ja": "私は星辰書庫で水の惑星と円環公転を照合する。"
            },
            {
                "nrs": "klorvoris",
                "pos": "名",
                "meaningJa": "円環公転、正円の公転周期、環状の巡り",
                "meaningEn": "circular revolution, ring orbital cycle, concentric planetary period",
                "morphemes": [
                    "klor",
                    "voris"
                ],
                "etymology": "klor(円) + voris(公転)",
                "category": "1. 天文・宇宙・時空",
                "example_sentence": "Vyrel el mi ia dardoran ul klorvoris uo livar.",
                "example_ja": "私は星辰書庫で水の惑星と円環公転を照合する。"
            },
            {
                "nrs": "vyrvalur",
                "pos": "名",
                "meaningJa": "恒星脈動、星の鼓動周期、天体の明滅律",
                "meaningEn": "stellar pulsation, starlight heartbeat, astral rhythmic oscillation",
                "morphemes": [
                    "vyr",
                    "valur"
                ],
                "etymology": "vyr(星) + valur(天体脈動)",
                "category": "1. 天文・宇宙・時空",
                "example_sentence": "Relen el vyrvalur uo livar.",
                "example_ja": "星辰書庫で恒星脈動がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-84",
        "batch": "Batch 21",
        "domain": "天文・潮汐力と軌道の引力",
        "title": "海の潮汐と月軌道の調べ",
        "communicative_need": "水を動かす潮汐の力、大地が保つ安定した引力、銀色に輝く軌道半径を計算する。",
        "agent_a": {
            "name": "Toa",
            "role": "潮位を測る舟守"
        },
        "agent_b": {
            "name": "Sev",
            "role": "軌道儀を回す灯守"
        },
        "turns": [
            {
                "speaker": "Toa",
                "nebulith": "Vymin el mi ia dartyril ul taltyral uo larar. Relen el tyniradin uo larar.",
                "japanese": "私は港の観測所で水辺の潮汐力と大地の引力を計測する。港の観測所で白銀の軌道半径がある。"
            },
            {
                "speaker": "Sev",
                "nebulith": "Soran el miin ia dartyril ul taltyral. Falun el tyniradin al miin.",
                "japanese": "私たちは水辺の潮汐力と大地の引力を記録する。私たちに白銀の軌道半径が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "dartyril",
                "pos": "名",
                "meaningJa": "水辺の潮汐力、海水を引く潮汐、満ち引きの力",
                "meaningEn": "aquatic tidal force, water-pulling tide, coastal tidal attraction",
                "morphemes": [
                    "dar",
                    "tyril"
                ],
                "etymology": "dar(しずく) + tyril(潮汐力)",
                "category": "1. 天文・宇宙・時空",
                "example_sentence": "Vymin el mi ia dartyril ul taltyral uo larar.",
                "example_ja": "私は港の観測所で水辺の潮汐力と大地の引力を計測する。"
            },
            {
                "nrs": "taltyral",
                "pos": "名",
                "meaningJa": "大地の引力、地表の重力場、盤石の引力",
                "meaningEn": "terrestrial gravity, earthbound attraction, planetary gravitational pull",
                "morphemes": [
                    "tal",
                    "tyral"
                ],
                "etymology": "tal(大地) + tyral(引力)",
                "category": "1. 天文・宇宙・時空",
                "example_sentence": "Vymin el mi ia dartyril ul taltyral uo larar.",
                "example_ja": "私は港の観測所で水辺の潮汐力と大地の引力を計測する。"
            },
            {
                "nrs": "tyniradin",
                "pos": "名",
                "meaningJa": "白銀の軌道半径、外周の軌道距離、銀環の半径",
                "meaningEn": "silver orbital radius, outer ring radius, argent orbital distance",
                "morphemes": [
                    "tyni",
                    "radin"
                ],
                "etymology": "tyni(銀色の) + radin(軌道半径)",
                "category": "1. 天文・宇宙・時空",
                "example_sentence": "Relen el tyniradin uo larar.",
                "example_ja": "港の観測所で白銀の軌道半径がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-85",
        "batch": "Batch 22",
        "domain": "航海・大海の波と季節風の便り",
        "title": "星映す大海と森を渡る季節風",
        "communicative_need": "星明かりを映す夜の海、森を揺らす季節風、地平線に浮かぶ暁の光を舟上から見守る。",
        "agent_a": {
            "name": "Toa",
            "role": "舵を握る舟守"
        },
        "agent_b": {
            "name": "Neri",
            "role": "風向きを読む採集師"
        },
        "turns": [
            {
                "speaker": "Toa",
                "nebulith": "Vyrel el mi ia vyrzylar ul velwylor uo daron. Relen el vyrzemin uo daron.",
                "japanese": "私は水路の上で星映す大海と樹海の季節風を見渡す。水路の上で星際の地平線がある。"
            },
            {
                "speaker": "Neri",
                "nebulith": "Cynel el miin ia vyrzylar ul velwylor. Falun el vyrzemin al miin.",
                "japanese": "私たちは星映す大海と樹海の季節風を愛する。私たちに星際の地平線が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "vyrzylar",
                "pos": "名",
                "meaningJa": "星映す大海、星明かりの海原、夜の蒼海",
                "meaningEn": "starlit sea, astral ocean expanse, star-mirroring waters",
                "morphemes": [
                    "vyr",
                    "zylar"
                ],
                "etymology": "vyr(星) + zylar(海)",
                "category": "16. 日常・自然・気象",
                "example_sentence": "Vyrel el mi ia vyrzylar ul velwylor uo daron.",
                "example_ja": "私は水路の上で星映す大海と樹海の季節風を見渡す。"
            },
            {
                "nrs": "velwylor",
                "pos": "名",
                "meaningJa": "樹海の季節風、森を渡る順風、緑の季節風",
                "meaningEn": "woodland monsoon, forest trade wind, sylvan seasonal breeze",
                "morphemes": [
                    "vel",
                    "wylor"
                ],
                "etymology": "vel(木) + wylor(季節風)",
                "category": "16. 日常・自然・気象",
                "example_sentence": "Vyrel el mi ia vyrzylar ul velwylor uo daron.",
                "example_ja": "私は水路の上で星映す大海と樹海の季節風を見渡す。"
            },
            {
                "nrs": "vyrzemin",
                "pos": "名",
                "meaningJa": "星際の地平線、星が昇る水平線、天と地の稜線",
                "meaningEn": "starlit horizon, astral skyline, celestial horizon rim",
                "morphemes": [
                    "vyr",
                    "zemin"
                ],
                "etymology": "vyr(星) + zemin(地平線)",
                "category": "16. 日常・自然・気象",
                "example_sentence": "Relen el vyrzemin uo daron.",
                "example_ja": "水路の上で星際の地平線がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-86",
        "batch": "Batch 22",
        "domain": "自然・氷結晶と鍾乳の洞窟",
        "title": "白銀の氷柱と水滴の洞窟",
        "communicative_need": "純白の氷の結晶、しずくが響く石灰の洞窟、緑の草原が広がる平原を探索する。",
        "agent_a": {
            "name": "Neri",
            "role": "鉱泉を探す採集師"
        },
        "agent_b": {
            "name": "Toa",
            "role": "地下川を案内する舟守"
        },
        "turns": [
            {
                "speaker": "Neri",
                "nebulith": "Vyrel el mi ia alinkyras ul darvuron uo talom. Relen el dartalom uo talom.",
                "japanese": "私は平原のほとりで純白の氷晶と水滴の鍾乳洞を観察する。平原のほとりで潤いの平原がある。"
            },
            {
                "speaker": "Toa",
                "nebulith": "Vymin el miin ia alinkyras ul darvuron. Falun el dartalom al miin.",
                "japanese": "私たちは純白の氷晶と水滴の鍾乳洞を保全する。私たちに潤いの平原が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "alinkyras",
                "pos": "名",
                "meaningJa": "純白の氷晶、白銀の氷塊、澄んだ白氷",
                "meaningEn": "pure white ice, clear frost crystal, alabaster glacier ice",
                "morphemes": [
                    "alin",
                    "kyras"
                ],
                "etymology": "alin(白い) + kyras(氷)",
                "category": "16. 日常・自然・気象",
                "example_sentence": "Vyrel el mi ia alinkyras ul darvuron uo talom.",
                "example_ja": "私は平原のほとりで純白の氷晶と水滴の鍾乳洞を観察する。"
            },
            {
                "nrs": "darvuron",
                "pos": "名",
                "meaningJa": "水滴の鍾乳洞、湧き水の洞窟、しずくの石窟",
                "meaningEn": "water cavern, dripping limestone grotto, underground spring cave",
                "morphemes": [
                    "dar",
                    "vuron"
                ],
                "etymology": "dar(しずく) + vuron(洞窟)",
                "category": "16. 日常・自然・気象",
                "example_sentence": "Vyrel el mi ia alinkyras ul darvuron uo talom.",
                "example_ja": "私は平原のほとりで純白の氷晶と水滴の鍾乳洞を観察する。"
            },
            {
                "nrs": "dartalom",
                "pos": "名",
                "meaningJa": "潤いの平原、水脈豊かな沃野、水辺の草原",
                "meaningEn": "watered plain, fertile meadowland, alluvial grassland",
                "morphemes": [
                    "dar",
                    "talom"
                ],
                "etymology": "dar(しずく) + talom(平原)",
                "category": "16. 日常・自然・気象",
                "example_sentence": "Relen el dartalom uo talom.",
                "example_ja": "平原のほとりで潤いの平原がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-87",
        "batch": "Batch 22",
        "domain": "自然・翠の森と白い山嶺・環状の島",
        "title": "白峰の雪と環礁の島影",
        "communicative_need": "白い雪を頂く山嶺、円環を描く湖中の島、大地の深い森の生態系を見守る。",
        "agent_a": {
            "name": "Neri",
            "role": "山麓を歩く採集師"
        },
        "agent_b": {
            "name": "Yura",
            "role": "地形図を描く写字生"
        },
        "turns": [
            {
                "speaker": "Neri",
                "nebulith": "Vyrel el mi ia alinnovan ul klortalon uo velom. Relen el talvelom uo velom.",
                "japanese": "私は森の中で白雪の霊峰と環礁の島を見上げる。森の中で大地の原生林がある。"
            },
            {
                "speaker": "Yura",
                "nebulith": "Soran el miin ia alinnovan ul klortalon. Falun el talvelom al miin.",
                "japanese": "私たちは白雪の霊峰と環礁の島を図録に記す。私たちに大地の原生林が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "alinnovan",
                "pos": "名",
                "meaningJa": "白雪の霊峰、白い山嶺、純白の頂き",
                "meaningEn": "snow-capped mountain, white peak, alabaster summit",
                "morphemes": [
                    "alin",
                    "novan"
                ],
                "etymology": "alin(白い) + novan(山)",
                "category": "16. 日常・自然・気象",
                "example_sentence": "Vyrel el mi ia alinnovan ul klortalon uo velom.",
                "example_ja": "私は森の中で白雪の霊峰と環礁の島を見上げる。"
            },
            {
                "nrs": "klortalon",
                "pos": "名",
                "meaningJa": "環礁の島、円環状の浮島、輪の島影",
                "meaningEn": "atoll island, circular isle, ring-shaped island",
                "morphemes": [
                    "klor",
                    "talon"
                ],
                "etymology": "klor(円) + talon(島)",
                "category": "16. 日常・自然・気象",
                "example_sentence": "Vyrel el mi ia alinnovan ul klortalon uo velom.",
                "example_ja": "私は森の中で白雪の霊峰と環礁の島を見上げる。"
            },
            {
                "nrs": "talvelom",
                "pos": "名",
                "meaningJa": "大地の原生林、深い樹海、内陸の大森林",
                "meaningEn": "inland primeval forest, terrestrial woodland, deep earthen timberland",
                "morphemes": [
                    "tal",
                    "velom"
                ],
                "etymology": "tal(大地) + velom(森)",
                "category": "16. 日常・自然・気象",
                "example_sentence": "Relen el talvelom uo velom.",
                "example_ja": "森の中で大地の原生林がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-88",
        "batch": "Batch 22",
        "domain": "自然・水鳥の巣と森の生き物",
        "title": "水辺の営巣と樹林の獣たち",
        "communicative_need": "水辺の葦原に作られた鳥の巣、森に暮らす穏やかな動物、木の枝の巣箱をそっと観察する。",
        "agent_a": {
            "name": "Neri",
            "role": "野鳥を見守る採集師"
        },
        "agent_b": {
            "name": "Sev",
            "role": "巣箱を修繕する灯守"
        },
        "turns": [
            {
                "speaker": "Neri",
                "nebulith": "Vyrel el mi ia darlyka ul velferas uo velar. Relen el vellyka uo velar.",
                "japanese": "私は庭の木陰で水辺の営巣と森林の生き物を静かに見守る。庭の木陰で樹上の巣がある。"
            },
            {
                "speaker": "Sev",
                "nebulith": "Vymin el miin ia darlyka ul velferas. Falun el vellyka al miin.",
                "japanese": "私たちは水辺の営巣と森林の生き物を保護する。私たちに樹上の巣が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "darlyka",
                "pos": "名",
                "meaningJa": "水辺の営巣、水鳥の浮き巣、葦原の巣",
                "meaningEn": "waterside nest, waterfowl reed nest, floating avian cradle",
                "morphemes": [
                    "dar",
                    "lyka"
                ],
                "etymology": "dar(しずく) + lyka(巣)",
                "category": "5. 生物・生態・環境",
                "example_sentence": "Vyrel el mi ia darlyka ul velferas uo velar.",
                "example_ja": "私は庭の木陰で水辺の営巣と森林の生き物を静かに見守る。"
            },
            {
                "nrs": "velferas",
                "pos": "名",
                "meaningJa": "森林の生き物、樹林の獣、森の動物たち",
                "meaningEn": "forest animal, woodland creature, sylvan fauna",
                "morphemes": [
                    "vel",
                    "feras"
                ],
                "etymology": "vel(木) + feras(動物)",
                "category": "5. 生物・生態・環境",
                "example_sentence": "Vyrel el mi ia darlyka ul velferas uo velar.",
                "example_ja": "私は庭の木陰で水辺の営巣と森林の生き物を静かに見守る。"
            },
            {
                "nrs": "vellyka",
                "pos": "名",
                "meaningJa": "樹上の巣、枝間の鳥の巣、木立の巣箱",
                "meaningEn": "treetop nest, arboreal bird nest, branch cradle",
                "morphemes": [
                    "vel",
                    "lyka"
                ],
                "etymology": "vel(木) + lyka(巣)",
                "category": "5. 生物・生態・環境",
                "example_sentence": "Relen el vellyka uo velar.",
                "example_ja": "庭の木陰で樹上の巣がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-89",
        "batch": "Batch 23",
        "domain": "工芸・銀の鋳型と大地の石材",
        "title": "工房の鋳型と白銀の金属器",
        "communicative_need": "精密な円形の鋳型、星光を宿す合金、樹紋を刻んだ庭石を工房で仕上げる。",
        "agent_a": {
            "name": "Sev",
            "role": "炉を守る灯守"
        },
        "agent_b": {
            "name": "Toa",
            "role": "石材を運ぶ舟守"
        },
        "turns": [
            {
                "speaker": "Sev",
                "nebulith": "Vymin el mi ia klordolas ul vyrtalur uo vorn. Relen el veltalyr uo vorn.",
                "japanese": "私は工房の部屋で円環の鋳型と星紋の合金を鍛え上げる。工房の部屋で木目石がある。"
            },
            {
                "speaker": "Toa",
                "nebulith": "Vyrel el miin ia klordolas ul vyrtalur. Falun el veltalyr al miin.",
                "japanese": "私たちは円環の鋳型と星紋の合金を点検する。私たちに木目石が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "klordolas",
                "pos": "名",
                "meaningJa": "円環の鋳型、輪形の鋳造枠、精密な丸鋳型",
                "meaningEn": "circular casting mold, ring foundry die, round metalworking matrix",
                "morphemes": [
                    "klor",
                    "dolas"
                ],
                "etymology": "klor(円) + dolas(鋳型)",
                "category": "8. 工学・建築・道具",
                "example_sentence": "Vymin el mi ia klordolas ul vyrtalur uo vorn.",
                "example_ja": "私は工房の部屋で円環の鋳型と星紋の合金を鍛え上げる。"
            },
            {
                "nrs": "vyrtalur",
                "pos": "名",
                "meaningJa": "星紋の合金、星光を映す金属、天鉄の地金",
                "meaningEn": "star-forged alloy, astral metal, luminous metallurgical ingot",
                "morphemes": [
                    "vyr",
                    "talur"
                ],
                "etymology": "vyr(星) + talur(金属)",
                "category": "8. 工学・建築・道具",
                "example_sentence": "Vymin el mi ia klordolas ul vyrtalur uo vorn.",
                "example_ja": "私は工房の部屋で円環の鋳型と星紋の合金を鍛え上げる。"
            },
            {
                "nrs": "veltalyr",
                "pos": "名",
                "meaningJa": "木目石、樹紋の庭石、珪化木の石材",
                "meaningEn": "wood-grained stone, petrified timber rock, arboreal patterned slate",
                "morphemes": [
                    "vel",
                    "talyr"
                ],
                "etymology": "vel(木) + talyr(石)",
                "category": "8. 工学・建築・道具",
                "example_sentence": "Relen el veltalyr uo vorn.",
                "example_ja": "工房の部屋で木目石がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-90",
        "batch": "Batch 23",
        "domain": "工芸・彫刻の小刀と書き手の筆",
        "title": "白銀の筆と木彫りの小刀",
        "communicative_need": "滑らかに書ける白軸の筆、薬草や木片を削る小刀、道具を収める収納箱を整える。",
        "agent_a": {
            "name": "Yura",
            "role": "筆を整える写字生"
        },
        "agent_b": {
            "name": "Neri",
            "role": "採取小刀を研ぐ採集師"
        },
        "turns": [
            {
                "speaker": "Yura",
                "nebulith": "Vymin el mi ia alinkirel ul darserel uo vorn. Relen el havkypal uo vorn.",
                "japanese": "私は作業部屋で白軸の細筆と水研ぎの小刀を手入れする。作業部屋で歳月の収納箱がある。"
            },
            {
                "speaker": "Neri",
                "nebulith": "Cynel el miin ia alinkirel ul darserel. Falun el havkypal al miin.",
                "japanese": "私たちは白軸の細筆と水研ぎの小刀を大切にする。私たちに歳月の収納箱が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "alinkirel",
                "pos": "名",
                "meaningJa": "白軸の細筆、純白の写字筆、白羽のペン",
                "meaningEn": "white-shafted pen, ivory calligraphy brush, pure quill",
                "morphemes": [
                    "alin",
                    "kirel"
                ],
                "etymology": "alin(白い) + kirel(筆)",
                "category": "8. 工学・建築・道具",
                "example_sentence": "Vymin el mi ia alinkirel ul darserel uo vorn.",
                "example_ja": "私は作業部屋で白軸の細筆と水研ぎの小刀を手入れする。"
            },
            {
                "nrs": "darserel",
                "pos": "名",
                "meaningJa": "水研ぎの小刀、澄んだ刃のナイフ、細工用の小刀",
                "meaningEn": "water-honed knife, fine carving blade, polished utility lancet",
                "morphemes": [
                    "dar",
                    "serel"
                ],
                "etymology": "dar(しずく) + serel(小刀)",
                "category": "8. 工学・建築・道具",
                "example_sentence": "Vymin el mi ia alinkirel ul darserel uo vorn.",
                "example_ja": "私は作業部屋で白軸の細筆と水研ぎの小刀を手入れする。"
            },
            {
                "nrs": "havkypal",
                "pos": "名",
                "meaningJa": "歳月の収納箱、年代物の保管箱、時の手文庫",
                "meaningEn": "time-seasoned chest, heirloom storage box, chronicle coffer",
                "morphemes": [
                    "hav",
                    "kypal"
                ],
                "etymology": "hav(時) + kypal(箱)",
                "category": "8. 工学・建築・道具",
                "example_sentence": "Relen el havkypal uo vorn.",
                "example_ja": "作業部屋で歳月の収納箱がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-91",
        "batch": "Batch 23",
        "domain": "住空間・休息の寝床と肘掛け椅子",
        "title": "白布の寝台と円卓の椅子",
        "communicative_need": "清潔な白布の寝床、円卓を囲む椅子、読書のための肘掛け椅子を客間にしつらえる。",
        "agent_a": {
            "name": "Sev",
            "role": "客間を整える灯守"
        },
        "agent_b": {
            "name": "Yura",
            "role": "書見台を置く写字生"
        },
        "turns": [
            {
                "speaker": "Sev",
                "nebulith": "Vymin el mi ia alinkymel ul klortasel uo govan. Relen el veltasor uo govan.",
                "japanese": "私は家の中で白布の寝床と円卓の椅子を整える。家の中で木製の肘掛け椅子がある。"
            },
            {
                "speaker": "Yura",
                "nebulith": "Cynel el miin ia alinkymel ul klortasel. Falun el veltasor al miin.",
                "japanese": "私たちは白布の寝床と円卓の椅子を好む。私たちに木製の肘掛け椅子が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "alinkymel",
                "pos": "名",
                "meaningJa": "白布の寝床、清潔な白い寝台、安眠の白ベッド",
                "meaningEn": "white-linened bed, clean resting couch, pure slumber berth",
                "morphemes": [
                    "alin",
                    "kymel"
                ],
                "etymology": "alin(白い) + kymel(寝床)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Vymin el mi ia alinkymel ul klortasel uo govan.",
                "example_ja": "私は家の中で白布の寝床と円卓の椅子を整える。"
            },
            {
                "nrs": "klortasel",
                "pos": "名",
                "meaningJa": "円卓の椅子、輪座の腰掛け、車座の木椅子",
                "meaningEn": "roundtable chair, circle-seating stool, council seat",
                "morphemes": [
                    "klor",
                    "tasel"
                ],
                "etymology": "klor(円) + tasel(椅子)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Vymin el mi ia alinkymel ul klortasel uo govan.",
                "example_ja": "私は家の中で白布の寝床と円卓の椅子を整える。"
            },
            {
                "nrs": "veltasor",
                "pos": "名",
                "meaningJa": "木製の肘掛け椅子、樹材の安楽椅子、森の読書椅子",
                "meaningEn": "wooden armchair, timber lounge seat, carved reading chair",
                "morphemes": [
                    "vel",
                    "tasor"
                ],
                "etymology": "vel(木) + tasor(肘掛け椅子)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Relen el veltasor uo govan.",
                "example_ja": "家の中で木製の肘掛け椅子がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-92",
        "batch": "Batch 23",
        "domain": "建築・夜の扉と養生の部屋・ハーブ園",
        "title": "宵の門扉と香草の庭",
        "communicative_need": "夜風を防ぐ重厚な扉、滋養と休息のための部屋、薬草が茂る庭を夕暮れに巡回する。",
        "agent_a": {
            "name": "Sev",
            "role": "鍵を確かめる灯守"
        },
        "agent_b": {
            "name": "Neri",
            "role": "鉢植えを並べる採集師"
        },
        "turns": [
            {
                "speaker": "Sev",
                "nebulith": "Vyrel el mi ia kymlerel ul nervorn uo velar. Relen el nervelar uo velar.",
                "japanese": "私は中庭で宵の門扉と養生の部屋を見回る。中庭で薬草の菜園がある。"
            },
            {
                "speaker": "Neri",
                "nebulith": "Vymin el miin ia kymlerel ul nervorn. Falun el nervelar al miin.",
                "japanese": "私たちは宵の門扉と養生の部屋を守る。私たちに薬草の菜園が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "kymlerel",
                "pos": "名",
                "meaningJa": "宵の門扉、夜を守る扉、夜間の防風戸",
                "meaningEn": "night portal, evening gate door, nocturnal shutter",
                "morphemes": [
                    "kym",
                    "lerel"
                ],
                "etymology": "kym(夜) + lerel(扉)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Vyrel el mi ia kymlerel ul nervorn uo velar.",
                "example_ja": "私は中庭で宵の門扉と養生の部屋を見回る。"
            },
            {
                "nrs": "nervorn",
                "pos": "名",
                "meaningJa": "養生の部屋、滋養と休息の室、歓待の食堂間",
                "meaningEn": "nourishment chamber, recuperation room, hospitality parlor",
                "morphemes": [
                    "ner",
                    "vorn"
                ],
                "etymology": "ner(滋養) + vorn(部屋)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Vyrel el mi ia kymlerel ul nervorn uo velar.",
                "example_ja": "私は中庭で宵の門扉と養生の部屋を見回る。"
            },
            {
                "nrs": "nervelar",
                "pos": "名",
                "meaningJa": "薬草の菜園、滋養草の庭、実りのキッチンガーデン",
                "meaningEn": "culinary herb garden, nourishing courtyard, kitchen garden plot",
                "morphemes": [
                    "ner",
                    "velar"
                ],
                "etymology": "ner(滋養) + velar(庭)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Relen el nervelar uo velar.",
                "example_ja": "中庭で薬草の菜園がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-93",
        "batch": "Batch 24",
        "domain": "交通・水辺の船着き場と森の乗合馬車",
        "title": "運河の駅舎と樹林の乗り物",
        "communicative_need": "水路の舟が発着する水辺の駅、森の道を走る木製の乗り物、広場に掲げる白い旗を準備する。",
        "agent_a": {
            "name": "Toa",
            "role": "桟橋を点検する舟守"
        },
        "agent_b": {
            "name": "Sev",
            "role": "合図旗を掲げる灯守"
        },
        "turns": [
            {
                "speaker": "Toa",
                "nebulith": "Vyrel el mi ia darlarar ul vellaros uo larar. Relen el alinvylar uo larar.",
                "japanese": "私は駅舎の前で水辺の船着き駅と木製の乗合馬車を確認する。駅舎の前で純白の合図旗がある。"
            },
            {
                "speaker": "Sev",
                "nebulith": "Vymin el miin ia darlarar ul vellaros. Falun el alinvylar al miin.",
                "japanese": "私たちは水辺の船着き駅と木製の乗合馬車を整備する。私たちに純白の合図旗が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "darlarar",
                "pos": "名",
                "meaningJa": "水辺の船着き駅、運河の停留所、水上駅舎",
                "meaningEn": "waterside station, canal boat depot, aquatic transit stop",
                "morphemes": [
                    "dar",
                    "larar"
                ],
                "etymology": "dar(しずく) + larar(駅)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Vyrel el mi ia darlarar ul vellaros uo larar.",
                "example_ja": "私は駅舎の前で水辺の船着き駅と木製の乗合馬車を確認する。"
            },
            {
                "nrs": "vellaros",
                "pos": "名",
                "meaningJa": "木製の乗合馬車、森林軌道の乗り物、木造の運搬車",
                "meaningEn": "wooden carriage, timber transit vehicle, forest wagon",
                "morphemes": [
                    "vel",
                    "laros"
                ],
                "etymology": "vel(木) + laros(乗り物)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Vyrel el mi ia darlarar ul vellaros uo larar.",
                "example_ja": "私は駅舎の前で水辺の船着き駅と木製の乗合馬車を確認する。"
            },
            {
                "nrs": "alinvylar",
                "pos": "名",
                "meaningJa": "純白の合図旗、出航の白旗、平和の白い幟",
                "meaningEn": "pure white flag, clear signal banner, alabaster pennant",
                "morphemes": [
                    "alin",
                    "vylar"
                ],
                "etymology": "alin(白い) + vylar(旗)",
                "category": "11. 都市・建築・住空間",
                "example_sentence": "Relen el alinvylar uo larar.",
                "example_ja": "駅舎の前で純白の合図旗がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-94",
        "batch": "Batch 24",
        "domain": "計測・携帯星盤と望遠スコープ",
        "title": "銀の星盤と水路の測度",
        "communicative_need": "旅先で方位を知る携帯星盤、遠くの灯台を捉える望遠スコープ、水深を測る測度器を携える。",
        "agent_a": {
            "name": "Toa",
            "role": "航路を測る舟守"
        },
        "agent_b": {
            "name": "Yura",
            "role": "目盛りを読む写字生"
        },
        "turns": [
            {
                "speaker": "Toa",
                "nebulith": "Vymin el mi ia vyrpelel ul alinvylom uo larar. Relen el darryvel uo larar.",
                "japanese": "私は港の桟橋で恒星の携帯星盤と澄んだ望遠スコープを校正する。港の桟橋で水深の測度がある。"
            },
            {
                "speaker": "Yura",
                "nebulith": "Vyrel el miin ia vyrpelel ul alinvylom. Falun el darryvel al miin.",
                "japanese": "私たちは恒星の携帯星盤と澄んだ望遠スコープを覗き込む。私たちに水深の測度が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "vyrpelel",
                "pos": "名",
                "meaningJa": "恒星の携帯星盤、星見のアストロラーベ、天測の懐中盤",
                "meaningEn": "stellar portable astrolabe, starfinder pocket dial, celestial navigation disc",
                "morphemes": [
                    "vyr",
                    "pelel"
                ],
                "etymology": "vyr(星) + pelel(携帯星盤)",
                "category": "8. 工学・建築・道具",
                "example_sentence": "Vymin el mi ia vyrpelel ul alinvylom uo larar.",
                "example_ja": "私は港の桟橋で恒星の携帯星盤と澄んだ望遠スコープを校正する。"
            },
            {
                "nrs": "alinvylom",
                "pos": "名",
                "meaningJa": "澄んだ望遠スコープ、高透過の観測鏡筒、白銀の望遠鏡",
                "meaningEn": "clear telescope scope, high-clarity sighting tube, bright opticalfinder",
                "morphemes": [
                    "alin",
                    "vylom"
                ],
                "etymology": "alin(白い) + vylom(スコープ)",
                "category": "8. 工学・建築・道具",
                "example_sentence": "Vymin el mi ia vyrpelel ul alinvylom uo larar.",
                "example_ja": "私は港の桟橋で恒星の携帯星盤と澄んだ望遠スコープを校正する。"
            },
            {
                "nrs": "darryvel",
                "pos": "名",
                "meaningJa": "水深の測度、水流の計測基準、水路の尺度",
                "meaningEn": "hydrological metric, water-depth measure, stream gauge standard",
                "morphemes": [
                    "dar",
                    "ryvel"
                ],
                "etymology": "dar(しずく) + ryvel(測度)",
                "category": "8. 工学・建築・道具",
                "example_sentence": "Relen el darryvel uo larar.",
                "example_ja": "港の桟橋で水深の測度がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-95",
        "batch": "Batch 24",
        "domain": "数理・星辰演算儀と記憶素の書庫",
        "title": "大地の演算儀と白銀の記憶素",
        "communicative_need": "地殻変動や暦を計算する演算儀、清らかな白銀の星石記憶素、双方向につながる交信ノードを点検する。",
        "agent_a": {
            "name": "Yura",
            "role": "記憶素を配列する写字生"
        },
        "agent_b": {
            "name": "Sev",
            "role": "蓄電器をつなぐ灯守"
        },
        "turns": [
            {
                "speaker": "Yura",
                "nebulith": "Vymin el mi ia talmator ul alinsoril uo livar. Relen el klorjytel uo livar.",
                "japanese": "私は星辰書庫で地勢の星辰演算儀と純白の星石記憶素を保守する。星辰書庫で環状接続ノードがある。"
            },
            {
                "speaker": "Sev",
                "nebulith": "Soran el miin ia talmator ul alinsoril. Falun el klorjytel al miin.",
                "japanese": "私たちは地勢の星辰演算儀と純白の星石記憶素を記録する。私たちに環状接続ノードが輝く。"
            }
        ],
        "words": [
            {
                "nrs": "talmator",
                "pos": "名",
                "meaningJa": "地勢の星辰演算儀、大地測量の計算機、基礎演算装置",
                "meaningEn": "geodetic computation engine, terrestrial calculator, earth-grid processor",
                "morphemes": [
                    "tal",
                    "mator"
                ],
                "etymology": "tal(大地) + mator(星辰演算儀)",
                "category": "3. 数理・情報・計算機",
                "example_sentence": "Vymin el mi ia talmator ul alinsoril uo livar.",
                "example_ja": "私は星辰書庫で地勢の星辰演算儀と純白の星石記憶素を保守する。"
            },
            {
                "nrs": "alinsoril",
                "pos": "名",
                "meaningJa": "純白の星石記憶素、初期状態の水晶記憶素、清浄なメモリ結晶",
                "meaningEn": "blank astral memory crystal, pure storage element, unblemished memory cell",
                "morphemes": [
                    "alin",
                    "soril"
                ],
                "etymology": "alin(白い) + soril(星石記憶素)",
                "category": "3. 数理・情報・計算機",
                "example_sentence": "Vymin el mi ia talmator ul alinsoril uo livar.",
                "example_ja": "私は星辰書庫で地勢の星辰演算儀と純白の星石記憶素を保守する。"
            },
            {
                "nrs": "klorjytel",
                "pos": "名",
                "meaningJa": "環状接続ノード、円環網の交信節点、リング型中継点",
                "meaningEn": "ring network node, circular hub junction, concentric relay vertex",
                "morphemes": [
                    "klor",
                    "jytel"
                ],
                "etymology": "klor(円) + jytel(ノード)",
                "category": "3. 数理・情報・計算機",
                "example_sentence": "Relen el klorjytel uo livar.",
                "example_ja": "星辰書庫で環状接続ノードがある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-96",
        "batch": "Batch 24",
        "domain": "通信・全天交信網と光のメッセージ",
        "title": "星の通信網と白羽の便り",
        "communicative_need": "空を結ぶ全天交信星網、星光に乗せて届けるメッセージ、水流や風で蓄えるバッテリーを運用する。",
        "agent_a": {
            "name": "Sev",
            "role": "交信灯を操作する灯守"
        },
        "agent_b": {
            "name": "Toa",
            "role": "離島の便りを受ける舟守"
        },
        "turns": [
            {
                "speaker": "Sev",
                "nebulith": "Vyrel el mi ia vyrtolom ul alintolas uo domom. Relen el darjynel uo domom.",
                "japanese": "私は街の通信塔で恒星間の交信網と吉報の白文を受信する。街の通信塔で水力蓄電池がある。"
            },
            {
                "speaker": "Toa",
                "nebulith": "Soran el miin ia vyrtolom ul alintolas. Falun el darjynel al miin.",
                "japanese": "私たちは恒星間の交信網と吉報の白文を返信する。私たちに水力蓄電池が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "vyrtolom",
                "pos": "名",
                "meaningJa": "恒星間の交信網、星々を結ぶ通信網、天球ネットワーク",
                "meaningEn": "stellar communication network, starlight relay web, astral telemetry grid",
                "morphemes": [
                    "vyr",
                    "tolom"
                ],
                "etymology": "vyr(星) + tolom(全天交信星網)",
                "category": "9. 通信・ネットワーク",
                "example_sentence": "Vyrel el mi ia vyrtolom ul alintolas uo domom.",
                "example_ja": "私は街の通信塔で恒星間の交信網と吉報の白文を受信する。"
            },
            {
                "nrs": "alintolas",
                "pos": "名",
                "meaningJa": "吉報の白文、清らかなメッセージ、平穏を告げる便り",
                "meaningEn": "clear tidings message, peaceful dispatch, white-sealed letter",
                "morphemes": [
                    "alin",
                    "tolas"
                ],
                "etymology": "alin(白い) + tolas(メッセージ)",
                "category": "9. 通信・ネットワーク",
                "example_sentence": "Vyrel el mi ia vyrtolom ul alintolas uo domom.",
                "example_ja": "私は街の通信塔で恒星間の交信網と吉報の白文を受信する。"
            },
            {
                "nrs": "darjynel",
                "pos": "名",
                "meaningJa": "水力蓄電池、水流充電のバッテリー、湿式蓄電槽",
                "meaningEn": "hydro-charged battery, water-powered cell, liquid electrolyte accumulator",
                "morphemes": [
                    "dar",
                    "jynel"
                ],
                "etymology": "dar(しずく) + jynel(バッテリー)",
                "category": "9. 通信・ネットワーク",
                "example_sentence": "Relen el darjynel uo domom.",
                "example_ja": "街の通信塔で水力蓄電池がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-97",
        "batch": "Batch 25",
        "domain": "数理・基本定数と時間の変数・連続関数",
        "title": "大地の定数と星軌道の関数",
        "communicative_need": "揺るがない大地の基本定数、時間とともに移ろう変数、滑らかに巡る円関数を黒板に書き出す。",
        "agent_a": {
            "name": "Yura",
            "role": "数式を解説する写字生"
        },
        "agent_b": {
            "name": "Sev",
            "role": "図形を描く灯守"
        },
        "turns": [
            {
                "speaker": "Yura",
                "nebulith": "Soran el mi ia talfiras ul vyrkelon uo livar. Relen el klorkiril uo livar.",
                "japanese": "私は講義室で基礎定数と天体変数を記述する。講義室で円関数がある。"
            },
            {
                "speaker": "Sev",
                "nebulith": "Vyrel el miin ia talfiras ul vyrkelon. Falun el klorkiril al miin.",
                "japanese": "私たちは基礎定数と天体変数を検証する。私たちに円関数が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "talfiras",
                "pos": "名",
                "meaningJa": "基礎定数、大地の不変定数、重力定数値",
                "meaningEn": "fundamental terrestrial constant, base physical invariant, earth constant",
                "morphemes": [
                    "tal",
                    "firas"
                ],
                "etymology": "tal(大地) + firas(定数)",
                "category": "3. 数理・情報・計算機",
                "example_sentence": "Soran el mi ia talfiras ul vyrkelon uo livar.",
                "example_ja": "私は講義室で基礎定数と天体変数を記述する。"
            },
            {
                "nrs": "vyrkelon",
                "pos": "名",
                "meaningJa": "天体変数、星位の変動数、軌道パラメータ",
                "meaningEn": "stellar variable, astronomical parameter, celestial coordinate variable",
                "morphemes": [
                    "vyr",
                    "kelon"
                ],
                "etymology": "vyr(星) + kelon(変数)",
                "category": "3. 数理・情報・計算機",
                "example_sentence": "Soran el mi ia talfiras ul vyrkelon uo livar.",
                "example_ja": "私は講義室で基礎定数と天体変数を記述する。"
            },
            {
                "nrs": "klorkiril",
                "pos": "名",
                "meaningJa": "円関数、周期の環状関数、回転の写像",
                "meaningEn": "circular function, trigonometric cycle mapping, periodic ring function",
                "morphemes": [
                    "klor",
                    "kiril"
                ],
                "etymology": "klor(円) + kiril(関数)",
                "category": "3. 数理・情報・計算機",
                "example_sentence": "Relen el klorkiril uo livar.",
                "example_ja": "講義室で円関数がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-98",
        "batch": "Batch 25",
        "domain": "数理・整数の集合と精密な小数",
        "title": "円環の集合と細やかな端数",
        "communicative_need": "完結した円環の集合、基準となる単位整数、微細な変化を表す小数を帳面で検算する。",
        "agent_a": {
            "name": "Yura",
            "role": "帳面を検算する写字生"
        },
        "agent_b": {
            "name": "Toa",
            "role": "積荷の目方を量る舟守"
        },
        "turns": [
            {
                "speaker": "Yura",
                "nebulith": "Vyrel el mi ia klorjylom ul talunor uo renar. Relen el dardelis uo renar.",
                "japanese": "私は市場の計量所で閉じた集合と基準整数を検算する。市場の計量所で微細な小数がある。"
            },
            {
                "speaker": "Toa",
                "nebulith": "Soran el miin ia klorjylom ul talunor. Falun el dardelis al miin.",
                "japanese": "私たちは閉じた集合と基準整数を明記する。私たちに微細な小数が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "klorjylom",
                "pos": "名",
                "meaningJa": "閉じた集合、円環の要素群、完全な集合族",
                "meaningEn": "closed set, circular ensemble, complete group collection",
                "morphemes": [
                    "klor",
                    "jylom"
                ],
                "etymology": "klor(円) + jylom(集合)",
                "category": "3. 数理・情報・計算機",
                "example_sentence": "Vyrel el mi ia klorjylom ul talunor uo renar.",
                "example_ja": "私は市場の計量所で閉じた集合と基準整数を検算する。"
            },
            {
                "nrs": "talunor",
                "pos": "名",
                "meaningJa": "基準整数、土台となる自然数、基本の整数値",
                "meaningEn": "base integer, foundational whole number, cardinal ground integer",
                "morphemes": [
                    "tal",
                    "unor"
                ],
                "etymology": "tal(大地) + unor(整数)",
                "category": "3. 数理・情報・計算機",
                "example_sentence": "Vyrel el mi ia klorjylom ul talunor uo renar.",
                "example_ja": "私は市場の計量所で閉じた集合と基準整数を検算する。"
            },
            {
                "nrs": "dardelis",
                "pos": "名",
                "meaningJa": "微細な小数、しずくのような端数、精密な小数部",
                "meaningEn": "fine decimal fraction, minute fractional part, droplet-scale precision",
                "morphemes": [
                    "dar",
                    "delis"
                ],
                "etymology": "dar(しずく) + delis(小数)",
                "category": "3. 数理・情報・計算機",
                "example_sentence": "Relen el dardelis uo renar.",
                "example_ja": "市場の計量所で微細な小数がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-99",
        "batch": "Batch 25",
        "domain": "学問・自然学者と数理士の探究",
        "title": "森の学者と天文学の数理士",
        "communicative_need": "森の植生を調べる自然学者、星の運行を計算する数理士、多次元の空間構造を議論する。",
        "agent_a": {
            "name": "Neri",
            "role": "標本を示す採集師"
        },
        "agent_b": {
            "name": "Yura",
            "role": "数理モデルを組む写字生"
        },
        "turns": [
            {
                "speaker": "Neri",
                "nebulith": "Vyrel el mi ia velsufis ul vyrsufor uo livar. Relen el vyrniven uo livar.",
                "japanese": "私は星辰書庫の広間で森林学者と天体数理士を討議する。星辰書庫の広間で天球の次元がある。"
            },
            {
                "speaker": "Yura",
                "nebulith": "Cynel el miin ia velsufis ul vyrsufor. Falun el vyrniven al miin.",
                "japanese": "私たちは森林学者と天体数理士を尊重する。私たちに天球の次元が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "velsufis",
                "pos": "名",
                "meaningJa": "森林学者、植物と生態の学者、自然博物学者",
                "meaningEn": "botanical scholar, forest naturalist, ecological researcher",
                "morphemes": [
                    "vel",
                    "sufis"
                ],
                "etymology": "vel(木) + sufis(学者)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Vyrel el mi ia velsufis ul vyrsufor uo livar.",
                "example_ja": "私は星辰書庫の広間で森林学者と天体数理士を討議する。"
            },
            {
                "nrs": "vyrsufor",
                "pos": "名",
                "meaningJa": "天体数理士、星辰軌道の計算士、天文数学者",
                "meaningEn": "celestial mathematician, astro-computational scholar, orbital analyst",
                "morphemes": [
                    "vyr",
                    "sufor"
                ],
                "etymology": "vyr(星) + sufor(星辰数理士)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Vyrel el mi ia velsufis ul vyrsufor uo livar.",
                "example_ja": "私は星辰書庫の広間で森林学者と天体数理士を討議する。"
            },
            {
                "nrs": "vyrniven",
                "pos": "名",
                "meaningJa": "天球の次元、星空間の次元軸、高次の天体空間",
                "meaningEn": "celestial dimension, astral spatial axis, cosmic coordinate plane",
                "morphemes": [
                    "vyr",
                    "niven"
                ],
                "etymology": "vyr(星) + niven(次元)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Relen el vyrniven uo livar.",
                "example_ja": "星辰書庫の広間で天球の次元がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-100",
        "batch": "Batch 25",
        "domain": "哲学・真偽の理と同一性の証明",
        "title": "澄んだ真理と揺るぎない証拠",
        "communicative_need": "曇りのない真偽の判断律、円環のように完結した同一性、大地の確かな物的証拠を確かめる。",
        "agent_a": {
            "name": "Yura",
            "role": "論考をまとめる写字生"
        },
        "agent_b": {
            "name": "Sev",
            "role": "記録を照らし合わせる灯守"
        },
        "turns": [
            {
                "speaker": "Yura",
                "nebulith": "Vyrel el mi ia alinvedil ul klorunvis uo klorcalor. Relen el talzydis uo klorcalor.",
                "japanese": "私は円卓評議の間で明晰な真偽律と円環の同一性を吟味する。円卓評議の間で物的証拠がある。"
            },
            {
                "speaker": "Sev",
                "nebulith": "Soran el miin ia alinvedil ul klorunvis. Falun el talzydis al miin.",
                "japanese": "私たちは明晰な真偽律と円環の同一性を証明する。私たちに物的証拠が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "alinvedil",
                "pos": "名",
                "meaningJa": "明晰な真偽律、曇りなき論理基準、純粋な判断律",
                "meaningEn": "clear truth-value law, transparent logical criterion, unclouded verity rule",
                "morphemes": [
                    "alin",
                    "vedil"
                ],
                "etymology": "alin(白い) + vedil(真偽律)",
                "category": "13. 精神・感情・内省",
                "example_sentence": "Vyrel el mi ia alinvedil ul klorunvis uo klorcalor.",
                "example_ja": "私は円卓評議の間で明晰な真偽律と円環の同一性を吟味する。"
            },
            {
                "nrs": "klorunvis",
                "pos": "名",
                "meaningJa": "円環の同一性、完全な一致律、揺るぎない自己同一性",
                "meaningEn": "complete identity, circular equivalence, unbroken self-sameness",
                "morphemes": [
                    "klor",
                    "unvis"
                ],
                "etymology": "klor(円) + unvis(同一性)",
                "category": "13. 精神・感情・内省",
                "example_sentence": "Vyrel el mi ia alinvedil ul klorunvis uo klorcalor.",
                "example_ja": "私は円卓評議の間で明晰な真偽律と円環の同一性を吟味する。"
            },
            {
                "nrs": "talzydis",
                "pos": "名",
                "meaningJa": "物的証拠、大地の確かな証跡、実地の証拠品",
                "meaningEn": "physical evidence, tangible terrestrial proof, material testimony",
                "morphemes": [
                    "tal",
                    "zydis"
                ],
                "etymology": "tal(大地) + zydis(証拠)",
                "category": "13. 精神・感情・内省",
                "example_sentence": "Relen el talzydis uo klorcalor.",
                "example_ja": "円卓評議の間で物的証拠がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-101",
        "batch": "Batch 26",
        "domain": "医療・植物細胞と清らかな血液・骨格",
        "title": "新芽の細胞と健やかな身体",
        "communicative_need": "みずみずしい植物の細胞、清らかに巡る血液、大地のように強靭な骨格を医学書で学ぶ。",
        "agent_a": {
            "name": "Neri",
            "role": "薬草学を教える採集師"
        },
        "agent_b": {
            "name": "Yura",
            "role": "解剖図を写す写字生"
        },
        "turns": [
            {
                "speaker": "Neri",
                "nebulith": "Vyrel el mi ia velkivan ul dardavel uo vorn. Relen el talduril uo vorn.",
                "japanese": "私は医務室で植物細胞と清らかな血流を観察する。医務室で強靭な骨格がある。"
            },
            {
                "speaker": "Yura",
                "nebulith": "Soran el miin ia velkivan ul dardavel. Falun el talduril al miin.",
                "japanese": "私たちは植物細胞と清らかな血流を図解する。私たちに強靭な骨格が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "velkivan",
                "pos": "名",
                "meaningJa": "植物細胞、木の葉の細胞組織、緑の生体細胞",
                "meaningEn": "plant cell, botanical tissue cell, leaf cellular structure",
                "morphemes": [
                    "vel",
                    "kivan"
                ],
                "etymology": "vel(木) + kivan(細胞)",
                "category": "4. 人体・生理・医療",
                "example_sentence": "Vyrel el mi ia velkivan ul dardavel uo vorn.",
                "example_ja": "私は医務室で植物細胞と清らかな血流を観察する。"
            },
            {
                "nrs": "dardavel",
                "pos": "名",
                "meaningJa": "清らかな血流、潤いの血液、健やかな循環血",
                "meaningEn": "healthy bloodstream, vital circulating blood, pure vascular flow",
                "morphemes": [
                    "dar",
                    "davel"
                ],
                "etymology": "dar(しずく) + davel(血液)",
                "category": "4. 人体・生理・医療",
                "example_sentence": "Vyrel el mi ia velkivan ul dardavel uo vorn.",
                "example_ja": "私は医務室で植物細胞と清らかな血流を観察する。"
            },
            {
                "nrs": "talduril",
                "pos": "名",
                "meaningJa": "強靭な骨格、盤石の骨組み、体幹の骨",
                "meaningEn": "sturdy bone structure, skeletal frame, foundational bone",
                "morphemes": [
                    "tal",
                    "duril"
                ],
                "etymology": "tal(大地) + duril(骨)",
                "category": "4. 人体・生理・医療",
                "example_sentence": "Relen el talduril uo vorn.",
                "example_ja": "医務室で強靭な骨格がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-102",
        "batch": "Batch 26",
        "domain": "医療・安らかな鼓動と癒やしの霊薬",
        "title": "穏やかな心臓と森の活力",
        "communicative_need": "穏やかに打つ心臓の鼓動、星露を集めた癒やしの薬、森の空気から得る活力を確かめる。",
        "agent_a": {
            "name": "Neri",
            "role": "脈を診る採集師"
        },
        "agent_b": {
            "name": "Toa",
            "role": "湯治から戻った舟守"
        },
        "turns": [
            {
                "speaker": "Neri",
                "nebulith": "Vymin el mi ia alinteira ul vyrzyvil uo vorn. Relen el velzyvor uo vorn.",
                "japanese": "私は養生室で穏やかな心臓と星露の霊薬を養う。養生室で森林の活力がある。"
            },
            {
                "speaker": "Toa",
                "nebulith": "Cynel el miin ia alinteira ul vyrzyvil. Falun el velzyvor al miin.",
                "japanese": "私たちは穏やかな心臓と星露の霊薬を感謝する。私たちに森林の活力が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "alinteira",
                "pos": "名",
                "meaningJa": "穏やかな心臓、澄んだ鼓動の胸、平静な心音",
                "meaningEn": "calm heart, steady heartbeat, serene cardiac rhythm",
                "morphemes": [
                    "alin",
                    "teira"
                ],
                "etymology": "alin(白い) + teira(心臓)",
                "category": "4. 人体・生理・医療",
                "example_sentence": "Vymin el mi ia alinteira ul vyrzyvil uo vorn.",
                "example_ja": "私は養生室で穏やかな心臓と星露の霊薬を養う。"
            },
            {
                "nrs": "vyrzyvil",
                "pos": "名",
                "meaningJa": "星露の霊薬、夜露で煎じた薬、癒やしの星薬",
                "meaningEn": "starlight elixir, night-dew medicine, celestial herbal remedy",
                "morphemes": [
                    "vyr",
                    "zyvil"
                ],
                "etymology": "vyr(星) + zyvil(薬)",
                "category": "4. 人体・生理・医療",
                "example_sentence": "Vymin el mi ia alinteira ul vyrzyvil uo vorn.",
                "example_ja": "私は養生室で穏やかな心臓と星露の霊薬を養う。"
            },
            {
                "nrs": "velzyvor",
                "pos": "名",
                "meaningJa": "森林の活力、樹々の生命力、緑の生気",
                "meaningEn": "woodland vitality, forest stamina, sylvan life vigor",
                "morphemes": [
                    "vel",
                    "zyvor"
                ],
                "etymology": "vel(木) + zyvor(活力)",
                "category": "4. 人体・生理・医療",
                "example_sentence": "Relen el velzyvor uo vorn.",
                "example_ja": "養生室で森林の活力がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-103",
        "batch": "Batch 26",
        "domain": "医療・水あたりと季節の養生・健やかな体",
        "title": "季節の養生と円満な健康",
        "communicative_need": "旅先での水あたりや不調を防ぎ、時の巡りに合わせた健康管理と清らかな体力を保つ。",
        "agent_a": {
            "name": "Neri",
            "role": "煎じ薬を配る採集師"
        },
        "agent_b": {
            "name": "Sev",
            "role": "湯を沸かす灯守"
        },
        "turns": [
            {
                "speaker": "Neri",
                "nebulith": "Vymin el mi ia darkylar ul havzyvas uo nerom. Relen el alinzyvor uo nerom.",
                "japanese": "私は共同厨房で水あたりと季節の養生を整える。共同厨房で清らかな気力がある。"
            },
            {
                "speaker": "Sev",
                "nebulith": "Vyrel el miin ia darkylar ul havzyvas. Falun el alinzyvor al miin.",
                "japanese": "私たちは水あたりと季節の養生を気遣う。私たちに清らかな気力が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "darkylar",
                "pos": "名",
                "meaningJa": "水あたり、湿気による不調、水辺の病",
                "meaningEn": "waterborne ailment, dampness sickness, traveler's water chill",
                "morphemes": [
                    "dar",
                    "kylar"
                ],
                "etymology": "dar(しずく) + kylar(病)",
                "category": "4. 人体・生理・医療",
                "example_sentence": "Vymin el mi ia darkylar ul havzyvas uo nerom.",
                "example_ja": "私は共同厨房で水あたりと季節の養生を整える。"
            },
            {
                "nrs": "havzyvas",
                "pos": "名",
                "meaningJa": "季節の養生、歳月を重ねた健康、日々の健やかさ",
                "meaningEn": "seasonal wellness, lifelong health, timely physical care",
                "morphemes": [
                    "hav",
                    "zyvas"
                ],
                "etymology": "hav(時) + zyvas(健康)",
                "category": "4. 人体・生理・医療",
                "example_sentence": "Vymin el mi ia darkylar ul havzyvas uo nerom.",
                "example_ja": "私は共同厨房で水あたりと季節の養生を整える。"
            },
            {
                "nrs": "alinzyvor",
                "pos": "名",
                "meaningJa": "清らかな気力、曇りなき体力、爽快な活力",
                "meaningEn": "pure stamina, refreshed vigor, unclouded bodily energy",
                "morphemes": [
                    "alin",
                    "zyvor"
                ],
                "etymology": "alin(白い) + zyvor(活力)",
                "category": "4. 人体・生理・医療",
                "example_sentence": "Relen el alinzyvor uo nerom.",
                "example_ja": "共同厨房で清らかな気力がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-104",
        "batch": "Batch 26",
        "domain": "身体・確かな足取りと澄んだ頭脳・語り口",
        "title": "大地を踏む足と明晰な頭脳",
        "communicative_need": "大地をしっかりと踏みしめる足、澄み切った頭脳、優しい言葉を紡ぐ口元を讃え合う。",
        "agent_a": {
            "name": "Toa",
            "role": "荷を担ぐ舟守"
        },
        "agent_b": {
            "name": "Yura",
            "role": "朗読を行う写字生"
        },
        "turns": [
            {
                "speaker": "Toa",
                "nebulith": "Vyrel el mi ia tallarin ul alinnoven uo domom. Relen el darfenel uo domom.",
                "japanese": "私は街の広場で大地を踏む足と明晰な頭脳を見守る。街の広場で潤いの口元がある。"
            },
            {
                "speaker": "Yura",
                "nebulith": "Cynel el miin ia tallarin ul alinnoven. Falun el darfenel al miin.",
                "japanese": "私たちは大地を踏む足と明晰な頭脳を信頼する。私たちに潤いの口元が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "tallarin",
                "pos": "名",
                "meaningJa": "大地を踏む足、健脚の足取り、確かな歩み",
                "meaningEn": "sure-footed step, grounded foot, sturdy stride",
                "morphemes": [
                    "tal",
                    "larin"
                ],
                "etymology": "tal(大地) + larin(足)",
                "category": "4. 人体・生理・医療",
                "example_sentence": "Vyrel el mi ia tallarin ul alinnoven uo domom.",
                "example_ja": "私は街の広場で大地を踏む足と明晰な頭脳を見守る。"
            },
            {
                "nrs": "alinnoven",
                "pos": "名",
                "meaningJa": "明晰な頭脳、澄み切った頭、冷静な思考力",
                "meaningEn": "clear head, lucid intellect, unclouded mind",
                "morphemes": [
                    "alin",
                    "noven"
                ],
                "etymology": "alin(白い) + noven(頭)",
                "category": "4. 人体・生理・医療",
                "example_sentence": "Vyrel el mi ia tallarin ul alinnoven uo domom.",
                "example_ja": "私は街の広場で大地を踏む足と明晰な頭脳を見守る。"
            },
            {
                "nrs": "darfenel",
                "pos": "名",
                "meaningJa": "潤いの口元、滑らかな語り口、澄んだ発声の口",
                "meaningEn": "eloquent mouth, fluent speech lips, gentle-spoken mouth",
                "morphemes": [
                    "dar",
                    "fenel"
                ],
                "etymology": "dar(しずく) + fenel(口)",
                "category": "4. 人体・生理・医療",
                "example_sentence": "Relen el darfenel uo domom.",
                "example_ja": "街の広場で潤いの口元がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-105",
        "batch": "Batch 27",
        "domain": "食文化・大地の恵み料理と白銀の果実酒",
        "title": "収穫の食卓と熟成の果実酒",
        "communicative_need": "根菜と穀物を煮込んだ大地の料理、山ぶどうの白い発酵果実酒、甘く熟した木の実を食卓に並べる。",
        "agent_a": {
            "name": "Sev",
            "role": "大皿を運ぶ灯守"
        },
        "agent_b": {
            "name": "Neri",
            "role": "果実酒を注ぐ採集師"
        },
        "turns": [
            {
                "speaker": "Sev",
                "nebulith": "Neran el mi ia talnerel ul alinvoril uo nerar. Relen el talvorin uo nerar.",
                "japanese": "私はカフェの食卓で大地の郷土料理と白の果実酒を味わう。カフェの食卓で大地の木の実がある。"
            },
            {
                "speaker": "Neri",
                "nebulith": "Cynel el miin ia talnerel ul alinvoril. Falun el talvorin al miin.",
                "japanese": "私たちは大地の郷土料理と白の果実酒を喜ぶ。私たちに大地の木の実が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "talnerel",
                "pos": "名",
                "meaningJa": "大地の郷土料理、根菜の滋養膳、収穫の温かい料理",
                "meaningEn": "earthy harvest meal, countryside stew dish, terrestrial home cooking",
                "morphemes": [
                    "tal",
                    "nerel"
                ],
                "etymology": "tal(大地) + nerel(料理)",
                "category": "12. 食文化・料理・飲食",
                "example_sentence": "Neran el mi ia talnerel ul alinvoril uo nerar.",
                "example_ja": "私はカフェの食卓で大地の郷土料理と白の果実酒を味わう。"
            },
            {
                "nrs": "alinvoril",
                "pos": "名",
                "meaningJa": "白の果実酒、澄んだ白ワイン、白ぶどうの発酵酒",
                "meaningEn": "white fruit wine, clear vintage cider, pale fermented nectar",
                "morphemes": [
                    "alin",
                    "voril"
                ],
                "etymology": "alin(白い) + voril(発酵果実酒)",
                "category": "12. 食文化・料理・飲食",
                "example_sentence": "Neran el mi ia talnerel ul alinvoril uo nerar.",
                "example_ja": "私はカフェの食卓で大地の郷土料理と白の果実酒を味わう。"
            },
            {
                "nrs": "talvorin",
                "pos": "名",
                "meaningJa": "大地の木の実、根菜と野の果実、里山の収穫果",
                "meaningEn": "earth-grown fruit, orchard berry, harvested ground fruit",
                "morphemes": [
                    "tal",
                    "vorin"
                ],
                "etymology": "tal(大地) + vorin(果実)",
                "category": "12. 食文化・料理・飲食",
                "example_sentence": "Relen el talvorin uo nerar.",
                "example_ja": "カフェの食卓で大地の木の実がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-106",
        "batch": "Batch 27",
        "domain": "食文化・水辺の厨房と熟練の料理人",
        "title": "運河の料理人と宵の薬草茶",
        "communicative_need": "新鮮な魚や水草を扱う水辺の厨房、森の香草を使いこなす料理人、夜に飲む安眠の煎じ茶を楽しむ。",
        "agent_a": {
            "name": "Toa",
            "role": "川魚を届ける舟守"
        },
        "agent_b": {
            "name": "Sev",
            "role": "竈に火を入れる灯守"
        },
        "turns": [
            {
                "speaker": "Toa",
                "nebulith": "Vyrel el mi ia darnerom ul velneror uo nerom. Relen el kymterin uo nerom.",
                "japanese": "私は厨房の中で水辺の厨房と森の料理人を手伝う。厨房の中で宵の安眠茶がある。"
            },
            {
                "speaker": "Sev",
                "nebulith": "Bion el miin ia darnerom ul velneror. Falun el kymterin al miin.",
                "japanese": "私たちは水辺の厨房と森の料理人を味わう。私たちに宵の安眠茶が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "darnerom",
                "pos": "名",
                "meaningJa": "水辺の厨房、清水を引いた調理室、運河沿いの炊事場",
                "meaningEn": "waterside kitchen, spring-fed galley, canal culinary room",
                "morphemes": [
                    "dar",
                    "nerom"
                ],
                "etymology": "dar(しずく) + nerom(厨房)",
                "category": "12. 食文化・料理・飲食",
                "example_sentence": "Vyrel el mi ia darnerom ul velneror uo nerom.",
                "example_ja": "私は厨房の中で水辺の厨房と森の料理人を手伝う。"
            },
            {
                "nrs": "velneror",
                "pos": "名",
                "meaningJa": "森の料理人、香草と木の実の調理師、山の料理番",
                "meaningEn": "woodland chef, herbalist cook, forest culinary master",
                "morphemes": [
                    "vel",
                    "neror"
                ],
                "etymology": "vel(木) + neror(料理人)",
                "category": "12. 食文化・料理・飲食",
                "example_sentence": "Vyrel el mi ia darnerom ul velneror uo nerom.",
                "example_ja": "私は厨房の中で水辺の厨房と森の料理人を手伝う。"
            },
            {
                "nrs": "kymterin",
                "pos": "名",
                "meaningJa": "宵の安眠茶、夜に飲む温かい煎じ茶、月見の香草茶",
                "meaningEn": "evening herbal tea, nighttime soothing brew, nocturnal infusion",
                "morphemes": [
                    "kym",
                    "terin"
                ],
                "etymology": "kym(夜) + terin(温かい煎じ茶)",
                "category": "12. 食文化・料理・飲食",
                "example_sentence": "Relen el kymterin uo nerom.",
                "example_ja": "厨房の中で宵の安眠茶がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-107",
        "batch": "Batch 27",
        "domain": "日常・木陰のカフェと白い毛皮・旅の衣",
        "title": "樹下の茶房と冬支度の衣服",
        "communicative_need": "大樹の下にある木陰のカフェ、暖かな白い毛皮の襟巻き、森を歩くための丈夫な衣服を整える。",
        "agent_a": {
            "name": "Neri",
            "role": "冬支度をする採集師"
        },
        "agent_b": {
            "name": "Yura",
            "role": "茶房で読書する写字生"
        },
        "turns": [
            {
                "speaker": "Neri",
                "nebulith": "Vyrel el mi ia velnerar ul alintenis uo nerar. Relen el velvalis uo nerar.",
                "japanese": "私は茶房の席で木陰のカフェと純白の冬毛皮を選ぶ。茶房の席で森歩きの衣がある。"
            },
            {
                "speaker": "Yura",
                "nebulith": "Cynel el miin ia velnerar ul alintenis. Falun el velvalis al miin.",
                "japanese": "私たちは木陰のカフェと純白の冬毛皮を愛用する。私たちに森歩きの衣が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "velnerar",
                "pos": "名",
                "meaningJa": "木陰のカフェ、森の茶房、樹下の憩い茶屋",
                "meaningEn": "woodland cafe, treeshade teahouse, forest coffeehouse",
                "morphemes": [
                    "vel",
                    "nerar"
                ],
                "etymology": "vel(木) + nerar(カフェ)",
                "category": "16. 日常・自然・気象",
                "example_sentence": "Vyrel el mi ia velnerar ul alintenis uo nerar.",
                "example_ja": "私は茶房の席で木陰のカフェと純白の冬毛皮を選ぶ。"
            },
            {
                "nrs": "alintenis",
                "pos": "名",
                "meaningJa": "純白の冬毛皮、白い羊毛布、柔らかな白毛皮",
                "meaningEn": "pure white fur, soft snowy fleece, alabaster pelt",
                "morphemes": [
                    "alin",
                    "tenis"
                ],
                "etymology": "alin(白い) + tenis(毛皮)",
                "category": "16. 日常・自然・気象",
                "example_sentence": "Vyrel el mi ia velnerar ul alintenis uo nerar.",
                "example_ja": "私は茶房の席で木陰のカフェと純白の冬毛皮を選ぶ。"
            },
            {
                "nrs": "velvalis",
                "pos": "名",
                "meaningJa": "森歩きの衣、草木染めの外투、樹皮繊維の衣服",
                "meaningEn": "forest cloak, botanical-dyed garment, woodland workwear",
                "morphemes": [
                    "vel",
                    "valis"
                ],
                "etymology": "vel(木) + valis(衣服)",
                "category": "16. 日常・自然・気象",
                "example_sentence": "Relen el velvalis uo nerar.",
                "example_ja": "茶房の席で森歩きの衣がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-108",
        "batch": "Batch 27",
        "domain": "植物・銀葉の枝と季節の若芽",
        "title": "月光を返す銀の葉と春の新芽",
        "communicative_need": "月や星の光を返す銀色の葉、季節の巡りを告げる新芽、白い花咲く中庭を手入れする。",
        "agent_a": {
            "name": "Neri",
            "role": "剪定を行う採集師"
        },
        "agent_b": {
            "name": "Sev",
            "role": "水やりをする灯守"
        },
        "turns": [
            {
                "speaker": "Neri",
                "nebulith": "Vymin el mi ia tynivelas ul havvelil uo velar. Relen el alinvelar uo velar.",
                "japanese": "私は中庭の花壇で銀色の葉と季節の新芽を育てる。中庭の花壇で白花の庭園がある。"
            },
            {
                "speaker": "Sev",
                "nebulith": "Vyrel el miin ia tynivelas ul havvelil. Falun el alinvelar al miin.",
                "japanese": "私たちは銀色の葉と季節の新芽を愛でる。私たちに白花の庭園が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "tynivelas",
                "pos": "名",
                "meaningJa": "銀色の葉、月光を返す銀葉、白銀の木の葉",
                "meaningEn": "silver leaf, moonlit foliage, argent-backed frond",
                "morphemes": [
                    "tyni",
                    "velas"
                ],
                "etymology": "tyni(銀色の) + velas(葉)",
                "category": "5. 生物・生態・環境",
                "example_sentence": "Vymin el mi ia tynivelas ul havvelil uo velar.",
                "example_ja": "私は中庭の花壇で銀色の葉と季節の新芽を育てる。"
            },
            {
                "nrs": "havvelil",
                "pos": "名",
                "meaningJa": "季節の新芽、春を告げる若芽、時満ちて芽吹くハーブ",
                "meaningEn": "seasonal sprout, timely spring shoot, vernal herb bud",
                "morphemes": [
                    "hav",
                    "velil"
                ],
                "etymology": "hav(時) + velil(新芽)",
                "category": "5. 生物・生態・環境",
                "example_sentence": "Vymin el mi ia tynivelas ul havvelil uo velar.",
                "example_ja": "私は中庭の花壇で銀色の葉と季節の新芽を育てる。"
            },
            {
                "nrs": "alinvelar",
                "pos": "名",
                "meaningJa": "白花の庭園、白い花が咲く庭、純白の中庭",
                "meaningEn": "white-blossom garden, alba courtyard, luminous flower garden",
                "morphemes": [
                    "alin",
                    "velar"
                ],
                "etymology": "alin(白い) + velar(庭)",
                "category": "5. 生物・生態・環境",
                "example_sentence": "Relen el alinvelar uo velar.",
                "example_ja": "中庭の花壇で白花の庭園がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-109",
        "batch": "Batch 28",
        "domain": "文芸・大地の叙事詩と白銀の鎮魂歌",
        "title": "古の叙事詩と水辺の書物",
        "communicative_need": "開拓の歴史を詠んだ大地の叙事詩、静かな森の鎮魂歌、航海と水路を記した本を紐解く。",
        "agent_a": {
            "name": "Yura",
            "role": "古写本を朗読する写字生"
        },
        "agent_b": {
            "name": "Toa",
            "role": "水路誌を聴く舟守"
        },
        "turns": [
            {
                "speaker": "Yura",
                "nebulith": "Vyrel el mi ia talcivom ul vellyren uo livar. Relen el darpamel uo livar.",
                "japanese": "私は星辰書庫で大地の叙事詩と樹海の鎮魂歌を読み解く。星辰書庫で水路の航海誌がある。"
            },
            {
                "speaker": "Toa",
                "nebulith": "Soran el miin ia talcivom ul vellyren. Falun el darpamel al miin.",
                "japanese": "私たちは大地の叙事詩と樹海の鎮魂歌を筆写する。私たちに水路の航海誌が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "talcivom",
                "pos": "名",
                "meaningJa": "大地の叙事詩、開拓の年代記詩、国土の英雄詩",
                "meaningEn": "epic of the land, terrestrial chronicle poem, foundational saga",
                "morphemes": [
                    "tal",
                    "civom"
                ],
                "etymology": "tal(大地) + civom(叙事詩)",
                "category": "15. 芸術・文化・娯楽",
                "example_sentence": "Vyrel el mi ia talcivom ul vellyren uo livar.",
                "example_ja": "私は星辰書庫で大地の叙事詩と樹海の鎮魂歌を読み解く。"
            },
            {
                "nrs": "vellyren",
                "pos": "名",
                "meaningJa": "樹海の鎮魂歌、森の挽歌、木漏れ日の祈りの歌",
                "meaningEn": "forest elegy, woodland requiem, sylvan lament",
                "morphemes": [
                    "vel",
                    "lyren"
                ],
                "etymology": "vel(木) + lyren(鎮魂歌)",
                "category": "15. 芸術・文化・娯楽",
                "example_sentence": "Vyrel el mi ia talcivom ul vellyren uo livar.",
                "example_ja": "私は星辰書庫で大地の叙事詩と樹海の鎮魂歌を読み解く。"
            },
            {
                "nrs": "darpamel",
                "pos": "名",
                "meaningJa": "水路の航海誌、水辺の記録本、泉の詩集",
                "meaningEn": "waterway manual, aquatic logbook, book of streams",
                "morphemes": [
                    "dar",
                    "pamel"
                ],
                "etymology": "dar(しずく) + pamel(本)",
                "category": "15. 芸術・文化・娯楽",
                "example_sentence": "Relen el darpamel uo livar.",
                "example_ja": "星辰書庫で水路の航海誌がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-110",
        "batch": "Batch 28",
        "domain": "芸術・星の光画と虹の分光・森の調和",
        "title": "星空の写真とプリズムの分光",
        "communicative_need": "長時間露光で写した星空の写真、水滴が作る七色の分光、森と人の美しい共生を語り合う。",
        "agent_a": {
            "name": "Sev",
            "role": "光学鏡を磨く灯守"
        },
        "agent_b": {
            "name": "Yura",
            "role": "画帖を編む写字生"
        },
        "turns": [
            {
                "speaker": "Sev",
                "nebulith": "Vyrel el mi ia vyrlyvel ul darfalos uo vorn. Relen el velsilan uo vorn.",
                "japanese": "私は光学室で星野の写真と水滴の分光を鑑賞する。光学室で緑陰の共鳴がある。"
            },
            {
                "speaker": "Yura",
                "nebulith": "Cynel el miin ia vyrlyvel ul darfalos. Falun el velsilan al miin.",
                "japanese": "私たちは星野の写真と水滴の分光を感嘆する。私たちに緑陰の共鳴が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "vyrlyvel",
                "pos": "名",
                "meaningJa": "星野の写真、天体光画、星軌跡の写し絵",
                "meaningEn": "astrophotograph, starlight plate image, celestial photo",
                "morphemes": [
                    "vyr",
                    "lyvel"
                ],
                "etymology": "vyr(星) + lyvel(写真)",
                "category": "15. 芸術・文化・娯楽",
                "example_sentence": "Vyrel el mi ia vyrlyvel ul darfalos uo vorn.",
                "example_ja": "私は光学室で星野の写真と水滴の分光を鑑賞する。"
            },
            {
                "nrs": "darfalos",
                "pos": "名",
                "meaningJa": "水滴の分光、虹のスペクトル、朝露の七色光",
                "meaningEn": "water-droplet spectrum, rainbow dispersion, dew prism light",
                "morphemes": [
                    "dar",
                    "falos"
                ],
                "etymology": "dar(しずく) + falos(分光)",
                "category": "15. 芸術・文化・娯楽",
                "example_sentence": "Vyrel el mi ia vyrlyvel ul darfalos uo vorn.",
                "example_ja": "私は光学室で星野の写真と水滴の分光を鑑賞する。"
            },
            {
                "nrs": "velsilan",
                "pos": "名",
                "meaningJa": "緑陰の共鳴、木々と風の共生、緑のハーモニー",
                "meaningEn": "woodland harmony, ecological balance, sylvan consonance",
                "morphemes": [
                    "vel",
                    "silan"
                ],
                "etymology": "vel(木) + silan(調和)",
                "category": "15. 芸術・文化・娯楽",
                "example_sentence": "Relen el velsilan uo vorn.",
                "example_ja": "光学室で緑陰の共鳴がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-111",
        "batch": "Batch 28",
        "domain": "内省・森の夢と水の記憶・聖なる畏敬",
        "title": "樹下の夢と星空への畏敬",
        "communicative_need": "木漏れ日の中で見る穏やかな夢、水面に刻まれた遠い日の記憶、星空を見上げたときの畏敬の念を語る。",
        "agent_a": {
            "name": "Yura",
            "role": "随想を綴る写字生"
        },
        "agent_b": {
            "name": "Neri",
            "role": "静かに耳を傾ける採集師"
        },
        "turns": [
            {
                "speaker": "Yura",
                "nebulith": "Vyrel el mi ia velsonir ul darsoras uo velom. Relen el vyrkefur uo velom.",
                "japanese": "私は森のほとりで木漏れ日の夢と水面の記憶を思い巡らす。森のほとりで星辰への畏敬がある。"
            },
            {
                "speaker": "Neri",
                "nebulith": "Soran el miin ia velsonir ul darsoras. Falun el vyrkefur al miin.",
                "japanese": "私たちは木漏れ日の夢と水面の記憶を書き留める。私たちに星辰への畏敬が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "velsonir",
                "pos": "名",
                "meaningJa": "木漏れ日の夢、森で見るまどろみの夢、緑陰の夢路",
                "meaningEn": "woodland dream, forest reverie, sylvan slumber vision",
                "morphemes": [
                    "vel",
                    "sonir"
                ],
                "etymology": "vel(木) + sonir(夢)",
                "category": "13. 精神・感情・内省",
                "example_sentence": "Vyrel el mi ia velsonir ul darsoras uo velom.",
                "example_ja": "私は森のほとりで木漏れ日の夢と水面の記憶を思い巡らす。"
            },
            {
                "nrs": "darsoras",
                "pos": "名",
                "meaningJa": "水面の記憶、流れに宿る思い出、しずくの記憶",
                "meaningEn": "water-borne memory, recollection of streams, rippling remembrance",
                "morphemes": [
                    "dar",
                    "soras"
                ],
                "etymology": "dar(しずく) + soras(記憶)",
                "category": "13. 精神・感情・内省",
                "example_sentence": "Vyrel el mi ia velsonir ul darsoras uo velom.",
                "example_ja": "私は森のほとりで木漏れ日の夢と水面の記憶を思い巡らす。"
            },
            {
                "nrs": "vyrkefur",
                "pos": "名",
                "meaningJa": "星辰への畏敬、天を仰ぐ崇高な思い、星空の畏敬の念",
                "meaningEn": "astral awe, reverence before the stars, cosmic wonder",
                "morphemes": [
                    "vyr",
                    "kefur"
                ],
                "etymology": "vyr(星) + kefur(畏敬の念)",
                "category": "13. 精神・感情・内省",
                "example_sentence": "Relen el vyrkefur uo velom.",
                "example_ja": "森のほとりで星辰への畏敬がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-112",
        "batch": "Batch 28",
        "domain": "精神・直感の閃きと揺るぎない心・真理",
        "title": "時の直感と大地の不動心",
        "communicative_need": "時機を見抜く鋭い直感、大地のように落ち着き払った心、清らかに澄み切った真理を探究する。",
        "agent_a": {
            "name": "Sev",
            "role": "夜の灯を守る灯守"
        },
        "agent_b": {
            "name": "Yura",
            "role": "哲学書を読む写字生"
        },
        "turns": [
            {
                "speaker": "Sev",
                "nebulith": "Vyrel el mi ia havfelyn ul talsylim uo govan. Relen el alinvyran uo govan.",
                "japanese": "私は静かな居間で時機の直感と不動の心を見つめる。静かな居間で純粋な真理がある。"
            },
            {
                "speaker": "Yura",
                "nebulith": "Cynel el miin ia havfelyn ul talsylim. Falun el alinvyran al miin.",
                "japanese": "私たちは時機の直感と不動の心を尊ぶ。私たちに純粋な真理が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "havfelyn",
                "pos": "名",
                "meaningJa": "時機の直感、好機のひらめき、瞬間の予感",
                "meaningEn": "timely intuition, flash of opportune insight, momentary foresight",
                "morphemes": [
                    "hav",
                    "felyn"
                ],
                "etymology": "hav(時) + felyn(直感)",
                "category": "13. 精神・感情・内省",
                "example_sentence": "Vyrel el mi ia havfelyn ul talsylim uo govan.",
                "example_ja": "私は静かな居間で時機の直感と不動の心を見つめる。"
            },
            {
                "nrs": "talsylim",
                "pos": "名",
                "meaningJa": "不動の心、大地のように穏やかな精神、落ち着いた心境",
                "meaningEn": "grounded mind, steadfast spirit, unshakeable composure",
                "morphemes": [
                    "tal",
                    "sylim"
                ],
                "etymology": "tal(大地) + sylim(心)",
                "category": "13. 精神・感情・内省",
                "example_sentence": "Vyrel el mi ia vyrfelyn ul talsylim uo govan.",
                "example_ja": "私は静かな居間で星光の直感と不動の心を見つめる。"
            },
            {
                "nrs": "alinvyran",
                "pos": "名",
                "meaningJa": "純粋な真理、曇りなき真実、白銀の理",
                "meaningEn": "pure truth, unblemished verity, clear philosophical truth",
                "morphemes": [
                    "alin",
                    "vyran"
                ],
                "etymology": "alin(白い) + vyran(真理)",
                "category": "13. 精神・感情・内省",
                "example_sentence": "Relen el alinvyran uo govan.",
                "example_ja": "静かな居間で純粋な真理がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-113",
        "batch": "Batch 29",
        "domain": "社会・森の民と水辺の市民・共同体の指導者",
        "title": "水辺の市民と円卓の導き手",
        "communicative_need": "森と共に生きる人々、水路の街に暮らす市民、円卓の合意をまとめる指導者の務めを話し合う。",
        "agent_a": {
            "name": "Toa",
            "role": "市民の声を届ける舟守"
        },
        "agent_b": {
            "name": "Yura",
            "role": "議事録を執る写字生"
        },
        "turns": [
            {
                "speaker": "Toa",
                "nebulith": "Vyrel el mi ia velmyren ul darpolor uo klorcalor. Relen el klornovor uo klorcalor.",
                "japanese": "私は評議の間で森の生活者と水辺の市民を尊重する。評議の間で円卓の指導者がある。"
            },
            {
                "speaker": "Yura",
                "nebulith": "Vymin el miin ia velmyren ul darpolor. Falun el klornovor al miin.",
                "japanese": "私たちは森の生活者と水辺の市民を支える。私たちに円卓の指導者が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "velmyren",
                "pos": "名",
                "meaningJa": "森の生活者、樹林と共生する人間、山の住人",
                "meaningEn": "forest dweller, woodland human, sylvan inhabitant",
                "morphemes": [
                    "vel",
                    "myren"
                ],
                "etymology": "vel(木) + myren(人間)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Vyrel el mi ia velmyren ul darpolor uo klorcalor.",
                "example_ja": "私は評議の間で森の生活者と水辺の市民を尊重する。"
            },
            {
                "nrs": "darpolor",
                "pos": "名",
                "meaningJa": "水辺の市民、運河都市の住民、港町の市民",
                "meaningEn": "waterside citizen, canal-town burgher, maritime resident",
                "morphemes": [
                    "dar",
                    "polor"
                ],
                "etymology": "dar(しずく) + polor(市民)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Vyrel el mi ia velmyren ul darpolor uo klorcalor.",
                "example_ja": "私は評議の間で森の生活者と水辺の市民を尊重する。"
            },
            {
                "nrs": "klornovor",
                "pos": "名",
                "meaningJa": "円卓の指導者、合議を導く議長、輪の調停役",
                "meaningEn": "roundtable leader, council moderator, guiding convener",
                "morphemes": [
                    "klor",
                    "novor"
                ],
                "etymology": "klor(円) + novor(指導者)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Relen el klornovor uo klorcalor.",
                "example_ja": "評議の間で円卓の指導者がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-114",
        "batch": "Batch 29",
        "domain": "社会・大地の働き手と基本の権利・法典",
        "title": "耕作の働き手と大地の基本法",
        "communicative_need": "大地を耕し石を積む労働者、すべての人に保障された基本の権利、水路と大地を守る法を確かめる。",
        "agent_a": {
            "name": "Sev",
            "role": "規約を読み上げる灯守"
        },
        "agent_b": {
            "name": "Neri",
            "role": "農地の境界を確認する採集師"
        },
        "turns": [
            {
                "speaker": "Sev",
                "nebulith": "Vymin el mi ia taldolor ul taltarin uo domom. Relen el dartaros uo domom.",
                "japanese": "私は街の集会所で大地の働き手と基本の生存権を遵守する。街の集会所で水利の法典がある。"
            },
            {
                "speaker": "Neri",
                "nebulith": "Soran el miin ia taldolor ul taltarin. Falun el dartaros al miin.",
                "japanese": "私たちは大地の働き手と基本の生存権を明文化する。私たちに水利の法典が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "taldolor",
                "pos": "名",
                "meaningJa": "大地の働き手、農耕と石工の労働者、現場の職人",
                "meaningEn": "land worker, terrestrial artisan, field laborer",
                "morphemes": [
                    "tal",
                    "dolor"
                ],
                "etymology": "tal(大地) + dolor(労働者)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Vymin el mi ia taldolor ul taltarin uo domom.",
                "example_ja": "私は街の集会所で大地の働き手と基本の生存権を遵守する。"
            },
            {
                "nrs": "taltarin",
                "pos": "名",
                "meaningJa": "基本の生存権、大地に生きる権利、固有の市民権",
                "meaningEn": "fundamental right, birthright of the land, inherent civic right",
                "morphemes": [
                    "tal",
                    "tarin"
                ],
                "etymology": "tal(大地) + tarin(権利)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Vymin el mi ia taldolor ul taltarin uo domom.",
                "example_ja": "私は街の集会所で大地の働き手と基本の生存権を遵守する。"
            },
            {
                "nrs": "dartaros",
                "pos": "名",
                "meaningJa": "水利の法典、水路と水源の法規、水辺の掟",
                "meaningEn": "water law, maritime and canal code, hydrological statute",
                "morphemes": [
                    "dar",
                    "taros"
                ],
                "etymology": "dar(しずく) + taros(法)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Relen el dartaros uo domom.",
                "example_ja": "街の集会所で水利の法典がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-115",
        "batch": "Batch 29",
        "domain": "人間関係・星の友情と無二の親友・感謝",
        "title": "星下の友情と白銀の感謝",
        "communicative_need": "同じ星を見上げて結んだ友情、苦楽を共にする親友、心からの清らかな感謝を言葉にして伝える。",
        "agent_a": {
            "name": "Toa",
            "role": "航海の無事を祝う舟守"
        },
        "agent_b": {
            "name": "Sev",
            "role": "迎え火を焚いた灯守"
        },
        "turns": [
            {
                "speaker": "Toa",
                "nebulith": "Cynel el mi ia vyrcynas ul talcynor uo larar. Relen el alincynur uo larar.",
                "japanese": "私は港の灯台下で星下の友情と盤石の親友を分かち合う。港の灯台下で白銀の謝意がある。"
            },
            {
                "speaker": "Sev",
                "nebulith": "Soran el miin ia vyrcynas ul talcynor. Falun el alincynur al miin.",
                "japanese": "私たちは星下の友情と盤石の親友を手紙に記す。私たちに白銀の謝意が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "vyrcynas",
                "pos": "名",
                "meaningJa": "星下の友情、変わらぬ友愛、星に誓う絆",
                "meaningEn": "starlit friendship, enduring camaraderie, astral bond of amity",
                "morphemes": [
                    "vyr",
                    "cynas"
                ],
                "etymology": "vyr(星) + cynas(友情)",
                "category": "13. 精神・感情・内省",
                "example_sentence": "Cynel el mi ia vyrcynas ul talcynor uo larar.",
                "example_ja": "私は港の灯台下で星下の友情と盤石の親友を分かち合う。"
            },
            {
                "nrs": "talcynor",
                "pos": "名",
                "meaningJa": "盤石の親友、生涯の盟友、頼れる無二の友",
                "meaningEn": "steadfast confidant, lifelong bosom friend, grounded companion",
                "morphemes": [
                    "tal",
                    "cynor"
                ],
                "etymology": "tal(大地) + cynor(親友)",
                "category": "13. 精神・感情・内省",
                "example_sentence": "Cynel el mi ia vyrcynas ul talcynor uo larar.",
                "example_ja": "私は港の灯台下で星下の友情と盤石の親友を分かち合う。"
            },
            {
                "nrs": "alincynur",
                "pos": "名",
                "meaningJa": "白銀の謝意、清らかな感謝の念、無垢の礼意",
                "meaningEn": "pure gratitude, wholehearted thanks, sincere appreciation",
                "morphemes": [
                    "alin",
                    "cynur"
                ],
                "etymology": "alin(白い) + cynur(感謝)",
                "category": "13. 精神・感情・内省",
                "example_sentence": "Relen el alincynur uo larar.",
                "example_ja": "港の灯台下で白銀の謝意がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-116",
        "batch": "Batch 29",
        "domain": "時間・移ろう季節と新しい時代・選択肢",
        "title": "緑の季節と星見の時代",
        "communicative_need": "若葉が萌える緑の季節、天文学と平和が花開く新しい時代、未来に向けた賢明な選択肢を語り合う。",
        "agent_a": {
            "name": "Yura",
            "role": "年代記を編む写字生"
        },
        "agent_b": {
            "name": "Neri",
            "role": "種籾を選別する採集師"
        },
        "turns": [
            {
                "speaker": "Yura",
                "nebulith": "Vyrel el mi ia velhavas ul vyrhavel uo livar. Relen el alinsevur uo livar.",
                "japanese": "私は書庫のテラスで新緑の季節と星見の時代を展望する。書庫のテラスで明快な選択肢がある。"
            },
            {
                "speaker": "Neri",
                "nebulith": "Soran el miin ia velhavas ul vyrhavel. Falun el alinsevur al miin.",
                "japanese": "私たちは新緑の季節と星見の時代を記録する。私たちに明快な選択肢が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "velhavas",
                "pos": "名",
                "meaningJa": "新緑の季節、草木が茂る時節、森の萌芽期",
                "meaningEn": "verdant season, woodland growing season, foliage time",
                "morphemes": [
                    "vel",
                    "havas"
                ],
                "etymology": "vel(木) + havas(季節)",
                "category": "1. 天文・宇宙・時空",
                "example_sentence": "Vyrel el mi ia velhavas ul vyrhavel uo livar.",
                "example_ja": "私は書庫のテラスで新緑の季節と星見の時代を展望する。"
            },
            {
                "nrs": "vyrhavel",
                "pos": "名",
                "meaningJa": "星見の時代、天文と航海の時代、星辰の世紀",
                "meaningEn": "astral era, age of stargazing, celestial epoch",
                "morphemes": [
                    "vyr",
                    "havel"
                ],
                "etymology": "vyr(星) + havel(時代)",
                "category": "1. 天文・宇宙・時空",
                "example_sentence": "Vyrel el mi ia velhavas ul vyrhavel uo livar.",
                "example_ja": "私は書庫のテラスで新緑の季節と星見の時代を展望する。"
            },
            {
                "nrs": "alinsevur",
                "pos": "名",
                "meaningJa": "明快な選択肢、曇りなき善後策、最良の選択",
                "meaningEn": "clear alternative, transparent option, honorable choice",
                "morphemes": [
                    "alin",
                    "sevur"
                ],
                "etymology": "alin(白い) + sevur(選択肢)",
                "category": "1. 天文・宇宙・時空",
                "example_sentence": "Relen el alinsevur uo livar.",
                "example_ja": "書庫のテラスで明快な選択肢がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-117",
        "batch": "Batch 30",
        "domain": "自然・水辺の朝日と晴天の昼・森の夕暮れ",
        "title": "朝日の水鏡と木立の夕映え",
        "communicative_need": "水面に昇る清々しい朝、白く輝く真昼の陽気、木立の間から差す穏やかな夕暮れを一日の巡りとして描く。",
        "agent_a": {
            "name": "Yura",
            "role": "日課表を記す写字生"
        },
        "agent_b": {
            "name": "Toa",
            "role": "朝舟を出す舟守"
        },
        "turns": [
            {
                "speaker": "Yura",
                "nebulith": "Vyrel el mi ia talvalar ul alinsovil uo daron. Relen el velkylas uo daron.",
                "japanese": "私は湖畔の桟橋で大地の夜明けと白光の真昼を見渡す。湖畔の桟橋で木立の夕暮れがある。"
            },
            {
                "speaker": "Toa",
                "nebulith": "Cynel el miin ia talvalar ul alinsovil. Falun el velkylas al miin.",
                "japanese": "私たちは大地の夜明けと白光の真昼を愛でる。私たちに木立の夕暮れが輝く。"
            }
        ],
        "words": [
            {
                "nrs": "talvalar",
                "pos": "名",
                "meaningJa": "大地の夜明け、野に昇る朝、地平の朝ぼらけ",
                "meaningEn": "terrestrial morning, dawn over the land, daybreak on the plains",
                "morphemes": [
                    "tal",
                    "valar"
                ],
                "etymology": "tal(大地) + valar(朝)",
                "category": "16. 日常・自然・気象",
                "example_sentence": "Vyrel el mi ia talvalar ul alinsovil uo daron.",
                "example_ja": "私は湖畔の桟橋で大地の夜明けと白光の真昼を見渡す。"
            },
            {
                "nrs": "alinsovil",
                "pos": "名",
                "meaningJa": "白光の真昼、晴れ渡る昼下がり、明るい日中",
                "meaningEn": "bright midday, clear sunlit daytime, radiant noon",
                "morphemes": [
                    "alin",
                    "sovil"
                ],
                "etymology": "alin(白い) + sovil(昼)",
                "category": "16. 日常・自然・気象",
                "example_sentence": "Vyrel el mi ia talvalar ul alinsovil uo daron.",
                "example_ja": "私は湖畔の桟橋で大地の夜明けと白光の真昼を見渡す。"
            },
            {
                "nrs": "velkylas",
                "pos": "名",
                "meaningJa": "木立の夕暮れ、森に降りる夕べ、樹影の黄昏",
                "meaningEn": "forest evening, woodland twilight, sylvan dusk",
                "morphemes": [
                    "vel",
                    "kylas"
                ],
                "etymology": "vel(木) + kylas(夕)",
                "category": "16. 日常・自然・気象",
                "example_sentence": "Relen el velkylas uo daron.",
                "example_ja": "湖畔の桟橋で木立の夕暮れがある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-118",
        "batch": "Batch 30",
        "domain": "自然・水面に映る太陽と大地の月・聖火",
        "title": "水鏡の太陽と地平の満月",
        "communicative_need": "水面にきらめく太陽の光、地平線から大きく昇る月、炉で赤々と燃える清浄な火を讃える。",
        "agent_a": {
            "name": "Sev",
            "role": "聖火を灯す灯守"
        },
        "agent_b": {
            "name": "Toa",
            "role": "夕凪の櫂を休める舟守"
        },
        "turns": [
            {
                "speaker": "Sev",
                "nebulith": "Vyrel el mi ia darzohar ul taltynes uo govan. Relen el alinpyris uo govan.",
                "japanese": "私は湖畔の広間で水鏡の太陽と地平の満月を仰ぎ見る。湖畔の広間で清浄な白炎がある。"
            },
            {
                "speaker": "Toa",
                "nebulith": "Vymin el miin ia darzohar ul taltynes. Falun el alinpyris al miin.",
                "japanese": "私たちは水鏡の太陽と地平の満月を守り継ぐ。私たちに清浄な白炎が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "darzohar",
                "pos": "名",
                "meaningJa": "水鏡の太陽、水面に煌めく日輪、湖上の陽光",
                "meaningEn": "water-mirrored sun, sunlight on the water, reflected solar disc",
                "morphemes": [
                    "dar",
                    "zohar"
                ],
                "etymology": "dar(しずく) + zohar(太陽)",
                "category": "16. 日常・自然・気象",
                "example_sentence": "Vyrel el mi ia darzohar ul taltynes uo govan.",
                "example_ja": "私は湖畔の広間で水鏡の太陽と地平の満月を仰ぎ見る。"
            },
            {
                "nrs": "taltynes",
                "pos": "名",
                "meaningJa": "地平の満月、大地を照らす月、野に昇る月輪",
                "meaningEn": "horizon moon, earth-lighting moon, low harvest moon",
                "morphemes": [
                    "tal",
                    "tynes"
                ],
                "etymology": "tal(大地) + tynes(月)",
                "category": "16. 日常・自然・気象",
                "example_sentence": "Vyrel el mi ia darzohar ul taltynes uo govan.",
                "example_ja": "私は湖畔の広間で水鏡の太陽と地平の満月を仰ぎ見る。"
            },
            {
                "nrs": "alinpyris",
                "pos": "名",
                "meaningJa": "清浄な白炎、澄み切った炉火、聖なる白い炎",
                "meaningEn": "pure white flame, clean hearth fire, clarified blaze",
                "morphemes": [
                    "alin",
                    "pyris"
                ],
                "etymology": "alin(白い) + pyris(火)",
                "category": "16. 日常・自然・気象",
                "example_sentence": "Relen el alinpyris uo govan.",
                "example_ja": "湖畔の広間で清浄な白炎がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-119",
        "batch": "Batch 30",
        "domain": "宇宙・深淵の彼方と銀河団・黒孔の観測",
        "title": "星々の銀河団と深淵の天体図",
        "communicative_need": "星々が渦巻く銀河団、光さえ吸い込む深淵の黒孔、果てしない宇宙の深淵を天体図に描き込む。",
        "agent_a": {
            "name": "Yura",
            "role": "星図を完成させる写字生"
        },
        "agent_b": {
            "name": "Sev",
            "role": "大望遠鏡を操る灯守"
        },
        "turns": [
            {
                "speaker": "Yura",
                "nebulith": "Vyrel el mi ia vyrkyrom ul klorkyron uo livar. Relen el kymkyrim uo livar.",
                "japanese": "私は天文台の最上階で恒星の銀河団と降着円盤の黒孔を観測する。天文台の最上階で常夜の深淵がある。"
            },
            {
                "speaker": "Sev",
                "nebulith": "Soran el miin ia vyrkyrom ul klorkyron. Falun el kymkyrim al miin.",
                "japanese": "私たちは恒星の銀河団と降着円盤の黒孔を星図に刻む。私たちに常夜の深淵が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "vyrkyrom",
                "pos": "名",
                "meaningJa": "恒星の銀河団、星々が集う大星団、輝く銀河の群れ",
                "meaningEn": "stellar galaxy cluster, luminous galactic group, star-dense supercluster",
                "morphemes": [
                    "vyr",
                    "kyrom"
                ],
                "etymology": "vyr(星) + kyrom(銀河団)",
                "category": "1. 天文・宇宙・時空",
                "example_sentence": "Vyrel el mi ia vyrkyrom ul klorkyron uo livar.",
                "example_ja": "私は天文台の最上階で恒星の銀河団と降着円盤の黒孔を観測する。"
            },
            {
                "nrs": "klorkyron",
                "pos": "名",
                "meaningJa": "降着円盤の黒孔、光環を伴うブラックホール、円環の暗黒星",
                "meaningEn": "ringed black hole, accretion-ring singularity, annular dark star",
                "morphemes": [
                    "klor",
                    "kyron"
                ],
                "etymology": "klor(円) + kyron(黒孔)",
                "category": "1. 天文・宇宙・時空",
                "example_sentence": "Vyrel el mi ia vyrkyrom ul klorkyron uo livar.",
                "example_ja": "私は天文台の最上階で恒星の銀河団と降着円盤の黒孔を観測する。"
            },
            {
                "nrs": "kymkyrim",
                "pos": "名",
                "meaningJa": "常夜の深淵、外宇宙の暗黒空間、果てなき深宇宙",
                "meaningEn": "nocturnal deep space, abyssal cosmic void, outer dark expanse",
                "morphemes": [
                    "kym",
                    "kyrim"
                ],
                "etymology": "kym(夜) + kyrim(深淵)",
                "category": "1. 天文・宇宙・時空",
                "example_sentence": "Relen el kymkyrim uo livar.",
                "example_ja": "天文台の最上階で常夜の深淵がある。"
            }
        ]
    },
    {
        "scenario_id": "CANON-CONV-120",
        "batch": "Batch 30",
        "domain": "総括・星辰の書庫と平和の灯・未来への記録",
        "title": "白銀の書庫と全百二十話の完結",
        "communicative_need": "白銀に輝く星辰書庫、大地に根ざした恒久の安寧、そして未来へ手渡す星辰の記述文を讃えて全120話を結ぶ。",
        "agent_a": {
            "name": "Yura",
            "role": "全巻の奥付を記す写字生"
        },
        "agent_b": {
            "name": "Sev",
            "role": "書庫の常夜灯を守る灯守"
        },
        "turns": [
            {
                "speaker": "Yura",
                "nebulith": "Vymin el mi ia alinlivar ul talsirar uo livar. Relen el alinzevil uo livar.",
                "japanese": "私は星辰書庫の中央で白銀の星辰書庫と大地の恒久平和を守り伝える。星辰書庫の中央で清書された記述文がある。"
            },
            {
                "speaker": "Sev",
                "nebulith": "Soran el miin ia alinlivar ul talsirar. Falun el alinzevil al miin.",
                "japanese": "私たちは白銀の星辰書庫と大地の恒久平和を完結させる。私たちに清書された記述文が輝く。"
            }
        ],
        "words": [
            {
                "nrs": "alinlivar",
                "pos": "名",
                "meaningJa": "白銀の星辰書庫、純白の大図書館、清らかな典籍殿",
                "meaningEn": "white astral repository, alabaster grand archive, pure library hall",
                "morphemes": [
                    "alin",
                    "livar"
                ],
                "etymology": "alin(白い) + livar(星辰書庫)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Vymin el mi ia alinlivar ul talsirar uo livar.",
                "example_ja": "私は星辰書庫の中央で白銀の星辰書庫と大地の恒久平和を守り伝える。"
            },
            {
                "nrs": "talsirar",
                "pos": "名",
                "meaningJa": "大地の恒久平和、揺るぎない国土の安寧、盤石の平和",
                "meaningEn": "terrestrial peace, enduring peace of the land, grounded tranquility",
                "morphemes": [
                    "tal",
                    "sirar"
                ],
                "etymology": "tal(大地) + sirar(安寧)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Vymin el mi ia alinlivar ul talsirar uo livar.",
                "example_ja": "私は星辰書庫の中央で白銀の星辰書庫と大地の恒久平和を守り伝える。"
            },
            {
                "nrs": "alinzevil",
                "pos": "名",
                "meaningJa": "清書された記述文、一点の曇りなき正本記述、完成された星辰譜",
                "meaningEn": "fair-copied celestial script, immaculate canonical notation, purely transcribed scroll",
                "morphemes": [
                    "alin",
                    "zevil"
                ],
                "etymology": "alin(白い) + zevil(星辰記述文)",
                "category": "14. コミュニケーション・言語・社会",
                "example_sentence": "Relen el alinzevil uo livar.",
                "example_ja": "星辰書庫の中央で清書された記述文がある。"
            }
        ]
    }
]


def build_and_verify_canonical_compounds(write_files: bool = True) -> dict:
    inventory = load_canonical_inventory()
    canon_by_nrs = {r["nrs"].lower(): r for r in inventory["canon"]}
    scenarios_by_id = {s["scenario_id"]: [s] for s in CURATED_SCENARIOS}

    # Load legacy pending candidates for explicit remediation traceability mapping
    legacy_ledger = json.loads((ROOT / "data/emergent_lexicon_audit.json").read_text(encoding="utf-8"))
    legacy_candidates = legacy_ledger.get("candidates", [])
    legacy_everyday = [c for c in legacy_candidates if str(c.get("scenario_id", "")).startswith("CONV-")]

    existing_ext = inventory["extensions"]
    max_ext_id = max((e.get("id", 0) for e in existing_ext), default=30300)
    next_id = max(max_ext_id + 1, 31001)

    candidates = []
    scenarios_clean = []
    remapping_table = []

    word_idx = 0
    for scen in CURATED_SCENARIOS:
        scen_copy = {
            "scenario_id": scen["scenario_id"],
            "batch": scen.get("batch", "Batch 1"),
            "domain": scen["domain"],
            "title": scen["title"],
            "communicative_need": scen["communicative_need"],
            "agent_a": scen["agent_a"],
            "agent_b": scen["agent_b"],
            "turns": scen["turns"],
        }
        scenarios_clean.append(scen_copy)

        for w in scen["words"]:
            candidate = dict(w)
            candidate["id"] = next_id
            candidate["batch"] = scen.get("batch", "Batch 1")
            candidate["scenario_id"] = scen["scenario_id"]
            candidate["domain"] = scen["domain"]
            candidate["constituentEntries"] = [
                {
                    "id": canon_by_nrs[m]["id"],
                    "nrs": m,
                    "pos": canon_by_nrs[m]["pos"],
                    "meaningJa": canon_by_nrs[m]["meaningJa"]
                }
                for m in candidate["morphemes"]
            ]

            # Link traceability to legacy pending everyday candidate
            if word_idx < len(legacy_everyday):
                legacy_row = legacy_everyday[word_idx]
                candidate["remediatesLegacyCandidateId"] = legacy_row["id"]
                remapping_table.append({
                    "canonicalCompoundId": next_id,
                    "canonicalNrs": candidate["nrs"],
                    "canonicalMorphemes": candidate["morphemes"],
                    "canonicalMeaningJa": candidate["meaningJa"],
                    "remediatedLegacyId": legacy_row["id"],
                    "legacyNrs": legacy_row["nrs"],
                    "legacyMorphemes": legacy_row.get("morphemes", [])
                })
            word_idx += 1

            res = validate_candidate_entry(candidate, scenarios_by_id, inventory)
            if not res["valid"]:
                raise ValueError(f"Validation failed for {w['nrs']}: {res['flags']}")
            candidate["speakers"] = res["speakers"]
            candidate["auditFlags"] = res["flags"]
            candidates.append(candidate)
            next_id += 1

    batch_report = audit_candidate_batch(candidates, scenarios_clean)
    if batch_report["verdict"] != "ZERO_FLAGS_VERIFIED":
        raise ValueError(f"Batch audit reported flags: {batch_report['flagCounts']}")

    dataset = {
        "schemaVersion": "1.1.0",
        "title": "Nebulith Verified Canonical Compound Vocabulary (Batches 1-30)",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "source": "data/lexicon.json",
        "validator": "tools/canonical_compound_validator.py",
        "summary": {
            "totalEntries": len(candidates),
            "totalScenarios": len(scenarios_clean),
            "batches": [f"Batch {i}" for i in range(1, 31)],
            "auditFlagCount": 0,
            "allConstituentsStandalone": True,
            "twoSpeakerReuseVerified": True,
            "remediatedLegacyCount": len(remapping_table)
        },
        "remappingTable": remapping_table,
        "scenarios": scenarios_clean,
        "entries": candidates
    }

    if write_files:
        VERIFIED_COMPOUNDS_PATH.parent.mkdir(parents=True, exist_ok=True)
        VERIFIED_COMPOUNDS_PATH.write_text(
            json.dumps(dataset, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8"
        )
        BATCH_AUDIT_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        BATCH_AUDIT_REPORT_PATH.write_text(
            json.dumps(batch_report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8"
        )

    return {"dataset": dataset, "auditReport": batch_report}


if __name__ == "__main__":
    out = build_and_verify_canonical_compounds(write_files=True)
    print(json.dumps({
        "verdict": out["auditReport"]["verdict"],
        "counts": out["auditReport"]["counts"],
        "flagCounts": out["auditReport"]["flagCounts"]
    }, ensure_ascii=False, indent=2))
