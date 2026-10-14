"""
Nebulith-Regular.ttf Font Generator
Generates an authentic TrueType font file for the Nebulith conlang script.
Features smooth rounded curves, loops, and celestial star nodes.
"""

import os
from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables._c_m_a_p import cmap_format_4
from fontTools.pens.ttGlyphPen import TTGlyphPen

def make_circle(pen, cx, cy, r):
    """Draw a smooth 2nd-order bezier circle (8-point approximation)."""
    k = r * 1.0  # control point extension
    pen.moveTo((cx + r, cy))
    pen.qCurveTo((cx + r, cy + k), (cx, cy + r))
    pen.qCurveTo((cx - k, cy + r), (cx - r, cy))
    pen.qCurveTo((cx - r, cy - k), (cx, cy - r))
    pen.qCurveTo((cx + k, cy - r), (cx + r, cy))
    pen.closePath()

def make_ring(pen, cx, cy, r_out, r_in):
    """Draw a ring (donut shape) with correct winding."""
    make_circle(pen, cx, cy, r_out)
    # inner circle counter-clockwise for hole
    k = r_in * 1.0
    pen.moveTo((cx + r_in, cy))
    pen.qCurveTo((cx + k, cy - r_in), (cx, cy - r_in))
    pen.qCurveTo((cx - r_in, cy - k), (cx - r_in, cy))
    pen.qCurveTo((cx - k, cy + r_in), (cx, cy + r_in))
    pen.qCurveTo((cx + r_in, cy + k), (cx + r_in, cy))
    pen.closePath()

def draw_star_node(pen, cx, cy, r=22):
    """Draw a distinct star node dot."""
    make_circle(pen, cx, cy, r)

def build_font():
    units_per_em = 1000
    ascender = 800
    descender = -200
    default_width = 650
    
    glyphs = {}
    glyph_order = []
    char_map = {}

    def add_glyph(name, char_code=None, width=default_width, draw_func=None):
        glyph_order.append(name)
        if char_code:
            char_map[char_code] = name
        pen = TTGlyphPen(None)
        if draw_func:
            draw_func(pen)
        glyphs[name] = (pen.glyph(), width)

    # 1. .notdef
    def draw_notdef(pen):
        pen.moveTo((100, 0))
        pen.lineTo((100, 700))
        pen.lineTo((550, 700))
        pen.lineTo((550, 0))
        pen.closePath()
        pen.moveTo((150, 50))
        pen.lineTo((500, 50))
        pen.lineTo((500, 650))
        pen.lineTo((150, 650))
        pen.closePath()
    add_glyph(".notdef", None, 650, draw_notdef)

    # 2. space
    add_glyph("space", 32, 320, lambda pen: None)

    # ==========================================
    # 6 VOWELS: a, e, i, o, u, y
    # ==========================================
    
    # 'a' : Dawn Arch (上向き円弧 ＋ 天頂星核)
    def draw_a(pen):
        pen.moveTo((120, 360))
        pen.qCurveTo((120, 180), (325, 180))
        pen.qCurveTo((530, 180), (530, 360))
        pen.lineTo((480, 360))
        pen.qCurveTo((480, 230), (325, 230))
        pen.qCurveTo((170, 230), (170, 360))
        pen.closePath()
        draw_star_node(pen, 325, 470, 26)
        draw_star_node(pen, 120, 360, 16)
        draw_star_node(pen, 530, 360, 16)
    add_glyph("a", ord("a"), 650, draw_a)
    add_glyph("A", ord("A"), 750, draw_a)

    # 'e' : Solar Wind Wave (たなびく波線 ＋ 双子星)
    def draw_e(pen):
        pen.moveTo((140, 220))
        pen.qCurveTo((200, 420), (340, 420))
        pen.qCurveTo((480, 420), (510, 220))
        pen.lineTo((460, 200))
        pen.qCurveTo((430, 370), (340, 370))
        pen.qCurveTo((230, 370), (190, 200))
        pen.closePath()
        draw_star_node(pen, 140, 220, 20)
        draw_star_node(pen, 510, 220, 20)
        draw_star_node(pen, 340, 460, 18)
    add_glyph("e", ord("e"), 650, draw_e)
    add_glyph("E", ord("E"), 750, draw_e)

    # 'i' : North Star Spire (天へ伸びる縦流線 ＋ 頂星)
    def draw_i(pen):
        pen.moveTo((290, 180))
        pen.qCurveTo((310, 350), (320, 560))
        pen.lineTo((360, 560))
        pen.qCurveTo((350, 350), (330, 180))
        pen.closePath()
        draw_star_node(pen, 340, 670, 28)
        draw_star_node(pen, 310, 180, 18)
    add_glyph("i", ord("i"), 550, draw_i)
    add_glyph("I", ord("I"), 650, draw_i)

    # 'o' : Full Moon Orbit (完全円環 ＋ 巡行星)
    def draw_o(pen):
        make_ring(pen, 340, 340, 170, 125)
        draw_star_node(pen, 340, 550, 22)
    add_glyph("o", ord("o"), 680, draw_o)
    add_glyph("O", ord("O"), 780, draw_o)

    # 'u' : Deep Abyss Bowl (深き器の円弧 ＋ 底星)
    def draw_u(pen):
        pen.moveTo((150, 480))
        pen.qCurveTo((150, 180), (330, 180))
        pen.qCurveTo((510, 180), (510, 480))
        pen.lineTo((465, 480))
        pen.qCurveTo((465, 225), (330, 225))
        pen.qCurveTo((195, 225), (195, 480))
        pen.closePath()
        draw_star_node(pen, 330, 110, 24)
        draw_star_node(pen, 150, 480, 18)
        draw_star_node(pen, 510, 480, 18)
    add_glyph("u", ord("u"), 660, draw_u)
    add_glyph("U", ord("U"), 760, draw_u)

    # 'y' : 6th Astral Vowel [y] (二重円弧ループ ＋ 屈折核)
    def draw_y(pen):
        pen.moveTo((160, 460))
        pen.qCurveTo((160, 260), (330, 260))
        pen.qCurveTo((500, 260), (500, 460))
        pen.lineTo((455, 460))
        pen.qCurveTo((455, 305), (330, 305))
        pen.qCurveTo((205, 305), (205, 460))
        pen.closePath()
        pen.moveTo((330, 260))
        pen.qCurveTo((330, 0), (240, -100))
        pen.qCurveTo((170, -120), (190, -40))
        pen.qCurveTo((210, -20), (285, 30))
        pen.qCurveTo((310, 100), (310, 260))
        pen.closePath()
        draw_star_node(pen, 180, -70, 20)
    add_glyph("y", ord("y"), 660, draw_y)
    add_glyph("Y", ord("Y"), 760, draw_y)

    # ==========================================
    # 16 CONSONANTS + 1 CARRIER
    # ==========================================

    # 'l' : High Oval Loop (天高く伸びるオーバルループ)
    def draw_l(pen):
        pen.moveTo((260, 180))
        pen.lineTo((260, 680))
        pen.qCurveTo((260, 780), (350, 780))
        pen.qCurveTo((440, 780), (440, 680))
        pen.qCurveTo((440, 480), (260, 360))
        pen.lineTo((300, 180))
        pen.closePath()
        draw_star_node(pen, 350, 780, 24)
        draw_star_node(pen, 500, 200, 20)
    add_glyph("l", ord("l"), 600, draw_l)
    add_glyph("L", ord("L"), 700, draw_l)

    # 'r' : Orbit Arc (公転ループ ＋ 右下への流線)
    def draw_r(pen):
        pen.moveTo((220, 180))
        pen.lineTo((220, 520))
        pen.qCurveTo((220, 580), (360, 580))
        pen.qCurveTo((480, 580), (480, 440))
        pen.qCurveTo((480, 320), (330, 320))
        pen.lineTo((260, 320))
        pen.lineTo((260, 180))
        pen.closePath()
        pen.moveTo((330, 320))
        pen.qCurveTo((430, 260), (490, 180))
        pen.lineTo((540, 190))
        pen.qCurveTo((460, 290), (340, 360))
        pen.closePath()
        draw_star_node(pen, 480, 440, 20)
        draw_star_node(pen, 520, 180, 20)
    add_glyph("r", ord("r"), 640, draw_r)
    add_glyph("R", ord("R"), 740, draw_r)

    # 'm' : Twin Mountains Arch (二重の丸い山型アーチ)
    def draw_m(pen):
        pen.moveTo((120, 180))
        pen.lineTo((120, 420))
        pen.qCurveTo((120, 520), (260, 520))
        pen.qCurveTo((380, 520), (380, 420))
        pen.lineTo((380, 180))
        pen.lineTo((340, 180))
        pen.lineTo((340, 420))
        pen.qCurveTo((340, 480), (260, 480))
        pen.qCurveTo((160, 480), (160, 420))
        pen.lineTo((160, 180))
        pen.closePath()
        pen.moveTo((340, 420))
        pen.qCurveTo((340, 520), (480, 520))
        pen.qCurveTo((600, 520), (600, 420))
        pen.lineTo((600, 180))
        pen.lineTo((560, 180))
        pen.lineTo((560, 420))
        pen.qCurveTo((560, 480), (480, 480))
        pen.qCurveTo((380, 480), (380, 420))
        pen.closePath()
        draw_star_node(pen, 260, 520, 18)
        draw_star_node(pen, 480, 520, 18)
    add_glyph("m", ord("m"), 720, draw_m)
    add_glyph("M", ord("M"), 820, draw_m)

    # 'n' : Single Arch (単一の丸い山型アーチ)
    def draw_n(pen):
        pen.moveTo((180, 180))
        pen.lineTo((180, 420))
        pen.qCurveTo((180, 540), (340, 540))
        pen.qCurveTo((500, 540), (500, 420))
        pen.lineTo((500, 180))
        pen.lineTo((455, 180))
        pen.lineTo((455, 420))
        pen.qCurveTo((455, 495), (340, 495))
        pen.qCurveTo((225, 495), (225, 420))
        pen.lineTo((225, 180))
        pen.closePath()
        draw_star_node(pen, 340, 540, 22)
    add_glyph("n", ord("n"), 660, draw_n)
    add_glyph("N", ord("N"), 760, draw_n)

    # 's' : Double S-Curve Nebula (流麗な二重S字曲線)
    def draw_s(pen):
        pen.moveTo((450, 480))
        pen.qCurveTo((250, 550), (220, 420))
        pen.qCurveTo((200, 320), (340, 320))
        pen.qCurveTo((470, 320), (440, 200))
        pen.qCurveTo((420, 140), (230, 180))
        pen.lineTo((210, 150))
        pen.qCurveTo((450, 80), (480, 210))
        pen.qCurveTo((510, 360), (340, 360))
        pen.qCurveTo((240, 360), (260, 430))
        pen.qCurveTo((280, 490), (470, 440))
        pen.closePath()
        draw_star_node(pen, 340, 340, 20)
    add_glyph("s", ord("s"), 660, draw_s)
    add_glyph("S", ord("S"), 760, draw_s)

    # 'z' : Resonant S (中央に連星ノードを持つ有声S)
    def draw_z(pen):
        draw_s(pen)
        draw_star_node(pen, 200, 200, 16)
        draw_star_node(pen, 480, 480, 16)
    add_glyph("z", ord("z"), 660, draw_z)
    add_glyph("Z", ord("Z"), 760, draw_z)

    # 'c' : Quiet Sh-Sound [ʃ] (三日月フック曲線)
    def draw_c(pen):
        pen.moveTo((480, 480))
        pen.qCurveTo((180, 500), (180, 340))
        pen.qCurveTo((180, 180), (480, 200))
        pen.lineTo((450, 240))
        pen.qCurveTo((230, 230), (230, 340))
        pen.qCurveTo((230, 450), (450, 440))
        pen.closePath()
        draw_star_node(pen, 480, 480, 20)
    add_glyph("c", ord("c"), 640, draw_c)
    add_glyph("C", ord("C"), 740, draw_c)

    # 'j' : Voiced Zh-Sound [ʒ] (下へ潜るディセンダーループ)
    def draw_j(pen):
        pen.moveTo((380, 500))
        pen.lineTo((380, -60))
        pen.qCurveTo((380, -180), (260, -180))
        pen.qCurveTo((160, -180), (180, -80))
        pen.lineTo((225, -70))
        pen.qCurveTo((210, -135), (260, -135))
        pen.qCurveTo((335, -135), (335, -50))
        pen.lineTo((335, 500))
        pen.closePath()
        draw_star_node(pen, 360, 620, 24)
        draw_star_node(pen, 190, -75, 18)
    add_glyph("j", ord("j"), 560, draw_j)
    add_glyph("J", ord("J"), 660, draw_j)

    # 'f' : Ascending Breath (軽やかな立ち上がりフック)
    def draw_f(pen):
        pen.moveTo((260, 180))
        pen.lineTo((260, 620))
        pen.qCurveTo((260, 740), (420, 740))
        pen.lineTo((420, 695))
        pen.qCurveTo((305, 695), (305, 610))
        pen.lineTo((305, 420))
        pen.lineTo((440, 420))
        pen.lineTo((440, 380))
        pen.lineTo((305, 380))
        pen.lineTo((305, 180))
        pen.closePath()
        draw_star_node(pen, 420, 740, 20)
    add_glyph("f", ord("f"), 560, draw_f)
    add_glyph("F", ord("F"), 660, draw_f)

    # 'v' : Wave Valley (丸い谷底を通る流線)
    def draw_v(pen):
        pen.moveTo((160, 480))
        pen.qCurveTo((220, 220), (330, 200))
        pen.qCurveTo((440, 220), (500, 480))
        pen.lineTo((455, 480))
        pen.qCurveTo((410, 260), (330, 245))
        pen.qCurveTo((250, 260), (205, 480))
        pen.closePath()
        draw_star_node(pen, 330, 200, 22)
    add_glyph("v", ord("v"), 650, draw_v)
    add_glyph("V", ord("V"), 750, draw_v)

    # 'h' : Open Sky (二本の柔らかな平行弧線)
    def draw_h(pen):
        pen.moveTo((220, 180))
        pen.lineTo((220, 720))
        pen.lineTo((265, 720))
        pen.lineTo((265, 460))
        pen.qCurveTo((265, 520), (380, 520))
        pen.qCurveTo((480, 520), (480, 420))
        pen.lineTo((480, 180))
        pen.lineTo((435, 180))
        pen.lineTo((435, 410))
        pen.qCurveTo((435, 475), (370, 475))
        pen.qCurveTo((265, 475), (265, 400))
        pen.lineTo((265, 180))
        pen.closePath()
        draw_star_node(pen, 240, 720, 20)
    add_glyph("h", ord("h"), 640, draw_h)
    add_glyph("H", ord("H"), 740, draw_h)

    # 'w' : Twilight Waves (下に広がる二連の谷線)
    def draw_w(pen):
        pen.moveTo((120, 460))
        pen.qCurveTo((180, 200), (260, 200))
        pen.qCurveTo((330, 200), (360, 380))
        pen.qCurveTo((400, 200), (480, 200))
        pen.qCurveTo((540, 200), (600, 460))
        pen.lineTo((560, 460))
        pen.qCurveTo((510, 240), (480, 240))
        pen.qCurveTo((420, 240), (380, 440))
        pen.lineTo((340, 440))
        pen.qCurveTo((300, 240), (260, 240))
        pen.qCurveTo((210, 240), (160, 460))
        pen.closePath()
        draw_star_node(pen, 260, 200, 18)
        draw_star_node(pen, 480, 200, 18)
    add_glyph("w", ord("w"), 720, draw_w)
    add_glyph("W", ord("W"), 820, draw_w)

    # 'p' : Ascending Loop (上部ループ ＋ ディセンダーステム)
    def draw_p(pen):
        pen.moveTo((220, -120))
        pen.lineTo((220, 480))
        pen.lineTo((265, 480))
        pen.qCurveTo((450, 480), (450, 330))
        pen.qCurveTo((450, 180), (265, 180))
        pen.lineTo((265, -120))
        pen.closePath()
        pen.moveTo((265, 225))
        pen.qCurveTo((400, 225), (400, 330))
        pen.qCurveTo((400, 435), (265, 435))
        pen.closePath()
        draw_star_node(pen, 450, 330, 20)
    add_glyph("p", ord("p"), 640, draw_p)
    add_glyph("P", ord("P"), 740, draw_p)

    # 'b' : Embracing Double Bowl (上下二連ループ)
    def draw_b(pen):
        pen.moveTo((220, 180))
        pen.lineTo((220, 720))
        pen.lineTo((265, 720))
        pen.lineTo((265, 480))
        pen.qCurveTo((450, 480), (450, 330))
        pen.qCurveTo((450, 180), (265, 180))
        pen.closePath()
        pen.moveTo((265, 225))
        pen.qCurveTo((400, 225), (400, 330))
        pen.qCurveTo((400, 435), (265, 435))
        pen.closePath()
        draw_star_node(pen, 240, 720, 20)
        draw_star_node(pen, 450, 330, 20)
    add_glyph("b", ord("b"), 640, draw_b)
    add_glyph("B", ord("B"), 740, draw_b)

    # 't' : Celestial Canopy (柔らかな水平天蓋 ＋ 下垂線)
    def draw_t(pen):
        pen.moveTo((150, 680))
        pen.qCurveTo((330, 720), (510, 680))
        pen.lineTo((500, 640))
        pen.qCurveTo((330, 675), (160, 640))
        pen.closePath()
        pen.moveTo((310, 180))
        pen.lineTo((310, 690))
        pen.lineTo((350, 690))
        pen.lineTo((350, 180))
        pen.closePath()
        draw_star_node(pen, 330, 720, 22)
        draw_star_node(pen, 330, 180, 18)
    add_glyph("t", ord("t"), 640, draw_t)
    add_glyph("T", ord("T"), 740, draw_t)

    # 'd' : Stable Earth (t の下に丸いボウル)
    def draw_d(pen):
        pen.moveTo((380, 180))
        pen.lineTo((380, 720))
        pen.lineTo((425, 720))
        pen.lineTo((425, 460))
        pen.qCurveTo((200, 460), (200, 320))
        pen.qCurveTo((200, 180), (380, 180))
        pen.closePath()
        pen.moveTo((380, 225))
        pen.qCurveTo((245, 225), (245, 320))
        pen.qCurveTo((245, 415), (380, 415))
        pen.closePath()
        draw_star_node(pen, 400, 720, 20)
    add_glyph("d", ord("d"), 640, draw_d)
    add_glyph("D", ord("D"), 740, draw_d)

    # 'k' : Radiant Rays (垂直軸 ＋ 放たれる光芒円弧)
    def draw_k(pen):
        pen.moveTo((220, 180))
        pen.lineTo((220, 720))
        pen.lineTo((265, 720))
        pen.lineTo((265, 180))
        pen.closePath()
        pen.moveTo((265, 380))
        pen.qCurveTo((380, 440), (480, 560))
        pen.lineTo((515, 530))
        pen.qCurveTo((400, 400), (265, 330))
        pen.closePath()
        pen.moveTo((265, 350))
        pen.qCurveTo((380, 280), (490, 180))
        pen.lineTo((525, 210))
        pen.qCurveTo((400, 310), (265, 390))
        pen.closePath()
        draw_star_node(pen, 495, 545, 20)
        draw_star_node(pen, 505, 195, 20)
    add_glyph("k", ord("k"), 640, draw_k)
    add_glyph("K", ord("K"), 740, draw_k)

    # 'g' : Gravity Ring (k の交点に重力環)
    def draw_g(pen):
        draw_k(pen)
        make_ring(pen, 340, 360, 75, 45)
    add_glyph("g", ord("g"), 640, draw_g)
    add_glyph("G", ord("G"), 740, draw_g)

    # ''' : Aether Carrier (原初軸・最小流線)
    def draw_apostrophe(pen):
        pen.moveTo((220, 520))
        pen.qCurveTo((240, 620), (250, 720))
        pen.lineTo((275, 720))
        pen.qCurveTo((265, 620), (245, 520))
        pen.closePath()
        draw_star_node(pen, 260, 730, 16)
    add_glyph("quotesingle", 39, 360, draw_apostrophe)

    # ==========================================
    # NUMERALS 0 - 9
    # ==========================================

    # '0' : Void Orbit (空の円環)
    def draw_num_0(pen):
        make_ring(pen, 330, 400, 180, 130)
    add_glyph("zero", ord("0"), 660, draw_num_0)

    # '1' : Solitary Star (縦流線 ＋ 単星)
    def draw_num_1(pen):
        pen.moveTo((300, 200))
        pen.lineTo((300, 650))
        pen.lineTo((345, 650))
        pen.lineTo((345, 200))
        pen.closePath()
        draw_star_node(pen, 320, 720, 28)
    add_glyph("one", ord("1"), 560, draw_num_1)

    # '2' : Binary Crescent (連星三日月)
    def draw_num_2(pen):
        pen.moveTo((420, 600))
        pen.qCurveTo((200, 600), (200, 400))
        pen.qCurveTo((200, 250), (450, 200))
        pen.lineTo((450, 245))
        pen.qCurveTo((250, 290), (250, 400))
        pen.qCurveTo((250, 555), (420, 555))
        pen.closePath()
        draw_star_node(pen, 420, 600, 20)
        draw_star_node(pen, 450, 200, 20)
    add_glyph("two", ord("2"), 650, draw_num_2)

    # '3' : Triple Orbit (三つ葉軌道)
    def draw_num_3(pen):
        make_circle(pen, 230, 300, 45)
        make_circle(pen, 430, 300, 45)
        make_circle(pen, 330, 500, 45)
        pen.moveTo((230, 300))
        pen.lineTo((430, 300))
        pen.lineTo((330, 500))
        pen.closePath()
    add_glyph("three", ord("3"), 660, draw_num_3)

    # '4' : Planetary Ring (土星環)
    def draw_num_4(pen):
        make_circle(pen, 330, 400, 90)
        pen.moveTo((150, 330))
        pen.qCurveTo((330, 520), (510, 470))
        pen.lineTo((510, 440))
        pen.qCurveTo((330, 490), (150, 300))
        pen.closePath()
    add_glyph("four", ord("4"), 660, draw_num_4)

    # '5' : Pentagram Curve (五芒流線)
    def draw_num_5(pen):
        pen.moveTo((180, 580))
        pen.lineTo((480, 580))
        pen.lineTo((280, 220))
        pen.lineTo((330, 640))
        pen.lineTo((450, 260))
        pen.closePath()
    add_glyph("five", ord("5"), 660, draw_num_5)

    # '6' : Comet Tail (彗星)
    def draw_num_6(pen):
        make_circle(pen, 260, 480, 70)
        pen.moveTo((310, 480))
        pen.qCurveTo((450, 360), (520, 200))
        pen.lineTo((480, 190))
        pen.qCurveTo((410, 330), (280, 430))
        pen.closePath()
    add_glyph("six", ord("6"), 660, draw_num_6)

    # '7' : Septet Canopy Arc (七星天蓋弧・天球弓と星列柱)
    # 脱・アラビア数字7：直角や斜め棒を完全排除し、天球を覆う天蓋アーチと中央の星流柱、星ノード列で構成
    def draw_num_7(pen):
        # 1. 天蓋ドームアーチ (Canopy Arch)
        pen.moveTo((160, 440))
        pen.qCurveTo((160, 620), (330, 620))
        pen.qCurveTo((500, 620), (500, 440))
        pen.lineTo((460, 440))
        pen.qCurveTo((460, 575), (330, 575))
        pen.qCurveTo((200, 575), (200, 440))
        pen.closePath()

        # 2. 中央の優雅な星流柱 (Starlight Pillar / Flow)
        pen.moveTo((310, 580))
        pen.qCurveTo((380, 390), (300, 200))
        pen.lineTo((345, 200))
        pen.qCurveTo((420, 390), (350, 580))
        pen.closePath()

        # 3. 昴・星列ノード群 (Pleiades Star Nodes)
        draw_star_node(pen, 330, 680, 24)  # 天頂主星
        draw_star_node(pen, 160, 440, 18)  # 左翼星
        draw_star_node(pen, 500, 440, 18)  # 右翼星
        draw_star_node(pen, 300, 180, 20)  # 基底星
        draw_star_node(pen, 385, 340, 15)  # 伴星1
        draw_star_node(pen, 275, 420, 13)  # 伴星2
    add_glyph("seven", ord("7"), 660, draw_num_7)

    # '8' : Bipolar Horizon (双極連星環・対向三日月と共鳴核)
    # 脱・アラビア数字8：上下丸2つの雪だるま型を完全排除し、中央連星核と左右に対向する三日月翼で構成
    def draw_num_8(pen):
        # 1. 中央連星共鳴核 (Central Resonant Core)
        make_ring(pen, 330, 400, 75, 38)

        # 2. 左翼三日月アーク (Left Wing Crescent)
        pen.moveTo((160, 580))
        pen.qCurveTo((265, 400), (160, 220))
        pen.lineTo((198, 220))
        pen.qCurveTo((298, 400), (198, 580))
        pen.closePath()

        # 3. 右翼三日月アーク (Right Wing Crescent)
        pen.moveTo((500, 580))
        pen.qCurveTo((395, 400), (500, 220))
        pen.lineTo((462, 220))
        pen.qCurveTo((362, 400), (462, 580))
        pen.closePath()

        # 4. 双極連星ノード (Polar Star Nodes)
        draw_star_node(pen, 160, 580, 18)  # 左上
        draw_star_node(pen, 160, 220, 18)  # 左下
        draw_star_node(pen, 500, 580, 18)  # 右上
        draw_star_node(pen, 500, 220, 18)  # 右下
        draw_star_node(pen, 330, 560, 18)  # 天頂連星
        draw_star_node(pen, 330, 240, 18)  # 天底連星
    add_glyph("eight", ord("8"), 660, draw_num_8)
    # '9' : Spiral Galaxy (銀河渦)
    def draw_num_9(pen):
        make_circle(pen, 330, 400, 50)
        pen.moveTo((330, 450))
        pen.qCurveTo((460, 450), (460, 320))
        pen.qCurveTo((460, 180), (300, 180))
        pen.qCurveTo((160, 180), (160, 360))
        pen.lineTo((195, 360))
        pen.qCurveTo((195, 215), (300, 215))
        pen.qCurveTo((425, 215), (425, 320))
        pen.qCurveTo((425, 415), (330, 415))
        pen.closePath()
    add_glyph("nine", ord("9"), 660, draw_num_9)

    # ==========================================
    # PUNCTUATION
    # ==========================================
    add_glyph("period", ord("."), 380, lambda pen: draw_star_node(pen, 190, 240, 24))
    def draw_comma(pen):
        make_circle(pen, 190, 250, 20)
        pen.moveTo((190, 250))
        pen.qCurveTo((170, 180), (140, 130))
        pen.lineTo((160, 125))
        pen.qCurveTo((195, 175), (210, 240))
        pen.closePath()
    add_glyph("comma", ord(","), 380, draw_comma)
    def draw_colon(pen):
        draw_star_node(pen, 190, 440, 18)
        draw_star_node(pen, 190, 240, 18)
    add_glyph("colon", ord(":"), 380, draw_colon)

    # ==========================================
    # ASSEMBLE TRUETYPE FONT TABLES
    # ==========================================
    font = TTFont()
    
    # 1. 'glyf' & 'loca'
    glyf_table = newTable("glyf")
    glyf_table.glyphs = {name: g[0] for name, g in glyphs.items()}
    font["glyf"] = glyf_table

    loca_table = newTable("loca")
    font["loca"] = loca_table

    # 2. 'head'
    head_table = newTable("head")
    head_table.tableVersion = 1.0
    head_table.fontRevision = 1.0
    head_table.checkSumAdjustment = 0
    head_table.magicNumber = 0x5F0F3CF5
    head_table.flags = 0x0003
    head_table.unitsPerEm = units_per_em
    head_table.created = 0
    head_table.modified = 0
    head_table.xMin = 0
    head_table.yMin = descender
    head_table.xMax = 800
    head_table.yMax = ascender
    head_table.macStyle = 0
    head_table.lowestRecPPEM = 8
    head_table.fontDirectionHint = 2
    head_table.indexToLocFormat = 0
    head_table.glyphDataFormat = 0
    font["head"] = head_table

    # 3. 'hhea'
    hhea_table = newTable("hhea")
    hhea_table.tableVersion = 0x00010000
    hhea_table.ascent = ascender
    hhea_table.descent = descender
    hhea_table.lineGap = 100
    hhea_table.advanceWidthMax = 850
    hhea_table.minLeftSideBearing = 0
    hhea_table.minRightSideBearing = 0
    hhea_table.xMaxExtent = 800
    hhea_table.caretSlopeRise = 1
    hhea_table.caretSlopeRun = 0
    hhea_table.caretOffset = 0
    hhea_table.reserved0 = 0
    hhea_table.reserved1 = 0
    hhea_table.reserved2 = 0
    hhea_table.reserved3 = 0
    hhea_table.metricDataFormat = 0
    hhea_table.numberOfHMetrics = len(glyph_order)
    font["hhea"] = hhea_table

    # 4. 'maxp'
    maxp_table = newTable("maxp")
    maxp_table.tableVersion = 0x00010000
    maxp_table.numGlyphs = len(glyph_order)
    maxp_table.maxPoints = 200
    maxp_table.maxContours = 20
    maxp_table.maxCompositePoints = 0
    maxp_table.maxCompositeContours = 0
    maxp_table.maxZones = 2
    maxp_table.maxTwilightPoints = 0
    maxp_table.maxStorage = 0
    maxp_table.maxFunctionDefs = 0
    maxp_table.maxInstructionDefs = 0
    maxp_table.maxStackElements = 0
    maxp_table.maxSizeOfInstructions = 0
    maxp_table.maxComponentElements = 0
    maxp_table.maxComponentDepth = 0
    font["maxp"] = maxp_table

    # 5. 'hmtx'
    hmtx_table = newTable("hmtx")
    hmtx_table.metrics = {name: (g[1], 30) for name, g in glyphs.items()}
    font["hmtx"] = hmtx_table

    # 6. 'cmap'
    cmap_table = newTable("cmap")
    cmap_table.tableVersion = 0
    subtable = cmap_format_4(4)
    subtable.platformID = 3
    subtable.platEncID = 1
    subtable.language = 0
    subtable.cmap = char_map
    cmap_table.tables = [subtable]
    font["cmap"] = cmap_table

    # 7. 'name'
    name_table = newTable("name")
    names = [
        (1, "Nebulith"),
        (2, "Regular"),
        (3, "Nebulith-Regular-v1.0"),
        (4, "Nebulith Regular"),
        (5, "Version 1.0"),
        (6, "Nebulith-Regular"),
        (9, "Reiun / DeepMind"),
    ]
    for name_id, text in names:
        name_table.setName(text, name_id, platformID=3, platEncID=1, langID=0x409)
        name_table.setName(text, name_id, platformID=1, platEncID=0, langID=0)
    font["name"] = name_table

    # 8. 'OS/2'
    os2_table = newTable("OS/2")
    os2_table.version = 4
    os2_table.xAvgCharWidth = 650
    os2_table.usWeightClass = 400
    os2_table.usWidthClass = 5
    os2_table.fsType = 0
    os2_table.ySubscriptXSize = 650
    os2_table.ySubscriptYSize = 600
    os2_table.ySubscriptXOffset = 0
    os2_table.ySubscriptYOffset = 75
    os2_table.ySuperscriptXSize = 650
    os2_table.ySuperscriptYSize = 600
    os2_table.ySuperscriptXOffset = 0
    os2_table.ySuperscriptYOffset = 350
    os2_table.yStrikeoutSize = 50
    os2_table.yStrikeoutPosition = 300
    os2_table.sFamilyClass = 0
    from fontTools.ttLib.tables.O_S_2f_2 import Panose; os2_table.panose = Panose()
    os2_table.ulUnicodeRange1 = 0x00000001
    os2_table.ulUnicodeRange2 = 0
    os2_table.ulUnicodeRange3 = 0
    os2_table.ulUnicodeRange4 = 0
    os2_table.achVendID = b"NEBU"
    os2_table.fsSelection = 0x0040
    os2_table.fsFirstCharIndex = 32
    os2_table.fsLastCharIndex = 126
    os2_table.sTypoAscender = ascender
    os2_table.sTypoDescender = descender
    os2_table.sTypoLineGap = 100
    os2_table.usWinAscent = ascender
    os2_table.usWinDescent = abs(descender)
    os2_table.ulCodePageRange1 = 0x00000001
    os2_table.ulCodePageRange2 = 0
    os2_table.sxHeight = 450
    os2_table.sCapHeight = 700
    os2_table.usDefaultChar = 0
    os2_table.usBreakChar = 32
    os2_table.usMaxContext = 0
    font["OS/2"] = os2_table

    # 9. 'post'
    post_table = newTable("post")
    post_table.formatType = 2.0
    post_table.italicAngle = 0.0
    post_table.underlinePosition = -100
    post_table.underlineThickness = 50
    post_table.isFixedPitch = 0
    post_table.minMemType42 = 0
    post_table.maxMemType42 = 0
    post_table.minMemType1 = 0
    post_table.maxMemType1 = 0
    post_table.extraNames = []
    post_table.mapping = {}
    post_table.glyphOrder = glyph_order
    font["post"] = post_table

    # Set Glyph Order
    font.setGlyphOrder(glyph_order)

    # Save to disk
    out_dir = r"C:\Users\danun\Desktop\Project\Nebulith\fonts"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "Nebulith-Regular.ttf")
    font.save(out_path)
    print(f"Successfully generated Nebulith TrueType font: {out_path}")
    print(f"Total glyphs: {len(glyph_order)}, mapped characters: {len(char_map)}")

if __name__ == "__main__":
    build_font()
