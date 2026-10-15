# tools/generate_dashboard_v20.py
import json

with open("data/lexicon.json", "r", encoding="utf-8") as f:
    data = json.load(f)

categories = data["categories"]
total = data["totalEntries"]
goal = data["targetGoal"]
pct = data["currentProgressPercent"]
ver = data["version"]

rows_html = ""
for c in categories:
    bar_width = min(100, int((c["wordsCount"] / 115) * 100))
    rows_html += f"""
    <tr>
      <td style="font-weight:600; color:#38bdf8; padding:7px 10px; border-bottom:1px solid #1e293b;">{c['id']}</td>
      <td style="font-weight:600; color:#f8fafc; padding:7px 10px; border-bottom:1px solid #1e293b;">{c['name']}</td>
      <td style="text-align:right; font-weight:700; color:#a78bfa; padding:7px 10px; border-bottom:1px solid #1e293b;">{c['wordsCount']}語</td>
      <td style="padding:7px 10px; border-bottom:1px solid #1e293b;">
        <div style="background:#0f172a; border-radius:4px; height:8px; width:100%; overflow:hidden;">
          <div style="background:linear-gradient(90deg, #38bdf8, #818cf8); height:100%; width:{bar_width}%;"></div>
        </div>
      </td>
      <td style="color:#94a3b8; font-size:12px; padding:7px 10px; border-bottom:1px solid #1e293b;">{c['description']}</td>
    </tr>
    """

html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<style>
  body {{
    margin: 0;
    padding: 12px 0;
    color: var(--foreground, #e2e8f0);
    font-family: var(--font-sans, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif);
  }}
  .card {{
    background: var(--card, #111827);
    border: 1px solid var(--border, #1f2937);
    border-radius: var(--radius, 12px);
    padding: 20px;
    box-shadow: 0 10px 25px -5px rgba(0,0,0,0.5);
  }}
  .header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--border, #1f2937);
    padding-bottom: 14px;
    margin-bottom: 16px;
  }}
  .badge {{
    background: rgba(56, 189, 248, 0.15);
    color: #38bdf8;
    border: 1px solid rgba(56, 189, 248, 0.3);
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
  }}
  .progress-box {{
    background: var(--muted, #1e293b);
    border-radius: 8px;
    padding: 14px;
    margin-bottom: 20px;
    border: 1px solid var(--border, #334155);
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 12px;
  }}
  th {{
    text-align: left;
    padding: 8px 10px;
    background: var(--muted, #1e293b);
    color: var(--muted-foreground, #94a3b8);
    font-weight: 600;
    border-bottom: 2px solid var(--border, #334155);
  }}
</style>
</head>
<body>
<div class="card">
  <div class="header">
    <div>
      <h2 style="margin:0; font-size:18px;">🌌 Nebulith Master Lexicon v{ver}</h2>
      <p style="margin:4px 0 0 0; color:var(--muted-foreground, #94a3b8); font-size:12px;">全16カテゴリー・{total}語幹拡充ステータス</p>
    </div>
    <div>
      <span class="badge">目標1,000語中 {pct}% 達成</span>
    </div>
  </div>

  <div class="progress-box">
    <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-weight:600; font-size:13px;">
      <span>総合語彙マイルストーン進捗</span>
      <span style="color:#38bdf8;">{total} / {goal} 語幹 ({pct}%)</span>
    </div>
    <div style="background:#0f172a; border-radius:6px; height:12px; width:100%; overflow:hidden;">
      <div style="background:linear-gradient(90deg, #38bdf8, #a855f7); height:100%; width:{pct}%;"></div>
    </div>
  </div>

  <table>
    <thead>
      <tr>
        <th style="width:24px;">#</th>
        <th style="width:170px;">カテゴリー名 (16 Domains)</th>
        <th style="width:50px; text-align:right;">語彙数</th>
        <th style="width:90px;">規模分布</th>
        <th>ドメイン概要</th>
      </tr>
    </thead>
    <tbody>
      {rows_html}
    </tbody>
  </table>
</div>
</body>
</html>
"""

with open("docs/dashboard_v20.html", "w", encoding="utf-8") as f:
    f.write(html_content)
print("Dashboard HTML generated at docs/dashboard_v20.html")
