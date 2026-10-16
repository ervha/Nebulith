# Nebulith on Google Colab: LLM推論サーバー連携ガイド

Google Colabの無料/有料GPU（T4 / A100）を利用してオープンソースLLM推論サーバーを立ち上げ、ローカルのNebulith言語開発システム（動的対話生成・6段階厳格審査・未対応キュー自動トリアージ）と連携させる手順書です。

---

## 1. 全体アーキテクチャ

```
+-------------------------------------------------------------+
| Google Colab (GPU: T4 / A100)                               |
|  - LLM: Qwen/Qwen2.5-7B-Instruct (or Llama-3.1-8B)          |
|  - 推論エンジン: vLLM (OpenAI互換 /v1/chat/completions)     |
|  - トンネル: Cloudflare Tunnel (trycloudflare.com)          |
+-------------------------------------------------------------+
                               | (HTTPS セキュア通信)
                               v
+-------------------------------------------------------------+
| ローカルPC (Nebulith プロジェクト)                          |
|  - tools/llm_agent_dialogue.py (マルチエージェント対話)     |
|  - StrictArbiterEngine (6段階厳格審査ゲート)                |
|  - translation_extensions.json (#40001+ 辞書自動昇格)       |
|  - Web Studio (index.html / standalone.html ダッシュボード) |
+-------------------------------------------------------------+
```

### なぜこの構成なのか？
1. **マシンスペック不要**: ローカルPCに高価なGPUがなくても、Colabの無料GPUで7B〜14BクラスのLLMを高速推論できます。
2. **アカウント登録不要**: トンネリングに Cloudflare Tunnel を使用するため、ngrokのようなアカウント登録やトークン設定、時間制限が一切不要です。
3. **OpenAI互換**: vLLM が OpenAI と全く同じエンドポイント形式（`/v1/chat/completions`）を提供するため、コード変更なしでシームレスに接続できます。

---

## 2. Google Colab で推論サーバーを建てる手順（所要時間: 約3分）

### Step 1: ノートブックを開く
1. ブラウザで [Google Colab](https://colab.research.google.com/) を開きます。
2. 「アップロード」タブから、本リポジトリの `colab/nebulith_inference_server.ipynb` をアップロードします。
3. 上部メニューの **「ランタイム」➔「ランタイムのタイプを変更」** をクリックし、**「T4 GPU」**（または A100）を選択して「保存」します。

### Step 2: セルを上から順に実行する
ノートブック内の各セルを実行します：
1. **Cell 1 (セットアップ)**: `vLLM` と `cloudflared` が自動インストールされます。
2. **Cell 2 (vLLM起動)**: `Qwen/Qwen2.5-7B-Instruct` がGPUにロードされ、OpenAI互換サーバーが立ち上がります。
3. **Cell 3 (トンネル発行)**: 公開アクセス用URLが発行されます。

出力の末尾に、以下のように表示されます：
```text
===========================================================================
★ Nebulith Colab 推論サーバーが接続準備完了しました！
API Base Endpoint: https://random-words-1234.trycloudflare.com/v1
===========================================================================
```

この `https://random-words-1234.trycloudflare.com/v1` をコピーします。

---

## 3. ローカルPCからの利用方法

ローカルのターミナル（PowerShell / Bash）で、コピーしたURLを指定して実行します。

### ① 接続テスト（ヘルスチェック）
```powershell
python tools/llm_agent_dialogue.py --provider colab --endpoint "https://random-words-1234.trycloudflare.com/v1" --health-check
```
> `[HEALTH-CHECK SUCCESS] Connected to https://...` と表示されれば接続成功です。

### ② 任意のテーマでAI対話生成＆6段階厳格審査を実行
```powershell
python tools/llm_agent_dialogue.py --provider colab --endpoint "https://random-words-1234.trycloudflare.com/v1" --topic "港と航海、波の音"
```
- Colab上のLLMが2体のエージェント（船乗り・見送り人）として対話を生成します。
- ローカルの審判エンジン（`StrictArbiterEngine`）がリアルタイムに6段階審査（音韻・語根衝突・意味重複・形態素・VSO構文・合意再利用）を実施します。
- 合格した新語は自動的に `#40001+` 番台として `data/translation_extensions.json` および監査台帳 `data/emergent_lexicon_audit.json` へ昇格・記録されます。

### ③ ユーザー未対応キュー（feedback_queue）の自動トリアージ
Web Studio からエクスポートした未対応辞書リクエスト（JSON）を、Colab推論サーバーを使って自動造語・審査・解決します：
```powershell
python tools/triage_feedback_queue.py data/your_feedback_queue.json --provider colab --endpoint "https://random-words-1234.trycloudflare.com/v1"
```

### ④ Web Studio への反映と確認
対話・新語生成が終わったら、Web Studio を再ビルドしてブラウザで確認します：
```powershell
python tools/build_web_studio.py
```
- [web/index.html](file:///C:/Users/danun/Desktop/Project/Nebulith/web/index.html) を開くと、第5タブ **「AI対話創発・厳格監査」** に Colab で生成された最新の対話ログと合格語彙が即座に反映されます。

---

## 4. 推奨モデル一覧

Colabの無料枠（T4: 16GB VRAM）および有料枠で動作確認済みの推奨モデル：

| モデル名 | サイズ | 特徴・推奨理由 |
| :--- | :--- | :--- |
| **`Qwen/Qwen2.5-7B-Instruct`**（デフォルト推奨） | 7B | 日本語・英語・未知構文の追従性能が極めて高く、VSO語順や格標識（`el, ia, uo...`）の規則を正確に守ります。T4で高速動作。 |
| **`meta-llama/Meta-Llama-3.1-8B-Instruct`** | 8B | 文脈推論・語彙合成の論理性が非常に高い。Hugging Faceのトークンが必要。 |
| **`elyza/Llama-3-ELYZA-JP-8B`** | 8B | 日本語のニュアンス理解に特化したモデル。 |

別のモデルを使用したい場合は、ノートブック内の `MODEL_ID = "..."` またはローカルの `--model "..."` 引数で切り替え可能です。
