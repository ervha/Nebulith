# tools/apply_naturalistic_refactor.py
"""
Applies the Naturalistic Conlang Refactoring (v23.0) to Nebulith Master Lexicon:
- De-couples robotic lego compounds in tal*, vel*, ner*, dom*, fal*, fer*
- Implements Ablaut (vowel gradation: a -> o -> u -> e -> i -> y)
- Implements historical consonant/nasal assimilation (mk -> nk, lp -> lb, etc.)
- Grants autonomous archaic roots to daily foundational items (plate, spoon, bread, desk, horn, claw, etc.)
- Completely purges all potential false cognates with Earth languages (table, salz, domus, mirror, spike, etc.)
- Maintains exact total root count: 1,008 roots across 16 categories
- Regenerates:
  1. docs/Nebulith Master Lexicon.md
  2. data/lexicon.json
  3. data/lexicon.csv
  4. data/StaticLexicon.kt
"""
import json
import csv
from collections import Counter

REFACTOR_MAP = {
    # 1. DOM* FAMILY (Architecture / Urban / Civic)
    "dom": ("vorn", "/vorn/", "奥室・内室を表す星辰古語幹。ラテン語domus・英語domesticと完全分離"),
    "domar": ("govan", "/govan/", "住処・炉床・定住地を表す原初語幹。ラテン語domusと完全分離"),
    "domkor": ("dankor", "/dankor/", "歴史的鼻音同化（dom-kor -> dankor: 市民、定住住民）"),
    "domkorv": ("dankorv", "/dankorv/", "歴史的鼻音同化（dom-korv -> dankorv: 元首、執政官）"),
    "domkar": ("dankar", "/dankar/", "歴史的鼻音同化（dom-kar -> dankar: 基礎、建築石礎）"),
    "domkarn": ("dankarn", "/dankarn/", "歴史的鼻音同化（dom-karn -> dankarn: 厩舎、飼育棟）"),
    "domtas": ("vostir", "/vostir/", "昇降傾斜を表す独立建築語幹。英語stairs・独語treppeと完全分離"),
    "domlik": ("kulmon", "/kulmon/", "直立支持石柱を表す巨石建築語幹。英語pillar・columnaと完全分離"),
    "domparn": ("borparn", "/borparn/", "横架材・天井梁を表す構造語幹"),
    "domparv": ("celporv", "/selporv/", "日除け・天蓋庇を表す建築語幹"),
    "celdom": ("celup", "/selup/", "天蓋内面・天井（cel空 + up仰ぐ面）。ceiling/plafondと完全分離"),
    "taldom": ("tolst", "/tolst/", "母音交替o-grade（tol床面）+ 古語接尾辞-st。floor/yukaと完全分離"),

    # 2. TAL* FAMILY (Earth / Utensils / Furniture / Stone)
    "talel": ("dovik", "/dovik/", "作業面・台盤を表す調度語幹。英語table・独語tischと完全分離"),
    "talvin": ("pylvin", "/pylvin/", "焼成施釉陶器の皿・深鉢。英語plate・dish・仏語platと完全分離"),
    "talyz": ("marnyz", "/marnyz/", "大地の結晶塩・調味塩。独語salz・ラテン語salと完全分離"),
    "talpak": ("kypal", "/kypal/", "収容木匣・格納ケース。英語box・西語cajaと完全分離"),
    "talpin": ("neltin", "/neltin/", "金属工芸の留め針・飾り針。英語pinと完全分離"),
    "talzar": ("hylzar", "/hylzar/", "環状装飾・宝飾印章環。大地talから独立"),
    "talzarv": ("kolzan", "/kolzan/", "彫琢された石像・モニュメント。大地talから独立"),
    "talson": ("tolsun", "/tolsun/", "母音交替・母音調和（tol-sun: 巨石アーチ橋）"),
    "talvir": ("tulvir", "/tulvir/", "母音交替u-grade（tul: 深底粘質土・陶土）"),
    "talcor": ("tolcor", "/tolcor/", "母音交替o-grade（tol: 重厚巨石・モノリス）"),
    "talpor": ("polytar", "/polytar/", "幾何学空間胞体・多面体。大地talから分離"),

    # 3. NER* FAMILY (Cuisine / Nutrients / Viscera / Time)
    "nerat": ("nyrat", "/nyrat/", "母音交替y-grade（nyr: 焼き固めた主食パン）。bread/pan/brotと完全分離"),
    "nerkul": ("vurlin", "/vurlin/", "椀型掬い具・匙。spoon/loeffelと完全分離"),
    "nerspik": ("zartik", "/zartik/", "三つ又刺し具・フォーク。英語spike/forkと完全分離"),
    "neron": ("korgon", "/korgon/", "消化臓腑・胃。stomach/magenと完全分離"),
    "nerin": ("syvan", "/syvan/", "時間的・生命的新鮮さ。new/novusと完全分離"),
    "neris": ("dolis", "/dolis/", "空間的近接。near/procheと完全分離"),
    "nersar": ("nyrsan", "/nyrsan/", "母音交替y-grade（nyr: 焼き菓子・クリスプ）"),
    "nersil": ("tursil", "/tursil/", "スープ具材・煮込み固形実"),
    "nerili": ("melysi", "/melysi/", "蜜のような甘味。sweet/suessと完全分離"),

    # 4. FAL* FAMILY (Light / Optics / Speed / Space)
    "falar": ("farnal", "/farnal/", "歴史的鼻音同化（fal-nar -> farnal: 採光窓）。window/fenetreと完全分離"),
    "falvis": ("zenkal", "/zenkal/", "反射鏡面・姿見。mirror/spiegel/visageと完全分離"),
    "faluri": ("vyril", "/vyril/", "星辰速度・迅速。fast/rapidと完全分離"),
    "falki": ("kyrpi", "/kyrpi/", "鋭利・切創刃先。sharp/scharfと完全分離"),
    "falas": ("tulan", "/tulan/", "遠隔空間・彼方。far/distantと完全分離"),
    "falel": ("lyvel", "/lyvel/", "刻印された受光像・写真。photo/imageと完全分離"),
    "falik": ("felyn", "/felyn/", "精神の閃き・直観"),

    # 5. FER* FAMILY (Fauna / Anatomy)
    "ferkrot": ("krota", "/krota/", "角・突起の独立古語名詞。horn/tsunoと完全分離"),
    "ferpar": ("pyrk", "/pyrk/", "単音節の古語鋭爪名詞。claw/griffeと完全分離"),
    "ferparv": ("paryv", "/paryv/", "牙・門歯の独立古語名詞。fangと完全分離"),
    "ferten": ("tenis", "/tenis/", "獣毛・保温毛皮の独立語幹。fur/pelzと完全分離"),
    "ferlik": ("lyka", "/lyka/", "洞穴・巣の独立古語幹。nest/nidと完全分離"),
    "ferpuk": ("puka", "/puka/", "蹄・甲角の独立語幹。hoof/sabotと完全分離"),

    # 6. VEL* FAMILY (Flora / Somatics / Mathematics)
    "velik": ("hylik", "/hylik/", "生体表皮・細胞被膜。樹木velから分離"),
    "velmor": ("vorst", "/vorst/", "体軸背部・脊椎面。樹木velから分離"),
    "velfin": ("syndir", "/syndir/", "探索・発見動詞。樹木velから分離"),
    "velton": ("corval", "/corval/", "天体力学的重心・軌道平衡点。樹木velから分離"),
    "velat": ("marnat", "/marnat/", "格子状行列・数学マトリクス。樹木velから分離"),
    "velpon": ("velbon", "/velbon/", "歴史的子音同化（lp -> lb: 樹皮・木幹）")
}

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
    "12. 食・飲料・調理・食器",
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
    "12. 食・飲料・調理・食器": "穀物、主食、温煮料理、発酵酒、茶器、食卓具",
    "13. 衣飾・携行具・日常品": "被服、布地、帯紐、携帯鞄、日用具、灯火、筆記具",
    "14. 精神・哲学・感情・芸術": "意識、思索、美学、詩歌旋律、情動、記憶遺産",
    "15. 性質・状態・色彩・感触": "星彩色彩、物性触感、状態属性、対極性質",
    "16. 動作・動態・時空・方向副詞": "基本動詞、時空概念、3次元方向副詞体系（語幹+-u）"
}

with open("data/lexicon.json", "r", encoding="utf-8") as f:
    vocab = json.load(f)["vocabulary"]

updated_entries = []
refactor_count = 0
for w in vocab:
    root = w["nrs"]
    cat = w["category"]
    ipa = w["ipa"]
    pos = w["pos"]
    ja = w["meaningJa"]
    en = w["meaningEn"]
    note = w["notes"]
    
    if root in REFACTOR_MAP:
        new_root, new_ipa, new_note = REFACTOR_MAP[root]
        root = new_root
        ipa = new_ipa
        note = new_note
        refactor_count += 1
        
    updated_entries.append((cat, root, ipa, pos, ja, en, note))

print(f"Total entries refactored: {refactor_count} / {len(REFACTOR_MAP)}")
assert refactor_count == len(REFACTOR_MAP)

def sort_key(entry):
    cat = entry[0]
    cat_idx = CATEGORIES_ORDER.index(cat) if cat in CATEGORIES_ORDER else 99
    return (cat_idx, entry[1])

updated_entries.sort(key=sort_key)
total_count = len(updated_entries)
assert total_count == 1008

cat_counts = Counter(e[0] for e in updated_entries)

# 1. docs/Nebulith Master Lexicon.md
md_lines = [
    "# Nebulith Master Lexicon (星石語 統御語彙大系)",
    "",
    "> **Version**: 23.0 (Organic & Naturalistic - 1,008 Master Roots across 16 Categories)  ",
    "> **Design Principle**: Complete Purge of Earth Borrowings & False Cognates, Organic Ablaut, Historical Assimilation & Irregular Archaic Roots  ",
    f"> **Progress**: {total_count} / 1000 roots ({total_count / 10:.1f}%) [GOAL ACHIEVED]  ",
    "> **Phonetic Base**: Sonorous vowels (a, e, i, o, u, y), liquid semivowels (r, l, v, w, j), resonant nasals (m, n), accented by restrained stops & fricatives (p, b, t, d, k, g, f, s, z, h). Strict exclusion of q, x.",
    "",
    "---",
    "",
    "## 16-Domain Category Overview (全16領域構成)",
    "",
    "| ID | カテゴリー名 (Domain) | 語彙数 (Words) | 構成比 | 概要 |",
    "|---|---|---|---|---|",
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
for idx, (cat, root, ipa, pos, ja, en, note) in enumerate(updated_entries, 1):
    if cat != current_cat:
        current_cat = cat
        md_lines.extend([
            f"### {current_cat} ({cat_counts[current_cat]}語)",
            "",
            "| ID | 語根 (NRS) | IPA | 品詞 | 日本語意味 | 英語意味 | 語源・備考 |",
            "|---|---|---|---|---|---|---|",
        ])
    md_lines.append(f"| {idx} | **{root}** | `{ipa}` | {pos} | {ja} | {en} | {note} |")
    
with open("docs/Nebulith Master Lexicon.md", "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines) + "\n")
print("Wrote docs/Nebulith Master Lexicon.md")

# 2. data/lexicon.json
json_vocab = []
for idx, (cat, root, ipa, pos, ja, en, note) in enumerate(updated_entries, 1):
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

json_data = {
    "version": "23.0",
    "lastUpdated": "2026-10-15",
    "totalEntries": total_count,
    "targetGoal": 1000,
    "currentProgressPercent": round((total_count / 1000) * 100, 1),
    "phoneticRules": {
        "validCharacters": "abcdefghijklmnoprstuvwyz",
        "forbiddenCharacters": "qx",
        "vowels": "aeiouy",
        "consonants": "bdfghjklmnprstvwz"
    },
    "categories": [
        {
            "id": idx,
            "name": cat,
            "description": cat_descriptions.get(cat, ""),
            "wordsCount": cat_counts[cat]
        }
        for idx, cat in enumerate(CATEGORIES_ORDER, 1)
    ],
    "vocabulary": json_vocab
}

with open("data/lexicon.json", "w", encoding="utf-8") as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2)
print("Wrote data/lexicon.json")

# 3. data/lexicon.csv
with open("data/lexicon.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "category", "nrs", "ipa", "pos", "meaningJa", "meaningEn", "notes"])
    for idx, (cat, root, ipa, pos, ja, en, note) in enumerate(updated_entries, 1):
        writer.writerow([idx, cat, root, ipa, pos, ja, en, note])
print("Wrote data/lexicon.csv")

# 4. data/StaticLexicon.kt
kt_lines = [
    "package com.nebulith.lexicon",
    "",
    "/**",
    " * Nebulith Master Static Lexicon v23.0",
    f" * Total Roots: {total_count} (Organically Harmonized, Earth-Borrowing Free)",
    " * Autogenerated by apply_naturalistic_refactor.py",
    " */",
    "object StaticLexicon {",
    "    data class LexiconEntry(",
    "        val id: Int,",
    "        val category: String,",
    "        val nrs: String,",
    "        val ipa: String,",
    "        val pos: String,",
    "        val meaningJa: String,",
    "        val meaningEn: String,",
    "        val notes: String",
    "    )",
    "",
    f"    const val VERSION = \"23.0\"",
    f"    const val TOTAL_ENTRIES = {total_count}",
    "",
    "    val entries: List<LexiconEntry> = listOf("
]

for idx, (cat, root, ipa, pos, ja, en, note) in enumerate(updated_entries, 1):
    esc_ja = ja.replace('"', '\\"')
    esc_en = en.replace('"', '\\"')
    esc_note = note.replace('"', '\\"')
    kt_lines.append(f"        LexiconEntry({idx}, \"{cat}\", \"{root}\", \"{ipa}\", \"{pos}\", \"{esc_ja}\", \"{esc_en}\", \"{esc_note}\"),")

kt_lines.extend([
    "    )",
    "}"
])

with open("data/StaticLexicon.kt", "w", encoding="utf-8") as f:
    f.write("\n".join(kt_lines) + "\n")
print("Wrote data/StaticLexicon.kt")
print("\nALL 4 MASTER ARTIFACTS SUCCESSFULLY GENERATED & SYNCHRONIZED!")
