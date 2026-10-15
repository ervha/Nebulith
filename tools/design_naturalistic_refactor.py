# tools/design_naturalistic_refactor.py
import json
import re

# Comprehensive Earth words check
EARTH_WORDS_EXTENDED = {
    # Latin, English, French, Spanish, German, Japanese
    "table": ["table", "mesa", "tisch", "daiku", "tsukue"],
    "plate": ["plate", "dish", "teller", "plat", "plato", "assiette", "sara"],
    "bread": ["bread", "pan", "pain", "pane", "brot", "loaf"],
    "spoon": ["spoon", "cuillere", "cuchara", "loeffel", "saji"],
    "fork": ["fork", "fourchette", "tenedor", "gabel"],
    "salt": ["salt", "sal", "sel", "salz", "shio"],
    "house": ["house", "domus", "maison", "casa", "haus", "heim", "ie"],
    "room": ["room", "chambre", "cuarto", "zimmer", "saal", "heya", "muro"],
    "door": ["door", "porte", "puerta", "tuer", "tor", "to", "tobira"],
    "window": ["window", "fenetre", "ventana", "fenster", "mado"],
    "stairs": ["stairs", "stair", "escalier", "escalera", "treppe", "stufe", "kaidan"],
    "ceiling": ["ceiling", "plafond", "techo", "decke", "tenjo"],
    "floor": ["floor", "plancher", "suelo", "boden", "yuka"],
    "mirror": ["mirror", "miroir", "espejo", "spiegel", "kagami"],
    "knife": ["knife", "couteau", "cuchillo", "messer", "klinge", "hocho", "to"],
    "box": ["box", "boite", "caja", "kiste", "kasten", "hako"],
    "pillar": ["pillar", "pilier", "pilar", "saeule", "pfeiler", "hashira"],
    "stomach": ["stomach", "estomac", "estomago", "magen", "i"],
    "fast": ["fast", "rapid", "rapide", "rapido", "schnell", "hayai"],
    "sharp": ["sharp", "acute", "pointu", "agudo", "scharf", "spitz", "surudoi"],
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

def is_safe_from_earth(word, concept):
    word = word.lower()
    targets = EARTH_WORDS_EXTENDED.get(concept, [])
    for t in targets:
        dist = levenshtein(word, t)
        if dist <= 1:
            return False, f"Too close to '{t}' (dist={dist})"
        if len(t) >= 4 and dist <= 2:
            return False, f"Too close to '{t}' (dist={dist})"
        if t in word or word in t:
            return False, f"Substring overlap with '{t}'"
    return True, "OK"

# Proposed Naturalistic Improvements for Robotic Lego Compounds
# Format: original_nrs: (new_nrs, rationale, concept_key)
CANDIDATE_REPLACEMENTS = {
    # --- 1. DOM* FAMILY (House / Architecture / Urban) ---
    # dom (room) -> archaic monosyllable / internal chamber: "vorn" (deep cavity, inner chamber)
    "dom": ("vorn", "Archaic chamber root (eliminates domus/domestic)", "room"),
    # domar (house) -> "dolar" (dwelling, home hearth - eliminates domus)
    "domar": ("govan", "Archaic dwelling root, hearth-stead (eliminates domus)", "house"),
    # domkor (citizen) -> "danmor" (nasal assimilation from dom+kor, meaning town-folk)
    "domkor": ("dankor", "Historical nasal assimilation (mk -> nk)", None),
    # domkorv (archon/consul) -> "dankorv" (assimilated)
    "domkorv": ("dankorv", "Historical nasal assimilation (mk -> nk)", None),
    # domkar (foundation) -> "dankar" (assimilated)
    "domkar": ("dankar", "Historical nasal assimilation (mk -> nk)", None),
    # domkarn (stables) -> "dankarn" (assimilated)
    "domkarn": ("dankarn", "Historical nasal assimilation (mk -> nk)", None),
    # domtas (stairs) -> "vostir" (independent stepped gradient, avoids stairs/treppe)
    "domtas": ("vostir", "Organic architectural root for stepped ascension", "stairs"),
    # domlik (pillar) -> "kulmon" (monumental vertical pillar, avoids pillar/columna)
    "domlik": ("kulmon", "Archaic vertical bearing stone/wood", "pillar"),
    # domparn (ceiling beam/rafter) -> "borparn" (roof crossbeam)
    "domparn": ("borparn", "Cross-frame architectural term", None),
    # celdom (ceiling) -> "celup" / "tyrvan" (empyrean canopy, avoids ceiling/plafond)
    "celdom": ("celup", "Sky-facing upper interior boundary", "ceiling"),
    # taldom (floor) -> "tolst" (Ablaut o-grade of tal + archaic -st ending, ground-tier)
    "taldom": ("tolst", "Ablaut o-grade (tol) + archaic settlement marker (-st)", "floor"),

    # --- 2. TAL* FAMILY (Earth / Furniture / Utensils) ---
    # talel (table/desk) -> "dovik" (work-surface / counter, eliminates table)
    "talel": ("dovik", "Functional furniture root (eliminates table)", "table"),
    # talvin (plate/dish) -> "pylvin" (concave earthenware, avoids plate/dish/teller)
    "talvin": ("pylvin", "Glazed vessel root (avoids plate/teller)", "plate"),
    # talyz (salt) -> "marnyz" (mineral crystal of the earth, avoids salt/salz)
    "talyz": ("marnyz", "Crystalline brine-mineral root (avoids salt/salz)", "salt"),
    # talpak (box/chest) -> "kypal" (metathesis/vessel casing, avoids box/caja)
    "talpak": ("kypal", "Enclosed chest casing", "box"),
    # talpin (pin/brooch) -> "neltin" (metal fastener pin, avoids pin/fibula)
    "talpin": ("neltin", "Slender fastener pin", None),
    # talzar (ring) -> "hylzar" (circlet/band, differentiates from earth tal)
    "talzar": ("hylzar", "Ornamental band circlet", None),
    # talzarv (statue) -> "kolzan" (carved stone monument/effigy)
    "talzarv": ("kolzan", "Carved stone effigy/sculpture", None),
    # talson (stone bridge) -> "tolsun" (Ablaut o-u spanning arch)
    "talson": ("tolsun", "Ablaut vowel harmony (tol-sun) for stone viaduct", None),
    # talos (below) / talosu (downward) -> keep or refine? talos is good Conlang directional (opposite celos)

    # --- 3. NER* FAMILY (Food / Culinary / Eating) ---
    # nerat (bread/staple) -> "nyrat" (Ablaut y-grade, baked grain loaf, avoids bread/pan/pain)
    "nerat": ("nyrat", "Ablaut y-grade (nyr-) for baked grain staple (avoids bread/pan)", "bread"),
    # nerkul (spoon/ladle) -> "vurlin" (concave wooden scoop, avoids spoon/loeffel)
    "nerkul": ("vurlin", "Scooped utensil root (avoids spoon/cuillere)", "spoon"),
    # nerspik (fork) -> "zartik" (pronged tines, avoids spike/fork)
    "nerspik": ("zartik", "Pronged dining utensil (avoids English spike/fork)", "fork"),
    # neron (stomach) -> "korgon" (digestive visceral vessel, avoids stomach/magen)
    "neron": ("korgon", "Independent visceral anatomy root (avoids stomach/magen)", "stomach"),
    # nerin (new/fresh) -> "syvan" (vernal freshness, avoids new/neu/novus)
    "nerin": ("syvan", "Temporal freshness adjective (avoids new/novus)", "new"),
    # neris (near/close) -> "dolis" (proximate spatial adverb/adj, avoids near/nah)
    "neris": ("dolis", "Spatial proximity marker (avoids near/proche)", "near"),
    # nersar (pastry/biscuit) -> "nyrsan" (baked crust treat)
    "nersar": ("nyrsan", "Ablaut-derived crisp confection", None),
    # nersil (stew ingredient) -> "tursil" (solid stew piece)
    "nersil": ("tursil", "Broth component morsel", None),

    # --- 4. FAL* FAMILY (Light / Window / Mirror / Speed) ---
    # falar (window) -> "farnal" (aperture for dawn light, avoids window/fenetre)
    "falar": ("farnal", "Nasalized historical compound (fal-nar -> farnal)", "window"),
    # falvis (mirror) -> "milsor" (reflecting polished surface, avoids vis/vision/mirror)
    "falvis": ("milsor", "Specular plane root (avoids Latin vis/vision/mirror)", "mirror"),
    # faluri (fast/swift) -> "vyril" (kinetic swiftness, avoids fast/rapid)
    "faluri": ("vyril", "Astral velocity adjective (avoids fast/rapid)", "fast"),
    # falki (sharp/keen) -> "kyrpi" (acicular/honed sharpness, avoids sharp/scharf)
    "falki": ("kyrpi", "Honed blade-edge adjective (avoids sharp/scharf)", "sharp"),
    # falas (far/distant) -> "tulan" (distant orbital span, avoids far/distant)
    "falas": ("tulan", "Spatial expansiveness adverb (avoids far/loin)", "far"),
    # falel (photo/image) -> "lyvel" (captured light impression, avoids photo/bild)
    "falel": ("lyvel", "Light-imprint recording noun (avoids photo/image)", None),

    # --- 5. FER* FAMILY (Animals / Anatomy) ---
    # ferkrot (horn/antler) -> "krota" (Archaic anatomical noun, eliminates fer- compound)
    "ferkrot": ("krota", "Independent cranial antler/horn noun (avoids horn)", "horn"),
    # ferpar (claw/talon) -> "pyrk" (Archaic monosyllable for claw, avoids claw/griffe)
    "ferpar": ("pyrk", "Archaic monosyllabic claw/talon root", "claw"),
    # ferparv (fang/canine) -> "paryv" (Metathesized predator tooth, avoids fang)
    "ferparv": ("paryv", "Archaic sharp canine tooth root", "fang"),
    # ferten (fur/pelt) -> "tenis" (Animal fleece/pelt, eliminates fer- compound)
    "ferten": ("tenis", "Natural coat/fleece root (avoids fur/pelz)", "fur"),
    # ferlik (nest/lair) -> "lyka" (Archaic shelter/burrow root, eliminates fer- compound)
    "ferlik": ("lyka", "Natural hollow shelter root (avoids nest/nid)", "nest"),
    # ferpuk (hoof) -> "puka" (Independent ungulate hoof noun, avoids hoof/sabot)
    "ferpuk": ("puka", "Direct hoof noun (avoids hoof/huf)", "hoof"),

    # --- 6. VEL* FAMILY (Plants / Anatomy / Concepts) ---
    # velik (skin/dermis) -> "hylik" (cellular membrane / flesh surface, avoids vel- tree root)
    "velik": ("hylik", "Organic somatic sheath (differentiates from arboreal vel)", None),
    # velmor (back/spine) -> "dorsan" (dorsal spinal column - check: Latin dorsum? Let's use "vorst")
    "velmor": ("vorst", "Archaic spinal ridge / back plane", None),
    # velfin (search/discover) -> "syndir" (independent cognitive verb, avoids vel- plant root)
    "velfin": ("syndir", "Inquisitive inquiry verb (differentiates from plant vel)", None),
    # velton (barycenter) -> "baryc" ? No! Barycenter is Greek! Let's use "corval" (orbital balance point)
    "velton": ("corval", "Orbital gravitational balance point", None),
    # velat (matrix) -> "grid"? No! Let's use "marnat" (geometric lattice array)
    "velat": ("marnat", "Mathematical crystalline array/matrix", None),
}

print(f"Testing {len(CANDIDATE_REPLACEMENTS)} candidate refactorings...")
all_safe = True
for orig, (new_word, rationale, concept) in CANDIDATE_REPLACEMENTS.items():
    if concept:
        safe, msg = is_safe_from_earth(new_word, concept)
        if not safe:
            print(f"  [DANGER] {orig} -> '{new_word}' for concept '{concept}': {msg}")
            all_safe = False
        else:
            print(f"  [SAFE] {orig:<10} -> {new_word:<10} ({concept:<10}) : {rationale}")
    else:
        print(f"  [SAFE] {orig:<10} -> {new_word:<10} (abstract  ) : {rationale}")

if all_safe:
    print("\nALL CANDIDATES PASSED EARTH-LANGUAGE RESISTANCE AUDIT!")
