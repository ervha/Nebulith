#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 7, Phase 11, Phase 15, Phase 19, & Phase 23:
Valnes Dialogues Companion Edition Builder (HTML / PDF / Markdown)
==================================================================
Compiles the 160 two-speaker everyday and craft dialogue scenarios and 480
zero-flag canonical compound words from data/verified_canonical_compounds.json,
plus a Domain/Category Index and a Constituent Root Cross-Reference Index,
into a source-backed companion volume of 『ヴァルネス遺聞』:
  - docs/Valnes_dialogues.html
  - docs/Valnes_dialogues.pdf
  - docs/VALNES_DIALOGUES_COMPANION.md
"""

import json
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from build_reviewed_codex import render_pdf
from canonical_compound_validator import audit_candidate_batch
from literary_layout import BOOK_CSS


def build_valnes_dialogues() -> dict:
    data_path = ROOT / "data/verified_canonical_compounds.json"
    dataset = json.loads(data_path.read_text(encoding="utf-8"))
    entries = dataset["entries"]
    scenarios = dataset["scenarios"]

    # Mechanical verification before building print/web artifacts
    report = audit_candidate_batch(entries, scenarios)
    if report["verdict"] != "ZERO_FLAGS_VERIFIED":
        raise ValueError(f"Cannot build Valnes Dialogues: audit flags present: {report['flagCounts']}")

    entries_by_scen = {}
    for row in entries:
        entries_by_scen.setdefault(row["scenario_id"], []).append(row)

    # Build category/domain index
    category_index = {}
    for row in entries:
        cat = row.get("category", "その他")
        category_index.setdefault(cat, []).append(row)

    # Build constituent root cross-reference index
    root_index = {}
    for row in entries:
        for c in row.get("constituentEntries", []):
            rn = c["nrs"]
            if rn not in root_index:
                root_index[rn] = {
                    "id": c["id"],
                    "nrs": rn,
                    "pos": c.get("pos", ""),
                    "meaningJa": c.get("meaningJa", "").split("、")[0],
                    "compounds": [],
                }
            root_index[rn]["compounds"].append(row)

    e = lambda text: escape(str(text))
    font = (ROOT / "fonts/font_b64.txt").read_text(encoding="utf-8").strip()

    css = BOOK_CSS + "@font-face{font-family:BookMincho;src:url(yumin.ttf);}"
    css += "@font-face{font-family:Nebulith;src:url(data:font/truetype;base64," + font + ") format('truetype');}"
    css += """
    .turn-box { margin: 6pt 0; padding: 6pt 10pt; border-left: 2pt solid #577488; background: #f7fafc; break-inside: avoid; }
    .speaker { font-weight: bold; color: #193b54; font-size: 9pt; }
    .turn-glyph { font-family: Nebulith; font-size: 13pt; color: #315e75; margin: 2pt 0; }
    .turn-nrs { font-family: Georgia, serif; font-size: 9.5pt; color: #183f58; margin: 2pt 0; }
    .turn-ja { font-size: 9pt; color: #24354a; margin: 2pt 0; }
    .compound-card { break-inside: avoid; padding: 6pt 0; border-bottom: 1px solid #d9e2e7; }
    .root-index-item { break-inside: avoid; padding: 4pt 0; border-bottom: 1px dashed #d9e2e7; font-size: 8.8pt; }
    """

    entry_count = len(entries)
    scen_count = len(scenarios)

    html_out = [
        '<!doctype html><html lang="ja"><meta charset="utf-8">',
        '<title>ヴァルネス遺聞・対話篇 — 灰環の暮らしと語らいの記録</title>',
        f'<style>{css}</style><body>',
        '<section class="cover">',
        '<p class="eyebrow">VALNES / DIALOGUES OF THE ASHEN CIRCLE</p>',
        '<p class="seal">◇</p>',
        '<h1>ヴァルネス遺聞・対話篇</h1>',
        f'<p class="subtitle">灰環の暮らしと語らいの記録（正本複合語{entry_count}選・{scen_count}対話・分野別＆語根別索引収録）</p>',
        '<p class="glyph">darfalun darterin havsirin talsilan</p>',
        '<p>写字生ユラ・灯守セヴ・採集師ネリ・舟守トアによる日常対話記録</p>',
        '<p class="muted">正本単独語根100%準拠・監査フラグ0件検証済み派生典籍 / 2026年 第4巻決定版</p>',
        '</section>',
        '<section class="section">',
        '<h2>凡例と編纂方針</h2>',
        f'<p>本巻『ヴァルネス遺聞・対話篇』は、正本辞書（<code>data/lexicon.json</code>）の自立語根のみを2語連結して構成された検証済み複合語{entry_count}語と、それらを実証する2話者対話シナリオ{scen_count}篇、および分野別索引・構成語根別クロスリファレンス索引を収録した派生典籍である。</p>',
        f'<p>収録された全{entry_count}語は、音素配列・無標コーダ・既存語重複ゼロ・構成語根の単独辞書実在性・英語グロスの純粋性・2話者による対話内再利用のすべてにおいて監査フラグ0件（<code>ZERO_FLAGS_VERIFIED</code>）を満たしている。</p>',
        '</section>',
        f'<section class="section"><h2>目次（全{scen_count}対話シナリオ＋双方向索引）</h2>'
    ]

    md_out = [
        "# ヴァルネス遺聞・対話篇 — 灰環の暮らしと語らいの記録",
        "",
        f"> **編纂区分**: 正本単独語根100%準拠・検証済み複合語{entry_count}語＋2話者対話{scen_count}篇＋分野別＆構成語根クロスリファレンス索引（`ZERO_FLAGS_VERIFIED`）",
        "",
        "## 目次",
        ""
    ]

    for idx, scen in enumerate(scenarios, 1):
        html_out.append(
            f'<p class="toc-item">第{idx}話（{e(scen["scenario_id"])} / {e(scen.get("batch", "Batch 1"))}）：'
            f'<b>{e(scen["title"])}</b> — <span class="muted">{e(scen["domain"])}</span></p>'
        )
        md_out.append(f"- **第{idx}話（{scen['scenario_id']}）**: {scen['title']}（{scen['domain']}）")

    html_out.append(f'<p class="toc-item"><b>巻末附録一：分野（カテゴリー）別正本複合語索引（全 {len(category_index)} 分野）</b></p>')
    html_out.append(f'<p class="toc-item"><b>巻末附録二：構成語根別クロスリファレンス索引（正本語根 {len(root_index)} 項目）</b></p>')
    html_out.append('</section>')
    md_out.append(f"- **巻末附録一**: 分野（カテゴリー）別正本複合語索引（全 {len(category_index)} 分野）")
    md_out.append(f"- **巻末附録二**: 構成語根別クロスリファレンス索引（正本語根 {len(root_index)} 項目）")
    md_out.append("")

    # Render each scenario chapter
    for idx, scen in enumerate(scenarios, 1):
        sid = scen["scenario_id"]
        a_name = scen["agent_a"]["name"]
        a_role = scen["agent_a"]["role"]
        b_name = scen["agent_b"]["name"]
        b_role = scen["agent_b"]["role"]
        scen_words = entries_by_scen.get(sid, [])

        html_out.append(f'<section class="section" id="{e(sid)}">')
        html_out.append(f'<p class="eyebrow">{e(sid)} / {e(scen.get("batch", "Batch 1"))} — {e(scen["domain"])}</p>')
        html_out.append(f'<h2>第{idx}話　{e(scen["title"])}</h2>')
        html_out.append(
            f'<p class="note"><b>対話者</b>：{e(a_name)}（{e(a_role)}） ＆ {e(b_name)}（{e(b_role)}）<br>'
            f'<b>場面の背景</b>：{e(scen["communicative_need"])}</p>'
        )

        md_out.extend([
            f"## 第{idx}話　{scen['title']} (`{sid}`)",
            f"- **領域**: {scen['domain']} ({scen.get('batch', 'Batch 1')})",
            f"- **対話者**: {a_name}（{a_role}） / {b_name}（{b_role}）",
            f"- **背景**: {scen['communicative_need']}",
            "",
            "### 対話記録",
            ""
        ])

        for t in scen["turns"]:
            html_out.append(
                f'<div class="turn-box">'
                f'<div class="speaker">{e(t["speaker"])}</div>'
                f'<div class="turn-glyph">{e(t["nebulith"])}</div>'
                f'<div class="turn-nrs">{e(t["nebulith"])}</div>'
                f'<div class="turn-ja">{e(t["japanese"])}</div>'
                f'</div>'
            )
            md_out.append(f"- **{t['speaker']}**: *{t['nebulith']}*  \n  「{t['japanese']}」")

        html_out.append('<h3>本話で実証された正本複合語</h3>')
        md_out.extend(["", "### 実証された正本複合語", ""])

        for w in scen_words:
            anchor = f"compound-{w['nrs']}"
            c_info = " ＋ ".join(
                f"{c['nrs']} (#{c['id']}: {c['meaningJa'].split('、')[0]})"
                for c in w.get("constituentEntries", [])
            )
            html_out.append(
                f'<div class="compound-card" id="{e(anchor)}">'
                f'<b class="root">{e(w["nrs"])}</b>　<span class="muted">[{e(w["pos"])}] #{w["id"]}</span>　'
                f'<b>{e(w["meaningJa"])}</b> / <span class="muted">{e(w["meaningEn"])}</span>'
                f'<div class="muted">語構成：{e(w["etymology"])}（正本語根：{e(c_info)}）｜実証話者：{e(", ".join(w.get("speakers", [])))}</div>'
                f'<div class="muted">代表例文：<code>{e(w["example_sentence"])}</code> — {e(w["example_ja"])}</div>'
                f'</div>'
            )
            md_out.append(
                f"- **`{w['nrs']}`** (`#{w['id']}`, {w['pos']}): {w['meaningJa']} / *{w['meaningEn']}*  \n"
                f"  - 語構成: `{w['etymology']}` ({c_info})  \n"
                f"  - 例文: `{w['example_sentence']}` （{w['example_ja']}）"
            )

        html_out.append('</section>')
        md_out.append("")

    # Render Appendix 1: Category / Domain Index
    html_out.append('<section class="section" id="domain-category-index">')
    html_out.append('<p class="eyebrow">APPENDIX I / DOMAIN & CATEGORY INDEX</p>')
    html_out.append(f'<h2>巻末附録一　分野（カテゴリー）別正本複合語索引（全 {len(category_index)} 分野）</h2>')
    html_out.append('<p class="note">収録された検証済み正本複合語の意味分野別一覧。</p>')

    md_out.extend([
        f"## 巻末附録一　分野（カテゴリー）別正本複合語索引（全 {len(category_index)} 分野）",
        "",
    ])

    for cat in sorted(category_index.keys()):
        cwords = category_index[cat]
        comp_links = " / ".join(
            f"{cw['nrs']}（{cw['meaningJa'].split('、')[0]} : {cw['scenario_id']}）"
            for cw in cwords
        )
        html_out.append(
            f'<div class="root-index-item">'
            f'<b>{e(cat)}</b> <span class="muted">({len(cwords)} 語)</span> → {e(comp_links)}'
            f'</div>'
        )
        md_out.append(f"- **{cat}** ({len(cwords)} 語) → {comp_links}")

    html_out.append('</section>')
    md_out.append("")

    # Render Appendix 2: Constituent Root Cross-Reference Index
    html_out.append('<section class="section" id="constituent-root-index">')
    html_out.append('<p class="eyebrow">APPENDIX II / CONSTITUENT ROOT CROSS-REFERENCE INDEX</p>')
    html_out.append(f'<h2>巻末附録二　構成語根別クロスリファレンス索引（全 {len(root_index)} 語根）</h2>')
    html_out.append('<p class="note">正本辞書（<code>data/lexicon.json</code>）の各単独語根から派生した正本複合語の一覧。</p>')

    md_out.extend([
        f"## 巻末附録二　構成語根別クロスリファレンス索引（全 {len(root_index)} 語根）",
        "",
    ])

    for rn in sorted(root_index.keys()):
        rinfo = root_index[rn]
        comp_links = " / ".join(
            f"{cw['nrs']}（{cw['meaningJa'].split('、')[0]} : {cw['scenario_id']}）"
            for cw in rinfo["compounds"]
        )
        html_out.append(
            f'<div class="root-index-item">'
            f'<b>{e(rn)}</b> <span class="muted">(#{rinfo["id"]} [{e(rinfo["pos"])}] {e(rinfo["meaningJa"])})</span> '
            f'→ {e(comp_links)}'
            f'</div>'
        )
        md_out.append(f"- **`{rn}`** (`#{rinfo['id']}`, {rinfo['meaningJa']}) → {comp_links}")

    html_out.append('</section>')
    html_out.append('</body></html>')

    html_path = ROOT / "docs/Valnes_dialogues.html"
    pdf_path = ROOT / "docs/Valnes_dialogues.pdf"
    md_path = ROOT / "docs/VALNES_DIALOGUES_COMPANION.md"

    html_path.write_text("\n".join(html_out) + "\n", encoding="utf-8")
    md_path.write_text("\n".join(md_out) + "\n", encoding="utf-8")
    render_pdf(html_path, pdf_path)

    return {
        "html": str(html_path.relative_to(ROOT)).replace("\\", "/"),
        "pdf": str(pdf_path.relative_to(ROOT)).replace("\\", "/"),
        "markdown": str(md_path.relative_to(ROOT)).replace("\\", "/"),
        "entries": len(entries),
        "scenarios": len(scenarios),
        "indexedCategories": len(category_index),
        "indexedRoots": len(root_index),
        "pdfBytes": pdf_path.stat().st_size,
    }


if __name__ == "__main__":
    res = build_valnes_dialogues()
    print(json.dumps(res, ensure_ascii=False, indent=2))
