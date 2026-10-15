# tools/inspect_lexicon.py
import json

with open("data/lexicon.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"=== Nebulith Lexicon v{data['version']} Overview ===")
print(f"Total Words: {data['totalEntries']} / {data['targetGoal']} ({data['currentProgressPercent']}%)")
print("\n--- Categories Breakdown (16 Domains) ---")
for c in data["categories"]:
    print(f"{c['id']:2d}. {c['name']:<24}: {c['wordsCount']:3d}語 | {c['description']}")
