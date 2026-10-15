# Nebulith（ネビュリス / 星辰語）

> **「天球の運行と共鳴する、静謐なる星辰の筆記言語」**

Nebulith（ネビュリス）は、天体運行論・軌道力学および自然言語の心地よい音韻美学（シャレイア語・キプソル語等を参考）に基づいて構築された架空言語（Conlang）体系、およびそのタイポグラフィ・ツールキットです。
地球言語（英語、ラテン語、ロマンス諸語等）の安易な借用・既視感を徹底排除した純粋な独自体系を備えています。

---

## ✦ プロジェクト構成

```text
Nebulith/
├── docs/                                # 仕様書・辞書・言語設計書
│   ├── Project Requirements And Design.md  # 総合要件定義書 (v17.0)
│   ├── Nebulith Master Lexicon.md          # 辞書・語彙リファレンス (v18.0 - 計500語幹（目標1,000語中50.0%達成・折り返し到達）・純粋星辰語版)
│   └── Nebulith Executive Summary.md       # プロジェクト総括リファレンス
├── data/                                # 機械可読・構造化語彙データ
│   ├── lexicon.json                     # JSON形式（文法・数詞・接尾辞・語彙メタデータ）
│   ├── lexicon.csv                      # CSV形式（表形式・スプレッドシート連携用）
│   └── StaticLexicon.kt                 # Kotlin形式（KMP Studio用インメモリ辞書コード）
├── fonts/                               # TrueTypeフォント成果物
│   ├── Nebulith-Regular.ttf             # Nebulith公式TrueTypeフォント
│   ├── font_b64.txt                     # Web埋め込み用 Base64
│   └── preview.html                     # フォント確認用HTMLプレビュー
├── tools/                               # フォント生成・辞書ビルド・検証ツール
│   ├── build_font.py                    # fontToolsを用いたTTFバイナリ生成スクリプト
│   ├── generate_preview_html.py         # プレビューHTMLジェネレーター
│   ├── build_master_lexicon_v15.py      # 全数監査＆多形式辞書生成（Markdown/JSON/CSV/Kotlin）
│   └── num_specimen.html                # 文字・数字グリフ見本
├── requirements.txt                     # 依存ライブラリ (fonttools)
└── README.md
```

---

## ✦ 音韻体系 & 公式転写規則（NRS: Nebulith Romanization System）

### 1. 母音（Vowels）
* **6単母音**:
  * `a` [a]（開前舌母音・天球の開口）
  * `e` [e]（半狭前舌母音・星風の流線）
  * `i` [i]（狭前舌母音・北極星の光芒）
  * `o` [o]（半狭後舌円唇母音・満ちる月環）
  * `u` [u]（狭後舌円唇母音・深き天底）
  * `y` [y]（狭前舌円唇母音・第六の星辰母音）
* **4公転二重母音**: `ai` [ai], `ei` [ei], `au` [au], `oi` [oi]

### 2. 16主星子音 + 1原初軸キャリア
* **流音・鼻音（余韻）**: `m, n, l, r`
* **摩擦音（星気）**: `s, z, c [ʃ], j [ʒ]`
* **唇音・気音**: `f, v, h, w`
* **破裂音（天体の会合）**: `p, t, k, b, d, g`
* **原初軸キャリア**: `'` [ʔ]（母音の頭音キャリア・音節分離）

### 3. 音節構造と「柔剛調和」の音韻美学
* **音節骨格**: `(C)V(C)`
* **無標ソノリティ（流麗な基調）**:
  * 開音節（母音終わり）および高い響き度を持つ流音・鼻音・歯擦音 **`l, r, n, m, s`** を基調とし、星辰の滑らかな運行と心地よい余韻を創出。
* **有標ソノリティ（破裂音・摩擦音の機能的活用）**:
  * 概念の硬質さ、瞬発性、鋭敏さ、制動（ブレーキ）やインパクトを表現するため、**破裂音（`-t, -k, -p, -d`）や摩擦音（`-f, -v`）による語末Coda** を積極的に共存。
  * 例: `suf` [suf] (計算・論理の刃), `tor` [tor] (しかし・制動逆接), `kiv` [kiv] (二値光点・最小情報単位), `jyt` [ʒyt] (ノード・網の結節点), `krap` [krap] (甲虫・硬質外骨格), `jylot` [ʒy.lot] (盟約・強固な結束), `torp` [torp] (天体衝突)。

---

### 4. 語根ファミリー血縁体系 & 役割接尾辞
* **単音節核と血縁関係**: `vyr` (星) → `vyris` (恒星), `vylan` (瞳), `vyrel` (観測) など、同じ概念が自然に似た音・文字を共有。
* **役割派生接尾辞**:
  * `-as` (日常の行為者: `neras` 配膳者, `civalas` 歌い手)
  * `-or` (専門職・医師・導師: `darisor` 医師, `sufor` プログラマー, `vyrelor` 観測官)
  * `-is` (学者・探求者: `vyranis` 哲学者, `sufis` 数理学者)
  * `-el` (道具・機械: `pelel` スマホ, `mator` 計算機, `nerel` 料理)
  * `-ar` / `-an` (場所・施設: `darisar` 診療所, `domar` 家, `nerar` カフェ)
  * `-om` (領域・世界: `velom` 森林, `domom` 都市, `sufom` IT空間)
  * `-il` (愛称・縮小: `velil` 若木・薬草)
  * `-i` / `-u` (形容詞化／副詞化: `faluni` 明るい, `eirinu` 常に)

---

## ✦ 独自文字「Nebulith Script」とフォント

具象的な絵文字（象形文字）を排し、流麗な円弧・ループ・星辰ノード（星核）で構成された「丸みを帯びた抽象筆記・記号文字」です。

* **TrueTypeフォント (`fonts/Nebulith-Regular.ttf`)**:
  * PCの標準キーボードから直接タイピング可能（ASCII文字に1対1マッピング）。
  * アルファベット小文字・大文字、星軌数詞（0〜9）、句読点（`. , :`）、原初軸キャリア（`'`）を完全収録（全64グリフ）。
  * 特に数字「7」（七星天蓋弧）、「8」（双極連星環）は地球のアラビア数字から完全に脱却した独自天体幾何学記号として設計。

---

## ✦ 環境構築 & フォント・辞書ビルド手順

```bash
# 仮想環境の作成と有効化
python -m venv .venv
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate

# 依存パッケージのインストール
pip install -r requirements.txt

# フォントのビルド（fonts/Nebulith-Regular.ttf を生成）
python tools/build_font.py

# プレビューHTMLの生成
python tools/generate_preview_html.py

# 全数音韻監査＆多形式辞書のビルド（Markdown, JSON, CSV, Kotlin を同時出力）
python tools/build_master_lexicon_v15.py
```

ブラウザで `fonts/preview.html` を開くことで、生成されたフォントのタイポグラフィと文字標本をインタラクティブに確認できます。
