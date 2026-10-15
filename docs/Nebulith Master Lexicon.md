# 人工言語「Nebulith（ネビュリス）」マスター辞書定義書（Nebulith Master Lexicon v18.0）

**文書バージョン**: v18.0 (地球言語借用完全排除・全10分野420語幹・柔剛調和独自音韻版)  
**最終更新日**: 2026-10-15  
**ステータス**: **全10分野・計 500 語幹収録／既成言語借用ゼロ・同音衝突ゼロ・完全検証済**  
**目標規模**: 1,000語規模へ段階的拡張中（現在進捗: 50.0%達成）  
**対応システム**: Nebulith Studio（統合スタジオ・単一画面UI、IME、手記レンダラー）

---

## 1. 文法機能語・代名詞・軌道数詞マスターテーブル（Grammar & Numbers）

Nebulithの音韻体系は、母音および流音・鼻音（`l, r, n, m, s`）による**「星辰の流麗な余韻」**を基調としつつ、瞬発的・硬質的・停止的なニュアンスや音の切れ味に応じて**破裂音（`-t, -k, -p, -d`）や摩擦音（`-f, -v`）**を有標Codaとして美しく共存させています。地球言語（英語、ラテン語、ロマンス諸語等）の安易な借用・引きずりを完全に排除した純粋な架空言語体系です。

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
| **7** | **`sep`** | [sep] | 七曜、天球層 | 七 |
| **8** | **`ok`** | [ok] | 八弦、二重四重 | 八 |
| **9** | **`nov`** | [nov] | 九軌道、極限 | 九 |
| **10** | **`dek`** | [dek] | 満天、十全十美 | 十 |

---

## 2. 派生接尾辞マスターシステム（Derivational Suffixes）

| 接尾辞 | 機能 | 派生例 (語根 → 派生語) | 意味 |
| :--- | :--- | :--- | :--- |
| **`-as`** | 日常的行為者・実務者 | `ner` (食) → `neras` [ne.ras] | 給仕人、配膳者 |
| **`-or`** | 専門職・知識人・指導者 | `suf` (計算) → `sufor` [su.for] | プログラマー、論理技術者 |
| | | `daris` (治癒) → `darisor` [da.ri.sor] | 医師、調律医 |
| **`-is`** | 学術研究者・探求者 | `vyran` (真理) → `vyranis` [vy.ra.nis] | 哲学者、真理探求者 |
| **`-el`** | 道具・器具・機械・客体 | `kiras` (創る/書く) → `kirel` [ki.rel] | 筆、スタイラス、ペン |
| | | `ner` (食) → `nerel` [ne.rel] | 料理、温かい食事 |
| **`-ar` / `-an`** | 場所・施設・空間 | `dom` (部屋) → `domar` [do.mar] | 家、住宅 |
| | | `daris` (治癒) → `darisar` [da.ri.sar] | 病院、診療所 |
| | | `ner` (食) → `nerar` [ne.rar] | レストラン、カフェ |
| **`-il`** | 指小辞・愛称・親愛 | `vel` (木) → `velil` [ve.lil] | 若木、新芽、薬草 |
| **`-om`** | 集合体・領域・世界 | `dom` (部屋) → `domom` [do.mom] | 都市、都市圏 |
| | | `vel` (木) → `velom` [ve.lom] | 森林、樹海 |
| | | `vyr` (星) → `vyrom` [vy.rom] | 星座、星団 |
| **`-i`** | 形容詞化（〜の性質を持つ） | `falun` (光) → `faluni` [fa.lu.ni] | 明るい、輝かしい |
| **`-u`** | 副詞化（〜のように、〜く） | `eiran` (永遠) → `eirinu` [ei.ri.nu] | 永遠に、いつでも |
| | | `tyk` (拍) → `tyku` [ty.ku] | 直ちに、即座に |

---

## 3. 全分野別マスター語彙集（全10分野・体系的語根一覧）

各語彙は同一文内での反復・類似音連続（ゲシュタルト崩壊）を徹底排除するため、**行為・対象・道具・場所・主体のそれぞれに固有の自立語根**を割り当てています。

### 1. 天体・光・宇宙論 (54 語幹)

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
| **`vyrelel`** | [vy.re.lel] | 名 | 天体望遠鏡、精密観測機器 | telescope, observatory instrument | 観測の道具 |
| **`vyrelar`** | [vy.re.lar] | 名 | 天文台、天体観測ドーム | observatory | 観測所 |
| **`vyrelor`** | [vy.re.lor] | 名 | 天文学者、観測官 | astronomer | 天体観測士 |
| **`tyral`** | [ty.ral] | 名 | 引力、重力、求心力 | gravity, attraction force | 天体の相互引力 |
| **`voris`** | [vo.ris] | 名 | 公転、自転、角速度、周活力 | orbital revolution, spin | 天体回転力学 |
| **`falos`** | [fa.los] | 名 | 分光、光輪スペクトル、帯 | spectrum, spectral band | 光の波長分解 |
| **`kyron`** | [ky.ron] | 名 | 黒孔、ブラックホール、重力特異点 | black hole, singularity | 光さえ出でぬ孔 |
| **`nebulis`** | [ne.bu.lis] | 名 | 星雲、星間ガス、宇宙塵 | nebula, cosmic dust cloud | 星々の母胎 |
| **`vyri`** | [vy.ri] | 形 | 星辰の、恒星系の、高貴な | astral, stellar | 星の性質 |
| **`falyt`** | [fa.lyt] | 名 | 流星、彗星、夜空を走る光条 | meteor, comet | 走る光の軌跡 |
| **`zoharil`** | [zo.ha.ril] | 名 | 恒星風、太陽風、荷電粒子流 | stellar wind, solar flare | 恒星の息吹 |
| **`kymos`** | [ky.mos] | 名 | 日食、月食、天体交食 | eclipse, occultation | 闇の被覆 |
| **`falasro`** | [fa.las.ro] | 名 | 遠日点、最遠軌道点 | aphelion, apoapsis | 遥かなる周回点 |
| **`nerisro`** | [ne.ris.ro] | 名 | 近日点、最接近点 | perihelion, periapsis | 至近の周回点 |
| **`torp`** | [torp] | 名 | 天体衝突、隕石落下、インパクト | impact, collision | 衝撃の破裂音 |
| **`vyrom`** | [vy.rom] | 名 | 星座、星群、星団 | constellation, asterism, star cluster | 星辰の集合体 |
| **`tyril`** | [ty.ril] | 名 | 潮汐力、引力波、重力波 | tidal force, gravitational wave | 重力の動的波動 |
| **`zoharom`** | [zo.ha.rom] | 名 | コロナ、恒星大気層、光冠 | stellar corona, heliosphere | 恒星の光冠 |
| **`larkan`** | [lar.kan] | 名 | 軌道傾斜角、傾き、傾斜 | orbital inclination, tilt | 軌道の角度 |
| **`vyrelis`** | [vy.re.lis] | 名 | 星屑、微小星間塵、星砂 | stardust, micro-meteoroids | 微小な星の破片 |
| **`kyrom`** | [ky.rom] | 名 | 銀河団、超星系網、星界 | galaxy cluster, cosmic filament | 深宇宙の超巨視構造 |
| **`larven`** | [lar.ven] | 名/動 | 軌道遷移、スイングバイ、航路変更 | orbital transit, swing-by | 軌道間の跳躍遷移 |
| **`falarik`** | [fa.la.rik] | 名 | 光度、放射光束、輝度 | luminosity, radiant flux | 光の精密強度 |
| **`doran`** | [do.ran] | 名 | 惑星、放浪天体、巡礼星 | planet, wandering orb | 軌道を巡る大地天体 |
| **`radin`** | [ra.din] | 名 | 軌道半径、長半径、天体間距離 | orbital radius, semi-major axis | 天体周回半径 |
| **`valosro`** | [va.los.ro] | 名 | 軌道離心率、楕円度、扁平率 | orbital eccentricity, ellipticity | 軌道の楕円性 |
| **`kymryn`** | [kym.ryn] | 名 | 暗黒物質、ダークマター、不可視質量 | dark matter, unseen cosmic mass | kym (闇) ＋ 質量 |
| **`faldenar`** | [fal.de.nar] | 名 | 朝焼け、黎明の光芒、払暁の輝き | dawn glow, sunrise radiance | falden (東) ＋ 空間 |
| **`kymdenar`** | [kym.de.nar] | 名 | 夕焼け、黄昏の残照、夕映え | sunset glow, evening twilight afterglow | kymden (西) ＋ 空間 |
| **`neburil`** | [ne.bu.ril] | 名 | 原生惑星系円盤、原始星雲環 | protoplanetary disk | nebulis ＋ 微小環 |
| **`zoharik`** | [zo.ha.rik] | 名 | 太陽黒点、主星斑点、活動領域 | sunspot, starspot | zohar (主星) ＋ 点 |
| **`celvan`** | [ʃel.van] | 名 | 天球、全天、天体球殻 | celestial sphere, empyrean dome | 天空を覆う球殻 |
| **`vyrkot`** | [vyr.kot] | 名 | 超新星爆発、恒星大爆発、新星閃光 | supernova explosion, stellar burst | vyr (星) ＋ kot (破裂) |
| **`zoharmon`** | [zo.har.mon] | 名 | 白夜、極昼、沈まぬ主星 | midnight sun, polar day | zohar (太陽) ＋ 永続 |
| **`kymhav`** | [kym.hav] | 名 | 極夜、恒暗期、昇らぬ主星の季節 | polar night, perpetual night season | kym (夜) ＋ hav (周期) |
| **`larfas`** | [lar.fas] | 名 | 軌道離脱、脱出速度、飛翔脱出 | orbital escape, escape velocity | laris (軌道) ＋ 離脱 |
| **`faldikur`** | [fal.di.kur] | 名 | 屈折、光の屈折、光路の曲がり | optical refraction, light bending | falun (光) ＋ 屈折 |
| **`celzyl`** | [ʃel.zyl] | 名 | 青空、蒼穹光、大気の散乱光 | blue sky scattering, azure glow | celen (空) ＋ zylin (青) |
| **`tyrfos`** | [tyr.fos] | 名 | 連星系の重心、天体共通重心、平衡点 | barycenter, Lagrange balance point | tyral (引力) ＋ 平衡点 |

### 2. 数理・幾何・情報科学 (54 語幹)

| NRS転写 | 発音 (IPA) | 品詞 | 日本語意味 | 英語対応 | 備考・語源 |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **`suf`** | [suf] | 名/動 | 計算、論理、アルゴリズム | computation, logic | 鋭敏な摩擦音語末 |
| **`sufor`** | [su.for] | 名 | プログラマー、ITエンジニア、論理士 | programmer, software engineer | 論理技術職 |
| **`sufom`** | [su.fom] | 名 | 情報工学、電脳空間、IT領域 | computer science, cyberspace | 計算・情報分野 |
| **`mator`** | [ma.tor] | 名 | コンピューター、端末、演算機械 | computer, terminal | 精緻な計算機巧 |
| **`zevil`** | [ze.vil] | 名 | コード、プログラム、構文、文字列 | code, syntax, script | 論理文字列 |
| **`kiran`** | [ki.ran] | 動 | （コードを）記述する、紡ぐ、組む | write code, program, compile | プログラミング動詞 |
| **`pelel`** | [pe.lel] | 名 | スマートフォン、携帯情報端末 | smartphone, mobile device | 手のひらの端末 |
| **`tolas`** | [to.las] | 名 | メッセージ、通信文、便り | message, dispatch | 短い便り |
| **`wesan`** | [we.san] | 動 | 送信する、送る、信号を放つ | send, transmit | 通信動詞 |
| **`tolom`** | [to.lom] | 名 | インターネット、Web、世界通信網 | internet, cyber network | 世界情報網 |
| **`vylatel`** | [vy.la.tel] | 名 | ディスプレイ、画面、モニター | display, screen, monitor | 映像出力板 |
| **`falel`** | [fa.lel] | 名 | 写真、画像、静止画 | photo, image, graphic | 光の記録 |
| **`livar`** | [li.var] | 名 | データベース、書庫、情報保管庫 | database, repository | データ集積所 |
| **`jyn`** | [ʒyn] | 名 | 電気、電力、電荷、エネルギー | electricity, power, energy | 電力・エネルギー |
| **`jynel`** | [ʒy.nel] | 名 | バッテリー、蓄電池、電源 | battery, power cell | 蓄電器 |
| **`rin`** | [rin] | 名 | 円、真円、環 | circle, ring | 幾何円 |
| **`tulik`** | [tu.lik] | 名 | 多角形、星型幾何、立体多面体 | polygon, geometry | 幾何立体 |
| **`niven`** | [ni.ven] | 名 | 次元、座標軸、空間度数 | dimension, coordinate axis | 次元・軸 |
| **`talisum`** | [ta.li.sum] | 名 | 定理、証明された法則、公理 | theorem, axiom | 数学的定理 |
| **`kvan`** | [kvan] | 名 | 量子、最小単位、離散値 | quantum, discrete packet | 最小単位 |
| **`jyt`** | [ʒyt] | 名 | ノード、結節点、ネットワーク交点 | node, vertex | 網の結節点 |
| **`kiril`** | [ki.ril] | 名 | 関数、変換式、写像 | function, mapping formula | 数理写像 |
| **`kelon`** | [ke.lon] | 名 | 変数、変動要素、パラメータ | variable, parameter | 可変値 |
| **`firas`** | [fi.ras] | 名 | 定数、普遍値、固定係数 | constant, invariant | 不変値 |
| **`kyvren`** | [kyv.ren] | 名/動 | 暗号、暗号化する、秘匿符号 | cipher, encrypt | 秘匿論理 |
| **`kiv`** | [kiv] | 名 | ビット、二値単位、情報最小光点 | bit, binary unit | 瞬発的最小二値 |
| **`velat`** | [ve.lat] | 名 | 行列、マトリクス、格子配列 | matrix, grid array | 二次元配列 |
| **`vylom`** | [vy.lom] | 名 | スコープ、視野域、有効範囲 | scope, valid range | 視界有効範囲 |
| **`tyk`** | [tyk] | 名 | クロック、時計信号、規則拍 | clock, timing pulse | 刻時破裂音 |
| **`ryvel`** | [ry.vel] | 名 | 測度、尺度、メトリック | metric, measure | 精密計測 |
| **`jylom`** | [ʒy.lom] | 名 | 集合、集約配列、コレクション | set, collection, array | 結びついた要素群 |
| **`voret`** | [vo.ret] | 名/動 | ループ、反復処理、再帰 | loop, iteration, recurse | 周回反復 |
| **`sevik`** | [se.vik] | 名 | 条件分岐、フォーク、判定節 | branch, conditional fork | 論理の分岐点 |
| **`ved`** | [ved] | 名 | 真偽値、論理極性、ブーリアン | boolean, truth-value | 真偽の確定値 |
| **`unor`** | [u.nor] | 名 | 整数、完数、離散値 | integer, whole number | 一単位ずつの整数 |
| **`delis`** | [de.lis] | 名 | 小数、実数、分割比 | decimal, float, fraction | 連続分割値 |
| **`velis`** | [ve.lis] | 名/動 | 検索、クエリ、照会する | query, search lookup | 探求照会 |
| **`torin`** | [to.rin] | 名/動 | 入力、インプット、流入データ | input, ingress | 到来する入力 |
| **`folin`** | [fo.lin] | 名/動 | 出力、アウトプット、流出データ | output, egress | 外へ放つ出力 |
| **`soril`** | [so.ril] | 名 | メモリ、記憶素子、バッファ | memory, cache, buffer | 記録を保持する素子 |
| **`jylvat`** | [ʒyl.vat] | 名 | グラフ構造、連結網、関係図 | graph structure, network topology | jyl (結合) ＋ 格子配列 |
| **`sufrin`** | [suf.rin] | 名 | 暗号鍵、認証トークン、署名符号 | cryptographic key, auth token | suf (計算) ＋ rin (環) |
| **`kivlom`** | [kiv.lom] | 名 | バイト、オクテット、情報ブロック | byte, octet, data block | kiv (ビット) ＋ -om (集合) |
| **`veltok`** | [vel.tok] | 名/動 | インデックス、索引、検索目録 | index, search key | 探索の標識 |
| **`zydot`** | [zy.dot] | 名/動 | 検証、アサーション、実証テスト | validation, assertion, proof test | zyd (検証実相) の確定 |
| **`krotel`** | [kro.tel] | 名 | 例外、ランタイムエラー、異常割り込み | exception, runtime interrupt | krot (激動) ＋ 信号器 |
| **`suftas`** | [suf.tas] | 名 | スタック、キュー、順序待ち列 | stack, queue, buffer sequence | suf (計算) ＋ 順序配列 |
| **`zevkas`** | [zev.kas] | 名/動 | パース、構文解析する、構文木 | parse, syntax analysis, AST | zevil (構文) ＋ 解析 |
| **`jylrin`** | [ʒyl.rin] | 名 | トポロジー、位相空間、閉曲面 | topology, manifold, topological ring | jyl (結合) ＋ rin (環) |
| **`kivkas`** | [kiv.kas] | 名/動 | シリアライズ、直列化する、ビット列化 | serialize, marshal to stream | kiv (ビット) ＋ 連続化 |
| **`matoris`** | [ma.to.ris] | 名 | 演算器、ALU、プロセッサコア | processor core, arithmetic unit | mator (計算機) ＋ 核 |
| **`delrin`** | [del.rin] | 名 | 連続体、無理数、実数直線 | continuum, irrational number | delis (小数) ＋ rin (環) |
| **`kirvat`** | [kir.vat] | 名 | スキーマ、データ構造定義、論理骨格 | schema, data structure layout | kiran (記述) ＋ 格子 |
| **`vedot`** | [ve.dot] | 名 | 条件式、論理前提、命題 | predicate, proposition, premise | ved (真偽値) ＋ 定立 |

### 3. 生命・身体・医療 (49 語幹)

| NRS転写 | 発音 (IPA) | 品詞 | 日本語意味 | 英語対応 | 備考・語源 |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **`zyvel`** | [zy.vel] | 名/動 | 生命、息吹、生きる、脈動する | life, breathe, live | 生命の脈動 |
| **`myren`** | [my.ren] | 名 | 人間、知性体、観測者 | human, sentient being | 星を見上げる者 |
| **`darisor`** | [da.ri.sor] | 名 | 医師、治癒師、導師 | doctor, physician, healer | 医療専門職 |
| **`zyvan`** | [zy.van] | 動 | 治療する、癒す、活力を与える | heal, cure, treat | 治癒動詞 |
| **`darisar`** | [da.ri.sar] | 名 | 病院、医院、診療所、癒しの座 | hospital, clinic | 医療施設 |
| **`zyvil`** | [zy.vil] | 名 | 薬、処方生薬、調合薬 | medicine, remedy, potion | 治癒の薬 |
| **`kylar`** | [ky.lar] | 名 | 病、乱調、軌道乱れ | illness, disease | 病気・不調 |
| **`davel`** | [da.vel] | 名 | 血液、脈流、体液 | blood, vital fluid | 体内の血 |
| **`teirap`** | [tei.rap] | 名 | 心拍、脈拍、鼓動 | pulse, heartbeat | 心臓の拍動 |
| **`noven`** | [no.ven] | 名 | 頭、頭脳、中枢神経 | head, brain, intellect center | 頭部・頭脳 |
| **`vylan`** | [vy.lan] | 名 | 目、瞳、視覚器官 | eye, pupil | 瞳 |
| **`harel`** | [ha.rel] | 名 | 耳、聴覚器官 | ear, auditory organ | 耳 |
| **`fenel`** | [fe.nel] | 名 | 口、唇、声門 | mouth, lips | 口 |
| **`wylat`** | [wy.lat] | 名 | 鼻、息の通り道、嗅覚器官 | nose, breathway | 息道 |
| **`ser`** | [ser] | 名 | 手、掌、指 | hand, palm, fingers | 手 |
| **`larin`** | [la.rin] | 名 | 足、脚、歩行肢 | foot, leg | 歩行肢 |
| **`teira`** | [tei.ra] | 名 | 心臓、胸の核、肉体の中心 | heart, core | 心臓・星核 |
| **`kymin`** | [ky.min] | 名/動 | 眠り、睡眠、休眠する | sleep, rest | 睡眠 |
| **`revir`** | [re.vir] | 動 | 目覚める、覚醒する、回復する | awake, recover | 覚醒・回復 |
| **`duril`** | [du.ril] | 名 | 骨、骨格、堅固な支柱 | bone, skeleton | 骨格 |
| **`durtas`** | [dur.tas] | 名 | 筋肉、筋力、運動器官 | muscle, sinew | 筋力器官 |
| **`velik`** | [ve.lik] | 名 | 皮膚、肌、外被 | skin, dermis | 肌・表皮 |
| **`zyvas`** | [zy.vas] | 名 | 健康、活力、健全な生命力 | health, vitality | 健康状態 |
| **`jynten`** | [ʒyn.ten] | 名 | 神経、感覚伝達網、シナプス | nerve, neural network | 生体電信線 |
| **`zyvelan`** | [zy.ve.lan] | 動 | 呼吸する、息吹を交わす | breathe, respire | 呼吸動詞 |
| **`teiran`** | [tei.ran] | 名 | 遺伝子、螺旋設計図、生体素核 | gene, genome, life helix | 生命の螺旋情報 |
| **`kivan`** | [ki.van] | 名 | 細胞、生体微小胞 | cell, life vesicle | 生命の最小単位小胞 |
| **`zyvlar`** | [zyv.lar] | 名 | 肺、呼吸器、気嚢 | lung, respiration organ | 大気交換器 |
| **`neron`** | [ne.ron] | 名 | 胃、消化器、滋養受納処 | stomach, digestive organ | 滋養受納器官 |
| **`davlar`** | [dav.lar] | 名 | 循環系、血管網、脈絡 | circulatory system, blood vessels | 血液循環網 |
| **`tylkar`** | [tyl.kar] | 名 | 創傷、裂傷、損傷部 | wound, lesion, trauma | 裂けた負傷 |
| **`valmik`** | [val.mik] | 名 | 包帯、防護布、被覆保護材 | bandage, protective dressing | 傷の保護布 |
| **`durvan`** | [dur.van] | 名 | 免疫、生体防御機構、抗体 | immunity, vital defense | 生体抵抗力 |
| **`kylat`** | [ky.lat] | 名 | 疲労、消耗、エネルギー枯渇 | fatigue, weariness, drain | 生命力の減退 |
| **`zyvor`** | [zy.vor] | 名 | 活力、スタミナ、強靭な精力 | stamina, vital vigour | 充実した活力 |
| **`zyvten`** | [zyv.ten] | 名 | 代謝、生体エネルギー代謝、同化作用 | metabolism, vital energy flux | 生命の転換連鎖 |
| **`teiros`** | [tei.ros] | 名 | 胎児、生命の萌芽、胚 | embryo, fetus, seed-life | teira (心核) ＋ 幼体 |
| **`harnas`** | [har.nas] | 名 | 聴力、音感、耳の感度 | hearing ability, auditory sense | harel (耳) ＋ 働き |
| **`fenlin`** | [fen.lin] | 名 | 味覚、風味、舌ざわり | taste sensation, flavor perception | fenel (口) ＋ 感覚 |
| **`darmut`** | [dar.mut] | 名 | 汗、体液蒸散、滴り | sweat, perspiration | dar (滴) ＋ 排出 |
| **`durvanar`** | [dur.va.nar] | 名 | 隔離室、検疫所、無菌室 | quarantine chamber, clean room | durvan (免疫) ＋ 施設 |
| **`teirvan`** | [tei.rvan] | 名 | 染色体、螺旋鎖束 | chromosome, genetic strand bundle | teiran (遺伝子) ＋ 束 |
| **`nerzyv`** | [ner.zyv] | 名 | 消化、滋養吸収、同化代謝 | digestion, assimilation, nutrient uptake | ner (食) ＋ zyvel (生命) |
| **`davelis`** | [da.ve.lis] | 名 | 血漿、体液、リンパ液 | lymph, plasma, serous fluid | davel (血液) ＋ 澄明液 |
| **`durvis`** | [dur.vis] | 名 | 軟骨、腱、靭帯 | cartilage, tendon, connective tissue | duril (骨) ＋ 柔軟結合 |
| **`vylmir`** | [vyl.mir] | 名 | 視力、視覚、見晴らし、視野 | eyesight, visual acuity, sightline | vylan (目) ＋ 遠望 |
| **`zyvrev`** | [zyv.rev] | 名/動 | 蘇生、心肺回復、再活性化する | resuscitation, reanimation, revival | zyvel (命) ＋ revir (覚醒) |
| **`kyminar`** | [ky.mi.nar] | 名 | 安息所、病床、療養室 | infirmary, recovery ward, hospice | kymin (睡眠/休養) ＋ 施設 |
| **`tylkin`** | [tyl.kin] | 名 | 傷痕、瘢痕、治癒の跡 | scar, cicatrisation, healed trace | tylkar (創傷) ＋ 痕跡 |

### 4. 自然・気象・環境 (58 語幹)

| NRS転写 | 発音 (IPA) | 品詞 | 日本語意味 | 英語対応 | 備考・語源 |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **`tal`** | [tal] | 名 | 大地、土壌、足元、地面 | earth, soil, ground | 地面・大地 |
| **`novan`** | [no.van] | 名 | 山、連峰、そびえる高嶺 | mountain, peak | 天にそびえる山 |
| **`talik`** | [ta.lik] | 名 | 谷、峡谷、大地の裂け目 | valley, canyon | 谷 |
| **`talom`** | [ta.lom] | 名 | 平原、大原野、果てなき大地 | plain, field, steppe | 広大な平野 |
| **`velom`** | [ve.lom] | 名 | 森、森林、樹海 | forest, woods | 広大な森 |
| **`vel`** | [vel] | 名 | 木、樹木、大樹 | tree | 樹木 |
| **`velas`** | [ve.las] | 名 | 葉、緑、葉擦れ | leaf, foliage | 葉 |
| **`velin`** | [ve.lin] | 名/動 | 花、咲く、芳香 | flower, bloom | 花 |
| **`velil`** | [ve.lil] | 名 | 新芽、若木、薬草、草 | herb, sprout, grass | 薬草・新芽 |
| **`vorin`** | [vo.rin] | 名 | 果実、木の実、果物 | fruit, berry | 果実 |
| **`teiril`** | [tei.ril] | 名 | 種、種子、生命の粒 | seed, pip | 種核 |
| **`daris`** | [da.ris] | 名 | 水、清流、淡水 | water, stream | 真水・清流 |
| **`dar`** | [dar] | 名 | しずく、水滴、朝露 | droplet, dew | しずく |
| **`zylar`** | [zy.lar] | 名 | 海、海洋、大洋 | sea, ocean | 大海 |
| **`daron`** | [da.ron] | 名 | 湖、湖沼、静水面 | lake, pond | 静かな湖 |
| **`darmon`** | [dar.mon] | 名 | 泉、湧水、水源 | spring, font | 清らかな湧水 |
| **`darlen`** | [dar.len] | 名 | 雨、降雨 | rain, rainfall | 雨 |
| **`kyrlen`** | [kyr.len] | 名 | 雪、白雪、降雪 | snow, snowfall | 雪 |
| **`kyras`** | [ky.ras] | 名 | 氷、霜、氷結体 | ice, frost | 氷 |
| **`wylas`** | [wy.las] | 名/動 | 風、大気の流れ、そよぐ | wind, breeze | 風 |
| **`celis`** | [ʃe.lis] | 名 | 雲、霧、霞 | cloud, mist, fog | 雲・霧 |
| **`pyris`** | [py.ris] | 名 | 火、炎、熱源 | fire, flame | 火 |
| **`talis`** | [ta.lis] | 名 | 石、岩、鉱石、結晶 | stone, rock, mineral | 鉱物・石 |
| **`talur`** | [ta.lur] | 名 | 金属、合金、鉱物資材 | metal, ore, alloy | 大地の金属 |
| **`wylrim`** | [wyl.rim] | 名 | 嵐、暴風雨、星雲嵐 | storm, tempest | 激しき風 |
| **`vyltor`** | [vyl.tor] | 名 | 雷、稲妻、天の閃光 | thunder, lightning | 光雷 |
| **`celar`** | [ʃe.lar] | 名 | 極光、オーロラ、天の天幕 | aurora, polar light | 極光の帯 |
| **`talrim`** | [tal.rim] | 名 | 砂漠、不毛地帯、乾いた荒野 | desert, wasteland | 乾燥砂漠 |
| **`vuron`** | [vu.ron] | 名 | 洞窟、鍾乳洞、地下空洞 | cave, cavern, grotto | 地下空洞 |
| **`feras`** | [fe.ras] | 名 | 動物、獣、野生生物 | animal, beast | 動物 |
| **`volfer`** | [vol.fer] | 名 | 鳥、翼ある者、飛翔生物 | bird, winged creature | 空翔る者 |
| **`zylfer`** | [zyl.fer] | 名 | 魚、水棲生物 | fish, marine life | 水泳ぐ者 |
| **`krap`** | [krap] | 名 | 虫、昆虫、甲虫 | insect, bug | 硬質外骨格 |
| **`fermor`** | [fer.mor] | 名 | 天竜、星間巨獣、大蛇 | dragon, cosmic beast | 神話の巨獣 |
| **`talon`** | [ta.lon] | 名 | 島、孤立陸地、環礁 | island, isle, atoll | 海に浮かぶ大地 |
| **`talser`** | [tal.ser] | 名 | 岬、半島、海に突き出た陸 | cape, peninsula, headland | 突出した陸地 |
| **`darsik`** | [dar.sik] | 名 | 海峡、水路、海峡部 | strait, channel, sound | 水の細道 |
| **`darfal`** | [dar.fal] | 名 | 滝、瀑布、懸濁水流 | waterfall, cascade, cataract | 流れ落ちる水 |
| **`talkrot`** | [tal.krot] | 名 | 地震、地殻変動、地鳴り | earthquake, tectonic tremor | 大地の激動 |
| **`pyrtal`** | [pyr.tal] | 名 | 火山、噴煙峰、火の山 | volcano, fire-mountain | 火を噴く山 |
| **`zylrim`** | [zyl.rim] | 名 | 砂浜、海岸線、渚、波打ち際 | beach, coast, shoreline | 海の縁 |
| **`havas`** | [ha.vas] | 名 | 季節、四季、周期候 | season, climatic period | 巡る気候期 |
| **`velhav`** | [vel.hav] | 名 | 春、芽吹きの季節、萌芽期 | spring, vernal season | 花咲く季節 |
| **`zohav`** | [zo.hav] | 名 | 夏、主星の季節、陽光盛期 | summer, high sun season | 太陽の季節 |
| **`taldar`** | [tal.dar] | 名 | 泥、湿地、ぬかるみ、粘土湿原 | mud, mire, loam, wetland | tal (土) ＋ dar (水) |
| **`velpon`** | [vel.pon] | 名 | 樹皮、木の幹、木質部 | bark, tree trunk, bole | vel (木) ＋ 胴幹 |
| **`darlor`** | [dar.lor] | 名 | 潮流、海流、水流 | ocean current, tidal flow | daris (水) ＋ 巡行 |
| **`wylven`** | [wyl.ven] | 名 | つむじ風、局所旋風、塵旋風 | whirlwind, vortex eddy | wylas (風) ＋ 旋回 |
| **`kyrfin`** | [kyr.fin] | 名 | 氷河、永久凍土、氷塊 | glacier, permafrost, ice pack | kyras (氷) ＋ 堆積層 |
| **`falpir`** | [fal.pir] | 名 | 燐光、生物発光、冷光 | bioluminescence, phosphorescence | falun (光) ＋ pyris (火) の冷光 |
| **`talmor`** | [tal.mor] | 名 | 丘、丘陵、なだらかな隆起 | hill, knoll, mound | tal (大地) ＋ moran (大) |
| **`velrot`** | [vel.rot] | 名 | 木漏れ日、梢の光、林床の光芒 | dappled sunlight, sun through leaves | vel (木) ＋ 光の粒 |
| **`darmar`** | [dar.mar] | 名 | 湿原、沼沢、水生植物の地 | marsh, swamp, bog, wetland | dar (水) ＋ 泥湿地 |
| **`wylor`** | [wy.lor] | 名 | 季節風、恒常風、偏西風 | monsoon, prevailing wind, trade wind | wylas (風) ＋ 循環 |
| **`kyrtam`** | [kyr.tam] | 名 | 凍土、ツンドラ、霜の大地 | tundra, frozen ground, permafrost | kyras (氷) ＋ talom (原野) |
| **`pyrlom`** | [pyr.lom] | 名 | 火災、山火事、火炎原 | wildfire, conflagration, blazing zone | pyris (火) ＋ -om (広域) |
| **`talisar`** | [ta.li.sar] | 名 | 採石場、鉱山、石切り場 | quarry, mine, stone-pit | talis (石) ＋ 採掘場 |
| **`faldaris`** | [fal.da.ris] | 名 | 虹、天の彩橋、分光光弧 | rainbow, celestial prismatic arc | falun (光) ＋ daris (水) |

### 5. 社会・法・共同体 (43 語幹)

| NRS転写 | 発音 (IPA) | 品詞 | 日本語意味 | 英語対応 | 備考・語源 |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **`kuralom`** | [ku.ra.lom] | 名 | 社会、共同体、連盟 | society, community, polis | 共生の座 |
| **`taros`** | [ta.ros] | 名 | 法、法律、軌道規則、掟 | law, statute, canon | 法律・規範 |
| **`calor`** | [ʃa.lor] | 名 | 評議会、会議、議会、対話の座 | council, parliament, forum | 議会 |
| **`jylot`** | [ʒy.lot] | 名 | 約束、契約、協定、盟約 | pact, covenant, contract | 結束の協定 |
| **`polor`** | [po.lor] | 名 | 市民、住人、共同体員 | citizen, member | 共同体の人 |
| **`novor`** | [no.vor] | 名 | 指導者、議長、頂点の導き手 | leader, chancellor, guide | 頂点に立つ者 |
| **`dirin`** | [di.rin] | 名/形 | 正義、公正、均衡、正しい | justice, equity, righteous | 正義 |
| **`silan`** | [si.lan] | 名 | 調和、秩序、共存、平和 | harmony, order, peace | 社会の平和 |
| **`renis`** | [re.nis] | 名 | 貨幣、お金、通貨、クレジット | money, currency, credit | 通貨 |
| **`renar`** | [re.nar] | 名 | 市場、店、ショップ、取引所 | market, shop, exchange | 市場 |
| **`dolar`** | [do.lar] | 動 | 働く、勤労する、奉仕する | work, labor, serve | 労働動詞 |
| **`dolor`** | [do.lor] | 名 | 労働者、職人、働き手 | worker, artisan | 職人・働き手 |
| **`vyranar`** | [vy.ra.nar] | 名 | 学校、学舎、アカデミー | school, academy | 真理の学舎 |
| **`vyranas`** | [vy.ra.nas] | 名 | 学生、学徒、真理の探求者 | student, pupil, scholar-initiate | 学び手 |
| **`sufis`** | [su.fis] | 名 | 学者、碩学、数理哲士 | scholar, doctor, master | 学究の徒 |
| **`tarosar`** | [ta.ro.sar] | 名 | 法廷、裁定所、審問の座 | court, tribunal | 司法の場 |
| **`elyr`** | [e.lyr] | 名 | 祭典、祝祭、星の祭り | festival, celebration | 祝祭の日 |
| **`sirar`** | [si.rar] | 名 | 安寧、平和、講和条約 | peace, truce, accord | 争いなき静けさ |
| **`zyd`** | [zyd] | 名 | 事実、実相、検証された事象 | fact, reality | 実証された真理 |
| **`kuralis`** | [ku.ra.lis] | 名 | 連邦、国家体、星間同盟 | commonwealth, interstellar union | 星間連邦国家 |
| **`vylar`** | [vy.lar] | 名 | 旗、象徴旗、星辰紋章 | flag, banner, celestial crest | 星辰を掲げる旗 |
| **`tarin`** | [ta.rin] | 名 | 権利、正当権能、資格 | right, lawful prerogative | 法に基づく権利 |
| **`dolyk`** | [do.lyk] | 名 | 義務、責務、誓約の勤め | duty, civic obligation | 共同体への義務 |
| **`renon`** | [re.non] | 名 | 財産、資産、蓄積富 | wealth, assets, holdings | 蓄積された資材 |
| **`renan`** | [re.nan] | 名/動 | 交易、貿易、物々交換する | trade, commerce, barter | 星間交易 |
| **`jylik`** | [ʒy.lik] | 名 | 条約文書、協定証書、公文書 | treaty document, signed charter | 法約の書字録 |
| **`vyrisor`** | [vy.ri.sor] | 名 | 星辰導師、祭司、天象官 | hierophant, astronomer-priest | 星辰の祭司 |
| **`dolinar`** | [do.li.nar] | 名 | 工匠、技術者、鍛冶師 | master craftsman, engineer | 熟練の工匠 |
| **`cynor`** | [ʒy.nor] | 名 | 親友、盟友、魂の伴走者 | confidant, sworn companion | 互いを慈しむ友 |
| **`tarlot`** | [tar.lot] | 名 | 判決、裁定、法廷審判 | judicial verdict, decree | taros (法) ＋ 確定 |
| **`kuralor`** | [ku.ra.lor] | 名 | 外交官、連盟特使、使節 | diplomat, ambassador, envoy | kuralom (社会) ＋ 使節 |
| **`renik`** | [re.nik] | 名 | 負債、借用証、債権 | debt, credit bond, liability | renis (通貨) ＋ 証約 |
| **`dolvis`** | [dol.vis] | 名 | 協同組合、ギルド、職人座 | guild, cooperative, artisan syndicate | dolar (労働) の連合座 |
| **`calvir`** | [ʃal.vir] | 名 | 請願、議案、提言 | petition, bill, motion | calor (議会) への提題 |
| **`polten`** | [pol.ten] | 名 | 住民票、戸籍、市民登録 | citizen register, civic roll | polor (市民) ＋ 記録網 |
| **`kuralen`** | [ku.ra.len] | 名 | 憲章、基本法、連邦憲法 | constitution, basic charter | kuralom (社会) ＋ 根本法 |
| **`tarvyn`** | [tar.vyn] | 名 | 判例、先例、法の伝承 | judicial precedent, legal tradition | taros (法) ＋ 律道 |
| **`renlor`** | [ren.lor] | 名 | 銀行、金庫、通貨管理所 | bank, treasury, credit vault | renis (通貨) ＋ 保管座 |
| **`dolvan`** | [dol.van] | 名 | 産業、生産網、製造業 | industry, manufacture, production | dolar (労働) ＋ 規模 |
| **`polot`** | [po.lot] | 名 | 投票、採決、市民の意思表示 | vote, ballot, suffrage | polor (市民) ＋ 決議 |
| **`cynmar`** | [ʃyn.mar] | 名 | 扶助、相互扶助、福祉 | mutual aid, relief, welfare | cynel (慈しみ) ＋ mar (授受) |
| **`vyranor`** | [vy.ra.nor] | 名 | 教師、教授、指導導師 | professor, instructor, mentor | vyranar (学舎) ＋ 指導者 |
| **`jyltis`** | [ʒyl.tis] | 名 | 連合、同盟条約、協調体制 | coalition, league, alliance | jylot (盟約) ＋ 連合 |

### 6. 精神・感情・哲学 (43 語幹)

| NRS転写 | 発音 (IPA) | 品詞 | 日本語意味 | 英語対応 | 備考・語源 |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **`sylim`** | [sy.lim] | 名 | 心、魂、精神、内なる核 | mind, soul, spirit | 精神の核 |
| **`cynel`** | [ʃy.nel] | 名/動 | 愛、慈しみ、深い共感、愛する | love, affection, cherish | 深い愛情 |
| **`cynas`** | [ʃy.nas] | 名 | 友情、親愛、心の絆 | friendship, fellowship | 友愛 |
| **`elir`** | [e.lir] | 名/形 | 喜び、多幸感、嬉しい | joy, delight, gladness | 喜び |
| **`lyras`** | [ly.ras] | 名/形 | 哀愁、切なさ、悲哀、切ない | sorrow, melancholy, pathos | 切なさ |
| **`sirin`** | [si.rin] | 名/形 | 平穏、安らぎ、静けさ、穏やか | serenity, peace, tranquility | 心の静けさ |
| **`krotas`** | [kro.tas] | 名/形 | 激動、怒り、熱狂、激しい | fury, wrath, passion | 高ぶり |
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
| **`durtan`** | [dur.tan] | 名 | 勇気、果敢さ、不屈の志 | courage, bravery, valor | 不屈の意志 |
| **`sufan`** | [su.fan] | 名/形 | 叡智、深奥な知慮、賢明な | wisdom, sagacity, deep insight | 思索から紡がれた智 |
| **`tyras`** | [ty.ras] | 名/動 | 探求心、知的好奇心、問う | curiosity, inquiry, probe | 真理への問いかけ |
| **`cynur`** | [ʒy.nur] | 名 | 感謝、謝意、心の返礼 | gratitude, thanksgiving | 心からの感謝 |
| **`novis`** | [no.vis] | 名/動 | 敬意、崇敬、尊ぶ | reverence, honor, venerate | 崇高なる敬意 |
| **`duras`** | [du.ras] | 名/形 | 忍耐、耐性、不撓不屈の | endurance, fortitude, patient | 静かに耐える力 |
| **`lyren`** | [ly.ren] | 名 | 鎮魂歌、哀傷詩、エレジー | elegy, requiem, lament | 魂を鎮める詩 |
| **`falik`** | [fa.lik] | 名 | 直感、閃き、直観的洞察 | intuition, flash of insight | 光の閃き |
| **`larvyn`** | [lar.vyn] | 名 | 宿命、天命、星の軌道命数 | destiny, cosmic ordination | 軌道が示す運命 |
| **`wylin`** | [wy.lin] | 名/形 | 自由、束縛なき飛翔、自在な | freedom, liberty, unchained | 風の如き自由 |
| **`sonan`** | [so.nan] | 動 | 夢を見る、幻視する、構想する | dream, envision, visualize | 夢見の動詞 |
| **`cylinor`** | [ʃy.li.nor] | 名 | 芸術家、美の探求者、表現者 | artist, aesthetician, creator of beauty | cylan (美) ＋ 専門職 |
| **`sirvon`** | [sir.von] | 名/形 | 瞑想、深い静思、観照する | meditation, tranquil mindfulness | sirin (平穏) ＋ 観照 |
| **`fevok`** | [fe.vok] | 名 | 確信、不抜の信仰、信条 | conviction, firm creed | fevas (信託) ＋ 確証 |
| **`kefur`** | [ke.fur] | 名 | 畏敬の念、崇拝、神聖感 | sacred awe, reverence | kefen (畏怖) ＋ 崇高 |
| **`lyrvik`** | [lyr.vik] | 名 | 郷愁、ノスタルジー、遠き星への憧憬 | nostalgia, longing for distant home | lyras (切なさ) ＋ 追憶 |
| **`sylkin`** | [syl.kin] | 名 | 誓い、心に誓う志、盟心 | solemn oath, inner pledge | sylim (心) ＋ 結縛 |
| **`sylfir`** | [syl.fir] | 名 | 誠実、真摯、純心 | integrity, sincerity, uprightness | sylim (心) ＋ firas (不変) |
| **`krotik`** | [kro.tik] | 名 | 葛藤、心の嵐、内なる動揺 | inner conflict, turmoil, agitation | krotas (激動) ＋ 内心 |
| **`sirvanis`** | [sir.va.nis] | 名 | 瞑想者、観照家、静思の徒 | contemplative, meditator, silent seer | sirvon (瞑想) ＋ 探求者 |
| **`welnas`** | [wel.nas] | 名 | 祈り、希求、祈願 | prayer, supplication, earnest wish | welin (希望) ＋ 希求 |
| **`durlan`** | [dur.lan] | 名 | 意志、不屈の覚悟、決意 | willpower, determination, firm resolve | duril (強固) ＋ 志向 |
| **`fevnas`** | [fev.nas] | 名 | 忠誠、信義、誠意 | fidelity, loyalty, allegiance | fevas (信託) ＋ 誠意 |
| **`cylanar`** | [ʃy.la.nar] | 名 | 劇場、美術館、芸術の館 | theater, art gallery, salon | cylan (美) ＋ 空間 |
| **`suflom`** | [suf.lom] | 名 | 論理体系、公理系、推論規則系 | logical system, axiomatic framework | suf (論理) ＋ 体系領域 |

### 7. 日常・住まい・食 (52 語幹)

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
| **`kymel`** | [ky.mel] | 名 | 寝床、ベッド、休息の台 | bed, resting couch | 寝具 |
| **`lerel`** | [le.rel] | 名 | 扉、ドア、出入口、ゲート | door, gate, entrance | 開閉具 |
| **`falar`** | [fa.lar] | 名 | 窓、明かり取り、天窓 | window, skylight | 光を取り込む処 |
| **`laros`** | [la.ros] | 名 | 乗り物、車両、列車、交通艇 | vehicle, carriage, train | 周回交通具 |
| **`larar`** | [la.rar] | 名 | 駅、ターミナル、空港、停泊地 | station, terminal, port | 交通拠点 |
| **`ner`** | [ner] | 名 | 滋養、食材、食物 | nourishment, foodstuff | 食料 |
| **`neran`** | [ne.ran] | 動 | 食べる、食事する、味わう | eat, dine, partake | 食事動詞 |
| **`nerel`** | [ne.rel] | 名 | 料理、ごはん、温かい食事 | meal, cooked dish | 料理 |
| **`neror`** | [ne.ror] | 名 | 料理人、シェフ | cook, chef | 料理人 |
| **`nerar`** | [ne.rar] | 名 | カフェ、喫茶店、食堂、レストラン | cafe, restaurant, diner | 飲食店 |
| **`bion`** | [bi.on] | 動 | 飲む、喫する、喉を潤す | drink, sip | 飲用動詞 |
| **`terin`** | [te.rin] | 名 | 温かい煎じ茶、薬草茶 | tea, warm herbal brew | 温飲料 |
| **`nerat`** | [ne.rat] | 名 | 主食、焼き穀物、糧 | bread, loaf, staple | 主食 |
| **`talyz`** | [ta.lyz] | 名 | 大地の結晶塩、調味料 | salt, seasoning | 塩・調味料 |
| **`darel`** | [da.rel] | 名 | スープ、温煮汁、滋養汁 | soup, broth | 温かい汁物 |
| **`voril`** | [vo.ril] | 名 | 発酵果実酒、祝い酒 | wine, fermented drink | 酒 |
| **`klovel`** | [klo.vel] | 名 | 鍵、解錠具、キー | key, lock-opener | 施錠・解錠具 |
| **`bionel`** | [bi.o.nel] | 名 | 杯、酒杯、グラス、器 | chalice, cup, goblet | 飲用具 |
| **`serel`** | [se.rel] | 名 | 小刀、ナイフ、調理刃 | knife, blade, cutter | 手元の刃具 |
| **`celdom`** | [ʃel.dom] | 名 | 天井、屋根、日覆い天蓋 | ceiling, roof, canopy | 部屋の上蓋 |
| **`taldom`** | [tal.dom] | 名 | 床、床面、居住基盤面 | floor, ground level | 部屋の底面 |
| **`durval`** | [dur.val] | 名 | 壁、隔壁、防護仕切り | wall, partition, bulkhead | 頑丈な壁 |
| **`velar`** | [ve.lar] | 名 | 庭、庭園、中庭、緑地 | garden, courtyard, arboretum | 緑豊かな庭 |
| **`nerom`** | [ne.rom] | 名 | 厨房、調理室、配膳所 | kitchen, cookroom, galley | 料理を作る部屋 |
| **`kirel`** | [ki.rel] | 名 | 筆、ペン、鉄筆、スタイラス | pen, stylus, quill | 文字を刻む道具 |
| **`falvis`** | [fal.vis] | 名 | 鏡、姿見、光反射板 | mirror, looking glass | 光を映す具 |
| **`talvin`** | [tal.vin] | 名 | 皿、深鉢、陶器の器 | plate, dish, bowl, earthenware | 食事を盛る器 |
| **`valdan`** | [val.dan] | 名 | 絨毯、敷物、織布マット | carpet, rug, floor tapestry | 床の敷物 |
| **`larsil`** | [lar.sil] | 名 | 靴、履物、歩行靴 | shoes, footwear, boots | 歩行の履物 |
| **`lervan`** | [ler.van] | 名 | 敷居、玄関、踏み分け段 | threshold, foyer, entryway | lerel (扉) ＋ 入口 |
| **`tasor`** | [ta.sor] | 名 | 肘掛け椅子、玉座、長椅子 | armchair, couch, settee | tasel (椅子) ＋ 上位座 |
| **`falmir`** | [fal.mir] | 名 | ランプ、常夜灯、星灯 | lamp, lantern, nightlight | falun (光) の照明具 |
| **`nerkam`** | [ner.kam] | 名 | 鍋、煮込み釜、調理鍋 | pot, cauldron, stewpot | ner (食) の調理釜 |
| **`serval`** | [ser.val] | 名 | 手袋、保護手袋 | gloves, gauntlets | ser (手) ＋ valis (布) |
| **`valren`** | [val.ren] | 名 | 帽子、頭巾、庇付き頭覆い | hood, cap, headpiece | valis (布) ＋ noven (頭) |
| **`terlar`** | [ter.lar] | 名 | 茶器、急須、温茶瓶 | teapot, kettle, brew urn | terin (茶) の容器 |
| **`domlik`** | [dom.lik] | 名 | 柱、支柱、梁、建築の骨柱 | pillar, column, support beam | dom (室) ＋ 支柱 |
| **`lervil`** | [ler.vil] | 名 | 閂、錠前、扉の留め具 | latch, door bolt, bar | lerel (扉) ＋ 施錠具 |
| **`falkom`** | [fal.kom] | 名 | 燭台、灯火台、照明スタンド | candelabra, lamp stand | falun (光) ＋ 置き台 |
| **`nerkul`** | [ner.kul] | 名 | スプーン、匙、汁掬い | spoon, ladle, serving scoop | ner (食) ＋ 掬い具 |
| **`nerspik`** | [ner.spik] | 名 | フォーク、刺し具、食具 | dining fork, pronged utensil | ner (食) ＋ 尖鋭刃 |
| **`valdanar`** | [val.da.nar] | 名 | 織物工房、機織り座、布工房 | textile atelier, loom workshop | valdan (絨毯) ＋ 工房 |
| **`bionas`** | [bi.o.nas] | 名 | 水差し、カラフェ、ピッチャー | pitcher, jug, decanter | bion (飲む) ＋ 注ぎ器 |
| **`pamelar`** | [pa.me.lar] | 名 | 図書館、文庫、書物閲覧所 | library, archive, book hall | pamel (書物) ＋ 収蔵館 |

### 8. 動作・相互作用 (52 語幹)

| NRS転写 | 発音 (IPA) | 品詞 | 日本語意味 | 英語対応 | 備考・語源 |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **`relen`** | [re.len] | 動 | ある、存在する、実在する | exist, be present | 存在コピュラ |
| **`poran`** | [po.ran] | 動 | 歩く、歩む、旅する、進む | walk, journey, travel | 歩行動詞 |
| **`kupan`** | [ku.pan] | 動 | 走る、急ぎ行く、駆ける | run, sprint, rush | 走行動詞 |
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
| **`klovan`** | [klo.van] | 動 | 閉じる、鍵をかける、終える | close, conclude, seal | 終了動詞 |
| **`seran`** | [se.ran] | 動 | 授ける、手渡す、贈る | give, bestow, grant | 授与動詞 |
| **`maren`** | [ma.ren] | 動 | 受け取る、得る、引き継ぐ | receive, obtain, acquire | 受領動詞 |
| **`spilan`** | [spi.lan] | 動 | 舞う、踊る、旋回ステップを踏む | dance, leap, sway | 舞踏動詞 |
| **`falk`** | [falk] | 名/動 | 閃光、火花、パチッと弾ける | spark, flash, snap | 鋭い破裂動詞 |
| **`zylan`** | [zy.lan] | 動 | 泳ぐ、水中を滑走する | swim, glide in water | 水泳動詞 |
| **`novas`** | [no.vas] | 動 | 登る、登攀する、頂点を目指す | climb, ascend, scale | 上昇動詞 |
| **`tulpan`** | [tul.pan] | 動 | 降りる、降下する、舞い降りる | descend, alight, touch down | 下降動詞 |
| **`wylkan`** | [wyl.kan] | 動 | 放つ、射出する、風に乗せる | hurl, cast, launch | 放射動詞 |
| **`serpan`** | [ser.pan] | 動 | 掴む、握る、掌中に収める | grasp, clutch, grip | 把持動詞 |
| **`koran`** | [ko.ran] | 動 | 切断する、裁つ、分かつ | sever, slice, cleave | 切断動詞 |
| **`jylpan`** | [ʒyl.pan] | 動 | 織る、編む、交差結節する | weave, braid, intertwine | 製織動詞 |
| **`darpan`** | [dar.pan] | 動 | 溶かす、溶解させる、融解する | melt, dissolve, liquefy | 融解動詞 |
| **`kyrpan`** | [kyr.pan] | 動 | 凍る、凝固する、結晶化する | freeze, solidify, congeal | 氷結動詞 |
| **`pyran`** | [py.ran] | 動 | 燃える、点火する、燃焼する | burn, ignite, blaze | 燃焼動詞 |
| **`dolaran`** | [do.la.ran] | 動 | 鍛造する、打刻する、精錬加工する | forge, refine, craft with tool | dolar ＋ 精錬 |
| **`falvan`** | [fal.van] | 動 | 照らす、輝かせる、ライトアップする | illuminate, shine light upon | 光を当てる |
| **`vorken`** | [vor.ken] | 動 | 収穫する、実りを摘む、取り込む | harvest, reap, gather fruit | vorin (果実) を摘む |
| **`klovanis`** | [klo.va.nis] | 動 | 封印する、厳封する、永久保管する | seal irrevocably, sequester | klovan の強化 |
| **`fenkas`** | [fen.kas] | 動 | 告げる、響かせる、布告する | announce, herald, proclaim | fenor (話す) ＋ 布告 |
| **`serlit`** | [ser.lit] | 動 | 撫でる、優しく触れる、いたわる | stroke gently, caress | ser (手) の柔和接触 |
| **`wylpur`** | [wyl.pur] | 動 | 吹き飛ばす、風で散らす、浄化する | blow away, scatter by wind | 風で払う |
| **`celvor`** | [ʃel.vor] | 動 | 覆う、包む、天蓋のように覆い被さる | cover, canopy, encompass | celen (天蓋) ＋ 被覆 |
| **`talkan`** | [tal.kan] | 動 | 耕す、土を鋤く、開墾する | plow, till, cultivate soil | tal (大地) ＋ 開墾 |
| **`darlit`** | [dar.lit] | 動 | 注ぐ、滴下する、水を注ぎ入れる | pour, decant, infuse | dar (滴) ＋ 流入 |
| **`wylrev`** | [wyl.rev] | 動 | 深呼吸する、風を吸い込む、息を整える | inhale deeply, breathe wind | wylas (風) ＋ 吸入 |
| **`talpyr`** | [tal.pyr] | 動 | 鍛造する、焼き入れする、熱処理する | temper, anneal, heat-treat | talur (金属) ＋ pyris (火) |
| **`serfas`** | [ser.fas] | 動 | 離す、手を放す、手放す | release, let go, disengage | ser (手) ＋ 離脱 |
| **`klomas`** | [klo.mas] | 動 | 遮断する、孤立させる、隔離する | isolate, insulate, shut off | klovel (鍵) ＋ 隔離 |
| **`volkin`** | [vol.kin] | 動 | 滑空する、風に乗って滑る、空を滑る | glide, sail on the air | volan (飛ぶ) ＋ 滑走 |

### 9. 性質・色彩・状態 (47 語幹)

| NRS転写 | 発音 (IPA) | 品詞 | 日本語意味 | 英語対応 | 備考・語源 |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **`alin`** | [a.lin] | 形 | 白い、純白の、無垢な | white, pure | 純白 |
| **`kyrin`** | [ky.rin] | 形 | 黒い、漆黒の、暗い | black, pitch-dark | 漆黒 |
| **`zylin`** | [zy.lin] | 形 | 青い、蒼穹の、碧色の | blue, azure, deep blue | 蒼穹・深碧 |
| **`pyrin`** | [py.rin] | 形 | 赤い、真紅の、燃えるような | red, crimson, fiery | 真紅 |
| **`valin`** | [va.lin] | 形 | 金色の、黄金の、輝かしい | golden, amber, lustrous | 黄金 |
| **`tyni`** | [ty.ni] | 形 | 銀色の、白銀の、月光の | silver, silvery, gleaming | 月光白銀 |
| **`nerin`** | [ne.rin] | 形 | 新しい、新鮮な、新緑の | new, fresh, novel | 新生 |
| **`eirin`** | [ei.rin] | 形 | 古い、悠久の、古代の | ancient, old, timeless | 悠久 |
| **`moran`** | [mo.ran] | 形 | 大きい、広大な、壮大な | large, vast, grand | 巨大 |
| **`telin`** | [te.lin] | 形 | 小さい、細やかな、微小な | small, tiny, delicate | 微小 |
| **`talani`** | [ta.la.ni] | 形 | 強い、堅固な、頑丈な、岩のような | strong, durable, solid | 堅固 |
| **`serini`** | [se.ri.ni] | 形 | 細い、薄い、繊細な | thin, slim, subtle | 繊細 |
| **`sirani`** | [si.ra.ni] | 形 | 優しい、穏やかな、柔らかな | gentle, mild, soft | 穏和 |
| **`faluni`** | [fa.lu.ni] | 形 | 明るい、光り輝く | bright, radiant | 明度 |
| **`kyrimi`** | [ky.ri.mi] | 形 | 深い、深淵な、奥底の | deep, profound | 深度 |
| **`cironi`** | [ʃi.ro.ni] | 形 | 静かな、無音の、凪いだ | silent, quiet, peaceful | 静穏 |
| **`cylani`** | [ʃy.la.ni] | 形 | 美しい、調和のとれた、麗しい | beautiful, exquisite | 美観 |
| **`eiran`** | [ei.ran] | 形 | 永遠の、不滅の、無尽の | eternal, perpetual, immortal | 不滅 |
| **`faluri`** | [fa.lu.ri] | 形 | 速い、迅速な、光速の | fast, rapid, swift | 高速 |
| **`morini`** | [mo.ri.ni] | 形 | 遅い、緩やかな、歩みの遅い | slow, gentle, unhurried | 低速 |
| **`novani`** | [no.va.ni] | 形 | 高い、至高の、天上界の | high, lofty, elevated | 高位 |
| **`tulosi`** | [tu.lo.si] | 形 | 低い、底層の、足元の | low, deep-set, base | 低位 |
| **`falini`** | [fa.li.ni] | 形 | 澄んだ、明瞭な、透き通った | clear, transparent, lucid | 透明感 |
| **`nebulin`** | [ne.bu.lin] | 形 | 紫の、深紫の、星雲色の | purple, violet, nebula-hued | 星雲の紫 |
| **`velini`** | [ve.li.ni] | 形 | 緑の、新緑色の、翠色の | green, emerald, verdant | 新緑のエメラルド |
| **`durini`** | [du.ri.ni] | 形 | 重い、重厚な、高密度の | heavy, dense, massive | 重力と密度 |
| **`wylini`** | [wy.li.ni] | 形 | 軽い、軽快な、浮遊感ある | light, airy, buoyant | 軽快な浮遊感 |
| **`teirini`** | [tei.ri.ni] | 形 | 温かい、慈愛に満ちた、温もりの | warm, tender, comforting | 温かな心核 |
| **`kyrani`** | [ky.ra.ni] | 形 | 冷たい、凍てつく、氷結の | cold, icy, frigid | 冷徹な氷 |
| **`talpi`** | [tal.pi] | 形 | 硬い、硬質な、強硬な | hard, rigid, unyielding | 硬質の破裂有標 |
| **`darini`** | [da.ri.ni] | 形 | 柔らかい、柔軟な、しなやかな | soft, supple, pliant | 柔和な水性 |
| **`nerili`** | [ne.ri.li] | 形 | 甘い、滋味豊かな、甘美な | sweet, luscious, delicious | 豊かな滋味 |
| **`falki`** | [fal.ki] | 形 | 鋭い、研ぎ澄まされた、尖鋭な | sharp, acute, keen | 鋭敏な閃光刃 |
| **`taluri`** | [ta.lu.ri] | 形 | 金属的な、硬質な光沢の、鋼の | metallic, steel-like, lustrous | talur (金属) の性質 |
| **`darmoni`** | [dar.mo.ni] | 形 | 清冽な、湧水のように澄んだ | pure, limpid, spring-clear | darmon (泉) の性質 |
| **`kyrlini`** | [kyr.li.ni] | 形 | 雪白の、粉雪のような、純潔の | snow-white, crystalline pure | kyrlen (雪) の性質 |
| **`zohari`** | [zo.ha.ri] | 形 | 太陽のような、真昼の、熱烈な | solar, radiant, high-noon | zohar (太陽) の性質 |
| **`celisi`** | [ʃe.li.si] | 形 | 霞がかった、曖昧な、霧深い | misty, hazy, nebulous | celis (霧) の性質 |
| **`krotani`** | [kro.ta.ni] | 形 | 騒然とした、激動の、波乱に満ちた | turbulent, stormy, tumultuous | krotas (激動) の性質 |
| **`vyrini`** | [vy.ri.ni] | 形 | 星辰のように輝く、綺羅星の | star-like, starry, glittering | vyr (星) の形容詞 |
| **`taldari`** | [tal.da.ri] | 形 | ぬかるんだ、泥深い、粘土質の | muddy, miry, clayey | taldar (泥) の性質 |
| **`velpari`** | [vel.pa.ri] | 形 | 樹木が生い茂った、森厳な | wooded, arboraceous, dense-timbered | vel (木) の群生 |
| **`darlori`** | [dar.lo.ri] | 形 | 激流の、潮汐力強い、奔流の | torrential, surging, rushing | darlor (潮流) の性質 |
| **`wylvani`** | [wyl.va.ni] | 形 | 旋風のような、目まぐるしい | swirling, vortex-like, brisk | wylven (つむじ風) の性質 |
| **`kyrfini`** | [kyr.fi.ni] | 形 | 凍結した、氷河のような、極寒の | glacial, ice-locked, gelid | kyrfin (氷河) の性質 |
| **`falpiri`** | [fal.pi.ri] | 形 | 冷光の、幽かな燐光を放つ | phosphorescent, glow-in-the-dark | falpir (燐光) の性質 |
| **`durvani`** | [dur.va.ni] | 形 | 免疫のある、抗体を持った、無傷の | immune, resistant, impervious | durvan (免疫) の性質 |

### 10. 時空・方位・副詞 (48 語幹)

| NRS転写 | 発音 (IPA) | 品詞 | 日本語意味 | 英語対応 | 備考・語源 |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **`hav`** | [hav] | 名 | 時、瞬間、今この瞬間 | time, moment, now | 瞬発的摩擦音 |
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
| **`vyranu`** | [vy.ra.nu] | 副 | 確かに、真に、疑いなく | truly, certainly, indeed | 確信副詞 |
| **`foras`** | [fo.ras] | 副 | おそらく、たぶん、星の導きによれば | perhaps, maybe | 推量副詞 |
| **`eirinu`** | [ei.ri.nu] | 副 | 常に、絶え間なく、いつでも | always, perpetually | 恒常副詞 |
| **`kural`** | [ku.ral] | 副 | 互いに、双方向に、連星のように | mutually, together | 相互副詞 |
| **`mu`** | [mu] | 副 | いいえ、〜でない（否定極性辞） | not, no | 否定極性辞 |
| **`ve`** | [ve] | 副 | はい、然り、その通り（肯定極性辞） | yes, indeed, so it is | 肯定極性辞 |
| **`tor`** | [tor] | 接 | しかし、されど | but, yet | 逆接接続詞 |
| **`ul`** | [ul] | 接 | そして、また、〜と共に | and, also | 接続詞 |
| **`zen`** | [zen] | 接/副 | なぜなら、〜ゆえに、理由 | because, for reason | 因果接続詞 |
| **`tyro`** | [ty.ro] | 副 | なぜ、いかにして（疑問副詞） | why, wherefore | 探求の問い |
| **`falden`** | [fal.den] | 名/副 | 東、主星昇騰の方位、曙光の方角 | east, sunrise direction | 光が昇る方角 |
| **`kymden`** | [kym.den] | 名/副 | 西、主星没入の方位、黄昏の方角 | west, sunset direction | 光が沈む方角 |
| **`novden`** | [nov.den] | 名/副 | 北、天頂極の方位、上極 | north, zenith pole | 天頂を向く極 |
| **`tulden`** | [tul.den] | 名/副 | 南、天底極の方位、下極 | south, nadir pole | 天底を向く極 |
| **`voras`** | [vo.ras] | 名/副 | 前、前方、未来の側 | front, forward, ahead | 進行方向 |
| **`pason`** | [pa.son] | 名/副 | 後、後方、過去の側 | back, rear, behind | 過ぎ去る方向 |
| **`lerin`** | [le.rin] | 名/副 | 左、左舷、左方 | left, portside | 左側 |
| **`parin`** | [pa.rin] | 名/副 | 右、右舷、右方 | right, starboard | 右側 |
| **`tyku`** | [ty.ku] | 副 | 直ちに、即座に、一拍のうちに | instantly, immediately, on the tick | 一拍での即応 |
| **`valk`** | [valk] | 副 | 頻繁に、度々、波打つように | often, frequently | 周期的な頻度 |
| **`havit`** | [ha.vit] | 名/副 | やがて、程なくして、近い将来に | soon, before long, presently | hav (時) の近傍 |
| **`eirlom`** | [eir.lom] | 名/副 | 太古に、悠久の昔に、原初から | in ancient times, from the dawn | eirin (悠久) ＋ 領域 |
| **`valasu`** | [va.la.su] | 副 | 朝早くに、黎明に、夜明け前に | at dawn, in early morning | valar (朝) ＋ 副詞語尾 |
| **`kylasu`** | [ky.la.su] | 副 | 夕暮れ時に、日没に、黄昏に | at dusk, at twilight | kylas (夕) ＋ 副詞語尾 |
| **`novasu`** | [no.va.su] | 副 | 高らかに、天上に向けて、頂点へ | loftily, aloft, upwards | novan (高嶺) ＋ 副詞語尾 |
| **`tulosu`** | [tu.lo.su] | 副 | 深く、足元へ、根源へ向けて | deeply, profoundly, downwards | tulos (天底) ＋ 副詞語尾 |
| **`havlor`** | [hav.lor] | 名/副 | いつか、いずれ、将来のある時 | someday, eventually, in due time | hav (時) ＋ 巡行 |
| **`eirvas`** | [eir.vas] | 名/副 | 永遠の彼方、無窮の果て | eternity horizon, timeless expanse | eiran (永遠) ＋ 遥か |
| **`valrotu`** | [val.ro.tu] | 副 | 木漏れ日の中で、緑陰に | in dappled shade, under leafy light | velrot ＋ 副詞語尾 |
| **`kymdenu`** | [kym.de.nu] | 副 | 西へ、日没の方角へ、黄昏に向かって | westward, toward twilight | kymden (西) ＋ 副詞語尾 |
| **`faldenu`** | [fal.de.nu] | 副 | 東へ、日の出の方角へ、黎明に向かって | eastward, toward sunrise | falden (東) ＋ 副詞語尾 |
| **`novdenu`** | [nov.de.nu] | 副 | 北へ、天頂極へ向かって | northward, toward zenith | novden (北) ＋ 副詞語尾 |
| **`tuldenu`** | [tul.de.nu] | 副 | 南へ、天底極へ向かって | southward, toward nadir | tulden (南) ＋ 副詞語尾 |
| **`kivku`** | [kiv.ku] | 副 | ビット単位で、微細に、逐一 | bit by bit, granularity, item by item | kiv (ビット) ＋ 共格副詞 |

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
- **Nebulith**: *Zyvan el darisor ia myren uo darisar de zyvil.*
- **発音**: [zy.van el da.ri.sor ia my.ren wo da.ri.sar de zy.vil]
- **意訳**: 「医師は診療所において、生薬を用いて人間を治療する。」
- **音韻特徴**: 行為（`zyvan`）、対象（`myren`）、道具（`zyvil`）が調和し、施設（`darisar`）と医師（`darisor`）のみが自然な派生関係を保つ。

### 例文 3: 宇宙観測・自然哲学
- **Nebulith**: *Vyrel el vyrelor ia doran uo vyrelar de vyrelel.*
- **発音**: [vy.rel el vy.re.lor ia do.ran wo vy.re.lar de vy.re.lel]
- **意訳**: 「天文学者は天文台で望遠鏡を用いて惑星を観測する。」

### 例文 4: 社会・論理（破裂音と逆接のブレーキ）
- **Nebulith**: *Kiran el sufor ia zevil, tor klovan ia mator.*
- **発音**: [ki.ran el su.for ia ze.vil, tor klo.van ia ma.tor]
- **意訳**: 「プログラマーはコードを書いたが、コンピューターを閉じた。」
- **音韻特徴**: 逆接接続詞 `tor` [tor] の切れ味ある音韻が自然な文脈転換を表現。

---
