import json
import os

def build_web_studio():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    lexicon_path = os.path.join(base_dir, 'data', 'lexicon.json')
    font_b64_path = os.path.join(base_dir, 'fonts', 'font_b64.txt')
    canon_path = os.path.join(base_dir, 'data', 'canon_corpus.json')
    ext_path = os.path.join(base_dir, 'data', 'extended_corpus_v2.json')
    web_dir = os.path.join(base_dir, 'web')
    
    html_path = os.path.join(web_dir, 'index.html')
    data_js_path = os.path.join(web_dir, 'data.js')
    standalone_path = os.path.join(web_dir, 'standalone.html')
    app_js_path = os.path.join(web_dir, 'app.js')

    with open(font_b64_path, 'r', encoding='utf-8') as f:
        font_b64 = f.read().strip()

    with open(lexicon_path, 'r', encoding='utf-8') as f:
        lex_data = json.load(f)
        vocab = lex_data.get('vocabulary', [])

    canon_examples = []
    if os.path.exists(canon_path):
        with open(canon_path, 'r', encoding='utf-8') as f:
            corpus_data = json.load(f)
            for u in corpus_data.get('units', []):
                canon_examples.append({
                    'id': u.get('id', ''),
                    'neb': u.get('nrs', ''),
                    'ja': u.get('translationJa', ''),
                    'lit': u.get('title', '')
                })

    ext_examples = []
    if os.path.exists(ext_path):
        with open(ext_path, 'r', encoding='utf-8') as f:
            ext_data = json.load(f)
            ext_examples = ext_data.get('sentences', [])

    compact_vocab = []
    for w in vocab:
        compact_vocab.append({
            'id': w.get('id', 0),
            'r': w.get('nrs', ''),
            'p': w.get('pos', ''),
            'm': w.get('meaningJa', ''),
            'i': w.get('ipa', ''),
            'en': w.get('meaningEn', ''),
            'c': w.get('category', ''),
            'n': w.get('notes', '')
        })

    # Write data.js
    data_js_content = f"""// Nebulith Studio Web - Embedded Data Bundle
const VOCAB = {json.dumps(compact_vocab, ensure_ascii=False)};
const CANON = {json.dumps(canon_examples, ensure_ascii=False)};
const EXT_SENTENCES = {json.dumps(ext_examples, ensure_ascii=False)};
"""
    with open(data_js_path, 'w', encoding='utf-8') as f:
        f.write(data_js_content)

    with open(app_js_path, 'r', encoding='utf-8') as f:
        app_js_content = f.read()

    # Base HTML template without inline data
    base_html = f'''<!DOCTYPE html>
<html lang="ja" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="theme-color" content="#111318">
  <link rel="icon" type="image/svg+xml" href="./favicon.svg">
  <link rel="manifest" href="./manifest.json">
  <title>Nebulith Studio Web - 星石語統合スタジオ</title>
  <style>
    @font-face {{
      font-family: 'Nebulith';
      src: url('data:font/ttf;base64,{font_b64}') format('truetype');
      font-weight: normal;
      font-style: normal;
      font-display: swap;
    }}

    :root {{
      --md-sys-color-primary: #a8c7fa;
      --md-sys-color-on-primary: #062e6f;
      --md-sys-color-primary-container: #1b448a;
      --md-sys-color-on-primary-container: #d3e3fd;
      --md-sys-color-surface: #111318;
      --md-sys-color-surface-dim: #111318;
      --md-sys-color-surface-container-lowest: #0c0e13;
      --md-sys-color-surface-container-low: #191c20;
      --md-sys-color-surface-container: #1e2025;
      --md-sys-color-surface-container-high: #282a2f;
      --md-sys-color-surface-container-highest: #33353a;
      --md-sys-color-on-surface: #e2e2e9;
      --md-sys-color-on-surface-variant: #c4c6d0;
      --md-sys-color-outline: #8e9099;
      --md-sys-color-outline-variant: #44474f;
      --md-sys-color-tertiary: #b0c6ff;
      --md-sys-color-error: #ffb4ab;
      --md-sys-color-error-container: #93000a;
      --md-sys-color-on-error: #690005;
      --font-family-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", "Yu Gothic UI", Meiryo, sans-serif;
      --font-family-nebulith: 'Nebulith', sans-serif;
      --radius-sm: 8px;
      --radius-md: 12px;
      --radius-lg: 16px;
      --radius-full: 9999px;
      --transition-fast: 0.18s cubic-bezier(0.2, 0, 0, 1);
      --transition-normal: 0.28s cubic-bezier(0.2, 0, 0, 1);
    }}

    [data-theme="light"] {{
      --md-sys-color-primary: #1952a5;
      --md-sys-color-on-primary: #ffffff;
      --md-sys-color-primary-container: #d3e3fd;
      --md-sys-color-on-primary-container: #041e49;
      --md-sys-color-surface: #f8f9ff;
      --md-sys-color-surface-dim: #d8dadf;
      --md-sys-color-surface-container-lowest: #ffffff;
      --md-sys-color-surface-container-low: #f2f3f8;
      --md-sys-color-surface-container: #eceef3;
      --md-sys-color-surface-container-high: #e6e8ed;
      --md-sys-color-surface-container-highest: #e0e2e7;
      --md-sys-color-on-surface: #191c20;
      --md-sys-color-on-surface-variant: #44474f;
      --md-sys-color-outline: #74777f;
      --md-sys-color-outline-variant: #c4c6d0;
      --md-sys-color-tertiary: #415f91;
      --md-sys-color-error: #ba1a1a;
      --md-sys-color-error-container: #ffdad6;
      --md-sys-color-on-error: #ffffff;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      font-family: var(--font-family-sans);
      background-color: var(--md-sys-color-surface);
      color: var(--md-sys-color-on-surface);
      line-height: 1.5;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
      transition: background-color var(--transition-normal), color var(--transition-normal);
    }}

    /* Header */
    header.app-bar {{
      background-color: var(--md-sys-color-surface-container);
      border-bottom: 1px solid var(--md-sys-color-outline-variant);
      padding: 12px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: sticky;
      top: 0;
      z-index: 100;
    }}

    .brand-section {{ display: flex; align-items: center; gap: 12px; }}

    .brand-icon-wrap {{
      width: 44px;
      height: 44px;
      border-radius: var(--radius-md);
      background: var(--md-sys-color-surface-container-high);
      border: 1px solid var(--md-sys-color-outline-variant);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 6px;
    }}

    .brand-icon-wrap svg {{ width: 100%; height: 100%; }}

    .brand-title-wrap h1 {{
      font-size: 1.15rem;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .badge-chip {{
      font-size: 0.72rem;
      font-weight: 500;
      padding: 2px 8px;
      border-radius: var(--radius-full);
      background: var(--md-sys-color-primary-container);
      color: var(--md-sys-color-on-primary-container);
    }}

    .brand-sub {{
      font-size: 0.78rem;
      color: var(--md-sys-color-on-surface-variant);
    }}

    .theme-toggle-btn {{
      background: var(--md-sys-color-surface-container-high);
      border: 1px solid var(--md-sys-color-outline-variant);
      color: var(--md-sys-color-on-surface);
      padding: 8px 14px;
      border-radius: var(--radius-full);
      cursor: pointer;
      font-size: 0.85rem;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    /* Navigation Bar */
    nav.tab-nav {{
      background: var(--md-sys-color-surface-container-low);
      padding: 0 24px;
      display: flex;
      gap: 8px;
      border-bottom: 1px solid var(--md-sys-color-outline-variant);
      overflow-x: auto;
    }}

    .tab-btn {{
      background: transparent;
      border: none;
      color: var(--md-sys-color-on-surface-variant);
      padding: 14px 18px;
      font-size: 0.92rem;
      font-weight: 500;
      cursor: pointer;
      position: relative;
      display: flex;
      align-items: center;
      gap: 8px;
      white-space: nowrap;
    }}

    .tab-btn:hover {{ color: var(--md-sys-color-on-surface); }}
    .tab-btn.active {{ color: var(--md-sys-color-primary); font-weight: 600; }}
    .tab-btn.active::after {{
      content: '';
      position: absolute;
      bottom: 0;
      left: 10px;
      right: 10px;
      height: 3px;
      background: var(--md-sys-color-primary);
      border-radius: 3px 3px 0 0;
    }}

    /* Main Container */
    main.app-main {{
      flex: 1;
      padding: 24px;
      max-width: 1440px;
      width: 100%;
      margin: 0 auto;
    }}

    .tab-content {{ display: none; animation: fadeIn var(--transition-normal); }}
    .tab-content.active {{ display: block; }}

    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(6px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    /* Search & Filter Panel */
    .search-panel {{
      background: var(--md-sys-color-surface-container);
      border-radius: var(--radius-lg);
      padding: 20px;
      margin-bottom: 24px;
      border: 1px solid var(--md-sys-color-outline-variant);
    }}

    .search-input-wrap {{ position: relative; margin-bottom: 16px; }}
    .search-input {{
      width: 100%;
      padding: 14px 20px 14px 44px;
      border-radius: var(--radius-full);
      border: 1px solid var(--md-sys-color-outline);
      background: var(--md-sys-color-surface-container-lowest);
      color: var(--md-sys-color-on-surface);
      font-size: 1rem;
      outline: none;
    }}
    .search-input:focus {{ border-color: var(--md-sys-color-primary); }}
    .search-icon {{
      position: absolute;
      left: 16px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--md-sys-color-on-surface-variant);
      pointer-events: none;
    }}

    .filter-chips {{ display: flex; gap: 8px; flex-wrap: wrap; }}
    .chip-btn {{
      background: var(--md-sys-color-surface-container-high);
      border: 1px solid var(--md-sys-color-outline-variant);
      color: var(--md-sys-color-on-surface-variant);
      padding: 6px 14px;
      border-radius: var(--radius-full);
      font-size: 0.82rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .chip-btn.active {{
      background: var(--md-sys-color-primary-container);
      color: var(--md-sys-color-on-primary-container);
      border-color: var(--md-sys-color-primary);
      font-weight: 600;
    }}

    .lexicon-summary {{
      margin-bottom: 16px;
      font-size: 0.88rem;
      color: var(--md-sys-color-on-surface-variant);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .word-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 16px;
    }}

    .word-card {{
      background: var(--md-sys-color-surface-container);
      border: 1px solid var(--md-sys-color-outline-variant);
      border-radius: var(--radius-md);
      padding: 16px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform var(--transition-fast), border-color var(--transition-fast);
      cursor: pointer;
      position: relative;
    }}
    .word-card:hover {{
      transform: translateY(-2px);
      border-color: var(--md-sys-color-primary);
    }}

    .card-fav-btn {{
      position: absolute;
      top: 14px;
      right: 14px;
      background: transparent;
      border: none;
      font-size: 1.1rem;
      cursor: pointer;
      opacity: 0.4;
      transition: opacity var(--transition-fast), transform var(--transition-fast);
    }}
    .card-fav-btn:hover {{ opacity: 1; transform: scale(1.15); }}
    .card-fav-btn.active {{ opacity: 1; color: #fbbc04; }}

    .word-roman {{ font-size: 1.15rem; font-weight: 700; color: var(--md-sys-color-primary); }}
    .word-pos {{
      font-size: 0.72rem;
      padding: 2px 8px;
      border-radius: var(--radius-sm);
      background: var(--md-sys-color-surface-container-highest);
      color: var(--md-sys-color-on-surface-variant);
      margin-left: 8px;
    }}
    .word-glyph {{
      font-family: var(--font-family-nebulith);
      font-size: 2.2rem;
      line-height: 1.2;
      color: var(--md-sys-color-on-surface);
      margin: 6px 0 10px 0;
    }}
    .word-meaning {{ font-size: 0.95rem; color: var(--md-sys-color-on-surface); }}
    .word-ipa {{ font-size: 0.78rem; color: var(--md-sys-color-outline); font-family: monospace; }}

    /* Detail Modal */
    .modal-backdrop {{
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0, 0, 0, 0.65);
      backdrop-filter: blur(4px);
      z-index: 200;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }}
    .modal-backdrop.active {{ display: flex; animation: fadeIn var(--transition-fast); }}

    .modal-box {{
      background: var(--md-sys-color-surface-container);
      border: 1px solid var(--md-sys-color-outline-variant);
      border-radius: var(--radius-lg);
      max-width: 620px;
      width: 100%;
      padding: 28px;
      position: relative;
      max-height: 90vh;
      overflow-y: auto;
      box-shadow: 0 16px 36px rgba(0,0,0,0.3);
    }}

    .modal-close-btn {{
      position: absolute;
      top: 20px;
      right: 20px;
      background: var(--md-sys-color-surface-container-high);
      border: 1px solid var(--md-sys-color-outline-variant);
      color: var(--md-sys-color-on-surface);
      width: 32px;
      height: 32px;
      border-radius: var(--radius-full);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
    }}

    .modal-glyph-large {{
      font-family: var(--font-family-nebulith);
      font-size: 4rem;
      line-height: 1.1;
      color: var(--md-sys-color-primary);
      text-align: center;
      margin: 10px 0 20px 0;
      border-bottom: 1px solid var(--md-sys-color-outline-variant);
      padding-bottom: 16px;
    }}

    .modal-field {{ margin-bottom: 14px; }}
    .modal-label {{
      font-size: 0.75rem;
      font-weight: 600;
      color: var(--md-sys-color-outline);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 4px;
    }}
    .modal-val {{ font-size: 1.05rem; color: var(--md-sys-color-on-surface); }}

    /* Translation Panel */
    .trans-container {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      margin-bottom: 20px;
    }}
    @media (max-width: 860px) {{ .trans-container {{ grid-template-columns: 1fr; }} }}

    .trans-box {{
      background: var(--md-sys-color-surface-container);
      border: 1px solid var(--md-sys-color-outline-variant);
      border-radius: var(--radius-lg);
      padding: 20px;
      display: flex;
      flex-direction: column;
    }}

    .trans-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }}
    .trans-title {{ font-size: 0.92rem; font-weight: 600; color: var(--md-sys-color-on-surface-variant); }}
    .trans-tools {{ display: flex; gap: 8px; }}
    .tool-btn {{
      background: var(--md-sys-color-surface-container-high);
      border: 1px solid var(--md-sys-color-outline-variant);
      color: var(--md-sys-color-on-surface);
      padding: 5px 12px;
      border-radius: var(--radius-sm);
      font-size: 0.8rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .trans-textarea {{
      width: 100%;
      height: 200px;
      background: var(--md-sys-color-surface-container-lowest);
      border: 1px solid var(--md-sys-color-outline);
      border-radius: var(--radius-md);
      padding: 14px;
      color: var(--md-sys-color-on-surface);
      font-size: 1rem;
      resize: vertical;
      outline: none;
      line-height: 1.6;
    }}

    .trans-result-area {{
      min-height: 200px;
      background: var(--md-sys-color-surface-container-lowest);
      border: 1px solid var(--md-sys-color-outline-variant);
      border-radius: var(--radius-md);
      padding: 14px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}

    .trans-result-text {{ font-size: 1.15rem; color: var(--md-sys-color-on-surface); margin-bottom: 8px; white-space: pre-wrap; }}
    .trans-result-glyph {{
      font-family: var(--font-family-nebulith);
      font-size: 1.8rem;
      line-height: 1.3;
      color: var(--md-sys-color-primary);
      margin-bottom: 12px;
      border-top: 1px dashed var(--md-sys-color-outline-variant);
      padding-top: 10px;
      white-space: pre-wrap;
    }}

    .trans-tags-list {{ display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 8px; }}
    .trans-structure-tag {{
      font-size: 0.75rem;
      font-weight: 600;
      padding: 3px 10px;
      border-radius: var(--radius-full);
      background: var(--md-sys-color-primary-container);
      color: var(--md-sys-color-on-primary-container);
    }}

    .align-box {{
      margin-top: 14px;
      padding-top: 12px;
      border-top: 1px dashed var(--md-sys-color-outline-variant);
    }}
    .align-header {{
      font-size: 0.8rem;
      font-weight: 600;
      color: var(--md-sys-color-primary);
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .align-list {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}
    .align-chip {{
      background: var(--md-sys-color-surface-container-high);
      border: 1px solid var(--md-sys-color-outline-variant);
      border-radius: var(--radius-sm);
      padding: 6px 10px;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 0.82rem;
    }}
    .align-src {{
      font-weight: 600;
      color: var(--md-sys-color-on-surface);
    }}
    .align-arrow {{
      color: var(--md-sys-color-primary);
      font-size: 0.75rem;
    }}
    .align-dst {{
      font-family: var(--font-family-sans);
      font-weight: 600;
      color: var(--md-sys-color-primary);
    }}
    .align-role {{
      font-size: 0.7rem;
      padding: 2px 6px;
      background: var(--md-sys-color-surface-container-highest);
      color: var(--md-sys-color-on-surface-variant);
      border-radius: var(--radius-full);
    }}

    .trans-notice {{
      font-size: 0.8rem;
      color: var(--md-sys-color-on-surface-variant);
      padding: 8px 12px;
      border-radius: var(--radius-sm);
      background: var(--md-sys-color-surface-container-high);
      display: flex;
      align-items: center;
      gap: 6px;
      margin-top: 14px;
    }}

    .trans-controls {{
      display: flex;
      justify-content: center;
      align-items: center;
      margin: 12px 0;
      gap: 12px;
      flex-wrap: wrap;
    }}

    .swap-btn {{
      background: var(--md-sys-color-primary);
      color: var(--md-sys-color-on-primary);
      border: none;
      border-radius: var(--radius-full);
      padding: 10px 20px;
      font-size: 0.88rem;
      font-weight: 600;
      cursor: pointer;
    }}

    .sample-selector {{
      background: var(--md-sys-color-surface-container-high);
      border: 1px solid var(--md-sys-color-outline-variant);
      color: var(--md-sys-color-on-surface);
      padding: 8px 14px;
      border-radius: var(--radius-full);
      font-size: 0.85rem;
      outline: none;
      cursor: pointer;
    }}

    /* Editor Section */
    .editor-card {{
      background: var(--md-sys-color-surface-container);
      border: 1px solid var(--md-sys-color-outline-variant);
      border-radius: var(--radius-lg);
      padding: 24px;
    }}

    .editor-controls {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 16px;
      flex-wrap: wrap;
      gap: 12px;
    }}

    .editor-actions {{ display: flex; gap: 8px; }}

    .slider-wrap {{
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 0.85rem;
      color: var(--md-sys-color-on-surface-variant);
    }}

    .editor-slider {{ accent-color: var(--md-sys-color-primary); }}

    .editor-input {{
      width: 100%;
      height: 160px;
      background: var(--md-sys-color-surface-container-lowest);
      border: 1px solid var(--md-sys-color-outline);
      border-radius: var(--radius-md);
      padding: 16px;
      color: var(--md-sys-color-on-surface);
      font-size: 1.05rem;
      resize: vertical;
      outline: none;
      margin-bottom: 12px;
    }}

    .editor-meta {{
      font-size: 0.8rem;
      color: var(--md-sys-color-outline);
      display: flex;
      justify-content: space-between;
      margin-bottom: 20px;
    }}

    .editor-preview-box {{
      background: var(--md-sys-color-surface-container-lowest);
      border: 1px solid var(--md-sys-color-outline-variant);
      border-radius: var(--radius-md);
      padding: 20px;
      min-height: 200px;
    }}

    .editor-preview-label {{
      font-size: 0.78rem;
      color: var(--md-sys-color-outline);
      margin-bottom: 12px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}

    .editor-preview-text {{
      font-family: var(--font-family-nebulith);
      color: var(--md-sys-color-on-surface);
      line-height: 1.6;
      word-break: break-all;
      white-space: pre-wrap;
    }}

    /* Corpus Cards */
    .corpus-list {{ display: flex; flex-direction: column; gap: 16px; }}
    .corpus-card {{
      background: var(--md-sys-color-surface-container);
      border: 1px solid var(--md-sys-color-outline-variant);
      border-radius: var(--radius-md);
      padding: 18px;
    }}
    .corpus-badge {{
      display: inline-block;
      font-size: 0.72rem;
      font-weight: 600;
      color: var(--md-sys-color-primary);
      margin-bottom: 6px;
    }}
    .corpus-glyph {{
      font-family: var(--font-family-nebulith);
      font-size: 1.8rem;
      color: var(--md-sys-color-on-surface);
      margin-bottom: 8px;
    }}
    .corpus-neb {{ font-size: 1.05rem; font-weight: 600; color: var(--md-sys-color-primary); margin-bottom: 4px; }}
    .corpus-ja {{ font-size: 0.95rem; color: var(--md-sys-color-on-surface); }}
    .corpus-lit {{ font-size: 0.8rem; color: var(--md-sys-color-outline); margin-top: 4px; }}

    footer.app-footer {{
      margin-top: auto;
      background: var(--md-sys-color-surface-container-lowest);
      border-top: 1px solid var(--md-sys-color-outline-variant);
      padding: 16px 24px;
      text-align: center;
      font-size: 0.8rem;
      color: var(--md-sys-color-on-surface-variant);
    }}
  </style>
</head>
<body>

  <!-- Header -->
  <header class="app-bar">
    <div class="brand-section">
      <div class="brand-icon-wrap">
        <svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="42" fill="none" stroke="#a8c7fa" stroke-width="6"/><path d="M50 15 Q50 50 15 50 Q50 50 50 85 Q50 50 85 50 Z" fill="#a8c7fa"/><circle cx="50" cy="50" r="10" fill="#ffffff"/></svg>
      </div>
      <div class="brand-title-wrap">
        <h1>Nebulith Studio <span class="badge-chip">PWA Edition</span></h1>
        <div class="brand-sub">星石語 統合辞書・完全オフライン多構文対訳・フォントスタジオ</div>
      </div>
    </div>
    <div class="header-actions">
      <button class="theme-toggle-btn" id="themeToggleBtn">
        <span id="themeIcon">☀️</span> <span id="themeLabel">Light</span>
      </button>
    </div>
  </header>

  <!-- Navigation Tabs -->
  <nav class="tab-nav">
    <button class="tab-btn active" data-tab="lexicon">
      <span>📖</span> 辞書・語根 (1,008語)
    </button>
    <button class="tab-btn" data-tab="translator">
      <span>🔄</span> 相互変換・多言語アライメント (JA / EN / NEB)
    </button>
    <button class="tab-btn" data-tab="editor">
      <span>✍️</span> 星石文字エディタ
    </button>
    <button class="tab-btn" data-tab="corpus">
      <span>📜</span> 3言語対訳コーパス (53例文)
    </button>
  </nav>

  <!-- Main Container -->
  <main class="app-main">

    <!-- TAB 1: Lexicon -->
    <div class="tab-content active" id="tab-lexicon">
      <div class="search-panel">
        <div class="search-input-wrap">
          <span class="search-icon">🔍</span>
          <input type="text" class="search-input" id="lexSearchInput" placeholder="ローマ字、日本語、星石文字、英語で検索... (クリックで詳細モーダル)">
        </div>
        <div class="filter-chips" id="filterChips">
          <button class="chip-btn active" data-pos="ALL">すべて (1,008)</button>
          <button class="chip-btn" data-pos="FAV">★ お気に入り (<span id="favCount">0</span>)</button>
          <button class="chip-btn" data-pos="名">名詞 (noun)</button>
          <button class="chip-btn" data-pos="動">動詞 (verb)</button>
          <button class="chip-btn" data-pos="形">形容詞 (adj)</button>
          <button class="chip-btn" data-pos="副">副詞 (adverb)</button>
        </div>
      </div>

      <div class="lexicon-summary">
        <span id="resultCount">表示中: 1,008 語</span>
        <span style="font-size: 0.8rem; color: var(--md-sys-color-outline);">カードクリックで詳細・語源・お気に入り登録</span>
      </div>

      <div class="word-grid" id="wordGrid"></div>
    </div>

    <!-- TAB 2: Translator -->
    <div class="tab-content" id="tab-translator">
      <div class="trans-controls">
        <div style="display: flex; align-items: center; gap: 8px;">
          <label style="font-size: 0.82rem; font-weight: 600; color: var(--md-sys-color-outline);">入力:</label>
          <select class="sample-selector" id="srcLangSelect">
            <option value="ja" selected>🇯🇵 日本語 (JA)</option>
            <option value="en">🇬🇧 英語 (EN)</option>
            <option value="neb">🌌 星石語 (NEB)</option>
          </select>
        </div>
        <button class="swap-btn" id="swapTransBtn">
          <span>⇄</span> 切替
        </button>
        <div style="display: flex; align-items: center; gap: 8px;">
          <label style="font-size: 0.82rem; font-weight: 600; color: var(--md-sys-color-outline);">出力:</label>
          <select class="sample-selector" id="dstLangSelect">
            <option value="neb" selected>🌌 星石語 (NEB)</option>
            <option value="ja">🇯🇵 日本語 (JA)</option>
            <option value="en">🇬🇧 英語 (EN)</option>
          </select>
        </div>
        <select class="sample-selector" id="sampleSelect">
          <option value="">▼ 拡張文型・英語・長文例文を選ぶ（単語アライメント表示）</option>
          <option value="私はあなたが好きです。">【好悪・日】私はあなたが好きです。</option>
          <option value="I like you.">【好悪・英】I like you.</option>
          <option value="私は美しい星が好きだ。">【好悪+形容・日】私は美しい星が好きだ。</option>
          <option value="I like beautiful stars.">【好悪+形容・英】I like beautiful stars.</option>
          <option value="星が輝くなら、私は歩く。">【条件節・日】星が輝くなら、私は歩く。</option>
          <option value="If stars shine, I walk.">【条件節・英】If stars shine, I walk.</option>
          <option value="あなたが私を好きなら、私は嬉しいです。">【条件節+感情・日】あなたが私を好きなら、私は嬉しいです。</option>
          <option value="If you like me, I am glad.">【条件節+感情・英】If you like me, I am glad.</option>
          <option value="星は夜よりも美しい。">【比較級・日】星は夜よりも美しい。</option>
          <option value="The star is more beautiful than the night.">【比較級・英】The star is more beautiful than the night.</option>
          <option value="太陽は星よりも光る。">【比較級・動詞・日】太陽は星よりも光る。</option>
          <option value="The sun shines more than the stars.">【比較級・動詞・英】The sun shines more than the stars.</option>
          <option value="あなたは誰ですか？">【疑問詞:誰】あなたは誰ですか？</option>
          <option value="Who are you?">【疑問詞:Who】Who are you?</option>
          <option value="これは何ですか？">【疑問詞:何】これは何ですか？</option>
          <option value="What is this?">【疑問詞:What】What is this?</option>
          <option value="あなたはどこへ歩きますか？">【疑問詞:どこ】あなたはどこへ歩きますか？</option>
          <option value="家へ歩きなさい。">【命令法】家へ歩きなさい。</option>
          <option value="星を観測しよう。">【勧誘法】星を観測しよう。</option>
          <option value="星が夜空で輝く。私はあなたが好きです。">【長文 2文】星が夜空で輝く。私はあなたが好きです。</option>
          <option value="夜は美しい。星が輝くから、私は歩く。私はあなたを信じている。">【長文 3文段落】夜は美しい。星が輝くから、私は歩く。私はあなたを信じている。</option>
        </select>
      </div>

      <div class="trans-container">
        <div class="trans-box">
          <div class="trans-header">
            <span class="trans-title" id="srcTitle">原文入力 (日本語 / English / 星石語)</span>
            <div class="trans-tools">
              <button class="tool-btn" id="clearSrcBtn">消去</button>
            </div>
          </div>
          <textarea class="trans-textarea" id="transInput" placeholder="翻訳する文章を入力してください。句点「。」やピリオド「.」で区切られた長文・段落も一括解析・変換します..."></textarea>
        </div>

        <div class="trans-box">
          <div class="trans-header">
            <span class="trans-title" id="dstTitle">訳文・解析結果</span>
            <div class="trans-tools">
              <button class="tool-btn" id="copyDstBtn">コピー</button>
            </div>
          </div>
          <div class="trans-result-area">
            <div>
              <div id="transTagsList" class="trans-tags-list"></div>
              <div class="trans-result-text" id="transOutputText">ここに訳文が表示されます</div>
              <div class="trans-result-glyph" id="transOutputGlyph"></div>
              <div id="transAlignmentBox" class="align-box"></div>
            </div>
            <div class="trans-notice" id="transNotice">
              <span>ℹ️</span> 外部AI・通信ゼロ。文法規則（VSO・格助詞・条件節zen・奪格比較va）と辞書で確定変換します。
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 3: Editor -->
    <div class="tab-content" id="tab-editor">
      <div class="editor-card">
        <div class="editor-controls">
          <span style="font-weight: 600; font-size: 0.95rem;">星石文字リアルタイムエディタ (Version 2.5)</span>
          <div class="editor-actions">
            <button class="tool-btn" id="downloadNebBtn">📥 .neb 保存</button>
            <button class="tool-btn" id="copyEditorBtn">📋 コピー</button>
            <button class="tool-btn" id="clearEditorBtn">消去</button>
          </div>
          <div class="slider-wrap">
            <span>文字サイズ:</span>
            <input type="range" class="editor-slider" id="fontSizeSlider" min="20" max="64" value="36">
            <span id="fontSizeVal">36px</span>
          </div>
        </div>
        <textarea class="editor-input" id="editorInput" placeholder="Nebulithローマ字を入力すると、下部に星石文字フォントでリアルタイム表示されます..."></textarea>
        <div class="editor-meta">
          <span id="editorStats">文字数: 0 | 単語数: 0 | 行数: 1</span>
          <span>下書きはブラウザ内に自動保存されます</span>
        </div>
        <div class="editor-preview-box">
          <div class="editor-preview-label">Nebulith Glyph Live Preview</div>
          <div class="editor-preview-text" id="editorPreview" style="font-size: 36px;">
            Cynel el mi ia ti. Zen falun el vyr, cylani el valar.
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 4: Corpus -->
    <div class="tab-content" id="tab-corpus">
      <div style="margin-bottom: 16px; color: var(--md-sys-color-on-surface-variant); font-size: 0.9rem;">
        公式正本30例文 ＋ 拡張構文（条件節・比較・疑問・長文）23例の全53例文・3言語（星石語/日本語/英語）対訳集です。
      </div>
      <div class="corpus-list" id="corpusList"></div>
    </div>

  </main>

  <!-- Word Detail Modal -->
  <div class="modal-backdrop" id="wordModal">
    <div class="modal-box">
      <button class="modal-close-btn" id="modalCloseBtn">✕</button>
      <div class="modal-glyph-large" id="modalGlyph">celen</div>
      
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
        <div style="display: flex; align-items: center; gap: 8px;">
          <h2 id="modalRoman" style="font-size: 1.5rem; color: var(--md-sys-color-primary);">celen</h2>
          <span id="modalPos" class="badge-chip">名詞</span>
          <span id="modalId" style="font-size: 0.75rem; color: var(--md-sys-color-outline);">#1</span>
        </div>
        <button class="tool-btn" id="modalFavToggle">★ お気に入りに追加</button>
      </div>

      <div class="modal-field">
        <div class="modal-label">日本語義 (Meaning JA)</div>
        <div class="modal-val" id="modalMeaningJa">空、天蓋、蒼穹、大気</div>
      </div>

      <div class="modal-field">
        <div class="modal-label">英語義 (Meaning EN)</div>
        <div class="modal-val" id="modalMeaningEn">sky, firmament, celestial dome</div>
      </div>

      <div class="modal-field">
        <div class="modal-label">IPA 音声表記</div>
        <div class="modal-val" id="modalIpa" style="font-family: monospace;">/[ʃe.len]/</div>
      </div>

      <div class="modal-field">
        <div class="modal-label">語根ノート・語源・天体概念</div>
        <div class="modal-val" id="modalNotes" style="font-size: 0.9rem; color: var(--md-sys-color-on-surface-variant);">天蓋</div>
      </div>

      <div style="display: flex; gap: 10px; margin-top: 24px; border-top: 1px solid var(--md-sys-color-outline-variant); padding-top: 16px;">
        <button class="tool-btn" id="copyModalRoman">ローマ字をコピー</button>
        <button class="tool-btn" id="copyModalGlyph">星石文字をコピー</button>
      </div>
    </div>
  </div>

  <!-- Footer -->
  <footer class="app-footer">
    Nebulith Project &bull; Language Version 23.5 &bull; TrueType Font Version 2.5 &bull; Standalone PWA
  </footer>

  <!-- Scripts -->
  <script src="./data.js"></script>
  <script src="./app.js"></script>
</body>
</html>
'''

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(base_html)

    # Standalone HTML (with inline data.js and app.js)
    standalone_html = base_html.replace(
        '<script src="./data.js"></script>\n  <script src="./app.js"></script>',
        f'<script>\n{data_js_content}\n{app_js_content}\n</script>'
    )
    with open(standalone_path, 'w', encoding='utf-8') as f:
        f.write(standalone_html)

    print(f"Build completed:")
    print(f" - {html_path} ({os.path.getsize(html_path):,} bytes)")
    print(f" - {data_js_path} ({os.path.getsize(data_js_path):,} bytes)")
    print(f" - {standalone_path} ({os.path.getsize(standalone_path):,} bytes)")

if __name__ == '__main__':
    build_web_studio()
