# tools/remediate_audit_findings.py
"""
Legacy v23.1 migration for 'audit/docs/Nebulith Audit Results 2026-10-15.md'.
Retained as implementation history; the current bounded fixes are in apply_reaudit02_fixes.py.
  1. F-03 / CHK-04: Surgically replaces 'ser' (hand) and derivatives with 'palv' roots.
  2. F-01: Fixes Category 12 name to '12. 食・飲料・調理・食具' across metadata & entries.
  3. F-02: Normalizes all 1,008 IPA entries to clean [...] brackets with strict
           conformance to phonetic rules (c -> ʃ, j -> ʒ).
  4. Synchronizes all 4 master formats:
       - data/lexicon.json
       - data/lexicon.csv
       - data/StaticLexicon.kt
       - docs/Nebulith Master Lexicon.md
"""
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CATEGORIES_ORDER = [
    "1. 天体・宇宙力学・光",
    "2. 数理・幾何・計測",
    "3. 情報・計算機・通信",
    "4. 生命・生体・医療",
    "5. 自然地形・地質・鉱物",
    "6. 気象・大気・水域",
    "7. 植物・生態・農耕",
    "8. 動物・生物種・共生",
    "9. 統治・社会・法・共同体",
    "10. 経済・交易・工芸・労働",
    "11. 建築・都市・住空間",
    "12. 食・飲料・調理・食具",
    "13. 衣飾・携行具・日常品",
    "14. 精神・哲学・感情・芸術",
    "15. 性質・状態・色彩・感触",
    "16. 動作・動態・時空・方向副詞"
]

CAT_DESCRIPTIONS = {
    "1. 天体・宇宙力学・光": "恒星、惑星、軌道力学、重力場、放射光、宇宙論",
    "2. 数理・幾何・計測": "理論数学、幾何学、次元、定数、公理、尺度",
    "3. 情報・計算機・通信": "計算機、コード構文、暗号、通信網、データ構造、記憶",
    "4. 生命・生体・医療": "生命現象、解剖構造、器官組織、脈動、治癒、薬理",
    "5. 自然地形・地質・鉱物": "大地、山岳、岩石、結晶鉱物、地層、地下洞窟",
    "6. 気象・大気・水域": "大気循環、風系、雲雪、海洋、水系、気象変動",
    "7. 植物・生態・農耕": "樹木、草花、種子、生態系、土壌、農耕栽培",
    "8. 動物・生物種・共生": "野生動物、鳥類、水棲生物、昆虫、生態共生",
    "9. 統治・社会・法・共同体": "法規範、評議会、市民共同体、誓約、身分同盟",
    "10. 経済・交易・工芸・労働": "市場経済、貨幣、交易路、冶金鍛造、手織機、職人技",
    "11. 建築・都市・住空間": "家屋、建築構造、門柱、都市区画、広場、居住基盤",
    "12. 食・飲料・調理・食具": "穀物、主食、温煮料理、発酵酒、茶器、食卓具",
    "13. 衣飾・携行具・日常品": "被服、布地、帯紐、携帯鞄、日用具、灯火、筆記具",
    "14. 精神・哲学・感情・芸術": "意識、思索、美学、詩歌旋律、情動、記憶遺産",
    "15. 性質・状態・色彩・感触": "星彩色彩、物性触感、状態属性、対極性質",
    "16. 動作・動態・時空・方向副詞": "基本動詞、時空概念、3次元方向副詞体系（語幹+-u）"
}

SLASH_MAP = {
    "corval": "[ʃor.val]",
    "polytar": "[po.ly.tar]",
    "lyvel": "[ly.vel]",
    "marnat": "[mar.nat]",
    "hylik": "[hy.lik]",
    "korgon": "[kor.gon]",
    "tolcor": "[tol.ʃor]",
    "tulvir": "[tul.vir]",
    "velbon": "[vel.bon]",
    "vorst": "[vorst]",
    "krota": "[kro.ta]",
    "lyka": "[ly.ka]",
    "paryv": "[pa.ryv]",
    "puka": "[pu.ka]",
    "pyrk": "[pyrk]",
    "tenis": "[te.nis]",
    "dankor": "[dan.kor]",
    "dankorv": "[dan.korv]",
    "borparn": "[bor.parn]",
    "celporv": "[ʃel.porv]",
    "celup": "[ʃe.lup]",
    "dankar": "[dan.kar]",
    "dankarn": "[dan.karn]",
    "farnal": "[far.nal]",
    "govan": "[go.van]",
    "kulmon": "[kul.mon]",
    "tolst": "[tolst]",
    "tolsun": "[tol.sun]",
    "vorn": "[vorn]",
    "vostir": "[vos.tir]",
    "dovik": "[do.vik]",
    "hylzar": "[hyl.zar]",
    "kypal": "[ky.pal]",
    "neltin": "[nel.tin]",
    "zenkal": "[zen.kal]",
    "felyn": "[fe.lyn]",
    "kolzan": "[kol.zan]",
    "kyrpi": "[kyr.pi]",
    "melysi": "[me.ly.si]",
    "syvan": "[sy.van]",
    "vyril": "[vy.ril]",
    "dolis": "[do.lis]",
    "syndir": "[syn.dir]",
    "tulan": "[tu.lan]",
    "marnyz": "[mar.nyz]",
    "nyrat": "[ny.rat]",
    "nyrsan": "[nyr.san]",
    "pylvin": "[pyl.vin]",
    "tursil": "[tur.sil]",
    "vurlin": "[vur.lin]",
    "zartik": "[zar.tik]",
}

SER_REPLACEMENTS = {
    "ser": ("palv", "[palv]", "手のひら・手掌を表す星辰語幹（旧serより改定、地球言語類似完全排除）"),
    "serjyt": ("palvjyt", "[palv.ʒyt]", "palv (手掌) + jyt (節点)"),
    "serval": ("palvval", "[palv.val]", "palv (手) + val (覆い・防護)"),
    "sersarn": ("palvsarn", "[palv.sarn]", "palv (手・触覚) + sarn (微粒子)"),
    "seran": ("palvan", "[pal.van]", "palv (手) + -an (授受動詞化)"),
    "sercor": ("palvcor", "[palv.ʃor]", "palv (手) + cor (協調・連環動詞)"),
    "serfas": ("palvfas", "[palv.fas]", "palv (手) + fas (離脱・開放)"),
    "serin": ("palvin", "[pal.vin]", "palv (手) + -in (接触・把持動詞)"),
    "serzan": ("palvzan", "[palv.zan]", "palv (手) + zan (牽引・引導)"),
}


def main():
    json_path = ROOT / "data/lexicon.json"
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    vocab = data["vocabulary"]
    assert len(vocab) == 1008

    # 1. Apply root replacements & IPA normalization
    for r in vocab:
        # Category 12 unification
        if r["category"].startswith("12."):
            r["category"] = "12. 食・飲料・調理・食具"

        # ser -> palv replacements
        nrs = r["nrs"]
        if nrs in SER_REPLACEMENTS:
            new_nrs, new_ipa, note_suffix = SER_REPLACEMENTS[nrs]
            r["nrs"] = new_nrs
            r["ipa"] = new_ipa
            if "ser" in r["notes"]:
                r["notes"] = r["notes"].replace("ser", "palv") + f"；{note_suffix}"
            else:
                r["notes"] = r["notes"] + f"；{note_suffix}"

        # IPA normalization
        cur_nrs = r["nrs"]
        cur_ipa = r["ipa"]
        if cur_nrs in SLASH_MAP:
            cur_ipa = SLASH_MAP[cur_nrs]
        elif cur_ipa.startswith("/") and cur_ipa.endswith("/"):
            cur_ipa = "[" + cur_ipa[1:-1] + "]"

        content = cur_ipa.strip("[]")
        if cur_nrs in ("cynor", "cynur"):
            content = content.replace("ʒ", "ʃ")
        content = content.replace("c", "ʃ").replace("j", "ʒ")
        r["ipa"] = f"[{content}]"

    # Category count validation
    cat_counts = Counter(r["category"] for r in vocab)
    for cat in CATEGORIES_ORDER:
        assert cat_counts[cat] > 0, f"Category {cat} has 0 words!"

    # 2. Write data/lexicon.json
    categories_meta = []
    for i, c in enumerate(CATEGORIES_ORDER):
        categories_meta.append({
            "id": i + 1,
            "name": c,
            "wordsCount": cat_counts[c],
            "description": CAT_DESCRIPTIONS.get(c, "")
        })

    json_obj = {
        "version": "23.1",
        "language": "Nebulith",
        "languageJa": "星石語 (Nebulith)",
        "updatedAt": "2026-10-15",
        "status": "Audit Remediated & Standard Compliant (v23.1: 1,008 roots across 16 categories with zero Earth cognates)",
        "targetGoal": 1000,
        "currentProgressPercent": 100.8,
        "totalEntries": len(vocab),
        "categories": categories_meta,
        "phoneticRules": {
            "validCharacters": "abcdefghijklmnoprstuvwyz'",
            "forbiddenCharacters": "qx",
            "vowels": "aeiouy",
            "diphthongs": ["ai", "ei", "au", "oi"],
            "consonants": "bcdfghjklmnprstvwz",
            "codaConsonants": "lrnms",
            "codaSonorityHierarchy": {
                "unmarkedBase": "aeiouylrnms (vowels, liquids, nasals, sibilant)",
                "markedExceptionsApproved": "vtpdkgfz (astronomical mechanics, boundaries, crystalline textures, archaic roots)"
            }
        },
        "vocabulary": vocab
    }

    crlf_nl = "\r\n"
    json_text = json.dumps(json_obj, ensure_ascii=False, indent=2)
    # Ensure CRLF line endings
    json_text_crlf = crlf_nl.join(json_text.splitlines()) + crlf_nl
    (ROOT / "data/lexicon.json").write_bytes(json_text_crlf.encode("utf-8"))
    print("Successfully updated data/lexicon.json")

    # 3. Write data/lexicon.csv
    csv_rows = [["id", "category", "nrs", "ipa", "pos", "meaningJa", "meaningEn", "notes"]]
    for r in vocab:
        csv_rows.append([
            str(r["id"]),
            r["category"],
            r["nrs"],
            r["ipa"],
            r["pos"],
            r["meaningJa"],
            r["meaningEn"],
            r["notes"]
        ])

    csv_lines = []
    for row in csv_rows:
        # Quote fields if needed
        quoted = []
        for val in row:
            if "," in val or '"' in val or "\n" in val:
                val = '"' + val.replace('"', '""') + '"'
            quoted.append(val)
        csv_lines.append(",".join(quoted))
    csv_text_crlf = crlf_nl.join(csv_lines) + crlf_nl
    (ROOT / "data/lexicon.csv").write_bytes(csv_text_crlf.encode("utf-8"))
    print("Successfully updated data/lexicon.csv")

    # 4. Write data/StaticLexicon.kt
    kt_lines = [
        "package com.nebulith.data",
        "",
        "/**",
        " * Autogenerated Static Lexicon for Nebulith (v23.1 - Standard Audit Compliant)",
        f" * Total vetted master entries: {len(vocab)}",
        " * Reorganized across 16 categories",
        " */",
        "data class LexiconEntry(",
        "    val id: Int,",
        "    val category: String,",
        "    val nrs: String,",
        "    val ipa: String,",
        "    val pos: String,",
        "    val meaningJa: String,",
        "    val meaningEn: String,",
        "    val notes: String",
        ")",
        "",
        "object StaticLexicon {",
        '    const val VERSION = "23.1"',
        f"    const val TOTAL_ENTRIES = {len(vocab)}",
        "",
        "    val entries: List<LexiconEntry> = listOf("
    ]

    for r in vocab:
        safe_ja = r["meaningJa"].replace('"', '\\"')
        safe_en = r["meaningEn"].replace('"', '\\"')
        safe_note = r["notes"].replace('"', '\\"')
        kt_lines.append(
            f'        LexiconEntry({r["id"]}, "{r["category"]}", "{r["nrs"]}", "{r["ipa"]}", "{r["pos"]}", "{safe_ja}", "{safe_en}", "{safe_note}"),'
        )

    kt_lines.extend([
        "    )",
        "}"
    ])
    kt_text_crlf = crlf_nl.join(kt_lines) + crlf_nl
    (ROOT / "data/StaticLexicon.kt").write_bytes(kt_text_crlf.encode("utf-8"))
    print("Successfully updated data/StaticLexicon.kt")

    # 5. Write docs/Nebulith Master Lexicon.md
    total_count = len(vocab)
    md_lines = [
        "# Nebulith Master Lexicon (星石語 統御語彙大系)",
        "",
        "> **Version**: 23.1 (Standard Audit Remediated - 1,008 Master Roots across 16 Categories)  ",
        "> **Design Principle**: Complete Purge of Earth Borrowings, De-confused Core Roots & Organic Irregularity  ",
        f"> **Progress**: {total_count} / 1000 roots ({total_count / 10:.1f}%) [GOAL ACHIEVED]  ",
        "> **Phonetic Base**: Sonorous vowels (a, e, i, o, u, y), liquid semivowels (r, l, v, w, j), resonant nasals (m, n), accented by restrained stops & fricatives (p, b, t, d, k, g, f, s, z, h). Strict exclusion of q, x.",
        "",
        "---",
        "",
        "## 16-Domain Category Overview (全16領域構成)",
        "",
        "| ID | カテゴリー名 (Domain) | 語彙数 (Words) | 構成比 | 概要 |",
        "|---|---|---|---|---|"
    ]

    for idx, cat in enumerate(CATEGORIES_ORDER, 1):
        count = cat_counts[cat]
        pct = (count / total_count) * 100
        desc = CAT_DESCRIPTIONS.get(cat, "")
        md_lines.append(f"| {idx} | **{cat}** | {count}語 | {pct:.1f}% | {desc} |")

    md_lines.extend([
        "",
        "---",
        "",
        "## 語彙目録 (Master Vocabulary Entries - 1,008 Roots)",
        ""
    ])

    current_cat = None
    for r in vocab:
        cat = r["category"]
        if cat != current_cat:
            current_cat = cat
            md_lines.extend([
                f"### {current_cat} ({cat_counts[current_cat]}語)",
                "",
                "| ID | 語根 (NRS) | IPA | 品詞 | 日本語意味 | 英語意味 | 語源・備考 |",
                "|---|---|---|---|---|---|---|"
            ])
        md_lines.append(f"| {r['id']} | **{r['nrs']}** | `{r['ipa']}` | {r['pos']} | {r['meaningJa']} | {r['meaningEn']} | {r['notes']} |")

    md_text_crlf = crlf_nl.join(md_lines) + crlf_nl
    (ROOT / "docs/Nebulith Master Lexicon.md").write_bytes(md_text_crlf.encode("utf-8"))
    print("Successfully updated docs/Nebulith Master Lexicon.md")
    print("Remediation of 4 master datasets completed successfully.")


if __name__ == "__main__":
    raise SystemExit('Legacy v23.1 migration is retired. Use tools/apply_reaudit02_fixes.py; do not reset current data.')
