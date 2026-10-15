"""v2.5: rebuild five critical forms, gently finish punctuation, retain spacing."""
from math import hypot
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates
from font_symbols import SYMBOLS

CRITICAL = {'i', 'I', 't', 'T', 'one'}
MINOR = {row[0] for row in SYMBOLS}
CHANGED_GLYPHS = CRITICAL | MINOR | {'.notdef'}


def soften(glyph, lean=0.025, radius=7):
    """Round line/line corners only; preserve existing quadratic curves/counters.

    A very small shear makes the pen flow less mechanical. Mirrored punctuation
    receives opposite shear; neutral punctuation uses a gentle forward lean.
    """
    coordinates, flags, ends = [], bytearray(), []
    start = 0
    for end in glyph.endPtsOfContours:
        pts = list(glyph.coordinates[start:end+1])
        fs = list(glyph.flags[start:end+1])
        for n, p in enumerate(pts):
            a,b = pts[n-1],pts[(n+1)%len(pts)]
            u,v = (a[0]-p[0],a[1]-p[1]),(b[0]-p[0],b[1]-p[1])
            lu,lv = hypot(*u),hypot(*v)
            if fs[n]&1 and fs[n-1]&1 and fs[(n+1)%len(pts)]&1 and lu and lv and u[0]*v[1]!=u[1]*v[0]:
                cut=min(radius,lu/4,lv/4)
                points=[((p[0]+u[0]*cut/lu,p[1]+u[1]*cut/lu),1),(p,0),
                        ((p[0]+v[0]*cut/lv,p[1]+v[1]*cut/lv),1)]
            else:
                points=[(p,fs[n]&1)]
            for point,flag in points:
                coordinates.append((round(point[0]+lean*(point[1]-355)),round(point[1])))
                flags.append(flag)
        ends.append(len(coordinates)-1)
        start=end+1
    glyph.coordinates=GlyphCoordinates(coordinates)
    glyph.flags=flags
    glyph.endPtsOfContours=ends
    glyph.numberOfContours=len(ends)


def revise_pending(glyphs,ring,node):
    def i(p):
        # Slanted tall counter and a rightward flowing foot, no dot over a stem.
        p.moveTo((330,650));p.qCurveTo((140,520),(200,300))
        p.qCurveTo((260,220),(340,380));p.qCurveTo((400,480),(330,650));p.closePath()
        p.moveTo((320,575));p.qCurveTo((350,470),(305,395))
        p.qCurveTo((255,295),(240,335));p.qCurveTo((200,480),(320,575));p.closePath()
        p.moveTo((215,320));p.qCurveTo((340,160),(495,230))
        p.lineTo((510,265));p.qCurveTo((355,205),(245,345));p.closePath()
    def t(p):
        # Two broad opposing sweeps joined at the side, not a cap on a stem.
        p.moveTo((145,495));p.qCurveTo((330,680),(510,500))
        p.lineTo((480,470));p.qCurveTo((330,615),(175,465));p.closePath()
        p.moveTo((180,250));p.qCurveTo((330,130),(480,300))
        p.lineTo((450,325));p.qCurveTo((330,195),(205,280));p.closePath()
        p.moveTo((165,480));p.qCurveTo((145,330),(205,265))
        p.lineTo((235,290));p.qCurveTo((185,350),(205,480));p.closePath()
        ring(p,225,375,48,25)
    def one(p):
        # High open brush sweep and lower counter; no straight numeral-one axis.
        p.moveTo((440,620));p.qCurveTo((190,570),(195,380))
        p.qCurveTo((195,320),(260,290));p.lineTo((280,325))
        p.qCurveTo((235,350),(235,390));p.qCurveTo((245,535),(450,580));p.closePath()
        p.moveTo((260,355));p.qCurveTo((425,410),(445,265))
        p.qCurveTo((440,145),(300,180));p.qCurveTo((190,225),(260,355));p.closePath()
        p.moveTo((285,315));p.qCurveTo((245,245),(310,220))
        p.qCurveTo((400,195),(405,270));p.qCurveTo((395,355),(285,315));p.closePath()
    drawers={'i':i,'t':t,'one':one}
    for name in sorted(CRITICAL):
        pen=TTGlyphPen(None);drawers[name.lower()](pen)
        glyphs[name]=(pen.glyph(),glyphs[name][1])
    for name in sorted(MINOR):
        glyph,width=glyphs[name]
        right=name.endswith('right')
        soften(glyph,lean=-0.025 if right else 0.025)
        glyphs[name]=(glyph,width)
    glyph,width=glyphs['.notdef']
    soften(glyph,lean=0,radius=10)
    glyphs['.notdef']=(glyph,width)
