# tools/update_all_remaining_glyphs.py
import re

with open("tools/build_font.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. NEW 6 VOWELS SECTION
vowels_pattern = r"(    # ==========================================\s+# 6 VOWELS: a, e, i, o, u, y\s+# ==========================================.*?)(    # =========================================================================\s+# 16 PRIMARY CONSONANTS)"

new_vowels = """    # =========================================================================
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

"""

code, n_subs1 = re.subn(vowels_pattern, new_vowels + r"\2", code, flags=re.DOTALL)
assert n_subs1 == 1, f"Failed to substitute vowels, count={n_subs1}"

# 2. NEW NUMERALS 1 - 9 SECTION (0, 7, 8 are already good, improve 1, 2, 3, 4, 5, 6, 9)
nums_pattern = r"(    # '1' : Solitary Star.*?)(    # ==========================================\s+# PUNCTUATION)"

new_nums = """    # '1' : Monopole Gravity Spire (単極重力尖塔 ＋ 天頂主星)
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

"""

code, n_subs2 = re.subn(nums_pattern, new_nums + r"\2", code, flags=re.DOTALL)
assert n_subs2 == 1, f"Failed to substitute numerals, count={n_subs2}"

# 3. NEW PUNCTUATION SECTION
punct_pattern = r"(    # ==========================================\s+# PUNCTUATION.*?)(    # ==========================================\s+# ASSEMBLE TRUETYPE FONT TABLES)"

new_punct = """    # =========================================================================
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

"""

code, n_subs3 = re.subn(punct_pattern, new_punct + r"\2", code, flags=re.DOTALL)
assert n_subs3 == 1, f"Failed to substitute punctuation, count={n_subs3}"

with open("tools/build_font.py", "w", encoding="utf-8") as f:
    f.write(code)

print("tools/build_font.py successfully updated with 100% Unified Astral Glyphs!")
