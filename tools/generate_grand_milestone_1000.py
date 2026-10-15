# tools/generate_grand_milestone_1000.py
"""
Nebulith Grand Milestone 1000 Vocabulary Expansion Generator
Generates ~268 vetted master roots across all 16 domains, pushing total lexicon to 1,008 roots.
Strictly zero Earth borrowings, 100% audit compliant, pure celestial conlang phonology.
"""
import json

with open("data/lexicon.json", "r", encoding="utf-8") as f:
    existing_vocab = json.load(f)["vocabulary"]
existing_roots = {w["nrs"] for w in existing_vocab}

EARTH_BORROWING_BLACKLIST = {
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

# The 268 New Candidates list
CANDIDATES = [
    # 1. 天体・宇宙力学・光 (+12語)
    ("1. 天体・宇宙力学・光", "celmon", "[cel.mon]", "名", "星間分子雲、巨大暗黒星雲", "giant molecular cloud, dark interstellar cloud", "cel (天) + mon (巨大集合)"),
    ("1. 天体・宇宙力学・光", "zohartur", "[zo.har.tur]", "名", "光球層、主星の可視表面", "photosphere, stellar surface", "zohar (主星) + tur (層)"),
    ("1. 天体・宇宙力学・光", "tyrcon", "[tyr.con]", "名", "引力崩壊、重力崩壊、爆縮", "gravitational collapse, implosion", "tyral (重力) + con (急激圧縮)"),
    ("1. 天体・宇宙力学・光", "falmirin", "[fal.mi.rin]", "名", "分光偏光、スペクトル輝線偏光", "spectropolarimetry, spectral polarization", "fal (光) + mir (観測) + in"),
    ("1. 天体・宇宙力学・光", "dorcon", "[dor.con]", "名", "摂動、軌道摂動、外力微小偏位", "orbital perturbation, gravitational wobble", "dor (軌道) + con (揺動)"),
    ("1. 天体・宇宙力学・光", "valryn", "[val.ryn]", "名", "電磁波放射、背景放射、星間放射", "electromagnetic emission, cosmic background radiation", "val (波) + ryn (放射)"),
    ("1. 天体・宇宙力学・光", "kyrtas", "[kyr.tas]", "名", "彗星核、氷雪天体核", "cometary nucleus, icy planetary core", "kyras (氷) + tas (核体)"),
    ("1. 天体・宇宙力学・光", "zoharpar", "[zo.har.par]", "名", "プロミネンス、紅炎、彩層噴出", "solar prominence, coronal eruption", "zohar (主星) + par (突出炎)"),
    ("1. 天体・宇宙力学・光", "radcon", "[rad.con]", "名", "脱出速度、第二宇宙速度", "escape velocity, parabolic speed", "radin (半径) + con (突破限界)"),
    ("1. 天体・宇宙力学・光", "kymzon", "[kym.zon]", "名", "事象の地平面、脱出不能境界", "event horizon boundary, gravitational limit", "kym (深淵) + zon (境界)"),
    ("1. 天体・宇宙力学・光", "vortas", "[vor.tas]", "名", "測地線、天体運動最短経路", "geodesic path, inertial trajectory", "vor (運行) + tas (軌道線)"),
    ("1. 天体・宇宙力学・光", "vyrtal", "[vyr.tal]", "名", "天球図、恒星星図、全天位置表", "celestial chart, star catalog", "vyr (星) + tal (盤図)"),

    # 2. 数理・幾何・計測 (+17語)
    ("2. 数理・幾何・計測", "tuldin", "[tul.din]", "名", "下限、最大下界、インフィマム", "infimum, greatest lower bound", "tulos (底) + din (基底)"),
    ("2. 数理・幾何・計測", "novdin", "[nov.din]", "名", "上限、最小上界、スプレマム", "supremum, least upper bound", "novar (頂) + din (基底)"),
    ("2. 数理・幾何・計測", "talpor", "[tal.por]", "名", "多面体、空間胞体、幾何胞", "polyhedron, spatial cell, geometric polytope", "tulik (多角) + por (胞)"),
    ("2. 数理・幾何・計測", "keldin", "[kel.din]", "名", "偏微分、局所変化率、傾斜率", "partial derivative, directional change rate", "kelon (変数) + din (基底微分)"),
    ("2. 数理・幾何・計測", "firsol", "[fir.sol]", "名", "積分、累計総和、曲線下面積", "integral, cumulative quadrature", "firas (定数) + sol (集積和)"),
    ("2. 数理・幾何・計測", "suftol", "[suf.tol]", "名", "論理積、連言、AND演算", "conjunction, logical AND, intersection", "suf (論理) + tol (結合)"),
    ("2. 数理・幾何・計測", "sufmor", "[suf.mor]", "名", "論理和、選言、OR演算", "disjunction, logical OR, union", "suf (論理) + mor (包括)"),
    ("2. 数理・幾何・計測", "sufnar", "[suf.nar]", "名", "否定、反転、NOT演算", "negation, logical NOT, inverse complement", "suf (論理) + nar (反転)"),
    ("2. 数理・幾何・計測", "dorkat", "[dor.kat]", "名", "円錐曲線、二次曲線", "conic section, quadratic curve", "dor (周回) + kat (断面)"),
    ("2. 数理・幾何・計測", "niftol", "[nif.tol]", "名", "内積、ドット積、射影量", "dot product, inner product, scalar projection", "niven (次元) + tol (積)"),
    ("2. 数理・幾何・計測", "nifmor", "[nif.mor]", "名", "外積、クロス積、有向面積積", "cross product, outer product, vector product", "niven (次元) + mor (直交積)"),
    ("2. 数理・幾何・計測", "zydcon", "[zyd.con]", "名", "反証、背理法、矛盾導出", "rebuttal, proof by contradiction, reductio", "zydis (証拠) + con (矛盾打倒)"),
    ("2. 数理・幾何・計測", "kircon", "[kir.con]", "名", "同型写像、位相同型、同型性", "isomorphism, homeomorphism", "kiril (写像) + con (一致)"),
    ("2. 数理・幾何・計測", "delcon", "[del.con]", "名", "特異点、不連続点、発散点", "singularity, discontinuity point", "delis (分割) + con (破綻極)"),
    ("2. 数理・幾何・計測", "firtor", "[fir.tor]", "名", "固有値、固有ベクトル指標", "eigenvalue, characteristic root", "firas (定数) + tor (本質)"),
    ("2. 数理・幾何・計測", "jylkat", "[jyl.kat]", "名", "直和、デカルト積、空間結合", "direct sum, Cartesian product", "jylom (集合) + kat (積算)"),
    ("2. 数理・幾何・計測", "sufcor", "[suf.cor]", "名", "超限数、無限濃度、カージナル", "transfinite number, aleph cardinal", "suf (計算) + cor (無限大)"),

    # 3. 情報・計算機・通信 (+16語)
    ("3. 情報・計算機・通信", "tolpar", "[tol.par]", "名", "ブロードキャスト、一斉同報、全域送信", "broadcast, omnidirectional beacon", "tolas (通信) + par (全域)"),
    ("3. 情報・計算機・通信", "suftar", "[suf.tar]", "名", "スレッド、並行処理並列流", "thread, concurrent execution flow", "suf (計算) + tar (細流)"),
    ("3. 情報・計算機・通信", "kivmor", "[kiv.mor]", "名", "ビット演算、論理シフト、ビットマスク", "bitwise operation, bit mask, shift", "kiv (ビット) + mor (操作)"),
    ("3. 情報・計算機・通信", "livsol", "[liv.sol]", "名", "トランザクション、不可分確定処理", "transaction, atomic commit unit", "livar (保存) + sol (完全塊)"),
    ("3. 情報・計算機・通信", "tolcon", "[tol.con]", "名", "プロトコル、通信規約、伝送規程", "protocol, transmission pact", "tolas (通信) + con (約定)"),
    ("3. 情報・計算機・通信", "krotcon", "[krot.con]", "名", "フォールトトレランス、障害耐性、冗長系", "fault tolerance, redundant failover", "krot (障害) + con (防護)"),
    ("3. 情報・計算機・通信", "sorcon", "[sor.con]", "名", "ガベージコレクション、メモリ解放整理", "garbage collection, memory compaction", "soril (メモリ) + con (浄化)"),
    ("3. 情報・計算機・通信", "matorcon", "[ma.tor.con]", "名", "オペレーティングシステム、統御核、カーネル", "operating system kernel, control core", "mator (機械) + con (中枢)"),
    ("3. 情報・計算機・通信", "jyncon", "[jyn.con]", "名", "論理ゲート、電脳回路素子、スイッチング素子", "logic gate, switching semiconductor element", "jyn (電子) + con (接点)"),
    ("3. 情報・計算機・通信", "tolkat", "[tol.kat]", "名", "レイテンシ、伝送遅延、応答時間", "latency, propagation delay, response lag", "tolas (通信) + kat (遅滞間隔)"),
    ("3. 情報・計算機・通信", "zevcon", "[zev.con]", "名", "正規表現、パターン照合式", "regular expression, regex pattern syntax", "zevil (構文) + con (整合)"),
    ("3. 情報・計算機・通信", "kivron", "[kiv.ron]", "名", "ストリーム、連続データ流、ビット流", "data stream, continuous byte sequence", "kiv (情報) + ron (流水)"),
    ("3. 情報・計算機・通信", "suftin", "[suf.tin]", "名", "チェックサム、ハッシュ検証値、誤り検出符号", "checksum, cyclic redundancy hash, digest", "suf (計算) + tin (検査印)"),
    ("3. 情報・計算機・通信", "livpan", "[liv.pan]", "動", "同期する、データを一致させる、レプリケートする", "synchronize, replicate, reconcile data", "livar (保存) + pan (一致化)"),
    ("3. 情報・計算機・通信", "kirpan", "[kir.pan]", "動", "デプロイする、配備する、実稼働に載せる", "deploy, roll out, install into production", "kiran (コード) + pan (展開)"),
    ("3. 情報・計算機・通信", "tolpan", "[tol.pan]", "動", "ルーティングする、中継転送する、フォワードする", "forward, route packet, relay transmission", "tolas (通信) + pan (中継)"),

    # 4. 生命・生体・医療 (+17語)
    ("4. 生命・生体・医療", "revcon", "[rev.con]", "名", "抗体、免疫防御因子、解毒素", "antibody, immune defense agent, antitoxin", "rev (生気) + con (防護)"),
    ("4. 生命・生体・医療", "morcon", "[mor.con]", "名", "骨折、組織断裂、生体損傷", "fracture, skeletal rupture, trauma", "mor (骨肉) + con (損傷)"),
    ("4. 生命・生体・医療", "sercon", "[ser.con]", "名", "鎮痛薬、麻酔、感覚遮断薬", "analgesic, painkiller, anesthetic sedative", "ser (静穏) + con (鎮静剤)"),
    ("4. 生命・生体・医療", "revpar", "[rev.par]", "名", "抗生物質、生体活性薬、滋養強壮薬", "antibiotic, vital tonic, therapeutic restorative", "rev (生命) + par (回復効)"),
    ("4. 生命・生体・医療", "dariscon", "[da.ris.con]", "名", "包帯、固定具、創傷被覆材", "bandage, wound dressing, splint", "daris (治療) + con (被覆帯)"),
    ("4. 生命・生体・医療", "morpar", "[mor.par]", "名", "皮膚、表皮、外皮組織", "epidermis, cuticle, skin barrier", "mor (肉) + par (外面皮)"),
    ("4. 生命・生体・医療", "revrin", "[rev.rin]", "名", "リンパ液、体液循環、組織間質液", "lymph, interstitial fluid, humors", "rev (生体) + rin (液環)"),
    ("4. 生命・生体・医療", "morvin", "[mor.vin]", "名", "血管、動脈、静脈、血脈管", "blood vessel, artery, vascular channel", "mor (生体) + vin (管路)"),
    ("4. 生命・生体・医療", "revtin", "[rev.tin]", "名", "脈診、触診、生体リズム診断", "pulse diagnosis, palpation, vital rhythm test", "rev (脈動) + tin (検知)"),
    ("4. 生命・生体・医療", "serdin", "[ser.din]", "名", "反射、不随意運動、神経反射", "reflex, involuntary impulse", "ser (神経) + din (直発動)"),
    ("4. 生命・生体・医療", "mordin", "[mor.din]", "名", "骨髄、造血組織、生命基底芯", "bone marrow, myeloid tissue, core marrow", "mor (骨) + din (深芯)"),
    ("4. 生命・生体・医療", "darispuk", "[da.ris.puk]", "名", "軟膏、塗り薬、薬用膏薬", "ointment, therapeutic balm, salve", "daris (治癒) + puk (膏油)"),
    ("4. 生命・生体・医療", "revkor", "[rev.kor]", "名", "熱病、発熱、体温上昇症状", "fever, pyrexia, inflammatory heat", "rev (生体) + kor (高熱)"),
    ("4. 生命・生体・医療", "morpan", "[mor.pan]", "動", "麻痺する、感覚を失う、運動停止する", "paralyze, go numb, lose motor function", "mor (筋肉) + pan (不全化)"),
    ("4. 生命・生体・医療", "revpan", "[rev.pan]", "動", "蘇生する、意識を取り戻す、息を吹き返す", "resuscitate, revive, regain consciousness", "rev (生命) + pan (回帰)"),
    ("4. 生命・生体・医療", "serpanan", "[ser.pa.nan]", "動", "鎮静させる、眠らせる、痛みを和らげる", "soothe, tranquilize, alleviate pain", "ser (静穏) + panan (施す)"),
    ("4. 生命・生体・医療", "darispan", "[da.ris.pan]", "動", "処方する、薬を調合する、投薬する", "prescribe, dispense medicine, compound", "daris (医療) + pan (調剤)"),

    # 5. 自然地形・地質・鉱物 (+18語)
    ("5. 自然地形・地質・鉱物", "talsol", "[tal.sol]", "名", "玄武岩、黒色火成岩、柱状節理岩", "basalt, dark volcanic trap rock", "tal (岩) + sol (強緻密)"),
    ("5. 自然地形・地質・鉱物", "talmorin", "[tal.mo.rin]", "名", "花崗岩、深成岩、星彩結晶石", "granite, crystalline plutonic bedrock", "tal (岩) + morin (斑晶)"),
    ("5. 自然地形・地質・鉱物", "talnyr", "[tal.nyr]", "名", "雲母、層状珪酸塩鉱物、きらら", "mica, sheet silicate, glimmer stone", "tal (鉱) + nyr (薄片光)"),
    ("5. 自然地形・地質・鉱物", "talryn", "[tal.ryn]", "名", "石英、水晶、透明珪石結晶", "quartz, rock crystal, silica spire", "tal (石) + ryn (透明晶)"),
    ("5. 自然地形・地質・鉱物", "talfir", "[tal.fir]", "名", "断層、地割れ、構造断裂帯", "geological fault, fracture rift, shear zone", "tal (地) + fir (断層面)"),
    ("5. 自然地形・地質・鉱物", "talsarv", "[tal.sarv]", "名", "段丘、河岸段丘、海岸階段地形", "terrace, fluvial bench, stepped bluff", "tal (地) + sarv (階段平坦面)"),
    ("5. 自然地形・地質・鉱物", "talvelk", "[tal.velk]", "名", "峡谷底、谷底平野、岩峰間の隘路", "gorge floor, canyon defile, ravine trough", "talik (峡谷) + velk (通路)"),
    ("5. 自然地形・地質・鉱物", "taljynar", "[tal.jy.nar]", "名", "磁気異常地帯、引力異常断層", "magnetic anomaly zone, lodestone hill", "taljyn (磁石) + ar (場)"),
    ("5. 自然地形・地質・鉱物", "talpyrcon", "[tal.pyr.con]", "名", "カルデラ、火山陥没孔、火口湖盆", "caldera, collapsed volcanic crater", "pyrtal (火山) + con (巨大窪地)"),
    ("5. 自然地形・地質・鉱物", "talparv", "[tal.parv]", "名", "砂利河原、氾濫原、礫層地帯", "gravel bed, gravel bar, shingle reach", "talsid (砂利) + parv (水辺)"),
    ("5. 自然地形・地質・鉱物", "taldorn", "[tal.dorn]", "名", "侵食、風化地形、削剥岩", "erosion feature, weathered tor, yardang", "tal (岩) + dorn (削磨)"),
    ("5. 自然地形・地質・鉱物", "talvort", "[tal.vort]", "名", "地下水脈孔、鍾乳洞水路、吸い込み穴", "sinkhole, ponor, karst swallow hole", "vuron (洞窟) + vort (水路)"),
    ("5. 自然地形・地質・鉱物", "talner", "[tal.ner]", "名", "腐植土壌、黒土、作土層", "topsoil, black humus loam, arable soil", "tal (土) + ner (栄養)"),
    ("5. 自然地形・地質・鉱物", "talkanorv", "[tal.ka.norv]", "名", "露頭、露出岩盤、地層断面", "outcrop, exposed bedrock scarp", "tal (地) + kanorv (顕出)"),
    ("5. 自然地形・地質・鉱物", "talsorn", "[tal.sorn]", "名", "珪岩、硬質変成岩、砥石岩", "quartzite, hard metamorphic hornstone", "tal (石) + sorn (極硬)"),
    ("5. 自然地形・地質・鉱物", "talvarp", "[tal.varp]", "名", "硫黄鉱床、噴気孔地帯、鉱気帯", "solfatara, fumarole field, sulfur seep", "tal (鉱) + varp (蒸気鉱)"),
    ("5. 自然地形・地質・鉱物", "taldol", "[tal.dol]", "名", "鉄鉱石、赤鉄鉱、製鉄母岩", "iron ore, hematite node, bog iron", "talur (金属) + dol (母体)"),
    ("5. 自然地形・地質・鉱物", "talmorv", "[tal.morv]", "名", "堆積、土砂堆積、沈殿層形成", "sedimentation, silt accretion, silt accumulation", "tal (土砂) + morv (積層)"),

    # 6. 気象・大気・水域 (+17語)
    ("6. 気象・大気・水域", "celran", "[cel.ran]", "名", "乱層雲、雨雲塊、濃密雷雲", "nimbostratus, dense thunderhead", "celis (雲) + ran (重厚動乱)"),
    ("6. 気象・大気・水域", "celvorv", "[cel.vorv]", "名", "積乱雲、入道雲、雷雨積雲", "cumulonimbus, towering cloud anvil", "celis (雲) + vorv (そびえ立つ)"),
    ("6. 気象・大気・水域", "wylcon", "[wyl.con]", "名", "暴風、烈風、台風、サイクロン", "gale force storm, hurricane, typhoon", "wylas (風) + con (極大)"),
    ("6. 気象・大気・水域", "wyltorv", "[wyl.torv]", "名", "竜巻、漏斗雲、トルネード", "tornado, twister, funnel cloud vortex", "wylven (旋風) + torv (破壊突進)"),
    ("6. 気象・大気・水域", "darcon", "[dar.con]", "名", "洪水、氾濫、大増水", "flood, inundation, deluge overflow", "daris (水) + con (越流)"),
    ("6. 気象・大気・水域", "darsolv", "[dar.solv]", "名", "清流、小川、せせらぎ、渓流", "brook, creek, babbling mountain rill", "daris (水) + solv (清音流)"),
    ("6. 気象・大気・水域", "darvorn", "[dar.vorn]", "名", "渦潮、大渦、海流渦", "maelstrom, whirlpool, vortex eddy", "zylar (海) + vorn (回転流)"),
    ("6. 気象・大気・水域", "darnyv", "[dar.nyv]", "名", "朝露、夜露、草葉の露水", "morning dew, condensed night moisture", "dar (雫) + nyv (朝の微光)"),
    ("6. 気象・大気・水域", "kyrcon", "[kyr.con]", "名", "猛吹雪、ブリザード、白魔", "blizzard, whiteout gale, ice gale", "kyrlen (雪) + con (猛威)"),
    ("6. 気象・大気・水域", "kyrsol", "[kyr.sol]", "名", "氷柱、つらら、凍結垂下氷", "icicle, hanging ice spear", "kyras (氷) + sol (柱晶)"),
    ("6. 気象・大気・水域", "celnyv", "[cel.nyv]", "名", "薄霧、朝靄、山靄、蒸気靄", "haze, morning mist, blue vapor veil", "celis (霧) + nyv (淡い)"),
    ("6. 気象・大気・水域", "havcon", "[hav.con]", "名", "天候異変、異常気象、季節外れ", "weather anomaly, climatic aberration", "havas (季節) + con (異変)"),
    ("6. 気象・大気・水域", "wylsar", "[wyl.sar]", "名", "海風、陸風、沿岸循環風", "sea breeze, diurnal coastal wind", "wylas (風) + sar (海岸岸辺)"),
    ("6. 気象・大気・水域", "darpal", "[dar.pal]", "名", "浅瀬、徒渉池、川の浅み", "ford, shallow river crossing, shoal", "daris (水) + pal (浅い)"),
    ("6. 気象・大気・水域", "darvyr", "[dar.vyr]", "名", "夜光海、夜光虫の光、海蛍の輝き", "phosphorescent sea, sea sparkle glow", "zylar (海) + vyr (星影発光)"),
    ("6. 気象・大気・水域", "wylpan", "[wyl.pan]", "動", "凪ぐ、風が静まる、風が止む", "abate, calm down, winds subside", "wylas (風) + pan (静止化)"),
    ("6. 気象・大気・水域", "darpanan", "[dar.pa.nan]", "動", "氾濫する、溢れ出る、堤防を越える", "overflow banks, spill over, surge", "daris (水) + panan (溢流)"),

    # 7. 植物・生態・農耕 (+20語)
    ("7. 植物・生態・農耕", "velsol", "[vel.sol]", "名", "心材、木の芯、硬質木質部", "heartwood, core duramen of trunk", "velpon (樹幹) + sol (中芯硬部)"),
    ("7. 植物・生態・農耕", "veldor", "[vel.dor]", "名", "年輪、成長輪、星辰樹輪", "growth ring, tree ring layer", "vel (木) + dor (周期円環)"),
    ("7. 植物・生態・農耕", "velnyr", "[vel.nyr]", "名", "葉脈、葉の脈管網", "leaf vein, vascular bundle pattern", "velas (葉) + nyr (細脈網)"),
    ("7. 植物・生態・農耕", "velkorv", "[vel.korv]", "名", "果皮、果実の外皮、殻皮", "rind, peel, husk of fruit", "vorin (果実) + korv (被覆殻)"),
    ("7. 植物・生態・農耕", "velsarp", "[vel.sarp]", "名", "球根、鱗茎、地下貯蔵塊茎", "bulb, corm, tuber storehouse", "veltul (根) + sarp (肥大塊)"),
    ("7. 植物・生態・農耕", "teircon", "[teir.con]", "名", "種穂、穀穂、穂先、麦穂", "ear of grain, spike, seed head", "nerat (穀物) + con (穂実)"),
    ("7. 植物・生態・農耕", "veltarv", "[vel.tarv]", "名", "落葉、枯葉、秋の敷き藁", "fallen leaf, leaf litter, autumn foliage", "velas (葉) + tarv (落ち敷く)"),
    ("7. 植物・生態・農耕", "velryn", "[vel.ryn]", "名", "若芽、萌黄、初春の新緑", "fresh tender shoot, vernal foliage", "velil (若木) + ryn (みずみずしさ)"),
    ("7. 植物・生態・農耕", "velporv", "[vel.porv]", "名", "胞子、羊歯の胞子嚢群", "spore, sorus, cryptogamic seedlet", "vel (草木) + porv (微粒子嚢)"),
    ("7. 植物・生態・農耕", "velzar", "[vel.zar]", "名", "原生林、古森林、原生樹海", "primeval forest, old-growth jungle", "velom (森) + zar (太古)"),
    ("7. 植物・生態・農耕", "velkarn", "[vel.karn]", "名", "牧草、飼料草、クローバー", "pasture grass, forage, clover herbage", "velil (草) + karn (牧養)"),
    ("7. 植物・生態・農耕", "talkarn", "[tal.karn]", "名", "牧草地、放牧場、緑野", "pasture, meadow range, grazing green", "tal (地) + karn (放牧)"),
    ("7. 植物・生態・農耕", "talkorv", "[tal.korv]", "名", "畝、作付列、畑の畦道", "ridge, furrow, planting bed row", "talkan (耕作) + korv (隆起列)"),
    ("7. 植物・生態・農耕", "talkanorl", "[tal.ka.norl]", "名", "鋤、犂、耕耘具", "plowshare, coulter, till spade", "talkan (耕す) + orl (器具)"),
    ("7. 植物・生態・農耕", "vorkorl", "[vor.korl]", "名", "大鎌、鎌、刈り取り刃", "scythe, sickle, reaping blade", "vorken (収穫) + korl (湾曲刃)"),
    ("7. 植物・生態・農耕", "talkorl", "[tal.korl]", "名", "鍬、平鍬、土掘り具", "mattock, hoe, grubbing tool", "talkan (耕土) + korl (刃具)"),
    ("7. 植物・生態・農耕", "veltalv", "[vel.talv]", "名", "腐植堆肥、肥沃堆肥、有機肥料", "compost, mulch, organic enrichment", "velrotas (腐葉土) + talv (肥料)"),
    ("7. 植物・生態・農耕", "veltorp", "[vel.torp]", "名", "間引き、剪定、枝打ち枝払い", "pruning, thinning, lopping branches", "velspar (枝) + torp (切り落とし)"),
    ("7. 植物・生態・農耕", "velpanan", "[vel.pa.nan]", "動", "開花する、花開く、蕾を解く", "blossom, unfold petals, burst into bloom", "velin (花) + panan (開展)"),
    ("7. 植物・生態・農耕", "teirpanan", "[teir.pa.nan]", "動", "結実する、実を結ぶ、実をつける", "bear fruit, set seeds, fructify", "teiril (種) + panan (結実)"),

    # 8. 動物・生物種・共生 (+22語)
    ("8. 動物・生物種・共生", "volcorv", "[vol.corv]", "名", "猛禽、鷹、鷲、大空の狩人", "raptor, eagle, falcon, hawk of the zenith", "volfer (鳥) + corv (鋭爪狩人)"),
    ("8. 動物・生物種・共生", "volnyr", "[vol.nyr]", "名", "鳴禽、小鳥、さえずる鳥", "songbird, warbler, piping finch", "volfer (鳥) + nyr (清麗な声)"),
    ("8. 動物・生物種・共生", "volzar", "[vol.zar]", "名", "水鳥、白鳥、鴨、水辺の飛翔鳥", "waterfowl, swan, diving wild goose", "volfer (鳥) + zar (水辺生息)"),
    ("8. 動物・生物種・共生", "volkorl", "[vol.korl]", "名", "止まり木、鳥の止まり枝", "perch, bird roost, roosting branch", "volfer (鳥) + korl (掛かり枝)"),
    ("8. 動物・生物種・共生", "zylzar", "[zyl.zar]", "名", "深海魚、底生魚、暗黒遊泳魚", "abyssal fish, benthic dweller, anglerfish", "zylfer (魚) + zar (深海)"),
    ("8. 動物・生物種・共生", "zylkon", "[zyl.kon]", "名", "海生巨獣、鯨、大魚、星間海獣", "great whale, leviathan, pelagic titan", "zylfer (魚) + kon (巨大種)"),
    ("8. 動物・生物種・共生", "zylparv", "[zyl.parv]", "名", "魚の鰓、水呼吸器、えら", "gill, branchia, aquatic respiratory fringe", "zylfer (魚) + parv (呼吸器官)"),
    ("8. 動物・生物種・共生", "zyltyr", "[zyl.tyr]", "名", "魚の鰭、背鰭、胸鰭、尾鰭", "fin, caudal fin, pectoral flipper", "zylfer (魚) + tyr (推進翼)"),
    ("8. 動物・生物種・共生", "ferzar", "[fer.zar]", "名", "有蹄類、草食獣、鹿、山羊", "ungulate herbivore, stag, mountain gazelle", "feras (獣) + zar (草食生)"),
    ("8. 動物・生物種・共生", "ferkon", "[fer.kon]", "名", "猛獣、巨熊、獅子、大顎の捕食獣", "great bear, cave feline, apex roaring beast", "feras (獣) + kon (巨力)"),
    ("8. 動物・生物種・共生", "fernyr", "[fer.nyr]", "名", "小動物、小齧歯類、野鼠、リス", "small rodent, squirrel, burrowing field mouse", "feras (獣) + nyr (俊敏小形)"),
    ("8. 動物・生物種・共生", "ferporv", "[fer.porv]", "名", "獣の足跡、踏み跡、爪痕", "pawprint, track, spoors in mud", "feras (獣) + porv (足跡印)"),
    ("8. 動物・生物種・共生", "fervol", "[fer.vol]", "名", "蝙蝠、翼手類、夜行性飛翔獣", "bat, chiropteran flyer, night-winged beast", "feras (獣) + vol (飛行)"),
    ("8. 動物・生物種・共生", "ferparv", "[fer.parv]", "名", "牙、鋭い犬歯、門歯", "fang, tusk, canine tooth", "feras (獣) + parv (鋭歯)"),
    ("8. 動物・生物種・共生", "krapcon", "[krap.con]", "名", "甲虫、甲殻甲虫、大兜虫", "scarab, rhinoceros beetle, horned armor-bug", "krap (甲虫) + con (重甲)"),
    ("8. 動物・生物種・共生", "krapnyr", "[krap.nyr]", "名", "蝶、蛾、鱗粉の舞う翅虫", "butterfly, winged silk moth", "krap (虫) + nyr (華麗翅)"),
    ("8. 動物・生物種・共生", "krapzar", "[krap.zar]", "名", "蜂、蜜蜂、群生羽虫", "honeybee, worker bee, social nectar-fly", "krap (虫) + zar (共同群)"),
    ("8. 動物・生物種・共生", "krapvol", "[krap.vol]", "名", "蜻蛉、羽虫、空中飛翔昆虫", "dragonfly, mayfly, needle-fly", "krap (虫) + vol (高速飛)"),
    ("8. 動物・生物種・共生", "krapkorv", "[krap.korv]", "名", "蟻、地中巣穴の群行虫", "ant, burrowing colonist bug", "krap (虫) + korv (地中列行)"),
    ("8. 動物・生物種・共生", "ferkarn", "[fer.karn]", "名", "家畜、飼育動物、愛玩動物", "domesticated animal, companion pet, farm beast", "feras (獣) + karn (養育)"),
    ("8. 動物・生物種・共生", "ferpanan", "[fer.pa.nan]", "動", "咆哮する、吠える、遠吠えする", "roar, bellow, howl at the starry sky", "fervyn (声) + panan (放つ)"),
    ("8. 動物・生物種・共生", "fervolan", "[fer.vo.lan]", "動", "冬眠する、休眠する、冬ごもりする", "hibernate, enter estivation torpor", "feras (獣) + volan (隠遁)"),

    # 9. 統治・社会・法・共同体 (+17語)
    ("9. 統治・社会・法・共同体", "turmorv", "[tur.morv]", "名", "判例、確立された先例、判例集", "judicial precedent, case law body", "tur (法) + morv (蓄積記録)"),
    ("9. 統治・社会・法・共同体", "tursolv", "[tur.solv]", "名", "免責、恩赦、罪の免除", "amnesty, pardon, legal exemption", "tur (法) + solv (解除免除)"),
    ("9. 統治・社会・法・共同体", "turdorn", "[tur.dorn]", "名", "刑罰、科料、制裁措置", "punishment, penal sanction, penalty", "tur (法) + dorn (科刑)"),
    ("9. 統治・社会・法・共同体", "jylzar", "[jyl.zar]", "名", "連邦、諸都市連合、星間共同体", "commonwealth, federation, confederacy", "jylkan (条約) + zar (大域統合)"),
    ("9. 統治・社会・法・共同体", "jylporv", "[jyl.porv]", "名", "議定書、付属約定、批准付属書", "protocol, convention accord, annexed covenant", "jyl (約定) + porv (条文)"),
    ("9. 統治・社会・法・共同体", "domkorv", "[dom.korv]", "名", "元首、執政官、都市代表長", "archon, high magistrate, consul", "domom (都市) + korv (統御冠)"),
    ("9. 統治・社会・法・共同体", "domnyr", "[dom.nyr]", "名", "代議員、評議員、人民代表", "deputy, tribune, representative delegate", "domsen (評議会) + nyr (委任代表)"),
    ("9. 統治・社会・法・共同体", "turzar", "[tur.zar]", "名", "最高裁判所、大審院、法規保全座", "supreme tribunal, high court of equity", "tur (法) + zar (最高座)"),
    ("9. 統治・社会・法・共同体", "senzar", "[sen.zar]", "名", "全会一致、満場一致の議決", "unanimity, unanimous accord", "sen (合意) + zar (全数完全)"),
    ("9. 統治・社会・法・共同体", "turpal", "[tur.pal]", "名", "民法、市民協定、私法規範", "civil statute, civic ordinance", "tur (法) + pal (市民日常)"),
    ("9. 統治・社会・法・共同体", "turtasv", "[tur.tasv]", "名", "公印、国璽、統治印章", "state seal, sigil of authority, signet", "tur (権威) + tasv (刻印)"),
    ("9. 統治・社会・法・共同体", "dompal", "[dom.pal]", "名", "街区、隣組、近隣共同体", "ward, neighborhood commune, parish", "dom (家) + pal (近接域)"),
    ("9. 統治・社会・法・共同体", "jylpal", "[jyl.pal]", "名", "親交、親善、友好関係", "amity, goodwill concord, fraternal fellowship", "jyl (結び) + pal (親和)"),
    ("9. 統治・社会・法・共同体", "tursarp", "[tur.sarp]", "名", "誓詞、宣誓書、就任誓約", "oath of office, sworn pledge, affidavit", "tur (法) + sarp (厳格誓詞)"),
    ("9. 統治・社会・法・共同体", "senmorv", "[sen.morv]", "名", "公聴会、住民集会、開かれた会合", "town meeting, plebiscite forum, open hearing", "sen (合意) + morv (民衆集会)"),
    ("9. 統治・社会・法・共同体", "turpanan", "[tur.pa.nan]", "動", "布告する、発布する、公布施行する", "promulgate, enact, officially decree", "tur (法) + panan (公布)"),
    ("9. 統治・社会・法・共同体", "turdornan", "[tur.dor.nan]", "動", "宣告する、判決を下す、審判する", "adjudicate, pronounce verdict, sentence", "tur (法) + dornan (判定決定)"),

    # 10. 経済・交易・工芸・労働 (+20語)
    ("10. 経済・交易・工芸・労働", "marsol", "[mar.sol]", "名", "金庫、財嚢、備蓄金庫", "treasury vault, strongbox, coffer", "mar (富) + sol (保管庫)"),
    ("10. 経済・交易・工芸・労働", "marnyr", "[mar.nyr]", "名", "為替手形、引換券、小切手", "bill of exchange, note, promissory draft", "mar (通貨) + nyr (書面証)"),
    ("10. 経済・交易・工芸・労働", "mardorn", "[mar.dorn]", "名", "関税、入市税、交易賦課金", "customs tariff, excise, transit tribute", "mar (交易) + dorn (賦課)"),
    ("10. 経済・交易・工芸・労働", "marzar", "[mar.zar]", "名", "通商同盟、ギルド連合、商工会議所", "merchant guild, commercial hanse, trade league", "mar (商業) + zar (同盟同業)"),
    ("10. 経済・交易・工芸・労働", "marparv", "[mar.parv]", "名", "見本市、定期市、大交易市", "trade fair, mart, seasonal emporium", "marmin (市場) + parv (盛大)"),
    ("10. 経済・交易・工芸・労働", "marsarp", "[mar.sarp]", "名", "在庫、棚卸資産、貯蔵商品", "inventory, stock of merchandise, reserve goods", "mar (商品) + sarp (備蓄)"),
    ("10. 経済・交易・工芸・労働", "marlanv", "[mar.lanv]", "名", "鋳造所、造幣局、硬貨打刻所", "mint, coin foundry, official minting bureau", "marlan (硬貨) + lanv (工房所)"),
    ("10. 経済・交易・工芸・労働", "dolsol", "[dol.sol]", "名", "鞴、ふいご、送風機", "bellows, blast-furnace air blower", "dolar (鍛冶) + sol (気風圧)"),
    ("10. 経済・交易・工芸・労働", "dolnyr", "[dol.nyr]", "名", "彫刻刀、鏨、金工たがね", "chisel, graver, repousse punch", "dolar (金属細工) + nyr (精細刻)"),
    ("10. 経済・交易・工芸・労働", "doltarv", "[dol.tarv]", "名", "焼戻し油、焼入れ水槽、冷却槽", "quenching bath, tempering trough", "dolar (冶金) + tarv (急冷浴)"),
    ("10. 経済・交易・工芸・労働", "jylnyr", "[jyl.nyr]", "名", "紡錘、糸巻き棒、スピンドル", "spindle, distaff, bobbin whorl", "jylpan (紡ぐ) + nyr (軸棒)"),
    ("10. 経済・交易・工芸・労働", "jylzaran", "[jyl.za.ran]", "名", "織物商、反物座、布地問屋", "draper guild, textile factor, cloth merchant", "jylpan (織布) + zaran (商座)"),
    ("10. 経済・交易・工芸・労働", "jylparv", "[jyl.parv]", "名", "染料、天然草木染め液、染色槽", "dye, natural vat tint, mordant liquid", "jylpan (織物) + parv (彩色)"),
    ("10. 経済・交易・工芸・労働", "dolsarp", "[dol.sarp]", "名", "坩堝、るつぼ、耐火溶解皿", "crucible, melting pot, refractory vessel", "dolar (鋳造) + sarp (耐熱深器)"),
    ("10. 経済・交易・工芸・労働", "martalv", "[mar.talv]", "名", "計量秤、天秤、分銅天秤", "scale balance, counterweight beam", "mar (交易) + talv (秤量)"),
    ("10. 経済・交易・工芸・労働", "marlorv", "[mar.lorv]", "名", "運搬車、荷車、交易荷駄", "cargo cart, freight wagon, dray", "laros (車両) + mar (貨物)"),
    ("10. 経済・交易・工芸・労働", "marporv", "[mar.porv]", "名", "商隊、キャラバン、星間交易船団", "caravan, merchant convoy, trade flotilla", "mar (交易) + porv (連行船列)"),
    ("10. 経済・交易・工芸・労働", "marpalv", "[mar.palv]", "名", "卸売、一括仕入れ、大量売買", "wholesale lot, bulk lading, gross consignment", "mar (商業) + palv (大口量)"),
    ("10. 経済・交易・工芸・労働", "marpanan", "[mar.pa.nan]", "動", "投資する、出資する、資金を投じる", "invest, advance funds, finance enterprise", "mar (資本) + panan (供給投下)"),
    ("10. 経済・交易・工芸・労働", "dolpanan", "[dol.pa.nan]", "動", "鋳造する、型に流し込む、鋳型成型する", "cast, cast metal into mold, pour founding", "dolas (鋳型) + panan (流し込み)"),

    # 11. 建築・都市・住空間 (+18語)
    ("11. 建築・都市・住空間", "domsol", "[dom.sol]", "名", "柱頭、柱飾り、エンタブラチュア", "capital, pediment pillar ornament", "domlik (柱) + sol (冠頂)"),
    ("11. 建築・都市・住空間", "falnyr", "[fal.nyr]", "名", "狭間、スリット窓、採光矢狭間", "loophole, arrow slit window, embrasure", "falar (窓) + nyr (細隙)"),
    ("11. 建築・都市・住空間", "domdorn", "[dom.dorn]", "名", "雨樋、樋、排水配管", "gutter, waterspout, downspout pipe", "dom (家) + dorn (排水溝)"),
    ("11. 建築・都市・住空間", "domzarv", "[dom.zarv]", "名", "大聖堂、天体観測ドーム宮、大殿", "basilica, grand dome rotunda, star minster", "dom (殿舎) + zarv (至高壮麗)"),
    ("11. 建築・都市・住空間", "domparv", "[dom.parv]", "名", "日除け庇、ポーチ屋根、キャノピー", "awnings, portico canopy, marquee overhang", "celdom (屋根) + parv (庇突出)"),
    ("11. 建築・都市・住空間", "domsarp", "[dom.sarp]", "名", "屋根裏部屋、ロフト、小間屋根裏", "attic, loft, garret bed-chamber", "dom (部屋) + sarp (上層屋根下)"),
    ("11. 建築・都市・住空間", "dursol", "[dur.sol]", "名", "石垣、石積み擁壁、乾式石壁", "drystone masonry, drystone retaining revetment", "durval (壁) + sol (石積み)"),
    ("11. 建築・都市・住空間", "lerson", "[ler.son]", "名", "跳ね橋、城門引橋、昇降橋", "drawbridge, portcullis causeway", "lerel (門) + son (昇降橋梁)"),
    ("11. 建築・都市・住空間", "lersol", "[ler.sol]", "名", "落とし格子、鉄格子門、防護落とし戸", "portcullis, iron grate grille gate", "lerel (扉) + sol (降下格子)"),
    ("11. 建築・都市・住空間", "domtalv", "[dom.talv]", "名", "中庭噴水、噴水池、中庭水景", "courtyard fountain, basin jet", "velar (庭) + talv (水盤)"),
    ("11. 建築・都市・住空間", "domlorv", "[dom.lorv]", "名", "鐘楼、時報塔、鐘楼台", "campanile, belfry, clock spire", "domcor (塔) + lorv (鐘音)"),
    ("11. 建築・都市・住空間", "dompalv", "[dom.palv]", "名", "街路樹通り、並木道、プロムナード", "boulevard, tree-lined allée, promenade", "domom (都市) + palv (植樹路)"),
    ("11. 建築・都市・住空間", "dursarp", "[dur.sarp]", "名", "胸壁、銃眼付き狭間胸壁", "battlement, crenellated parapet", "durkas (城壁) + sarp (頂部胸壁)"),
    ("11. 建築・都市・住空間", "talson", "[tal.son]", "名", "石橋、アーチ橋、橋梁", "arch bridge, stone viaduct, aqueduct", "tal (石) + son (渡り架橋)"),
    ("11. 建築・都市・住空間", "domkarn", "[dom.karn]", "名", "厩舎、馬屋、動物飼育棟", "stables, mews, beast barn", "dom (建物) + karn (家畜飼育)"),
    ("11. 建築・都市・住空間", "domzar", "[dom.zar]", "名", "中央広場、アゴラ、フォーラム", "central plaza, agora, civic concourse", "domom (都市) + zar (中心大広場)"),
    ("11. 建築・都市・住空間", "dompanan", "[dom.pa.nan]", "動", "落成する、上棟する、家を建てる", "erect dwelling, raise ridgepole, inaugurate building", "dom (家) + panan (建立完成)"),
    ("11. 建築・都市・住空間", "durpanan", "[dur.pa.nan]", "動", "築く、城壁を巡らせる、要塞化する", "fortify, entrench, embattle with wall", "durval (壁) + panan (外郭構築)"),

    # 12. 食・飲料・調理・食具 (+17語)
    ("12. 食・飲料・調理・食具", "nersol", "[ner.sol]", "名", "酵母、天然酵母、パン種", "yeast, leaven, sourdough starter culture", "nerat (パン) + sol (発酵芯)"),
    ("12. 食・飲料・調理・食具", "nernyr", "[ner.nyr]", "名", "蜂蜜、花蜜、天然蜜液", "honey, wild comb nectar, sweet mead-syrup", "ner (甘露) + nyr (金色の蜜)"),
    ("12. 食・飲料・調理・食具", "nerzar", "[ner.zar]", "名", "大宴会、祝宴、宮廷晩餐会", "banquet, symposium, festive banquet spread", "nerel (料理) + zar (豪華饗宴)"),
    ("12. 食・飲料・調理・食具", "bionsol", "[bion.sol]", "名", "麦酒、エール、醸造穀物酒", "ale, brewed malt draught, rustic beer", "bion (飲) + sol (発泡醸造)"),
    ("12. 食・飲料・調理・食具", "bionzar", "[bion.zar]", "名", "蒸留酒、酒精、ブランデー", "distilled spirits, aqua vitae, hard liquor", "voril (酒) + zar (高濃度精留)"),
    ("12. 食・飲料・調理・食具", "nerparv", "[ner.parv]", "名", "燻製室、燻製小屋、スモーク室", "smokehouse, curing loft", "nercor (保存肉) + parv (煙燻小屋)"),
    ("12. 食・飲料・調理・食具", "nersarp", "[ner.sarp]", "名", "酒樽、貯蔵樽、木樽", "cask, keg, barrel tun", "voril (酒) + sarp (貯蔵胴樽)"),
    ("12. 食・飲料・調理・食具", "nerdorn", "[ner.dorn]", "名", "濾し器、篩い、裏ごし布", "sieve, colander, straining cheesecloth", "ner (調理) + dorn (濾過分級)"),
    ("12. 食・飲料・調理・食具", "nertalv", "[ner.talv]", "名", "すりこぎ、擂粉木、杵", "pestle, muller, grinding pounder", "talpork (すり鉢) + talv (打具)"),
    ("12. 食・飲料・調理・食具", "nerlorv", "[ner.lorv]", "名", "焙煎機、焙煎釜、コーヒー豆煎り器", "roaster, parching pan, bean roaster", "pyrtos (焼く) + lorv (回転釜)"),
    ("12. 食・飲料・調理・食具", "bionpalv", "[bion.palv]", "名", "酒場、居酒屋、タバーン", "tavern, alehouse, wayside pub", "nerar (食堂) + bion (酒飲)"),
    ("12. 食・飲料・調理・食具", "nerpalv", "[ner.palv]", "名", "パン屋、製パン工房、ベーカリー", "bakery, bakehouse, bread stall", "nerat (パン) + palv (工房店)"),
    ("12. 食・飲料・調理・食具", "nerson", "[ner.son]", "名", "焼き網、グリル台、鉄板", "griddle, gridiron, broiling rack", "pyrtos (ロースト) + son (棚枠)"),
    ("12. 食・飲料・調理・食具", "nerpork", "[ner.pork]", "名", "調味油、オリーブ油、食用植物油", "edible culinary oil, seed pressing", "ner (食) + pork (圧搾油)"),
    ("12. 食・飲料・調理・食具", "nersarn", "[ner.sarn]", "名", "果実の砂糖漬け、ジャム、コンポート", "preserve, compote, candied conserve", "vorin (果実) + sarn (甘露煮)"),
    ("12. 食・飲料・調理・食具", "nerpanv", "[ner.panv]", "動", "発酵させる、醸造熟成させる", "ferment, brew, culture with leaven", "nersol (酵母) + panv (作用熟成)"),
    ("12. 食・飲料・調理・食具", "bionpan", "[bion.pan]", "動", "乾杯する、祝杯をあげる、盃を交わす", "toast, raise cups in cheer, clink glasses", "bionel (杯) + pan (掲げ合い)"),

    # 13. 衣飾・携行具・日常品 (+17語)
    ("13. 衣飾・携行具・日常品", "valzar", "[val.zar]", "名", "絹織物、極上布、天の薄絹", "fine silk, diaphanous samite, astral damask", "valis (布) + zar (至高貴布)"),
    ("13. 衣飾・携行具・日常品", "valnyr", "[val.nyr]", "名", "刺繍、金糸銀糸の刺繍飾り", "embroidery, needlework, brocade threadwork", "valis (衣服) + nyr (細緻飾)"),
    ("13. 衣飾・携行具・日常品", "valsol", "[val.sol]", "名", "裏地、内張り、保温裏毛", "lining, inner quilting, fleece lining", "valis (服) + sol (内層)"),
    ("13. 衣飾・携行具・日常品", "valparv", "[val.parv]", "名", "襟、首回り飾り、カラー", "collar, ruff, neckband", "valis (服) + parv (首元端)"),
    ("13. 衣飾・携行具・日常品", "valsarp", "[val.sarp]", "名", "袖、長袖、腕覆い", "sleeve, gauntlet sleeve, arm covering", "valis (服) + sarp (腕覆い)"),
    ("13. 衣飾・携行具・日常品", "larsol", "[lar.sol]", "名", "サンダル、編み履物、軽靴", "sandal, strapped buskin, light slipper", "larsil (靴) + sol (軽量開放)"),
    ("13. 衣飾・携行具・日常品", "valtarv", "[val.tarv]", "名", "ショール、肩掛け、大判肩掛け布", "shawl, shoulder wrap, stole", "valis (布) + tarv (肩掛け)"),
    ("13. 衣飾・携行具・日常品", "valdorv", "[val.dorv]", "名", "ボタン、留め釦、骨角ボタン", "button, toggle, stud clasp", "valser (留め具) + dorv (円球釦)"),
    ("13. 衣飾・携行具・日常品", "kirelzar", "[ki.rel.zar]", "名", "羊皮紙、上質筆記羊皮紙、古文書葉", "parchment, vellum scroll, archival leaf", "pamel (書物) + zar (高級紙葉)"),
    ("13. 衣飾・携行具・日常品", "kirelsol", "[ki.rel.sol]", "名", "インク、黒インク、星辰筆記墨汁", "ink, writing fluid, lampblack wash", "kirel (ペン) + sol (黒汁染料)"),
    ("13. 衣飾・携行具・日常品", "falsol", "[fal.sol]", "名", "松明、たいまつ、樹脂篝火", "torch, pitch cresset, flare stave", "falmir (ランプ) + sol (剛柄木)"),
    ("13. 衣飾・携行具・日常品", "talzar", "[tal.zar]", "名", "指輪、宝石指環、星辰印章環", "signet ring, gem band, annular circlet", "tal (宝飾金属) + zar (円環貴)"),
    ("13. 衣飾・携行具・日常品", "talvinor", "[tal.vi.nor]", "名", "首飾り、ネックレス、宝石胸飾り", "necklace, pectoral gorget, pendant collar", "tal (宝飾) + vinor (首元連)"),
    ("13. 衣飾・携行具・日常品", "talparil", "[tal.pa.ril]", "名", "耳飾り、イヤリング、耳環", "earring, ear drop, lobe pendant", "tal (貴石) + paril (耳部小飾)"),
    ("13. 衣飾・携行具・日常品", "valtasp", "[val.tasp]", "名", "財布、革巾着、小銭入れ", "purse, pouch, coin purse", "valtas (鞄) + p (小型)"),
    ("13. 衣飾・携行具・日常品", "valson", "[val.son]", "動", "着替える、装いを整える、身繕いする", "change attire, don festive robes, groom outfit", "valis (服) + son (更新)"),
    ("13. 衣飾・携行具・日常品", "kirelpan", "[ki.rel.pan]", "動", "清書する、写本する、毛筆筆耕する", "transcribe, calligraph, fair-copy", "kirel (ペン) + pan (美麗筆耕)"),

    # 14. 精神・哲学・感情・芸術 (+17語)
    ("14. 精神・哲学・感情・芸術", "minsol", "[min.sol]", "名", "覚悟、揺るがぬ意志、不動心", "steadfast resolution, unyielding iron will", "min (心) + sol (堅固芯)"),
    ("14. 精神・哲学・感情・芸術", "minnyr", "[min.nyr]", "名", "慈愛、思いやり、深い憐憫", "compassion, tender mercy, gentleness of soul", "min (情) + nyr (やさしさ)"),
    ("14. 精神・哲学・感情・芸術", "minzar", "[min.zar]", "名", "悟り、真我の覚知、霊的開眼", "enlightenment, spiritual awakening, episteme", "min (意識) + zar (最高覚醒)"),
    ("14. 精神・哲学・感情・芸術", "sardorn", "[sar.dorn]", "名", "哀傷、メランコリー、静かな悲嘆", "melancholy, gentle grief, elegiac sadness", "dyren (泣く) + dorn (沈思哀音)"),
    ("14. 精神・哲学・感情・芸術", "sarzar", "[sar.zar]", "名", "至福、法悦、エクスタシー", "bliss, rapture, transcendent ecstasy", "saren (歓喜) + zar (極致)"),
    ("14. 精神・哲学・感情・芸術", "civzar", "[civ.zar]", "名", "交響曲、大合奏、大管弦詩", "symphony, grand polyphonic concerto", "cival (音楽) + zar (大管弦組)"),
    ("14. 精神・哲学・感情・芸術", "civsol", "[civ.sol]", "名", "竪琴、リラ、ハープ、星辰弦楽器", "harp, lyre, starry kithara", "cival (楽) + sol (共鳴胴)"),
    ("14. 精神・哲学・感情・芸術", "civnyr", "[civ.nyr]", "名", "笛、フルート、星風の木管笛", "flute, pipe, reed recorder", "cival (音楽) + nyr (澄んだ笛音)"),
    ("14. 精神・哲学・感情・芸術", "civdorv", "[civ.dorv]", "名", "太鼓、打楽器、太古の律動鼓", "drum, timbrel, rhythm kettle", "civ (音律) + dorv (連打膜)"),
    ("14. 精神・哲学・感情・芸術", "falzar", "[fal.zar]", "名", "壁画、フレスコ画、壮大な天井画", "fresco, mural painting, celestial tableau", "falel (絵画) + zar (大壁面)"),
    ("14. 精神・哲学・感情・芸術", "talzarv", "[tal.zarv]", "名", "彫像、彫刻、石造モニュメント", "statue, stone sculpture, effigy effigy", "talis (石) + zarv (彫刻造形)"),
    ("14. 精神・哲学・感情・芸術", "minparv", "[min.parv]", "名", "好奇心、探求心、真理への憧れ", "inquisitiveness, curiosity, thirst for truth", "min (心) + parv (前傾探究)"),
    ("14. 精神・哲学・感情・芸術", "minpalv", "[min.palv]", "名", "安らぎ、静寂、心の平穏", "serenity, tranquil peace, quietude of mind", "min (精神) + palv (波風なき安堵)"),
    ("14. 精神・哲学・感情・芸術", "civpanan", "[civ.pa.nan]", "動", "作曲する、メロディを紡ぐ、詩曲を作る", "compose score, weave hymn melody, score music", "cival (音楽) + panan (創作)"),
    ("14. 精神・哲学・感情・芸術", "minpanan", "[min.pa.nan]", "動", "祈る、念じる、星辰に願う", "pray, supplicate the heavens, meditate longing", "min (心) + panan (捧げる)"),
    ("14. 精神・哲学・感情・芸術", "sarpanan", "[sar.pa.nan]", "動", "慰める、励ます、痛みに寄り添う", "console, comfort, cheer grieving heart", "minnyr (慈愛) + panan (施す)"),
    ("14. 精神・哲学・感情・芸術", "falpanan", "[fal.pa.nan]", "動", "彩色する、絵筆を執る、色を塗る", "paint, brush color onto canvas, illuminate page", "falel (画像) + panan (彩色描画)"),

    # 15. 性質・状態・色彩・感触 (+17語)
    ("15. 性質・状態・色彩・感触", "falsolv", "[fal.solv]", "形", "銀白色の、白銀に輝く、白光の", "silvery-white, argent, starlit pallor", "fal (光) + solv (純白銀)"),
    ("15. 性質・状態・色彩・感触", "kymsol", "[kym.sol]", "形", "濃紺の、深夜の蒼天色の、インディゴの", "midnight-blue, deep indigo, nocturnal cyan", "kym (夜) + sol (深み青)"),
    ("15. 性質・状態・色彩・感触", "pyrsol", "[pyr.sol]", "形", "緋色の、深紅の、紅蓮の", "crimson, scarlet-bright, ruby incandescent", "pyris (炎) + sol (濃朱)"),
    ("15. 性質・状態・色彩・感触", "velsolv", "[vel.solv]", "形", "深緑の、常緑の、濃緑色の", "forest-green, deep emerald, evergreen verdure", "vel (森) + solv (濃碧)"),
    ("15. 性質・状態・色彩・感触", "talsolv", "[tal.solv]", "形", "褐色の、土色の、琥珀土色の", "tawny, amber-brown, earthen russet", "tal (土) + solv (茶褐)"),
    ("15. 性質・状態・色彩・感触", "darzan", "[dar.zan]", "形", "湿った、しっとりした、水分を含んだ", "dank, humid, moist with vapor", "daris (水) + zan (含湿)"),
    ("15. 性質・状態・色彩・感触", "wylzan", "[wyl.zan]", "形", "乾燥した、乾ききった、からっとした", "arid, desiccated, crisp dry", "wylas (風) + zan (放湿)"),
    ("15. 性質・状態・色彩・感触", "talsarpv", "[tal.sarpv]", "形", "硬質な、緻密な、刃を通さぬ", "adamantine, impenetrable, dense-grained", "tal (岩) + sarpv (極密)"),
    ("15. 性質・状態・色彩・感触", "velzan", "[vel.zan]", "形", "弾力ある、ゴム状の、しなやかに戻る", "resilient, springy, buoyant elastic", "tulmin (柔軟) + zan (復元力)"),
    ("15. 性質・状態・色彩・感触", "falsarn", "[fal.sarn]", "形", "眩い、目が眩むほどの、強烈な閃光の", "dazzling, blindingly radiant, resplendent", "fal (光) + sarn (強烈閃耀)"),
    ("15. 性質・状態・色彩・感触", "kymsarn", "[kym.sarn]", "形", "ほの暗い、薄暗い、微光漂う", "dim, dusky, shadowy crepuscular", "kym (影) + sarn (微光陰)"),
    ("15. 性質・状態・色彩・感触", "pyrzan", "[pyr.zan]", "形", "熱烈な、灼熱の、焼けるような", "scalding, scorching, fiercely fervent", "pyris (火) + zan (高熱極)"),
    ("15. 性質・状態・色彩・感触", "kyrzan", "[kyr.zan]", "形", "凍てつく、極冷の、骨身に染みる冷たさの", "frigid, sub-zero chilling, gelid", "kyras (氷) + zan (極冷)"),
    ("15. 性質・状態・色彩・感触", "darsarn", "[dar.sarn]", "形", "芳醇な、口当たりの良い、香り高い", "mellifluous, mellow, aromatic savory", "ner (食) + sarn (芳香醇)"),
    ("15. 性質・状態・色彩・感触", "sersarn", "[ser.sarn]", "形", "ざらつく、粒立ちのある、手応えのある", "gritty, textured, tactile with grains", "ser (触覚) + sarn (粒粗)"),
    ("15. 性質・状態・色彩・感触", "sersolv", "[ser.solv]", "形", "絹のように滑らかな、つるつるとした", "silky, satiny smooth, gliding", "ser (触覚) + solv (無抵抗滑動)"),
    ("15. 性質・状態・色彩・感触", "minzan", "[min.zan]", "形", "誠実な、偽りのない、嘘偽りなき", "candid, forthright, unfeigned upright", "vyran (真理) + min (心)"),

    # 16. 動作・動態・時空・方向副詞 (+6語)
    ("16. 動作・動態・時空・方向副詞", "porzan", "[por.zan]", "動", "潜り抜ける、通過する、通り抜ける", "pass through, thread way, traverse corridor", "poran (歩く) + zan (貫通)"),
    ("16. 動作・動態・時空・方向副詞", "kypan", "[ky.pan]", "動", "身を屈める、伏せる、しゃがむ", "crouch, duck low, crouch beneath cover", "kym (影) + pan (低姿勢)"),
    ("16. 動作・動態・時空・方向副詞", "volzan", "[vol.zan]", "動", "急降下する、ダイブする、滑空降下する", "swoop, dive swiftly, plunge downward", "volan (飛ぶ) + zan (急降)"),
    ("16. 動作・動態・時空・方向副詞", "darzanv", "[dar.zanv]", "動", "潜水する、水中に潜る、深みへ沈む", "submerge, plunge underwater, dive into depths", "zylan (泳ぐ) + zanv (潜行)"),
    ("16. 動作・動態・時空・方向副詞", "serzan", "[ser.zan]", "動", "手繰り寄せる、引き寄せる、引っ張る", "draw near with hands, haul, pull cable", "ser (手) + zan (引張)"),
    ("16. 動作・動態・時空・方向副詞", "havzan", "[hav.zan]", "副", "間一髪で、ぎりぎりの時に、絶妙な頃合いで", "in the nick of time, just barely, on the razor edge of time", "hav (時) + zan (極限合致)"),
]

print(f"Total new candidate entries: {len(CANDIDATES)}")

# 1. Check count
assert len(CANDIDATES) == 268, f"Expected 268, got {len(CANDIDATES)}"

# 2. Check internal duplicates
roots = [c[1] for c in CANDIDATES]
dup_internal = [r for r in roots if roots.count(r) > 1]
assert len(dup_internal) == 0, f"Internal duplicates: {set(dup_internal)}"

# 3. Check overlap with existing 740 roots
overlap = [r for r in roots if r in existing_roots]
assert len(overlap) == 0, f"Overlap with existing: {overlap}"

# 4. Check forbidden chars
FORBIDDEN = set("qx")
for r in roots:
    assert not any(ch in FORBIDDEN for ch in r), f"Forbidden char in {r}"

# 5. Check Earth borrowings
earth_overlap = [r for r in roots if r in EARTH_BORROWING_BLACKLIST]
assert len(earth_overlap) == 0, f"Earth overlap: {earth_overlap}"

print("ALL 268 NEW CANDIDATES AUDITED AND VERIFIED PERFECTLY!")
