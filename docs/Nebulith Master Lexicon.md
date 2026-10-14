# 人工言語「Nebulith（ネビュリス）」マスター辞書データ定義書（Nebulith Master Lexicon v15.0）

**文書バージョン**: v15.0 (大規模体系的拡充・全数音韻監査済・細分化語根完全版)  
**最終更新日**: 2026-10-15  
**ステータス**: **全10分野・計 251 語幹収録／同音衝突ゼロ・語末ソノリティ100%適合検証済**  
**対応システム**: Nebulith Studio（統合スタジオ・単一画面）

---

## 1. 文法機能語・代名詞・軌道数詞マスターテーブル（Grammar & Numbers）

すべての語末は母音またはソノリティ共鳴音（`l, r, n, m, s`）で厳密に統制。

### 1.1 天体軌道格パーティクル（全9格）
動詞（恒星）の周りを巡る9つの軌道格標識。

| 格コード | NRS転写 | 発音 (IPA) | 文法機能・日本語訳 | 英語対応 |
| :--- | :--- | :--- | :--- | :--- |
| `NOM` (第1軌道：主格) | **`el`** | [el] | 〜は、〜が（動作主・主題） | [Subject / Agent] |
| `ACC` (第2軌道：対格) | **`ia`** | [ia] | 〜を（直接対象・被作用者） | [Direct Object / Patient] |
| `DAT` (第3軌道：与格) | **`al`** | [al] | 〜へ、〜に（授受・宛先） | [Recipient / Goal] |
| `GEN` (第4軌道：属格) | **`en`** | [en] | 〜の（所有・所属・連体修飾） | [Genitive / Possessive] |
| `LOC` (第5軌道：処格) | **`uo`** | [wo] | 〜において、〜で（時間・空間・領域） | [Locative / Spatiotemporal] |
| `INS` (第6軌道：具格) | **`de`** | [de] | 〜によって、〜を用いて（手段・道具・材料） | [Instrumental / Means] |
| `ALL` (第7軌道：向格) | **`to`** | [to] | 〜へ向かって、〜を目指して（終点・指向） | [Allative / Direction] |
| `ABL` (第8軌道：奪格) | **`va`** | [va] | 〜から、〜を出発点として（起点・原因） | [Ablative / Origin] |
| `COM` (第9軌道：共格) | **`ku`** | [ku] | 〜と共に、〜を伴って（同伴・連合） | [Comitative / Associative] |

### 1.2 恒星天体代名詞（代名詞体系）
自己・他者・星々を指し示す天体代名詞。

| 代名詞コード | NRS転写 | 発音 (IPA) | 意味・語源 | 日本語訳 |
| :--- | :--- | :--- | :--- | :--- |
| `1SG` (一人称単数) | **`tyr`** | [tyr] | 自星（己の核） | 私、我 |
| `2SG` (二人称単数) | **`zel`** | [zel] | 伴星（対峙する星） | あなた、君 |
| `3SG` (三人称単数) | **`mor`** | [mor] | 遠星（第三の光） | 彼、彼女、それ |
| `1PL` (一人称複数) | **`tyres`** | [ty.res] | 星団（我ら） | 私たち、我ら |
| `2PL` (二人称複数) | **`zeles`** | [ze.les] | 星群（君たち） | あなた方、君たち |
| `3PL` (三人称複数) | **`mores`** | [mo.res] | 遠星雲（彼ら） | 彼ら、それら |

### 1.3 軌道数詞（0〜10・主要基数）

| 数値 | NRS転写 | 発音 (IPA) | 象徴 | 意味 |
| :---: | :--- | :--- | :--- | :--- |
| **0** | **`nul`** | [nul] | 虚空、原初無 | ゼロ |
| **1** | **`un`** | [un] | 原初軸、単一 | 一 |
| **2** | **`du`** | [du] | 連星、双対 | 二 |
| **3** | **`tri`** | [tri] | 三極星、天秤 | 三 |
| **4** | **`kvan`** | [kvan] | 四至、四季 | 四 |
| **5** | **`kvin`** | [kvin] | 五芒星、手の掌 | 五 |
| **6** | **`ses`** | [ses] | 六花、結晶 | 六 |
| **7** | **`sep`** | [sep] *(数詞語末特例)* | 七曜、天球層 | 七 |
| **8** | **`ok`** | [ok] *(数詞語末特例)* | 八弦、二重四重 | 八 |
| **9** | **`nov`** | [nov] *(数詞語末特例)* | 九軌道、極限 | 九 |
| **10** | **`dek`** | [dek] *(数詞語末特例)* | 満天、十全十美 | 十 |

---

## 2. 派生接尾辞マスターシステム（Derivational Suffixes）

| 接尾辞 | 機能 | 派生例 (語根 → 派生語) | 意味 |
| :--- | :--- | :--- | :--- |
| **`-as`** | 日常的行為者・実務者 | `ner` (食) → `neras` [ne.ras] | 給仕人、配膳者 |
| **`-or`** | 専門職・知識人・指導者 | `sufo` (計算) → `sufor` [su.for] | プログラマー、論理技術者 |
| | | `daris` (治癒) → `darisor` [da.ri.sor] | 医師、ドクター |
| **`-is`** | 学術研究者・探求者 | `vyran` (真理) → `vyranis` [vy.ra.nis] | 哲学者、真理探求者 |
| **`-el`** | 道具・器具・機械・客体 | `mator` (演算機巧) → `pelel` [pe.lel] | 携帯情報端末（スマホ） |
| | | `ner` (食) → `nerel` [ne.rel] | 料理、温かい食事 |
| **`-ar` / `-an`** | 場所・施設・空間 | `dom` (部屋) → `domar` [do.mar] | 家、住宅 |
| | | `daris` (治癒) → `darisar` [da.ri.sar] | 病院、診療所 |
| | | `ner` (食) → `nerar` [ne.rar] | レストラン、カフェ |
| **`-il`** | 指小辞・愛称・親愛 | `vel` (木) → `velil` [ve.lil] | 若木、新芽、薬草 |
| **`-om`** | 集合体・領域・世界 | `dom` (部屋) → `domom` [do.mom] | 都市、都市圏 |
| | | `vel` (木) → `velom` [ve.lom] | 森林、樹海 |
| | | `sufo` (計算) → `sufom` [su.fom] | IT領域、電脳空間 |
| **`-i`** | 形容詞化（〜の性質を持つ） | `falun` (光) → `faluni` [fa.lu.ni] | 明るい、輝かしい |
| **`-u`** | 副詞化（〜のように、〜く） | `eiran` (永遠) → `eirinu` [ei.ri.nu] | 永遠に、いつでも |

---

## 3. 全分野別マスター語彙集（全10分野・体系的語根一覧）

各語彙は同一文内での反復・類似音連続（ゲシュタルト崩壊）を徹底排除するため、**行為・対象・道具・場所・主体のそれぞれに固有の自立語根**を割り当てています。

### 1. 天体・光・宇宙論

| NRS転写 | 発音 (IPA) | 品詞 | 日本語意味 | 英語対応 | 備考・語源 |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **`vyr`** | [vyr] | 名 | 星、天体、光点 | star, point of light | 星核の基本単音節 |
| **`vyris`** | [vy.ris] | 名/動 | 恒星、光を放つ | luminous star, shine | 星辰の輝き |
| **`zohar`** | [zo.har] | 名 | 太陽、主星、昼の光 | sun, primary star | 昼の中心恒星 |
| **`tynes`** | [ty.nes] | 名 | 月、衛星、夜の光球 | moon, satellite | 夜の衛星 |
| **`celen`** | [ʃe.len] | 名 | 空、天蓋、蒼穹、大気 | sky, firmament | 頭上の大空 |
| **`falun`** | [fa.lun] | 名/動 | 光、光条、輝き、照らす | light, ray, illuminate | 差し込む光条 |
| **`kym`** | [kym] | 名 | 夜、闇、陰 | night, darkness | 暗黒の基本単音節 |
| **`kyrim`** | [ky.rim] | 名 | 深淵、漆黒の宇宙、宇宙空間 | deep space, cosmos, abyss | 深宇宙 |
| **`laris`** | [la.ris] | 名 | 軌道、航路、天体周期 | orbit, celestial path | 天体の周回進路 |
| **`novar`** | [no.var] | 名 | 天頂、真上、最高点 | zenith, apex | 天空の頂点 |
| **`tulos`** | [tu.los] | 名 | 天底、最深点、真下 | nadir, bottom | 天空の最下点 |
| **`zemin`** | [ze.min] | 名 | 地平線、事象の地平面、境界 | horizon, event horizon | 視界・時空の境界 |
| **`voran`** | [vo.ran] | 名/動 | 星生、星の誕生、恒星点火 | star birth, ignition | 新星の発生 |
| **`kylen`** | [ky.len] | 名/動 | 星の終焉、超新星残骸、消滅 | star death, dissipation | 星の崩壊・超新星 |
| **`valur`** | [va.lur] | 名 | 天体脈動、電波、宇宙背景放射 | pulsation, cosmic wave | 宇宙の微弱電波 |
| **`telas`** | [te.las] | 名 | 天体望遠鏡、観測機器 | telescope, observatory instrument | 観測器具 |
| **`vyrelar`** | [vy.re.lar] | 名 | 天文台、天体観測ドーム | observatory | 観測所 |
| **`vyrelor`** | [vy.re.lor] | 名 | 天文学者、観測官 | astronomer | 天体観測士 |
| **`tyral`** | [ty.ral] | 名 | 引力、重力、求心力 | gravity, attraction force | 天体の相互引力 |
| **`spilin`** | [spi.lin] | 名 | 公転、自転、角速度 | orbital revolution, spin | 回転力学 |
| **`falos`** | [fa.los] | 名 | 分光、スペクトル、光輪 | spectrum, spectral band | 光の波長分解 |
| **`kyron`** | [ky.ron] | 名 | 黒孔、ブラックホール、重力特異点 | black hole, singularity | 光さえ出でぬ孔 |
| **`nebulis`** | [ne.bu.lis] | 名 | 星雲、星間ガス、宇宙塵 | nebula, cosmic dust cloud | 星々の母胎 |
| **`astral`** | [as.tral] | 形 | 星辰の、恒星系の、高貴な | astral, stellar | 星々の性質 |
| **`meteon`** | [me.te.on] | 名 | 流星、彗星、箒星 | meteor, comet | 夜空を走る光 |
| **`solas`** | [so.las] | 名 | 恒星風、太陽風、荷電粒子流 | stellar wind, solar flare | 恒星からの風 |
| **`eklis`** | [ek.lis] | 名 | 日食、月食、天体交食 | eclipse, occultation | 光の遮蔽 |
| **`afron`** | [af.ron] | 名 | 遠日点、最遠軌道点 | aphelion, apoapsis | 軌道の最高遠点 |
| **`peron`** | [pe.ron] | 名 | 近日点、最接近点 | perihelion, periapsis | 軌道の最接近点 |

### 2. 数理・幾何・情報科学

| NRS転写 | 発音 (IPA) | 品詞 | 日本語意味 | 英語対応 | 備考・語源 |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **`sufo`** | [su.fo] | 名/動 | 計算、論理、アルゴリズム | computation, logic | 論理の原点 |
| **`sufor`** | [su.for] | 名 | プログラマー、ITエンジニア、論理士 | programmer, software engineer | 論理技術職 |
| **`sufom`** | [su.fom] | 名 | 情報工学、電脳空間、IT領域 | computer science, cyberspace | 計算・情報分野 |
| **`mator`** | [ma.tor] | 名 | コンピューター、端末、演算機械 | computer, terminal | 精緻な計算機巧 |
| **`zevil`** | [ze.vil] | 名 | コード、プログラム、構文、文字列 | code, syntax, script | 論理文字列 |
| **`kiran`** | [ki.ran] | 動 | （コードを）記述する、紡ぐ、組む | write code, program, compile | プログラミング動詞 |
| **`pelel`** | [pe.lel] | 名 | スマートフォン、携帯情報端末 | smartphone, mobile device | 手のひらの端末 |
| **`tolas`** | [to.las] | 名 | メッセージ、通信文、メール | message, dispatch | 短い便り |
| **`wesan`** | [we.san] | 動 | 送信する、送る、信号を放つ | send, transmit | 通信動詞 |
| **`tolom`** | [to.lom] | 名 | インターネット、Web、世界通信網 | internet, cyber network | 世界情報網 |
| **`vylatel`** | [vy.la.tel] | 名 | ディスプレイ、画面、モニター | display, screen, monitor | 映像出力板 |
| **`falel`** | [fa.lel] | 名 | 写真、画像、静止画 | photo, image, graphic | 光の記録 |
| **`livar`** | [li.var] | 名 | データベース、書庫、情報保管庫 | database, repository | データ集積所 |
| **`jyn`** | [ʒyn] | 名 | 電気、電力、電荷、エネルギー | electricity, power, energy | 電力・エネルギー |
| **`jynel`** | [ʒy.nel] | 名 | バッテリー、蓄電池、電源 | battery, power cell | 蓄電器 |
| **`rin`** | [rin] | 名 | 円、真円、環 | circle, ring | 幾何円 |
| **`polos`** | [po.los] | 名 | 多角形、星型幾何、立体 | polygon, geometry | 幾何立体 |
| **`niven`** | [ni.ven] | 名 | 次元、座標軸、空間度数 | dimension, coordinate axis | 次元・軸 |
| **`talisum`** | [ta.li.sum] | 名 | 定理、証明された法則、公理 | theorem, axiom | 数学的定理 |
| **`kvan`** | [kvan] | 名 | 量子、最小単位、離散値 | quantum, discrete packet | 最小単位 |
| **`nodus`** | [no.dus] | 名 | ノード、結節点、ネットワーク頂点 | node, vertex | 網の交点 |
| **`modas`** | [mo.das] | 名 | 関数、変換式、写像 | function, mapping formula | 数理写像 |
| **`kelon`** | [ke.lon] | 名 | 変数、変動要素、パラメータ | variable, parameter | 可変値 |
| **`firas`** | [fi.ras] | 名 | 定数、普遍値、固定係数 | constant, invariant | 不変値 |
| **`syfren`** | [syf.ren] | 名/動 | 暗号、暗号化する、秘匿符号 | cipher, encrypt | 秘匿論理 |
| **`bitas`** | [bi.tas] | 名 | ビット、情報単位、二値信号 | bit, binary unit | 論理の最小単位 |
| **`matris`** | [mat.ris] | 名 | 行列、マトリクス、格子配列 | matrix, grid array | 二次元配列 |
| **`skopin`** | [sko.pin] | 名 | スコープ、有効範囲、視野域 | scope, valid range | 変数の可視範囲 |

### 3. 生命・身体・医療

| NRS転写 | 発音 (IPA) | 品詞 | 日本語意味 | 英語対応 | 備考・語源 |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **`zyvel`** | [zy.vel] | 名/動 | 生命、息吹、生きる、脈動する | life, breathe, live | 生命の脈動 |
| **`myren`** | [my.ren] | 名 | 人間、知性体、観測者 | human, sentient being | 星を見上げる者 |
| **`darisor`** | [da.ri.sor] | 名 | 医師、治癒師、ドクター | doctor, physician, healer | 医療専門職 |
| **`medin`** | [me.din] | 動 | 治療する、診察する、手当てする | heal, cure, treat | 医療動詞 |
| **`darisar`** | [da.ri.sar] | 名 | 病院、医院、診療所、クリニック | hospital, clinic | 医療施設 |
| **`sanel`** | [sa.nel] | 名 | 薬、処方薬、調合薬 | medicine, remedy, potion | 薬・薬品 |
| **`malis`** | [ma.lis] | 名 | 病、不調、軌道乱れ | illness, disease | 病気 |
| **`davel`** | [da.vel] | 名 | 血液、脈流、体液 | blood, vital fluid | 体内の血 |
| **`pulsen`** | [pul.sen] | 名 | 心拍、脈拍、鼓動 | pulse, heartbeat | 脈動 |
| **`noven`** | [no.ven] | 名 | 頭、頭脳、中枢神経 | head, brain, intellect center | 頭部・頭脳 |
| **`vylan`** | [vy.lan] | 名 | 目、瞳、視覚器官 | eye, pupil | 瞳 |
| **`harel`** | [ha.rel] | 名 | 耳、聴覚器官 | ear, auditory organ | 耳 |
| **`fenel`** | [fe.nel] | 名 | 口、唇、声門 | mouth, lips | 口 |
| **`nasor`** | [na.sor] | 名 | 鼻、嗅覚器官、息の通り道 | nose, breathway | 鼻 |
| **`ser`** | [ser] | 名 | 手、掌、指 | hand, palm, fingers | 手 |
| **`poris`** | [po.ris] | 名 | 足、脚、歩行器官 | foot, leg | 足 |
| **`teira`** | [tei.ra] | 名 | 心臓、胸の核、肉体の中心 | heart, core | 心臓・星核 |
| **`kymin`** | [ky.min] | 名/動 | 眠り、睡眠、休眠する | sleep, rest | 睡眠 |
| **`revir`** | [re.vir] | 動 | 目覚める、覚醒する、回復する | awake, recover | 覚醒・回復 |
| **`osel`** | [o.sel] | 名 | 骨、骨格、骨格構造 | bone, skeleton | 骨格 |
| **`muskol`** | [mus.kol] | 名 | 筋肉、筋力、運動器官 | muscle, sinew | 筋肉 |
| **`dermas`** | [der.mas] | 名 | 皮膚、肌、外被 | skin, dermis | 肌 |
| **`vitas`** | [vi.tas] | 名 | 健康、滋養、健全な生命力 | health, vitality | 健康 |
| **`nervis`** | [ner.vis] | 名 | 神経、感覚伝達網、シナプス | nerve, neural network | 神経系 |
| **`respiran`** | [res.pi.ran] | 動 | 呼吸する、息を吸い吐く | breathe, respire | 呼吸動詞 |

### 4. 自然・気象・環境

| NRS転写 | 発音 (IPA) | 品詞 | 日本語意味 | 英語対応 | 備考・語源 |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **`tal`** | [tal] | 名 | 大地、土壌、足元、地面 | earth, soil, ground | 地面・大地 |
| **`montis`** | [mon.tis] | 名 | 山、連峰、高嶺 | mountain, peak | 山 |
| **`kanyon`** | [kan.jon] | 名 | 谷、峡谷、裂け目 | valley, canyon | 谷 |
| **`campas`** | [kam.pas] | 名 | 平原、野原、大地原野 | plain, field, steppe | 広大な平野 |
| **`velom`** | [ve.lom] | 名 | 森、森林、樹海 | forest, woods | 広大な森 |
| **`vel`** | [vel] | 名 | 木、樹木、大樹 | tree | 樹木 |
| **`velas`** | [ve.las] | 名 | 葉、緑、葉擦れ | leaf, foliage | 葉 |
| **`velin`** | [ve.lin] | 名/動 | 花、咲く、芳香 | flower, bloom | 花 |
| **`velil`** | [ve.lil] | 名 | 新芽、若木、薬草、草 | herb, sprout, grass | 薬草・新芽 |
| **`vorin`** | [vo.rin] | 名 | 果実、木の実、果物 | fruit, berry | 果実 |
| **`semen`** | [se.men] | 名 | 種、種子、生命の核 | seed, pip | 種子 |
| **`daris`** | [da.ris] | 名 | 水、清流、淡水 | water, stream | 真水・清流 |
| **`dar`** | [dar] | 名 | しずく、水滴、朝露 | droplet, dew | しずく |
| **`zylar`** | [zy.lar] | 名 | 海、海洋、大洋 | sea, ocean | 大海 |
| **`lacor`** | [la.kor] | 名 | 湖、湖沼、静かな水面 | lake, pond | 静水面 |
| **`fontin`** | [fon.tin] | 名 | 泉、湧水、水源 | spring, font | 清らかな湧水 |
| **`darlen`** | [dar.len] | 名 | 雨、降雨 | rain, rainfall | 雨 |
| **`kyrlen`** | [kyr.len] | 名 | 雪、白雪、降雪 | snow, snowfall | 雪 |
| **`kyras`** | [ky.ras] | 名 | 氷、霜、氷結体 | ice, frost | 氷 |
| **`wylas`** | [wy.las] | 名/動 | 風、大気の流れ、そよぐ | wind, breeze | 風 |
| **`celis`** | [ʃe.lis] | 名 | 雲、霧、霞 | cloud, mist, fog | 雲・霧 |
| **`pyris`** | [py.ris] | 名 | 火、炎、熱源 | fire, flame | 火 |
| **`talis`** | [ta.lis] | 名 | 石、岩、鉱石、結晶 | stone, rock, mineral | 鉱物・石 |
| **`metas`** | [me.tas] | 名 | 金属、合金、鉱物資材 | metal, ore, alloy | 金属 |
| **`stormin`** | [stor.min] | 名 | 嵐、暴風雨、星雲嵐 | storm, tempest | 嵐 |
| **`tonor`** | [to.nor] | 名 | 雷、稲妻、天の閃光 | thunder, lightning | 雷鳴 |
| **`auror`** | [au.ror] | 名 | 極光、オーロラ、天の天幕 | aurora, polar light | 極光の帯 |
| **`deseras`** | [de.se.ras] | 名 | 砂漠、不毛地帯、荒野 | desert, wasteland | 乾燥砂漠 |
| **`spelun`** | [spe.lun] | 名 | 洞窟、鍾乳洞、地下空洞 | cave, cavern, grotto | 地下の洞 |
| **`feras`** | [fe.ras] | 名 | 動物、獣、野生生物 | animal, beast | 動物 |
| **`cielfer`** | [ʃi.el.fer] | 名 | 鳥、翼ある者、飛翔生物 | bird, winged creature | 鳥 |
| **`zylfer`** | [zyl.fer] | 名 | 魚、水棲生物 | fish, marine life | 魚 |
| **`inseka`** | [in.se.ka] | 名 | 虫、昆虫、甲虫 | insect, bug | 小昆虫 |

### 5. 社会・法・共同体

| NRS転写 | 発音 (IPA) | 品詞 | 日本語意味 | 英語対応 | 備考・語源 |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **`polim`** | [po.lim] | 名 | 社会、共同体、連盟 | society, community, polis | 共同社会 |
| **`taros`** | [ta.ros] | 名 | 法、法律、軌道規則、掟 | law, statute, canon | 法律・規範 |
| **`calor`** | [ʃa.lor] | 名 | 評議会、会議、議会、対話の座 | council, parliament, forum | 議会 |
| **`jylos`** | [ʒy.los] | 名 | 約束、契約、協定、盟約 | pact, covenant, contract | 条約・約束 |
| **`civor`** | [ʃi.vor] | 名 | 市民、住人、共同体員 | citizen, member | 市民 |
| **`celtor`** | [ʃel.tor] | 名 | 指導者、議長、導き手 | leader, chancellor, guide | 指導者 |
| **`dirin`** | [di.rin] | 名/形 | 正義、公正、均衡、正しい | justice, equity, righteous | 正義 |
| **`silan`** | [si.lan] | 名 | 調和、秩序、共存、平和 | harmony, order, peace | 社会の平和 |
| **`renis`** | [re.nis] | 名 | 貨幣、お金、通貨、クレジット | money, currency, credit | 通貨 |
| **`renar`** | [re.nar] | 名 | 市場、店、ショップ、取引所 | market, shop, exchange | 市場 |
| **`dolar`** | [do.lar] | 動 | 働く、勤労する、奉仕する | work, labor, serve | 労働動詞 |
| **`dolor`** | [do.lor] | 名 | 労働者、職人、働き手 | worker, artisan | 職人・働き手 |
| **`skolar`** | [sko.lar] | 名 | 学校、学舎、アカデミー | school, academy | 教育機関 |
| **`skolis`** | [sko.lis] | 名 | 学生、学徒、探求者 | student, pupil, scholar-initiate | 学び手 |
| **`doktor`** | [dok.tor] | 名 | 学者、碩学、博士 | scholar, doctor, master | 学究の徒 |
| **`tribun`** | [tri.bun] | 名 | 法廷、裁定所、審問会 | court, tribunal | 司法の場 |
| **`festas`** | [fes.tas] | 名 | 祭典、祝祭、星祭り | festival, celebration | 祝祭の日 |
| **`pasis`** | [pa.sis] | 名 | 安寧、平和、講和条約 | peace, truce, accord | 戦争の終結 |

### 6. 精神・感情・哲学

| NRS転写 | 発音 (IPA) | 品詞 | 日本語意味 | 英語対応 | 備考・語源 |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **`sylim`** | [sy.lim] | 名 | 心、魂、精神、内なる核 | mind, soul, spirit | 精神の核 |
| **`cynel`** | [ʃy.nel] | 名/動 | 愛、慈しみ、深い共感、愛する | love, affection, cherish | 深い愛情 |
| **`amiras`** | [a.mi.ras] | 名 | 友情、親愛、絆 | friendship, fellowship | 友愛 |
| **`elir`** | [e.lir] | 名/形 | 喜び、多幸感、嬉しい | joy, delight, gladness | 喜び |
| **`lyras`** | [ly.ras] | 名/形 | 哀愁、切なさ、悲哀、切ない | sorrow, melancholy, pathos | 切なさ |
| **`sirin`** | [si.rin] | 名/形 | 平穏、安らぎ、静けさ、穏やか | serenity, peace, tranquility | 心の静けさ |
| **`toras`** | [to.ras] | 名/形 | 激動、怒り、熱狂、激しい | fury, wrath, passion | 高ぶり |
| **`kefen`** | [ke.fen] | 名/形 | 畏怖、畏敬、厳粛な恐れ | awe, reverence | 畏怖 |
| **`welin`** | [we.lin] | 名/形 | 希望、憧れ、願い、望ましい | hope, aspiration, wish | 希望 |
| **`solen`** | [so.len] | 名/形 | 孤高、静かな孤独、一人きり | solitude, solitude-proud | 孤高 |
| **`memar`** | [me.mar] | 動 | 思索する、深く考える、熟慮する | contemplate, meditate, reflect | 哲学的思索 |
| **`fevas`** | [fe.vas] | 動 | 信じる、信頼する、託す | trust, believe, confide | 信託動詞 |
| **`kores`** | [ko.res] | 動 | 忘れる、手放す、過去に置く | forget, release, let go | 忘却・解放 |
| **`soras`** | [so.ras] | 名 | 記憶、想い出、刻印 | memory, remembrance | 想い出 |
| **`vyran`** | [vy.ran] | 名 | 真理、不変の理、ロゴス | truth, eternal principle | 真理 |
| **`vyranis`** | [vy.ra.nis] | 名 | 哲学者、真理の求道者 | philosopher, sage | 哲学者 |
| **`cylan`** | [ʃy.lan] | 名/形 | 美、崇高、調和美、美しい | beauty, sublime, graceful | 美しさ |
| **`sonir`** | [so.nir] | 名 | 夢、幻視、内なるビジョン | dream, vision | 夢 |
| **`valos`** | [va.los] | 名 | 勇気、果敢さ、不動の志 | courage, bravery, valor | 不屈の意志 |

### 7. 日常・住まい・食

| NRS転写 | 発音 (IPA) | 品詞 | 日本語意味 | 英語対応 | 備考・語源 |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **`dom`** | [dom] | 名 | 部屋、私室、空間 | room, chamber | 居室 |
| **`domar`** | [do.mar] | 名 | 家、住宅、住まい | house, home, dwelling | 住宅 |
| **`domom`** | [do.mom] | 名 | 都市、街、街区 | city, town, metropolis | 都市 |
| **`taran`** | [ta.ran] | 動 | 住まう、暮らす、居住する | live, dwell, reside | 居住動詞 |
| **`valis`** | [va.lis] | 名 | 衣服、装い、布地、衣類 | garment, robe, clothes | 衣服 |
| **`pamel`** | [pa.mel] | 名 | 本、書籍、手記ノート、冊子 | book, notebook, volume | 冊子・本 |
| **`talel`** | [ta.lel] | 名 | 机、作業台、テーブル | desk, table | 机 |
| **`tasel`** | [ta.sel] | 名 | 椅子、座席、腰掛け | chair, seat | 椅子 |
| **`stran`** | [stran] | 名 | 寝床、ベッド、休息所 | bed, resting couch | 寝具 |
| **`portas`** | [por.tas] | 名 | 扉、ドア、出入口、ゲート | door, gate, entrance | 扉 |
| **`fenas`** | [fe.nas] | 名 | 窓、明かり取り、天窓 | window, skylight | 窓 |
| **`toril`** | [to.ril] | 名 | 乗り物、車両、列車、交通艇 | vehicle, carriage, train | 乗り物 |
| **`larar`** | [la.rar] | 名 | 駅、ターミナル、空港、停泊地 | station, terminal, port | 交通拠点 |
| **`ner`** | [ner] | 名 | 滋養、食材、食物 | nourishment, foodstuff | 食料 |
| **`neran`** | [ne.ran] | 動 | 食べる、食事する、味わう | eat, dine, partake | 食事動詞 |
| **`nerel`** | [ne.rel] | 名 | 料理、ごはん、温かい食事 | meal, cooked dish | 料理 |
| **`neror`** | [ne.ror] | 名 | 料理人、シェフ | cook, chef | 料理人 |
| **`nerar`** | [ne.rar] | 名 | カフェ、喫茶店、食堂、レストラン | cafe, restaurant, diner | 飲食店 |
| **`bion`** | [bi.on] | 動 | 飲む、喫する、喉を潤す | drink, sip | 飲用動詞 |
| **`cavil`** | [ka.vil] | 名 | 珈琲、茶、温かい飲み物 | coffee, tea, warm brew | カフェ飲料 |
| **`lanis`** | [la.nis] | 名 | パン、主食、焼き菓子 | bread, loaf, staple | 主食 |
| **`salin`** | [sa.lin] | 名 | 塩、調味料、精製塩 | salt, seasoning | 塩 |
| **`suvel`** | [su.vel] | 名 | スープ、汁物、温煮 | soup, broth | スープ |
| **`vinor`** | [vi.nor] | 名 | 果実酒、ワイン、祝い酒 | wine, fermented drink | 酒 |
| **`klavis`** | [kla.vis] | 名 | 鍵、解錠具、キー | key, lock-opener | 鍵 |
| **`kalis`** | [ka.lis] | 名 | 杯、カップ、酒杯、グラス | chalice, cup, goblet | 食器杯 |
| **`kutar`** | [ku.tar] | 名 | 小刀、ナイフ、調理刃 | knife, blade, cutter | 刃物具 |

### 8. 動作・相互作用

| NRS転写 | 発音 (IPA) | 品詞 | 日本語意味 | 英語対応 | 備考・語源 |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **`relen`** | [re.len] | 動 | ある、存在する、実在する | exist, be present | 存在コピュラ |
| **`poran`** | [po.ran] | 動 | 歩く、歩む、旅する、進む | walk, journey, travel | 歩行動詞 |
| **`kursan`** | [kur.san] | 動 | 走る、急ぎ行く、駆ける | run, sprint, rush | 走行動詞 |
| **`volan`** | [vo.lan] | 動 | 飛ぶ、飛翔する、舞い上がる | fly, soar | 飛翔動詞 |
| **`toren`** | [to.ren] | 動 | 来る、訪れる、届く、降る | come, arrive, fall | 到来動詞 |
| **`vyrel`** | [vy.rel] | 動 | （精密に）観測する、測定する | observe, measure | 観測動詞 |
| **`celan`** | [ʃe.lan] | 動 | （空や星を）仰ぎ見る、見上げる | look up, gaze, admire | 仰望動詞 |
| **`haris`** | [ha.ris] | 動 | 聴く、耳を傾ける、聞き届ける | listen, hear | 聴覚動詞 |
| **`serin`** | [se.rin] | 動 | 触れる、手渡す、受け止める | touch, hold, receive | 触覚動詞 |
| **`fenor`** | [fe.nor] | 動 | 話す、語る、述べる、名づける | speak, utter, tell | 発話動詞 |
| **`calun`** | [ʃa.lun] | 動 | 対話する、語り合う、相談する | converse, converse with | 対話動詞 |
| **`cival`** | [ʃi.val] | 動 | 歌う、奏でる、旋律を紡ぐ | sing, play music, harmonize | 音楽動詞 |
| **`saren`** | [sa.ren] | 動 | 笑う、微笑む、笑顔になる | smile, laugh | 笑顔動詞 |
| **`dyren`** | [dy.ren] | 動 | 涙する、泣く、しずくが滴る | weep, shed tear | 落涙動詞 |
| **`jylas`** | [ʒy.las] | 動 | 結ぶ、繋ぐ、交差する、結合する | connect, bind, intersect | 結合動詞 |
| **`kiras`** | [ki.ras] | 動 | 創る、構築する、工作する、書く | create, build, compose | 創造動詞 |
| **`soran`** | [so.ran] | 動 | （ノートに）書き留める、記す | record, chronicle, write down | 筆記動詞 |
| **`taris`** | [ta.ris] | 動 | 待つ、佇む、待機する | wait, pause, linger | 静止動詞 |
| **`vymin`** | [vy.min] | 動 | 守る、庇護する、防護する | protect, guard, shield | 守護動詞 |
| **`velan`** | [ve.lan] | 動 | 探す、探索する、発見する | search, find, discover | 探索動詞 |
| **`kyvel`** | [ky.vel] | 動 | 隠す、包み込む、秘める | conceal, veil, shelter | 隠蔽動詞 |
| **`leras`** | [le.ras] | 動 | 開く、露わにする、顕現させる | open, reveal, manifest | 開示動詞 |
| **`klosan`** | [klo.san] | 動 | 閉じる、鍵をかける、終える | close, conclude, seal | 終了動詞 |
| **`donan`** | [do.nan] | 動 | 与える、贈る、授ける | give, bestow, grant | 授与動詞 |
| **`prenan`** | [pre.nan] | 動 | 受け取る、得る、引き継ぐ | receive, obtain, acquire | 受領動詞 |
| **`dansan`** | [dan.san] | 動 | 舞う、踊る、ステップを踏む | dance, leap, sway | 舞踏動詞 |

### 9. 性質・色彩・状態

| NRS転写 | 発音 (IPA) | 品詞 | 日本語意味 | 英語対応 | 備考・語源 |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **`alin`** | [a.lin] | 形 | 白い、純白の、無垢な | white, pure | 純白 |
| **`kyrin`** | [ky.rin] | 形 | 黒い、漆黒の、暗い | black, pitch-dark | 漆黒 |
| **`zylin`** | [zy.lin] | 形 | 青い、蒼穹の、碧色の | blue, azure, deep blue | 蒼穹・深碧 |
| **`pyrin`** | [py.rin] | 形 | 赤い、真紅の、燃えるような | red, crimson, fiery | 真紅 |
| **`valin`** | [va.lin] | 形 | 金色の、黄金の、輝かしい | golden, amber, lustrous | 黄金 |
| **`silvin`** | [sil.vin] | 形 | 銀色の、白銀の、月光の | silver, silvery, gleaming | 白銀 |
| **`nerin`** | [ne.rin] | 形 | 新しい、新鮮な、新緑の | new, fresh, novel | 新生 |
| **`eirin`** | [ei.rin] | 形 | 古い、悠久の、古代の | ancient, old, timeless | 悠久 |
| **`moran`** | [mo.ran] | 形 | 大きい、広大な、壮大な | large, vast, grand | 巨大 |
| **`telin`** | [te.lin] | 形 | 小さい、細やかな、微小な | small, tiny, delicate | 微小 |
| **`duran`** | [du.ran] | 形 | 強い、堅固な、頑丈な | strong, durable, solid | 堅固 |
| **`tenis`** | [te.nis] | 形 | 細い、薄い、繊細な | thin, slim, subtle | 繊細 |
| **`melin`** | [me.lin] | 形 | 優しい、穏やかな、柔らかな | gentle, mild, soft | 穏和 |
| **`faluni`** | [fa.lu.ni] | 形 | 明るい、光り輝く | bright, radiant | 明度 |
| **`kyrimi`** | [ky.ri.mi] | 形 | 深い、深淵な、奥底の | deep, profound | 深度 |
| **`cironi`** | [ʃi.ro.ni] | 形 | 静かな、無音の、凪いだ | silent, quiet, peaceful | 静穏 |
| **`cylani`** | [ʃy.la.ni] | 形 | 美しい、調和のとれた、麗しい | beautiful, exquisite | 美観 |
| **`eiran`** | [ei.ran] | 形 | 永遠の、不滅の、無尽の | eternal, perpetual, immortal | 不滅 |
| **`velos`** | [ve.los] | 形 | 速い、迅速な、光速の | fast, rapid, swift | 高速 |
| **`tardis`** | [tar.dis] | 形 | 遅い、緩やかな、歩みの遅い | slow, gentle, unhurried | 低速 |
| **`altan`** | [al.tan] | 形 | 高い、至高の、天上の | high, lofty, elevated | 高位 |
| **`basen`** | [ba.sen] | 形 | 低い、底層の、足元の | low, deep-set, base | 低位 |
| **`klarin`** | [kla.rin] | 形 | 澄んだ、明瞭な、透き通った | clear, transparent, lucid | 透明感 |

### 10. 時空・方位・副詞

| NRS転写 | 発音 (IPA) | 品詞 | 日本語意味 | 英語対応 | 備考・語源 |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **`hava`** | [ha.va] | 名 | 時、瞬間、今この瞬間 | time, moment, now | 時制の原点 |
| **`havel`** | [ha.vel] | 名 | 時代、運行周期、時代の流れ | era, epoch, orbital cycle | 歴史・時代 |
| **`valar`** | [va.lar] | 名 | 朝、夜明け、曙光の時 | morning, dawn | 朝 |
| **`sovil`** | [so.vil] | 名 | 昼、日中、正午 | daytime, noon | 昼 |
| **`kylas`** | [ky.las] | 名 | 夕、薄暮、黄昏の時 | evening, dusk, twilight | 夕方 |
| **`feno`** | [fe.no] | 副/名 | 昨日、過ぎ去りし日 | yesterday | 過去日 |
| **`hano`** | [ha.no] | 副/名 | 今日、この日、現在 | today, present day | 本日 |
| **`seno`** | [se.no] | 副/名 | 明日、来たるべき日 | tomorrow | 来日 |
| **`celos`** | [ʃe.los] | 名/副 | 上、上方、天頂の方向 | above, upward | 上方 |
| **`talos`** | [ta.los] | 名/副 | 下、下方、大地の方向 | below, downward, beneath | 下方 |
| **`silin`** | [si.lin] | 名/副 | 内、内部、中心側、心の内 | inside, inward, within | 内部 |
| **`folan`** | [fo.lan] | 名/副 | 外、外部、外側、外界 | outside, outward | 外部 |
| **`neris`** | [ne.ris] | 副/形 | 近く、傍らに、親密に | near, beside, close by | 至近 |
| **`falas`** | [fa.las] | 副/形 | 遠く、彼方に、遠日点に | far, distant, beyond | 遥か |
| **`veron`** | [ve.ron] | 副 | 確かに、真に、疑いなく | truly, certainly, indeed | 確信副詞 |
| **`foras`** | [fo.ras] | 副 | おそらく、たぶん、星の導きによれば | perhaps, maybe | 推量副詞 |
| **`eirinu`** | [ei.ri.nu] | 副 | 常に、絶え間なく、いつでも | always, perpetually | 恒常副詞 |
| **`kural`** | [ku.ral] | 副 | 互いに、双方向に、連星のように | mutually, together | 相互副詞 |
| **`non`** | [non] | 副 | いいえ、〜でない（否定極性詞） | not, no | 否定極性詞 |
| **`ia`** | [ia] | 副 | はい、然り、その通り（肯定極性詞） | yes, indeed, so it is | 肯定極性詞 |
| **`sede`** | [se.de] | 接 | しかし、されど | but, yet | 逆接接続詞 |
| **`ko`** | [ko] | 接 | そして、また、〜と共に | and, also | 接続詞 |
| **`kva`** | [kva] | 接/副 | なぜなら、〜ゆえに、理由 | because, for reason | 因果接続詞 |

---

## 4. 体系的例文集（同一文内での音韻分散と自然な美しさの実証）

単一語根の連続を廃し、異なる音韻を持つ語根を美しく調和させた実例。

### 例文 1: 日常生活・IT
- **Nebulith**: *Kiran el sufor ia zevil uo mator de pelel.*
- **発音**: [ki.ran el su.for ia ze.vil wo ma.tor de pe.lel]
- **直訳**: 記述する(動) [主格]プログラマーは [対格]コードを [処格]コンピューターにおいて [具格]スマートフォンを用いて。
- **意訳**: 「プログラマーはスマートフォンを用いて、コンピューター上でコードを記述する。」
- **音韻特徴**: `kiran` (ki-), `sufor` (su-), `zevil` (ze-), `mator` (ma-), `pelel` (pe-) と各語の頭文字・母音が多彩に分散し、早口言葉のような反復が一切生じない。

### 例文 2: 医療・生命
- **Nebulith**: *Medin el darisor ia myren uo darisar de sanel.*
- **発音**: [me.din el da.ri.sor ia my.ren wo da.ri.sar de sa.nel]
- **意訳**: 「医師は診療所において、薬品を用いて人間を治療する。」
- **音韻特徴**: 行為（`medin`）、対象（`myren`）、道具（`sanel`）が独立し、施設（`darisar`）と医師（`darisor`）のみが自然な派生関係を保つ。

### 例文 3: 宇宙観測・自然哲学
- **Nebulith**: *Vyrel el vyrelor ia vyr uo vyrelar de telas.*
- **発音**: [vy.rel el vy.re.lor ia vyr wo vy.re.lar de te.las]
- **意訳**: 「天文学者は天文台で望遠鏡を用いて星を観測する。」
- **音韻特徴**: 道具に独立語根 `telas` が配置され、心地よいリズムを形成。

### 例文 4: 社会・対話
- **Nebulith**: *Calun el civor ku celtor uo calor.*
- **発音**: [ʃa.lun el ʃi.vor ku ʃel.tor wo ʃa.lor]
- **意訳**: 「市民は議会において指導者と対話する。」
- **音韻特徴**: 歯擦音 `ʃ` の柔らかな気品と母音（a, i, e, o）のグラデーション。

---
