# tools/apply_lexicon_tunings.py
"""
Applies the 11 targeted core-root tunings to Nebulith Master Lexicon v22.1.
Regenerates:
  1. docs/Nebulith Master Lexicon.md
  2. data/lexicon.json
  3. data/lexicon.csv
  4. data/StaticLexicon.kt
"""
import json
import csv

CATEGORIES_ORDER = [
    "1. 天体・宇宙力学・光",
    "2. 数理・幾何・計測",
    "3. 情報・計算機・通信",
    "4. 生命・生体・医療",
    "5. 自然地形・地質・鉱物",
    "6. 気象・大気・水域",
    "7. 植物・生態・農耕",
    "8. 動物・生物種・共生",
    "9. 統治・社会・法・共同体",
    "10. 経済・交易・工芸・労働",
    "11. 建築・都市・住空間",
    "12. 食・飲料・調理・食具",
    "13. 衣飾・携行具・日常品",
    "14. 精神・哲学・感情・芸術",
    "15. 性質・状態・色彩・感触",
    "16. 動作・動態・時空・方向副詞"
]

cat_descriptions = {
    "1. 天体・宇宙力学・光": "恒星、惑星、軌道力学、重力場、放射光、宇宙論",
    "2. 数理・幾何・計測": "理論数学、幾何学、次元、定数、公理、尺度",
    "3. 情報・計算機・通信": "計算機、コード構文、暗号、通信網、データ構造、記憶",
    "4. 生命・生体・医療": "生命現象、解剖構造、器官組織、脈動、治癒、薬理",
    "5. 自然地形・地質・鉱物": "大地、山岳、岩石、結晶鉱物、地層、地下洞窟",
    "6. 気象・大気・水域": "大気循環、風系、雲雪、海洋、水系、気象変動",
    "7. 植物・生態・農耕": "樹木、草花、種子、生態系、土壌、農耕栽培",
    "8. 動物・生物種・共生": "野生動物、鳥類、水棲生物、昆虫、生態共生",
    "9. 統治・社会・法・共同体": "法規範、評議会、市民共同体、誓約、身分同盟",
    "10. 経済・交易・工芸・労働": "市場経済、貨幣、交易路、冶金鍛造、手織機、職人技",
    "11. 建築・都市・住空間": "家屋、建築構造、門柱、都市区画、広場、居住基盤",
    "12. 食・飲料・調理・食具": "穀物、主食、温煮料理、発酵酒、茶器、食卓具",
    "13. 衣飾・携行具・日常品": "被服、布地、帯紐、携帯鞄、日用具、灯火、筆記具",
    "14. 精神・哲学・感情・芸術": "意識、思索、美学、詩歌旋律、情動、記憶遺産",
    "15. 性質・状態・色彩・感触": "星彩色彩、物性触感、状態属性、対極性質",
    "16. 動作・動態・時空・方向副詞": "基本動詞、時空概念、3次元方向副詞体系（語幹+-u）"
}

from tune_confusing_heteronyms import TUNING_MAP

with open("data/lexicon.json", "r", encoding="utf-8") as f:
    vocab = json.load(f)["vocabulary"]

tuned_entries = []
for w in vocab:
    root = w["nrs"]
    cat = w["category"]
    ipa = w["ipa"]
    pos = w["pos"]
    ja = w["meaningJa"]
    en = w["meaningEn"]
    note = w["notes"]
    
    if root in TUNING_MAP:
        new_root, new_ipa, new_note = TUNING_MAP[root]
        root = new_root
        ipa = new_ipa
        note = new_note
        
    tuned_entries.append((cat, root, ipa, pos, ja, en, note))

def sort_key(entry):
    cat = entry[0]
    cat_idx = CATEGORIES_ORDER.index(cat) if cat in CATEGORIES_ORDER else 99
    return (cat_idx, entry[1])

tuned_entries.sort(key=sort_key)
total_count = len(tuned_entries)
assert total_count == 1008

from collections import Counter
cat_counts = Counter(e[0] for e in tuned_entries)

# 1. Generate Markdown: docs/Nebulith Master Lexicon.md
md_lines = [
    "# Nebulith Master Lexicon (星石語 統御語彙大系)",
    "",
    "> **Version**: 22.1 (Tuned & Harmonized - 1,008 Master Roots across 16 Categories)  ",
    "> **Design Principle**: Complete Purge of Earth Borrowings, De-confused Core Roots & Organic Irregularity  ",
    f"> **Progress**: {total_count} / 1000 roots ({total_count / 10:.1f}%) [GOAL ACHIEVED]  ",
    "> **Phonetic Base**: Sonorous vowels (a, e, i, o, u, y), liquid semivowels (r, l, v, w, j), resonant nasals (m, n), accented by restrained stops & fricatives (p, b, t, d, k, g, f, s, z, h). Strict exclusion of q, x.",
    "",
    "---",
    "",
    "## 16-Domain Category Overview (全16領域構成)",
    "",
    "| ID | カテゴリー名 (Domain) | 語彙数 (Words) | 構成比 | 概要 |",
    "|---|---|---|---|---|"
]

for idx, cat in enumerate(CATEGORIES_ORDER, 1):
    count = cat_counts[cat]
    pct = (count / total_count) * 100
    desc = cat_descriptions.get(cat, "")
    md_lines.append(f"| {idx} | **{cat}** | {count}語 | {pct:.1f}% | {desc} |")
    
md_lines.extend([
    "",
    "---",
    "",
    "## 語彙目録 (Master Vocabulary Entries - 1,008 Roots)",
    ""
])

current_cat = None
for idx, (cat, root, ipa, pos, ja, en, note) in enumerate(tuned_entries, 1):
    if cat != current_cat:
        current_cat = cat
        md_lines.extend([
            f"### {current_cat} ({cat_counts[current_cat]}語)",
            "",
            "| ID | 語根 (NRS) | IPA | 品詞 | 日本語意味 | 英語意味 | 語源・備考 |",
            "|---|---|---|---|---|---|---|"
        ])
    md_lines.append(f"| {idx} | **{root}** | `{ipa}` | {pos} | {ja} | {en} | {note} |")
    
with open("docs/Nebulith Master Lexicon.md", "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines) + "\n")
print("Successfully written to docs/Nebulith Master Lexicon.md!")

# 2. Generate JSON: data/lexicon.json
json_vocab = []
for idx, (cat, root, ipa, pos, ja, en, note) in enumerate(tuned_entries, 1):
    json_vocab.append({
        "id": idx,
        "category": cat,
        "nrs": root,
        "ipa": ipa,
        "pos": pos,
        "meaningJa": ja,
        "meaningEn": en,
        "notes": note
    })
    
json_obj = {
    "version": "22.1",
    "language": "Nebulith",
    "languageJa": "星石語 (Nebulith)",
    "updatedAt": "2026-10-15",
    "status": "Grand Milestone 1000 Harmonized (v22.1: 1,008 roots across 16 categories with tuned heteronyms)",
    "targetGoal": 1000,
    "currentProgressPercent": round((total_count / 1000) * 100, 1),
    "totalEntries": total_count,
    "categories": [
        {"id": i + 1, "name": c, "wordsCount": cat_counts[c], "description": cat_descriptions.get(c, "")}
        for i, c in enumerate(CATEGORIES_ORDER)
    ],
    "phonology": {
        "vowels": ["a", "e", "i", "o", "u", "y"],
        "diphthongs": ["ai", "ei", "au", "oi"],
        "consonants": ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "r", "s", "t", "v", "w", "z", "'"],
        "excluded": ["q", "x"]
    },
    "grammar": {
        "cases": 8,
        "verbStems": "-an (active), -en (stative), -in (inchoative), -on (perfective), -un (habitual), with organic irregular/archaic roots",
        "directionalAdverbs": "Root + -u (e.g., kymdenu = westward, vorasu = forward, valku = frequently), preserving fused particles (forvis, kural, tyro)"
    },
    "vocabulary": json_vocab
}

with open("data/lexicon.json", "w", encoding="utf-8") as f:
    json.dump(json_obj, f, ensure_ascii=False, indent=2)
print(f"Successfully written {total_count} entries to data/lexicon.json!")

# 3. Generate CSV: data/lexicon.csv
with open("data/lexicon.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "category", "nrs", "ipa", "pos", "meaningJa", "meaningEn", "notes"])
    for idx, (cat, root, ipa, pos, ja, en, note) in enumerate(tuned_entries, 1):
        writer.writerow([idx, cat, root, ipa, pos, ja, en, note])
print("Successfully written to data/lexicon.csv!")

# 4. Generate Kotlin: data/StaticLexicon.kt
kt_lines = [
    "package com.nebulith.data",
    "",
    "/**",
    " * Autogenerated Static Lexicon for Nebulith (v22.1 - Tuned & Harmonized)",
    f" * Total vetted master entries: {total_count}",
    f" * Reorganized across 16 categories",
    " */",
    "data class LexiconEntry(",
    "    val id: Int,",
    "    val category: String,",
    "    val nrs: String,",
    "    val ipa: String,",
    "    val pos: String,",
    "    val meaningJa: String,",
    "    val meaningEn: String,",
    "    val notes: String",
    ")",
    "",
    "object StaticLexicon {",
    f"    const val VERSION = \"22.1\"",
    f"    const val TOTAL_ENTRIES = {total_count}",
    "",
    "    val entries: List<LexiconEntry> = listOf("
]

for idx, (cat, root, ipa, pos, ja, en, note) in enumerate(tuned_entries, 1):
    safe_ja = ja.replace('"', '\\"')
    safe_en = en.replace('"', '\\"')
    safe_note = note.replace('"', '\\"')
    kt_lines.append(
        f'        LexiconEntry({idx}, "{cat}", "{root}", "{ipa}", "{pos}", "{safe_ja}", "{safe_en}", "{safe_note}"),'
    )
    
kt_lines.extend([
    "    )",
    "}"
])

with open("data/StaticLexicon.kt", "w", encoding="utf-8") as f:
    f.write("\n".join(kt_lines) + "\n")
print("Successfully written to data/StaticLexicon.kt!")
