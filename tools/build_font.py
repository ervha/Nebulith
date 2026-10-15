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

    # =========================================================================
    # 16 PRIMARY CONSONANTS (Completely De-Latinized Celestial Graphemes)
    # =========================================================================

    # 1. 'l' : Zenith Spire & Slingshot Ring (天頂スピンドル ＋ 軌道スリングショット環)
    # 脱・ラテンl（直線の縦棒・筆記体を排除：天頂から直下して下部で環を描き右へ反転脱出）
    def draw_l(pen):
        pen.moveTo((310, 720))
        pen.lineTo((350, 720))
        pen.lineTo((350, 380))
        pen.lineTo((310, 380))
        pen.closePath()
        make_ring(pen, 330, 270, 110, 70)
        pen.moveTo((420, 240))
        pen.qCurveTo((480, 240), (520, 310))
        pen.lineTo((545, 280))
        pen.qCurveTo((495, 205), (410, 205))
        pen.closePath()
        draw_star_node(pen, 330, 745, 24)
        draw_star_node(pen, 545, 310, 18)
    add_glyph("l", ord("l"), 620, draw_l)
    add_glyph("L", ord("L"), 720, draw_l)

    # 2. 'r' : Crescent Slingshot Sweep (三日月公転フック ＋ 放物脱出スウィープ)
    # 脱・ラテンr（左の直線ステムを完全排除：天頂右膨らみ三日月から左下・右外へ抜ける重力軌道）
    def draw_r(pen):
        pen.moveTo((220, 580))
        pen.qCurveTo((480, 620), (480, 420))
        pen.qCurveTo((480, 270), (320, 270))
        pen.lineTo((320, 310))
        pen.qCurveTo((435, 310), (435, 410))
        pen.qCurveTo((435, 570), (220, 540))
        pen.closePath()
        pen.moveTo((320, 310))
        pen.qCurveTo((200, 310), (160, 180))
        pen.lineTo((195, 170))
        pen.qCurveTo((230, 275), (330, 275))
        pen.closePath()
        draw_star_node(pen, 210, 560, 20)
        draw_star_node(pen, 480, 420, 22)
        draw_star_node(pen, 160, 175, 20)
    add_glyph("r", ord("r"), 640, draw_r)
    add_glyph("R", ord("R"), 740, draw_r)

    # 3. 'm' : Celestial Bipolar Wings & Hanging Core (双天球交差翼 ＋ 降下星流核)
    # 脱・ラテンm（山2つを完全排除：中央天頂から左右に広がる天蓋翼と下垂する星流軸）
    def draw_m(pen):
        pen.moveTo((330, 500))
        pen.qCurveTo((210, 520), (160, 390))
        pen.qCurveTo((140, 270), (230, 270))
        pen.qCurveTo((280, 270), (280, 350))
        pen.lineTo((245, 350))
        pen.qCurveTo((245, 305), (225, 305))
        pen.qCurveTo((180, 305), (195, 380))
        pen.qCurveTo((230, 475), (330, 455))
        pen.closePath()
        pen.moveTo((330, 500))
        pen.qCurveTo((450, 520), (500, 390))
        pen.qCurveTo((520, 270), (430, 270))
        pen.qCurveTo((380, 270), (380, 350))
        pen.lineTo((415, 350))
        pen.qCurveTo((415, 305), (435, 305))
        pen.qCurveTo((480, 305), (465, 380))
        pen.qCurveTo((430, 475), (330, 455))
        pen.closePath()
        pen.moveTo((312, 470))
        pen.lineTo((312, 190))
        pen.lineTo((348, 190))
        pen.lineTo((348, 470))
        pen.closePath()
        draw_star_node(pen, 330, 530, 22)
        draw_star_node(pen, 330, 160, 24)
        draw_star_node(pen, 150, 390, 16)
        draw_star_node(pen, 510, 390, 16)
    add_glyph("m", ord("m"), 680, draw_m)
    add_glyph("M", ord("M"), 780, draw_m)

    # 4. 'n' : Vortex Inception Ribbon (始動スパイラル ＋ 上昇軌道リボン)
    # 脱・ラテンn（山1つを完全排除：左下の微小渦巻きから右上へ抜ける非対称星辰流線）
    def draw_n(pen):
        pen.moveTo((200, 240))
        pen.qCurveTo((150, 240), (150, 320))
        pen.qCurveTo((150, 400), (240, 400))
        pen.qCurveTo((310, 400), (310, 320))
        pen.qCurveTo((310, 240), (200, 240))
        pen.closePath()
        pen.moveTo((210, 275))
        pen.qCurveTo((275, 275), (275, 320))
        pen.qCurveTo((275, 365), (230, 365))
        pen.qCurveTo((185, 365), (185, 320))
        pen.qCurveTo((185, 275), (210, 275))
        pen.closePath()
        pen.moveTo((270, 370))
        pen.qCurveTo((340, 430), (440, 560))
        pen.lineTo((475, 530))
        pen.qCurveTo((370, 400), (280, 330))
        pen.closePath()
        draw_star_node(pen, 225, 320, 18)
        draw_star_node(pen, 460, 575, 24)
    add_glyph("n", ord("n"), 640, draw_n)
    add_glyph("N", ord("N"), 740, draw_n)

    # 5. 's' : Hourglass Bipolar Arc (砂時計型・双極磁場弧)
    # 脱・ラテンs（英字S字カーブを完全排除：上開き三日月と下開き三日月が中央核で点接触）
    def draw_s(pen):
        pen.moveTo((240, 560))
        pen.qCurveTo((440, 560), (345, 360))
        pen.lineTo((315, 360))
        pen.qCurveTo((395, 515), (240, 520))
        pen.closePath()
        pen.moveTo((420, 160))
        pen.qCurveTo((220, 160), (315, 360))
        pen.lineTo((345, 360))
        pen.qCurveTo((265, 205), (420, 200))
        pen.closePath()
        draw_star_node(pen, 330, 360, 24)
        draw_star_node(pen, 240, 560, 18)
        draw_star_node(pen, 420, 160, 18)
    add_glyph("s", ord("s"), 660, draw_s)
    add_glyph("S", ord("S"), 760, draw_s)

    # 6. 'z' : Resonant Bipolar Ring (連星共鳴環・双極幾何学)
    # 脱・ラテンz（Sに点ではなく、双極磁場の中央に完全な連星リングが嵌まる幾何学）
    def draw_z(pen):
        draw_s(pen)
        make_ring(pen, 330, 360, 75, 42)
        draw_star_node(pen, 170, 460, 16)
        draw_star_node(pen, 490, 260, 16)
    add_glyph("z", ord("z"), 660, draw_z)
    add_glyph("Z", ord("Z"), 760, draw_z)

    # 7. 'c' : Celestial Canopy Shade [ʃ] (静寂の天蓋シェード ＋ 垂下星核)
    # 脱・ラテンc（C字開口を排除：水平の静寂バーから滑らかな天蓋が下り内部に星核を宿す）
    def draw_c(pen):
        pen.moveTo((160, 520))
        pen.lineTo((500, 520))
        pen.lineTo((500, 480))
        pen.lineTo((160, 480))
        pen.closePath()
        pen.moveTo((180, 480))
        pen.qCurveTo((180, 220), (330, 220))
        pen.qCurveTo((480, 220), (480, 480))
        pen.lineTo((440, 480))
        pen.qCurveTo((440, 260), (330, 260))
        pen.qCurveTo((220, 260), (220, 480))
        pen.closePath()
        draw_star_node(pen, 330, 360, 24)
        draw_star_node(pen, 160, 520, 18)
        draw_star_node(pen, 500, 520, 18)
    add_glyph("c", ord("c"), 660, draw_c)
    add_glyph("C", ord("C"), 760, draw_c)

    # 8. 'j' : Binary Apex & Abyss Anchor [ʒ] (天頂連星対 ＋ 深淵旋回アンカー)
    # 脱・ラテンj（直線の縦棒＋フックを排除：天頂の双子星から右回りに深淵へ潜る螺旋アンカー）
    def draw_j(pen):
        pen.moveTo((330, 520))
        pen.qCurveTo((460, 520), (460, 260))
        pen.qCurveTo((460, -80), (300, -80))
        pen.qCurveTo((180, -80), (200, 40))
        pen.lineTo((235, 30))
        pen.qCurveTo((220, -40), (295, -40))
        pen.qCurveTo((415, -40), (415, 260))
        pen.qCurveTo((415, 480), (330, 480))
        pen.closePath()
        draw_star_node(pen, 270, 600, 20)
        draw_star_node(pen, 380, 600, 20)
        draw_star_node(pen, 215, 40, 18)
    add_glyph("j", ord("j"), 620, draw_j)
    add_glyph("J", ord("J"), 720, draw_j)

    # 9. 'f' : Aurora Ascent Curtain (上昇オーロラカーテン ＋ 左右対称天翼)
    # 脱・ラテンf（ステッキ＋横棒を完全排除：中央流線からオーロラのように上昇する左右の天翼）
    def draw_f(pen):
        pen.moveTo((310, 180))
        pen.lineTo((350, 180))
        pen.lineTo((350, 660))
        pen.lineTo((310, 660))
        pen.closePath()
        pen.moveTo((310, 360))
        pen.qCurveTo((180, 360), (160, 540))
        pen.lineTo((195, 545))
        pen.qCurveTo((215, 395), (310, 395))
        pen.closePath()
        pen.moveTo((350, 360))
        pen.qCurveTo((480, 360), (500, 540))
        pen.lineTo((465, 545))
        pen.qCurveTo((445, 395), (350, 395))
        pen.closePath()
        draw_star_node(pen, 330, 690, 24)
        draw_star_node(pen, 160, 540, 18)
        draw_star_node(pen, 500, 540, 18)
    add_glyph("f", ord("f"), 660, draw_f)
    add_glyph("F", ord("F"), 760, draw_f)

    # 10. 'v' : Celestial Cradle Bowl (天球受容ボウル ＋ 浮遊星辰核)
    # 脱・ラテンv（鋭角な尖ったV谷底を排除：天球を優雅に受容する深底パラボラと中央星核）
    def draw_v(pen):
        pen.moveTo((150, 520))
        pen.qCurveTo((180, 180), (330, 180))
        pen.qCurveTo((480, 180), (510, 520))
        pen.lineTo((465, 520))
        pen.qCurveTo((440, 225), (330, 225))
        pen.qCurveTo((220, 225), (195, 520))
        pen.closePath()
        draw_star_node(pen, 330, 370, 28)
        draw_star_node(pen, 150, 520, 18)
        draw_star_node(pen, 510, 520, 18)
    add_glyph("v", ord("v"), 660, draw_v)
    add_glyph("V", ord("V"), 760, draw_v)

    # 11. 'h' : Gateway of Celestial Pillars (双対天門ピラー)
    # 脱・ラテンh（棒＋山を排除：下部で結ばれ天に向かって大きく広がる星辰の門）
    def draw_h(pen):
        pen.moveTo((240, 180))
        pen.qCurveTo((200, 420), (170, 680))
        pen.lineTo((210, 680))
        pen.qCurveTo((240, 420), (275, 180))
        pen.closePath()
        pen.moveTo((420, 180))
        pen.qCurveTo((460, 420), (490, 680))
        pen.lineTo((450, 680))
        pen.qCurveTo((420, 420), (385, 180))
        pen.closePath()
        pen.moveTo((220, 220))
        pen.lineTo((440, 220))
        pen.lineTo((440, 180))
        pen.lineTo((220, 180))
        pen.closePath()
        draw_star_node(pen, 170, 680, 20)
        draw_star_node(pen, 490, 680, 20)
        draw_star_node(pen, 330, 360, 22)
    add_glyph("h", ord("h"), 660, draw_h)
    add_glyph("H", ord("H"), 760, draw_h)

    # 12. 'w' : Gravity Well Ripple (三次元重力波紋)
    # 脱・ラテンw（谷底2連を完全排除：同心円状に一段深く沈み込む重力波紋幾何学）
    def draw_w(pen):
        pen.moveTo((130, 460))
        pen.qCurveTo((200, 200), (330, 200))
        pen.qCurveTo((460, 200), (530, 460))
        pen.lineTo((495, 460))
        pen.qCurveTo((430, 240), (330, 240))
        pen.qCurveTo((230, 240), (165, 460))
        pen.closePath()
        pen.moveTo((220, 460))
        pen.qCurveTo((250, 310), (330, 310))
        pen.qCurveTo((410, 310), (440, 460))
        pen.lineTo((405, 460))
        pen.qCurveTo((380, 345), (330, 345))
        pen.qCurveTo((280, 345), (255, 460))
        pen.closePath()
        draw_star_node(pen, 330, 140, 24)
        draw_star_node(pen, 330, 410, 20)
    add_glyph("w", ord("w"), 660, draw_w)
    add_glyph("W", ord("W"), 760, draw_w)

    # 13. 'p' : Hanging Astral Pod (懸垂光芒ポッド)
    # 脱・ラテンp（左下棒＋丸を完全排除：天蓋水平軸から雫のように美しく下垂する閉鎖軌道ポッド）
    def draw_p(pen):
        pen.moveTo((180, 540))
        pen.lineTo((480, 540))
        pen.lineTo((480, 500))
        pen.lineTo((180, 500))
        pen.closePath()
        pen.moveTo((330, 500))
        pen.qCurveTo((220, 400), (220, 260))
        pen.qCurveTo((220, 160), (330, 160))
        pen.qCurveTo((440, 160), (440, 260))
        pen.qCurveTo((440, 400), (330, 500))
        pen.closePath()
        pen.moveTo((330, 430))
        pen.qCurveTo((395, 360), (395, 260))
        pen.qCurveTo((395, 200), (330, 200))
        pen.qCurveTo((265, 200), (265, 260))
        pen.qCurveTo((265, 360), (330, 430))
        pen.closePath()
        draw_star_node(pen, 330, 110, 22)
    add_glyph("p", ord("p"), 660, draw_p)
    add_glyph("P", ord("P"), 760, draw_p)

    # 14. 'b' : Dual Orbit Shell & Stem (二重軌道シェル ＋ 昇華ステム)
    # 脱・ラテンb（縦棒＋丸を完全排除：垂直昇華軸を上下から左右非対称に包み込む二重軌道シェル）
    def draw_b(pen):
        pen.moveTo((310, 160))
        pen.lineTo((350, 160))
        pen.lineTo((350, 700))
        pen.lineTo((310, 700))
        pen.closePath()
        pen.moveTo((310, 620))
        pen.qCurveTo((180, 620), (180, 460))
        pen.qCurveTo((180, 380), (310, 380))
        pen.lineTo((310, 420))
        pen.qCurveTo((225, 420), (225, 460))
        pen.qCurveTo((225, 580), (310, 580))
        pen.closePath()
        pen.moveTo((350, 440))
        pen.qCurveTo((480, 440), (480, 280))
        pen.qCurveTo((480, 200), (350, 200))
        pen.lineTo((350, 240))
        pen.qCurveTo((435, 240), (435, 280))
        pen.qCurveTo((435, 400), (350, 400))
        pen.closePath()
        draw_star_node(pen, 330, 725, 22)
        draw_star_node(pen, 180, 460, 18)
        draw_star_node(pen, 480, 280, 18)
    add_glyph("b", ord("b"), 660, draw_b)
    add_glyph("B", ord("B"), 760, draw_b)

    # 15. 't' : Curved Canopy & Tri-Anchor (反り天蓋 ＋ 3点支持アンカー)
    # 脱・ラテンt（単なる十字架を完全排除：弓なりに天を仰ぐ優美な天蓋と3点接地アンカー）
    def draw_t(pen):
        pen.moveTo((150, 620))
        pen.qCurveTo((330, 550), (510, 620))
        pen.lineTo((500, 660))
        pen.qCurveTo((330, 595), (160, 660))
        pen.closePath()
        pen.moveTo((310, 240))
        pen.lineTo((310, 600))
        pen.lineTo((350, 600))
        pen.lineTo((350, 240))
        pen.closePath()
        pen.moveTo((310, 320))
        pen.lineTo((200, 230))
        pen.lineTo((220, 210))
        pen.lineTo((330, 300))
        pen.closePath()
        pen.moveTo((350, 320))
        pen.lineTo((460, 230))
        pen.lineTo((440, 210))
        pen.lineTo((330, 300))
        pen.closePath()
        draw_star_node(pen, 330, 180, 24)
        draw_star_node(pen, 200, 230, 18)
        draw_star_node(pen, 460, 230, 18)
        draw_star_node(pen, 150, 630, 18)
        draw_star_node(pen, 510, 630, 18)
    add_glyph("t", ord("t"), 660, draw_t)
    add_glyph("T", ord("T"), 760, draw_t)

    # 16. 'd' : Crescent Base & Ascending Spire (基底台座三日月 ＋ 直立尖塔スパーク)
    # 脱・ラテンd（丸＋棒を排除：安定した台座三日月の中央から天へ突き抜ける直立尖塔）
    def draw_d(pen):
        pen.moveTo((140, 340))
        pen.qCurveTo((140, 160), (330, 160))
        pen.qCurveTo((520, 160), (520, 340))
        pen.lineTo((475, 340))
        pen.qCurveTo((475, 205), (330, 205))
        pen.qCurveTo((185, 205), (185, 340))
        pen.closePath()
        pen.moveTo((310, 160))
        pen.lineTo((310, 660))
        pen.lineTo((350, 660))
        pen.lineTo((350, 160))
        pen.closePath()
        draw_star_node(pen, 330, 710, 26)
        draw_star_node(pen, 140, 340, 18)
        draw_star_node(pen, 520, 340, 18)
    add_glyph("d", ord("d"), 660, draw_d)
    add_glyph("D", ord("D"), 760, draw_d)

    # 17. 'k' : Tri-Radiant Prominence & Star Nucleus (三方放射プロミネンス ＋ 中心核)
    # 脱・ラテンk（縦棒＋くの字を完全排除：中心核から三方120度へ放たれる優美な光芒弧）
    def draw_k(pen):
        pen.moveTo((315, 360))
        pen.qCurveTo((315, 540), (260, 680))
        pen.lineTo((295, 680))
        pen.qCurveTo((345, 540), (345, 360))
        pen.closePath()
        pen.moveTo((330, 340))
        pen.qCurveTo((440, 340), (510, 200))
        pen.lineTo((480, 180))
        pen.qCurveTo((410, 305), (330, 305))
        pen.closePath()
        pen.moveTo((330, 340))
        pen.qCurveTo((220, 340), (150, 200))
        pen.lineTo((180, 180))
        pen.qCurveTo((250, 305), (330, 305))
        pen.closePath()
        draw_star_node(pen, 330, 350, 28)
        draw_star_node(pen, 275, 690, 20)
        draw_star_node(pen, 495, 190, 20)
        draw_star_node(pen, 165, 190, 20)
    add_glyph("k", ord("k"), 660, draw_k)
    add_glyph("K", ord("K"), 760, draw_k)

    # 18. 'g' : Gravitational Lens Prominence (重力屈折プロミネンス ＋ 完全天球環)
    # 脱・ラテンg（kに丸を描いただけを排除：三方光芒が周囲の完全天球リングと共鳴交差する幾何学）
    def draw_g(pen):
        draw_k(pen)
        make_ring(pen, 330, 350, 190, 150)
    add_glyph("g", ord("g"), 680, draw_g)
    add_glyph("G", ord("G"), 780, draw_g)

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

    # '0' : Nodal Reticle & Singularity Void (特異点・天球照準環)
    # 脱・アラビア数字0：単なる丸を完全排除。円環の中央に星辰特異点核、南北に貫く繊細な原初照準軸、左右照準刻線
    def draw_num_0(pen):
        make_ring(pen, 330, 400, 180, 130)
        # 南北垂直照準軸 (Vertical Reticle Axis)
        pen.moveTo((315, 620))
        pen.lineTo((345, 620))
        pen.lineTo((345, 180))
        pen.lineTo((315, 180))
        pen.closePath()
        # 水平照準刻線 (Horizontal Ticks)
        pen.moveTo((110, 415))
        pen.lineTo((190, 415))
        pen.lineTo((190, 385))
        pen.lineTo((110, 385))
        pen.closePath()
        pen.moveTo((470, 415))
        pen.lineTo((550, 415))
        pen.lineTo((550, 385))
        pen.lineTo((470, 385))
        pen.closePath()
        # 中央の特異点星辰核 (Singularity Node)
        draw_star_node(pen, 330, 400, 28)
        draw_star_node(pen, 330, 640, 18)
        draw_star_node(pen, 330, 160, 18)
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

    import base64
    with open(out_path, "rb") as f:
        b64_str = base64.b64encode(f.read()).decode("ascii")
    b64_path = os.path.join(out_dir, "font_b64.txt")
    with open(b64_path, "w", encoding="ascii") as f:
        f.write(b64_str)
    print(f"Base64 font saved to {b64_path} ({len(b64_str)} chars)")


if __name__ == "__main__":
    build_font()
