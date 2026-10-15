# tools/map_reorganization.py
import json
from collections import defaultdict

with open("data/lexicon.json", "r", encoding="utf-8") as f:
    data = json.load(f)

vocab = data["vocabulary"]
by_cat = defaultdict(list)
for w in vocab:
    by_cat[w["category"]].append(w)

for cat in sorted(by_cat.keys()):
    words = by_cat[cat]
    print(f"=== {cat} ({len(words)} words) ===")
    for w in words:
        print(f"  {w['nrs']:<12} [{w['ipa']:<14}] {w['pos']:<5} {w['meaningJa']:<20} {w['meaningEn']}")
