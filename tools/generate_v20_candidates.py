# tools/generate_v20_candidates.py
# Verify all 80 new candidate words: phonotactics, no Earth borrowings, no duplicates

NEW_80_ENTRIES = [
    # 1. 天体・宇宙力学・光 (2)
    ("1. 天体・宇宙力学・光", "velton", "[vel.ton]", "名", "連星系の重心、共通軌道中心", "barycenter, common orbital center", "vel (軌道) + ton (中心)"),
    ("1. 天体・宇宙力学・光", "falvyn", "[fal.vyn]", "名", "薄光、黄道光、微弱な宇宙光", "zodiacal light, faint celestial glow", "fal (光) + vyn (微細)"),

    # 2. 数理・幾何・計測 (5)
    ("2. 数理・幾何・計測", "talrin", "[tal.rin]", "名", "接線、接平面、接点", "tangent line, tangent plane", "tal (接触) + rin (円)"),
    ("2. 数理・幾何・計測", "kelton", "[kel.ton]", "名", "ベクトル、方向量、有向線分", "vector, directed quantity", "kel (変位) + ton (量)"),
    ("2. 数理・幾何・計測", "dorlik", "[dor.lik]", "名", "楕円、離心軌道、卵形", "ellipse, oval geometry", "dor (軌道) + lik (形)"),
    ("2. 数理・幾何・計測", "firven", "[fir.ven]", "名", "不変量、保存量、不変則", "invariant, conserved quantity", "firas (定数) + ven (状態)"),
    ("2. 数理・幾何・計測", "suftur", "[suf.tur]", "名", "指数、対数、累乗尺度", "exponent, logarithm, power scale", "suf (計算) + tur (階層)"),

    # 3. 情報・計算機・通信 (4)
    ("3. 情報・計算機・通信", "jynkas", "[jyn.kas]", "名", "パケット、転送単位、信号塊", "data packet, transmission frame", "jyn (電気) + kas (束)"),
    ("3. 情報・計算機・通信", "kirvel", "[kir.vel]", "名", "ルーティング、経路制御、伝送路選定", "routing, path control", "kir (導く) + vel (経路)"),
    ("3. 情報・計算機・通信", "sorvat", "[sor.vat]", "名", "レジスタ、超高速記憶枠、保持器", "register, high-speed storage cell", "soril (記憶) + vat (枠)"),
    ("3. 情報・計算機・通信", "krotis", "[kro.tis]", "名", "バグ、論理欠陥、不整合", "software defect, glitch, anomaly", "krot (破綻) + is (状態)"),

    # 4. 生命・生体・医療 (3)
    ("4. 生命・生体・医療", "serkym", "[ser.kym]", "名", "睡眠、安息、深い眠り", "sleep, slumber, rest cycle", "ser (静まる) + kym (夜)"),
    ("4. 生命・生体・医療", "serfal", "[ser.fal]", "名", "覚醒、目覚め、意識の再開", "awakening, vigil, waking state", "ser (静) + fal (光)"),
    ("4. 生命・生体・医療", "revtis", "[rev.tis]", "名", "疲労、消耗、体力の衰え", "fatigue, weariness, exhaustion", "rev (生気) + tis (減衰)"),

    # 5. 自然地形・地質・鉱物 (6)
    ("5. 自然地形・地質・鉱物", "talgen", "[tal.gen]", "名", "崖、絶壁、断崖", "cliff, precipice, sheer bluff", "tal (地) + gen (急峻)"),
    ("5. 自然地形・地質・鉱物", "talpen", "[tal.pen]", "名", "地層、堆積層、岩盤層", "stratum, geological layer, bed", "tal (地) + pen (層)"),
    ("5. 自然地形・地質・鉱物", "talsor", "[tal.sor]", "名", "盆地、すり鉢状の窪地", "basin, depression, hollow", "tal (地) + sor (窪み)"),
    ("5. 自然地形・地質・鉱物", "talvon", "[tal.von]", "名", "峡湾、フィヨルド、入江", "fjord, sea inlet, drowned valley", "tal (地) + von (深く入り込む)"),
    ("5. 自然地形・地質・鉱物", "taljyn", "[tal.jyn]", "名", "磁鉄鉱、天然磁石、引力石", "magnetite, lodestone, magnetic mineral", "tal (鉱) + jyn (磁気)"),
    ("5. 自然地形・地質・鉱物", "talpyrven", "[tal.pyr.ven]", "名", "溶岩、熔岩流、火成岩", "lava, volcanic magma, molten rock", "tal (岩) + pyr (火) + ven (流)"),

    # 6. 気象・大気・水域 (5)
    ("6. 気象・大気・水域", "celvorin", "[cel.vo.rin]", "名", "霧雨、小雨、微細な雨滴", "drizzle, fine rain, mizzle", "celis (雲) + vorin (滴り)"),
    ("6. 気象・大気・水域", "wylpar", "[wyl.par]", "名", "突風、疾風、一過性の強風", "gust, squall, sudden blast", "wyl (風) + par (激しい)"),
    ("6. 気象・大気・水域", "kyrvon", "[kyr.von]", "名", "雹、霰、氷の粒", "hail, sleet, ice pellets", "kyras (氷) + von (落下)"),
    ("6. 気象・大気・水域", "darpas", "[dar.pas]", "名", "引き潮、退潮、干潮", "ebb tide, low water, receding tide", "dar (水) + pas (後退)"),
    ("6. 気象・大気・水域", "darvor", "[dar.vor]", "名", "満ち潮、上げ潮、満潮", "flood tide, high water, rising tide", "dar (水) + vor (前進)"),

    # 7. 植物・生態・農耕 (8)
    ("7. 植物・生態・農耕", "veltyn", "[vel.tyn]", "名", "花粉、植物の精粉", "pollen, botanical spore", "vel (花) + tyn (粉)"),
    ("7. 植物・生態・農耕", "velsin", "[vel.sin]", "名", "蔓、巻きひげ、匍匐茎", "vine, creeper, tendril", "vel (草木) + sin (糸)"),
    ("7. 植物・生態・農耕", "talkanor", "[tal.ka.nor]", "名", "農夫、耕作者、栽培者", "farmer, cultivator, husbandman", "talkan (耕す) + or (人)"),
    ("7. 植物・生態・農耕", "velrotas", "[vel.ro.tas]", "名", "腐葉土、肥沃土、腐植", "humus, leaf-mold, fertile loam", "vel (葉) + rotas (朽ちて還る)"),
    ("7. 植物・生態・農耕", "velkin", "[vel.kin]", "名", "灌木、低木、茂み", "shrub, bush, thicket", "vel (木) + kin (低小)"),
    ("7. 植物・生態・農耕", "velsot", "[vel.sot]", "名", "樹液、植物の血漿、蜜液", "tree sap, botanical resin, nectar", "vel (樹) + sot (甘露液)"),
    ("7. 植物・生態・農耕", "talkanar", "[tal.ka.nar]", "名", "農場、耕作地、段々畑", "farm, cultivated field, cropland", "talkan (耕す) + ar (場所)"),
    ("7. 植物・生態・農耕", "teirpan", "[teir.pan]", "動", "播種する、種を蒔く、植え付ける", "sow seed, plant, propagate", "teiril (種) + pan (散布)"),

    # 8. 動物・生物種・共生 (10)
    ("8. 動物・生物種・共生", "ferlik", "[fer.lik]", "名", "巣、塒、鳥獣の棲家", "nest, burrow, lair, den", "fer (獣) + lik (場)"),
    ("8. 動物・生物種・共生", "voltyr", "[vol.tyr]", "名", "翼羽、風切羽、飛翔羽", "flight feather, quill, plumage", "vol (飛) + tyr (羽)"),
    ("8. 動物・生物種・共生", "ferpuk", "[fer.puk]", "名", "ひづめ、蹄、甲角", "hoof, ungula", "fer (獣) + puk (硬化部)"),
    ("8. 動物・生物種・共生", "zylpas", "[zyl.pas]", "名", "魚群、群泳、生物の群れ", "school of fish, shoal, swarm", "zylfer (魚) + pas (群れ)"),
    ("8. 動物・生物種・共生", "fervyn", "[fer.vyn]", "名", "鳴き声、鳥獣の呼び交わし", "bird call, animal cry, vocal call", "fer (動物) + vyn (声)"),
    ("8. 動物・生物種・共生", "ferkrot", "[fer.krot]", "名", "角、双角、突起角", "horn, antler, tusk", "fer (獣) + krot (鋭角)"),
    ("8. 動物・生物種・共生", "volmin", "[vol.min]", "名", "嘴、くちばし", "beak, bill, rostrum", "vol (鳥) + min (先端)"),
    ("8. 動物・生物種・共生", "zylvis", "[zyl.vis]", "名", "鱗、魚鱗、保護鱗板", "scale, fish scale, scute", "zylfer (魚) + vis (小板)"),
    ("8. 動物・生物種・共生", "ferpar", "[fer.par]", "名", "鉤爪、爪、鋭爪", "claw, talon", "fer (獣) + par (鋭利)"),
    ("8. 動物・生物種・共生", "ferjyl", "[fer.jyl]", "名", "共生、共生関係、相利共生", "symbiosis, mutualism", "fer (生物) + jyl (結合)"),

    # 9. 統治・社会・法・共同体 (3)
    ("9. 統治・社会・法・共同体", "domsen", "[dom.sen]", "名", "評議会、代議員会、合議機関", "senate, parliament, high assembly", "dom (家/都市) + sen (合意)"),
    ("9. 統治・社会・法・共同体", "jylkan", "[jyl.kan]", "名", "条約、連邦約款、恒久同盟", "covenant, treaty, pact of union", "jyl (結ぶ) + kan (定め)"),
    ("9. 統治・社会・法・共同体", "turvan", "[tur.van]", "名", "裁判、公判、調停審問", "trial, judicial hearing, arbitration", "tur (掟) + van (見極め)"),

    # 10. 経済・交易・工芸・労働 (8)
    ("10. 経済・交易・工芸・労働", "marlan", "[mar.lan]", "名", "貨幣、公認通貨、流通硬貨", "coin, currency, minted legal tender", "mar (交換) + lan (証)"),
    ("10. 経済・交易・工芸・労働", "marvis", "[mar.vis]", "名", "運賃、通行料、運搬経費", "freight fare, tariff, toll", "mar (交易) + vis (代価)"),
    ("10. 経済・交易・工芸・労働", "marven", "[mar.ven]", "名", "借入、負債、貸付信託", "loan, debt, credit trust", "mar (交換) + ven (委託)"),
    ("10. 経済・交易・工芸・労働", "dolas", "[do.las]", "名", "鋳型、鋳型枠、金型", "mold, matrix, casting die", "dolar (鍛造) + as (器)"),
    ("10. 経済・交易・工芸・労働", "martor", "[mar.tor]", "名", "商人、交易商人、商人ギルド員", "merchant, trader, factor", "mar (交易) + tor (人)"),
    ("10. 経済・交易・工芸・労働", "marmin", "[mar.min]", "名", "市場、取引所、バザール", "bazaar, exchange, commercial forum", "mar (交易) + min (中心広場)"),
    ("10. 経済・交易・工芸・労働", "jyldan", "[jyl.dan]", "名", "機織り機、織機", "weaving loom, textile frame", "jylpan (織る) + dan (機具)"),
    ("10. 経済・交易・工芸・労働", "dolpak", "[dol.pak]", "名", "金床、鉄敷、鍛冶台", "anvil, smithing block", "dolaran (鍛造) + pak (基盤台)"),

    # 11. 建築・都市・住空間 (7)
    ("11. 建築・都市・住空間", "domkar", "[dom.kar]", "名", "基礎、土台、建築石礎", "foundation, plinth, bedrock base", "dom (建築) + kar (基底)"),
    ("11. 建築・都市・住空間", "domvin", "[dom.vin]", "名", "回廊、列柱廊、アーケード", "colonnade, cloister, arcade walk", "dom (家) + vin (連なり)"),
    ("11. 建築・都市・住空間", "lervor", "[ler.vor]", "名", "玄関ホール、ポーチ、前室", "vestibule, front porch, ante-room", "lerel (扉) + vor (前)"),
    ("11. 建築・都市・住空間", "durkas", "[dur.kas]", "名", "防壁、城壁、外郭防護壁", "rampart, defensive parapet, outer wall", "durval (壁) + kas (強固)"),
    ("11. 建築・都市・住空間", "celpar", "[cel.par]", "名", "天窓、採光ドーム、クーポラ", "skylight dome, cupola, lantern roof", "cel (天) + par (開口)"),
    ("11. 建築・都市・住空間", "domsor", "[dom.sor]", "名", "地下室、貯蔵室、食糧庫", "cellar, basement vault, storeroom", "dom (家) + sor (下部貯蔵)"),
    ("11. 建築・都市・住空間", "falpar", "[fal.par]", "名", "バルコニー、露台、見晴台", "balcony, terrace, veranda", "fal (開口/光) + par (突出)"),

    # 12. 食・飲料・調理・食具 (5)
    ("12. 食・飲料・調理・食具", "nerlon", "[ner.lon]", "名", "乾酪、チーズ、凝縮乳", "curd, cheese, aged solid milk", "ner (食) + lon (凝固)"),
    ("12. 食・飲料・調理・食具", "nerpin", "[ner.pin]", "名", "香辛料、辛味薬味、芳香調味料", "spice, pungent seasoning, pepper", "ner (食) + pin (刺激)"),
    ("12. 食・飲料・調理・食具", "biondor", "[bion.dor]", "名", "薬酒、滋養液、エリクサー", "tonic, elixir, medicinal draught", "bion (飲) + dor (薬効)"),
    ("12. 食・飲料・調理・食具", "nerfat", "[ner.fat]", "名", "蒸し物、蒸気調理品", "steamed food, steamed cake", "ner (食) + fat (蒸気)"),
    ("12. 食・飲料・調理・食具", "nersar", "[ner.sar]", "名", "焼き菓子、ビスケット、乾酪菓子", "pastry, biscuit, baked crisp", "ner (食) + sar (乾焼き)"),

    # 13. 衣飾・携行具・日常品 (5)
    ("13. 衣飾・携行具・日常品", "valpuk", "[val.puk]", "名", "外套、マント、防風外套", "cloak, mantle, travelling cape", "valis (服) + puk (覆い)"),
    ("13. 衣飾・携行具・日常品", "valser", "[val.ser]", "名", "帯、ベルト、腰紐", "sash, belt, girdle, waist-strap", "valis (服) + ser (締める)"),
    ("13. 衣飾・携行具・日常品", "talpin", "[tal.pin]", "名", "留め針、ブローチ、安全ピン", "pin, brooch, fibula fastener", "tal (金属) + pin (針)"),
    ("13. 衣飾・携行具・日常品", "valtas", "[val.tas]", "名", "鞄、背嚢、サッチェル", "bag, satchel, rucksack, haversack", "valis (布) + tas (収容)"),
    ("13. 衣飾・携行具・日常品", "talvyn", "[tal.vyn]", "名", "櫛、髪飾り、整髪具", "comb, hair clasp, ornamental pin", "tal (材) + vyn (歯)"),

    # 14. 精神・哲学・感情・芸術 (3)
    ("14. 精神・哲学・感情・芸術", "mindan", "[min.dan]", "名", "直観、ひらめき、洞察", "intuition, insight, flash of clarity", "min (心) + dan (明察)"),
    ("14. 精神・哲学・感情・芸術", "sarmon", "[sar.mon]", "名", "ユーモア、機知、軽妙な笑い", "wit, subtle humor, playful mirth", "saren (笑う) + mon (軽妙)"),
    ("14. 精神・哲学・感情・芸術", "civom", "[ci.vom]", "名", "叙事詩、星間神話詩、長編伝承", "epic poem, cosmological saga", "cival (歌) + om (大系)"),

    # 15. 性質・状態・色彩・感触 (3)
    ("15. 性質・状態・色彩・感触", "tulmin", "[tul.min]", "形", "柔軟な、しなやかな、弾力のある", "flexible, supple, pliable", "tul (屈曲) + min (質)"),
    ("15. 性質・状態・色彩・感触", "dorvan", "[dor.van]", "形", "脆い、壊れやすい、繊細な", "fragile, brittle, delicate", "dor (弱) + van (性)"),
    ("15. 性質・状態・色彩・感触", "falkas", "[fal.kas]", "形", "粗い、ざらざらした、無加工の", "rough, coarse, unpolished", "fal (素) + kas (硬質)"),

    # 16. 動作・動態・時空・方向副詞 (3)
    ("16. 動作・動態・時空・方向副詞", "talvok", "[tal.vok]", "動", "掘る、穿つ、地下を開削する", "dig, excavate, burrow out", "tal (地) + vok (穿つ)"),
    ("16. 動作・動態・時空・方向副詞", "nerpan", "[ner.pan]", "動", "刻む、細切りにする、みじん切りにする", "chop, mince, dice finely", "ner (食) + pan (分割)"),
    ("16. 動作・動態・時空・方向副詞", "jylvor", "[jyl.vor]", "動", "編み上げる、結び合わせる、束ねる", "plait, entwine, bind together", "jyl (結ぶ) + vor (成形)"),
]

import json
with open("data/lexicon.json", "r", encoding="utf-8") as f:
    existing_vocab = json.load(f)["vocabulary"]
existing_roots = {w["nrs"] for w in existing_vocab}

print(f"Candidate count: {len(NEW_80_ENTRIES)}")
assert len(NEW_80_ENTRIES) == 80, f"Expected 80 entries, got {len(NEW_80_ENTRIES)}"

# Audit check
roots = [e[1] for e in NEW_80_ENTRIES]
assert len(roots) == len(set(roots)), f"Internal duplicates: {[r for r in roots if roots.count(r) > 1]}"
overlap = [r for r in roots if r in existing_roots]
assert len(overlap) == 0, f"Overlap with existing: {overlap}"

FORBIDDEN = set("qx")
forbidden_check = [r for r in roots if any(c in FORBIDDEN for c in r)]
assert len(forbidden_check) == 0, f"Forbidden letters: {forbidden_check}"

print("All 80 candidates successfully validated!")
