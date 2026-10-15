"""Synchronize font bytes, corpus text and visible version labels separately."""
import base64
import html
import json
import re

from fontTools.ttLib import TTFont
from nebulith_data import ROOT, corpus_markdown, validate_corpus, corpus_semantic_pending


def main():
    font_path = ROOT / 'fonts/Nebulith-Regular.ttf'
    raw = font_path.read_bytes()
    b64 = base64.b64encode(raw).decode('ascii')
    font_version = TTFont(font_path)['name'].getDebugName(5).removeprefix('Version ')
    inventory = json.loads((ROOT / 'fonts/inventory.json').read_text(encoding='utf-8'))
    corpus = json.loads((ROOT / 'data/canon_corpus.json').read_text(encoding='utf-8'))
    vocab = json.loads((ROOT / 'data/lexicon.json').read_text(encoding='utf-8'))['vocabulary']
    errors = validate_corpus(corpus, vocab)
    if errors:
        raise ValueError(errors)
    pending = corpus_semantic_pending(corpus, vocab)
    review_label = ('字句参照を検証済み。意味・統語の審査は未完了です。' if pending else
                    '字句参照・公式コーパスの意味と項構造をAIが審査記録済み。リリース承認とは別です。')
    cards = ['<!-- BEGIN GENERATED CORPUS -->', '<section id="canon-corpus" class="specimen-card">',
             f'<h2>規範コーパス候補 v{html.escape(corpus["version"])}</h2>',
             '<p>'+review_label+'</p>']
    for unit in corpus['units']:
        cards += [f'<h3>{html.escape(unit["title"])}</h3>',
                  f'<div class="nebulith-font font-display-medium">{html.escape(unit["nrs"])}</div>',
                  f'<p class="roman-caption">{html.escape(unit["nrs"])}</p>',
                  f'<p>{html.escape(unit["translationJa"])}</p>']
    block = '\n'.join(cards+['</section>', '<!-- END GENERATED CORPUS -->'])
    for path in ['fonts/preview.html', 'tools/num_specimen.html']:
        p = ROOT / path
        text = p.read_text(encoding='utf-8')
        text, replacements = re.subn(r'base64,[A-Za-z0-9+/=]+', 'base64,'+b64, text)
        if replacements != 1:
            raise ValueError(f'Expected one embedded font in {path}, got {replacements}')
        text = text.replace('16主星子音', '18主星子音').replace('16 Roots', '18 Roots')
        text = text.replace('Completely De-Latinized', 'Glyph Specimen')
        text = text.replace('全グリフ完全脱ラテン化標本', '全グリフ標本（独自性評価は審査中）')
        text = text.replace('完全刷新されました。', '描画標本です。字形独自性は個別審査中です。')
        text = re.sub(r'Nebulith-Regular\.ttf (?:Specimen )?v[0-9.]+',
                      lambda m: ('Nebulith-Regular.ttf Specimen v' if 'Specimen' in m[0] else 'Nebulith-Regular.ttf v')+font_version, text)
        text = re.sub(r'Nebulith Script v[0-9.]+', 'Nebulith Script v'+font_version, text)
        if path == 'fonts/preview.html':
            if '<!-- BEGIN GENERATED CORPUS -->' in text:
                text, count = re.subn(r'<!-- BEGIN GENERATED CORPUS -->.*?<!-- END GENERATED CORPUS -->',
                                     lambda _: block, text, flags=re.S)
                if count != 1:
                    raise ValueError('Duplicate corpus blocks')
            else:
                title = text.index('Canon Corpus Specimen')
                start = text.rfind('  <div class="specimen-card">', 0, title)
                end = text.rfind('</div>\n</body>')
                if start < 0 or end < start:
                    raise ValueError('Unable to locate legacy corpus block')
                text = text[:start]+block+'\n'+text[end:]
            symbol_link = '<!-- SYMBOL SPECIMEN LINK --><p><a href="punctuation.html">疑問符・句読点・括弧・引用符・演算記号の専用字形標本</a></p>'
            if '<!-- SYMBOL SPECIMEN LINK -->' not in text:
                text = text.replace('</body>', symbol_link+'\n</body>')
        p.write_text(text, encoding='utf-8')
    (ROOT / 'fonts/font_b64.txt').write_text(b64, encoding='ascii')
    specimen_rows = []
    style_samples = ['Aa Ee Ii Oo Uu Yy Ss Zz Jj Ff Tt', '0123456789 ？? 。. 、, “ ” ( ) + =',
                     corpus['units'][0]['nrs'], corpus['units'][2]['nrs']]
    for size in [16, 24, 48, 72]:
        specimen_rows.append(f'<section><h2>{size}px</h2>'+''.join(
            f'<div class="sample" style="font-size:{size}px">{html.escape(sample)}</div>'
            f'<p class="caption">{html.escape(sample)}</p>' for sample in style_samples)+'</section>')
    handwriting = '''<!doctype html><html lang="ja"><meta charset="utf-8"><title>Nebulith 筆流標本 vVERSION</title>
<style>@font-face{font-family:Nebulith;src:url(data:font/ttf;base64,FONT)}
body{font:15px system-ui;margin:24px;color:#e7edf6;background:#101623}main{max-width:1100px;margin:auto}
h1{font-size:24px}h2{font-size:16px}section{padding:18px;border:1px solid #41516a;border-radius:12px;margin:16px 0}
.sample{font-family:Nebulith;line-height:1.8;overflow-wrap:anywhere}.caption{font-size:12px;color:#bbc8d9;line-height:1.6}
</style><main><h1>Nebulith 筆流・文字列標本 vVERSION</h1><p>同じ文字との比較と、周囲の字形との丸み・線幅・大きさ・字間を確認する標本です。人間の手書き・長文読字試験とは別です。</p>ROWS</main></html>'''
    (ROOT / 'fonts/handwriting.html').write_text(handwriting.replace('VERSION', font_version).replace('FONT', b64)
                                                .replace('ROWS', '\n'.join(specimen_rows)), encoding='utf-8')
    spec_path = ROOT / 'docs/Project Requirements And Design.md'
    spec = spec_path.read_text(encoding='utf-8')
    start = spec.index('<!-- BEGIN GENERATED CANON -->')
    spec_path.write_text(spec[:start]+corpus_markdown(corpus, vocab), encoding='utf-8')
    cells = []
    for symbol in inventory['symbols']:
        chars = html.escape(symbol['characters'])
        cells.append(f'<article><div class="sign">{html.escape(symbol["characters"][0])}</div>'
                     f'<b>{chars}</b><p>{html.escape(symbol["motif"])}</p></article>')
    specimen = '''<!doctype html><html lang="ja"><meta charset="utf-8"><title>Nebulith 記号標本</title>
<style>@font-face{font-family:Nebulith;src:url(data:font/ttf;base64,FONT)}
*{box-sizing:border-box}body{font-family:system-ui;background:#101623;color:#edf2f7;margin:0;padding:24px}
main{max-width:1000px;margin:auto}h1{font-size:24px}p{line-height:1.6}.muted{color:#b6c4d6}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px}
article,.sample{border:1px solid #34455e;border-radius:12px;padding:16px;background:#182235}
.sign{font:64px Nebulith,serif;line-height:1.4;color:#8cd5f5}article p{font-size:12px;color:#b6c4d6;margin-bottom:0}
.sample{margin-top:18px}.line{font:32px Nebulith,serif;line-height:1.8;overflow-wrap:anywhere}
code{white-space:normal}a{color:#8cd5f5}</style><main>
<h1>Nebulith 記号標本 vVERSION</h1><p class="muted">GLYPHSグリフ / MAPPED文字。全角・和文の別表記は同じ字形へ対応します。</p>
<div class="grid">CELLS</div>
<section class="sample"><h2>文中での表示</h2>
<div class="line">Poran el taas to kauo ka? Falun el vyrin!</div><code>Poran el taas to kauo ka? Falun el vyrin!</code>
<div class="line">“Relen el laris en taas ia sirin.” (Falun el vyr.)</div><code>“Relen el laris en taas ia sirin.” (Falun el vyr.)</code>
<div class="line">[1 + 2 = 3]; 4 × 2 = 8 / 6 ÷ 2 = 3 …</div><code>[1 + 2 = 3]; 4 × 2 = 8 / 6 ÷ 2 = 3 …</code>
<div class="line">？? ！！ 。. 、, （）() 「」“”</div><code>全角・和文と半角の対応</code>
<p class="muted">記号の意味は入力文字どおりです。音素キャリアの ' と、引用符 ‘ ’ は別の字形です。字形の独自性は監査の個別評価待ちです。</p></section>
<p><a href="preview.html">本文と文字・数字の標本へ</a></p></main>
<script>document.fonts.ready.then(()=>console.log(JSON.stringify({loaded:document.fonts.check('64px Nebulith'),symbols:document.querySelectorAll('article').length})))</script></html>'''
    specimen = (specimen.replace('FONT', b64).replace('VERSION', font_version)
                .replace('GLYPHS', str(inventory['glyphCount'])).replace('MAPPED', str(inventory['mappedCharacterCount']))
                .replace('CELLS', '\n'.join(cells)))
    (ROOT / 'fonts/punctuation.html').write_text(specimen, encoding='utf-8')
    print('Synchronized font bytes, visible font version and shared corpus source.')


if __name__ == '__main__':
    main()
