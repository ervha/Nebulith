"""Apply and record the specific five-unit corpus review of 2026-10-15."""
import json
import re
from nebulith_data import ROOT, dump, entry_hash, reference, validate_corpus, corpus_markdown
from corpus_review import analyze_unit, dependency_hash


def main():
    p = ROOT / 'data/canon_corpus.json'
    corpus = json.loads(p.read_text(encoding='utf-8'))
    vocab = json.loads((ROOT / 'data/lexicon.json').read_text(encoding='utf-8'))['vocabulary']
    roots = {r['nrs']: r for r in vocab}
    rules = json.loads((ROOT / 'data/corpus_rules.json').read_text(encoding='utf-8'))
    spec_path = ROOT / 'docs/Project Requirements And Design.md'
    spec = spec_path.read_text(encoding='utf-8')
    start = spec.index('<!-- BEGIN GENERATED CANON -->')
    prefix = spec[:start]
    if '<!-- CORPUS FRAME SCOPE -->' not in prefix:
        prefix += ('<!-- CORPUS FRAME SCOPE -->\n'
                   '### 6.4.1 公式コーパスの項構造・時制の明示\n\n'
                   'コーパスで用いる動詞の語義・必須項・許容格は `data/corpus_rules.json` に記録する。'
                   'この表は全文法を解析するものではなく、公式例文の解釈を固定する。'
                   'falunは§6.2の「光る」の自動詞用法、relenはel主語＋ia補語、poranはel主体＋任意のto目的地、'
                   'neranはel主体＋任意のia食物を取る。vyrelの受動態は被観測対象をelで示す。'
                   '独立する過去節はfeを各節へ明記し、前文からの時制継承を仮定しない。'
                   '箴言の「時が歩む」は擬人化で、実際の歩行や時制・願望の追加を意味しない。\n\n')
    spec_path.write_text(prefix+spec[start:], encoding='utf-8')
    revisions = {
        'aphorism': ('Relen el vyran ia tolst en sente. Tor poran el havel, falun el vyr.',
                     '真理は万物の礎である。時が進んでも、星は輝く。',
                     'relenの主語vyran・補語tolst en sente、tor節の主語havelとporanの擬人化、主節の自動詞falunを照合。klovanの他動詞語義を尽きるへ拡張する旧表現を削除。'),
        'observation': ('Fe vyrelcor el vyrelor uo vyrelar to falden. Fe falunast el vyr syvan uo celvan. Fe revyrel el corval en celmon.',
                        '天文学者は天文台にて東方を定期観測した。天球で新しい星が輝き始めた。暗黒星雲の重心が観測された。',
                        '3節へ過去feを明記。反復cor・始動ast・受動re、uo場所・to方向・en属格を照合。既存形容詞syvanを直接後置し、不要な-iを除去。'),
        'dialogue-a1': ('Falun el vyrin. Poran el taas to kauo ka?',
                        '星々が輝きます。あなたはどこへ歩きますか。',
                        'vyr+-inの複数、無標現在、二人称taas、向格to kauoと文末kaを照合。祈願や進行を訳へ付加しない。'),
        'dialogue-b': ('Poran el mi to govan en cynor. Nerancor el mi ia nyrat uo nerar.',
                       '私は友の家へ歩きます。私は普段、食堂で主食を食べます。',
                       '単数mi、govan en cynorの所有関係、反復cor、対格nyrat・処格nerarを照合。複数・共同行為・進行の旧訳を除去。'),
        'dialogue-a2': ('Relen el laris en taas ia sirin. Poran el mi to falden.',
                        'あなたの軌道は穏やかです。私は東へ歩きます。',
                        'relenのel主語laris en taas・ia性質補語sirin、poranのel miとto faldenを照合。軌道の穏やかさは比喩で、祈願・未来の保証を含めない。')}
    if {u['id'] for u in corpus['units']} != revisions.keys():
        raise ValueError('This review only covers the five declared units')
    for unit in corpus['units']:
        nrs, translation, note = revisions[unit['id']]
        unit['nrs'], unit['translationJa'] = nrs, translation
        unit['tokens'] = [{'id': f"{unit['id']}:t{i:02d}", 'surface': token, **reference(token, roots)}
                          for i, token in enumerate(re.findall(r"[a-z']+", nrs.lower()), 1)]
        analysis = analyze_unit(unit, vocab, rules)
        if analysis['errors']:
            raise ValueError(analysis)
        unit['syntaxReview'] = analysis
        batch = json.loads((ROOT / 'data/audit/corpus_review_batch_2026-10-15.json').read_text(encoding='utf-8'))
        if dependency_hash(unit, vocab, rules) != batch['dependencyHashes'].get(unit['id']):
            raise ValueError('Review dependencies changed; perform a new semantic review instead of reusing this batch')
        content = {k: v for k, v in unit.items() if k != 'review'}
        unit['review'] = {'status': 'approved', 'reviewer': 'Codex', 'reviewType': 'AI linguistic review',
                          'criteriaVersion': rules['version'], 'note': note,
                          'reviewedAgainstUnitHash': entry_hash(content),
                          'reviewedAgainstDependenciesHash': dependency_hash(unit, vocab, rules)}
    if validate_corpus(corpus, vocab):
        raise ValueError('Invalid references')
    dump(p, corpus)
    spec_path.write_text(prefix+corpus_markdown(corpus, vocab), encoding='utf-8')
    print('Reviewed five units against explicit frames, dictionary senses and translations.')


if __name__ == '__main__':
    main()
