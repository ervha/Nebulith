"""Apply bounded, repeatable corrections; never approve outstanding reviews."""
import json
import re
from pathlib import Path

from nebulith_data import ROOT, corpus_markdown, dump, entry_hash, export_lexicon, reference


def main():
    data = json.loads((ROOT / 'data/lexicon.json').read_text(encoding='utf-8'))
    ids = set(range(253, 258)) | set(range(386, 391)) | {775, 776, 820, 851, 852, 853}
    for r in data['vocabulary']:
        if r['id'] in ids:
            r['ipa'] = r['ipa'].replace('ei', 'eɪ')
    if tuple(map(int, data['version'].split('.'))) < (23, 2):
        data['version'] = '23.2'
    data['status'] = '監査中。全項目適合・リリース承認は未実施。'
    data['phoneticRules']['codaSonorityHierarchy'].pop('markedExceptionsApproved', None)
    data['phoneticRules']['codaSonorityHierarchy']['markedReviewFile'] = 'data/audit/coda_reviews.json'
    export_lexicon(data)
    vocab = data['vocabulary']
    roots = {r['nrs']: r for r in vocab}
    corpus_path = ROOT / 'data/canon_corpus.json'
    if not corpus_path.exists():
        draft = [
            ('aphorism', 'テクスト1：星辰箴言', 'NRS',
             'Relen el vyran ia tolst en sente: tor poran el havel, ne klovol el falun en vyr.',
             '真理は万物の床（礎）である。時が歩み去ろうとも、星の光が尽き果てることはない。',
             'klovan/klovolの自他・項構造と詩的な意味を要確認。'),
            ('observation', 'テクスト2：天文台の日誌', 'NRS',
             'Fe vyrelcor el vyrelor uo vyrelar to falden. Falunast el vyr syvani uo celvan, fe revyrel el corval en celmon.',
             '天文学者は天文台にて東の空を定期観測した。天球に新たな星が光を放ち始め、暗黒星雲の重心が観測された。',
             '時制の連続と観測内容の意味を要確認。'),
            ('dialogue-a1', 'テクスト3：対話A（導入）', 'A',
             'Falun el vyrin. Poran el taas to kauo ka?',
             '星々が輝いています。あなたはどこへ歩きますか。', '一般構文へ改訂。対話全体の意味審査待ち。'),
            ('dialogue-b', 'テクスト3：対話B', 'B',
             'Poran el mi to govan en cynor. Nerancor el mi ia nyrat uo nerar.',
             '私は友の家へ歩きます。私は普段、食堂で主食を食べます。', '単数・反復相へ和訳を修正。全体の意味審査待ち。'),
            ('dialogue-a2', 'テクスト3：対話A（応答）', 'A',
             'Relen el laris en taas ia sirin. Poran el mi to falden.',
             'あなたの軌道は穏やかです。私は東へ歩きます。', '祈願を叙述へ改訂。対話全体の意味審査待ち。')]
        corpus = {'version': '23.2', 'units': []}
        for id_, title, label, nrs, ja, note in draft:
            tokens = [{'id': f'{id_}:t{i:02d}', 'surface': token, **reference(token, roots)}
                      for i, token in enumerate(re.findall(r"[a-z']+", nrs.lower()), 1)]
            corpus['units'].append({'id': id_, 'title': title, 'label': label, 'nrs': nrs,
                                    'translationJa': ja, 'review': {'status': 'pending', 'note': note},
                                    'tokens': tokens})
        dump(corpus_path, corpus)
    corpus = json.loads(corpus_path.read_text(encoding='utf-8'))
    spec_path = ROOT / 'docs/Project Requirements And Design.md'
    spec = spec_path.read_text(encoding='utf-8')
    spec = re.sub(r'\*\*文書バージョン\*\*:.*', f"**文書バージョン**: v{data['version']}（監査中・個別の未完了項目あり）", spec)
    spec = spec.replace('16主星子音', '18主星子音').replace('16主子音', '18主子音').replace('16子音', '18子音')
    inventory_path = ROOT / 'fonts/inventory.json'
    if inventory_path.exists():
        inventory = json.loads(inventory_path.read_text(encoding='utf-8'))
        spec = spec.replace('65グリフ', str(inventory['glyphCount'])+'グリフ')
        spec = spec.replace('Nebulith Script v2.1', 'Nebulith Script v'+inventory['fontVersion'])
    start = spec.index('* **無標基底末子音')
    end = spec.index('\n---', start)
    marked = [r for r in vocab if r['nrs'][-1] not in 'aeiouylrnms']
    spec = spec[:start] + (
        f'* **無標基底末子音**: `l, r, n, m, s` または母音末を基底とする。現在は{len(vocab)-len(marked)}語、有標末子音は{len(marked)}語。件数は辞書から検証する。\n'
        '* **有標末子音の個別審査**: 堅固・瞬発概念等の適用理由を `data/audit/coda_reviews.json` に語別に記録する。専門語・カテゴリー所属だけで一括承認しない。承認・棄却・未完了数は台帳から計算し、全件を一括承認して準拠率を引き上げない。\n'
        '* **形態論層**: 相接尾辞 `-ast/-in/-ol/-cor`、方向副詞化 `-u` 等は§2.3/§6.2の結合規則に従い、辞書語幹の末子音審査とは分ける。\n'
    ) + spec[end:]
    spec = spec.replace('動作主・道具・原因は具格 **`de`**（〜によって）または起格 **`al`**（〜より）で後置される。',
                        '動作主・道具・原因は具格 **`de`**（〜によって）で後置される。起点は奪格 **`va`**、受け手・受益者は与格 **`al`** を用い、alを起格に再定義しない。')
    spec = spec.replace('`.notdef` は外周矩形＋中央星辰特異点核', '`.notdef` は2つの矩形輪郭による欠字枠（中央核なし）')
    spec = spec.replace('Advance Width 400', 'Advance Width 320、左サイドベアリング30')
    spec = spec.replace('全接尾辞は語末ソノリティ制限 `l, r, n, m, s` に完全適合',
                        '接尾辞は語幹のソノリティ審査と区別して各結合規則で定義')
    spec = spec.replace('Windows/Androidの標準フォントローダーで100%確実にレンダリングされる',
                        'Windows/Androidの標準フォントローダーを検証対象とする。描画の適合は各対象環境で確認する')
    spec = spec.replace('この客観的基準に基づき、全65グリフにおいて英数字の単純骨格残存は **0件** であることが立証される。',
                        '上表はデザイン意図の説明であり、残存0件の判定記録ではない。全65グリフの個別評価は `data/audit/glyph_reviews.json` に記録し、現在は審査待ちとする。')
    spec = spec.replace('は、ラテンアルファベットやアラビア数字の単純な活字骨格（縦直線・単一円弧・クロスバー）を完全に脱却し、',
                        'は、ラテンアルファベットやアラビア数字からの独立した意匠を目指し、')
    if '<!-- BEGIN QUERY RULES -->' not in spec:
        at = spec.index('\n---', spec.index('### 2.6 '))
        spec = spec[:at] + ('\n<!-- BEGIN QUERY RULES -->\n'
             '* **格句内の疑問語**: 場所相関詞kauoを`to kauo`のように格詞の後へ置き、文末kaで問いを示せる（例: `Poran el taas to kauo ka?`）。\n'
             '* **コピュラ補語**: relenのia補語には名詞または性質を表す形容詞を置ける（例: `Relen el laris en taas ia sirin.`）。\n'
             '<!-- END QUERY RULES -->\n') + spec[at:]
    if '<!-- BEGIN GENERATED CANON -->' in spec:
        spec = spec[:spec.index('<!-- BEGIN GENERATED CANON -->')]
    else:
        spec = spec[:spec.index('### 6.5 ')]
    spec += corpus_markdown(corpus, vocab)
    spec_path.write_text(spec, encoding='utf-8')
    coda_path = ROOT / 'data/audit/coda_reviews.json'
    if not coda_path.exists():
        dump(coda_path, {'scope': 'SOP CHK-08; semantic review required', 'entries': [
            {'lexiconId': r['id'], 'nrs': r['nrs'], 'finalConsonant': r['nrs'][-1],
             'decision': 'pending', 'ruleId': None, 'reason': None, 'reviewer': None,
             'reviewedAgainstEntryHash': entry_hash(r)} for r in marked]})
    glyph_path = ROOT / 'data/audit/glyph_reviews.json'
    if not glyph_path.exists():
        import hashlib
        from fontTools.ttLib import TTFont
        font_path = ROOT / 'fonts/Nebulith-Regular.ttf'
        font = TTFont(font_path)
        cmap = font.getBestCmap()
        dump(glyph_path, {'fontSha256': hashlib.sha256(font_path.read_bytes()).hexdigest(),
                         'entries': [{'glyph': name, 'codepoints': [c for c, g in cmap.items() if g == name],
                                      'decision': 'pending', 'reason': None, 'reviewer': None}
                                     for name in font.getGlyphOrder()]})
    print('Applied bounded corrections; review decisions remain in their individual ledgers.')


if __name__ == '__main__':
    main()
