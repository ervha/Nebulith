# -*- coding: utf-8 -*-
import json
import os

new_vocab_entries = [
    # --- 副詞群（時間・頻度） ---
    {
        "id": 30048,
        "nrs": "havon",
        "category": "追加語彙（副詞・頻度）",
        "pos": "副",
        "meaningJa": "いつも、常に、恒常的に",
        "meaningEn": "always, constantly, perpetually",
        "ipa": "[ha.von]",
        "notes": "マイルストーン2造語。hav(周期・時間)+-on(持続)。恒常的な反復・普遍的持続を表す。"
    },
    {
        "id": 30049,
        "nrs": "havtul",
        "category": "追加語彙（副詞・頻度）",
        "pos": "副",
        "meaningJa": "時々、たまに、断続的に",
        "meaningEn": "sometimes, occasionally, at times",
        "ipa": "[hav.tul]",
        "notes": "マイルストーン2造語。hav(周期)+tul(浅い・稀少)。間隔を置いた断続的生起を表す。"
    },
    {
        "id": 30050,
        "nrs": "feval",
        "category": "追加語彙（副詞・時間）",
        "pos": "副",
        "meaningJa": "すでに、もう、事前に",
        "meaningEn": "already, beforehand",
        "ipa": "[fe.val]",
        "notes": "マイルストーン2造語。fe(過去)+val(到達境界)。事象が既に完了・到達している様態。"
    },
    {
        "id": 30051,
        "nrs": "divan",
        "category": "追加語彙（副詞・時間）",
        "pos": "副",
        "meaningJa": "まだ、今なお、依然として",
        "meaningEn": "still, yet, continuously",
        "ipa": "[di.van]",
        "notes": "マイルストーン2造語。di(進行)+van(維持大気)。状態が解消されず継続している様態。"
    },
    {
        "id": 30052,
        "nrs": "tasik",
        "category": "追加語彙（副詞・時間）",
        "pos": "副",
        "meaningJa": "すぐに、直ちに、即座に",
        "meaningEn": "immediately, promptly, at once",
        "ipa": "[ta.sik]",
        "notes": "マイルストーン2造語。tas(迅速能動)+-ik(副詞化辞)。間髪を入れず次の動作へ移る様態。"
    },

    # --- 副詞群（程度・強調） ---
    {
        "id": 30053,
        "nrs": "solpar",
        "category": "追加語彙（副詞・程度）",
        "pos": "副",
        "meaningJa": "とても、非常に、極めて、たいへん",
        "meaningEn": "very, extremely, exceedingly",
        "ipa": "[sol.par]",
        "notes": "マイルストーン2造語。sol(集積量)+par(突出強調)。程度が通常閾値を大きく超える様態。"
    },
    {
        "id": 30054,
        "nrs": "vyntul",
        "category": "追加語彙（副詞・程度）",
        "pos": "副",
        "meaningJa": "少し、わずかに、やや",
        "meaningEn": "a little, slightly, marginally",
        "ipa": "[vyn.tul]",
        "notes": "マイルストーン2造語。vyn(微細)+tul(浅小)。微量の変化や控えめな程度を表す。"
    },
    {
        "id": 30055,
        "nrs": "narval",
        "category": "追加語彙（副詞・強調）",
        "pos": "副",
        "meaningJa": "全く、少しも、完全に（否定呼応）",
        "meaningEn": "at all, not in the least, entirely",
        "ipa": "[nar.val]",
        "notes": "マイルストーン2造語。nar(否定)+val(極限境界)。否定辞neと呼応して全否定を強調する。"
    },
    {
        "id": 30056,
        "nrs": "radon",
        "category": "追加語彙（副詞・程度）",
        "pos": "副",
        "meaningJa": "かなり、相当に、随分と",
        "meaningEn": "quite, considerably, rather",
        "ipa": "[ra.don]",
        "notes": "マイルストーン2造語。rad(規模半径)+-on(存在態)。無視できない相当の規模を表す。"
    },

    # --- 副詞群（様態） ---
    {
        "id": 30057,
        "nrs": "moril",
        "category": "追加語彙（副詞・様態）",
        "pos": "副",
        "meaningJa": "ゆっくり、緩やかに、穏やかに",
        "meaningEn": "slowly, gently, leisurely",
        "ipa": "[mo.ril]",
        "notes": "マイルストーン2造語。mor(静止身体)+-il(様態)。急がず静穏に進行する様態。"
    },
    {
        "id": 30058,
        "nrs": "tasin",
        "category": "追加語彙（副詞・様態）",
        "pos": "副",
        "meaningJa": "早く、速く、迅速に",
        "meaningEn": "quickly, swiftly, fast",
        "ipa": "[ta.sin]",
        "notes": "マイルストーン2造語。tas(速度能動)+-in(様態)。速度を上げて俊敏に動く様態。"
    },
    {
        "id": 30059,
        "nrs": "sirik",
        "category": "追加語彙（副詞・様態）",
        "pos": "副",
        "meaningJa": "静かに、ひそかに、沈黙のうちに",
        "meaningEn": "quietly, silently, softly",
        "ipa": "[si.rik]",
        "notes": "マイルストーン2造語。sir(静寂)+-ik(副詞辞)。物音や気配を立てず静謐に行う様態。"
    },
    {
        "id": 30060,
        "nrs": "kulen",
        "category": "追加語彙（副詞・様態）",
        "pos": "副",
        "meaningJa": "共に、一緒に、一体となって",
        "meaningEn": "together, jointly, in unison",
        "ipa": "[ku.len]",
        "notes": "マイルストーン2造語。ku(共同格)+-len(協調結合)。他者と足並みをそろえて協同する様態。"
    },
    {
        "id": 30061,
        "nrs": "minkir",
        "category": "追加語彙（副詞・様態）",
        "pos": "副",
        "meaningJa": "独りで、単独で、自ら",
        "meaningEn": "alone, singly, by oneself",
        "ipa": "[min.kir]",
        "notes": "マイルストーン2造語。min(個別主体)+kir(単一確定)。同伴者なく単独で行動する様態。"
    },

    # --- 自然・環境名詞 ---
    {
        "id": 30062,
        "nrs": "darlan",
        "category": "追加語彙（自然名詞）",
        "pos": "名",
        "meaningJa": "雨、天降る雨、慈雨",
        "meaningEn": "rain, rainfall, atmospheric shower",
        "ipa": "[dar.lan]",
        "notes": "マイルストーン2造語。dar(液体水)+lan(天よりの降下)。空から大地へ降り注ぐ雨水。"
    },
    {
        "id": 30063,
        "nrs": "kyrlan",
        "category": "追加語彙（自然名詞）",
        "pos": "名",
        "meaningJa": "雪、降雪、白雪",
        "meaningEn": "snow, snowfall",
        "ipa": "[kyr.lan]",
        "notes": "マイルストーン2造語。kyr/kyras(氷結晶)+lan(降下)。白く凍った結晶降下物。"
    },
    {
        "id": 30064,
        "nrs": "seldor",
        "category": "追加語彙（自然名詞）",
        "pos": "名",
        "meaningJa": "森、森林、樹林、樹木群落",
        "meaningEn": "forest, woods, grove",
        "ipa": "[sel.dor]",
        "notes": "マイルストーン2造語。sel(樹木生命)+dor(領域群集)。大地に繁茂する樹木の群生地。"
    },
    {
        "id": 30065,
        "nrs": "darven",
        "category": "追加語彙（自然名詞）",
        "pos": "名",
        "meaningJa": "川、小川、流水、清流",
        "meaningEn": "river, stream, flowing water",
        "ipa": "[dar.ven]",
        "notes": "マイルストーン2造語。dar(水)+ven(流動進行)。大地を絶えず流れる水流。"
    },
    {
        "id": 30066,
        "nrs": "vanur",
        "category": "追加語彙（自然名詞）",
        "pos": "名",
        "meaningJa": "風、大気の息吹、そよ風",
        "meaningEn": "wind, breeze, atmospheric air-current",
        "ipa": "[va.nur]",
        "notes": "マイルストーン2造語。van(大気)+ur(波動流動)。空間を巡る大気の動的運動。"
    },
    {
        "id": 30067,
        "nrs": "talmar",
        "category": "追加語彙（自然名詞）",
        "pos": "名",
        "meaningJa": "大地、原野、大地平原、野",
        "meaningEn": "earth, plain, wilderness field",
        "ipa": "[tal.mar]",
        "notes": "マイルストーン2造語。tal(大地)+mar(広袤領域)。見渡す限りに広がる堅牢な地表面。"
    },

    # --- 生活・道具・文化名詞 ---
    {
        "id": 30068,
        "nrs": "tasilel",
        "category": "追加語彙（生活名詞）",
        "pos": "名",
        "meaningJa": "道具、器具、手持ち器具",
        "meaningEn": "tool, utensil, implement",
        "ipa": "[ta.si.lel]",
        "notes": "マイルストーン2造語。tas(細工能動)+-el(道具素子)。人間が操作し作業を行う実体器具。"
    },
    {
        "id": 30069,
        "nrs": "fevtor",
        "category": "追加語彙（生活名詞）",
        "pos": "名",
        "meaningJa": "書物、本、記録書、典籍",
        "meaningEn": "book, tome, inscribed volume",
        "ipa": "[fev.tor]",
        "notes": "マイルストーン2造語。fev(記録文字)+tor(集成束)。文字と伝承が記され束ねられた書物。"
    },
    {
        "id": 30070,
        "nrs": "valtur",
        "category": "追加語彙（生活名詞）",
        "pos": "名",
        "meaningJa": "服、衣服、衣、外套",
        "meaningEn": "clothes, garment, robe",
        "ipa": "[val.tur]",
        "notes": "マイルストーン2造語。val(包み)+tur(層・布)。身体を保護し包み込む布製の衣類。"
    },
    {
        "id": 30071,
        "nrs": "zonpar",
        "category": "追加語彙（生活名詞）",
        "pos": "名",
        "meaningJa": "門、扉、出入口、ゲート",
        "meaningEn": "gate, door, portal",
        "ipa": "[zon.par]",
        "notes": "マイルストーン2造語。zon(境界)+par(開放孔)。境界を出入り可能にする扉・門口。"
    },
    {
        "id": 30072,
        "nrs": "poras",
        "category": "追加語彙（生活名詞）",
        "pos": "名",
        "meaningJa": "道、道路、小道、路",
        "meaningEn": "road, path, pathway",
        "ipa": "[po.ras]",
        "notes": "マイルストーン2造語。por(歩行)+as(敷設路)。歩行や移動のために拓かれた地上の道。"
    },
    {
        "id": 30073,
        "nrs": "govom",
        "category": "追加語彙（生活名詞）",
        "pos": "名",
        "meaningJa": "街、町、集落、集う場",
        "meaningEn": "town, village, settlement",
        "ipa": "[go.vom]",
        "notes": "マイルストーン2造語。govan(家)+-om(集合体)。複数の家々が集まり成す居住コミュニティ。"
    },
    {
        "id": 30074,
        "nrs": "vyllik",
        "category": "追加語彙（文化名詞）",
        "pos": "名",
        "meaningJa": "歌、歌曲、旋律歌、賛歌",
        "meaningEn": "song, chant, melody",
        "ipa": "[vyl.lik]",
        "notes": "マイルストーン2造語。vyl(声)+lik(形式調律)。声によって節をつけて紡がれる歌曲。"
    },
    {
        "id": 30075,
        "nrs": "vorpar",
        "category": "追加語彙（生活名詞）",
        "pos": "名",
        "meaningJa": "火、灯火、炎、篝火",
        "meaningEn": "fire, flame, hearth light",
        "ipa": "[vor.par]",
        "notes": "マイルストーン2造語。vor(発火点火)+par(突出光炎)。暗夜を照らし暖をもたらす炎。"
    },

    # --- 身体・心・感情名詞 ---
    {
        "id": 30076,
        "nrs": "civtor",
        "category": "追加語彙（心身名詞）",
        "pos": "名",
        "meaningJa": "心、精神、胸の内、心核",
        "meaningEn": "heart, mind, inner spirit",
        "ipa": "[civ.tor]",
        "notes": "マイルストーン2造語。civ(想念)+tor(中心核)。知性と感情が宿る精神的中心。"
    },
    {
        "id": 30077,
        "nrs": "celmir",
        "category": "追加語彙（身体名詞）",
        "pos": "名",
        "meaningJa": "瞳、目、まなざし",
        "meaningEn": "eye, gaze, pupil",
        "ipa": "[cel.mir]",
        "notes": "マイルストーン2造語。cel(星光景)+mir(観測)。外界の光と真理を捉える視覚器官。"
    },
    {
        "id": 30078,
        "nrs": "morpar",
        "category": "追加語彙（身体名詞）",
        "pos": "名",
        "meaningJa": "手、手のひら、御手",
        "meaningEn": "hand, palm",
        "ipa": "[mor.par]",
        "notes": "マイルストーン2造語。mor(身体)+par(操作端)。道具を握り他者と触れ合う上肢末端。"
    },
    {
        "id": 30079,
        "nrs": "porpar",
        "category": "追加語彙（身体名詞）",
        "pos": "名",
        "meaningJa": "足、脚、歩脚",
        "meaningEn": "foot, leg",
        "ipa": "[por.par]",
        "notes": "マイルストーン2造語。por(歩行)+par(支持端)。大地を踏みしめ歩行を支える下肢。"
    },
    {
        "id": 30080,
        "nrs": "novciv",
        "category": "追加語彙（身体名詞）",
        "pos": "名",
        "meaningJa": "頭、頭脳、思索座",
        "meaningEn": "head, brain, seat of thought",
        "ipa": "[nov.civ]",
        "notes": "マイルストーン2造語。nov(頂点)+civ(想念)。理知と思索を司る頭部。"
    },
    {
        "id": 30081,
        "nrs": "falmin",
        "category": "追加語彙（感情名詞）",
        "pos": "名",
        "meaningJa": "喜び、歓喜、喜悦、嬉しさ",
        "meaningEn": "joy, delight, gladness",
        "ipa": "[fal.min]",
        "notes": "マイルストーン2造語。fal(光明)+min(心境)。心が晴れやかに満たされる感情。"
    },
    {
        "id": 30082,
        "nrs": "kymmin",
        "category": "追加語彙（感情名詞）",
        "pos": "名",
        "meaningJa": "悲しみ、哀愁、悲嘆",
        "meaningEn": "sadness, grief, sorrow",
        "ipa": "[kym.min]",
        "notes": "マイルストーン2造語。kym(影闇)+min(心境)。胸に暗い影が落ちる哀傷の情。"
    },
    {
        "id": 30083,
        "nrs": "vorkot",
        "category": "追加語彙（感情名詞）",
        "pos": "名",
        "meaningJa": "怒り、激憤、憤り",
        "meaningEn": "anger, wrath, fury",
        "ipa": "[vor.kot]",
        "notes": "マイルストーン2造語。vor(猛火)+kot(破裂激発)。不正や侵害に対し炎のごとく滾る感情。"
    },
    {
        "id": 30084,
        "nrs": "fevran",
        "category": "追加語彙（感情名詞）",
        "pos": "名",
        "meaningJa": "勇気、気概、剛胆さ",
        "meaningEn": "courage, bravery, valor",
        "ipa": "[fev.ran]",
        "notes": "マイルストーン2造語。fev(確信誓言)+ran(前進意志)。恐れを超えて前へ進む強い心。"
    },
    {
        "id": 30085,
        "nrs": "sefast",
        "category": "追加語彙（感情名詞）",
        "pos": "名",
        "meaningJa": "希望、憧憬、望み",
        "meaningEn": "hope, aspiration, wish",
        "ipa": "[se.fast]",
        "notes": "マイルストーン2造語。sef(未来観測)+ast(希求願望)。明るい未来を希求する志向性。"
    },
    {
        "id": 30086,
        "nrs": "sirval",
        "category": "追加語彙（概念名詞）",
        "pos": "名",
        "meaningJa": "平和、安寧、静穏、平穏",
        "meaningEn": "peace, tranquility, serenity",
        "ipa": "[sir.val]",
        "notes": "マイルストーン2造語。sir(静寂)+val(調和充足)。争いや動揺がなく調和が保たれた状態。"
    },
    {
        "id": 30087,
        "nrs": "cylmin",
        "category": "追加語彙（感情名詞）",
        "pos": "名",
        "meaningJa": "愛、親愛、深い慈しみ",
        "meaningEn": "love, affection, tenderness",
        "ipa": "[cyl.min]",
        "notes": "マイルストーン2造語。cyl(調和美)+min(心情)。対象を深く慈しみ尊重する精神的絆。"
    },
    {
        "id": 30088,
        "nrs": "vylen",
        "category": "追加語彙（身体文化名詞）",
        "pos": "名",
        "meaningJa": "声、音声、言葉の響き",
        "meaningEn": "voice, vocal sound",
        "ipa": "[vy.len]",
        "notes": "マイルストーン2造語。vyl(音響)+-en(実体)。人間や生命が発する固有の音声。"
    }
]

# Update data/translation_extensions.json
ext_path = 'data/translation_extensions.json'
with open(ext_path, 'r', encoding='utf-8') as f:
    ext_data = json.load(f)

existing_ids = {e['id'] for e in ext_data.get('entries', [])}
added = 0
for entry in new_vocab_entries:
    if entry['id'] not in existing_ids:
        ext_data['entries'].append(entry)
        added += 1

with open(ext_path, 'w', encoding='utf-8') as f:
    json.dump(ext_data, f, ensure_ascii=False, indent=2)

print(f"SUCCESS: Added {added} new lexical entries to translation_extensions.json (Total: {len(ext_data['entries'])})")
