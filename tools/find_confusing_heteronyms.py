# tools/find_confusing_heteronyms.py
import json

with open("data/lexicon.json", "r", encoding="utf-8") as f:
    vocab = json.load(f)["vocabulary"]

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

# Find pairs where lev(w1, w2) == 1 and meaning is completely different
# especially short roots (length <= 5)
hetero_pairs = []

for i in range(len(vocab)):
    w1 = vocab[i]
    r1 = w1["nrs"]
    c1 = w1["category"]
    m1 = w1["meaningJa"]
    for j in range(i + 1, len(vocab)):
        w2 = vocab[j]
        r2 = w2["nrs"]
        c2 = w2["category"]
        m2 = w2["meaningJa"]
        
        if abs(len(r1) - len(r2)) > 1:
            continue
        if lev(r1, r2) == 1:
            # Check if they share the same semantic root prefix
            # If categories are different or meanings are unrelated
            # Check if derivation: e.g. r2 == r1 + 'u' (directional adverb) or r2 == r1 + 'i'
            if r2 == r1 + "u" or r1 == r2 + "u" or r2 == r1 + "i" or r1 == r2 + "i":
                continue # Normal systematic derivation
            if r2.startswith(r1) and w2["notes"].startswith(r1):
                continue # Direct etymological compound
            if r1.startswith(r2) and w1["notes"].startswith(r2):
                continue
                
            # These are potentially confusing heteronyms!
            if len(r1) <= 5 and len(r2) <= 5:
                hetero_pairs.append((r1, r2, m1, m2, c1, c2, w1["pos"], w2["pos"]))

print(f"Total potential confusing heteronym pairs: {len(hetero_pairs)}")
for r1, r2, m1, m2, c1, c2, p1, p2 in hetero_pairs:
    print(f"  {r1:<7} ({p1}:{m1[:10]}) vs {r2:<7} ({p2}:{m2[:10]}) | [{c1[:4]} vs {c2[:4]}]")
