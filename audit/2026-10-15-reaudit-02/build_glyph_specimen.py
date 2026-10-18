"""Build an inspection artifact from the audited binary in the reaudit directory."""
import base64
import html
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

root = Path(__file__).resolve().parents[2]
raw = (root / 'fonts/Nebulith-Regular.ttf').read_bytes()
font = TTFont(root / 'fonts/Nebulith-Regular.ttf')
cmap = font.getBestCmap()
glyphs = font.getGlyphSet()
cells = []
for code, name in sorted(cmap.items()):
    char = chr(code)
    label = 'SPACE' if code == 32 else html.escape(char)
    cells.append(f'<div><small>U+{code:04X} {label}</small><span>{html.escape(char)}</span></div>')
pen = SVGPathPen(glyphs)
glyphs['.notdef'].draw(pen)
cells.append('<div><small>.notdef (outline)</small><svg viewBox="0 0 1000 1000">'
             f'<path transform="translate(0 850) scale(1 -1)" d="{pen.getCommands()}"/></svg></div>')
page = '''<!doctype html><html lang="ja"><meta charset="utf-8"><style>
@font-face{font-family:Nebulith;src:url(data:font/ttf;base64,FONT)}
body{font-family:system-ui;color:#182532;background:#fff;margin:16px}
h1{font-size:18px}p{font-size:12px}.grid{display:grid;grid-template-columns:repeat(8,1fr);gap:6px}
.grid>div{border:1px solid #ccd4da;min-height:93px;padding:6px}
small{display:block;font-size:11px}.grid span{display:block;font:60px Nebulith;line-height:76px}
svg{height:76px;width:76px;fill:#182532}
</style><h1>Nebulith 全65グリフ再監査標本 (v2.1)</h1><p>64 cmap文字 + .notdef。空白は意図した非描画。数字・大小文字・約物を全件表示。</p><div class="grid">CELLS</div>
<script>document.fonts.ready.then(()=>console.log(JSON.stringify({fonts:[...document.fonts].map(f=>({family:f.family,status:f.status})),loaded:document.fonts.check('60px Nebulith'),cells:document.querySelectorAll('.grid>div').length})))</script></html>'''
(root / 'audit/2026-10-15-reaudit-02/glyph-specimen.html').write_text(
    page.replace('FONT', base64.b64encode(raw).decode()).replace('CELLS',''.join(cells)), encoding='utf-8')
print("Successfully generated audit/2026-10-15-reaudit-02/glyph-specimen.html")
