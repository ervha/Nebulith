"""Book typography and the literary source edition shared with Web references."""
from html import escape as e


BOOK_CSS = '''
@page {size:A5;margin:18mm 16mm 18mm}
body {font-family:BookMincho,serif;color:#302b26;font-size:9.3pt;line-height:1.95;background:#ffffff}
h1,h2,h3 {font-family:BookMincho,serif;color:#493d32;font-weight:normal}
h1 {font-size:26pt;line-height:1.65;letter-spacing:3px} h2 {font-size:18pt;border-bottom:1px solid #a58b62;padding-bottom:12pt}
h3 {font-size:13pt;margin-top:24pt;break-after:avoid} p {margin:0 0 11pt}
.cover {height:135mm;padding:12mm 8mm;border:1px solid #a58b62;background:#f4eedf;page-break-after:always;text-align:center}
.eyebrow {font-family:Georgia,serif;letter-spacing:4px;color:#8e7653;font-size:8pt}
.cover .subtitle {font-size:12pt;line-height:2;margin:16pt 0 26pt} .cover .seal {font-size:28pt;color:#906849;margin:22pt 0}
.section,.work-opening {page-break-before:always} .work-opening {padding-top:20mm}
.work-kicker {color:#9a714c;letter-spacing:3px;font-size:8pt} .work-title {font-size:25pt;line-height:1.8;margin:22pt 0 18pt}
.opening {font-size:10pt;line-height:2.1} .scene {page-break-inside:avoid;break-inside:avoid;margin:12pt 0}
.scene-locus {font-family:Georgia,serif;color:#8c7d68;font-size:7pt;margin-bottom:3pt;letter-spacing:1px}
.scene p {text-indent:1em} .closing {margin-top:25pt;border-top:1px solid #aa9778;padding-top:16pt;font-size:10pt}
.root,.nrs {font-family:Georgia,serif;color:#6e4736} .nrs {font-size:11pt}
.glyph {font-family:Nebulith;font-size:15pt;color:#9a866a}
.entry {break-inside:avoid;padding:6pt 0;border-bottom:1px solid #e4dccd}
.muted {color:#817563;font-size:7.5pt} .note {background:#f3eee3;padding:12pt;border-left:2px solid #a58b62}
.example {break-inside:avoid;padding:12pt 0;border-bottom:1px solid #d9ceba}
.toc-item {padding:8pt 0;border-bottom:1px solid #e4dccd} a {color:#785839;text-decoration:none}
'''


def story_html(book, only_work=None):
    parts=[]
    works=book['works'] if not only_work else [w for w in book['works'] if w['id']==only_work]
    for work in works:
        parts.append(f'<section class="work-opening" id="work-{e(work["id"])}"><p class="work-kicker">{e(work["subtitle"])}</p><h2 class="work-title">{e(work["title"])}</h2><p>{e(work["place"])}</p><p class="muted">語り手　{e(work["voice"])}</p></section>')
        for i,chapter in enumerate(work['chapters'],1):
            parts.append(f'<section class="section"><p class="work-kicker">{e(work["title"])}</p><h3>第{i}章　{e(chapter["title"])}</h3><p class="opening">{e(chapter["opening"])}</p><p class="opening">{e(chapter["continuation"])}</p>')
            for row in book['entries']:
                if row['work']!=work['id'] or row['chapter']!=i:continue
                parts.append(f'<article class="scene" id="{e(row["anchor"])}"><div class="scene-locus">{e(row["id"])}</div><p>{e(row["quote"])}</p></article>')
            parts.append('</section>')
        parts.append(f'<p class="closing">{e(work["ending"])}</p>')
    return '\n'.join(parts)


def story_markdown(book):
    out=['# '+book['title']+' — '+book['subtitle'],'',book['editorialNote'],'']
    for work in book['works']:
        out+=['## '+work['title'],'',work['subtitle'],'']
        for i,chapter in enumerate(work['chapters'],1):
            out+=['### 第'+str(i)+'章 '+chapter['title'],'',chapter['opening'],'',chapter['continuation'],'']
            for row in book['entries']:
                if row['work']==work['id'] and row['chapter']==i:out += ['#### '+row['id'],'',row['quote'],'']
        out+=['',work['ending'],'']
    return '\n'.join(out)
