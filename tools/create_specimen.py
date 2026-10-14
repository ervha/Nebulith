import base64

with open('fonts/font_b64.txt', 'r', encoding='utf-8') as f:
    b64 = f.read().strip()

html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<style>
  @font-face {{
    font-family: 'Nebulith';
    src: url('data:font/truetype;charset=utf-8;base64,{b64}') format('truetype');
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    color: #e6edf3;
    margin: 0;
    padding: 10px 0;
  }}
  .container {{
    display: flex;
    flex-direction: column;
    gap: 16px;
  }}
  .card {{
    background: rgba(22, 27, 34, 0.85);
    border: 1px solid rgba(48, 54, 61, 0.8);
    border-radius: 12px;
    padding: 18px 20px;
  }}
  .badge {{
    display: inline-block;
    padding: 3px 8px;
    font-size: 11px;
    font-weight: 600;
    border-radius: 6px;
    background: rgba(56, 139, 253, 0.2);
    color: #58a6ff;
    border: 1px solid rgba(56, 139, 253, 0.4);
    margin-bottom: 8px;
  }}
  .title {{
    font-size: 16px;
    font-weight: 700;
    color: #e3b341;
    margin-bottom: 12px;
  }}
  .nebulith {{
    font-family: 'Nebulith', sans-serif;
  }}
  .comparison-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }}
  .glyph-box {{
    background: rgba(13, 17, 23, 0.85);
    border: 1px solid rgba(48, 54, 61, 0.7);
    border-radius: 10px;
    padding: 16px;
    text-align: center;
  }}
  .glyph-char {{
    font-size: 80px;
    color: #e3b341;
    line-height: 1.1;
    margin: 8px 0;
  }}
  .glyph-name {{
    font-size: 14px;
    font-weight: 600;
    color: #58a6ff;
  }}
  .glyph-desc {{
    font-size: 12px;
    color: #8b949e;
    margin-top: 6px;
    line-height: 1.45;
    text-align: left;
  }}
  .all-digits {{
    display: flex;
    justify-content: space-around;
    align-items: center;
    background: rgba(13, 17, 23, 0.85);
    border: 1px solid rgba(48, 54, 61, 0.7);
    border-radius: 10px;
    padding: 16px 10px;
    margin-top: 8px;
  }}
  .digit-item {{
    text-align: center;
  }}
  .digit-item .char {{
    font-size: 34px;
    color: #f0f6fc;
  }}
  .digit-item.highlight .char {{
    color: #e3b341;
    font-size: 40px;
  }}
  .digit-item .sub {{
    font-size: 11px;
    color: #8b949e;
    font-family: monospace;
    margin-top: 4px;
  }}
  .digit-item.highlight .sub {{
    color: #58a6ff;
    font-weight: bold;
  }}
</style>
</head>
<body>
<div class="container">
  <div class="card">
    <div class="badge">REFINED GLYPH ARCHITECTURE</div>
    <div class="title">✦ 数字「7」「8」の再設計（アラビア数字からの完全脱却）</div>
    <div class="comparison-grid">
      <div class="glyph-box">
        <div class="glyph-name">【7】Septet Canopy Arc（七星天蓋弧）</div>
        <div class="nebulith glyph-char">7</div>
        <div class="glyph-desc">
          直角折れの地球アラビア数字を破棄。<br>
          天球を覆う「天蓋ドームアーチ」と、天頂から下降する「星流柱」、そして昴（プレアデス）を象徴する整列星ノード群で構成。
        </div>
      </div>
      <div class="glyph-box">
        <div class="glyph-name">【8】Bipolar Horizon（双極連星環）</div>
        <div class="nebulith glyph-char">8</div>
        <div class="glyph-desc">
          上下の丸2つを重ねた雪だるま型を破棄。<br>
          中央の連星共鳴核（二重円環）と、左右に大きく広がる「対向三日月翼」および双極端の連星ノードで構成。
        </div>
      </div>
    </div>
  </div>

  <div class="card">
    <div class="title">✦ 星軌数詞（0 〜 9）連続シークエンス比較</div>
    <div class="all-digits">
      <div class="digit-item"><div class="nebulith char">0</div><div class="sub">0 (環)</div></div>
      <div class="digit-item"><div class="nebulith char">1</div><div class="sub">1 (柱)</div></div>
      <div class="digit-item"><div class="nebulith char">2</div><div class="sub">2 (月)</div></div>
      <div class="digit-item"><div class="nebulith char">3</div><div class="sub">3 (三葉)</div></div>
      <div class="digit-item"><div class="nebulith char">4</div><div class="sub">4 (環星)</div></div>
      <div class="digit-item"><div class="nebulith char">5</div><div class="sub">5 (五芒)</div></div>
      <div class="digit-item"><div class="nebulith char">6</div><div class="sub">6 (彗尾)</div></div>
      <div class="digit-item highlight"><div class="nebulith char">7</div><div class="sub">7 (天蓋弧)</div></div>
      <div class="digit-item highlight"><div class="nebulith char">8</div><div class="sub">8 (双極環)</div></div>
      <div class="digit-item"><div class="nebulith char">9</div><div class="sub">9 (渦)</div></div>
    </div>
  </div>
</div>
</body>
</html>
"""

with open('tools/num_specimen.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Generated tools/num_specimen.html')
