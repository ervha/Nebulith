# tools/generate_preview_html.py
import os

with open(r'fonts/font_b64.txt', 'r', encoding='ascii') as f:
    b64 = f.read().strip()

html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>Nebulith-Regular.ttf Specimen v2.0</title>
<style>
  @font-face {{
    font-family: 'Nebulith';
    src: url('data:font/truetype;charset=utf-8;base64,{b64}') format('truetype');
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #0b0f19;
    color: #e6edf3;
    margin: 0;
    padding: 24px;
  }}
  .container {{
    max-width: 900px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 20px;
  }}
  .header-card {{
    background: rgba(22, 27, 34, 0.85);
    border: 1px solid rgba(56, 189, 248, 0.3);
    border-radius: 12px;
    padding: 20px 28px;
    box-shadow: 0 10px 25px -5px rgba(0,0,0,0.5);
  }}
  .title {{
    font-size: 22px;
    font-weight: 700;
    color: #38bdf8;
    margin: 0 0 6px 0;
  }}
  .subtitle {{
    font-size: 13px;
    color: #94a3b8;
    margin: 0;
  }}
  .nebulith-font {{
    font-family: 'Nebulith', sans-serif;
  }}
  .specimen-card {{
    background: rgba(17, 24, 39, 0.75);
    border: 1px solid rgba(48, 54, 61, 0.8);
    border-radius: 12px;
    padding: 22px;
    display: flex;
    flex-direction: column;
    gap: 14px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
  }}
  .card-label {{
    font-size: 14px;
    font-weight: 600;
    color: #a78bfa;
    margin: 0;
    display: flex;
    justify-content: space-between;
  }}
  .font-display-large {{
    font-size: 40px;
    letter-spacing: 8px;
    color: #e2e8f0;
    line-height: 1.4;
    padding: 16px 20px;
    background: rgba(15, 23, 42, 0.6);
    border-radius: 8px;
    border: 1px solid rgba(56, 189, 248, 0.2);
  }}
  .font-display-medium {{
    font-size: 28px;
    letter-spacing: 4px;
    color: #f8fafc;
    line-height: 1.6;
    padding: 16px 20px;
    background: rgba(15, 23, 42, 0.6);
    border-radius: 8px;
    border: 1px solid rgba(56, 189, 248, 0.2);
  }}
  .roman-caption {{
    font-size: 13px;
    color: #94a3b8;
    font-family: monospace;
    line-height: 1.6;
  }}
</style>
</head>
<body>
<div class="container">
  <div class="header-card">
    <div class="title">🌌 Nebulith-Regular.ttf v2.0 全グリフ完全脱ラテン化標本</div>
    <p class="subtitle">数字「0〜9」・母音6・主子音16・約物のすべてが、天体力学・星辰観測幾何学の統一デザイン言語で完全刷新されました。</p>
  </div>

  <div class="specimen-card">
    <div class="card-label">
      <span>✦ 6大星辰母音（Astral Monophthongs）</span>
      <span style="font-size:12px; color:#38bdf8;">a, e, i, o, u, y</span>
    </div>
    <div class="nebulith-font font-display-large" style="color:#38bdf8;">a e i o u y</div>
    <div class="roman-caption">[NRS]: a (黎明天蓋弧), e (星風二連交差波), i (北極星尖塔), o (満月軌道環), u (深淵受容杯), y (第6星辰結晶環)</div>
  </div>

  <div class="specimen-card">
    <div class="card-label">
      <span>✦ 16主星子音（Primary Consonants - Completely De-Latinized）</span>
      <span style="font-size:12px; color:#a78bfa;">16 Roots</span>
    </div>
    <div class="nebulith-font font-display-large" style="font-size: 32px; letter-spacing: 6px;">
      m n l r  s z c j  f v h w  p t k b d g
    </div>
    <div class="roman-caption">
      [鼻音・流音]: m (双天球交差翼), n (始動スパイラル), l (天頂スピンドル), r (三日月公転スウィープ)<br>
      [歯擦・摩擦]: s (双極磁場弧), z (連星共鳴環), c (静寂天蓋シェード), j (深淵旋回アンカー)<br>
      [唇音・気音]: f (上昇オーロラ翼), v (受容ボウル星核), h (双対天門ピラー), w (重力井戸波紋)<br>
      [破裂音群]: p (懸垂光芒ポッド), t (反り天蓋アンカー), k (三方放射光芒), b (二重軌道シェル), d (台座尖塔), g (重力屈折環)
    </div>
  </div>

  <div class="specimen-card">
    <div class="card-label">
      <span>✦ 星軌数詞（Orbital Numerals 0〜9）</span>
      <span style="font-size:12px; color:#facc15;">0 1 2 3 4 5 6 7 8 9</span>
    </div>
    <div class="nebulith-font font-display-large" style="color:#facc15;">0 1 2 3 4 5 6 7 8 9</div>
    <div class="roman-caption">
      0 (特異点照準環), 1 (単極重力尖塔), 2 (対向公転三日月), 3 (三つ葉トリスケル), 4 (四天球ダイヤ),<br>
      5 (五芒螺旋リボン), 6 (彗星核テイル), 7 (七星天蓋弧), 8 (双極連星環), 9 (頂点日食コロナ)
    </div>
  </div>

  <div class="specimen-card">
    <div class="card-label">
      <span>✦ 公式規範テクスト（Canon Corpus Specimen）</span>
      <span style="font-size:12px; color:#34d399;">VSO軌道統語論 ＆ 星辰幾何学組版</span>
    </div>

    <!-- 箴言 -->
    <div class="nebulith-font font-display-medium" style="color: #38bdf8;">
      Relen el vyran ia tolst en sentis: tor poran el havel, ne korol el falun en vyr.
    </div>
    <div class="roman-caption">
      <b>[星辰箴言]</b> Relen el vyran ia tolst en sentis: tor poran el havel, ne korol el falun en vyr.<br>
      <b>[日本語訳]</b> 真理は万物の床（礎）である。時が歩み去ろうとも、星の光が尽き果てることはない。
    </div>

    <!-- 天文日誌 -->
    <div class="nebulith-font font-display-medium" style="color: #e2e8f0; margin-top: 10px;">
      Fe vyrelcor el vyrelor uo vyrelar to falden. Falunast el vyr syvani uo celvan.
    </div>
    <div class="roman-caption">
      <b>[観測日誌]</b> Fe vyrelcor el vyrelor uo vyrelar to falden. Falunast el vyr syvani uo celvan.<br>
      <b>[日本語訳]</b> 天文学者は天文台にて東の空を観測した。天球に新たな星が光を放ち始めた。
    </div>

    <!-- 相関詞・日常対話 -->
    <div class="nebulith-font font-display-medium" style="color: #facc15; margin-top: 10px;">
      Hite relen el govan en dolas, vate relen el vyrelar.
    </div>
    <div class="roman-caption">
      <b>[相関詞構文]</b> Hite relen el govan en dolas, vate relen el vyrelar.<br>
      <b>[日本語訳]</b> これが友の家であり、あれが天文台である。（近称 hite vs 遠称 vate）
    </div>
  </div>
</div>
</body>
</html>
"""

with open('fonts/preview.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("fonts/preview.html successfully rebuilt with complete v2.0 specimen!")
