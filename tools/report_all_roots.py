"""Publish the exhaustive screening inventory without auto-renaming roots."""
import hashlib
import json
from collections import Counter
from urllib.parse import quote
from compare_all_roots import ROOT, RUN, LANGUAGES
from nebulith_data import dump


# Individually assessed priority examples, not a distance-based decision rule.
# Accent removal is only screening normalization; a source spelling is retained.
PRIORITY = {
    (110,'en','ring'):'円・環の語義が重なり、rin/ring は末尾1字差。優先して改名案を検討。',
    (222,'ja','kamin'):'眠りと仮眠で近接した語義。kymin/kaminは第2字の母音だけが異なる。日本語の原語形・語義も確認して改名案を検討。',
    (245,'en','palm'):'掌の語義が重なり、palv/palm は末尾1字差。手の語族への影響を調べて改名案を検討。',
    (428,'la','fera'):'動物・獣の語義が重なり、feras/fera は末尾sの有無。優先して改名案を検討。',
    (743,'es','soñar'):'夢を見るという動詞の語義が一致し、正規化後sonan/sonarは末尾1字差。ñの音価差も明記して改名案を検討。',
    (896,'de','Norden'):'北の語義が一致し、novden/nordenはv/rの1字差。方向語の関連語も調べて改名案を検討。',
    (949,'de','voraus'):'前方の語義が重なり、voras/voraus はuの有無。関連する950もまとめて改名案を検討。',
    (950,'de','voraus'):'前へという語義が重なり、vorasu/vorausは末尾su/usの転置。949と語族単位で改名案を検討。',
}


def main():
    result=json.loads((RUN/'comparison.json').read_text(encoding='utf-8'))
    summary=result['summary']; vocab={e['id']:e for e in json.loads((ROOT/'data/lexicon.json').read_text(encoding='utf-8'))['vocabulary']}
    priorities=[];seen=set()
    for c in result['candidates']:
        key=(c['lexiconId'],c['language'],c['sourceForm'])
        if key not in PRIORITY or key in seen:continue
        # Noun/verb confusion cannot silently become a confirmed semantic match.
        if key[0]==743 and c['sourcePos']!='Verb':continue
        seen.add(key)
        priorities.append({'lexiconId':key[0],'entryHash':hashlib.sha256(json.dumps(vocab[key[0]],ensure_ascii=False,sort_keys=True).encode()).hexdigest(),
            'language':key[1],'sourceForm':key[2],'source':c['source'],'sourceSense':c['sourceSense'],
            'meaningSimilar':True,'wholeSpellingSimilar':True,'decision':'propose-change',
            'reviewer':'Codex AI review','reason':PRIORITY[key],
            'limitation':'Orthographic/semantic desk review; not a complete phonetic or human acceptance review.'})
    dump(RUN/'priority-reviews.json',{'scope':'Selected clear spelling-and-meaning pairs; all other screening candidates still require individual review.',
        'dictionarySha256':summary['dictionarySha256'],'entries':priorities})
    languages={'en':'英語','la':'ラテン語','fr':'フランス語','es':'スペイン語','de':'ドイツ語','ja':'日本語（出典のローマ字）'}
    lines=['# 全1008語幹の多言語一括比較（2026-10-15）','',
      f"辞書 v{summary['dictionaryVersion']} の全{summary['processedEntries']}項目を一括処理した。英語の掲載語義は延べ{summary['comparisonCounts']['en']}件、重複を除く照会語は{summary['uniqueEnglishLookups']}件。対象は各辞書項目のNRS語形であり、派生語内部の形態素を別の語幹として追加計数していない。",
      '',f"外部の翻訳表が得られたのは **{summary['entriesWithExternalTranslations']}語**。英語を含む6言語すべてに最低1語形があるのは **{summary['entriesWithAllSixLanguageForms']}語**。これは各項目の全語義を6言語で審査できたという意味ではない。",
      '', '## 一括照合の結果','', '| 言語 | 語幹との比較組数 | 比較語形がある項目数 |','|---|---:|---:|']
    for language in LANGUAGES:
        lines.append(f"| {languages[language]} | {summary['comparisonCounts'][language]} | {sum(bool(e['comparisonCounts'][language]) for e in result['entries'])} |")
    lines += ['',f"合計{sum(summary['comparisonCounts'].values())}組。複数の英語照会語・語義に同じ翻訳が現れる場合も比較組として数える。固有語形数や監査基準の2000語形とは別の指標。取得ページは{summary['retrievedPages']}件。取得失敗・制限により照会できなかったバッチは{len(summary['sourceErrors'])}件。",
      '',f"距離2以下または包含関係による抽出は **{summary['screeningCandidates']}組・{summary['candidateEntryCount']}項目**。これは違反数ではない。意味と語形の両方が一致・酷似する場合だけ変更する方針を維持する。",
      '', '## 優先して修正案を作る項目','', '以下は机上で意味と全体の綴りの近さを確認した例。辞書自体は変更していない。英語2件は既存英語語義との直接比較、他言語は保存したWiktionary翻訳表との比較。発音・語族影響・候補語の再比較を含む改名作業は別段階。',
      '', '| ID | 現語幹 | 比較語 | 判断 |','|---:|---|---|---|']
    for review in priorities:
        entry=vocab[review['lexiconId']]
        lines.append(f"| {entry['id']} | {entry['nrs']} | {languages[review['language']]} {review['sourceForm']} | {review['reason']} |")
    lines += ['', '## 誤検出と保留の扱い','',
      '- `tulos`（天底）に対する `culus/culo` は尻・肛門という別語義。`rin` に対する `Augenringe` は目の下のくま。これらは改名理由にしない。',
      '- `martor` は商人。`factor` の数学的因子・経済資源・構成要素という翻訳を商人の訳と扱わない。',
      '- `sonir` は名詞。動詞「夢を見る」の翻訳に似ているだけでは、同じ品詞・語義の衝突を認定しない。',
      '- `bion/bibō` など、以前に全体の語形が酷似しないと判断した組は、今回再抽出されても距離だけで判断を覆さない。',
      '- 上記以外の抽出候補は候補CSVに原語義と品詞を残した。優先例以外について、個別審査済み・不適合なしとは扱わない。',
      '', '## 全語義比較として残る範囲','',
      '英語照会は辞書のカンマ区切り語義すべてを使い、省略した語幹はない。ただし日本語側だけにある追加語義は独立した対応付けが必要。英語の多義語は全翻訳語義を取得して候補抽出しており、対応しない語義・品詞が混じる。ページなし、翻訳表なし、翻訳先への参照だけの表、今回の抽出器が扱わない入れ子テンプレートは未充足として残す。日本語は出典に明記されたローマ字だけを使い、読みを生成して補わない。',
      '', 'したがって「全1008語を処理」は完了したが、「全1008語の全語義について6言語の意味対応まで審査完了」ではない。CHK-04のWarnと、従来の全語義審査未完了は維持する。今回の大量候補を、承認済み概念リンクや語形変更判定に自動昇格させない。',
      '', '## 成果物と再実行','',
      '- [全1008項目CSV](../runs/2026-10-15-all-roots/entries.csv)：日本語・英語語義、言語別比較組数、候補数、比較語形のない言語。',
      '- [抽出候補CSV](../runs/2026-10-15-all-roots/candidates.csv)：照会語義、翻訳表の語義・品詞、原語形、距離、出典。',
      '- [全比較結果JSON](../runs/2026-10-15-all-roots/comparison.json)：全ID・全英語語義の取得状況、辞書SHA256、制限。',
      '- [優先項目の机上判断](../runs/2026-10-15-all-roots/priority-reviews.json)：現行項目ハッシュ、出典、理由、AI審査の範囲。',
      '- [出典目録](../runs/2026-10-15-all-roots/sources.json)と[sources](../runs/2026-10-15-all-roots/sources/)：API要求、原文スナップショット、SHA256。',
      '- [翻訳表抽出データ](../runs/2026-10-15-all-roots/translations.json)：ページ版ID、出典URL、翻訳表の語義と品詞。',
      '- [監査の検証記録](../runs/2026-10-15-all-roots/check/)：既存監査への補足として今回のスクリーニングを記録。CHK-04の承認とは分ける。',
      '', 'Wiktionary contributorsの出典・版IDを保持する。ライセンスは[Wiktionary:Copyrights](https://en.wiktionary.org/wiki/Wiktionary:Copyrights)を参照。翻訳表は[語義と品詞ごとに分かれる](https://en.wiktionary.org/wiki/Wiktionary:Translations)ため、同じ見出し語という理由だけで意味対応を承認しない。',
      '', '```powershell', '.venv-audit/Scripts/python.exe tools/compare_all_roots.py --offline', '.venv-audit/Scripts/python.exe tools/report_all_roots.py', '```','',
      '保存済み出典でオフライン再実行できる。オンライン取得は同じスナップショットを再利用し、HTTP 429ではRetry-Afterに従う。過去の封印済み監査結果は更新しない。','']
    report=ROOT/'audit/docs/Nebulith All Roots Multilingual Comparison 2026-10-15.md'
    report.write_text('\n'.join(lines),encoding='utf-8')
    print('Report:',report,'priority entries:',len(priorities))


if __name__=='__main__':main()
