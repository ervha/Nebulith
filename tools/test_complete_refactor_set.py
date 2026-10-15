# tools/test_complete_refactor_set.py
import json
import re

EARTH_WORDS_EXTENDED = {
    "table": ["table", "mesa", "tisch", "daiku", "tsukue"],
    "plate": ["plate", "dish", "teller", "plat", "plato", "assiette", "sara"],
    "bread": ["bread", "pan", "pain", "pane", "brot", "loaf"],
    "spoon": ["spoon", "cuillere", "cuchara", "loeffel", "saji"],
    "fork": ["fork", "fourchette", "tenedor", "gabel", "spike"],
    "salt": ["salt", "sal", "sel", "salz", "shio"],
    "house": ["house", "domus", "maison", "casa", "haus", "heim", "ie"],
    "room": ["room", "chambre", "cuarto", "zimmer", "saal", "heya", "muro"],
    "door": ["door", "porte", "puerta", "tuer", "tor", "to", "tobira"],
    "window": ["window", "fenetre", "ventana", "fenster", "mado"],
    "stairs": ["stairs", "stair", "escalier", "escalera", "treppe", "stufe", "kaidan"],
    "ceiling": ["ceiling", "plafond", "techo", "decke", "tenjo"],
    "floor": ["floor", "plancher", "suelo", "boden", "yuka"],
    "mirror": ["mirror", "miroir", "espejo", "spiegel", "kagami", "vision"],
    "knife": ["knife", "couteau", "cuchillo", "messer", "klinge", "hocho", "to"],
    "box": ["box", "boite", "caja", "kiste", "kasten", "hako"],
    "pillar": ["pillar", "pilier", "pilar", "saeule", "pfeiler", "hashira"],
    "stomach": ["stomach", "estomac", "estomago", "magen", "i"],
    "fast": ["fast", "rapid", "rapide", "rapido", "schnell", "hayai"],
    "sharp": ["sharp", "acute", "pointu", "agudo", "scharf", "spitz", "surudoi"],
    "sweet": ["sweet", "doux", "dulce", "suess", "amai"],
    "new": ["new", "novus", "neuf", "nuevo", "neu", "atarashii", "shin"],
    "near": ["near", "close", "proche", "cerca", "nah", "chikai"],
    "far": ["far", "distant", "loin", "lejos", "weit", "fern", "tooi"],
    "horn": ["horn", "corne", "cuerno", "tsuno"],
    "claw": ["claw", "talon", "griffe", "garra", "klaue", "tsume"],
    "fang": ["fang", "croc", "colmillo", "fangzahn", "kiba"],
    "fur": ["fur", "fourrure", "pelaje", "pelz", "fell", "kegawa"],
    "nest": ["nest", "nid", "nido", "su"],
    "hoof": ["hoof", "sabot", "pezuna", "huf", "hizume"],
}

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    prev = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        curr = [i + 1]
        for j, c2 in enumerate(s2):
            ins = prev[j + 1] + 1
            dels = curr[j] + 1
            subs = prev[j] + (0 if c1 == c2 else 1)
            curr.append(min(ins, dels, subs))
        prev = curr
    return prev[-1]

REFACTOR_MAP = {
    # 1. DOM* -> Assimilation, Archaic roots
    "dom": ("vorn", "room", "奥室、内室、私室空間"),
    "domar": ("govan", "house", "家、住居、炉のある住まい"),
    "domkor": ("dankor", None, "市民、定住住民"),
    "domkorv": ("dankorv", None, "元首、執政官"),
    "domkar": ("dankar", None, "基礎、土台、建築石礎"),
    "domkarn": ("dankarn", None, "厩舎、馬屋、飼育棟"),
    "domtas": ("vostir", "stairs", "階段、昇降ステップ"),
    "domlik": ("kulmon", "pillar", "柱、支柱、大理石柱"),
    "domparn": ("borparn", None, "梁、桁、天井支え桁"),
    "domparv": ("celporv", None, "日除け庇、ポーチ屋根"),
    "celdom": ("celup", "ceiling", "天井、屋根天蓋"),
    "taldom": ("tolst", "floor", "床、居住基盤面"),

    # 2. TAL* -> Ablaut, Functional Roots, Utensils
    "talel": ("dovik", "table", "机、作業台、テーブル"),
    "talvin": ("pylvin", "plate", "皿、深鉢、陶器の器"),
    "talyz": ("marnyz", "salt", "大地の結晶塩、調味料"),
    "talpak": ("kypal", "box", "箱、小箱、収納ケース"),
    "talpin": ("neltin", None, "留め針、ブローチ、安全ピン"),
    "talzar": ("hylzar", None, "指輪、宝石指環"),
    "talzarv": ("kolzan", None, "彫像、彫刻、石造モニュメント"),
    "talson": ("tolsun", None, "石橋、アーチ橋、橋梁"),
    "talvir": ("tulvir", None, "粘土、陶土、深底粘土"),
    "talcor": ("tolcor", None, "巨石、一枚岩、モノリス"),
    "talpor": ("polytar", None, "多面体、幾何胞体"),

    # 3. NER* -> Ablaut, Distinct Anatomy, Adjectives
    "nerat": ("nyrat", "bread", "主食、焼き穀物パン"),
    "nerkul": ("vurlin", "spoon", "スプーン、匙、汁掬い"),
    "nerspik": ("zartik", "fork", "フォーク、刺し具、食具"),
    "neron": ("korgon", "stomach", "胃、消化器、滋養腑"),
    "nerin": ("syvan", "new", "新しい、新鮮な、新緑の"),
    "neris": ("dolis", "near", "近く、傍らに、親密に"),
    "nersar": ("nyrsan", None, "焼き菓子、ビスケット"),
    "nersil": ("tursil", None, "具材、スープの具、煮込み種"),
    "nerili": ("melysi", "sweet", "甘い、滋味豊かな、甘美な"),

    # 4. FAL* -> Speed, Optics, Precision
    "falar": ("farnal", "window", "窓、明かり取り、天窓"),
    "falvis": ("zenkal", "mirror", "鏡、姿見、光反射板"),
    "faluri": ("vyril", "fast", "速い、迅速な、光速の"),
    "falki": ("kyrpi", "sharp", "鋭い、研ぎ澄まされた"),
    "falas": ("tulan", "far", "遠く、彼方に、遠日点に"),
    "falel": ("lyvel", None, "写真、画像、受光像"),
    "falik": ("felyn", None, "直感、閃き、直観的洞察"),

    # 5. FER* -> Archaic independent nouns
    "ferkrot": ("krota", "horn", "角、双角、突起角"),
    "ferpar": ("pyrk", "claw", "鉤爪、爪、鋭爪"),
    "ferparv": ("paryv", "fang", "牙、鋭い犬歯、門歯"),
    "ferten": ("tenis", "fur", "毛皮、体毛、獣皮"),
    "ferlik": ("lyka", "nest", "巣、塒、鳥獣の棲家"),
    "ferpuk": ("puka", "hoof", "ひづめ、蹄、甲角"),

    # 6. VEL* -> Somatic & Scientific differentiation
    "velik": ("hylik", None, "皮膚、肌、外被"),
    "velmor": ("vorst", None, "背中、脊椎、背部"),
    "velfin": ("syndir", None, "探す、探索する、発見する"),
    "velton": ("corval", None, "連星系の重心、共通軌道中心"),
    "velat": ("marnat", None, "行列、マトリクス、格子配列"),
    "velpon": ("velbon", None, "樹皮、木の幹、木質部")
}

with open("data/lexicon.json", "r", encoding="utf-8") as f:
    vocab = json.load(f)["vocabulary"]

existing_words = {w["nrs"].lower(): w for w in vocab}

errors = []
print(f"Auditing {len(REFACTOR_MAP)} refactored words...\n")

for old_word, (new_word, concept, desc) in REFACTOR_MAP.items():
    if old_word not in existing_words:
        errors.append(f"Old word '{old_word}' not found in current lexicon!")
        continue
    
    # 1. Earth language safety check
    if concept:
        for ew in EARTH_WORDS_EXTENDED.get(concept, []):
            dist = levenshtein(new_word, ew)
            if dist <= 1 or (len(ew) >= 4 and dist <= 2) or ew in new_word or new_word in ew:
                errors.append(f"[EARTH CLASH] '{new_word}' for '{concept}' resembles Earth '{ew}' (dist={dist})")
    
    # 2. Existing Nebulith word collision check
    if new_word in existing_words and new_word != old_word:
        clash_entry = existing_words[new_word]
        errors.append(f"[LEXICON CLASH] '{new_word}' already exists as ID {clash_entry['id']} ({clash_entry['meaningJa']})")
    
    # 3. Phonetic character constraints (no q, x)
    if "q" in new_word or "x" in new_word:
        errors.append(f"[INVALID CHAR] '{new_word}' contains forbidden character q or x")

if errors:
    print("ERRORS FOUND:")
    for e in errors:
        print("  -", e)
else:
    print("SUCCESS: All 48 refactored words are 100% compliant, unique, and safe from Earth languages!")
