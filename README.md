# Nebulith（ネビュリス／星辰語）

天体をモチーフにした人工言語と、手書き風の専用字体・辞書・検証ツールです。

**現在の成果物：辞書v23.4・1008項目／フォントv2.5・87字形・112文字／公式コーパス30件。**

語彙は意味と語形の両方が既存言語と一致・酷似する場合だけ修正します。字形は同じコードの文字と比較し、手書きの筆流を残します。重要な問題は骨格から再編し、軽微な記号は慣用形を残して整えます。

多言語比較の網羅性、人間による筆記・長文読字評価、Windows／Android実機でのアプリ受入は未完了です。「類似ゼロ」「言語全体の完成」「リリース承認」とは扱いません。現行の言語仕様は6母音・4二重母音・18子音と声門キャリアを持ちます。

## 入口

- [開発計画](docs/NEXT_DEVELOPMENT_PLAN.md)
- [言語とアプリの仕様](docs/Project%20Requirements%20And%20Design.md)
- [マスター辞書](docs/Nebulith%20Master%20Lexicon.md)
- [監査結果と判断の履歴](audit/README.md)
- [筆流・サイズ別標本](fonts/handwriting.html)、[記号標本](fonts/punctuation.html)

## 開発と実行の範囲

辞書の正本は `data/lexicon.json`、コーパスの正本は `data/canon_corpus.json`、字体生成は `tools/build_font.py` です。CSV・Kotlin・Markdown、TTF・Web標本は配布・表示用の生成物であり、同じ目的の重複ファイルとして削除しません。

アプリは個人用・完全オフライン・静的辞書を前提とします。開発中の資料取得・監査結果の保存・配布物の作成は、アプリ実行時の外部I/Oとは分けます。自由文の自動翻訳・Android IME・同期機能は実装済みと扱いません。

## 検証と生成

```powershell
.\.venv-audit\Scripts\python.exe -m unittest discover -s tests -v
.\.venv-audit\Scripts\python.exe tools/run_standard_audit.py
.\.venv-audit\Scripts\python.exe tools/build_font.py
.\.venv-audit\Scripts\python.exe tools/sync_web_fonts.py
```

フォント変更は字形審査を、辞書・規則・仕様変更はコーパス審査を失効させる場合があります。単に再生成しただけでは再承認になりません。監査出力は新規ディレクトリへ保存し、封印済み証跡を上書きしません。

## 最小アプリ

[Studioの起動・検証手順](studio/README.md)を参照してください。実装範囲と未確認事項を分けて記録しています。
