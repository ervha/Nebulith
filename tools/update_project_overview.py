"""Refresh maintained entry documents; never alter historical audit reports."""
import json
from nebulith_data import ROOT


def main():
    data=json.loads((ROOT/'data/lexicon.json').read_text(encoding='utf-8'))
    font=json.loads((ROOT/'fonts/inventory.json').read_text(encoding='utf-8'))
    corpus=json.loads((ROOT/'data/canon_corpus.json').read_text(encoding='utf-8'))
    status=f"辞書v{data['version']}・{len(data['vocabulary'])}項目／フォントv{font['fontVersion']}・{font['glyphCount']}字形・{font['mappedCharacterCount']}文字／公式コーパス{len(corpus['units'])}件"
    intro=f'''# Nebulith（ネビュリス／星辰語）

天体をモチーフにした人工言語と、手書き風の専用字体・辞書・検証ツールです。

**現在の成果物：{status}。**

語彙は意味と語形の両方が既存言語と一致・酷似する場合だけ修正します。字形は同じコードの文字と比較し、手書きの筆流を残します。重要な問題は骨格から再編し、軽微な記号は慣用形を残して整えます。

多言語比較の網羅性、人間による筆記・長文読字評価、ブラウザー・モバイルでのアプリ受入は未完了です。「類似ゼロ」「言語全体の完成」「リリース承認」とは扱いません。現行の言語仕様は6母音・4二重母音・18子音と声門キャリアを持ちます。

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
.\\.venv-audit\\Scripts\\python.exe -m unittest discover -s tests -v
.\\.venv-audit\\Scripts\\python.exe tools/run_standard_audit.py
.\\.venv-audit\\Scripts\\python.exe tools/build_font.py
.\\.venv-audit\\Scripts\\python.exe tools/sync_web_fonts.py
.\\.venv-audit\\Scripts\\python.exe tools/build_web_studio.py
.\\.venv-audit\\Scripts\\python.exe tools/verify_web_bundle.py
```

フォント変更は字形審査を、辞書・規則・仕様変更はコーパス審査を失効させる場合があります。単に再生成しただけでは再承認になりません。監査出力は新規ディレクトリへ保存し、封印済み証跡を上書きしません。
'''
    if (ROOT/'web').exists():
        intro+='\n## Webアプリ\n\n[Web版の利用・生成手順](web/README.md)を参照してください。単一HTML版はダウンロードしてオフラインで開けます。exe・JVM版は廃止しました。\n'
    (ROOT/'README.md').write_text(intro,encoding='utf-8')
    summary='''# Nebulith 現状と設計の総括

**更新日：2026-10-15。**

STATUS。

現在は言語・字体・検証ツールを整備し、Webアプリを整備する段階です。過去の文書にあった「地球言語類似ゼロ」「完全完成」という表現は現在の認定ではありません。多言語比較の不足と、人間による使用評価は別に残っています。

## 方針と実装範囲

1. 語彙変更は意味と語形が両方とも一致・酷似する場合に限定し、個別に根拠を記録する。語末だけによる一律改名はしない。
2. 字体は同じ文字との骨格比較と筆流・字風の調和を確認し、別の文字との競合は無視する。記号の慣用形を許容し、機能字形は別に確認する。
3. アプリはWeb版に一本化。辞書・文法語検索、専用字体表示、途中入力の日本語→Nebulith変換、登録対訳、未対応記録を端末内で扱う。exe・JVM版は廃止した。
4. 自動造語・辞書昇格・一般的な双方向構文変換・AndroidシステムIME・ピュアKotlin字体生成は後続の設計であり、現在の機能として扱わない。

開発時には出典の取得、生成物の書き出し、検査ログの保存を行う。アプリのオフライン実行・入力処理とは区別する。外部サーバー、アカウント、同期は導入しない。

## 正本と証跡

- 辞書：`data/lexicon.json`。CSV・Kotlin・Markdownへ決定論的に展開する。
- コーパス：`data/canon_corpus.json`。本文・訳・語彙参照・審査を管理する。
- 字体：生成コードと`fonts/inventory.json`。現在の配布物と標本を同期する。
- 監査：[audit/README.md](../audit/README.md)。過去の判定は当時の基準による履歴として保持する。
- 実行順序：[開発計画](NEXT_DEVELOPMENT_PLAN.md)。完了と未実施を区別して追記する。

人間の筆記・長文読字、ブラウザー・モバイルの実機受入、最終リリース判断は自動検査・AI審査と分離する。
'''.replace('STATUS',status)
    (ROOT/'docs/Nebulith Executive Summary.md').write_text(summary,encoding='utf-8')


if __name__=='__main__':main()
