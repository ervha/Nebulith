# Nebulith 監査資料

- [口語否定・保留語の継続開発記録](maintenance/negative-readings-20261023/report.md)：意味選択、関連語との語義差、検証範囲と残件。言語体系全体の監査完了を意味しません。

- [最新：全1008語幹の多言語一括比較](docs/Nebulith%20All%20Roots%20Multilingual%20Comparison%202026-10-15.md)：6言語35,082組を照合、153候補・43項目、優先修正候補8項目。外部翻訳910項目、6言語の語形あり673項目。全語義の意味対応審査は未完了。

監査手順・報告書・修正案は [`docs/`](docs/) に集約しています。言語の仕様とマスター辞書は引き続きルートの `docs/` にあります。

- [最新：開発計画の実行と整理](docs/Nebulith%20Development%20Execution%202026-10-15.md)：辞書v23.4、50項目の出典調査、コーパス30件、Kotlin/JVMのWindows PoC、不要82ファイル整理。実機受入・全語義比較は未完了。

- [保留字形の重要度別修正](docs/Nebulith%20Pending%20Glyph%20Remediation%202026-10-15.md)：v2.5で重要5字形を再編、記号27字形を微修正、機能2字形を確認。デザイン85承認・機能2確認・保留0。Pass 13 / Warn 1 / Reference 1。

- [手書き感と対応文字による再確認](docs/Nebulith%20Handwriting%20Glyph%20Review%202026-10-15.md)：v2.4のA/a・S/sを曲線主体に修正。当時の全87字形を確認し、53承認・34保留。別文字との競合は対象外。

- [字形v2.3の修正と再確認](docs/Nebulith%20Glyph%20Revision%202026-10-15.md)：Pass 12 / Warn 2 / Reference 1。U/u・J/jの骨格修正、多言語比較87語・587組。全項目適合は未認定。

- [現行方針による再監査（字形修正前）](docs/Nebulith%20Policy%20Aligned%20Audit%202026-10-15.md)：Pass 12 / Fail 1 / Warn 1 / Reference 1。84語・551組の比較、飛ぶの語幹修正、語末基準の参考化。

- [語彙変更の現行方針](docs/Nebulith%20Lexical%20Change%20Policy%202026-10-15.md)：意味と語形の両方が一致・酷似する場合だけ変更。それ以外はスルー。語末だけを理由とする127語の改名は進めない。

- [直前の個別審査・修正結果](docs/Nebulith%20Review%20Findings%202026-10-15.md)：当時の基準でPass 12 / Fail 2 / Warn 1。コーパス審査と石の語族修正、語末127語・字形4件の不適合、多言語の残範囲。

- [記号フォントv2.2の追加・検証](docs/Nebulith%20Symbols%20Validation%202026-10-15.md)：疑問符等の追加と監査対象の版更新。字形独自性は引き続き保留。

- [修正実施状況](docs/Nebulith%20Remediation%20Progress%202026-10-15.md)：今回の変更・検証・未審査事項。
- [第2回再監査](docs/Nebulith%20Audit%20Results%202026-10-15-Reaudit-02.md)：修正前の確定記録。Pass 10 / Fail 1 / Warn 4。
- [修正案](docs/Nebulith%20Remediation%20Proposal%202026-10-15.md)：変更方針・完了条件。
- [標準監査手順書](docs/Nebulith%20Standard%20Audit%20Report.md)：監査基準。
- [初回監査](docs/Nebulith%20Audit%20Results%202026-10-15.md)、[第1回再監査](docs/Nebulith%20Audit%20Results%202026-10-15-Reaudit.md)：履歴。第1回の15/15・RELEASE APPROVEDは第2回で裏付け不足と判定されています。

`2026-10-15*` は過去の証跡、`runs/` は上書きしない新規実行結果です。今回の自動検査が通っても、多言語比較・個別例外・字形・コーパス意味審査の完了やリリース承認を意味しません。

## 文書移動と過去のハッシュ

相対リンクを更新した閲覧用文書を `docs/` へ移しました。移動前の文書は [`archive/original-documents/`](archive/original-documents/) にバイト単位で保存し、旧パス・新パス・原本ハッシュを [`document-migration.json`](document-migration.json) に記録しました。過去の証跡中のパス・ハッシュは当時の入力を示し、現在の成果物との相違を隠すために書き換えていません。

```powershell
python tools/verify_audit_archive.py
.\.venv-audit\Scripts\python.exe -m unittest discover -s tests -v
.\.venv-audit\Scripts\python.exe tools/run_standard_audit.py
```

コマンドはリポジトリルートで実行します。監査出力は既定で `audit/runs/<UTC日時>-<実行ID>/` を新規作成します。`--output audit/runs/<新しい名前>` でも指定できます。既存出力先への書き込みは拒否します。

終了コードは0＝自動検査範囲で適合、1＝不適合あり、2＝範囲・個別審査が未完了。実行エラーは例外として出力され、合格記録を生成しません。不適合と未完了が混在すれば1を返し、内訳は `evidence.json` に残ります。検査結果と意味・字形の審査記録は分けて確認します。
