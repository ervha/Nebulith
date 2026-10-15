"""Record the dated corresponding-character and handwriting review, pinned to its font."""
import hashlib
import json
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
from nebulith_data import ROOT, dump

LETTERS = {
 'a':'偏心した非対称の閉環と左へ流れる二つの曲線。Aの頂点・両脚・横棒、aのボウルと右の直立軸を除去。新しい曲線と細い光芒は既存字形の筆流に合わせた。',
 'e':'二つの交差する公転曲線が主体。Eの縦軸と三横画、eの開いた横棒付きボウルを主骨格にしない。',
 'i':'長い直立軸と上の点がI/iを連想させる。台座と側翼はあるが、16〜24pxの文字列で主軸が目立つため再設計候補。',
 'o':'円環を横断する赤道バーが内部を分割する。O/oの単一の空洞から接続・閉路構造が変化している。丸みは全体の手書き調を保つ。別コードの文字との比較はしない。',
 'u':'閉じた菱形軌道と下降軸。U/uの開いた杯を除去済み。v2.3から輪郭を維持。角張りは周囲の曲線より強いため今後の柔らかさ調整候補。',
 'y':'対向弧の下に閉じた滴形ループがある。Y/yの二股と単なる下行軸の構造を維持せず、曲線主体で統一。',
 'l':'長い軸の下部に大きな閉環と右上へ抜ける曲線がある。Lの直角足・lの単純縦軸と異なり、閉路と右端の反転が主構造。',
 'r':'左の直立軸を使わず、公転弧と左下へ抜ける曲線を接続する。Rの軸・右上のボウル・斜脚、rの短い軸と肩にしない。',
 'm':'中心から左右へ垂れる対向した曲線翼と中央軸。Mの折れ線・mの並んだ山形ではない。',
 'n':'左下の閉じた小渦と右上へ伸びる斜めの曲線。Nの二軸と斜線・nの山形を排し、ループと上行流線を主体にする。',
 's':'連続するS字曲線を除去。上部の開いた筆流と下部の非対称な閉じた滴形ループへ変更し、S/sにない閉路を主骨格とした。三角形の試案を採用せず、周囲の曲線へ合わせた。',
 'z':'対向する二つの弧と中央の大きな共鳴環。Z/zの二横画と斜めの連結線ではなく、曲線と閉環が骨格。',
 'c':'水平の天蓋から下がる閉じた受容形と中心核。C/cの右向きの開口と単一弧を維持しない。',
 'j':'上下左右にずれた二つの閉環と接続橋。J/jの縦軸と下端の鉤を除去済み。v2.3の輪郭を維持。別コードとの偶然の類似は判定対象外。',
 'f':'中央軸から左右へ上行する対称な曲線翼。Fの片側二横画、fの上部フックと横棒を保持しない。',
 'v':'尖ったV/vの谷を丸い深底の放物線へ変更している。細い連続曲線と中央核を保ち、丸みだけを不適合理由にしない。',
 'h':'二本の傾いた腕が下端で接続する閉底の形。Hの中央横棒、hの片側の肩を形成しない。',
 'w':'三重の重なった曲線弧と中央核。W/wの折れ線による二つの谷ではなく、入れ子の弧を主骨格とする。',
 'p':'上部の水平軸から下がる閉じた滴形。P/pの片側縦軸と上部側方ボウルの配置を保持しない。',
 'b':'中央軸の左右に逆向きで上下の異なる曲線シェルを置く。Bの片側二ボウル、bの片側一ボウルと接続・配置が異なる。',
 't':'反った天蓋と中央縦軸はT/tの横画と軸を連想させる。基底の三叉を持つが小サイズでT型が目立つため再設計候補。',
 'd':'底部の三日月と中央の上行軸。Dの片側外周、dのボウルに接する片側軸と異なり、両側対称の開口と中央軸を構成する。',
 'k':'中央から上・左右下へ放射する三本の曲線。K/kの片側縦軸と右へ出る二本の斜線とは接続点・方向が異なる。',
 'g':'三方の曲線放射を大きな天球環が横断する。Gの開いた環と横棒、gの一段・二段ボウルと下行部の骨格を保持しない。'}
NUMBERS={
 'zero':'円環を縦軸が横断し左右の刻線が接続する。0の単一輪郭と空洞に対し、閉路内部と接続を変更。',
 'one':'直立した一本の軸が主体であり、環と点があっても1型を連想させる。小サイズでの識別と筆流を再検討する。',
 'two':'左右の対向する二つの公転弧。2の上部ボウルから下方へ斜走し横画に終わる連続構造がない。',
 'three':'中央環と三方向の滴形ループ。3の右側に並ぶ二つの開いたボウルではない。',
 'four':'四方へ伸びるダイヤ状の光芒と中央閉環。4の片側縦画・三角形・横棒の骨格ではない。',
 'five':'五芒の軌道枠と内部の閉路。5の上横画・左縦画・下側のボウルという折れと開口を維持しない。',
 'six':'左上の彗星環と右下へ並行して流れる二本の尾。6の下側にある一つの大きなボウルとは閉路配置と放射が異なる。',
 'seven':'上部天蓋と下方へ曲がる軌道。7の上横画から左下へ落ちる直線の連続とは方向と曲線構造が異なる。',
 'eight':'中央環の左右へ開く対向弧。8の上下に閉じた二つのループとは開口と閉路数が異なる。',
 'nine':'上で横並びの二つの閉環と下向きの二本の光芒。9の一つの上ボウルと一本の下降軸とは閉路数と接続が異なる。'}


def main():
    path=ROOT/'fonts/Nebulith-Regular.ttf'
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    batch=json.loads((ROOT/'data/audit/glyph_review_batch_v24.json').read_text(encoding='utf-8'))
    if digest != batch['fontSha256']:
        raise ValueError('Changed font requires a new visual review')
    font=TTFont(path);gs=font.getGlyphSet()
    metadata=json.loads((ROOT/'audit/comparisons/glyph-v2.4/inventory.json').read_text(encoding='utf-8'))
    records=[]
    symbol_motifs={r['glyph']:r['motif'] for r in json.loads((ROOT/'fonts/inventory.json').read_text(encoding='utf-8'))['symbols']}
    for row in metadata['glyphs']:
        name=row['glyph'];lower=name.lower()
        if len(name)==1 and lower in LETTERS:
            decision='pending' if lower in ['i','t'] else 'approved'
            reason=LETTERS[lower]
        elif name in NUMBERS:
            decision='pending' if name=='one' else 'approved'
            reason=NUMBERS[name]
        elif name in ['space','.notdef']:
            decision='pending';reason='空白または欠字の機能字形。文字割り当て・送り幅・輪郭の有無は技術検証するが、独自性の適合認定とは分離して扱う。'
        else:
            decision='pending';reason=symbol_motifs[name]+'。同じ記号の慣用配置・曲線・直線が残る。文字列の読みやすさと独自性の扱いを含む最終デザイン審査は未確定。一括改形・一括合格にはしない。'
        pen=BoundsPen(gs);gs[name].draw(pen)
        records.append({**row,'decision':decision,'reviewer':'Codex','reviewType':'AI corresponding-character and style review',
                        'reason':reason,'styleInspection':'曲線・閉路・主軸・送り幅を確認。16/24/48/72pxの文字列標本も併用。人間の手書き試験と長文読字試験は未実施。',
                        'bounds':list(pen.bounds) if pen.bounds else None,
                        'advance':font['hmtx'][name][0], 'investigated':True})
        if decision=='approved':
            records[-1]['approvalEvidence']={'scope':'corresponding-codepoint','sameCharacterCompared':True,
                                             'styleCompared':True,'fontSha256':digest}
    assert len(records)==87
    dump(ROOT/'data/audit/glyph_reviews.json',{'fontSha256':digest,'comparisonScope':'corresponding-codepoint',
         'criteriaVersion':'SOP-v2.4-corresponding-handwriting-1',
         'criteria':'同じコードの文字との比較のみ。別コードの競合は無視する。点だけの追加でなく閉路・開口・接続を評価し、丸み・筆流・線幅・字間の調和を確認。',
         'entries':records})
    print(json.dumps({'investigated':len(records),'approved':sum(r['decision']=='approved' for r in records),'pending':sum(r['decision']=='pending' for r in records)}))


if __name__=='__main__':
    main()
