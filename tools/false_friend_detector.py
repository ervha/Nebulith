# tools/false_friend_detector.py
"""
Multilingual False Friend & Cognate Detector for Nebulith (Conlang Audit Framework)
Compares Nebulith NRS roots against core vocabulary across 6 major Earth languages:
  1. English (en)
  2. Latin (la)
  3. French (fr)
  4. Spanish (es)
  5. German (de)
  6. Japanese (ja / Hepburn romaji)

Standard Levenshtein threshold:
  Distance <= 2 or substring containment for semantic equivalents constitutes a violation (CHK-04).
"""
import json
import re

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

# Common Earth language words mapped to their concept meanings
# Normalized lowercase ASCII/Hepburn forms across En, La, Fr, Es, De, Ja
EARTH_WORDS = {
    # Food / dining
    "bread": ["bread", "pan", "pain", "pane", "brot"],
    "meat": ["meat", "carne", "viande", "fleisch", "niku"],
    "soup": ["soup", "suppe", "soupe", "sopa", "shiru"],
    "pot": ["pot", "topf", "olla", "marmite", "nabe"],
    "spoon": ["spoon", "cuillere", "cuchara", "loeffel", "saji"],
    "fork": ["fork", "fourchette", "tenedor", "gabel"],
    "knife": ["knife", "couteau", "cuchillo", "messer", "hocho"],
    "plate": ["plate", "plat", "plato", "teller", "sara"],
    "honey": ["honey", "miel", "honig", "hachimitsu"],
    "cheese": ["cheese", "fromage", "queso", "kaese"],
    "salt": ["salt", "sal", "sel", "salz", "shio"],
    "meal": ["meal", "repas", "comida", "mahlzeit", "gohan", "meshi"],
    "cook": ["cook", "cuisinier", "cocinero", "koch"],
    "kitchen": ["kitchen", "cuisine", "cocina", "kueche", "daidokoro"],
    "eat": ["eat", "manger", "comer", "essen", "taberu"],

    # House / Architecture / Furniture
    "table": ["table", "mesa", "tisch"],
    "box": ["box", "boite", "caja", "kiste", "hako"],
    "house": ["house", "domus", "maison", "casa", "haus", "ie"],
    "room": ["room", "chambre", "cuarto", "zimmer", "heya"],
    "door": ["door", "porte", "puerta", "tuer", "tobira", "to"],
    "window": ["window", "fenetre", "ventana", "fenster", "mado"],
    "wall": ["wall", "mur", "pared", "mauer", "wand", "kabe"],
    "roof": ["roof", "toit", "techo", "dach", "yane"],
    "stairs": ["stairs", "escalier", "escalera", "treppe", "kaidan"],
    "pillar": ["pillar", "pilier", "columna", "pfeiler", "hashira"],
    "tower": ["tower", "tour", "torre", "turm", "to"],
    "city": ["city", "cite", "ciudad", "stadt", "machi", "toshi"],

    # Nature / Plants / Animals
    "tree": ["tree", "arbor", "arbre", "arbol", "baum", "ki"],
    "leaf": ["leaf", "feuille", "hoja", "blatt", "ha"],
    "flower": ["flower", "flos", "fleur", "flor", "blume", "hana"],
    "root": ["root", "radix", "racine", "raiz", "wurzel", "ne"],
    "forest": ["forest", "silva", "foret", "bosque", "wald", "mori", "hayashi"],
    "animal": ["animal", "tier", "beast", "doubutsu", "kemono"],
    "dog": ["dog", "canis", "chien", "perro", "hund", "inu"],
    "cat": ["cat", "felis", "chat", "gato", "katze", "neko"],
    "bird": ["bird", "avis", "oiseau", "ave", "vogel", "tori"],
    "fish": ["fish", "piscis", "poisson", "pez", "fisch", "sakana"],
    "stone": ["stone", "petra", "pierre", "piedra", "stein", "ishi"],
    "earth": ["earth", "terra", "terre", "tierra", "erde", "tsuchi"],
    "mountain": ["mountain", "mons", "mont", "montana", "berg", "yama"],
    "river": ["river", "riviere", "rio", "fluss", "kawa"],
    "sea": ["sea", "mare", "mer", "mar", "meer", "see", "umi"],
    "sun": ["sun", "sol", "soleil", "sonne", "hi", "taiyo"],
    "moon": ["moon", "luna", "lune", "mond", "tsuki"],
    "star": ["star", "stella", "etoile", "estrella", "stern", "hoshi"],
    "sky": ["sky", "ciel", "cielo", "himmel", "sora"],
    "cloud": ["cloud", "nuage", "nube", "wolke", "kumo"],
    "rain": ["rain", "pluie", "lluvia", "regen", "ame"],
    "wind": ["wind", "vent", "viento", "kaze"],
    "fire": ["fire", "ignis", "feu", "fuego", "feuer", "hi"],
    "water": ["water", "aqua", "eau", "agua", "wasser", "mizu"],

    # Body
    "hand": ["hand", "manus", "main", "mano", "te"],
    "foot": ["foot", "pes", "pied", "pie", "fuss", "ashi"],
    "head": ["head", "caput", "tete", "cabeza", "kopf", "atama"],
    "eye": ["eye", "oculus", "oeil", "ojo", "auge", "me"],
    "ear": ["ear", "auris", "oreille", "oreja", "ohr", "mimi"],
    "mouth": ["mouth", "os", "bouche", "boca", "mund", "kuchi"],
    "heart": ["heart", "cor", "coeur", "corazon", "herz", "kokoro", "shinzo"],
    "blood": ["blood", "sanguis", "sang", "sangre", "blut", "chi"],
    "skin": ["skin", "cutis", "peau", "piel", "haut", "hada"],

    # Adjectives / Adverbs
    "fast": ["fast", "rapid", "rapide", "schnell", "hayai"],
    "slow": ["slow", "lent", "lento", "langsam", "osoi"],
    "sharp": ["sharp", "acute", "pointu", "agudo", "scharf", "surudoi"],
    "sweet": ["sweet", "doux", "dulce", "suess", "amai"],
    "bitter": ["bitter", "amer", "amargo", "nigai"],
    "hard": ["hard", "dur", "duro", "hart", "katai"],
    "soft": ["soft", "mou", "suave", "weich", "yawarakai"],
    "new": ["new", "novus", "neuf", "nouveau", "nuevo", "neu", "atarashii"],
    "old": ["old", "vetus", "vieux", "viejo", "alt", "furui"],
    "far": ["far", "distant", "loin", "lejos", "weit", "tooi"],
    "near": ["near", "proche", "cerca", "nah", "chikai"],
    "high": ["high", "altus", "haut", "alto", "hoch", "takai"],
    "low": ["low", "bas", "bajo", "niedrig", "hikui"],
    "big": ["big", "great", "grand", "grande", "gross", "ookii"],
    "small": ["small", "petit", "pequeno", "klein", "chiisai"],
    "good": ["good", "bon", "bueno", "gut", "ii", "yoi"],
    "bad": ["bad", "mal", "malo", "schlecht", "warui"],

    # Verbs
    "see": ["see", "voir", "ver", "sehen", "miru"],
    "hear": ["hear", "entendre", "oir", "hoeren", "kiku"],
    "speak": ["speak", "parler", "hablar", "sprechen", "hanasu"],
    "walk": ["walk", "marcher", "caminar", "gehen", "aruku"],
    "run": ["run", "courir", "correr", "rennen", "lauf", "hashiru"],
    "give": ["give", "donner", "dar", "geben", "ataeru"],
    "take": ["take", "prendre", "tomar", "nehmen", "toru"],
    "sleep": ["sleep", "dormir", "schlafen", "nemuru"],
    "wake": ["wake", "reveiller", "despertar", "wecken", "okiru"],
}

def check_false_friends(vocab):
    suspects = []
    for entry in vocab:
        nrs = entry["nrs"].lower()
        en_desc = entry["meaningEn"].lower()

        for concept, words in EARTH_WORDS.items():
            concept_match = False
            if re.search(r'\b' + re.escape(concept) + r'\b', en_desc):
                concept_match = True
            
            if concept_match:
                for ew in words:
                    dist = levenshtein(nrs, ew)
                    if dist <= 2 or ew in nrs or nrs in ew:
                        suspects.append({
                            "id": entry["id"],
                            "nrs": nrs,
                            "concept": concept,
                            "earth_word": ew,
                            "distance": dist,
                            "meaningEn": entry["meaningEn"],
                            "meaningJa": entry["meaningJa"]
                        })
    return suspects

if __name__ == "__main__":
    with open("data/lexicon.json", "r", encoding="utf-8") as f:
        vocab = json.load(f)["vocabulary"]
    
    suspects = check_false_friends(vocab)
    print(f"Total potential false cognates found: {len(suspects)}")
    for s in suspects:
        print(f"ID {s['id']:4d}: NRS '{s['nrs']}' vs Earth '{s['earth_word']}' (dist={s['distance']}) for concept '{s['concept']}' -> {s['meaningJa']}")
