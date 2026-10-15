"""Nebulith punctuation: celestial nuclei, open orbits and paired anchors.

ASCII and Japanese/fullwidth aliases share outlines, never rewrite source text.
The phonemic ASCII apostrophe is preserved separately from typographic quotes.
"""
from math import hypot

FONT_VERSION = '2.5'
SYMBOLS = [
    ('period', '.．。', '終止核', 400), ('comma', ',，、', '彗星の小休止', 400),
    ('colon', ':：', '連星の接続', 400), ('hyphen', '-－', '短い軌道橋', 500),
    ('quotesingle', "'", '声門キャリア（音素）', 360),
    ('question', '?？', '開いた探索軌道と中心核', 620),
    ('exclam', '!！', '放射する三角光芒と基底核', 500),
    ('semicolon', ';；', '上部連星環と流下する彗星尾', 440),
    ('ellipsis', '…⋯', '三つの終止核', 760),
    ('parenleft', '(（', '左の抱擁軌道', 440), ('parenright', ')）', '右の抱擁軌道', 440),
    ('bracketleft', '[［', '左の観測枠', 440), ('bracketright', ']］', '右の観測枠', 440),
    ('braceleft', '{｛', '左の双極境界', 480), ('braceright', '}｝', '右の双極境界', 480),
    ('quoteleft', '‘', '左の浮遊核', 340), ('quoteright', '’', '右の浮遊核', 340),
    ('quotedblleft', '“「『', '左の二重浮遊核', 520),
    ('quotedblright', '”」』', '右の二重浮遊核', 520),
    ('quotedbl', '"＂', '中立の二重引用核', 520),
    ('slash', '/／', '斜交する軌道橋', 560), ('plus', '+＋', '四方の連結核', 620),
    ('equal', '=＝', '平行する双軌道', 620), ('emdash', '—―', '長い連星架橋', 900),
    ('asterisk', '*＊', '六方の星印', 620), ('multiply', '×', '交差する二つの軌道', 620),
    ('divide', '÷', '上下の核と分離軌道', 620),
]


def add_symbols(add_glyph, char_map, ring, node):
    def line(pen, a, b, width=28):
        dx, dy = b[0]-a[0], b[1]-a[1]
        length = hypot(dx, dy)
        ox, oy = -dy/length*width/2, dx/length*width/2
        pen.moveTo((a[0]+ox, a[1]+oy))
        pen.lineTo((b[0]+ox, b[1]+oy))
        pen.lineTo((b[0]-ox, b[1]-oy))
        pen.lineTo((a[0]-ox, a[1]-oy))
        pen.closePath()

    def arc(pen, points, thickness=30):
        """Quadratic ribbon: points=(start, control, end), horizontal thickness."""
        a, c, b = points
        pen.moveTo(a)
        pen.qCurveTo(c, b)
        pen.lineTo((b[0]+thickness, b[1]))
        pen.qCurveTo((c[0]+thickness, c[1]), (a[0]+thickness, a[1]))
        pen.closePath()

    def question(p):
        # Open orbital sweep surrounding a separate star, with a low terminal ring.
        arc(p, [(160, 500), (210, 690), (440, 510)], 30)
        arc(p, [(440, 510), (500, 350), (260, 330)], 30)
        line(p, (260, 330), (260, 265))
        ring(p, 300, 445, 38, 20)
        ring(p, 260, 155, 34, 17)
        node(p, 160, 500, 20)

    def exclam(p):
        # Two converging rays leave an open triangular fan rather than a plain stem.
        line(p, (130, 620), (250, 295), 28)
        line(p, (370, 620), (250, 295), 28)
        ring(p, 250, 500, 35, 18)
        ring(p, 250, 155, 34, 17)
        node(p, 130, 620, 17)
        node(p, 370, 620, 17)

    def semicolon(p):
        ring(p, 220, 470, 38, 20)
        ring(p, 220, 230, 30, 15)
        arc(p, [(220, 215), (295, 120), (155, 65)], 25)

    def ellipsis(p):
        for x in [160, 380, 600]:
            ring(p, x, 180, 32, 16)
            node(p, x, 180, 8)

    def parenthesis(p, right=False):
        x = lambda v: 440-v if right else v
        arc(p, [(x(300), 650), (x(30), 355), (x(300), 60)], -30 if right else 30)
        node(p, x(300), 650, 18)
        node(p, x(300), 60, 18)
        ring(p, x(155), 355, 25, 12)

    def bracket(p, right=False):
        x = lambda v: 440-v if right else v
        for a, b in [((290, 640), (140, 640)), ((140, 640), (140, 80)), ((140, 80), (290, 80))]:
            line(p, (x(a[0]), a[1]), (x(b[0]), b[1]), 28)
        ring(p, x(140), 360, 32, 17)
        node(p, x(290), 640, 18)
        node(p, x(290), 80, 18)

    def brace(p, right=False):
        x = lambda v: 480-v if right else v
        arc(p, [(x(330), 650), (x(145), 650), (x(210), 430)], -28 if right else 28)
        arc(p, [(x(210), 430), (x(215), 360), (x(100), 355)], -28 if right else 28)
        arc(p, [(x(100), 355), (x(215), 350), (x(210), 280)], -28 if right else 28)
        arc(p, [(x(210), 280), (x(145), 60), (x(330), 60)], -28 if right else 28)
        ring(p, x(100), 355, 25, 12)

    def quote(p, right=False, double=False, neutral=False):
        for x in ([150, 350] if double else [170]):
            ring(p, x, 590, 35, 18)
            if not neutral:
                direction = 1 if right else -1
                line(p, (x, 570), (x+direction*55, 480), 24)
                node(p, x+direction*55, 480, 15)

    def slash(p):
        line(p, (145, 100), (415, 620), 30)
        ring(p, 280, 360, 32, 17)
        node(p, 145, 100, 18)
        node(p, 415, 620, 18)

    def plus(p):
        line(p, (120, 360), (500, 360))
        line(p, (310, 160), (310, 560))
        ring(p, 310, 360, 54, 32)
        for a in [(120, 360), (500, 360), (310, 160), (310, 560)]:
            node(p, *a, 16)

    def equal(p):
        for y in [270, 450]:
            line(p, (125, y), (495, y))
            ring(p, 125, y, 25, 12)
            ring(p, 495, y, 25, 12)

    def emdash(p):
        line(p, (100, 360), (800, 360), 25)
        ring(p, 450, 360, 42, 22)
        node(p, 100, 360, 18)
        node(p, 800, 360, 18)

    def asterisk(p):
        for a, b in [((310, 150), (310, 570)), ((130, 255), (490, 465)), ((130, 465), (490, 255))]:
            line(p, a, b, 25)
        ring(p, 310, 360, 45, 24)

    def multiply(p):
        line(p, (150, 200), (470, 520))
        line(p, (150, 520), (470, 200))
        ring(p, 310, 360, 45, 24)
        for a in [(150, 200), (470, 520), (150, 520), (470, 200)]:
            node(p, *a, 16)

    def divide(p):
        line(p, (125, 360), (495, 360))
        ring(p, 310, 180, 32, 16)
        ring(p, 310, 540, 32, 16)
        node(p, 125, 360, 16)
        node(p, 495, 360, 16)

    drawers = {'question': question, 'exclam': exclam, 'semicolon': semicolon, 'ellipsis': ellipsis,
               'parenleft': lambda p: parenthesis(p), 'parenright': lambda p: parenthesis(p, True),
               'bracketleft': lambda p: bracket(p), 'bracketright': lambda p: bracket(p, True),
               'braceleft': lambda p: brace(p), 'braceright': lambda p: brace(p, True),
               'quoteleft': lambda p: quote(p), 'quoteright': lambda p: quote(p, True),
               'quotedblleft': lambda p: quote(p, double=True), 'quotedblright': lambda p: quote(p, True, True),
               'quotedbl': lambda p: quote(p, double=True, neutral=True), 'slash': slash,
               'plus': plus, 'equal': equal, 'emdash': emdash, 'asterisk': asterisk,
               'multiply': multiply, 'divide': divide}
    for name, chars, _, width in SYMBOLS:
        if name in drawers:
            add_glyph(name, ord(chars[0]), width, drawers[name])
        for char in chars:
            if ord(char) in char_map and char_map[ord(char)] != name:
                raise ValueError(f'Duplicate mapping: {char}')
            char_map[ord(char)] = name
