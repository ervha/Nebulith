# tools/analyze_lexicon_roots.py
import json
from collections import Counter

with open("data/lexicon.json", "r", encoding="utf-8") as f:
    vocab = json.load(f)["vocabulary"]

# Prefix / Root family analysis (first 3 letters)
prefixes = [w["nrs"][:3] for w in vocab if len(w["nrs"]) >= 3]
c_pref = Counter(prefixes)

print("Top Root Families (Prefix 3-grams):")
for p, count in c_pref.most_common(20):
    print(f"  '{p}*': {count} words (e.g. {[w['nrs'] for w in vocab if w['nrs'].startswith(p)][:4]})")

# Length distribution
lens = [len(w["nrs"]) for w in vocab]
c_lens = Counter(lens)
print("\nWord Length Distribution:")
for l in sorted(c_lens.keys()):
    print(f"  Length {l:2d}: {c_lens[l]:3d} words ({'#' * (c_lens[l] // 5)})")
