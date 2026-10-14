import os

with open(r'C:\Users\danun\Desktop\Project\Nebulith\fonts\font_b64.txt', 'r', encoding='utf-8') as f:
    b64 = f.read().strip()

html_content = f"""<!DOCTYPE html>
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
    padding: 16px 0;
  }}
  .container {{
    display: flex;
    flex-direction: column;
    gap: 18px;
  }}
  .header-card {{
    background: rgba(22, 27, 34, 0.75);
    border: 1px solid rgba(48, 54, 61, 0.8);
    border-radius: 12px;
    padding: 18px 24px;
  }}
  .title {{
    font-size: 20px;
    font-weight: 700;
    color: #e3b341;
    margin: 0 0 6px 0;
  }}
  .subtitle {{
    font-size: 13px;
    color: #8b949e;
    margin: 0;
  }}
  .nebulith-font {{
    font-family: 'Nebulith', sans-serif;
  }}
  .specimen-card {{
    background: rgba(22, 27, 34, 0.75);
    border: 1px solid rgba(48, 54, 61, 0.8);
    border-radius: 12px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 14px;
  }}
  .card-label {{
    font-size: 14px;
    font-weight: 600;
    color: #58a6ff;
    margin: 0;
  }}
  .font-display-large {{
    font-size: 44px;
    letter-spacing: 8px;
    color: #e3b341;
    line-height: 1.4;
    padding: 14px 18px;
    background: rgba(13, 17, 23, 0.6);
    border-radius: 8px;
    border: 1px solid rgba(48, 54, 61, 0.5);
  }}
  .font-display-medium {{
    font-size: 32px;
    letter-spacing: 5px;
    color: #e6edf3;
    line-height: 1.5;
    padding: 14px 18px;
    background: rgba(13, 17, 23, 0.6);
    border-radius: 8px;
    border: 1px solid rgba(48, 54, 61, 0.5);
  }}
  .roman-caption {{
    font-size: 13px;
    color: #8b949e;
    font-family: monospace;
  }}
</style>
</head>
<body>
<div class="container">
  <div class="header-card">
    <div class="title">✦ Nebulith-Regular.ttf 生成完了プレビュー</div>
    <p class="subtitle">実際に生成されたTrueTypeフォント（.ttf）を直結ロードしてレンダリングしています</p>
  </div>

  <div class="specimen-card">
    <div class="card-label">✦ 6大母音 ＆ 星軌数詞（0〜9）</div>
    <div class="nebulith-font font-display-large">a e i o u y</div>
    <div class="roman-caption">[Vowels]: a, e, i, o, u, y (Monophthongs)</div>
    
    <div class="nebulith-font font-display-large" style="font-size: 36px;">0 1 2 3 4 5 6 7 8 9</div>
    <div class="roman-caption">[Numerals]: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 (Orbital Numerals)</div>
  </div>

  <div class="specimen-card">
    <div class="card-label">✦ 16主星子音（Consonants）</div>
    <div class="nebulith-font font-display-medium">m n l r s z c j f v h w p t k b d g</div>
    <div class="roman-caption">m n l r  s z c j  f v h w  p t k b d g</div>
  </div>

  <div class="specimen-card">
    <div class="card-label">✦ 参考文章（VSO天体軌道構文）の実フォント組版</div>
    <div class="nebulith-font font-display-medium" style="color: #e3b341;">
      Esara el sylim ia lymis en keiran.
    </div>
    <div class="roman-caption">
      [NRS転写]: Esara el sylim ia lymis en keiran.<br>
      [日本語訳]: 星は、光の軌道である。（コピュラ構文）
    </div>

    <div class="nebulith-font font-display-medium" style="margin-top: 8px;">
      Dokilor el an ku ri uo dokilad.
    </div>
    <div class="roman-caption">
      [NRS転写]: Dokilor el an ku ri uo dokilad.<br>
      [日本語訳]: 私は彼と共に学校で教師をしている。（VSO構文）
    </div>
  </div>
</div>
</body>
</html>
"""

out_path = r'C:\Users\danun\Desktop\Project\Nebulith\fonts\preview.html'
with open(out_path, 'w', encoding='utf-8') as out:
    out.write(html_content)

print("Created preview.html successfully!")
