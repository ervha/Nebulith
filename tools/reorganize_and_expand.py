# tools/reorganize_and_expand.py
import json

with open("data/lexicon.json", "r", encoding="utf-8") as f:
    data = json.load(f)

vocab = data["vocabulary"]

# Mapping dictionary for existing 580 words to New 16 Categories
# We'll build specific rules and explicit maps
CAT_ASTRONOMY = "1. 天体・宇宙力学・光"
CAT_MATH = "2. 数理・幾何・計測"
CAT_COMPUTING = "3. 情報・計算機・通信"
CAT_BIOLOGY = "4. 生命・生体・医療"
CAT_GEOLOGY = "5. 自然地形・地質・鉱物"
CAT_METEOROLOGY = "6. 気象・大気・水域"
CAT_FLORA = "7. 植物・生態・農耕"
CAT_FAUNA = "8. 動物・生物種・共生"
CAT_GOVERNANCE = "9. 統治・社会・法・共同体"
CAT_ECONOMY = "10. 経済・交易・工芸・労働"
CAT_ARCHITECTURE = "11. 建築・都市・住空間"
CAT_FOOD = "12. 食・飲料・調理・食具"
CAT_EVERYDAY = "13. 衣飾・携行具・日常品"
CAT_PHILOSOPHY = "14. 精神・哲学・感情・芸術"
CAT_QUALITIES = "15. 性質・状態・色彩・感触"
CAT_ACTIONS = "16. 動作・動態・時空・方向副詞"

# Explicit categorization map for existing words
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

# Now let's see how each word gets mapped
reclassified = []
unmapped = []
for w in vocab:
    root = w["nrs"]
    old_cat = w["category"]
    
    if root in EXPLICIT_CAT:
        new_cat = EXPLICIT_CAT[root]
    elif old_cat.startswith("1."):
        new_cat = CAT_ASTRONOMY
    elif old_cat.startswith("3."):
        new_cat = CAT_BIOLOGY
    elif old_cat.startswith("5."):
        # Check if trade/economy
        if "交易" in w["meaningJa"] or "市場" in w["meaningJa"] or "貨幣" in w["meaningJa"] or "財" in w["meaningJa"] or "商" in w["meaningJa"]:
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
        unmapped.append(w)
    
    reclassified.append((new_cat, w))

from collections import Counter
counts = Counter(c for c, _ in reclassified)
print("=== Reclassified Category Counts for Existing 580 words ===")
for cat in sorted(counts.keys()):
    print(f"{cat}: {counts[cat]} words")
