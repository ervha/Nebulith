# tools/reclassify_lexicon.py
import json

with open("data/lexicon.json", "r", encoding="utf-8") as f:
    data = json.load(f)

vocab = data["vocabulary"]

# Let's inspect category 4 (自然・気象・環境), category 7 (日常・住まい・食), category 2 (数理・幾何・情報科学), category 8 (動作・相互作用), category 10 (時空・方位・副詞)
for cat_name in ["2. 数理・幾何・情報科学", "4. 自然・気象・環境", "7. 日常・住まい・食", "8. 動作・相互作用", "10. 時空・方位・副詞"]:
    print(f"\n=================== {cat_name} ===================")
    for w in vocab:
        if w["category"] == cat_name:
            print(f"{w['nrs']:<12} : {w['meaningJa'][:25]} ({w['meaningEn'][:30]})")
