# 人工言語「Nebulith」統合スタジオ 要件定義および設計仕様書

**文書バージョン**: v17.0 (シャレイア・キプソル準拠新音韻体系・抽象星辰筆記文字・公式ラテン文字転写確定版)  
**最終更新日**: 2026-10-14  
**関連ドキュメント**: `Nebulith Master Lexicon.md`（マスター辞書定義書 v12.0 ※新体系へリセット・再構築中）  
**利用スコープ**: **完全個人専用（シングルユーザー・完全オフライン・サーバー＆外部I/Oゼロ）**  
**ターゲット環境**: **Windows 10/11 (JVM Desktop `.exe` / `.msi`)** および **Android 10〜15+ (`.apk`)**  

---

## 1. アーキテクチャ基本方針とKMPモジュール構成

### 1.1 完全自律スタンドアロン・ゼロI/O設計
本プロジェクトは、外部データベース（SQLite等）、デバイス間通信同期、および外部ストレージのファイル読み書き（CSV等）を**一切行わない**。

1. **アプリ内静的辞書バンドル**: 基本語幹、文法機能語、主要派生語・複合語は、Kotlinコード内の不変コレクション（`StaticLexicon`）としてバイナリに直結内包する。
2. **決定論的造語と静的昇格サイクル**: 未登録語はFNV-1aハッシュと新音韻規則で即座に自動生成する。正式採用時はインスペクターで整合性を検証し、Kotlinコード定義（`LexiconEntry`）として出力・ソースコードへコミットしてバイナリへ恒久統合する。
3. **インメモリ直結のAndroid IME**: システムキーボード（`NebulithInputMethodService`）はファイルI/Oを一切介さず、`commonMain` のオンメモリ辞書と変換エンジンを直接参照して高速動作する。

### 1.2 KMP モジュール構造とソースセット設計

```text
nebulith-kmp-studio/
├── build.gradle.kts
├── settings.gradle.kts
└── composeApp/
    ├── build.gradle.kts
    └── src/
        ├── commonMain/kotlin/com/reiun/nebulith/       【全OS共通コア (共有率 95%以上)】
        │   ├── domain/
        │   │   ├── model/         (SyllableToken, WordBlock, LexiconEntry)
        │   │   ├── phonology/     (PhonologyConfig: 6母音+4二重母音+16子音、ソノリティ規則、FNV-1a造語)
        │   │   ├── morphology/    (語形成規則・品詞接辞展開・逆解析ステートマシン)
        │   │   ├── validation/    (LexiconIntegrityValidator: 新音韻・衝突・重複・複合検証)
        │   │   └── syntax/        (日英SOV/SVO ⇔ Nebulith VSO 双方向構文変換器)
        │   ├── data/
        │   │   └── lexicon/       (StaticLexicon: 新体系基本語幹・機能語・焼き込み定数)
        │   ├── font/
        │   │   ├── glyph/         (1000×1000 EM座標系 抽象星辰筆記文字ベクターパス定義)
        │   │   └── ttf/           (NebulithTtfBuilder: ピュアKotlin TrueTypeバイナリ生成)
        │   ├── renderer/
        │   │   ├── canvas/        (Compose Canvas による手書き風インク描画器)
        │   │   └── notebook/      (天文学者野帳・罫線・万年筆インクかすれ筆致エンジン)
        │   └── ui/                (Compose Multiplatform 統合UI)
        │       ├── theme/         (Astronomer Notebook / Celestial Ink テーマ)
        │       └── screen/        (NebulithStudioScreen: 変換・検証・辞書昇格・描画統合画面)
        │
        ├── commonTest/kotlin/com/reiun/nebulith/       【ビルド時・静的辞書整合性CIテスト】
        │   └── LexiconIntegrityTest.kt (全登録語彙の新音韻規則・同音衝突・規則重複の自動検証)
        │
        ├── androidMain/kotlin/com/reiun/nebulith/      【Android 固有実装】
        │   ├── MainActivity.kt    (Compose Activity)
        │   └── ime/               (NebulithInputMethodService: オンメモリ直結システムIME)
        │
        └── desktopMain/kotlin/com/reiun/nebulith/      【Windows (JVM Desktop) 固有実装】
            └── main.kt            (Window管理・デスクトップ起動エントリポイント)
```

---

## 2. 言語仕様：新音韻・転写体系・語形成・天体軌道格文法

シャレイア語（Shaleian）およびキプソル語（Qipshor）の言語設計美学を取り入れ、日本語特有の「アイウエオ平坦拍」を完全に脱却した流麗・透明な音韻体系を構築する。

### 2.1 新・音韻体系（Phonological System）

#### ① 6大単母音（Monophthongs）
* **`a`** [a]: 開いた明瞭な陽の音（アー）
* **`e`** [e]: 軽快で知的な前舌音（エー）
* **`i`** [i]: 高く澄んだ極星の音（イー）
* **`o`** [o]: 円唇の豊かな満月の音（オー）
* **`u`** [u]: 深く受容する深淵の音（ウー）
* **`y`** [y]: **【第6の天体母音】** 前舌円唇母音（ドイツ語 `ü`、フランス語 `u`、古代ギリシャ語 `υ`）。
  * 舌を「イ」の位置にしたまま唇を丸めて発音する冷涼・透明な音。星雲の冷気や神秘性を宿す。

#### ② 4大公転二重母音（Orbital Diphthongs）
1音節の息の中で滑らかに音色が滑る、流麗な抑揚を生み出す。
* **`ai`** [aɪ]: 星の瞬き（例: `sailis` サィリス）
* **`ei`** [eɪ]: 光の軌道（例: `keiran` ケィラン）
* **`au`** [aʊ]: 夜空の深み（例: `naura` ナゥラ）
* **`oi`** [ɔɪ]: 満ちる月影（例: `soilar` ソィラル）

#### ③ 16主星子音 ＋ 1原初軸（Consonants & Aether Carrier）
* **鼻音・流音（高ソノリティ・流麗群）**:
  * `m` [m], `n` [n], `l` [l] (澄んだ側面音), `r` [r/ɾ] (流麗なはじき音)
* **摩擦音・接近音（風・気音・波群）**:
  * `s` [s] (星雲のささやき), `z` [z] (連星の共鳴), `c` [ʃ] (静寂のシ音), `j` [ʒ] (深いジ音)
  * `f` [f], `v` [v], `h` [h], `w` [w]
* **破裂音（明瞭な天体アンカー群）**:
  * 無声音: `p` [p], `t` [t], `k` [k]
  * 有声音: `b` [b], `d` [d], `g` [g]
* **原初軸（Aether Carrier）**:
  * `'` [ʔ]: 母音単独で始まる音節の頭子音キャリア。

#### ④ 音節構造とソノリティ制限（Coda Consonants）
* **基本構造**: `C V (C)` または `C V1V2 (C)` （2音節・4〜5文字が語幹の標準長）。
* **許容末子音（Coda）**: 語末の音を硬い閉鎖音（`-k, -t, -p`）で終わらせず、心地よい余韻を残すため **`l, r, n, m, s` の5種** に厳密に限定する。

---

### 2.2 公式ラテン文字転写体系（Nebulith Romanization Standard: NRS）

キーボード入力、ソースコード（Kotlinの `StaticLexicon`）、および学術的記録において、完全な可逆変換（無損失）を保証する転写規則。

| 区分 | Nebulith転写文字 | IPA発音 | 備考・キーボード入力 |
| :--- | :--- | :--- | :--- |
| **単母音** | `a` | [a] | 通常キー `a` |
| | `e` | [e] | 通常キー `e` |
| | `i` | [i] | 通常キー `i` |
| | `o` | [o] | 通常キー `o` |
| | `u` | [u] | 通常キー `u` |
| | **`y`** | [y] | 通常キー `y`（ウムラウト入力不要） |
| **二重母音** | `ai, ei, au, oi` | [aɪ, eɪ, aʊ, ɔɪ] | 2打鍵（1音節として発音） |
| **子音** | `m, n, l, r` | [m, n, l, ɾ] | 通常キー |
| | `s, z, f, v, h, w` | [s, z, f, v, h, w] | 通常キー |
| | `c` | [ʃ] | 通常キー `c`（英語の sh 音） |
| | `j` | [ʒ] | 通常キー `j`（英語の measure の s 音） |
| | `p, t, k, b, d, g` | [p, t, k, b, d, g] | 通常キー |
| **原初軸** | `'` | [ʔ] | アポストロフィキー |

---

### 2.3 多元的語彙形成規則（8大語形成パターン）

| 規則ID | 規則名称 | 形成構造 | 具体例 |
| :--- | :--- | :--- | :--- |
| **`RULE_1_AGENT_OR`** | ① 動作主・行為者 | `[語幹] + -or` | `dokil` (教える) → **`dokilor`** (教師) |
| **`RULE_2_EXPERT_IS`** | ② 専門職・学者 | `[語幹] + -is` | `sufan` (数理) → **`sufanis`** (数学者) |
| **`RULE_3_TOOL_EK`** | ③ 道具・装置・機械 | `[語幹] + -ek` | `sufan` (計算) → **`sufanek`** (計算機・PC) |
| **`RULE_4_PLACE_AD`** | ④ 場所・施設・空間 | `[語幹] + -ad` | `dokil` (教育) → **`dokilad`** (学校) |
| **`RULE_5_SYSTEM_UM`** | ⑤ 学問・体系・抽象 | `[語幹] + -um` | `sylim` (星) → **`sylimum`** (天文学) |
| **`RULE_6_PATIENT_AT`**| ⑥ 被行為者・結果物 | `[語幹] + -at` | `kreas` (創る) → **`kreasat`** (作品) |
| **`RULE_7_COMPOUND_O`**| ⑦ 連星複合語（縮約調和） | `[語幹A'] + o + [語幹B]` | `syli(m)` + `o` + `kura(n)` → **`sylokuran`** (星時計) |
| **`RULE_8_PREFIX`** | ⑧ 意味階層・反転接頭辞 | `[ku/ar/mi/ko/re] + [語幹]`| `ku-` (反転): `bonas` (美) → **`kubonas`** (醜) |

* **文法活用接尾辞**: 名詞単数 `-∅` / 名詞複数 `-es` / 動詞現在 `-a` / 動詞過去 `-o` / 動詞未来 `-u` / 動名詞 `-an` / 形容詞 `-i` / 副詞 `-e`

### 2.4 統語論：「天体軌道格」文法（VSO）
* **基本語順**: `[動詞 (Sun)] + el [主語] + ia [目的語] + al [与格] + uo/de/to/va/ku [斜格] + [文末助詞 ka/ze/na/lo].`
* **コピュラ文**: `Esara el [主語A] ia [補語B].`（AはBである）
* **全9格標識**: `el` (主格), `ia` (対格), `al` (与格), `en` (属格: `A en B`＝BのA), `uo` (処格), `de` (具格), `to` (向格), `va` (奪格), `ku` (共格)

---

## 3. 全方位語彙解決パイプライン ＆ 未知語の静的辞書昇格仕様

### 3.1 決定論的造語エンジン（`DeterministicLexiconEngine`）
新音韻規則（6母音＋4二重母音＋16子音、許容末子音 `l, r, n, m, s`）に完全準拠し、未登録語から美しい2音節語幹（`C1 V1 C2 V2 C3` または `C1 V1V2 C2 V2`）を決定論的に生成する。

```kotlin
// commonMain/kotlin/com/reiun/nebulith/domain/phonology/DeterministicLexiconEngine.kt
package com.reiun.nebulith.domain.phonology

object DeterministicLexiconEngine {
    val ONSET_CONSONANTS = listOf('s', 'k', 't', 'n', 'm', 'l', 'r', 'h', 'f', 'v', 'd', 'b', 'g', 'c', 'j', 'p')
    val VOWELS = listOf("a", "e", "i", "o", "u", "y", "ai", "ei", "au", "oi")
    val CODA_CONSONANTS = listOf('l', 'r', 'n', 'm', 's')

    fun generateRoot(word: String, existingRoots: Set<String>): String {
        var salt = 0
        while (true) {
            val target = if (salt == 0) word else "$word#$salt"
            var hash = 0x811c9dc5.toLong()
            for (b in target.encodeToByteArray()) {
                hash = hash xor (b.toLong() and 0xff)
                hash = (hash * 0x01000193) and 0xffffffffL
            }
            val c1 = ONSET_CONSONANTS[(hash and 0xF).toInt() % ONSET_CONSONANTS.size]
            val v1 = VOWELS[((hash shr 4) and 0xF).toInt() % VOWELS.size]
            val c2 = ONSET_CONSONANTS[((hash shr 8) and 0xF).toInt() % ONSET_CONSONANTS.size]
            val v2 = VOWELS[((hash shr 12) and 0x7).toInt() % 6] // 第2母音は単母音中心
            val c3 = CODA_CONSONANTS[((hash shr 15) and 0x7).toInt() % CODA_CONSONANTS.size]
            val candidate = "$c1$v1$c2$v2$c3"

            if (candidate !in existingRoots) return candidate
            salt++
        }
    }
}
```

---

## 4. 独自文字「Nebulith Script（星辰筆記文字）」描画 ＆ TTF生成仕様

象形文字（具象画）を完全に排し、シャレイア文字・キプソル文字に準拠した**「丸みを帯びた抽象筆記・記号文字（Abstract Cursive Script）」**として実装する。

### 4.1 グリフ幾何学構造（1000×1000 EM座標系）
* **ベースライン ($Y = 200$)**:
  * すべての文字が共通のベースライン上に整然と接地し、自然な行の流れを形成する。
* **文字領域構成**:
  * **X-Height ($Y = 200 \sim 600$)**: 母音および子音の主骨格（ボウル・アーチ）。
  * **Ascender ($Y = 600 \sim 850$)**: `l, k, t` 等の天高く伸びる柔らかなオーバルループ。
  * **Descender ($Y = 200 \sim 50$)**: `j, p, y` 等のベースライン下へ潜る流線。
  * **結節点ノード（Node Dots）**: ストロークの始端・終端・変曲点に自然なインク溜まり（星核）が付与される。

### 4.2 ピュアKotlin TrueType（`.ttf`）バイナリビルダー
* `NebulithTtfBuilder` が、自立型アルファベットグリフの2次ベジェ曲線パスから OpenType 必須10テーブル（`head`, `hhea`, `maxp`, `OS/2`, `hmtx`, `cmap`, `loca`, `glyf`, `name`, `post`）を計算・直結生成する。
* 複雑な重ね合わせテーブル（GPOS）に依存しないため、Windows/Androidの標準フォントローダーで100%確実にレンダリングされる。

### 4.3 天文学者野帳（Astronomer Notebook）描画器（Compose Canvas）
* **手書きインク表現**:
  * 鉄胆セピアインク（Iron Gall Sepia）の自然な濃淡、微細なインク滲み（Bleeding）、ペン先の走り（Cursive flow）をプロシージャル計算。
* **野帳・罫線キャンバス**:
  * 薄いブルー／グレーの横罫線とマージン線を持つ手記ページテクスチャの上に、文章を流麗にレンダリングして高解像度 PNG として出力する。

---

## 5. 統合スタジオUI および Android IME 仕様

### 5.1 単一統合画面構成（`NebulithStudioScreen`）
1. **上段：リアルタイム双方向変換パネル**
   * 日本語/英語テキスト ⇔ Nebulith NRS転写 ⇔ 独自星辰筆記文字プレビュー。
2. **中段：形態素インスペクター ＆ 未知語昇格パネル**
   * 単語の語幹・接辞・格スロットをチップ表示。
   * 自動造語には `[Auto-Generated]` バッジと「ワンタップ Kotlin コード（`LexiconEntry`）コピー」を提供。
3. **下段：天文学者手記プレビュー ＆ アセット出力パネル**
   * 手書きインク風の手記レンダリングプレビュー、PNG画像保存、および `Nebulith-Regular.ttf` フォント出力。

### 5.2 Android カスタムキーボード（`NebulithInputMethodService`）
* NRS転写ローマ字（`s, y, l, i, m` 等）を入力すると、オンメモリの `StaticLexicon` からリアルタイムに単語候補および独自文字グリフを予測変換バーに提示。
* 通常テキスト（NRSアルファベット）入力と、リッチ画像（手書き手記風ワンフレーズ画像）送信をワンタップで切り替え可能。
