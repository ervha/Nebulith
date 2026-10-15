# tools/build_master_lexicon_v20.py
"""
Nebulith Master Lexicon v20.0 Build & Audit Script
Reorganized from 10 categories to 16 comprehensive domains.
Completely purged of Earth-language borrowings (English, Latin, Romance).
Expanded to 660 master roots (Progress: 66.0% towards 1000-root milestone).

Generates:
  1. docs/Nebulith Master Lexicon.md  (Human-readable Markdown specification)
  2. data/lexicon.json                (Machine-readable structured JSON format)
  3. data/lexicon.csv                 (Tabular CSV format)
  4. data/StaticLexicon.kt            (Ready-to-use Kotlin source code for KMP)
"""
import json
import csv
import os
from generate_v20_candidates import NEW_80_ENTRIES

VOWELS = set("aeiouy")
DIPHTHONGS = {"ai", "ei", "au", "oi"}
VALID_CHARS = set("abcdefghijklmnoprstuvwyz'")

# Forbidden Earth root and loanword blacklist (exact match check)
EARTH_BORROWING_BLACKLIST = {
    "auto", "tele", "port", "sign", "part", "post", "line", "point", "cord", "mode",
    "base", "cell", "gene", "data", "text", "form", "core", "disk", "node", "unit",
    "byte", "code", "host", "link", "root", "site", "star", "moon", "sun", "sky",
    "dark", "deep", "time", "year", "life", "dead", "mind", "soul", "body", "head",
    "hand", "foot", "home", "room", "city", "town", "land", "rock", "iron", "gold",
    "fire", "wind", "rain", "snow", "tree", "leaf", "bird", "fish", "walk", "sing",
    "talk", "open", "shut", "good", "evil", "true", "real", "fact", "high", "down",
    "left", "east", "west", "past", "soon", "here", "there", "when", "what", "where",
    "love", "hope", "fear", "path", "road", "gate", "door", "wall", "roof", "ship",
    "book", "page", "word", "name", "king", "lord", "rule", "law", "duty", "gold",
    "bell", "ring", "song", "horn", "iron", "lead", "zinc", "salt", "acid", "flow",
    "wave", "tide", "beam", "ray", "void", "space", "dust", "cloud", "storm", "gale",
    "bank", "cost", "debt", "fund", "loan", "loss", "mark", "pay", "plan", "rate",
    "sale", "shop", "toll", "wage", "boss", "crew", "farm", "mill", "mine", "crop",
    "beef", "beer", "cake", "corn", "dish", "diet", "feed", "flour", "food", "fork",
    "herb", "meal", "meat", "milk", "pork", "rice", "salt", "soup", "stew", "wine"
}

# 16 Categories Specification
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

CAT_ASTRONOMY = CATEGORIES_ORDER[0]
CAT_MATH = CATEGORIES_ORDER[1]
CAT_COMPUTING = CATEGORIES_ORDER[2]
CAT_BIOLOGY = CATEGORIES_ORDER[3]
CAT_GEOLOGY = CATEGORIES_ORDER[4]
CAT_METEOROLOGY = CATEGORIES_ORDER[5]
CAT_FLORA = CATEGORIES_ORDER[6]
CAT_FAUNA = CATEGORIES_ORDER[7]
CAT_GOVERNANCE = CATEGORIES_ORDER[8]
CAT_ECONOMY = CATEGORIES_ORDER[9]
CAT_ARCHITECTURE = CATEGORIES_ORDER[10]
CAT_FOOD = CATEGORIES_ORDER[11]
CAT_EVERYDAY = CATEGORIES_ORDER[12]
CAT_PHILOSOPHY = CATEGORIES_ORDER[13]
CAT_QUALITIES = CATEGORIES_ORDER[14]
CAT_ACTIONS = CATEGORIES_ORDER[15]

EXPLICIT_CAT = {
    # Computing
    "suf": CAT_COMPUTING, "sufor": CAT_COMPUTING, "sufom": CAT_COMPUTING, "mator": CAT_COMPUTING,
    "zevil": CAT_COMPUTING, "kiran": CAT_COMPUTING, "pelel": CAT_COMPUTING, "tolas": CAT_COMPUTING,
    "wesan": CAT_COMPUTING, "tolom": CAT_COMPUTING, "vylatel": CAT_COMPUTING, "falel": CAT_COMPUTING,
    "livar": CAT_COMPUTING, "jyn": CAT_COMPUTING, "jynel": CAT_COMPUTING, "kyvren": CAT_COMPUTING,
    "kiv": CAT_COMPUTING, "velat": CAT_COMPUTING, "vylom": CAT_COMPUTING, "tyk": CAT_COMPUTING,
    "jylom": CAT_COMPUTING, "voret": CAT_COMPUTING, "sevik": CAT_COMPUTING, "ved": CAT_COMPUTING,
    "velis": CAT_COMPUTING, "torin": CAT_COMPUTING, "folin": CAT_COMPUTING, "soril": CAT_COMPUTING,
    "jylvat": CAT_COMPUTING, "sufrin": CAT_COMPUTING, "kivlom": CAT_COMPUTING, "veltok": CAT_COMPUTING,
    "zydot": CAT_COMPUTING, "krotel": CAT_COMPUTING, "suftas": CAT_COMPUTING, "zevkas": CAT_COMPUTING,
    "kivkas": CAT_COMPUTING, "matoris": CAT_COMPUTING, "kirvat": CAT_COMPUTING, "kivku": CAT_COMPUTING,
    "suflit": CAT_COMPUTING, "kirfas": CAT_COMPUTING,

    # Math & Geometry
    "rin": CAT_MATH, "tulik": CAT_MATH, "niven": CAT_MATH, "talisum": CAT_MATH, "kvan": CAT_MATH,
    "jyt": CAT_MATH, "kiril": CAT_MATH, "kelon": CAT_MATH, "firas": CAT_MATH, "ryvel": CAT_MATH,
    "unor": CAT_MATH, "delis": CAT_MATH, "jylrin": CAT_MATH, "delrin": CAT_MATH, "vedot": CAT_MATH,
    "zydis": CAT_MATH, "sevur": CAT_MATH, "firtas": CAT_MATH, "kelvis": CAT_MATH, "unvis": CAT_MATH,
    "vedkar": CAT_MATH,

    # Geology & Minerals
    "tal": CAT_GEOLOGY, "novan": CAT_GEOLOGY, "talik": CAT_GEOLOGY, "talom": CAT_GEOLOGY,
    "talis": CAT_GEOLOGY, "talur": CAT_GEOLOGY, "talrim": CAT_GEOLOGY, "vuron": CAT_GEOLOGY,
    "talon": CAT_GEOLOGY, "talser": CAT_GEOLOGY, "talkrot": CAT_GEOLOGY, "pyrtal": CAT_GEOLOGY,
    "taldar": CAT_GEOLOGY, "talmor": CAT_GEOLOGY, "talisar": CAT_GEOLOGY, "talsid": CAT_GEOLOGY,
    "talfot": CAT_GEOLOGY,

    # Meteorology & Water
    "daris": CAT_METEOROLOGY, "dar": CAT_METEOROLOGY, "zylar": CAT_METEOROLOGY, "daron": CAT_METEOROLOGY,
    "darmon": CAT_METEOROLOGY, "darlen": CAT_METEOROLOGY, "kyrlen": CAT_METEOROLOGY, "kyras": CAT_METEOROLOGY,
    "wylas": CAT_METEOROLOGY, "celis": CAT_METEOROLOGY, "pyris": CAT_METEOROLOGY, "wylrim": CAT_METEOROLOGY,
    "vyltor": CAT_METEOROLOGY, "celar": CAT_METEOROLOGY, "darsik": CAT_METEOROLOGY, "darfal": CAT_METEOROLOGY,
    "zylrim": CAT_METEOROLOGY, "havas": CAT_METEOROLOGY, "velhav": CAT_METEOROLOGY, "zohav": CAT_METEOROLOGY,
    "darlor": CAT_METEOROLOGY, "wylven": CAT_METEOROLOGY, "kyrfin": CAT_METEOROLOGY, "darmar": CAT_METEOROLOGY,
    "wylor": CAT_METEOROLOGY, "kyrtam": CAT_METEOROLOGY, "pyrlom": CAT_METEOROLOGY, "faldaris": CAT_METEOROLOGY,
    "darpuk": CAT_METEOROLOGY, "wylsuk": CAT_METEOROLOGY, "celkym": CAT_METEOROLOGY, "darrot": CAT_METEOROLOGY,

    # Flora
    "velom": CAT_FLORA, "vel": CAT_FLORA, "velas": CAT_FLORA, "velin": CAT_FLORA, "velil": CAT_FLORA,
    "vorin": CAT_FLORA, "teiril": CAT_FLORA, "velpon": CAT_FLORA, "velrot": CAT_FLORA, "velspar": CAT_FLORA,
    "veltul": CAT_FLORA, "vorken": CAT_FLORA, "talkan": CAT_FLORA, "velmor": CAT_FLORA,

    # Fauna
    "feras": CAT_FAUNA, "volfer": CAT_FAUNA, "zylfer": CAT_FAUNA, "krap": CAT_FAUNA, "fermor": CAT_FAUNA,
    "falpir": CAT_FAUNA,

    # Economy & Trade & Craft
    "dolaran": CAT_ECONOMY, "talpyr": CAT_ECONOMY, "jylpan": CAT_ECONOMY, "valdanar": CAT_ECONOMY,
    "maren": CAT_ECONOMY, "koran": CAT_ECONOMY, "kirasen": CAT_ECONOMY, "dolor": CAT_ECONOMY,

    # Architecture & Living Spaces
    "dom": CAT_ARCHITECTURE, "domar": CAT_ARCHITECTURE, "domom": CAT_ARCHITECTURE, "taran": CAT_ARCHITECTURE,
    "lerel": CAT_ARCHITECTURE, "falar": CAT_ARCHITECTURE, "laros": CAT_ARCHITECTURE, "larar": CAT_ARCHITECTURE,
    "celdom": CAT_ARCHITECTURE, "taldom": CAT_ARCHITECTURE, "durval": CAT_ARCHITECTURE, "velar": CAT_ARCHITECTURE,
    "domlik": CAT_ARCHITECTURE, "lervan": CAT_ARCHITECTURE, "domtas": CAT_ARCHITECTURE, "lertal": CAT_ARCHITECTURE,

    # Food & Drink & Cookery
    "ner": CAT_FOOD, "neran": CAT_FOOD, "nerel": CAT_FOOD, "neror": CAT_FOOD, "nerar": CAT_FOOD,
    "bion": CAT_FOOD, "terin": CAT_FOOD, "nerat": CAT_FOOD, "talyz": CAT_FOOD, "darel": CAT_FOOD,
    "voril": CAT_FOOD, "nerom": CAT_FOOD, "talvin": CAT_FOOD, "nerkam": CAT_FOOD, "terlar": CAT_FOOD,
    "nerkul": CAT_FOOD, "nerspik": CAT_FOOD, "bionas": CAT_FOOD, "nerkot": CAT_FOOD, "bionel": CAT_FOOD,
    "nerpas": CAT_FOOD, "pyrtos": CAT_FOOD, "darpan": CAT_FOOD,

    # Everyday Goods & Clothing
    "valis": CAT_EVERYDAY, "pamel": CAT_EVERYDAY, "talel": CAT_EVERYDAY, "tasel": CAT_EVERYDAY,
    "kymel": CAT_EVERYDAY, "klovel": CAT_EVERYDAY, "serel": CAT_EVERYDAY, "kirel": CAT_EVERYDAY,
    "falvis": CAT_EVERYDAY, "valdan": CAT_EVERYDAY, "larsil": CAT_EVERYDAY, "tasor": CAT_EVERYDAY,
    "falmir": CAT_EVERYDAY, "serval": CAT_EVERYDAY, "valren": CAT_EVERYDAY, "lervil": CAT_EVERYDAY,
    "falkom": CAT_EVERYDAY, "pamelar": CAT_EVERYDAY, "valkor": CAT_EVERYDAY, "faldisan": CAT_EVERYDAY,
    "talpak": CAT_EVERYDAY, "biondis": CAT_EVERYDAY, "pamelis": CAT_EVERYDAY,
}

def load_all_entries():
    with open("data/lexicon.json", "r", encoding="utf-8") as f:
        existing_vocab = json.load(f)["vocabulary"]
    
    all_entries = []
    
    # 1. Process existing 580 words with 16-category mapping
    for w in existing_vocab:
        root = w["nrs"]
        old_cat = w["category"]
        ipa = w["ipa"]
        pos = w["pos"]
        ja = w["meaningJa"]
        en = w["meaningEn"]
        note = w["notes"]
        
        if root in EXPLICIT_CAT:
            new_cat = EXPLICIT_CAT[root]
        elif old_cat.startswith("1."):
            new_cat = CAT_ASTRONOMY
        elif old_cat.startswith("3."):
            new_cat = CAT_BIOLOGY
        elif old_cat.startswith("5."):
            if any(k in ja for k in ["交易", "市場", "貨幣", "財", "商"]):
                new_cat = CAT_ECONOMY
            else:
                new_cat = CAT_GOVERNANCE
        elif old_cat.startswith("6."):
            new_cat = CAT_PHILOSOPHY
        elif old_cat.startswith("9."):
            new_cat = CAT_QUALITIES
        elif old_cat.startswith("10.") or old_cat.startswith("8."):
            new_cat = CAT_ACTIONS
        else:
            new_cat = old_cat
            
        all_entries.append((new_cat, root, ipa, pos, ja, en, note))
        
    # 2. Add New 80 Entries
    for entry in NEW_80_ENTRIES:
        all_entries.append(entry)
        
    return all_entries

def audit_lexicon(entries):
    roots = set()
    errors = []
    
    for cat, root, ipa, pos, ja, en, note in entries:
        # Check duplicate
        if root in roots:
            errors.append(f"DUPLICATE ROOT: '{root}'")
        roots.add(root)
        
        # Check forbidden chars
        for ch in root:
            if ch not in VALID_CHARS:
                errors.append(f"INVALID CHAR '{ch}' in '{root}'")
            if ch in ("q", "x"):
                errors.append(f"FORBIDDEN CHAR '{ch}' in '{root}'")
                
        # Check Earth borrowings
        if root in EARTH_BORROWING_BLACKLIST:
            errors.append(f"EARTH BORROWING DETECTED: '{root}' in {EARTH_BORROWING_BLACKLIST}")
            
    if errors:
        print("\n".join(errors))
        raise ValueError(f"Audit failed with {len(errors)} errors!")
    print(f"AUDIT PASSED! Total vetted master entries: {len(entries)}")

def sort_key(entry):
    cat = entry[0]
    cat_idx = CATEGORIES_ORDER.index(cat) if cat in CATEGORIES_ORDER else 99
    return (cat_idx, entry[1])

def build_all():
    entries = load_all_entries()
    audit_lexicon(entries)
    
    # Sort entries by category order then root
    entries.sort(key=sort_key)
    
    total_count = len(entries)
    assert total_count == 660, f"Expected 660 entries, got {total_count}"
    
    # 1. Generate Markdown: docs/Nebulith Master Lexicon.md
    md_lines = [
        "# Nebulith Master Lexicon (星石語 統御語彙大系)",
        "",
        "> **Version**: 20.0 (Expansion to 660 Master Roots across 16 Categories)  ",
        "> **Design Principle**: Complete Purge of Earth Borrowings & Harmonious Celestial Aesthetics  ",
        f"> **Progress**: {total_count} / 1000 roots ({total_count / 10:.1f}%)  ",
        "> **Phonetic Base**: Sonorous vowels (a, e, i, o, u, y), liquid semivowels (r, l, v, w, j), resonant nasals (m, n), accented by restrained stops & fricatives (p, b, t, d, k, g, f, s, z, h). Strict exclusion of q, x.",
        "",
        "---",
        "",
        "## 16-Domain Category Overview",
        "",
        "| ID | カテゴリー名 (Domain) | 語彙数 (Words) | 概要 |",
        "|---|---|---|---|"
    ]
    
    from collections import Counter
    cat_counts = Counter(e[0] for e in entries)
    
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
    
    for idx, cat in enumerate(CATEGORIES_ORDER, 1):
        count = cat_counts[cat]
        desc = cat_descriptions.get(cat, "")
        md_lines.append(f"| {idx} | **{cat}** | {count}語 | {desc} |")
        
    md_lines.extend([
        "",
        "---",
        "",
        "## 語彙目録 (Master Vocabulary Entries)",
        ""
    ])
    
    current_cat = None
    for idx, (cat, root, ipa, pos, ja, en, note) in enumerate(entries, 1):
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
    for idx, (cat, root, ipa, pos, ja, en, note) in enumerate(entries, 1):
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
        "version": "20.0",
        "language": "Nebulith",
        "languageJa": "星石語 (Nebulith)",
        "updatedAt": "2026-10-15",
        "status": "Expanding towards 1000 roots milestone (Reorganized into 16 categories)",
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
            "verbStems": "-an (active), -en (stative), -in (inchoative), -on (perfective), -un (habitual)",
            "directionalAdverbs": "Root + -u (e.g., kymdenu = westward, vorasu = forward, celosu = upward)"
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
        for idx, (cat, root, ipa, pos, ja, en, note) in enumerate(entries, 1):
            writer.writerow([idx, cat, root, ipa, pos, ja, en, note])
    print("Successfully written to data/lexicon.csv!")
    
    # 4. Generate Kotlin: data/StaticLexicon.kt
    kt_lines = [
        "package com.nebulith.data",
        "",
        "/**",
        " * Autogenerated Static Lexicon for Nebulith (v20.0)",
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
        f"    const val VERSION = \"20.0\"",
        f"    const val TOTAL_ENTRIES = {total_count}",
        "",
        "    val entries: List<LexiconEntry> = listOf("
    ]
    
    for idx, (cat, root, ipa, pos, ja, en, note) in enumerate(entries, 1):
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

if __name__ == "__main__":
    build_all()
