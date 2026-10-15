# tools/audit_new_lexicon_candidates.py
import json

with open("data/lexicon.json", "r", encoding="utf-8") as f:
    data = json.load(f)

existing_roots = {w["nrs"] for w in data["vocabulary"]}

# Let's inspect the existing directional adverbs
dir_adverbs = [w for w in data["vocabulary"] if w["nrs"].endswith("u") and w["pos"] == "副"]
print(f"Existing -u adverbs ({len(dir_adverbs)}):", [w["nrs"] for w in dir_adverbs])
