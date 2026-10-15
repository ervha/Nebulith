# tools/check_levenshtein_660.py
import json
from generate_v20_candidates import NEW_80_ENTRIES

with open("data/lexicon.json", "r", encoding="utf-8") as f:
    existing_vocab = json.load(f)["vocabulary"]

all_words = {w["nrs"]: w["meaningJa"] for w in existing_vocab}
for cat, root, ipa, pos, ja, en, note in NEW_80_ENTRIES:
    all_words[root] = ja

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

words = sorted(all_words.keys())
print(f"Total words to check: {len(words)}")

close_pairs = []
for i in range(len(words)):
    w1 = words[i]
    for j in range(i + 1, len(words)):
        w2 = words[j]
        # Only check if lengths are close
        if abs(len(w1) - len(w2)) > 1:
            continue
        d = lev(w1, w2)
        if d == 1:
            # Check if one is an obvious derivation with suffix (like -u, -an, -ar, -el, -om)
            close_pairs.append((w1, w2, all_words[w1], all_words[w2]))

print(f"Found {len(close_pairs)} close pairs (edit distance = 1).")
print("Sample pairs:")
for w1, w2, m1, m2 in close_pairs[:15]:
    print(f"  {w1:<10} vs {w2:<10} | {m1[:15]:<15} vs {m2[:15]:<15}")
