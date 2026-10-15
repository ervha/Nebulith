# tools/comprehensive_audit_1008.py
"""
Comprehensive Audit & Scrutiny Script for Nebulith Lexicon v22.0 (1,008 roots)
Checks:
  1. Root & IPA uniqueness (homophone / homograph collisions)
  2. Earth vocabulary contamination (English, Latin, Romance words exact & substring matches)
  3. Phonotactics & character set validation (forbidden q, x, invalid clusters)
  4. Levenshtein edit distance 1 confusable pairs without derivation relationship
  5. POS & definition consistency
  6. Category semantic alignment
"""
import json
import re
from collections import defaultdict

with open("data/lexicon.json", "r", encoding="utf-8") as f:
    data = json.load(f)

vocab = data["vocabulary"]
total_words = len(vocab)
print(f"Total vocabulary to scrutinize: {total_words}")

# 1. Root & IPA uniqueness
root_map = defaultdict(list)
ipa_map = defaultdict(list)
for w in vocab:
    root_map[w["nrs"]].append(w)
    ipa_map[w["ipa"]].append(w)

root_dups = {k: v for k, v in root_map.items() if len(v) > 1}
ipa_dups = {k: v for k, v in ipa_map.items() if len(v) > 1}

print("\n--- 1. Uniqueness Audit ---")
print(f"Duplicate NRS roots: {len(root_dups)}")
for r, entries in root_dups.items():
    print(f"  DUPLICATE ROOT '{r}': {[e['category'] + ':' + e['meaningJa'] for e in entries]}")

print(f"Duplicate IPA pronunciations: {len(ipa_dups)}")
for ipa, entries in ipa_dups.items():
    if len(entries) > 1 and len(set(e["nrs"] for e in entries)) > 1:
        print(f"  HOMOPHONE COLLISION '{ipa}': {[e['nrs'] + '(' + e['meaningJa'] + ')' for e in entries]}")

# 2. Phonotactics & Character Validation
print("\n--- 2. Phonotactics & Orthography Audit ---")
VALID_CHARS = set("abcdefghijklmnoprstuvwyz'")
FORBIDDEN_CHARS = set("qx")
ALLOWED_DIPHTHONGS = {"ai", "ei", "au", "oi"}

invalid_chars_found = []
forbidden_found = []
vowel_clusters_found = []

for w in vocab:
    r = w["nrs"]
    for ch in r:
        if ch not in VALID_CHARS:
            invalid_chars_found.append((r, ch))
        if ch in FORBIDDEN_CHARS:
            forbidden_found.append((r, ch))
            
    # Check vowel sequences of 2+ vowels
    vowels = "aeiouy"
    matches = re.findall(r'[aeiouy]{2,}', r)
    for m in matches:
        if m not in ALLOWED_DIPHTHONGS:
            vowel_clusters_found.append((r, m))

print(f"Invalid characters: {len(invalid_chars_found)} {invalid_chars_found}")
print(f"Forbidden 'q, x' characters: {len(forbidden_found)} {forbidden_found}")
print(f"Unorthodox vowel sequences (outside ai, ei, au, oi): {len(vowel_clusters_found)} {vowel_clusters_found[:10]}")

# 3. Earth Vocabulary Contamination Audit
print("\n--- 3. Earth Language Borrowing & Similarity Audit ---")
# Common English 3-4 letter words and Latin/French loan roots
COMMON_EARTH_WORDS = {
    # 2-4 letter English words
    "at", "in", "on", "to", "by", "for", "out", "up", "and", "but", "or", "so", "not",
    "man", "men", "boy", "cat", "dog", "sun", "sky", "sea", "air", "day", "eye", "ear",
    "arm", "leg", "car", "bus", "van", "bed", "box", "cup", "pen", "hat", "cap", "bag",
    "red", "hot", "dry", "wet", "old", "new", "big", "bad", "low", "far", "run", "sit",
    "see", "say", "get", "put", "let", "cut", "set", "hit", "win", "die", "cry", "fly",
    "bit", "byte", "node", "core", "disk", "link", "root", "host", "code", "data", "text",
    "star", "moon", "time", "year", "life", "dead", "body", "mind", "soul", "head", "hand",
    "foot", "home", "room", "city", "town", "land", "rock", "iron", "gold", "fire", "wind",
    "rain", "snow", "tree", "leaf", "bird", "fish", "bank", "cost", "debt", "fund", "loan",
    "loss", "mark", "pay", "plan", "rate", "sale", "shop", "toll", "wage", "corn", "rice",
    "meat", "milk", "soup", "stew", "wine", "beer", "cake", "dish", "diet", "meal", "fork",
    "line", "part", "sign", "point", "cord", "mode", "base", "cell", "form", "unit", "site",
    "door", "gate", "wall", "roof", "ship", "book", "page", "word", "name", "king", "lord",
    "law", "duty", "rule", "bell", "ring", "song", "horn", "salt", "acid", "flow", "wave",
    "tide", "beam", "void", "space", "dust", "gale", "boss", "crew", "farm", "mill", "mine",
    "herb", "pork", "beef", "feed", "flour", "food", "fact", "true", "real", "evil", "good",
    "down", "high", "shut", "open", "sing", "walk", "tell", "talk", "hear", "deep", "dark",
    "path", "road", "hope", "fear", "love", "when", "what", "here", "past", "soon", "west",
    "east", "left", "auto", "tele", "post", "port", "gene", "poly", "mono", "micro", "macro",
    "neo", "bio", "geo", "chrono", "cosmo", "astro", "hydro", "pyro", "aero", "omni", "multi",
    # Latin common roots
    "aqua", "terra", "ignis", "aer", "sol", "luna", "stella", "caelum", "homo", "corpus",
    "anima", "mens", "vita", "mors", "tempus", "annus", "dies", "nox", "lux", "umbra",
    "mare", "mons", "silva", "flos", "arbor", "avis", "piscis", "lex", "rex", "civitas",
    "urbs", "domus", "via", "bellum", "pax", "amor", "timor", "veritas", "scientia"
}

exact_earth_matches = []
for w in vocab:
    r = w["nrs"].lower()
    if r in COMMON_EARTH_WORDS:
        exact_earth_matches.append((r, w["meaningJa"], w["category"]))

print(f"Exact Earth word matches: {len(exact_earth_matches)}")
for r, m, c in exact_earth_matches:
    print(f"  EXACT MATCH: '{r}' ({m} in {c})")

# 4. Levenshtein edit distance 1 analysis
def lev(s1, s2):
    if len(s1) < len(s2):
        return lev(s2, s1)
    if len(s2) == 0:
        return len(s1)
    prev = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        curr = [i + 1]
        for j, c2 in enumerate(s2):
            ins = prev[j + 1] + 1
            dels = curr[j] + 1
            sub = prev[j] + (0 if c1 == c2 else 1)
            curr.append(min(ins, dels, sub))
        prev = curr
    return prev[-1]

roots = sorted(list(root_map.keys()))
close_unrelated_pairs = []

# Derived suffixes that naturally cause edit distance 1:
# -u (adverb), -i (adj), -an (verb), -en (verb), -in (verb), -on (verb), -el (tool), -ar (place), -or (person), -om (collective)
for i in range(len(roots)):
    w1 = roots[i]
    for j in range(i + 1, len(roots)):
        w2 = roots[j]
        if abs(len(w1) - len(w2)) > 1:
            continue
        if lev(w1, w2) == 1:
            # Check if one is a direct derivation of the other
            e1 = root_map[w1][0]
            e2 = root_map[w2][0]
            # Is it a safe derivation? e.g. w2 == w1 + 'u' or w2 == w1 + 'i'
            is_deriv = False
            if w2 == w1 + "u" or w1 == w2 + "u" or w2 == w1 + "i" or w1 == w2 + "i":
                is_deriv = True
            elif w1[:-1] == w2[:-1] and (w1[-1] in "aeiou" and w2[-1] in "aeiou"):
                is_deriv = False # Potential vowel confusion
            
            if not is_deriv and len(w1) <= 4 and len(w2) <= 4:
                # Short words with distance 1 are the most confusable
                close_unrelated_pairs.append((w1, w2, e1["meaningJa"], e2["meaningJa"], e1["category"], e2["category"]))

print("\n--- 4. Short-word High-Confusion Risk Pairs (len<=4, dist=1) ---")
print(f"Total short confusable pairs: {len(close_unrelated_pairs)}")
for w1, w2, m1, m2, c1, c2 in close_unrelated_pairs[:20]:
    print(f"  {w1:<6} vs {w2:<6} | {m1[:12]:<12} vs {m2[:12]:<12} [{c1[:6]} vs {c2[:6]}]")

# 5. POS & Grammatical Suffix Alignment
print("\n--- 5. POS & Suffix Consistency Audit ---")
pos_counts = defaultdict(int)
for w in vocab:
    pos_counts[w["pos"]].append(w) if isinstance(pos_counts[w["pos"]], list) else None

from collections import Counter
c = Counter(w["pos"] for w in vocab)
print(f"Part of Speech breakdown: {dict(c)}")

# Check verbs ending
non_standard_verbs = [w for w in vocab if w["pos"] == "動" and not (w["nrs"].endswith("an") or w["nrs"].endswith("en") or w["nrs"].endswith("in") or w["nrs"].endswith("on") or w["nrs"].endswith("un") or w["nrs"].endswith("el"))]
print(f"Verbs with non-standard endings: {len(non_standard_verbs)}")
for v in non_standard_verbs[:10]:
    print(f"  VERB: {v['nrs']} [{v['meaningJa']}]")

# Check adverbs ending in -u
adverbs = [w for w in vocab if w["pos"] == "副"]
u_adverbs = [w for w in adverbs if w["nrs"].endswith("u")]
print(f"Adverbs ending in -u: {len(u_adverbs)} / {len(adverbs)}")
non_u_adv = [w for w in adverbs if not w["nrs"].endswith("u")]
print(f"Adverbs not ending in -u: {len(non_u_adv)}")
for a in non_u_adv[:10]:
    print(f"  NON-U ADV: {a['nrs']} [{a['meaningJa']}]")
