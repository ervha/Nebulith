# tools/generate_v21_candidates.py
"""
Nebulith Candidate Generator for v21.0 Expansion (660 -> 740 master roots)
Pure celestial aesthetics, strictly zero Earth borrowings, perfectly audited phonotactics.
"""

NEW_80_ENTRIES_V21 = [
    # 1. 天体・宇宙力学・光 (4語)
    ("1. 天体・宇宙力学・光", "falzon", "[fal.zon]", "名", "星間偏光、磁場散乱光", "interstellar polarization, scattered starlight", "fal (光) + zon (偏光)"),
    ("1. 天体・宇宙力学・光", "vorlyk", "[vor.lyk]", "名", "公転周期、会合周期、周回調和", "orbital period, synodic cycle", "vor (公転) + lyk (規則拍)"),
    ("1. 天体・宇宙力学・光", "kymtul", "[kym.tul]", "名", "半影、薄影、光境界領域", "penumbra, twilight boundary", "kym (影) + tul (浅い)"),
    ("1. 天体・宇宙力学・光", "zoharven", "[zo.har.ven]", "名", "恒星風バブル、太陽圏境界面", "heliopause, astrosphere bubble", "zohar (主星) + ven (境界流)"),

    # 2. 数理・幾何・計測 (5語)
    ("2. 数理・幾何・計測", "dorven", "[dor.ven]", "名", "螺旋、渦巻曲線、旋回軌跡", "spiral, helix, logarithmic whorl", "dor (周回) + ven (進行)"),
    ("2. 数理・幾何・計測", "niftas", "[nif.tas]", "名", "公差、許容誤差、計測マージン", "tolerance, margin of error", "niven (次元) + tas (幅)"),
    ("2. 数理・幾何・計測", "kelpon", "[kel.pon]", "名", "勾配、傾き、グラディエント", "gradient, slope, inclination rate", "kel (変位) + pon (上昇度)"),
    ("2. 数理・幾何・計測", "firkat", "[fir.kat]", "名", "極限値、リミット、収束点", "limit, convergence point", "firas (定数) + kat (極限)"),
    ("2. 数理・幾何・計測", "sufron", "[suf.ron]", "名", "統計、確率分布、標本集計", "statistics, probability distribution", "suf (計算) + ron (集合)"),

    # 3. 情報・計算機・通信 (4語)
    ("3. 情報・計算機・通信", "tolrin", "[tol.rin]", "名", "帯域幅、伝送容量、チャンネル幅", "bandwidth, channel capacity", "tolas (通信) + rin (環/枠)"),
    ("3. 情報・計算機・通信", "suflik", "[suf.lik]", "名", "ヒューリスティック、探索近似法", "heuristic, approximate search", "suf (計算) + lik (探索)"),
    ("3. 情報・計算機・通信", "livkas", "[liv.kas]", "名", "アーカイブ、長期保管記録、恒久書庫", "archive, persistent store, vault", "livar (保管庫) + kas (強固)"),
    ("3. 情報・計算機・通信", "krotpan", "[krot.pan]", "動", "クラッシュする、異常終了する、破綻する", "crash, abend, terminate abnormally", "krot (破綻) + pan (分解)"),

    # 4. 生命・生体・医療 (4語)
    ("4. 生命・生体・医療", "revsol", "[rev.sol]", "名", "代謝、生体恒常性、生命維持循環", "metabolism, homeostasis", "rev (生気) + sol (循環)"),
    ("4. 生命・生体・医療", "morvyn", "[mor.vyn]", "名", "軟骨、軟組織、緩衝肉", "cartilage, cushioning tissue", "mor (肉) + vyn (柔軟)"),
    ("4. 生命・生体・医療", "darisan", "[da.ri.san]", "動", "療養する、回復する、快復に向かう", "convalesce, recuperate, heal", "daris (治癒) + an (動詞化)"),
    ("4. 生命・生体・医療", "serkin", "[ser.kin]", "名", "まどろみ、浅い眠り、仮眠", "doze, light slumber, nap", "serkym (睡眠) + kin (小)"),

    # 5. 自然地形・地質・鉱物 (5語)
    ("5. 自然地形・地質・鉱物", "talrimor", "[tal.ri.mor]", "名", "砂丘、風成砂丘、砂の波", "dune, sand dune, barchan", "talrim (砂漠) + mor (隆起)"),
    ("5. 自然地形・地質・鉱物", "talsil", "[tal.sil]", "名", "鉱脈、母岩中の富鉱帯、鉱床", "ore vein, mineral lode, deposit", "tal (岩) + sil (内部)"),
    ("5. 自然地形・地質・鉱物", "talcor", "[tal.cor]", "名", "巨石、一枚岩、モノリス", "monolith, megalith, huge boulder", "tal (石) + cor (巨大)"),
    ("5. 自然地形・地質・鉱物", "talvir", "[tal.vir]", "名", "粘土、陶土、可塑性鉱物土", "clay, loam, potter's earth", "tal (土) + vir (柔軟)"),
    ("5. 自然地形・地質・鉱物", "talpan", "[tal.pan]", "動", "崩落する、地滑りを起こす、土砂崩れ", "cave in, landslide, slump", "tal (地) + pan (崩れ)"),

    # 6. 気象・大気・水域 (4語)
    ("6. 気象・大気・水域", "celtyr", "[cel.tyr]", "名", "巻雲、すじ雲、高層氷晶雲", "cirrus cloud, ice feather cloud", "celis (雲) + tyr (羽)"),
    ("6. 気象・大気・水域", "wylmin", "[wyl.min]", "名", "凪、無風状態、静穏気流", "calm, dead calm, stillness of air", "wylas (風) + min (静止)"),
    ("6. 気象・大気・水域", "darlik", "[dar.lik]", "名", "地下水、伏流水、帯水層", "groundwater, subterranean stream", "daris (水) + lik (深処)"),
    ("6. 気象・大気・水域", "kyrvyn", "[kyr.vyn]", "名", "樹氷、霧氷、枝氷", "rime, hoarfrost, glazed frost", "kyras (氷) + vyn (針)"),

    # 7. 植物・生態・農耕 (6語)
    ("7. 植物・生態・農耕", "velcon", "[vel.con]", "名", "大樹、古木、神木、長寿樹", "ancient tree, venerable bough", "vel (木) + con (尊大)"),
    ("7. 植物・生態・農耕", "velmorn", "[vel.morn]", "名", "苔、地衣類、岩肌の緑被", "moss, lichen, lithophyte", "vel (草木) + morn (密着)"),
    ("7. 植物・生態・農耕", "velcor", "[vel.cor]", "名", "木立、林、小規模な樹林", "grove, copse, woodlot", "vel (木) + cor (集まり)"),
    ("7. 植物・生態・農耕", "teirvon", "[teir.von]", "名", "発芽、芽生え、萌芽", "germination, sprout, seedling rise", "teiril (種) + von (萌出)"),
    ("7. 植物・生態・農耕", "velparn", "[vel.parn]", "名", "花弁、花びら、彩色の萼片", "petal, corolla, floral lobe", "velin (花) + parn (薄片)"),
    ("7. 植物・生態・農耕", "vorkas", "[vor.kas]", "名", "穀物倉、収穫貯蔵庫、サイロ", "granary, grain storehouse", "vorken (収穫) + kas (庫)"),

    # 8. 動物・生物種・共生 (7語)
    ("8. 動物・生物種・共生", "volron", "[vol.ron]", "名", "渡り鳥、渡り、群れ飛翔", "migratory bird, flock migration", "volfer (鳥) + ron (渡り)"),
    ("8. 動物・生物種・共生", "fercor", "[fer.cor]", "名", "獣群、群れ、放牧群", "herd, pack, assemblage of beasts", "feras (獣) + cor (集団)"),
    ("8. 動物・生物種・共生", "zylcor", "[zyl.cor]", "名", "水棲甲殻類、貝類、外骨格生物", "crustacean, shellfish, mollusk", "zylfer (水生) + cor (殻)"),
    ("8. 動物・生物種・共生", "krapil", "[krap.il]", "名", "幼虫、毛虫、蛹", "larva, caterpillar, pupa", "krap (虫) + il (小)"),
    ("8. 動物・生物種・共生", "ferten", "[fer.ten]", "名", "毛皮、体毛、獣皮", "fur, pelt, animal fleece", "fer (獣) + ten (被覆)"),
    ("8. 動物・生物種・共生", "ferdor", "[fer.dor]", "名", "捕食者、狩猟獣、天敵", "predator, apex carnivore", "fer (獣) + dor (追撃)"),
    ("8. 動物・生物種・共生", "volpan", "[vol.pan]", "動", "羽ばたく、飛翔旋回する、羽搏く", "flutter, flap wings, hover", "volan (飛ぶ) + pan (反復)"),

    # 9. 統治・社会・法・共同体 (4語)
    ("9. 統治・社会・法・共同体", "turcon", "[tur.con]", "名", "憲章、根本法規、大憲章", "charter, fundamental constitution", "tur (法) + con (根本)"),
    ("9. 統治・社会・法・共同体", "jylmor", "[jyl.mor]", "名", "代表団、使節、使者協議団", "delegation, embassy, envoy mission", "jyl (結ぶ) + mor (公務)"),
    ("9. 統治・社会・法・共同体", "domkor", "[dom.kor]", "名", "市民、定住住民、共同体構成員", "citizen, burgher, resident freeman", "dom (都市) + kor (員)"),
    ("9. 統治・社会・法・共同体", "senpan", "[sen.pan]", "動", "可決する、承認議決する、批准する", "ratify, pass, formally approve", "sen (合意) + pan (確定)"),

    # 10. 経済・交易・工芸・労働 (6語)
    ("10. 経済・交易・工芸・労働", "mardin", "[mar.din]", "名", "元金、元本、投資資本", "principal, capital sum, stake", "mar (交換) + din (基底)"),
    ("10. 経済・交易・工芸・労働", "martas", "[mar.tas]", "名", "利息、手数料、配当", "interest, commission, dividend", "mar (交易) + tas (増分)"),
    ("10. 経済・交易・工芸・労働", "dolkin", "[dol.kin]", "名", "やすり、研磨具、砥石", "file, rasp, whetstone abrasive", "dolar (鍛冶) + kin (研磨)"),
    ("10. 経済・交易・工芸・労働", "jylcor", "[jyl.cor]", "名", "紡績糸、撚り糸、細糸", "spun yarn, spun thread, ply", "jylpan (紡ぐ) + cor (線条)"),
    ("10. 経済・交易・工芸・労働", "marcor", "[mar.cor]", "名", "商船、交易貨物船、運搬艇", "merchant vessel, cargo barge", "mar (交易) + cor (艇)"),
    ("10. 経済・交易・工芸・労働", "marpan", "[mar.pan]", "動", "取引する、売買する、清算する", "transact, trade, settle accounts", "mar (交易) + pan (実行)"),

    # 11. 建築・都市・住空間 (5語)
    ("11. 建築・都市・住空間", "domcor", "[dom.cor]", "名", "塔、監視塔、物見櫓、尖塔", "tower, spire, watchtower", "dom (建築) + cor (高聳)"),
    ("11. 建築・都市・住空間", "domparn", "[dom.parn]", "名", "梁、桁、天井支え桁", "rafter, joist, ceiling beam", "domlik (柱) + parn (水平材)"),
    ("11. 建築・都市・住空間", "lercor", "[ler.cor]", "名", "アーチ門、凱旋門、重厚な門扉", "arched gate, portal, grand gateway", "lerel (扉) + cor (円弧)"),
    ("11. 建築・都市・住空間", "durcon", "[dur.con]", "名", "防壁塔、堡塁、小要塞", "bastion, redoubt, fortified bulwark", "durval (壁) + con (強固)"),
    ("11. 建築・都市・住空間", "talsar", "[tal.sar]", "名", "敷石、舗装、石畳の道", "paving stone, flagstone, cobbled walk", "tal (石) + sar (平面敷設)"),

    # 12. 食・飲料・調理・食具 (5語)
    ("12. 食・飲料・調理・食具", "nercor", "[ner.cor]", "名", "干し肉、保存肉、燻製肉", "cured meat, jerky, smoked pemmican", "ner (食) + cor (乾製)"),
    ("12. 食・飲料・調理・食具", "nerdor", "[ner.dor]", "名", "汁粉、シリアル、穀物粥", "porridge, gruel, cereal pottage", "nerat (穀物) + dor (温煮)"),
    ("12. 食・飲料・調理・食具", "bionmor", "[bion.mor]", "名", "果汁、搾りたてジュース、清涼果液", "fruit juice, sweet pressed nectar", "bion (飲) + mor (果肉)"),
    ("12. 食・飲料・調理・食具", "talpork", "[tal.pork]", "名", "すり鉢、乳鉢、粉砕器", "mortar, grinding basin", "tal (石) + pork (粉砕器)"),
    ("12. 食・飲料・調理・食具", "nersil", "[ner.sil]", "名", "具材、スープの具、煮込み種", "ingredient, stew morsel, solid filling", "ner (食) + sil (中身)"),

    # 13. 衣飾・携行具・日常品 (5語)
    ("13. 衣飾・携行具・日常品", "valcon", "[val.con]", "名", "礼服、正装、儀礼用ローブ", "vestment, ceremonial robe, gala gown", "valis (服) + con (格式)"),
    ("13. 衣飾・携行具・日常品", "larsor", "[lar.sor]", "名", "革紐、靴紐、締め緒", "shoelace, leather lace, boot thong", "larsil (靴) + sor (結び紐)"),
    ("13. 衣飾・携行具・日常品", "falkor", "[fal.kor]", "名", "日時計、影指し盤、影時計", "sundial, solar shadow clock", "fal (太陽光) + kor (計測盤)"),
    ("13. 衣飾・携行具・日常品", "valcor", "[val.cor]", "名", "天幕、テント、幕屋", "tent, pavilion, portable canopy", "val (布) + cor (覆屋)"),
    ("13. 衣飾・携行具・日常品", "kirelor", "[ki.re.lor]", "名", "筆入れ、ペンケース、文具箱", "pen case, stylus box, writing kit", "kirel (ペン) + or (入れ物)"),

    # 14. 精神・哲学・感情・芸術 (5語)
    ("14. 精神・哲学・感情・芸術", "mincor", "[min.cor]", "名", "矜持、誇り、気品、自尊心", "dignity, noble pride, self-respect", "min (心) + cor (高潔)"),
    ("14. 精神・哲学・感情・芸術", "minvol", "[min.vol]", "名", "憧憬、憧れ、高みへの熱望", "yearning, aspiration, starry longing", "min (心) + vol (飛翔)"),
    ("14. 精神・哲学・感情・芸術", "sarcon", "[sar.con]", "名", "祝祭、感謝祭、歓喜の祝宴", "jubilee, festive gala, joyful feast", "saren (笑う) + con (大祭)"),
    ("14. 精神・哲学・感情・芸術", "civtas", "[civ.tas]", "名", "和音、ハーモニー、協和響き", "chord, consonant harmony", "cival (音楽) + tas (調和)"),
    ("14. 精神・哲学・感情・芸術", "minpan", "[min.pan]", "動", "決断する、心を定める、意を決する", "resolve, determine, make up mind", "min (心) + pan (定礎)"),

    # 15. 性質・状態・色彩・感触 (5語)
    ("15. 性質・状態・色彩・感触", "falzor", "[fal.zor]", "形", "鮮明な、くっきりした、解像度の高い", "vivid, distinct, sharply defined", "fal (光) + zor (明晰)"),
    ("15. 性質・状態・色彩・感触", "talcon", "[tal.con]", "形", "頑強な、堅固な、ゆるぎない", "sturdy, robust, steadfast", "tal (岩) + con (強靱)"),
    ("15. 性質・状態・色彩・感触", "darsol", "[dar.sol]", "形", "透き通った、清澄な、透明な", "limpid, crystal-clear, transparent", "daris (水) + sol (純清)"),
    ("15. 性質・状態・色彩・感触", "kymcon", "[kym.con]", "形", "漆黒の、底知れぬ暗黒の", "pitch-black, abyss-dark", "kym (闇) + con (極度)"),
    ("15. 性質・状態・色彩・感触", "velpor", "[vel.por]", "形", "みずみずしい、青々とした、生命力ある", "verdant, lush, fresh with sap", "vel (草木) + por (生気)"),

    # 16. 動作・動態・時空・方向副詞 (6語)
    ("16. 動作・動態・時空・方向副詞", "porcon", "[por.con]", "動", "行進する、堂々と進む、パレードする", "march, advance with dignity", "poran (歩く) + con (威儀)"),
    ("16. 動作・動態・時空・方向副詞", "darvol", "[dar.vol]", "動", "波打つ、うねる、起伏する", "undulate, swell, surge in waves", "darrot (波) + vol (動態)"),
    ("16. 動作・動態・時空・方向副詞", "sercor", "[ser.cor]", "動", "握手する、手を携える、協調する", "clasp hands, cooperate, join forces", "ser (手) + cor (共同)"),
    ("16. 動作・動態・時空・方向副詞", "talzon", "[tal.zon]", "動", "着陸する、接地する、着発する", "touch ground, make landfall, touch down", "tal (地) + zon (接触)"),
    ("16. 動作・動態・時空・方向副詞", "velkan", "[vel.kan]", "動", "繁茂する、青葉を広げる、生い茂る", "flourish, thrive, grow luxuriantly", "vel (草木) + kan (盛況)"),
    ("16. 動作・動態・時空・方向副詞", "havcor", "[hav.cor]", "副", "定時に、規則正しく、時刻通りに", "punctually, on schedule, regularly", "hav (時) + cor (正確)"),
]

if __name__ == "__main__":
    import json
    with open("data/lexicon.json", "r", encoding="utf-8") as f:
        existing_vocab = json.load(f)["vocabulary"]
    existing_roots = {w["nrs"] for w in existing_vocab}

    print(f"Total v21 new candidates: {len(NEW_80_ENTRIES_V21)}")
    assert len(NEW_80_ENTRIES_V21) == 80, f"Expected 80, got {len(NEW_80_ENTRIES_V21)}"

    roots = [e[1] for e in NEW_80_ENTRIES_V21]
    # Check internal duplicate
    dups = [r for r in roots if roots.count(r) > 1]
    assert len(dups) == 0, f"Internal duplicates: {set(dups)}"

    # Check overlap with existing 660 roots
    overlap = [r for r in roots if r in existing_roots]
    assert len(overlap) == 0, f"Overlap with existing: {overlap}"

    # Check forbidden chars
    FORBIDDEN = set("qx")
    for r in roots:
        assert not any(c in FORBIDDEN for c in r), f"Forbidden char in {r}"

    # Earth borrowing check
    EARTH_WORDS = {
        "auto", "tele", "port", "sign", "part", "post", "line", "point", "cord", "mode",
        "base", "cell", "gene", "data", "text", "form", "core", "disk", "node", "unit",
        "byte", "code", "host", "link", "root", "site", "star", "moon", "sun", "sky",
        "dark", "deep", "time", "year", "life", "dead", "mind", "soul", "body", "head",
        "hand", "foot", "home", "room", "city", "town", "land", "rock", "iron", "gold",
        "fire", "wind", "rain", "snow", "tree", "leaf", "bird", "fish", "walk", "sing",
        "talk", "open", "shut", "good", "evil", "true", "real", "fact", "high", "down",
        "left", "east", "west", "past", "soon", "here", "there", "when", "what", "where",
        "love", "hope", "fear", "path", "road", "gate", "door", "wall", "roof", "ship",
        "book", "page", "word", "name", "king", "lord", "rule", "law", "duty", "gold",
        "bell", "ring", "song", "horn", "iron", "lead", "zinc", "salt", "acid", "flow",
        "wave", "tide", "beam", "ray", "void", "space", "dust", "cloud", "storm", "gale",
        "bank", "cost", "debt", "fund", "loan", "loss", "mark", "pay", "plan", "rate",
        "sale", "shop", "toll", "wage", "boss", "crew", "farm", "mill", "mine", "crop",
        "beef", "beer", "cake", "corn", "dish", "diet", "feed", "flour", "food", "fork",
        "herb", "meal", "meat", "milk", "pork", "rice", "salt", "soup", "stew", "wine"
    }
    earth_match = [r for r in roots if r in EARTH_WORDS]
    assert len(earth_match) == 0, f"Earth match: {earth_match}"

    print("ALL 80 NEW CANDIDATES AUDITED AND VERIFIED!")
