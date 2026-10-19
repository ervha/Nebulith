# Nebulith on Google Colab: LLM推論サーバー連携ガイド

Google Colabの無料/有料GPU（T4 / A100）を利用してオープンソースLLM推論サーバーを立ち上げ、ローカルのNebulith言語開発システム（トピック自動生成・動的対話生成・6段階厳格審査・監査待ち台帳記録）と連携させる手順書です。

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
|  - tools/llm_agent_dialogue.py                              |
|    * トピック自動発案（Auto-Topic Generator）               |
|    * マルチエージェント対話（Colab Qwen2.5-7B連携）         |
|    * 回数指定自動ループ実行（--rounds N）                   |
|  - StrictArbiterEngine (6段階厳格審査ゲート)                |
|  - emergent_lexicon_audit.json (監査待ち候補台帳)           |
|    ※本番単語辞書への組み込みは人間による本番監査後とする   |
+-------------------------------------------------------------+
```

---

## 2. 実行コマンド（トピック自動生成＆回数指定ループ）

Colab ノートブックは起動のたびに API キーを生成し、vLLM を `--api-key` 付きで立ち上げます。表示されたキーとトンネル URL を、ローカルでは次の環境変数に入れてください。公開トンネルの URL はリポジトリに既定値として書きません。

- `NEBULITH_LLM_ENDPOINT` … ノートブックが表示した `https://….trycloudflare.com/v1`
- `NEBULITH_LLM_API_KEY` … ノートブックが表示した vLLM の API キー

`OPENAI_API_KEY` は `api.openai.com` にだけ送ります。自前のトンネルやローカル vLLM には使いません。

### ① 接続テスト（ヘルスチェック）
```powershell
$env:NEBULITH_LLM_ENDPOINT = "https://your-tunnel.trycloudflare.com/v1"
$env:NEBULITH_LLM_API_KEY = "ノートブックが表示したキー"
python tools/llm_agent_dialogue.py --health-check
```
> `[HEALTH-CHECK SUCCESS] Connected to https://... (Available models: ['Qwen/Qwen2.5-7B-Instruct'])` と表示されれば接続完了です。

同じ値は `--endpoint` と `--api-key` でも渡せます。

### ② トピック自動生成＆回数指定の自動連続実行（推奨）
トピックを指定せず、指定した回数（例: 5回）自動で新しいシチュエーションを発案し、対話と新語生成・6段階審査を連続実行します：
```powershell
# 5ラウンド自動実行
python tools/llm_agent_dialogue.py --endpoint $env:NEBULITH_LLM_ENDPOINT --api-key $env:NEBULITH_LLM_API_KEY --rounds 5

# 10ラウンド自動実行
python tools/llm_agent_dialogue.py --rounds 10
```

**各ラウンドの自動実行フロー**:
1. **トピック自動発案**: 星辰文明・天測・自然気象・工芸・生活・感情等のテーマから、未表現の語彙ギャップをLLMが自動着想
2. **マルチエージェント対話生成**: 2体の話者（Agent A, Agent B）が状況に応じた対話を交わし、新語（*word）を提案・了解・再利用
3. **6段階厳格審査（Strict Arbiter）**: 音韻、レーベンシュタイン距離（編集距離>=1）、意味重複、形態論、VSO構文、合意再利用をリアルタイム審査
4. **監査待ち台帳へ記録**: 審査合格語は `data/emergent_lexicon_audit.json` に「監査待ち（pending_review）」として安全に記録・蓄積（本番辞書へは自動組み込みされません）

### ③ 特定のトピックを指定して実行する場合
```powershell
python tools/llm_agent_dialogue.py --topic "港の朝露と砕ける波音、船旅への祈り"
```

### ④ 新しいColabエンドポイントURLを指定する場合
Colabを再起動すると Cloudflare Tunnel の URL と API キーが新しくなります。どちらも省略せず指定します：
```powershell
python tools/llm_agent_dialogue.py --endpoint "https://your-new-tunnel.trycloudflare.com/v1" --api-key "ノートブックが表示したキー" --rounds 3
```

語彙の一括拡張も同じ接続先を要求します。

```powershell
python tools/batch_colab_lexicon_expansion.py --endpoint $env:NEBULITH_LLM_ENDPOINT --api-key $env:NEBULITH_LLM_API_KEY
python tools/batch_colab_daily_conversation_expansion.py --endpoint $env:NEBULITH_LLM_ENDPOINT --api-key $env:NEBULITH_LLM_API_KEY
```

---

## 3. ガバナンス方針：実際の単語への組み込みは監査後

生成された単語候補は、自動で本番辞書（`data/translation_extensions.json`）には書き込まれません。
- すべて [data/emergent_lexicon_audit.json](file:///C:/Users/danun/Desktop/Project/Nebulith/data/emergent_lexicon_audit.json) に審査スコア・対話シナリオ全文・不合格ログと共に蓄積されます。
- 人間による本番監査・レビューを経て、公式語彙や体系拡張（#20000+）へ正式に昇格させる厳格な運用を行っています。
