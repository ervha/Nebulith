"""Create local-font visual comparison sheets without redistributing Arial."""
import base64
import hashlib
import html
import json
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from nebulith_data import ROOT, dump


def main():
    font_path = ROOT / 'fonts/Nebulith-Regular.ttf'
    reference_path = Path('C:/Windows/Fonts/arial.ttf')
    font, reference = TTFont(font_path), TTFont(reference_path)
    glyphs = font.getGlyphSet()
    cmap = font.getBestCmap()
    inv = json.loads((ROOT / 'fonts/inventory.json').read_text(encoding='utf-8'))
    version = inv['fontVersion']
    out = ROOT / f'audit/comparisons/glyph-v{version}'
    out.mkdir(parents=True, exist_ok=False)
    groups = {'letters-lower': [], 'letters-upper': [], 'numbers': [], 'symbols': []}
    metadata = []
    for name in font.getGlyphOrder():
        codes = [c for c, g in cmap.items() if g == name]
        primary = next((c for c in codes if c < 128), codes[0] if codes else None)
        char = chr(primary) if primary is not None else None
        group = 'letters-lower' if char and 'a' <= char <= 'z' else 'letters-upper' if char and 'A' <= char <= 'Z' else 'numbers' if char and char.isdigit() else 'symbols'
        pen = SVGPathPen(glyphs)
        glyphs[name].draw(pen)
        path = pen.getCommands()
        reference_char = html.escape(char) if char and char != ' ' else '（空白）' if char == ' ' else '（欠字枠）'
        svg = f'<svg viewBox="0 -200 1000 1100"><path transform="translate(0 700) scale(1 -1)" d="{path}"/></svg>'
        card = f'<article id="glyph-{name}"><h2>{html.escape(name)} {"U+%04X"%primary if primary else ""}</h2><div class="pair"><div>{svg}<small>Nebulith</small></div><div class="reference">{reference_char}<small>Arial</small></div></div><p>advance {font["hmtx"][name][0]}</p></article>'
        groups[group].append(card)
        metadata.append({'glyph': name, 'codepoints': codes,
                         'outlineSha256': hashlib.sha256(path.encode()).hexdigest(),
                         'comparisonReference': f'audit/comparisons/glyph-v{version}/{group}.html#glyph-{name}'})
    style = '''<style>body{font-family:system-ui;background:#fff;color:#182532;margin:16px}h1{font-size:20px}
.grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}article{border:1px solid #ccd4da;padding:10px;break-inside:avoid}h2{font-size:12px;margin:0}.pair{display:grid;grid-template-columns:1fr 1fr}.pair>div{height:110px;text-align:center}svg{height:88px;width:100%;fill:#182532}small{display:block;font:11px system-ui;color:#566979}.reference{font:64px Arial,sans-serif;line-height:88px}p{font-size:11px}a{color:#1c6284}</style>'''
    for group, cards in groups.items():
        page = '<!doctype html><html lang="ja"><meta charset="utf-8">'+style+f'<h1>Nebulith v{version} / Arial — {group}</h1><p>全87字形の比較資料。Arialは端末のローカルフォントを参照し、フォントファイルを複製しない。対応する同じコードの文字と骨格を比較する。別の文字との偶然の類似は判定対象外。</p><div class="grid">'+''.join(cards)+'</div></html>'
        (out / f'{group}.html').write_text(page, encoding='utf-8')
    digest = hashlib.sha256(font_path.read_bytes()).hexdigest()
    dump(out / 'inventory.json', {'fontSha256': digest, 'fontVersion': inv['fontVersion'],
         'reference': {'family': reference['name'].getDebugName(1), 'version': reference['name'].getDebugName(5),
                       'sha256': hashlib.sha256(reference_path.read_bytes()).hexdigest(),
                       'localPath': str(reference_path), 'redistributed': False}, 'glyphs': metadata})
    reviews = {'fontSha256': digest, 'criteriaVersion': f'SOP-v{version}-skeletal-compare-1',
               'comparisonScope': 'corresponding-codepoint',
               'criteria': '点・小装飾のみを主骨格変更と数えず、幹・開口・ループ・接続を比較する。全字形へ一律の合格を与えない。',
               'entries': [{**row, 'decision': 'pending', 'reason': '', 'reviewer': ''} for row in metadata]}
    dump(ROOT / 'data/audit/glyph_reviews.json', reviews)
    print('Prepared 87 glyph comparisons; generation alone does not approve or reject any glyph.')


if __name__ == '__main__':
    main()
