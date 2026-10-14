# Nebulith（星辰語・ネブリステ語）

> **「天球の運行と共鳴する、静謐なる星辰の筆記言語」**

Nebulith（ネブリステ語）は、天体運行論・軌道力学および自然言語の心地よい音韻美学（シャレイア語・キプソル語等を参考）に基づいて構築された架空言語（Conlang）体系、およびそのタイポグラフィ・ツールキットです。

---

## ✦ プロジェクト構成

```text
Nebulith/
├── docs/                                # 仕様書・辞書・言語設計書
│   ├── Project Requirements And Design.md  # 総合要件定義書 (v17.0)
│   ├── Nebulith Master Lexicon.md          # 辞書・語彙リファレンス (v12.0)
│   └── Nebulith Executive Summary.md       # プロジェクト総括リファレンス
├── fonts/                               # TrueTypeフォント成果物
│   ├── Nebulith-Regular.ttf             # Nebulith公式TrueTypeフォント
│   ├── font_b64.txt                     # Web埋め込み用 Base64
│   └── preview.html                     # フォント確認用HTMLプレビュー
├── tools/                               # フォント生成・検証ツール
│   ├── build_font.py                    # fontToolsを用いたTTFバイナリ生成スクリプト
│   ├── generate_preview_html.py         # プレビューHTMLジェネレーター
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

### 3. 音節構造とソノリティ制限
* **音節骨格**: `(C)V(C)`
* **語末子音（Coda）制限**: 語末（Coda）に立ちうる子音を高い響き度を持つ **`l, r, n, m, s` の5種** に限定。音節の切れ味と余韻の心地よさを両立。

---

## ✦ 独自文字「Nebulith Script」とフォント

具象的な絵文字（象形文字）を排し、流麗な円弧・ループ・星辰ノード（星核）で構成された「丸みを帯びた抽象筆記・記号文字」です。

* **TrueTypeフォント (`fonts/Nebulith-Regular.ttf`)**:
  * PCの標準キーボードから直接タイピング可能（ASCII文字に1対1マッピング）。
  * アルファベット小文字・大文字、星軌数詞（0〜9）、句読点（`. , :`）、原初軸キャリア（`'`）を完全収録。
  * 特に数字「7」（七星天蓋弧）、「8」（双極連星環）は地球のアラビア数字から完全に脱却した独自天体幾何学記号として設計。

---

## ✦ 環境構築 & フォント生成手順

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
```

ブラウザで `fonts/preview.html` を開くことで、生成されたフォントのタイポグラフィと文字標本をインタラクティブに確認できます。
