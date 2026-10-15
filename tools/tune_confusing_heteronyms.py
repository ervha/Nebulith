# tools/tune_confusing_heteronyms.py
"""
Harmonization and de-confusion script for confusing heteronym pairs in Nebulith v22.0.
Refines short heteronym roots to maintain distinct phonological identities while preserving
natural irregular morphology and organic variations.
"""
import json

with open("data/lexicon.json", "r", encoding="utf-8") as f:
    vocab = json.load(f)["vocabulary"]

# Proposed surgical tunings for confusing heteronym pairs
# (old_root -> new_root, new_ipa, new_notes)
TUNING_MAP = {
    # 1. foras (おそらく) vs voras (前・前方) -> foras is easily misheard as voras
    "foras": ("forvis", "[for.vis]", "for (星の導き) + vis (推量様態: おそらく)"),

    # 2. valk (頻繁に) vs falk (閃光) -> valk takes standard adverb suffix -u
    "valk": ("valku", "[val.ku]", "valk (波打つ頻度) + -u (副詞化: 頻繁に、度々)"),

    # 3. ved (真偽値) vs ve (はい) vs vel (木) -> differentiate the boolean root
    "ved": ("vedil", "[ve.dil]", "ved (論理極性) + -il (値/素子: 真偽値、ブーリアン)"),

    # 4. elyr (祭典) vs elir (喜び) -> differentiate festival from joy
    "elyr": ("elyrat", "[e.ly.rat]", "elyr (星祭) + -at (大儀礼: 星の祭り、祭典)"),

    # 5. kypan (身を屈める) vs kupan (走る) -> differentiate physical posture
    "kypan": ("kympan", "[kym.pan]", "kym (影) + pan (低姿勢に伏せる、身を屈める)"),

    # 6. velan (探す) vs celan (仰ぎ見る) vs volan (飛ぶ) -> strengthen 'search' without colliding with velkan
    "velan": ("velfin", "[vel.fin]", "vel (探索の眼差し) + fin (見出す、探す、発見する)"),

    # 7. cylan (美・崇高) vs zylan (泳ぐ) -> clarify abstract beauty noun/adj
    "cylan": ("cylas", "[cy.las]", "cyl (調和美) + -as (崇高美、美しい、優雅)"),

    # 8. koran (切断する) vs poran (歩く) vs pyran (燃える) -> strengthen 'sever'
    "koran": ("kortan", "[kor.tan]", "kor (刃) + tan (断ち切る、切断する、裁つ)"),

    # 9. maren (受け取る) vs saren (笑う) -> refine transaction verb
    "maren": ("martan", "[mar.tan]", "mar (交換) + tan (収受する、受け取る、引き継ぐ)"),

    # 10. haris (聴く) vs taris (待つ) -> strengthen auditory verb
    "haris": ("harvan", "[har.van]", "har (耳) + van (傾聴する、聴く、聞き届ける)"),

    # 11. jyt (ノード・結節) vs jyn (電気) -> clarify node element
    "jyt": ("jytel", "[jy.tel]", "jyt (結節点) + -el (素子: ノード、ネットワーク交点)"),
}

print(f"Total targeted tunings: {len(TUNING_MAP)}")

# Check if any new root collides with existing vocabulary
existing_roots = {w["nrs"] for w in vocab}
collisions = 0
for old_r, (new_r, ipa, note) in TUNING_MAP.items():
    if new_r in existing_roots and new_r != old_r:
        print(f"COLLISION WARNING: {new_r} already exists!")
        collisions += 1
    else:
        print(f"  Tuned '{old_r}' -> '{new_r}' {ipa}")

assert collisions == 0, "Collisions detected!"
print("All 11 tunings are completely non-colliding and verified!")
