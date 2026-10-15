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

    # =========================================================================
    # 6 PRIMARY VOWELS (De-Latinized Astral Vowel Geometry)
    # =========================================================================
    
    # 'a' : Dawn Arch & Solar Ray (黎明の天蓋弧 ＋ 昇華光芒軸 ＋ 三連星核)
    # 脱・単なるU反転：天蓋ドームの中央から昇る黎明の垂直光芒と、天頂・東西の三連星辰核
    def draw_a(pen):
        # 1. 黎明天蓋弧 (Dawn Canopy Arch)
        pen.moveTo((140, 260))
        pen.qCurveTo((140, 480), (330, 480))
        pen.qCurveTo((520, 480), (520, 260))
        pen.lineTo((475, 260))
        pen.qCurveTo((475, 435), (330, 435))
        pen.qCurveTo((185, 435), (185, 260))
        pen.closePath()
        # 2. 昇華光芒軸 (Vertical Solar Spire)
        pen.moveTo((312, 260))
        pen.lineTo((312, 620))
        pen.lineTo((348, 620))
        pen.lineTo((348, 260))
        pen.closePath()
        # 3. 星辰核 (Nodes)
        draw_star_node(pen, 330, 650, 26)  # 天頂主星
        draw_star_node(pen, 140, 260, 18)  # 東翼星
        draw_star_node(pen, 520, 260, 18)  # 西翼星
        draw_star_node(pen, 330, 380, 20)  # 中央核
    add_glyph("a", ord("a"), 660, draw_a)
    add_glyph("A", ord("A"), 760, draw_a)

    # 'e' : Solar Wind Diphthong Wave (星風二連交差波 ＋ 双子星核)
    # 脱・単なる波線：2本の平行する流麗な公転波線が優雅に交差し、上下に双子星ノードを抱く
    def draw_e(pen):
        # 上昇波線 (Ascending Solar Ribbon)
        pen.moveTo((140, 260))
        pen.qCurveTo((220, 480), (330, 480))
        pen.qCurveTo((450, 480), (520, 320))
        pen.lineTo((485, 300))
        pen.qCurveTo((425, 435), (330, 435))
        pen.qCurveTo((240, 435), (175, 240))
        pen.closePath()
        # 下降反転波線 (Counter Wave)
        pen.moveTo((140, 380))
        pen.qCurveTo((210, 220), (330, 220))
        pen.qCurveTo((440, 220), (520, 440))
        pen.lineTo((485, 460))
        pen.qCurveTo((415, 265), (330, 265))
        pen.qCurveTo((230, 265), (175, 400))
        pen.closePath()
        # 双子連星核 (Gemini Astral Nodes)
        draw_star_node(pen, 330, 520, 22)
        draw_star_node(pen, 330, 180, 22)
        draw_star_node(pen, 140, 320, 18)
        draw_star_node(pen, 520, 380, 18)
    add_glyph("e", ord("e"), 660, draw_e)
    add_glyph("E", ord("E"), 760, draw_e)

    # 'i' : Polaris Celestial Spire (北極星の基底尖塔 ＋ 頂点八芒主星)
    # 脱・単なる縦棒＋点：基底の安定した台座から天頂へ鋭く昇華する光芒尖塔と頂点の輝く主星
    def draw_i(pen):
        # 1. 基底天蓋台座 (Plinth Arc)
        pen.moveTo((180, 220))
        pen.qCurveTo((330, 260), (480, 220))
        pen.lineTo((470, 180))
        pen.qCurveTo((330, 220), (190, 180))
        pen.closePath()
        # 2. 直立尖塔光芒 (Ascending Polaris Spire)
        pen.moveTo((312, 200))
        pen.lineTo((312, 650))
        pen.lineTo((348, 650))
        pen.lineTo((348, 200))
        pen.closePath()
        # 3. 尖塔翼 (Spire Flanges)
        pen.moveTo((312, 420))
        pen.lineTo((240, 360))
        pen.lineTo((255, 340))
        pen.lineTo((312, 380))
        pen.closePath()
        pen.moveTo((348, 420))
        pen.lineTo((420, 360))
        pen.lineTo((405, 340))
        pen.lineTo((348, 380))
        pen.closePath()
        # 4. 北極主星核 (Polaris Primary Node)
        draw_star_node(pen, 330, 710, 30)
        draw_star_node(pen, 180, 220, 16)
        draw_star_node(pen, 480, 220, 16)
        draw_star_node(pen, 330, 380, 20)
    add_glyph("i", ord("i"), 620, draw_i)
    add_glyph("I", ord("I"), 720, draw_i)

    # 'o' : Full Moon Orbit & Equatorial Axis (満月天球二重環 ＋ 巡行衛星対)
    # 脱・単なるリング＋点：完全な二重円環の内部に赤道光芒バーが走り、軌道上に2つの巡行衛星ノードが対峙
    def draw_o(pen):
        make_ring(pen, 330, 360, 180, 130)
        # 赤道光芒バー (Equatorial Starlight Bar)
        pen.moveTo((170, 375))
        pen.lineTo((490, 375))
        pen.lineTo((490, 345))
        pen.lineTo((170, 345))
        pen.closePath()
        # 天頂・天底巡行衛星対 (Orbital Satellites)
        draw_star_node(pen, 330, 575, 24)
        draw_star_node(pen, 330, 145, 24)
        draw_star_node(pen, 330, 360, 22)
    add_glyph("o", ord("o"), 680, draw_o)
    add_glyph("O", ord("O"), 780, draw_o)

    # 'u' : Deep Abyss Chalice (天底の深淵杯 ＋ 3点支持星辰核)
    # 脱・単なるU字：優雅な外反りを持つ天底の受容杯と、底面を支える3点星辰アンカー
    def draw_u(pen):
        # 深淵受容杯 (Abyss Chalice)
        pen.moveTo((140, 520))
        pen.qCurveTo((180, 480), (180, 300))
        pen.qCurveTo((180, 180), (330, 180))
        pen.qCurveTo((480, 180), (480, 300))
        pen.qCurveTo((480, 480), (520, 520))
        pen.lineTo((480, 535))
        pen.qCurveTo((440, 460), (440, 300))
        pen.qCurveTo((440, 220), (330, 220))
        pen.qCurveTo((220, 220), (220, 300))
        pen.qCurveTo((220, 460), (180, 535))
        pen.closePath()
        # 3点支持アンカー核 (Tri-Anchor Nodes)
        draw_star_node(pen, 330, 120, 26)  # 中央深底核
        draw_star_node(pen, 190, 160, 18)  # 左脚核
        draw_star_node(pen, 470, 160, 18)  # 右脚核
        draw_star_node(pen, 140, 520, 18)  # 左杯縁
        draw_star_node(pen, 520, 520, 18)  # 右杯縁
    add_glyph("u", ord("u"), 660, draw_u)
    add_glyph("U", ord("U"), 760, draw_u)

    # 'y' : Astral Ypsilon Crystallography (第6星辰結晶環 ＋ 屈折ループ)
    # 脱・英字y骨格：左右の対向三日月弧が下部中央で交差し、深淵へ向かって対称的な結晶ループを描く
    def draw_y(pen):
        # 上部左右対向三日月 (Upper Bipolar Crescents)
        pen.moveTo((150, 520))
        pen.qCurveTo((240, 340), (330, 340))
        pen.qCurveTo((420, 340), (510, 520))
        pen.lineTo((470, 535))
        pen.qCurveTo((395, 380), (330, 380))
        pen.qCurveTo((265, 380), (190, 535))
        pen.closePath()
        # 下部結晶ドロップループ (Subterranean Crystal Loop)
        pen.moveTo((330, 360))
        pen.qCurveTo((420, 220), (420, 40))
        pen.qCurveTo((420, -100), (330, -100))
        pen.qCurveTo((240, -100), (240, 40))
        pen.qCurveTo((240, 220), (330, 360))
        pen.closePath()
        # ループ内空洞
        pen.moveTo((330, 290))
        pen.qCurveTo((280, 180), (280, 40))
        pen.qCurveTo((280, -55), (330, -55))
        pen.qCurveTo((380, -55), (380, 40))
        pen.qCurveTo((380, 180), (330, 290))
        pen.closePath()
        # 星辰核
        draw_star_node(pen, 150, 520, 20)
        draw_star_node(pen, 510, 520, 20)
        draw_star_node(pen, 330, 360, 24)
        draw_star_node(pen, 330, -100, 22)
    add_glyph("y", ord("y"), 660, draw_y)
    add_glyph("Y", ord("Y"), 760, draw_y)

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

    # '1' : Monopole Gravity Spire (単極重力尖塔 ＋ 天頂主星)
    # 脱・アラビア数字1：中央垂直光芒軸の天頂に主星、中央に重力リングが嵌まる端正な天球軸
    def draw_num_1(pen):
        pen.moveTo((312, 180))
        pen.lineTo((312, 660))
        pen.lineTo((348, 660))
        pen.lineTo((348, 180))
        pen.closePath()
        make_ring(pen, 330, 400, 65, 35)
        draw_star_node(pen, 330, 710, 28)
        draw_star_node(pen, 330, 160, 22)
    add_glyph("one", ord("1"), 600, draw_num_1)

    # '2' : Binary Mutual Crescents (対向公転三日月対)
    # 脱・アラビア数字2：左右から互いに向かい合って公転する連星二重弧
    def draw_num_2(pen):
        # 左側公転弧 (Left Orbit Arc)
        pen.moveTo((180, 560))
        pen.qCurveTo((330, 560), (330, 380))
        pen.qCurveTo((330, 200), (180, 200))
        pen.lineTo((215, 200))
        pen.qCurveTo((290, 200), (290, 380))
        pen.qCurveTo((290, 520), (180, 520))
        pen.closePath()
        # 右側公転弧 (Right Orbit Arc)
        pen.moveTo((480, 560))
        pen.qCurveTo((330, 560), (330, 380))
        pen.qCurveTo((330, 200), (480, 200))
        pen.lineTo((445, 200))
        pen.qCurveTo((370, 200), (370, 380))
        pen.qCurveTo((370, 520), (480, 520))
        pen.closePath()
        draw_star_node(pen, 180, 560, 20)
        draw_star_node(pen, 180, 200, 20)
        draw_star_node(pen, 480, 560, 20)
        draw_star_node(pen, 480, 200, 20)
        draw_star_node(pen, 330, 380, 24)
    add_glyph("two", ord("2"), 660, draw_num_2)

    # '3' : Triskele Orbital Loops (三つ葉星辰トリスケル)
    # 脱・丸を直線で結んだだけ：120度ごとに優雅に広がる三つ葉軌道ループと3つの星辰核
    def draw_num_3(pen):
        make_ring(pen, 330, 400, 60, 32)
        # 上部ループ
        pen.moveTo((330, 460))
        pen.qCurveTo((240, 580), (330, 640))
        pen.qCurveTo((420, 580), (330, 460))
        pen.closePath()
        # 右下ループ
        pen.moveTo((370, 360))
        pen.qCurveTo((520, 340), (480, 220))
        pen.qCurveTo((380, 240), (370, 360))
        pen.closePath()
        # 左下ループ
        pen.moveTo((290, 360))
        pen.qCurveTo((140, 340), (180, 220))
        pen.qCurveTo((280, 240), (290, 360))
        pen.closePath()
        draw_star_node(pen, 330, 640, 22)
        draw_star_node(pen, 480, 220, 22)
        draw_star_node(pen, 180, 220, 22)
        draw_star_node(pen, 330, 400, 20)
    add_glyph("three", ord("3"), 660, draw_num_3)

    # '4' : Quad Nodal Cross & Diamond (四天球結節ダイヤ)
    # 脱・丸に楕円：四方に広がる優美なダイヤ型軌道枠と四隅の天体アンカー
    def draw_num_4(pen):
        make_ring(pen, 330, 400, 70, 38)
        # 四方光芒スパーク (Quad Diamond Flares)
        pen.moveTo((330, 660))
        pen.lineTo((350, 470))
        pen.lineTo((540, 400))
        pen.lineTo((350, 330))
        pen.lineTo((330, 140))
        pen.lineTo((310, 330))
        pen.lineTo((120, 400))
        pen.lineTo((310, 470))
        pen.closePath()
        draw_star_node(pen, 330, 660, 22)
        draw_star_node(pen, 540, 400, 22)
        draw_star_node(pen, 330, 140, 22)
        draw_star_node(pen, 120, 400, 22)
    add_glyph("four", ord("4"), 660, draw_num_4)

    # '5' : Pentagram Vortex Ribbon (五芒螺旋リボン)
    # 脱・カクカク直線の一筆書き：滑らかな曲線で結ばれる五連星雲ループ
    def draw_num_5(pen):
        make_ring(pen, 330, 400, 50, 25)
        # 外周五星への光芒曲線 (5-Point Astral Curve)
        pen.moveTo((330, 650))
        pen.qCurveTo((480, 560), (490, 420))
        pen.qCurveTo((500, 280), (430, 200))
        pen.qCurveTo((330, 200), (230, 200))
        pen.qCurveTo((160, 280), (170, 420))
        pen.qCurveTo((180, 560), (330, 650))
        pen.closePath()
        # 内側抜き
        pen.moveTo((330, 600))
        pen.qCurveTo((210, 520), (210, 410))
        pen.qCurveTo((210, 260), (330, 260))
        pen.qCurveTo((450, 260), (450, 410))
        pen.qCurveTo((450, 520), (330, 600))
        pen.closePath()
        draw_star_node(pen, 330, 650, 20)
        draw_star_node(pen, 520, 420, 20)
        draw_star_node(pen, 430, 180, 20)
        draw_star_node(pen, 230, 180, 20)
        draw_star_node(pen, 140, 420, 20)
    add_glyph("five", ord("5"), 660, draw_num_5)

    # '6' : Comet Head & Sweeping Tail (彗星核 ＋ 長大放物線テイル)
    # 脱・アラビア数字6：上部左の巨大彗星核から右下へ向かって長大に広がる放物線テイル
    def draw_num_6(pen):
        # 彗星核 (Comet Core)
        make_ring(pen, 250, 500, 90, 45)
        # 上部テイル (Upper Parabolic Tail)
        pen.moveTo((310, 540))
        pen.qCurveTo((460, 500), (540, 220))
        pen.lineTo((505, 210))
        pen.qCurveTo((430, 465), (290, 500))
        pen.closePath()
        # 下部テイル (Lower Parabolic Tail)
        pen.moveTo((260, 415))
        pen.qCurveTo((380, 360), (480, 160))
        pen.lineTo((445, 150))
        pen.qCurveTo((355, 335), (235, 415))
        pen.closePath()
        draw_star_node(pen, 250, 500, 28)
        draw_star_node(pen, 540, 220, 20)
        draw_star_node(pen, 480, 160, 20)
    add_glyph("six", ord("6"), 660, draw_num_6)

    # '7' : Septet Canopy Arc (七星天蓋弧)
    def draw_num_7(pen):
        pen.moveTo((160, 440))
        pen.qCurveTo((160, 620), (330, 620))
        pen.qCurveTo((500, 620), (500, 440))
        pen.lineTo((460, 440))
        pen.qCurveTo((460, 575), (330, 575))
        pen.qCurveTo((200, 575), (200, 440))
        pen.closePath()
        pen.moveTo((310, 580))
        pen.qCurveTo((380, 390), (300, 200))
        pen.lineTo((345, 200))
        pen.qCurveTo((420, 390), (350, 580))
        pen.closePath()
        draw_star_node(pen, 330, 680, 24)
        draw_star_node(pen, 160, 440, 18)
        draw_star_node(pen, 500, 440, 18)
        draw_star_node(pen, 300, 180, 20)
        draw_star_node(pen, 385, 340, 15)
        draw_star_node(pen, 275, 420, 13)
    add_glyph("seven", ord("7"), 660, draw_num_7)

    # '8' : Bipolar Horizon (双極連星環)
    def draw_num_8(pen):
        make_ring(pen, 330, 400, 75, 38)
        pen.moveTo((160, 580))
        pen.qCurveTo((265, 400), (160, 220))
        pen.lineTo((198, 220))
        pen.qCurveTo((298, 400), (198, 580))
        pen.closePath()
        pen.moveTo((500, 580))
        pen.qCurveTo((395, 400), (500, 220))
        pen.lineTo((462, 220))
        pen.qCurveTo((362, 400), (462, 580))
        pen.closePath()
        draw_star_node(pen, 160, 580, 18)
        draw_star_node(pen, 160, 220, 18)
        draw_star_node(pen, 500, 580, 18)
        draw_star_node(pen, 500, 220, 18)
        draw_star_node(pen, 330, 560, 18)
        draw_star_node(pen, 330, 240, 18)
    add_glyph("eight", ord("8"), 660, draw_num_8)

    # '9' : Apex Eclipse Corona (頂点食・二重天球コロナ)
    # 脱・アラビア数字9：天頂で重なり合う2つの天球円環と、下方へ放たれるコロナ光芒
    def draw_num_9(pen):
        # 主星天球
        make_ring(pen, 300, 480, 110, 65)
        # 食を起こす伴星天球 (Occulting Body)
        make_ring(pen, 380, 480, 90, 50)
        # 降下コロナ光芒 (Coronal Downward Rays)
        pen.moveTo((315, 380))
        pen.lineTo((315, 160))
        pen.lineTo((345, 160))
        pen.lineTo((345, 380))
        pen.closePath()
        pen.moveTo((380, 395))
        pen.qCurveTo((440, 300), (480, 180))
        pen.lineTo((450, 170))
        pen.qCurveTo((410, 290), (355, 380))
        pen.closePath()
        draw_star_node(pen, 330, 150, 24)
        draw_star_node(pen, 480, 180, 18)
    add_glyph("nine", ord("9"), 660, draw_num_9)

    # =========================================================================
    # PUNCTUATION & CONNECTORS (Astral Signets)
    # =========================================================================

    # Period '.' : Stellar Nucleus Dot (星辰特異点ドット)
    def draw_period(pen):
        make_ring(pen, 200, 180, 35, 15)
        draw_star_node(pen, 200, 180, 12)
    add_glyph("period", ord("."), 400, draw_period)

    # Comma ',' : Comet Tail Point (彗星テールコンマ)
    def draw_comma(pen):
        draw_star_node(pen, 200, 220, 22)
        pen.moveTo((215, 210))
        pen.qCurveTo((230, 120), (160, 50))
        pen.lineTo((185, 40))
        pen.qCurveTo((255, 110), (235, 210))
        pen.closePath()
    add_glyph("comma", ord(","), 400, draw_comma)

    # Colon ':' : Binary Alignment (天体直列コロン)
    def draw_colon(pen):
        draw_star_node(pen, 200, 420, 20)
        draw_star_node(pen, 200, 200, 20)
        # 接続光芒ライン
        pen.moveTo((193, 200))
        pen.lineTo((193, 420))
        pen.lineTo((207, 420))
        pen.lineTo((207, 200))
        pen.closePath()
    add_glyph("colon", ord(":"), 400, draw_colon)

    # Hyphen '-' : Orbital Bridge Connector (星間架橋ハイフン)
    def draw_hyphen(pen):
        pen.moveTo((120, 375))
        pen.lineTo((380, 375))
        pen.lineTo((380, 345))
        pen.lineTo((120, 345))
        pen.closePath()
        draw_star_node(pen, 120, 360, 18)
        draw_star_node(pen, 380, 360, 18)
        draw_star_node(pen, 250, 360, 14)
    add_glyph("hyphen", ord("-"), 500, draw_hyphen)

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
