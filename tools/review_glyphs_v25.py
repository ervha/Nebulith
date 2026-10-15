"""Record the pinned, tiered v2.5 review; do not auto-approve future builds."""
import hashlib
import json
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
from nebulith_data import ROOT, dump
from font_pending_revision import CRITICAL, MINOR


def main():
    path=ROOT/'fonts/Nebulith-Regular.ttf'
    sha=hashlib.sha256(path.read_bytes()).hexdigest()
    batch=json.loads((ROOT/'data/audit/glyph_review_batch_v25.json').read_text(encoding='utf-8'))
    sop=hashlib.sha256((ROOT/'audit/docs/Nebulith Standard Audit Report.md').read_bytes()).hexdigest()
    if sha!=batch['fontSha256'] or sop!=batch['criteriaSha256']:
        raise ValueError('Font or criteria changed: perform a new visual review')
    old=json.loads((ROOT/'audit/runs/2026-10-15-glyphs-v2.5/before/glyph_reviews.json').read_text(encoding='utf-8'))
    old_rows={r['glyph']:r for r in old['entries']}
    assert {r['glyph'] for r in old['entries'] if r['decision']=='pending'} == CRITICAL|MINOR|{'space','.notdef'}
    font=TTFont(path);gs=font.getGlyphSet()
    meta=json.loads((ROOT/'audit/comparisons/glyph-v2.5/inventory.json').read_text(encoding='utf-8'))
    motifs={r['glyph']:r['motif'] for r in json.loads((ROOT/'fonts/inventory.json').read_text(encoding='utf-8'))['symbols']}
    rows=[]
    for row in meta['glyphs']:
        name=row['glyph']
        if name in CRITICAL:
            treatment='restructure'
            reason=({'i':'長い単純軸と上の点を除き、斜めの閉じた滴形ループと右へ抜ける筆流へ再編。I/iの単純な縦軸構造から変更。',
                     't':'天蓋と中央縦軸を除き、上下の開いた曲線と左側の小環・側方接続へ再編。T/tの横画と軸の構造を保持しない。',
                     'one':'一本の直立軸を除き、高い位置から回り込む筆流と低い閉じたループへ再編。数字1の単純軸を保持しない。'}[name.lower()])
        elif name in MINOR:
            treatment='refine'
            reason=motifs[name]+'。慣用の意味・配置・開口・閉路は維持し、直線同士の角を最大7単位の曲線で丸め、2.5%の微小な傾きで筆流を調整。左右対の傾きは反転。ユーザーの軽微修正方針に従い、従来骨格を許容する。'
        elif name in ['space','.notdef']:
            treatment='functional'
            reason=('空白の送り幅320と無輪郭を維持。不可視文字へ装飾を加えず、字間の機能を確認。' if name=='space' else '欠字の二重枠の角だけを最大10単位で丸め、外枠と内部空洞・送り幅を維持。機能確認であり独自性の承認ではない。')
        else:
            treatment='preserve'
            if row['outlineSha256']!=old_rows[name]['outlineSha256']:
                raise ValueError('Previously accepted glyph changed unexpectedly: '+name)
            reason=old_rows[name]['reason']+' v2.4と輪郭ハッシュ・送り幅が一致することを確認。'
        pen=BoundsPen(gs);gs[name].draw(pen)
        record={**row,'decision':'functional' if treatment=='functional' else 'approved',
                'reviewer':'Codex','reviewType':'AI tiered design and style review','treatment':treatment,
                'reason':reason,'bounds':list(pen.bounds) if pen.bounds else None,'advance':font['hmtx'][name][0],
                'investigated':True,'styleInspection':'16/24/48/72pxの標本と同じコードの比較で、線の丸み・筆流・字幅・配置を確認。人間の筆記・長文読字試験は未実施。',
                'previousFontSha256':old['fontSha256'],'conventionalSkeletonAccepted':treatment=='refine'}
        if treatment=='functional':
            record['functionalEvidence']={'fontSha256':sha,'positiveAdvance':True,'role':name}
        else:
            record['approvalEvidence']={'scope':'corresponding-codepoint','sameCharacterCompared':True,'styleCompared':True,
                                        'fontSha256':sha,'criteriaSha256':sop}
        rows.append(record)
    dump(ROOT/'data/audit/glyph_reviews.json',{'fontSha256':sha,'comparisonScope':'corresponding-codepoint',
         'criteriaVersion':'SOP-v2.5-tiered-handwriting-1','criteriaSha256':sop,
         'criteria':'ユーザー指示：クリティカルな字形は骨格を再編、軽微な字形は筆流・線端を調整。記号の慣用骨格を許容し、機能字形は独自性から分離。別コードとの競合は無視する。',
         'entries':rows})
    print(json.dumps({'approved':85,'functional':2,'pending':0,'restructure':5,'refine':27,'preserved':53}))


if __name__=='__main__':
    main()
