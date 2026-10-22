import json
import os
import hashlib
import re
from pathlib import Path
from studio_dictionary import dictionary_entries
from extended_corpus import validate_examples

def update_service_worker(web_dir):
    """Version the offline cache from the exact assets distributed by this build."""
    web_dir = Path(web_dir)
    path = web_dir / 'service-worker.js'
    script = path.read_text(encoding='utf-8')
    precache = re.search(r'const PRECACHE_ASSETS = \[(.*?)\];', script, re.S)
    if not precache:
        raise ValueError('Service Worker precache assets are missing')
    assets = sorted(set(re.findall(r"'\./([^']*)'", precache[1])))
    digest = hashlib.sha256()
    for asset in assets:
        name = asset or 'index.html'
        digest.update(name.encode('utf-8') + b'\0')
        digest.update(hashlib.sha256((web_dir / name).read_bytes()).digest())
    cache_name = 'nebulith-studio-' + digest.hexdigest()[:20]
    updated, count = re.subn(r"const CACHE_NAME = '[^']+';", "const CACHE_NAME = '" + cache_name + "';", script)
    if count != 1:
        raise ValueError('Service Worker cache name is missing or ambiguous')
    path.write_text(updated, encoding='utf-8')
    return cache_name

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
        vocab = dictionary_entries(lex_data.get('vocabulary', []))

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
            validate_examples(ext_examples, vocab)

    with open(os.path.join(base_dir,'data','usage_examples.json'),encoding='utf-8') as f:
        usage_examples=json.load(f)['examples']
    with open(os.path.join(base_dir,'data','verified_canonical_compounds.json'),encoding='utf-8') as f:
        verified_canonical_compounds=json.load(f)
    total_examples=len(canon_examples)+len(ext_examples)+len(usage_examples)



    with open(os.path.join(base_dir,'data','translation_input_rules.json'),encoding='utf-8') as f:
        input_rules=json.load(f)
    with open(os.path.join(base_dir,'data','corpus_rules.json'),encoding='utf-8') as f:
        grammar_frames=json.load(f)['frames']
    with open(os.path.join(base_dir,'data','translation_extensions.json'),encoding='utf-8') as f:
        translation_extensions=json.load(f)
    with open(os.path.join(base_dir,'data','translation_patterns.json'),encoding='utf-8') as f:
        translation_extensions['productive']=json.load(f)
    with open(os.path.join(base_dir,'data','compound_translation_patterns.json'),encoding='utf-8') as f:
        translation_extensions['compoundProductive']=json.load(f)
    with open(os.path.join(base_dir,'data','roadmap_lexical_rules.json'),encoding='utf-8') as f:
        translation_extensions['roadmapProductive']=json.load(f)
    with open(os.path.join(base_dir,'data','studio_categories.json'),encoding='utf-8') as f:
        translation_extensions['catalogCategories']=json.load(f)
    with open(os.path.join(web_dir,'workspace.js'),encoding='utf-8') as f:
        workspace_js=f.read()
    with open(os.path.join(web_dir,'bidirectional.js'),encoding='utf-8') as f:
        bidirectional_js=f.read()
    with open(os.path.join(web_dir,'incremental.js'),encoding='utf-8') as f:
        incremental_js=f.read()

    from literary_sourcebook import source_hash
    literary_path=Path(base_dir)/'data/literary_sourcebook.json'
    literary=json.loads(literary_path.read_text(encoding='utf-8'))
    literary_entries={row['root']:row for row in literary['entries']}
    for row in vocab:
        if row['nrs'] not in literary_entries or literary_entries[row['nrs']]['sourceHash']!=source_hash(row):
            raise ValueError('Rebuild/review literary source edition before Web bundle: '+row['nrs'])
    literary_bundle={'title':literary['title'],'works':{w['id']:w['title'] for w in literary['works']},
        'entries':{r['root']:{k:r[k] for k in ['id','work','chapter','chapterTitle','quote','anchor']} for r in literary['entries']}}
    (Path(web_dir)/'library.html').write_bytes((Path(base_dir)/'docs/Valnes_Ibun.html').read_bytes())

    compact_vocab = []
    for w in vocab:
        wid = w.get('id', 0)
        origin = w.get('origin') or ('canon' if wid <= 1008 else 'curated_ext')
        compact_vocab.append({
            'id': wid,
            'r': w.get('nrs', ''),
            'p': w.get('pos', ''),
            'm': w.get('meaningJa', ''),
            'i': w.get('ipa', ''),
            'en': w.get('meaningEn', ''),
            'c': w.get('category', ''),
            'n': w.get('notes', ''),
            'o': origin,
            'as': w.get('auditStatus', 'canon_verified' if wid <= 1008 else 'curated'),
            'sc': w.get('auditScore', 1.0),
            'sid': w.get('scenarioId', ''),
            'et': w.get('etymology', '')
        })

    # Write data.js
    data_js_content = f"""// Nebulith Studio Web - Embedded Data Bundle
const VOCAB = {json.dumps(compact_vocab, ensure_ascii=False)};
const CANON = {json.dumps(canon_examples, ensure_ascii=False)};
const LITERARY_BOOK = {json.dumps(literary_bundle, ensure_ascii=False)};
const INPUT_RULES = {json.dumps(input_rules, ensure_ascii=False)};
const GRAMMAR_FRAMES = {json.dumps(grammar_frames, ensure_ascii=False)};
const TRANSLATION_EXTENSIONS = {json.dumps(translation_extensions, ensure_ascii=False)};
const EXT_SENTENCES = {json.dumps(ext_examples, ensure_ascii=False)};
const USAGE_EXAMPLES = {json.dumps(usage_examples, ensure_ascii=False)};
const VERIFIED_CANONICAL_COMPOUNDS = {json.dumps(verified_canonical_compounds, ensure_ascii=False)};
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
    [hidden] {{ display: none !important; }}
    button:focus-visible, select:focus-visible, input:focus-visible {{ outline: 2px solid var(--md-sys-color-primary); outline-offset: 3px; }}

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
      min-height: 44px;
      border-radius: var(--radius-full);
      cursor: pointer;
      font-size: 0.85rem;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: background var(--transition-fast);
    }}
    .theme-toggle-btn:hover {{
      background: var(--md-sys-color-surface-container-highest);
    }}

    .queue-badge {{
      background: var(--md-sys-color-primary);
      color: var(--md-sys-color-on-primary);
      padding: 2px 7px;
      border-radius: var(--radius-full);
      font-size: 0.72rem;
      font-weight: 700;
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
      top: 8px;
      right: 8px;
      width: 44px;
      height: 44px;
      min-width: 44px;
      min-height: 44px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      background: transparent;
      border: none;
      padding: 0;
      font-size: 1.35rem;
      line-height: 1;
      color: var(--md-sys-color-on-surface);
      cursor: pointer;
      opacity: 0.9;
      transition: opacity var(--transition-fast), transform var(--transition-fast);
    }}
    .card-fav-btn:hover {{ opacity: 1; transform: scale(1.08); }}
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

    /* Empty state */
    .empty-state {{
      grid-column: 1 / -1;
      background: var(--md-sys-color-surface-container);
      border: 1px dashed var(--md-sys-color-outline-variant);
      border-radius: var(--radius-lg);
      padding: 36px 20px;
      text-align: center;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 10px;
    }}

    .record-btn {{
      background: var(--md-sys-color-primary-container);
      color: var(--md-sys-color-on-primary-container);
      border: 1px solid var(--md-sys-color-primary);
      padding: 8px 18px;
      border-radius: var(--radius-full);
      font-size: 0.88rem;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: background var(--transition-fast);
    }}
    .record-btn:hover {{
      background: var(--md-sys-color-primary);
      color: var(--md-sys-color-on-primary);
    }}

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
      top: 16px;
      right: 16px;
      background: var(--md-sys-color-surface-container-high);
      border: 1px solid var(--md-sys-color-outline-variant);
      color: var(--md-sys-color-on-surface);
      width: 44px;
      height: 44px;
      min-width: 44px;
      min-height: 44px;
      border-radius: var(--radius-full);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-size: 1.5rem;
      line-height: 1;
      padding: 0;
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

    /* Queue Modal Styles */
    .queue-list {{
      display: flex;
      flex-direction: column;
      gap: 10px;
      max-height: 50vh;
      overflow-y: auto;
      margin: 16px 0;
    }}
    .queue-card {{
      background: var(--md-sys-color-surface-container-high);
      border: 1px solid var(--md-sys-color-outline-variant);
      border-radius: var(--radius-md);
      padding: 12px 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
    }}
    .queue-card-content {{
      display: flex;
      flex-direction: column;
      gap: 4px;
      flex: 1;
    }}
    .queue-card-tag {{
      font-size: 0.72rem;
      font-weight: 600;
      color: var(--md-sys-color-primary);
    }}
    .queue-card-text {{
      font-size: 0.95rem;
      font-weight: 500;
      color: var(--md-sys-color-on-surface);
      word-break: break-all;
    }}
    .queue-card-meta {{
      font-size: 0.75rem;
      color: var(--md-sys-color-outline);
    }}

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
    .tool-btn.icon-btn {{
      min-width: 44px;
      min-height: 44px;
      padding: 0 12px;
      justify-content: center;
      font-size: 1.35rem;
      line-height: 1;
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

    .missing-box {{
      margin-top: 14px;
      padding: 12px 16px;
      background: var(--md-sys-color-surface-container-high);
      border: 1px dashed var(--md-sys-color-error);
      border-radius: var(--radius-md);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
    }}
    .missing-text {{
      font-size: 0.85rem;
      color: var(--md-sys-color-error);
      display: flex;
      align-items: center;
      gap: 6px;
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

    /* Dialogues & Compounds Section */
    .dialogue-search-panel {{
      background: var(--md-sys-color-surface-container);
      border-radius: var(--radius-lg);
      padding: 20px;
      margin-bottom: 24px;
      border: 1px solid var(--md-sys-color-outline-variant);
    }}
    .view-mode-group {{
      display: flex;
      gap: 10px;
      margin-bottom: 14px;
      flex-wrap: wrap;
    }}
    .view-mode-btn {{
      background: var(--md-sys-color-surface-container-high);
      border: 1px solid var(--md-sys-color-outline-variant);
      color: var(--md-sys-color-on-surface-variant);
      padding: 8px 18px;
      border-radius: var(--radius-full);
      font-size: 0.88rem;
      cursor: pointer;
      font-weight: 500;
      transition: background var(--transition-fast);
    }}
    .view-mode-btn.active {{
      background: var(--md-sys-color-primary-container);
      color: var(--md-sys-color-on-primary-container);
      border-color: var(--md-sys-color-primary);
      font-weight: 600;
    }}
    .dialogue-list {{ display: flex; flex-direction: column; gap: 18px; }}
    .dialogue-card {{
      background: var(--md-sys-color-surface-container);
      border: 1px solid var(--md-sys-color-outline-variant);
      border-radius: var(--radius-md);
      padding: 20px;
      transition: border-color var(--transition-fast);
    }}
    .dialogue-card:hover {{ border-color: var(--md-sys-color-primary); }}
    .dialogue-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 14px;
      flex-wrap: wrap;
      gap: 8px;
      border-bottom: 1px solid var(--md-sys-color-outline-variant);
      padding-bottom: 10px;
    }}
    .dialogue-id {{
      font-size: 0.78rem;
      font-weight: 700;
      color: var(--md-sys-color-primary);
      font-family: monospace;
    }}
    .dialogue-title {{
      font-size: 1.05rem;
      font-weight: 600;
      color: var(--md-sys-color-on-surface);
    }}
    .dialogue-speakers {{
      font-size: 0.8rem;
      color: var(--md-sys-color-on-surface-variant);
    }}
    .dialogue-turn {{
      background: var(--md-sys-color-surface-container-lowest);
      border-left: 3px solid var(--md-sys-color-primary);
      border-radius: var(--radius-sm);
      padding: 10px 14px;
      margin: 8px 0;
    }}
    .turn-speaker {{
      font-weight: 700;
      font-size: 0.82rem;
      color: var(--md-sys-color-primary);
      margin-bottom: 4px;
    }}
    .turn-glyph {{
      font-family: var(--font-family-nebulith);
      font-size: 1.35rem;
      color: var(--md-sys-color-on-surface);
      line-height: 1.3;
    }}
    .turn-nrs {{
      font-family: Georgia, serif;
      font-size: 0.92rem;
      color: var(--md-sys-color-on-surface);
      margin-top: 2px;
    }}
    .turn-ja {{
      font-size: 0.88rem;
      color: var(--md-sys-color-on-surface-variant);
      margin-top: 2px;
    }}
    .dialogue-compounds {{
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
      margin-top: 12px;
      padding-top: 8px;
    }}
    .dialogue-actions {{
      display: flex;
      gap: 8px;
      margin-top: 10px;
      justify-content: flex-end;
    }}
    .compound-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 14px;
    }}
    .compound-card {{
      background: var(--md-sys-color-surface-container);
      border: 1px solid var(--md-sys-color-outline-variant);
      border-radius: var(--radius-md);
      padding: 16px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform var(--transition-fast), border-color var(--transition-fast);
      cursor: pointer;
    }}
    .compound-card:hover {{
      transform: translateY(-2px);
      border-color: var(--md-sys-color-primary);
    }}
    .compound-roots {{
      font-family: monospace;
      font-size: 0.78rem;
      color: var(--md-sys-color-outline);
      margin: 4px 0 8px 0;
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


    /* Mobile & Smartphone Responsive Styles */
    @media (max-width: 768px) {{
      header.app-bar {{
        padding: 10px 14px;
        gap: 8px;
        flex-wrap: wrap;
      }}
      .brand-section {{
        gap: 8px;
      }}
      .brand-icon-wrap {{
        width: 36px;
        height: 36px;
        padding: 4px;
      }}
      .brand-title-wrap h1 {{
        font-size: 1.02rem;
      }}
      .brand-sub {{
        display: none;
      }}
      .header-actions {{
        gap: 6px;
        margin-left: auto;
      }}
      .theme-toggle-btn {{
        padding: 6px 10px;
        font-size: 0.78rem;
      }}
      
      nav.tab-nav {{
        padding: 0 10px;
        gap: 4px;
        -webkit-overflow-scrolling: touch;
        scrollbar-width: none;
      }}
      nav.tab-nav::-webkit-scrollbar {{
        display: none;
      }}
      .tab-btn {{
        padding: 12px 10px;
        font-size: 0.84rem;
        min-height: 44px;
      }}

      main.app-main {{
        padding: 14px 10px;
      }}

      .search-panel {{
        padding: 14px 12px;
        margin-bottom: 16px;
        border-radius: var(--radius-md);
      }}
      .search-input {{
        font-size: 16px;
        padding: 10px 14px 10px 38px;
      }}
      .search-icon {{
        left: 12px;
      }}
      .filter-chips {{
        gap: 6px;
      }}
      .chip-btn {{
        padding: 5px 10px;
        font-size: 0.76rem;
      }}

      .word-grid {{
        grid-template-columns: 1fr;
        gap: 12px;
      }}
      .word-card {{
        padding: 14px;
      }}
      .word-glyph {{
        font-size: 1.9rem;
      }}

      .trans-container {{
        grid-template-columns: 1fr;
        gap: 14px;
      }}
      .trans-box {{
        padding: 14px;
        border-radius: var(--radius-md);
      }}
      .trans-textarea, .trans-result-area {{
        min-height: 140px;
        height: 150px;
        font-size: 16px;
        padding: 10px;
      }}
      .trans-result-glyph {{
        font-size: 1.45rem;
      }}
      .align-chip {{
        padding: 4px 8px;
        font-size: 0.76rem;
      }}

      .editor-card {{
        padding: 14px;
        border-radius: var(--radius-md);
      }}
      .editor-input {{
        height: 120px;
        font-size: 16px;
        padding: 12px;
      }}
      .editor-preview-box {{
        padding: 14px;
        min-height: 140px;
      }}

      .modal-box {{
        padding: 18px 14px;
        border-radius: var(--radius-md);
        max-width: 95vw;
        max-height: 92vh;
      }}
      .modal-glyph-large {{
        font-size: 2.8rem;
        margin: 6px 0 12px 0;
        padding-bottom: 10px;
      }}
    }}

    @media (max-width: 440px) {{
      .brand-title-wrap h1 {{
        font-size: 0.92rem;
      }}
      .badge-chip {{
        display: none;
      }}
      .theme-toggle-btn span:not(.queue-badge) {{
        font-size: 0.72rem;
      }}
      .tab-btn {{
        padding: 10px 8px;
        font-size: 0.78rem;
      }}
    }}

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
    <div class="header-actions" style="display: flex; align-items: center; gap: 10px;">
      <button class="theme-toggle-btn" id="queueToggleBtn" title="未対応リクエスト・キュー">
        <span>未対応キュー</span> <span class="queue-badge" id="queueCountBadge">0</span>
      </button>
      <button type="button" class="theme-toggle-btn" id="themeToggleBtn" aria-label="ライトテーマに切り替え">
        <span id="themeIcon" aria-hidden="true"><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M19.1 4.9l-1.4 1.4M6.3 17.7l-1.4 1.4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></span><span id="themeLabel">Light</span>
      </button>
    </div>
  </header>

  <!-- Navigation Tabs -->
  <nav class="tab-nav">
    <button class="tab-btn active" data-tab="lexicon">
      辞書・語根・文法 ({len(vocab)+len(verified_canonical_compounds.get('entries', [])):,}項目)
    </button>
    <button class="tab-btn" data-tab="translator">
      相互変換・多言語アライメント (JA / EN / NEB)
    </button>
    <button class="tab-btn" data-tab="editor">
      星石文字エディタ
    </button>
    <button class="tab-btn" data-tab="corpus">
      例文・対訳コーパス ({total_examples}例)
    </button>
  </nav>

  <div style="padding:8px 24px">
    <div id="storageStatus" role="status" aria-live="polite" style="color:var(--md-sys-color-error)"></div>
    <div id="pwaUpdateStatus" role="status" aria-live="polite"></div>
    <button class="tool-btn" id="pwaReload" type="button" hidden>下書きを保存して更新を反映</button>
    <details><summary>保存・バックアップ</summary>
      <p>このブラウザーの設定・下書き・記録を保存します。別ブラウザーや別URLでは保存領域が異なります。</p>
      <button class="tool-btn" id="backupExport">全データをバックアップ</button>
      <label>バックアップ取込 <input type="file" id="backupImport" accept=".json,application/json"></label>
      <div id="backupPreview" role="status"></div><button class="tool-btn" id="backupApply" disabled>内容を確認して復元</button>
    </details>
  </div>
  <!-- Main Container -->
  <main class="app-main">

    <!-- TAB 1: Lexicon -->
    <div class="tab-content active" id="tab-lexicon">
      <div class="search-panel">
        <div class="search-input-wrap">
          <span class="search-icon"></span>
          <input type="text" class="search-input" id="lexSearchInput" placeholder="ローマ字、日本語、星石文字、英語で検索... (クリックで詳細モーダル)">
        </div>
        <div style="display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:12px 0;">
          <label>カテゴリ <select class="tool-btn" id="lexCategoryFilter" aria-label="辞書のカテゴリ" style="max-width:100%;"></select></label>
          <label>バッチ <select class="tool-btn" id="lexBatchFilter" aria-label="複合語のバッチ"></select></label>
          <button class="tool-btn" id="lexResetFilters" type="button">条件をリセット</button>
        </div>
        <div class="filter-chips" id="filterChips">
          <button class="chip-btn active" data-pos="ALL">すべて ({len(vocab)+len(verified_canonical_compounds.get("entries",[])):,})</button>
          <button class="chip-btn" data-pos="CANON">正本 (1,008)</button>
          <button class="chip-btn" data-pos="CURATED_EXT">体系拡張</button>
          <button class="chip-btn" data-pos="VERIFIED_COMPOUNDS">検証済み複合語 ({len(verified_canonical_compounds.get('entries', []))})</button>
          <button class="chip-btn" data-pos="FAV">お気に入り (<span id="favCount">0</span>)</button>
          <button class="chip-btn" data-pos="HISTORY">閲覧履歴</button>
          <button class="chip-btn" data-pos="名">名詞 (noun)</button>
          <button class="chip-btn" data-pos="動">動詞 (verb)</button>
          <button class="chip-btn" data-pos="形">形容詞 (adj)</button>
          <button class="chip-btn" data-pos="副">副詞 (adverb)</button>
          <button class="chip-btn" data-pos="代名詞">代名詞</button>
          <button class="chip-btn" data-pos="相関詞">相関詞</button>
          <button class="chip-btn" data-pos="格標識">格標識</button>
          <button class="chip-btn" data-pos="機能語">機能語</button>
          <button class="chip-btn" data-pos="接辞">接辞</button>
        </div>
      </div>

      <div class="lexicon-summary">
        <span id="resultCount" aria-live="polite">表示中: {len(vocab)+len(verified_canonical_compounds.get('entries', [])):,} 項目</span>
        <span style="font-size: 0.8rem; color: var(--md-sys-color-outline);">カードクリックで詳細・語源・お気に入り登録</span>
      </div>

      <div class="word-grid" id="wordGrid"></div>
      <nav aria-label="辞書のページ" style="display:flex;justify-content:center;align-items:center;gap:14px;margin:20px 0;">
        <button class="tool-btn" id="lexPrevPage" type="button">前へ</button>
        <span id="lexPageInfo" aria-live="polite"></span>
        <button class="tool-btn" id="lexNextPage" type="button">次へ</button>
      </nav>
    </div>

    <!-- TAB: Dialogues & Canonical Compounds -->
    <div class="tab-content" id="tab-dialogues">
      <div class="dialogue-search-panel">
        <div class="view-mode-group">
          <button type="button" class="view-mode-btn active" id="viewModeScenarios">対話シナリオ一覧 ({len(verified_canonical_compounds.get('scenarios', []))}篇)</button>
          <button type="button" class="view-mode-btn" id="viewModeCompounds">複合語一覧 ({len(verified_canonical_compounds.get('entries', []))}語)</button>
        </div>
        <div class="search-input-wrap">
          <input type="search" class="search-input" id="dialogueSearchInput" placeholder="対話文、複合語、日本語義、話者名、シナリオID、構成語根で検索...">
        </div>
        <div class="filter-chips" id="dialogueCategoryChips"></div>
      </div>
      <div id="dialoguesCount" style="margin-bottom: 12px; font-size: 0.88rem; color: var(--md-sys-color-on-surface-variant);" aria-live="polite"></div>
      <div id="dialoguesList"></div>
    </div>

    <!-- TAB 2: Translator -->
    <div class="tab-content" id="tab-translator">
      <div class="trans-controls">
        <div style="display: flex; align-items: center; gap: 8px;">
          <label style="font-size: 0.82rem; font-weight: 600; color: var(--md-sys-color-outline);">入力:</label>
          <select class="sample-selector" id="srcLangSelect">
            <option value="ja" selected> 日本語 (JA)</option>
            <option value="en"> 英語 (EN)</option>
            <option value="neb"> 星石語 (NEB)</option>
          </select>
        </div>
        <button class="swap-btn" id="swapTransBtn">
          <span>⇄</span> 切替
        </button>
        <div style="display: flex; align-items: center; gap: 8px;">
          <label style="font-size: 0.82rem; font-weight: 600; color: var(--md-sys-color-outline);">出力:</label>
          <select class="sample-selector" id="dstLangSelect">
            <option value="neb" selected> 星石語 (NEB)</option>
            <option value="ja"> 日本語 (JA)</option>
            <option value="en"> 英語 (EN)</option>
          </select>
        </div>
      </div>

      <div id="sessionStatus" role="status" aria-live="polite"></div>
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
              <div id="inputInterpretation" style="margin:12px 0" aria-live="polite"></div>
              <div id="inputFragments" style="margin:12px 0"></div>
              <div id="inputChoices" style="display:none;gap:8px;flex-wrap:wrap;margin:12px 0">
                <label id="inputSentenceLabel" style="display:none">編集する文 <select id="inputSentence"></select></label>
                <label id="inputSubjectLabel">主体の補完 <select id="inputSubject"><option value="">原文のまま</option><option>私</option><option>あなた</option><option>彼／彼女</option></select></label>
                <label id="inputVerbLabel">動作の解釈 <select id="inputVerb"><option value="">未選択</option><option>観測する</option><option>仰ぎ見る</option><option>見上げる</option><option>展望する</option><option>予見する</option><option>話す</option><option>語り合う</option><option>告げる</option><option>ささやく</option><option>問う</option><option>歩く</option><option>走る</option><option>行進する</option><option>滑空する</option><option>信じる</option><option>思索する</option><option>決断する</option><option>尊ぶ</option></select></label>
                <label id="inputPossessionLabel" style="display:none">所有範囲 <select id="inputPossession"><option value="">未選択</option><option value="shared">（AとB）のC・共有所有</option><option value="separate">Aと（BのC）・別々の並列項</option></select></label>
                <label id="inputSenseLabel" style="display:none">語義 <select id="inputSense"><option value="">未選択</option></select></label>
                <div id="inputNounChoices"></div>
                <button class="tool-btn" id="confirmInputCandidate">この解釈で確定</button>
              </div>
              <button class="tool-btn" id="copyConfirmedParts" style="display:none">確定した文だけコピー</button>
              <div id="transAlignmentBox" class="align-box"></div>
              <details style="margin:12px 0"><summary>対応する動詞・表現の範囲</summary><div id="translationCoverage"></div></details>
              <div id="transMissingBox" class="missing-box" style="display: none;">
                <span class="missing-text">この文章の文型は現在未対応です</span>
                <button class="record-btn" id="recordMissingTransBtn">未対応文章として記録する</button>
              </div>
            </div>
            <div class="trans-notice" id="transNotice">
              完全オフライン。日本語の語句・意味候補を読み取り、Nebulithの文法を検証して確定します。
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
            <button class="tool-btn" id="downloadNebBtn">.neb 保存</button>
            <button class="tool-btn" id="copyEditorBtn">コピー</button>
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
        公式正本{len(canon_examples)}例 ＋ 拡張構文{len(ext_examples)}例 ＋ 学習用例{len(usage_examples)}例、計{total_examples}例です。各例の区分・解釈条件と、用意されている日本語・英語・Nebulithの対訳を表示します。
      </div>
      <input type="search" id="corpusSearch" class="search-input" style="margin-bottom:12px" placeholder="例文を日本語・英語・NRS・文型で検索" aria-label="例文を検索">
      <div id="corpusCount" style="margin-bottom:12px" aria-live="polite"></div>
      <div class="corpus-list" id="corpusList"></div>
    </div></main>

  <!-- Word Detail Modal -->
  <div class="modal-backdrop" id="wordModal" role="dialog" aria-modal="true" aria-labelledby="modalRoman">
    <div class="modal-box">
      <button type="button" class="modal-close-btn" id="modalCloseBtn" aria-label="閉じる">×</button>
      <div class="modal-glyph-large" id="modalGlyph">celen</div>
      
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; flex-wrap: wrap; gap: 8px;">
        <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
          <h2 id="modalRoman" style="font-size: 1.6rem; font-weight: 700; color: var(--md-sys-color-primary); letter-spacing: 0.02em;">celen</h2>
          <span id="modalKana" class="badge-chip" style="background: rgba(138, 180, 248, 0.12); color: var(--md-sys-color-primary); font-weight: 500;">シェレン</span>
          <span id="modalPos" class="badge-chip">名詞</span>
        </div>
        <button class="tool-btn" id="modalFavToggle">お気に入りに追加</button>
      </div>

      <!-- Meaning Section -->
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 14px;">
        <div class="modal-field" style="margin-bottom: 0;">
          <div class="modal-label">日本語義 (Meaning JA)</div>
          <div class="modal-val" id="modalMeaningJa" style="font-weight: 600;">空、天蓋、蒼穹、大気</div>
        </div>
        <div class="modal-field" style="margin-bottom: 0;">
          <div class="modal-label">英語義 (Meaning EN)</div>
          <div class="modal-val" id="modalMeaningEn" style="color: var(--md-sys-color-on-surface-variant);">sky, firmament, celestial dome</div>
        </div>
      </div>

      <!-- Pronunciation & Phonetics Section -->
      <div class="modal-field" style="background: rgba(255,255,255,0.03); border: 1px solid var(--md-sys-color-outline-variant); border-radius: var(--radius-sm); padding: 10px 14px; margin-bottom: 14px;">
        <div class="modal-label" style="display: flex; justify-content: space-between; align-items: center;">
          <span>発音ガイド & 音声表記 (Phonetics & IPA)</span>
          <span id="modalIpa" style="font-family: monospace; font-size: 0.85rem; color: var(--md-sys-color-primary);">/[ʃe.len]/</span>
        </div>
        <div id="modalPronGuide" style="font-size: 0.88rem; color: var(--md-sys-color-on-surface); margin-top: 4px;">c=[ʃ]（シャ行音）。母音eは明瞭に発音。</div>
      </div>

      <div class="modal-field" id="modalNotesField" style="margin-bottom: 14px;">
        <div class="modal-label">使い方・補足</div>
        <div class="modal-val" id="modalNotes" style="font-size: 0.88rem; line-height: 1.5; color: var(--md-sys-color-on-surface-variant);"></div>
      </div>

      <!-- Enhanced: Forms Section -->
      <div class="modal-field" id="modalFormsField" style="display: none;">
        <div class="modal-label">主な形 <span style="font-size:0.72rem; font-weight:normal; color:var(--md-sys-color-outline);">(クリックでコピー)</span></div>
        <div class="modal-val" id="modalFormsList" style="display: flex; flex-wrap: wrap; gap: 6px; margin-top: 6px;"></div>
      </div>

      <!-- Enhanced: Contextual Examples Section -->
      <div class="modal-field" id="modalExamplesField" style="display: none;">
        <div class="modal-label">例文 <span style="font-size:0.75rem; font-weight:normal; color:var(--md-sys-color-outline);">(クリックで翻訳ボックスへ入力)</span></div>
        <div class="modal-val" id="modalExamplesList" style="display: flex; flex-direction: column; gap: 8px; margin-top: 6px;"></div>
      </div>

      <div class="modal-field" id="modalLiteraryField" style="display:none;">
        <div class="modal-label">物語の中で <span style="font-size:0.72rem;font-weight:normal;">日本語の物語用例</span></div>
        <p id="modalLiteraryQuote" style="line-height:1.9;margin:8px 0;"></p>
        <div id="modalLiterarySource" style="font-size:0.78rem;color:var(--md-sys-color-outline);"></div>
      </div>

      <div style="display: flex; gap: 10px; margin-top: 24px; border-top: 1px solid var(--md-sys-color-outline-variant); padding-top: 16px;">
        <button class="tool-btn" id="copyModalRoman">ローマ字をコピー</button>
        <button class="tool-btn" id="copyModalGlyph">星石文字をコピー</button>
      </div>
    </div>
  </div>

  <!-- Missing / Unsupported Queue Manager Modal -->
  <div class="modal-backdrop" id="queueModal">
    <div class="modal-box">
      <button type="button" class="modal-close-btn" id="queueCloseBtn" aria-label="閉じる">×</button>
      <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
        
        <h2 style="font-size: 1.3rem; font-weight: 600;">未対応リクエスト・キュー回収</h2>
      </div>
      <p style="font-size: 0.82rem; color: var(--md-sys-color-on-surface-variant); margin-bottom: 14px;">
        辞書検索や文章翻訳で未対応だった単語・構文を記録したキューです。JSONファイルとして一括回収（エクスポート）し、語彙・構文の拡充開発にそのまま活用できます。
      </p>

      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <span id="queueSummaryText" style="font-size: 0.88rem; font-weight: 600;">記録件数: 0 件</span>
        <button class="tool-btn" id="clearAllQueueBtn" style="color: var(--md-sys-color-error);">全て消去</button>
      </div>

      <label>未対応JSONを取込 <input type="file" id="importQueueFiles" accept=".json,application/json" multiple></label>
      <div id="queueImportPreview" role="status" aria-live="polite"></div>
      <button class="tool-btn" id="applyQueueImport" disabled>検証した記録を統合</button>
      <label>状態で表示 <select id="queueStatusFilter"><option value="all">すべて</option><option value="untriaged">未整理</option><option value="investigating">調査中</option><option value="implemented">実装済み</option><option value="review">審査待ち</option><option value="held">保留</option></select></label>
      <div class="queue-list" id="queueList"></div>

      <div style="display: flex; gap: 10px; margin-top: 16px; border-top: 1px solid var(--md-sys-color-outline-variant); padding-top: 16px; flex-wrap: wrap;">
        <button class="record-btn" id="exportQueueJsonBtn">JSONファイルで回収 (.json)</button>
        <button class="tool-btn" id="copyQueueJsonBtn">JSONをコピー</button>
      </div>
    </div>
  </div>

  <!-- Footer -->
  <footer class="app-footer">
    Nebulith Project &bull; Language Version 23.5 &bull; TrueType Font Version 2.5 &bull; Standalone PWA
  </footer>

  <!-- Scripts -->
  <script src="./data.js"></script>
  <script src="./bidirectional.js"></script>
  <script src="./incremental.js"></script>
  <script src="./workspace.js"></script>
  <script src="./app.js"></script>
</body>
</html>
'''

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(base_html)

    # Standalone HTML (with inline data.js and app.js)
    standalone_html = base_html.replace(
        '<script src="./data.js"></script>\n  <script src="./bidirectional.js"></script>\n  <script src="./incremental.js"></script>\n  <script src="./workspace.js"></script>\n  <script src="./app.js"></script>',
        f'<script>\n{data_js_content}\n{bidirectional_js}\n{incremental_js}\n{workspace_js}\n{app_js_content}\n</script>'
    )
    with open(standalone_path, 'w', encoding='utf-8') as f:
        f.write(standalone_html)

    update_service_worker(web_dir)

    files = ['tools/build_web_studio.py', 'tools/studio_dictionary.py', 'tools/extended_corpus.py', 'data/lexicon.json',
             'data/literary_sourcebook.json', 'data/lexicon_canonical_loci.json', 'docs/Valnes_Ibun.html', 'web/library.html', 'data/grammar_dictionary.json', 'data/usage_examples.json', 'data/verified_canonical_compounds.json', 'data/translation_extensions.json', 'data/translation_patterns.json', 'data/canon_corpus.json', 'data/extended_corpus_v2.json',
             'data/translation_input_rules.json', 'data/translation_input_fixtures.json', 'data/corpus_rules.json', 'data/compound_translation_patterns.json', 'data/roadmap_lexical_rules.json', 'data/studio_categories.json',
             'fonts/font_b64.txt', 'web/app.js', 'web/workspace.js', 'web/bidirectional.js', 'web/incremental.js', 'web/data.js',
             'web/index.html', 'web/standalone.html', 'web/manifest.json', 'web/service-worker.js', 'web/icon.svg', 'web/favicon.svg']
    hashes = {p: hashlib.sha256((Path(base_dir)/p).read_bytes()).hexdigest() for p in files}
    (Path(web_dir)/'build-manifest.json').write_text(json.dumps({'schemaVersion':1, 'sha256':hashes}, indent=2)+'\n', encoding='utf-8')

    print(f"Build completed:")
    print(f" - {html_path} ({os.path.getsize(html_path):,} bytes)")
    print(f" - {data_js_path} ({os.path.getsize(data_js_path):,} bytes)")
    print(f" - {standalone_path} ({os.path.getsize(standalone_path):,} bytes)")

if __name__ == '__main__':
    build_web_studio()

