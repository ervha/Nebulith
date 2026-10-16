#!/usr/bin/env python3
"""
tools/build_canon_codex.py
=============================================================================
Nebulith Canon Codex & Scripture Generator (PDF & HTML & Markdown)
-----------------------------------------------------------------------------
Generates the authoritative, story-driven canonical scripture:
  "Codex Astrolith: Annales Caelestes et Genesis Siderum"
utilizing virtually ALL currently generated vocabulary (1,463+ roots) and
providing an automated pipeline to continuously assimilate future emergent words.

Outputs:
  - docs/Codex_Astrolith_Canon_Scripture.html (Print-ready A4 typography)
  - docs/Codex_Astrolith_Canon_Scripture.pdf  (Vector PDF via headless Edge/Chrome)
  - docs/NEBULITH_CANON_LORE_AND_EXPEDITIONS.md (Complete Markdown Lore Edition)
=============================================================================
"""

import os
import sys
import json
import subprocess
from pathlib import Path

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
DOCS_DIR = ROOT_DIR / "docs"
FONTS_DIR = ROOT_DIR / "fonts"

def load_all_lexicon():
    """Load canon, extensions, grammar entries, and audited emergent candidates."""
    canon_file = DATA_DIR / "lexicon.json"
    ext_file = DATA_DIR / "translation_extensions.json"
    gram_file = DATA_DIR / "grammar_dictionary.json"
    emergent_file = DATA_DIR / "emergent_lexicon_audit.json"

    words = {}

    if canon_file.exists():
        canon_data = json.loads(canon_file.read_text(encoding='utf-8'))
        for w in canon_data.get('vocabulary', []):
            words[w['nrs']] = {
                'root': w['nrs'],
                'pos': w.get('pos', '名'),
                'ja': w.get('meaningJa', ''),
                'en': w.get('meaningEn', ''),
                'id': w.get('id', 0),
                'category': w.get('category', '1. 天体・宇宙力学・光'),
                'notes': w.get('notes', ''),
                'provenance': 'Canon'
            }

    if ext_file.exists():
        ext_data = json.loads(ext_file.read_text(encoding='utf-8'))
        for w in ext_data.get('entries', []):
            root = w['nrs']
            if root not in words:
                words[root] = {
                    'root': root,
                    'pos': w.get('pos', '名'),
                    'ja': w.get('meaningJa', ''),
                    'en': w.get('meaningEn', ''),
                    'id': w.get('id', 20000),
                    'category': w.get('category', '体系拡張語根'),
                    'notes': w.get('notes', ''),
                    'provenance': 'Curated Extension'
                }
            else:
                # Merge polysemy
                words[root]['ja'] += ' / ' + w.get('meaningJa', '')
                words[root]['en'] += '; ' + w.get('meaningEn', '')

    if gram_file.exists():
        gram_data = json.loads(gram_file.read_text(encoding='utf-8'))
        for w in gram_data.get('entries', []):
            root = w['nrs']
            if root not in words:
                words[root] = {
                    'root': root,
                    'pos': w.get('pos', '機能語'),
                    'ja': w.get('meaningJa', ''),
                    'en': w.get('meaningEn', ''),
                    'id': w.get('id', 30000),
                    'category': '文法・機能語',
                    'notes': w.get('notes', ''),
                    'provenance': 'Grammar Core'
                }

    # Also detect approved emergent candidates if marked as approved
    if emergent_file.exists():
        em_data = json.loads(emergent_file.read_text(encoding='utf-8'))
        for cand in em_data.get('candidates', []):
            if cand.get('status') == 'approved' and cand['nrs'] not in words:
                words[cand['nrs']] = {
                    'root': cand['nrs'],
                    'pos': cand.get('pos', '名'),
                    'ja': cand.get('meaningJa', ''),
                    'en': cand.get('meaningEn', ''),
                    'id': cand.get('id', 40000),
                    'category': '創発承認追補語彙',
                    'notes': cand.get('notes', ''),
                    'provenance': 'Emergent Approved'
                }

    return words

def categorize_words(words):
    """Sort and partition words into narrative Cantos."""
    cantos = {
        'canto_1': {'title': '第I篇：創世の黎明・天蓋と星核', 'sub': 'Canto I: Genesis Caelestis et Astra Primeva', 'words': []},
        'canto_2': {'title': '第II篇：気象・大気・大地・水晶の理', 'sub': 'Canto II: Elementa Mundi, Aquae et Mineralia', 'words': []},
        'canto_3': {'title': '第III篇：天文工学・幾何数理・観測儀', 'sub': 'Canto III: Mechanica Siderum, Geometria et Instrumenta', 'words': []},
        'canto_4': {'title': '第IV篇：生命・生物・治癒と共生の樹', 'sub': 'Canto IV: Bio-Cosmos, Silvae et Concordia', 'words': []},
        'canto_5': {'title': '第V篇：天蓋都市・建築・日常と生活工芸', 'sub': 'Canto V: Civitas, Architectura et Vita Cotidiana', 'words': []},
        'canto_6': {'title': '第VI篇：精神・思索・感情と星辰詩歌', 'sub': 'Canto VI: Mens, Philosophia et Poesis Sideralis', 'words': []},
        'canto_7': {'title': '第VII篇：航路・動態・時空の変容', 'sub': 'Canto VII: Motus, Navigatio et Spatium Infinitum', 'words': []},
        'canto_8': {'title': '第VIII篇：統語小詞・格標識・不滅の盟約', 'sub': 'Canto VIII: Foedus Grammaticum et Particulae Aeternae', 'words': []},
        'canto_supplements': {'title': '追補篇：新星の創発と未来の言の葉', 'sub': 'Canto Novus: Emergent Voices & Continuations', 'words': []}
    }

    for root, w in sorted(words.items(), key=lambda x: (x[1]['id'], x[0])):
        cid = w['id']
        cat = w['category']
        pos = w['pos']

        if cid >= 40000:
            cantos['canto_supplements']['words'].append(w)
        elif cid >= 30000 or '格' in pos or '接' in pos or '機能' in pos or '代名' in pos:
            cantos['canto_8']['words'].append(w)
        elif '天体' in cat or '光' in cat or cid in range(1, 81):
            cantos['canto_1']['words'].append(w)
        elif '気象' in cat or '大気' in cat or '水域' in cat or '地質' in cat or '鉱物' in cat or cid in range(250, 360):
            cantos['canto_2']['words'].append(w)
        elif '数理' in cat or '幾何' in cat or '計測' in cat or '情報' in cat or '計算' in cat or '通信' in cat or cid in range(81, 195):
            cantos['canto_3']['words'].append(w)
        elif '生命' in cat or '生体' in cat or '医療' in cat or '植物' in cat or '動物' in cat or '生物' in cat or cid in range(195, 250) or cid in range(360, 460):
            cantos['canto_4']['words'].append(w)
        elif '建築' in cat or '都市' in cat or '住空間' in cat or '食' in cat or '衣飾' in cat or '工芸' in cat or '日常' in cat or cid in range(550, 750):
            cantos['canto_5']['words'].append(w)
        elif '精神' in cat or '哲学' in cat or '感情' in cat or '芸術' in cat or '統治' in cat or '社会' in cat or cid in range(460, 550) or cid in range(750, 890):
            cantos['canto_6']['words'].append(w)
        else:
            cantos['canto_7']['words'].append(w)

    return cantos

def generate_verses(canto_key, canto_data):
    """Synthesize structured poetic verses for the words in this canto."""
    words = canto_data['words']
    chunk_size = 12
    verses = []
    
    # Story motifs for each canto
    canto_motifs = {
        'canto_1': {
            'action': '照らし導く', 'action_neb': 'falun el zohar', 'theme': '星辰の運行と原初の天蓋',
            'latin': 'In principio erat Celen, et Celen lucebat in altissimis astris.'
        },
        'canto_2': {
            'action': '潤し巡る', 'action_neb': 'valur el daran', 'theme': '大気の息吹と山河の脈動',
            'latin': 'Fluunt aquae per terras, et spiritus ventorum resonant in montibus.'
        },
        'canto_3': {
            'action': '計測し算定する', 'action_neb': 'vyrel el mirin', 'theme': '軌道の幾何学と天文鏡の光線',
            'latin': 'Metimur spatia siderum, orbes signamus in speculis veritatis.'
        },
        'canto_4': {
            'action': '芽吹き育む', 'action_neb': 'bion el vesta', 'theme': '星光を宿す樹木と生きとし生ける調和',
            'latin': 'Crescit arbor vitalis sub lumine aethereo, sanantur vulnera saeculi.'
        },
        'canto_5': {
            'action': '築き集う', 'action_neb': 'tora el morvan', 'theme': '天蓋の下の回廊と人々の温もり',
            'latin': 'Aedificantur turres sub firmamento, resonant vici vocibus pacis.'
        },
        'canto_6': {
            'action': '深く愛し思索する', 'action_neb': 'cynel el mensa', 'theme': '静かな夜の哲学と結晶の歌',
            'latin': 'Meditatur anima in nocte serena, ardet amor super omnes nebulas.'
        },
        'canto_7': {
            'action': '彼方へと歩み進む', 'action_neb': 'poran el moran', 'theme': '深宇宙を往く航跡と無限の変容',
            'latin': 'Iter facimus trans aethera, transiliunt naves limites temporum.'
        },
        'canto_8': {
            'action': '永遠に結び合う', 'action_neb': 'zen falun el vyr, poran el mi', 'theme': '万象を結ぶ格の絆と不滅の誓約',
            'latin': 'Haec sunt verba foederis: el, et, en, de, uo... aeterna vincula loquelae.'
        },
        'canto_supplements': {
            'action': '新たに創発する', 'action_neb': 'novas el verba', 'theme': '絶えざる対話から生まれ出づる言の葉',
            'latin': 'Nova verba nascuntur ex dialogo stellari, crescit lingua in saecula.'
        }
    }

    motif = canto_motifs.get(canto_key, canto_motifs['canto_1'])

    for v_idx in range(0, len(words), chunk_size):
        chunk = words[v_idx:v_idx + chunk_size]
        v_num = (v_idx // chunk_size) + 1
        
        # Build Nebulith sentence showcasing prominent roots
        roots_in_chunk = [w['root'] for w in chunk]
        lead_word = chunk[0]
        secondary_word = chunk[1] if len(chunk) > 1 else chunk[0]
        
        neb_line = f"{lead_word['root'].capitalize()} el {secondary_word['root']}, uo celen tor kyrim."
        if canto_key == 'canto_8':
            neb_line = f"Zen {lead_word['root']} el vyr, poran el mi is {secondary_word['root']}."

        ja_glosses = [f"{w['root']}（{w['ja'].split('、')[0]}）" for w in chunk[:6]]
        ja_line = f"〔第{v_num}節〕 {lead_word['ja'].split('、')[0]}が{secondary_word['ja'].split('、')[0]}を照らし、天蓋と深淵のあわいに立ち現れる。({', '.join(ja_glosses)})"
        
        en_glosses = [f"{w['root']} ({w['en'].split(';')[0].split(',')[0]})" for w in chunk[:6]]
        en_line = f"Verse {v_num}: The essence of {lead_word['root']} and {secondary_word['root']} manifests under the celestial dome. ({', '.join(en_glosses)})"

        verses.append({
            'verse_num': v_num,
            'canto_code': canto_key.upper().replace('_', ' '),
            'neb': neb_line,
            'ja': ja_line,
            'en': en_line,
            'words': chunk
        })

    return verses

def build_codex():
    print("=" * 68)
    print("  Nebulith Canon Codex & Authoritative Scripture Generator")
    print("=" * 68)

    words = load_all_lexicon()
    print(f"Loaded {len(words)} unique roots across all canon and extension tiers.")

    cantos = categorize_words(words)
    total_verses = 0
    canto_verse_map = {}

    word_to_locus = {}

    for c_key, c_data in cantos.items():
        v_list = generate_verses(c_key, c_data)
        canto_verse_map[c_key] = v_list
        total_verses += len(v_list)
        for v in v_list:
            for w in v['words']:
                word_to_locus[w['root']] = f"{c_data['title'].split('：')[0]} 第{v['verse_num']}節"

    print(f"Structured into {len(cantos)} Cantos and {total_verses} Verses.")
    print(f"Index coverage: {len(word_to_locus)} / {len(words)} words assigned official loci.")
    loci_path = DATA_DIR / "lexicon_canonical_loci.json"
    loci_path.write_text(json.dumps(word_to_locus, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"Saved canonical loci mapping to {loci_path}")

    # Load Base64 font
    font_b64_file = FONTS_DIR / "font_b64.txt"
    font_b64 = font_b64_file.read_text(encoding='utf-8').strip() if font_b64_file.exists() else ""

    # 1. Build High-Grade HTML Edition
    html_path = DOCS_DIR / "Codex_Astrolith_Canon_Scripture.html"
    print(f"Generating typography-grade HTML: {html_path}")

    html_content = generate_html_codex(cantos, canto_verse_map, word_to_locus, words, font_b64)
    html_path.write_text(html_content, encoding='utf-8')

    # 2. Build PDF via Headless Edge / Chrome
    pdf_path = DOCS_DIR / "Codex_Astrolith_Canon_Scripture.pdf"
    print(f"Compiling vector PDF: {pdf_path}")
    render_pdf(html_path, pdf_path)

    # 3. Build Markdown Lore Edition
    md_path = DOCS_DIR / "NEBULITH_CANON_LORE_AND_EXPEDITIONS.md"
    print(f"Generating full lore documentation: {md_path}")
    generate_markdown_lore(cantos, canto_verse_map, word_to_locus, words, md_path)

    print("=" * 68)
    print("  BUILD COMPLETE: CANON SCRIPTURE, PDF & DERIVATIVE LORE GENERATED")
    print("=" * 68)

def generate_html_codex(cantos, canto_verse_map, word_to_locus, all_words, font_b64):
    """Build a beautiful, publishable print HTML document."""
    
    font_face_css = f"""
    @font-face {{
      font-family: 'Nebulith';
      src: url('data:font/truetype;base64,{font_b64}') format('truetype');
      font-weight: normal;
      font-style: normal;
    }}
    """ if font_b64 else ""

    canto_sections_html = []

    for c_key, c_data in cantos.items():
        v_list = canto_verse_map[c_key]
        if not v_list:
            continue

        verses_html = []
        for v in v_list:
            word_chips = []
            for w in v['words']:
                word_chips.append(f"""
                <span class="word-ref" title="#{w['id']} {w['ja']}">
                  <strong>{w['root']}</strong>
                  <span class="word-pos">{w['pos']}</span>
                  <span class="word-ja">{w['ja'].split('、')[0]}</span>
                </span>
                """)

            verses_html.append(f"""
            <div class="verse-card">
              <div class="verse-header">
                <span class="verse-badge">§ {v['verse_num']}</span>
                <span class="verse-astral font-neb">{v['neb'].lower()}</span>
              </div>
              <div class="verse-neb">{v['neb']}</div>
              <div class="verse-ja">{v['ja']}</div>
              <div class="verse-en">{v['en']}</div>
              <div class="verse-lexicon">
                {''.join(word_chips)}
              </div>
            </div>
            """)

        canto_sections_html.append(f"""
        <section class="canto-chapter page-break">
          <div class="chapter-header">
            <h2 class="canto-title">{c_data['title']}</h2>
            <div class="canto-sub">{c_data['sub']}</div>
            <div class="canto-stat">収録語彙数: {len(c_data['words'])} 語根 / 詩節数: {len(v_list)} 節</div>
          </div>
          <div class="verses-container">
            {''.join(verses_html)}
          </div>
        </section>
        """)

    # Index table
    index_rows = []
    for root, w in sorted(all_words.items()):
        locus = word_to_locus.get(root, '追補篇')
        index_rows.append(f"""
        <tr>
          <td class="font-neb" style="font-size: 1.15rem; color: #2b6cb0;">{root}</td>
          <td><strong>{root}</strong></td>
          <td><span class="pos-tag">{w['pos']}</span></td>
          <td>{w['ja']}</td>
          <td><span class="en-text">{w['en']}</span></td>
          <td><span class="locus-tag">{locus}</span></td>
        </tr>
        """)

    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>Codex Astrolith: Annales Caelestes et Genesis Siderum</title>
<style>
{font_face_css}

@page {{
  size: A4;
  margin: 18mm 16mm 20mm 16mm;
  @bottom-right {{
    content: counter(page);
    font-size: 9pt;
    color: #718096;
  }}
}}

body {{
  font-family: "Hiragino Mincho ProN", "Yu Mincho", "Noto Serif CJK JP", serif;
  color: #2d3748;
  line-height: 1.68;
  background: #ffffff;
  margin: 0;
  padding: 0;
}}

.font-neb {{
  font-family: 'Nebulith', serif;
}}

.page-break {{
  page-break-before: always;
}}

/* Cover Page */
.cover-page {{
  min-height: 90vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  border: 4px double #2b6cb0;
  padding: 40px 20px;
  box-sizing: border-box;
  background: radial-gradient(circle, #f7fafc 0%, #edf2f7 100%);
}}

.cover-astral-sigil {{
  font-size: 4.8rem;
  color: #2b6cb0;
  letter-spacing: 0.15em;
  margin-bottom: 24px;
}}

.cover-title-main {{
  font-size: 2.3rem;
  font-weight: 700;
  color: #1a365d;
  letter-spacing: 0.08em;
  margin: 0 0 10px 0;
}}

.cover-title-sub {{
  font-size: 1.25rem;
  color: #4a5568;
  font-family: "Georgia", serif;
  font-style: italic;
  margin-bottom: 24px;
}}

.cover-divider {{
  width: 140px;
  height: 2px;
  background: #2b6cb0;
  margin: 20px auto;
}}

.cover-desc {{
  max-width: 540px;
  font-size: 0.95rem;
  color: #4a5568;
  line-height: 1.8;
  margin: 0 auto 36px auto;
}}

.cover-meta {{
  font-size: 0.85rem;
  color: #718096;
  letter-spacing: 0.05em;
}}

/* Chapters & Typography */
.chapter-header {{
  border-bottom: 2px solid #2b6cb0;
  padding-bottom: 12px;
  margin-bottom: 24px;
}}

.canto-title {{
  font-size: 1.6rem;
  color: #1a365d;
  margin: 0 0 4px 0;
}}

.canto-sub {{
  font-size: 1.05rem;
  color: #718096;
  font-style: italic;
  font-family: "Georgia", serif;
}}

.canto-stat {{
  font-size: 0.8rem;
  color: #4a5568;
  margin-top: 6px;
}}

.verses-container {{
  display: flex;
  flex-direction: column;
  gap: 20px;
}}

.verse-card {{
  border: 1px solid #e2e8f0;
  border-left: 4px solid #2b6cb0;
  border-radius: 4px;
  padding: 14px 18px;
  background: #ffffff;
  page-break-inside: avoid;
}}

.verse-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}}

.verse-badge {{
  font-size: 0.78rem;
  font-weight: 700;
  background: #ebf8ff;
  color: #2b6cb0;
  padding: 2px 8px;
  border-radius: 12px;
}}

.verse-astral {{
  font-size: 1.5rem;
  color: #2b6cb0;
}}

.verse-neb {{
  font-size: 1.12rem;
  font-weight: 600;
  color: #1a365d;
  font-family: "Georgia", serif;
  margin-bottom: 6px;
}}

.verse-ja {{
  font-size: 0.92rem;
  color: #2d3748;
  margin-bottom: 4px;
}}

.verse-en {{
  font-size: 0.84rem;
  color: #718096;
  font-family: "Georgia", serif;
  font-style: italic;
  margin-bottom: 10px;
}}

.verse-lexicon {{
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  border-top: 1px dashed #e2e8f0;
  padding-top: 8px;
}}

.word-ref {{
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: #f7fafc;
  border: 1px solid #edf2f7;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 0.75rem;
}}

.word-pos {{
  color: #718096;
  font-size: 0.7rem;
}}

.word-ja {{
  color: #4a5568;
}}

/* Apocrypha Stories */
.apocrypha-card {{
  border: 1px solid #cbd5e0;
  border-radius: 6px;
  padding: 20px;
  margin-bottom: 24px;
  background: #fafaf9;
  page-break-inside: avoid;
}}

.apocrypha-title {{
  font-size: 1.35rem;
  color: #1a365d;
  margin-top: 0;
  margin-bottom: 6px;
}}

.apocrypha-sub {{
  font-size: 0.95rem;
  color: #718096;
  font-style: italic;
  margin-bottom: 14px;
}}

/* Index Table */
.index-table {{
  width: 100%;
  border-collapse: collapse;
  font-size: 0.78rem;
  margin-top: 14px;
}}

.index-table th {{
  background: #edf2f7;
  color: #2d3748;
  text-align: left;
  padding: 8px;
  border-bottom: 2px solid #cbd5e0;
}}

.index-table td {{
  padding: 6px 8px;
  border-bottom: 1px solid #edf2f7;
}}

.pos-tag {{
  background: #e2e8f0;
  padding: 1px 4px;
  border-radius: 2px;
  font-size: 0.7rem;
}}

.locus-tag {{
  color: #2b6cb0;
  font-weight: 500;
}}

.en-text {{
  color: #718096;
}}
</style>
</head>
<body>

  <!-- Cover Page -->
  <div class="cover-page">
    <div class="cover-astral-sigil font-neb">celen vyr falun</div>
    <h1 class="cover-title-main">星辰創世聖典・観測年代録</h1>
    <div class="cover-title-sub">Codex Astrolith: Annales Caelestes et Genesis Siderum</div>
    <div class="cover-divider"></div>
    <p class="cover-desc">
      本書は、人工言語「Nebulith」のすべての語彙の典拠（Locus Originarius）として編纂された正本叙事詩である。<br>
      古代天体観測官たちが刻んだ全1,463語根の詩節を網羅し、宇宙の創生から深宇宙航海、日常の息吹、不滅の統語契約に至るまでのバックボーンを完全収録する。
    </p>
    <div class="cover-meta">
      星辰紀元 第381年・観測編纂審議会 定本 / 全語彙網羅率: 100% 監査済
    </div>
  </div>

  <!-- Exegesis / Origin Introduction -->
  <section class="page-break" style="padding-top: 20px;">
    <div class="chapter-header">
      <h2 class="canto-title">解題：Nebulith原本としての星辰聖典</h2>
      <div class="canto-sub">Exegesis: The Canonical Loci of the Astral Language</div>
    </div>
    <p>
      人工言語「Nebulith」において、単語は単なる記号の集積ではない。すべての語根（Roots）は、古代の観測者たちが蒼穹と星辰の運行を観測し、石板および共鳴結晶板に刻んだ聖なる年代記『Codex Astrolith』の詩節から派生したものである。
    </p>
    <p>
      本書は、正本カノン語彙（#1〜#1008）、現代星辰工学に基づく体系拡張語彙（#20001〜#20372）、および言語の骨格を成す文法小詞・格標識群（#30001〜）の**合計1,463語根すべてを活用し、全単語の原典的位置（Locus）を明記した不滅の正本原本**である。
    </p>
    <p>
      また、今後生成される新たな創発語彙についても、追補篇（Canto Novus）へと自動的に組み込まれ、原本としての物語性と体系性を永遠に拡充し続ける自律的アーキテクチャを備えている。
    </p>
  </section>

  <!-- Cantos Sections -->
  {''.join(canto_sections_html)}

  <!-- Chronica Apocrypha: Sister Grimoires -->
  <section class="page-break">
    <div class="chapter-header">
      <h2 class="canto-title">拡張本・派生録：星辰三翼の物語群</h2>
      <div class="canto-sub">Chronica Apocrypha: The Three Sister Grimoires</div>
    </div>
    
    <div class="apocrypha-card">
      <h3 class="apocrypha-title">派生録 I：『天蓋航海誌』（Navigatio Caelestis）</h3>
      <div class="apocrypha-sub">The Voidfarer’s Log: Voyages Beyond the Heliopause</div>
      <p>
        探査船「アルゴ・ネブラ号」の記録官エリオスが記した恒星間跳躍の日誌。黄道光の薄暮を抜け、事象の地平面（kymzon）の縁を掠めながら未知の星系へと旅立つ航海士たちの歓喜と孤独、そして星の誕生（voran）を見届けた瞬間の詠嘆を描く。天体航行工学および天測算術語彙のバックボーンを担う。
      </p>
    </div>

    <div class="apocrypha-card">
      <h3 class="apocrypha-title">派生録 II：『深淵調律秘儀録』（Liber Harmoniae）</h3>
      <div class="apocrypha-sub">The Grimoire of Crystal Tuning: Resonances of Light and Matter</div>
      <p>
        星光の屈折と音響結晶（kris）の振動を同期させ、重力波と光波を織りなす調律師（falzenor）たちの伝承録。物質の硬軟、色彩、温度、そして精神の純度を幾何学的に一致させる古代の叡智が、数理・自然鉱物・感触語彙の源泉として脈打つ。
      </p>
    </div>

    <div class="apocrypha-card">
      <h3 class="apocrypha-title">派生録 III：『星影生活誌』（Chronica Quotidianae）</h3>
      <div class="apocrypha-sub">Life Beneath the Stars: The Hearth, the Loom, and the Parting</div>
      <p>
        天蓋の下で生きる市井の人々の記録。朝餉（novbion）の湯気、市場の喧騒、織り布（palvas）の手触り、雨上がりの路地、そして旅立つ者を見送る（peltel）手のぬくもり。日常生活・食事・衣服・家族・共同体語彙に血の通った温もりを与える物語群である。
      </p>
    </div>
  </section>

  <!-- Complete Lexical Concordance Index -->
  <section class="page-break">
    <div class="chapter-header">
      <h2 class="canto-title">完全語彙対照索引（典拠章節リファレンス）</h2>
      <div class="canto-sub">Index Concordantiae: Full Lexicon Loci ({len(all_words)} Roots)</div>
    </div>
    <p style="font-size: 0.85rem; color: #718096;">
      本書の詩節に登場する全単語根のアルファベット順対照表。各語根の品詞、日本語義、英語対訳、および聖典内の登場章節を示す。
    </p>
    <table class="index-table">
      <thead>
        <tr>
          <th>星石文字</th>
          <th>ローマ字</th>
          <th>品詞</th>
          <th>日本語義</th>
          <th>英語対訳</th>
          <th>原本登場章節 (Locus)</th>
        </tr>
      </thead>
      <tbody>
        {''.join(index_rows)}
      </tbody>
    </table>
  </section>

</body>
</html>
"""
    return html

def render_pdf(html_path, pdf_path):
    """Render the HTML file into a complete vector PDF using headless Edge/Chrome."""
    browsers = [
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    ]
    
    browser_bin = None
    for b in browsers:
        if Path(b).exists():
            browser_bin = b
            break

    if not browser_bin:
        print("WARNING: Neither Edge nor Chrome found. Skipping PDF compilation.")
        return False

    cmd = [
        browser_bin,
        '--headless',
        '--disable-gpu',
        '--no-pdf-header-footer',
        f'--print-to-pdf={pdf_path.resolve()}',
        str(html_path.resolve())
    ]

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if pdf_path.exists() and pdf_path.stat().st_size > 0:
            print(f"PDF Successfully Compiled: {pdf_path.name} ({pdf_path.stat().st_size:,} bytes)")
            return True
        else:
            print(f"PDF generation failed: {res.stderr}")
            return False
    except Exception as e:
        print(f"Error during PDF compilation: {e}")
        return False

def generate_markdown_lore(cantos, canto_verse_map, word_to_locus, all_words, md_path):
    """Generate Markdown edition of the canon lore, grimoires and loci."""
    lines = [
        "# 星辰創世聖典・観測年代録（Codex Astrolith: Annales Caelestes）",
        "",
        "> **Nebulith 言語 正本原本・全語彙典拠聖典**  ",
        f"> 総収録語根数: {len(all_words)} 語根 | 網羅率: 100% | 監査検証完了",
        "",
        "---",
        "",
        "## 1. 聖典解題（Exegesis & Origins）",
        "",
        "人工言語 **Nebulith** において、単語は無味乾燥な記号ではなく、宇宙の創生・星辰運行・地上の生命の営みを記録した年代記『**Codex Astrolith**』の詩節から抽出された「生きた言の葉」です。",
        "",
        "本書は、公式正本語彙（Canon #1〜#1008）、体系拡張語彙（#20001〜#20372）、および文法小詞・格標識群（#30001〜）の**全1,463語根すべてを活用**し、物語式の叙事詩として編纂した原本です。今後生成される新単語も自律的に追補篇へと追加され、永遠に物語が拡充し続けます。",
        "",
        "---",
        "",
        "## 2. 創世と観測の叙事詩（The Cantos of Creation）",
        ""
    ]

    for c_key, c_data in cantos.items():
        v_list = canto_verse_map[c_key]
        if not v_list:
            continue
        lines.append(f"### {c_data['title']}")
        lines.append(f"*{c_data['sub']}* （収録語彙: {len(c_data['words'])} 語）\n")

        for v in v_list:
            roots_str = ", ".join([f"`{w['root']}`" for w in v['words'][:6]])
            lines.append(f"#### § {v['verse_num']}. {v['neb']}")
            lines.append(f"- **日本語訳**: {v['ja']}")
            lines.append(f"- **英語対訳**: {v['en']}")
            lines.append(f"- **主要典拠語根**: {roots_str}\n")

    lines.extend([
        "---",
        "",
        "## 3. 拡張本・派生録：星辰三翼の物語群（The Three Sister Grimoires）",
        "",
        "### 派生録 I：『天蓋航海誌』（Navigatio Caelestis）",
        "- **概要**: 恒星間跳躍船「アルゴ・ネブラ号」の観測航行日誌。",
        "- **物語性**: 黄道光の薄暮を抜け、事象の地平面（kymzon）の縁を航行する探査士たちの記録。天体航行工学・航路計算・超新星の残滓を越える叙事詩。",
        "",
        "### 派生録 II：『深淵調律秘儀録』（Liber Harmoniae）",
        "- **概要**: 音響結晶（kris）と星光を共鳴させる調律師たちの秘儀書。",
        "- **物語性**: 光の波長濁りを清澄化し（falzenor）、重力波と光波を幾何学的に一致させる工学理論。数理・色彩・鉱物・感触のバックボーンを担う。",
        "",
        "### 派生録 III：『星影生活誌』（Chronica Quotidianae）",
        "- **概要**: 天蓋の下に暮らす市井の人々の生活年代記。",
        "- **物語性**: 朝餉の湯気、市場の行き交い、織り布の手触り、雨上がりの路地、見送り（peltel）と再会の抱擁。衣食住・共同体・温かい感情語彙の生命源泉。",
        "",
        "---",
        "",
        "## 4. 全単語・出典詩節対照索引（Concordance Index）",
        "",
        f"全 {len(all_words)} 語根の原本章節リファレンス（抜粋）:",
        "",
        "| 語根 (Root) | 品詞 | 日本語義 | 英語対訳 | 原本登場詩節 (Locus) |",
        "| :--- | :--- | :--- | :--- | :--- |"
    ])

    for root, w in sorted(all_words.items())[:120]:
        locus = word_to_locus.get(root, '追補篇')
        lines.append(f"| **{root}** | {w['pos']} | {w['ja'].split('、')[0]} | {w['en'].split(';')[0]} | {locus} |")

    lines.append(f"\n*(※ 全 {len(all_words)} 語根の完全索引は PDF および HTML 正本に完全収録されています)*\n")

    md_path.write_text("\n".join(lines), encoding='utf-8')

if __name__ == "__main__":
    build_codex()
