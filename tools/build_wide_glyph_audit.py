"""Historical research utility, excluded from the current same-codepoint SOP.

Rank cross-script silhouettes for optional research; similarity is not a verdict.

Uses only fontTools. Local reference fonts are identified, never redistributed.
Glyph outlines are flattened and fit into a common square preserving aspect ratio.
Nonzero fill masks provide IoU candidates, not skeleton or readability proofs.
"""
import argparse
import hashlib
import html
import json
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from nebulith_data import ROOT, dump

SIZE = 48
REFERENCE_FILES = ['arial.ttf', 'times.ttf', 'consola.ttf', 'seguisym.ttf', 'meiryo.ttc']
REPERTOIRE = sorted(set(range(33,127)) | set(range(0x391,0x3ca)) |
                    set(range(0x410,0x450)) | set(range(0x621,0x64b)) |
                    set(range(0x3041,0x3097)) | set(range(0x30a1,0x30fb)) |
                    {ord(c) for c in '一二三十人口日月木山川田中土大天上下左右水火石工口円〇ΦΨΩθφψωЖФЦШЩЪЬЫЭЮЯ∞∅∂∇∈∩∪⊂⊃⊕⊗⊥⊢⊣△▽◇□○◎◉◌◍●◐◑◒◓◔◕◖◗☉☊☋♁♀♂♃♄♅♆♇♧♤♡♢†‡±÷×=+−…:;()[]{}'})


class FlattenPen(BasePen):
    def __init__(self, glyphs):
        super().__init__(glyphs)
        self.contours = []
    def _moveTo(self, p):
        self.points = [p]
    def _lineTo(self, p):
        self.points.append(p)
    def _qCurveToOne(self, control, end):
        start = self._getCurrentPoint()
        for n in range(1, 13):
            t = n/12
            self.points.append(tuple((1-t)**2*start[i]+2*(1-t)*t*control[i]+t*t*end[i] for i in [0,1]))
    def _curveToOne(self, a, b, end):
        start = self._getCurrentPoint()
        for n in range(1, 17):
            t = n/16
            self.points.append(tuple((1-t)**3*start[i]+3*(1-t)**2*t*a[i]+3*(1-t)*t*t*b[i]+t**3*end[i] for i in [0,1]))
    def _closePath(self):
        self.contours.append(self.points)
    def _endPath(self):
        self._closePath()


def silhouette(glyphs, name):
    pen = FlattenPen(glyphs)
    glyphs[name].draw(pen)
    all_points = [p for c in pen.contours for p in c]
    if not all_points:
        return 0
    lo = [min(p[i] for p in all_points) for i in [0,1]]
    hi = [max(p[i] for p in all_points) for i in [0,1]]
    scale = (SIZE-4)/max(hi[i]-lo[i] for i in [0,1])
    offset = [(SIZE-(hi[i]-lo[i])*scale)/2 for i in [0,1]]
    contours = [[tuple((p[i]-lo[i])*scale+offset[i] for i in [0,1]) for p in c] for c in pen.contours]
    mask = 0
    for y in range(SIZE):
        crossings = []
        for c in contours:
            for a,b in zip(c,c[1:]+c[:1]):
                if min(a[1],b[1]) <= y+.5 < max(a[1],b[1]):
                    x = a[0]+(y+.5-a[1])*(b[0]-a[0])/(b[1]-a[1])
                    crossings.append((x,1 if b[1]>a[1] else -1))
        crossings.sort()
        winding, index = 0, 0
        for x in range(SIZE):
            while index < len(crossings) and crossings[index][0] <= x+.5:
                winding += crossings[index][1]
                index += 1
            if winding:
                mask |= 1 << (y*SIZE+x)
    return mask


def iou(a,b):
    return (a&b).bit_count()/(a|b).bit_count() if a|b else 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    parser.add_argument('--research-cross-code', action='store_true', help='Explicitly opt into research outside the current user policy')
    args = parser.parse_args()
    if not args.research_cross_code:
        parser.error('Cross-code comparison is excluded from the current SOP; this tool requires explicit research opt-in')
    out = (ROOT/args.output).resolve()
    if ROOT/'audit/comparisons' not in out.parents:
        parser.error('Output must be under audit/comparisons')
    out.mkdir(parents=True,exist_ok=False)
    path = ROOT/'fonts/Nebulith-Regular.ttf'
    font = TTFont(path)
    gs, cmap = font.getGlyphSet(), font.getBestCmap()
    sources, reference = [], []
    for filename in REFERENCE_FILES:
        p = Path('C:/Windows/Fonts')/filename
        f = TTFont(p, fontNumber=0) if p.suffix == '.ttc' else TTFont(p)
        mapping, glyphs = f.getBestCmap(), f.getGlyphSet()
        supported = [c for c in REPERTOIRE if c in mapping]
        family = f['name'].getDebugName(1)
        sources.append({'file':str(p),'fontIndex':0,'family':family,'version':f['name'].getDebugName(5),
                        'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'comparedCodepoints':supported,'redistributed':False})
        for code in supported:
            reference.append({'codepoint':code,'char':chr(code),'family':family,'mask':silhouette(glyphs,mapping[code])})
    masks = {name:silhouette(gs,name) for name in font.getGlyphOrder()}
    groups = {'lower':[],'upper':[],'numbers':[],'symbols':[]}
    records=[]
    for name in font.getGlyphOrder():
        codes=[c for c,g in cmap.items() if g==name]
        char=chr(codes[0]) if codes else ''
        group='lower' if char.islower() else 'upper' if char.isupper() else 'numbers' if char.isdigit() else 'symbols'
        ranked=sorted(reference,key=lambda r:iou(masks[name],r['mask']),reverse=True)[:6] if masks[name] else []
        candidates=[{k:v for k,v in r.items() if k!='mask'}|{'iou':round(iou(masks[name],r['mask']),4)} for r in ranked]
        pen=SVGPathPen(gs);gs[name].draw(pen)
        target=f'<svg viewBox="0 -200 800 1100"><path transform="translate(0 700) scale(1 -1)" d="{pen.getCommands()}"/></svg>'
        refs=''.join(f'<span style="font-family:{html.escape(r["family"])}">{html.escape(r["char"])}<small>{html.escape(r["family"])} U+{r["codepoint"]:04X}<br>{r["iou"]:.3f}</small></span>' for r in candidates)
        groups[group].append(f'<article id="glyph-{name}"><h2>{name} {html.escape(char)}</h2><div class="pair"><div>{target}<small>Nebulith</small></div><div class="refs">{refs}</div></div></article>')
        internal=sorted(({'glyph':n,'iou':round(iou(masks[name],m),4)} for n,m in masks.items() if n!=name and m),key=lambda r:r['iou'],reverse=True)[:5] if masks[name] else []
        records.append({'glyph':name,'codepoints':codes,'externalCandidates':candidates,'internalCandidates':internal,
                        'outlineSha256':hashlib.sha256(pen.getCommands().encode()).hexdigest(),
                        'comparisonReference':out.relative_to(ROOT).as_posix()+f'/{group}.html#glyph-{name}'})
    style='<style>body{font:14px system-ui;color:#182532;background:white;margin:20px}.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}article{border:1px solid #ccd4da;padding:12px}h2{font-size:14px}.pair{display:grid;grid-template-columns:100px 1fr;gap:8px}svg{height:100px;width:100px;fill:currentColor}.refs{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}.refs span{font-size:38px;text-align:center}small{display:block;font:9px system-ui;color:#657383}p{line-height:1.6}</style>'
    for group,cards in groups.items():
        (out/(group+'.html')).write_text('<!doctype html><meta charset="utf-8">'+style+f'<h1>Nebulith {font["name"].getDebugName(5)} / {group}</h1><p>英数字・ギリシャ・キリル・アラビア・かな・選定漢字・記号。5書体の対応字のみ比較。48×48正規化輪郭IoUの上位候補。順位は類似・不適合の確定ではない。書体はローカル参照。</p><div class="grid">'+''.join(cards)+'</div>',encoding='utf-8')
    dump(out/'inventory.json',{'fontSha256':hashlib.sha256(path.read_bytes()).hexdigest(),'fontVersion':font['name'].getDebugName(5),
         'method':'48x48 aspect-preserving nonzero silhouettes; IoU ranks only; no skeleton or universal originality certification',
         'referenceFonts':sources,'referenceForms':len(reference),'glyphs':records})
    print(json.dumps({'glyphs':len(records),'referenceForms':len(reference),'output':str(out)}))


if __name__=='__main__':
    main()
