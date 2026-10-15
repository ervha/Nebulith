import os

def create_snippet():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    font_b64_path = os.path.join(base_dir, 'fonts', 'font_b64.txt')
    out_path = os.path.join(base_dir, 'web', 'thread_render.html')

    with open(font_b64_path, 'r', encoding='utf-8') as f:
        b64 = f.read().strip()

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @font-face {{
    font-family: 'Nebulith';
    src: url('data:font/ttf;base64,{b64}') format('truetype');
  }}
  :root {{
    font-family: var(--font-sans, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif);
    color: var(--foreground, #e2e2e9);
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  
  .container {{
    display: flex;
    flex-direction: column;
    gap: 16px;
    padding: 4px 0;
  }}

  /* Comparison Banner */
  .compare-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
  }}
  @media (max-width: 580px) {{
    .compare-grid {{ grid-template-columns: 1fr; }}
  }}
  .card {{
    background: var(--card, #1e2025);
    border: 1px solid var(--border, #44474f);
    border-radius: var(--radius, 12px);
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }}
  .card.highlight {{
    border-color: var(--primary, #a8c7fa);
    background: var(--accent-surface, rgba(168, 199, 250, 0.06));
    box-shadow: 0 0 16px rgba(168, 199, 250, 0.1);
  }}
  .badge {{
    display: inline-block;
    padding: 3px 10px;
    border-radius: 9999px;
    font-size: 11px;
    font-weight: 600;
    width: fit-content;
  }}
  .badge-exe {{ background: rgba(255, 180, 171, 0.15); color: #ffb4ab; }}
  .badge-web {{ background: rgba(168, 199, 250, 0.2); color: #a8c7fa; }}

  .metric-row {{
    display: flex;
    justify-content: space-between;
    font-size: 12.5px;
    border-bottom: 1px dashed var(--border, #33353a);
    padding-bottom: 5px;
  }}
  .metric-label {{ color: var(--muted-foreground, #8e9099); }}
  .metric-val {{ font-weight: 600; }}

  /* Interactive Web Mockup */
  .mockup-wrap {{
    background: var(--card, #191c20);
    border: 1px solid var(--primary, #a8c7fa);
    border-radius: var(--radius, 12px);
    padding: 18px;
    display: flex;
    flex-direction: column;
    gap: 14px;
  }}
  .mockup-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--border, #44474f);
    padding-bottom: 10px;
  }}
  .mockup-title {{
    font-size: 14px;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--primary, #a8c7fa);
  }}
  .mockup-tabs {{
    display: flex;
    gap: 6px;
  }}
  .mockup-tab {{
    background: rgba(255,255,255,0.06);
    border: none;
    color: var(--muted-foreground, #8e9099);
    padding: 4px 10px;
    font-size: 11px;
    border-radius: 6px;
  }}
  .mockup-tab.active {{
    background: var(--primary, #a8c7fa);
    color: #062e6f;
    font-weight: 600;
  }}

  /* Interactive Demo */
  .demo-input {{
    width: 100%;
    padding: 10px 14px;
    background: rgba(0,0,0,0.25);
    border: 1px solid var(--border, #44474f);
    border-radius: 8px;
    color: inherit;
    font-size: 13.5px;
    outline: none;
  }}
  .demo-input:focus {{
    border-color: var(--primary, #a8c7fa);
  }}
  .demo-output-box {{
    background: rgba(0,0,0,0.2);
    border-radius: 8px;
    padding: 14px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    border: 1px solid var(--border, #33353a);
  }}
  .neb-font {{
    font-family: 'Nebulith', sans-serif;
    font-size: 26px;
    color: var(--primary, #a8c7fa);
    line-height: 1.3;
    letter-spacing: 0.05em;
  }}
  .demo-caption {{
    font-size: 11.5px;
    color: var(--muted-foreground, #8e9099);
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 6px;
  }}
</style>
</head>
<body>
<div class="container">
  
  <div class="compare-grid">
    <div class="card">
      <span class="badge badge-exe">現行: デスクトップEXE</span>
      <h3 style="font-size: 14px;">単一実行ファイル版</h3>
      <div class="metric-row">
        <span class="metric-label">ファイル容量</span>
        <span class="metric-val">92 MB (JRE同梱)</span>
      </div>
      <div class="metric-row">
        <span class="metric-label">対応OS</span>
        <span class="metric-val">Windows x64 のみ</span>
      </div>
      <div class="metric-row">
        <span class="metric-label">起動障壁</span>
        <span class="metric-val">SmartScreen警告の可能性</span>
      </div>
      <div class="metric-row">
        <span class="metric-label">配布形態</span>
        <span class="metric-val">ZIP配布・ローカル解凍</span>
      </div>
    </div>

    <div class="card highlight">
      <span class="badge badge-web">移行案: Webアプリケーション</span>
      <h3 style="font-size: 14px; color: var(--primary, #a8c7fa);">Nebulith Web Studio (SPA/PWA)</h3>
      <div class="metric-row">
        <span class="metric-label">ファイル容量</span>
        <span class="metric-val" style="color: var(--primary, #a8c7fa);">約 193 KB (約1/470)</span>
      </div>
      <div class="metric-row">
        <span class="metric-label">対応環境</span>
        <span class="metric-val">全OS (Win, Mac, iOS, Android)</span>
      </div>
      <div class="metric-row">
        <span class="metric-label">起動障壁</span>
        <span class="metric-val" style="color: #6dd58c;">0秒 / ブラウザで開くだけ</span>
      </div>
      <div class="metric-row">
        <span class="metric-label">オフライン性</span>
        <span class="metric-val">完全オフライン (PWA対応)</span>
      </div>
    </div>
  </div>

  <div class="mockup-wrap">
    <div class="mockup-header">
      <div class="mockup-title">
        <span>🌌</span>
        <span>Nebulith Web Studio (プロトタイプ生成済み: web/index.html)</span>
      </div>
      <div class="mockup-tabs">
        <button class="mockup-tab active">リアルタイム変換</button>
        <button class="mockup-tab">1,008語辞書</button>
        <button class="mockup-tab">公式コーパス</button>
      </div>
    </div>

    <div>
      <div style="font-size: 11.5px; margin-bottom: 6px; color: var(--muted-foreground, #8e9099);">
        ローマ字入力でWebフォント（Nebulith-Regular v2.5 base64）による星石文字をリアルタイム描画：
      </div>
      <input type="text" class="demo-input" id="nebInput" value="Vyrel el mi ia vyr pyrin." placeholder="文字を入力...">
    </div>

    <div class="demo-output-box">
      <div class="neb-font" id="nebOutput">Vyrel el mi ia vyr pyrin.</div>
      <div class="demo-caption">
        <span>星石語レンダリング: <strong style="color: var(--primary, #a8c7fa);">Version 2.5 正本字形</strong></span>
        <span>逐語訳: 「私は赤い星を観測します。」</span>
      </div>
    </div>
  </div>

</div>

<script>
  const inp = document.getElementById('nebInput');
  const out = document.getElementById('nebOutput');
  inp.addEventListener('input', () => {{
    out.textContent = inp.value || 'Vyrel el mi ia vyr pyrin.';
  }});
</script>
</body>
</html>"""

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Created thread_render.html ({len(html)} bytes)")

if __name__ == '__main__':
    create_snippet()
