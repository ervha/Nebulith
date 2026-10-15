# tools/append_comprehensive_grammar_spec.py
import re

with open("docs/Project Requirements And Design.md", "r", encoding="utf-8") as f:
    content = f.read()

# Update version and date in header
content = content.replace("v17.0 (シャレイア・キプソル準拠新音韻体系・抽象星辰筆記文字・公式ラテン文字転写確定版)", 
                          "v23.0 (自然言語化・新星辰幾何学フォントv2.0・統括言語体系D案仕様確定版)")
content = content.replace("**最終更新日**: 2026-10-14", "**最終更新日**: 2026-10-15")

grammar_chapter = """

---

## 6. 統括言語体系仕様（D案：星辰軌道相・相関詞グリッド・複文統語論・規範コーパス）

Nebulithの語彙大系（全16カテゴリー・計1,008語幹）が完成したことを受け、単なる単語の集積から**生きた思考・哲学・観測を記述できる完全な自然主義的人工言語（Naturalistic Conlang）**へと昇華させるための統括文法仕様を定義する。

### 6.1 幾何学的星辰相関詞グリッド（Correlatives Matrix）
指示詞・代名詞・疑問詞・不定詞を、天体距離軸（6種）× 概念存在軸（6種）の直交マトリクス（計36語）として幾何学的に固定する。

| 概念存在軸 \ 天体距離軸 | 近称（この・ここ）<br>**`hi-`** | 中称（その・そこ）<br>**`ta-`** | 遠称（あの・あそこ）<br>**`va-`** | 疑問（どれ・どこ）<br>**`ka-`** | 全称（すべての）<br>**`sen-`** | 否定（何もない）<br>**`ni-`** |
|---|---|---|---|---|---|---|
| **事物・概念** (`-te`) | **`hite`**（これ） | **`tate`**（それ） | **`vate`**（あれ） | **`kate`**（何・どれ） | **`sente`**（万物・全て） | **`nite`**（無・何も〜ない） |
| **人物・生命** (`-as`) | **`hias`**（この人） | **`taas`**（その人） | **`vaas`**（あの人） | **`kaas`**（誰） | **`senas`**（全員・万人） | **`nias`**（誰も〜ない） |
| **座標・場所** (`-uo`) | **`hiuo`**（ここ） | **`tauo`**（そこ） | **`vauo`**（あそこ） | **`kauo`**（どこ） | **`senuo`**（至る所・全域） | **`niuo`**（どこにも〜ない） |
| **時・周期** (`-hav`) | **`hihav`**（今・この時）| **`tahav`**（その時） | **`vahav`**（往時・あの時）| **`kahav`**（いつ） | **`senhav`**（常に・永遠に）| **`nihav`**（決して〜ない） |
| **様態・方法** (`-ku`) | **`hiku`**（このように） | **`taku`**（そのように） | **`vaku`**（あのように） | **`kaku`**（どう・いかに）| **`senku`**（あらゆる方法で）| **`niku`**（どうやっても〜ない）|
| **理由・動機** (`-zen`)| **`hizen`**（この故に） | **`tazen`**（それ故に） | **`vazen`**（あの故に） | **`kazen`**（なぜ・どうして）| **`senzen`**（あらゆる理由で）| **`nizen`**（何の理由もなく） |

---

### 6.2 動詞の星辰軌道相（Orbital Aspects）と態（Voice）

動詞の事象展開を「天体の運行状態」になぞらえて精密に記述するアスペクト体系。

#### 1. 時制（Tense: 空間的時間軸）
* **過去**: 前置小詞 **`fe`**（例: `fe poran el laranas`「旅人は歩いた」）
* **現在**: **無標（∅）**（例: `poran el laranas`「旅人は歩く」）
* **未来**: 前置小詞 **`se`**（例: `se poran el laranas`「旅人は歩くだろう」）

#### 2. 4大軌道相（Aspects: 運行の幾何学的段階）
1. **始動相（Inceptive: 軌道突入・事象の開始）**: 語尾 **`-ast`**
   * `falun`（光る） ➔ **`falunast`**（パッと光り始める、点灯する）
   * `cival`（歌う） ➔ **`civalast`**（歌い出す、声を合わせ始める）
2. **継続・進行相（Progressive: 巡行中）**: 前置辞 **`di`** または語尾 **`-in`**
   * `kiran`（書く） ➔ **`di kiran`** / **`kiranin`**（今まさに書き綴っている）
3. **完了相（Perfective: 会合到達・成就）**: 語尾 **`-ol`**
   * `kiran`（書く） ➔ **`kirol`**（書き上げた、記述を完了した）
   * `syndir`（探す） ➔ **`syndirol`**（見つけ出した、発見に至った）
4. **周期・反復相（Iterative: 軌道公転・恒常的習慣）**: 語尾 **`-cor`**
   * `vyrel`（観測する） ➔ **`vyrelcor`**（定期観測する、日々星を見守る）
   * `neran`（食べる） ➔ **`nerancor`**（日々の糧を食む、常食する）

#### 3. 態（Voice: 能動・反照・連星）
* **能動態**: 基本語形（`Sun [動詞] + el [主語] + ia [目的語]`）
* **反照・受動態（Reflective / Passive）**: 動詞頭に接語 **`re-`**
   * `falun`（照らす） ➔ **`refalun`**（照らされる、光を浴びる）
   * 例: `Refalun el govan ia de falun en vyr.`（家は星の光によって照らされている。）
* **連星・相互態（Binary / Reciprocal Voice）**: 動詞頭に接頭辞 **`co-`**
   * 対等な二者が互いに作用し合う連星の運行を表現する。
   * `cival`（歌う） ➔ **`cocival`**（互いに唱和する、二重奏を奏でる）
   * `sercor`（手を携える） ➔ **`cosercor`**（手を取り合い固く誓い合う）

---

### 6.3 名詞の数体系（Number）と有生性階層（Animacy）

天体運行言語としてのアイデンティティを深める名詞形態論。

1. **数体系（Number）**:
   * **単数（Singular）**: 語幹無標（`∅`）（例: `vyr` 単一の星）
   * **双数・連星数（Dual Number）**: 接尾辞 **`-el`**（対になる器官・連星対・対話する二者）
     * `vyr`（星） ➔ **`vyrel`**（連星、対をなす二重星）
     * `ser`（手） ➔ **`serel`**（両手、一対の手）
     * `vylan`（目・瞳） ➔ **`vylanel`**（両眼、双眸）
     * `laranas`（旅人） ➔ **`laranasel`**（旅の道連れ、二人連れ）
   * **複数（Plural）**: 接尾辞 **`-in`**（無数の集まり・群）
     * `vyr`（星） ➔ **`vyrin`**（星群、無数の星々）
2. **有生性階層（Animacy Hierarchy）**:
   * **天体・高位知性体（Stars, Archons, Sages）**: 尊称接尾辞 `-on` や敬意前置標識 `al-` を伴い、能動文の真の主星（Sun）として振る舞う。
   * **無生物・現象・道具（Utensils, Stone, Mechanics）**: 道具格 `de` や受動格 `ia` を担い、自発的な行動主体としては擬人化文脈以外では現れない。

---

### 6.4 複文統語論と関係節（Complex Syntax）

VSO（動詞・主語・目的語）語順の力学的明瞭さを保ちながら、複雑な論理・観測条件を表現する統語構造。

#### 1. 関係節標識 `i`（〜であるところの）
修飾される名詞（先行詞）の直後に **`i`** を配置し、節内を通常の格標識で展開する。
* **基本構文**: `[先行詞名詞] + i + [動詞] + [節内格標識...]`
* 例: 
  * `govan i fe relen el vyrelor`
  * （かつて天文学者が暮らしていた家 ＝ 家 [関係標識] [過去] 住んでいた [主語: 天文学者]）
  * `marnyz i syndirol el laranas uo talik`
  * （旅人が渓谷で見つけ出した結晶塩 ＝ 塩 [関係標識] [完了] 見つけた [主語: 旅人] [処格: 渓谷にて]）

#### 2. 4大従属接続詞（Subordinating Conjunctions）
文頭または主節の後に配置され、宇宙の因果律を記述する。
1. **条件（もし〜なら）: `sen`**
   * `Sen falunast el vyr, se poran el laranas.`
   * （もし星が輝き始めるならば、旅人は歩み出すだろう。）
2. **理由（〜の故に・なので）: `zen`**
   * `Fe revir el korgon, zen fe neran el hias ia nyrat.`
   * （この人が主食パンを食べたので、胃は回復した。）
3. **譲歩（〜だけれども）: `tor`**
   * `Tor kymdenu relen el sola, di falun el vyris.`
   * （太陽は西へと沈んだけれども、星光は輝き続けている。）
4. **時間・同時（〜のとき）: `hav`**
   * `Hav cocival el civalasel, fe relen el domom uo calar.`
   * （二人の歌い手が唱和したとき、都市は静寂に包まれた。）

---

### 6.5 公式規範コーパス集（Nebulith Canon Corpus）

言語の実際の運用美を証明する3大規範テクスト。

#### テクスト 1：星辰箴言（Philosophical Aphorism）
> **NRS**: `Relen el vyran ia tolst en sentis: tor poran el havel, ne korol el falun en vyr.`  
> **逐語分解**: `Relen` (存在コピュラ) `el vyran` (主格: 理法/真理は) `ia tolst` (対格: 床/確固たる基盤) `en sentis` (属格: 万有の) : `tor poran` (譲歩: 歩み去るが) `el havel` (主格: 時間は), `ne korol` (否定完了: 尽き果てることはない) `el falun` (主格: 光は) `en vyr` (属格: 恒星の).  
> **日本語訳**: 「真理は万物の床（礎）である。時が歩み去ろうとも、星の光が尽き果てることはない。」

#### テクスト 2：天文台の日誌（Astronomer's Observation Log）
> **NRS**: `Fe vyrelcor el vyrelor uo vyrelar to falden. Falunast el vyr syvani uo celvan, fe rekorval el corval en cel mon.`  
> **逐語分解**: `Fe vyrelcor` (過去反復: 定期観測した) `el vyrelor` (主格: 天文学者は) `uo vyrelar` (処格: 天文台にて) `to falden` (向格: 東方へ向けて). `Falunast` (始動相: 輝き始めた) `el vyr syvani` (主格: 新しい星が) `uo celvan` (処格: 天球において), `fe rekorval` (過去受動: 平衡化された) `el corval` (主格: 重心中心が) `en cel mon` (属格: 暗黒星雲の).  
> **日本語訳**: 「天文学者は天文台にて東の空を観測した。天球に新たな星が光を放ち始め、暗黒星雲の重心軌道が整えられた。」

#### テクスト 3：日常対話プロトコル（Daily Dialogue Protocol）
> **A**: `Vyrin faluni al taas! Kauo poran el taas?`  
> （星光の導きがあなたにあらんことを！ あなたはどこへ歩まれるのですか？）  
> **B**: `Poran el mi to govan en dolas. Nerancor el mi ia nyrat uo nerar.`  
> （私は友の家へと歩んでいます。私たちはカフェで主食パンを共にいただくところです。）  
> **A**: `Solsun el keiran en taas! Faldenu poran el mi.`  
> （あなたの軌道に平安あれ！ 私は東へと向かいます。）

"""

content += grammar_chapter

with open("docs/Project Requirements And Design.md", "w", encoding="utf-8") as f:
    f.write(content)

print("docs/Project Requirements And Design.md successfully updated with Chapter 6 Grammar Specs!")
