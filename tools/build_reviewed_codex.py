"""Source-backed print edition. No synthetic scripture or unreviewed candidate promotion."""
import hashlib
from evidence_hash import recorded_digest_matches
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def build_codex():
    from nebulith_data import validate_corpus, corpus_semantic_pending
    from corpus_review import analyze_unit, dependency_hash
    from literary_sourcebook import build_sourcebook, words as literary_words
    from literary_layout import BOOK_CSS, story_html, story_markdown
    book=build_sourcebook()
    corpus = load('data/canon_corpus.json')
    canon = load('data/lexicon.json')['vocabulary']
    rules = load('data/corpus_rules.json')
    if corpus_semantic_pending(corpus, canon, rules):
        raise ValueError('Corpus content or semantic approval is stale')
    if validate_corpus(corpus, canon):
        raise ValueError('Corpus reference errors')
    for unit in corpus['units']:
        review = unit.get('review', {})
        if review.get('status') != 'approved' or review.get('reviewedAgainstDependenciesHash') != dependency_hash(unit, canon, rules):
            raise ValueError('Stale or missing corpus approval: ' + unit['id'])
        if analyze_unit(unit, canon, rules)['errors']:
            raise ValueError('Corpus syntax error: ' + unit['id'])
    learning = load('data/everyday_vocabulary_review.json')
    source_sha = hashlib.sha256((ROOT / learning['source']).read_bytes()).hexdigest()
    if not recorded_digest_matches(ROOT / learning['source'], learning['sourceSha256']):
        raise ValueError('Learning index source is stale')
    by_id = {r['id']: r for r in canon}
    for row in learning['entries']:
        if any(row[k] != by_id[row['id']][k] for k in row):
            raise ValueError('Learning entry differs from canonical source')
    words = {r['nrs']: r for r in canon}
    for row in load('data/grammar_dictionary.json')['entries']:
        words.setdefault(row['nrs'], row)
    words={r['nrs']:r for r in literary_words()}
    e = lambda text: escape(str(text))
    font = (ROOT / 'fonts/font_b64.txt').read_text(encoding='utf-8').strip()
    css = '''
    @page {size:A4;margin:17mm 15mm 18mm;}
    * {box-sizing:border-box} body {font-family:'Yu Gothic','Meiryo',sans-serif;color:#24354a;font-size:9pt;line-height:1.65;margin:0}
    h1 {font-family:'Yu Mincho',serif;font-size:29pt;line-height:1.6;color:#193b54}
    h2 {font-size:19pt;border-bottom:1px solid #95b1c5;padding-bottom:8pt} h3 {font-size:12pt;color:#315e75}
    .cover {height:240mm;padding:25mm 9mm;border:2px solid #315e75;page-break-after:always}
    .eyebrow {letter-spacing:3px;font-size:10pt;color:#577488}.subtitle {font-size:14pt;margin:18pt 0 28pt}
    .section {page-break-before:always} .note {background:#f0f5f7;padding:10pt 12pt;color:#4b6576}
    .example {break-inside:avoid;padding:10pt 0;border-bottom:1px solid #d9e2e7}
    .nrs {font-family:Georgia,serif;font-size:12pt;color:#183f58} .glyph {font-family:Nebulith;font-size:15pt;color:#577488}
    table {width:100%;border-collapse:collapse;table-layout:fixed;font-size:8pt} thead {display:table-header-group}
    th {background:#e8f0f4;text-align:left;color:#31536a} th,td {padding:5pt 6pt;border-bottom:1px solid #d9e2e7;overflow-wrap:anywhere;vertical-align:top}
    .entry {break-inside:avoid;padding:5pt 0;border-bottom:1px solid #d9e2e7} h3 {break-after:avoid} tr {break-inside:avoid} .root {font-family:Georgia,serif;color:#193b54} .muted {color:#627a89;font-size:8pt}
    '''
    css = BOOK_CSS + "@font-face{font-family:BookMincho;src:url(yumin.ttf);}"
    css += "@font-face{font-family:Nebulith;src:url(data:font/truetype;base64," + font + ") format('truetype');}"
    out = ['<!doctype html><html lang="ja"><meta charset="utf-8"><title>ヴァルネス遺聞 — 灰環の灯を継ぐ者たち</title><style>'+css+'</style><body>']
    out.append('<section class="cover"><p class="eyebrow">VALNES / THE ASHEN CIRCLE</p><p class="seal">◇</p><h1>ヴァルネス遺聞</h1><p class="subtitle">灰環の灯を継ぐ者たち</p><p class="glyph">celen vyr falun</p><p>原本巻・航海別巻・観測別巻・生活別巻</p><p class="muted">物語用例の出典原本 / 2026年 改訂</p></section>')
    out.append('<h2>原本について</h2><p>本書を、ヴァルネスの物語と各語の物語用例を引用するための編集原本とする。日本語の物語へNebulithの語を織り込み、各節へ変わらない出典番号を付した。語の歴史的な初出や語源を証明するものではない。</p><p>以下の物語篇は日本語の文学作品であり、Nebulith全文の対訳ではない。拡張語の掲載によって、辞書の審査状態が変更されることもない。既存の語義を保ち、確認済みのNRS文は後半の用例篇へ分けて残した。</p>')
    out.append('<section class="section"><h2>目次</h2>'+''.join('<p class="toc-item">'+e(w['subtitle'])+'<br><b>'+e(w['title'])+'</b></p>' for w in book['works'])+'<p class="toc-item">資料篇　暮らしの語彙500 / 正本の用例 / 語彙索引</p></section>')
    out.append(story_html(book))
    out.append('<section class="section"><h2>資料篇・改訂の記録</h2>')
    out.append('<h2>この版について</h2><p>旧版の自動生成詩節は、文法・対訳を確認した例文としては利用できないため、この版から除いた。文学的な設定と語彙の正当性は別に扱う。</p><p>創発候補1,020件の自動承認を取り消し、再審査待ちとして隔離した。新語の本番昇格は行っていない。日常500語は既存正本から再編集した学習索引であり、500件の新造語を意味しない。</p><p>既存辞書の語を物語用例と索引へ収録する。追加拡張語は今回の審査で一括承認しておらず、掲載は文法や語源の承認を意味しない。</p>')
    out.append(f'<div class="note">正本語幹 {len(canon)}語 / 学習索引 500語 / 用例 {len(corpus["units"])}件。用例には既存のAIによる言語審査記録があり、今回その参照・依存データ・構文を照合した。人間による独立審査を代替するものではない。</div>')
    out.append('</section><section class="section"><h2>暮らしの語彙500</h2><p>動作、食事、身の回り品、住まい、性質、感情、身体、気象、共同体、仕事。既存の語義を変えずにまとめた分野別索引。</p>')
    md = [story_markdown(book), '# 資料篇 — 語彙と用例', '', '2026-10-16 改訂。未検証の自動生成詩節を除き、既存語の学習索引と参照を確認した例文を収録。新造語の昇格なし。', '', '## 暮らしの語彙500', '']
    current = None
    loci = {}
    for row in learning['entries']:
        if row['category'] != current:
            if current is not None:
                out.append('</tbody></table>')
            current = row['category']
            out.append('<h3>'+e(current)+'</h3><table><thead><tr><th style="width:18%">語</th><th style="width:10%">品詞</th><th style="width:40%">日本語</th><th>英語</th></tr></thead><tbody>')
            md += ['### '+current, '']
        out.append(f'<tr><td class="root">{e(row["nrs"])}</td><td>{e(row["pos"])}</td><td>{e(row["meaningJa"])}</td><td>{e(row["meaningEn"])}</td></tr>')
        md.append(f'- **{row["nrs"]}**（{row["pos"]}）：{row["meaningJa"]} / {row["meaningEn"]}')
        loci[row['nrs']] = '暮らしの語彙500 / ' + row['category']
    out.append('</tbody></table></section><section class="section"><h2>正本の用例</h2>')
    md += ['', '## 正本の用例', '']
    for unit in corpus['units']:
        out.append(f'<article class="example"><h3>{e(unit["title"])}</h3><p class="glyph">{e(unit["nrs"])}</p><p class="nrs">{e(unit["nrs"])}</p><p>{e(unit["translationJa"])}</p></article>')
        md += ['### '+unit['title'], unit['nrs'], '', unit['translationJa'], '']
    out.append('</section><section class="section"><h2>語彙索引</h2><p>既存辞書の語幹・拡張語・文法項目。語義と品詞は既存辞書の定義を参照する。語の掲載は未定義の派生形や造語規則の承認を意味しない。</p><table><thead><tr><th style="width:18%">語</th><th style="width:10%">品詞</th><th style="width:40%">日本語</th><th>英語</th></tr></thead><tbody>')
    for root, row in sorted(words.items()):
        out.append(f'<tr><td class="root">{e(root)}</td><td>{e(row["pos"])}</td><td>{e(row["meaningJa"])}</td><td>{e(row["meaningEn"])}</td></tr>')
        citation=next(r for r in book['entries'] if r['root']==root)
        work=next(w for w in book['works'] if w['id']==citation['work'])
        loci[root]='『'+work['title']+'』第'+str(citation['chapter'])+'章 '+citation['id']
    out.append('</tbody></table></section></body></html>')
    html = ROOT / 'docs/Valnes_Ibun.html'
    pdf = html.with_suffix('.pdf')
    markup='\n'.join(out)
    import re
    markup=re.sub(r'<table.*?<tbody>', '', markup, flags=re.S)
    markup=markup.replace('</tbody></table>', '')
    markup=re.sub(r'<tr><td class="root">(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td></tr>', r'<div class="entry"><b class="root">\1</b>　<span class="muted">\2</span>　\3<div class="muted">\4</div></div>', markup)
    html.write_text(markup, encoding='utf-8')
    (ROOT / 'docs/NEBULITH_CANON_LORE_AND_EXPEDITIONS.md').write_text('\n'.join(md), encoding='utf-8')
    (ROOT / 'data/lexicon_canonical_loci.json').write_text(json.dumps(loci, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    render_pdf(html, pdf)
    # Stable old paths remain compatible with existing links.
    (ROOT/'docs/Codex_Astrolith_Canon_Scripture.html').write_bytes(html.read_bytes())
    (ROOT/'docs/Codex_Astrolith_Canon_Scripture.pdf').write_bytes(pdf.read_bytes())
    subsidiary=[]
    for work in book['works'][1:]:
        subhtml=ROOT/('docs/Valnes_'+work['id']+'.html')
        subpdf=subhtml.with_suffix('.pdf')
        subhtml.write_text('<!doctype html><html lang="ja"><meta charset="utf-8"><title>'+e(work['title'])+'</title><style>'+css+'</style><body><section class="cover"><p class="eyebrow">VALNES / '+work['id'].upper()+'</p><p class="seal">◇</p><h1>'+e(work['title'])+'</h1><p class="subtitle">'+e(work['subtitle'])+'</p><p class="muted">'+e(work['ending'])+'</p></section>'+story_html(book,work['id']).replace('</section>','<p class="muted">'+e(book['editorialNote'])+'</p></section>',1)+'</body></html>',encoding='utf-8')
        render_pdf(subhtml,subpdf)
        subsidiary += [subhtml,subpdf]
    manifest = {'canonicalRoots': len(canon), 'indexedWords': len(words), 'learningEntries': 500,
                'corpusUnits': len(corpus['units']), 'emergentPromoted': 0,
                'title':book['title'], 'literaryUsages':len(book['entries']), 'works':len(book['works']),
                'excluded': 'All 1020 held emergent candidates; existing extension usages are literary only',
                'sha256': {str(p.relative_to(ROOT)).replace('\\','/'): hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in [html, pdf, ROOT/'docs/Codex_Astrolith_Canon_Scripture.pdf', ROOT/'data/literary_sourcebook.json', ROOT/'data/everyday_vocabulary_review.json', ROOT/'data/canon_corpus.json', ROOT/'data/lexicon.json', ROOT/'data/translation_extensions.json', ROOT/'data/grammar_dictionary.json', ROOT/'data/corpus_rules.json', ROOT/'tools/literary_sourcebook.py', ROOT/'tools/literary_layout.py', ROOT/'tools/build_reviewed_codex.py', ROOT/'docs/NEBULITH_CANON_LORE_AND_EXPEDITIONS.md']+subsidiary}}
    from publication_manifest import build_manifest, CURRENT
    manifest = build_manifest(ROOT)
    (ROOT / CURRENT).write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in manifest.items() if k != 'sha256'}))


def render_pdf(html, pdf):
    """MuPDF paginates the same HTML without depending on a user's browser process."""
    import pymupdf as fitz
    markup = html.read_text(encoding='utf-8')
    # Story resolves physical font resources through its archive.
    markup = markup.replace('font-family:\'Yu Gothic\',\'Meiryo\',sans-serif', 'font-family:sans-serif')
    markup = markup.replace('font-family:\'Yu Mincho\',serif', 'font-family:serif')
    markup = __import__('re').sub(r"src:url\(data:font/truetype;base64,[^)]+\)", 'src:url(Nebulith-Regular.ttf)', markup)
    staging = pdf.with_name(pdf.stem + '.staging.pdf')
    archive=fitz.Archive(str(ROOT/'fonts'))
    archive.add('C:/Windows/Fonts')
    story = fitz.Story(html=markup, archive=archive)
    writer = fitz.DocumentWriter(str(staging))
    page = fitz.paper_rect('a5')
    frame = page + (40, 43, -40, -43)
    pages = 0
    try:
        more = True
        while more:
            device = writer.begin_page(page)
            more, filled = story.place(frame)
            story.draw(device)
            writer.end_page()
            pages += 1
            if pages > 800:
                raise ValueError('PDF layout did not converge')
    finally:
        writer.close()
    del writer
    with fitz.open(staging) as doc:
        if not len(doc) or not any(p.get_text().strip() for p in doc):
            raise ValueError('PDF content validation failed')
        for i,p in enumerate(doc):
            if i>0:
                p.insert_text((40,p.rect.height-23),'VALNES   /   '+str(i+1),fontname='Times-Roman',fontsize=7,color=(0.45,0.39,0.3))
        doc.set_metadata({'title':__import__('re').search(r'<title>(.*?)</title>',markup).group(1),'author':'Nebulith Project','subject':'Valnes literary source edition'})
        doc.saveIncr()
    staging.replace(pdf)
    print('PDF pages:', pages)


if __name__ == '__main__':
    build_codex()
