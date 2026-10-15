"""v2.4: revise A/a and S/s, comparing corresponding characters per user policy."""
from fontTools.pens.ttGlyphPen import TTGlyphPen

CHANGED_GLYPHS = {'a', 'A', 's', 'S'}


def revise_glyphs(glyphs, ring, node):
    def draw(p):
        # Asymmetric, gently leaning orbit with two tapered flowing tails.
        p.moveTo((245,440));p.qCurveTo((255,555),(385,540))
        p.qCurveTo((525,525),(500,370));p.qCurveTo((480,235),(350,250))
        p.qCurveTo((210,265),(245,440));p.closePath()
        p.moveTo((285,435));p.qCurveTo((255,300),(350,290))
        p.qCurveTo((445,275),(460,375));p.qCurveTo((480,485),(385,500))
        p.qCurveTo((290,510),(285,435));p.closePath()
        p.moveTo((265,465));p.qCurveTo((200,505),(130,550))
        p.lineTo((110,580));p.qCurveTo((195,550),(290,485));p.closePath()
        p.moveTo((270,300));p.qCurveTo((185,240),(115,235))
        p.lineTo((110,205));p.qCurveTo((195,200),(295,275));p.closePath()
        node(p,365,385,19)
    def draw_s(p):
        # Open upper brush sweep and closed lower droplet, without rigid polygons.
        p.moveTo((120,485));p.qCurveTo((190,625),(330,555))
        p.qCurveTo((410,510),(455,460));p.lineTo((425,435))
        p.qCurveTo((365,485),(315,515));p.qCurveTo((220,565),(160,465));p.closePath()
        p.moveTo((330,390));p.qCurveTo((530,405),(500,230))
        p.qCurveTo((470,120),(360,180));p.qCurveTo((245,245),(330,390));p.closePath()
        p.moveTo((355,345));p.qCurveTo((305,255),(375,215))
        p.qCurveTo((445,175),(462,240));p.qCurveTo((490,350),(355,345));p.closePath()
        node(p,145,478,15);node(p,440,448,15)
    for name in sorted(CHANGED_GLYPHS):
        p = TTGlyphPen(None)
        (draw_s if name.lower() == 's' else draw)(p)
        glyphs[name] = (p.glyph(), glyphs[name][1])
