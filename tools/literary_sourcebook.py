"""Editable literary setting and stable, source-linked Japanese story usages.

The prose is a literary use of dictionary words, not an NRS translation corpus or
an etymological claim. Existing scenes survive new vocabulary being appended.
"""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TITLE = 'ヴァルネス遺聞'
SUBTITLE = '灰環の灯を継ぐ者たち'
WORKS = [
    {'id':'valnes','title':'灰環の灯を継ぐ者たち','subtitle':'ヴァルネス遺聞・原本巻',
     'voice':'写字生ユラ','place':'環状都市ヴァルネスの廃観測院',
     'chapters':[
         ('焼け残った名簿','都市が沈黙した朝、鐘は一度も鳴らなかった。写字生ユラが灰の下から拾ったのは、表紙も持ち主の名も失った一冊だった。頁の穴は火の形ではない。誰かが、必要な箇所だけを切り取っていた。','灯守セヴは、その帳面を燃やすなと言った。「欠けていることも、残っていることの一つだ」。ユラは余白に最初の記録を書いた。'),
         ('傾いた観測輪','観測院の上階では、巨大な輪が一つだけ北へ傾いていた。星を追う装置だと教わってきたのに、その影は地下へ延びていた。ユラは輪の寸法と欠けた頁の幅を比べ、同じ比を見つけた。','帳面は説明書ではなかった。遠く離れた人へ、場所を指し示す手紙だった。'),
         ('沈黙の議場','評議の席には、いまも十二人分の椅子が並んでいる。ユラは空席へ向かって、街に残された言葉を読んだ。かつて正しいとされた名にも、書き直しの跡があった。','セヴは訂正した行を消さず、細い線で囲んだ。「前に何を信じたかを失えば、また同じ間違いをする」。'),
         ('灰環の外側','夜、城壁の割れ目から細い灯が見えた。都市の外は何もない、と名簿には書かれている。ユラはその一行の横へ、小さな疑問符を置いた。','外へ出た二人は、瓦礫の向こうに他の人々の足跡を見つけた。街は世界の終わりではなかった。'),
         ('空白を運ぶ者','切り取られた頁は港で見つかった。避難した者たちは、失われた街の言葉を包み紙や舟板へ写して持ち出していた。一つの原本が失われても、言葉は誰かの暮らしに残る。','ユラは頁を元へ戻そうとして手を止めた。旅のあいだに書き足された文字まで、古い順番に閉じ込めることはできなかった。'),
         ('綴じ終えない本','帰還の日、セヴは灯を観測輪の中心へ置いた。輪はもう星を追わない。外の道を歩く人に、ここに帰れると知らせる灯となった。','ユラは最後の頁を白いまま残した。本を閉じるための空白ではなく、次の手が続きを書くための空白だった。')],
     'ending':'これをヴァルネスの遺聞とする。灰の下に残ったものだけでなく、灰の外で育ったものを、ともに綴じる。'},
    {'id':'saltwind','title':'塩風の余白','subtitle':'ヴァルネス遺聞・航海別巻','voice':'舟守トア','place':'灰環の外海と干潟の港',
     'chapters':[
         ('出帆のない朝','舟守トアは、出港を命じる鐘を待つのをやめた。桟橋の柱に小さな札を結び、戻る日を空欄にした。船に積んだのは物資よりも、誰に届けるかを書いた紙片だった。','ユラから渡された薄い帳面には、陸で使われる言葉が詰まっていた。海では同じものにも別の呼び方がある。トアは相違を削らず、二つを並べて記した。'),
         ('浅瀬の約束','最初の入り江で、船底が泥に触れた。地図には深い航路とある。少年のころに覚えた道が、いまの船を守るとは限らなかった。','トアは潮が戻るまで待った。古い地図を捨てず、変わった水際を別の色で描き足した。'),
         ('秤を持たない市','南の市では、品の重さより、それを作るあいだ誰が待ったかが語られた。値段だけを写していた帳面に、トアは初めて作り手の名を書いた。','取り引きのあと、見知らぬ女が食事を分けてくれた。その礼は、別の港で別の誰かへ返してよいという。'),
         ('夜を縫う帆','嵐の前に帆を降ろした者を、臆病だと笑う声があった。トアは笑わなかった。遠くの稲光が消えるまで、船員たちは一枚の帆を縫い続けた。','進まない夜にも、旅は続いていた。針を渡す手の動きが、舟を次の朝へ運んでいた。'),
         ('名のない帰路','霧のなかで、帰りの岬を見失った。トアは帳面を開く。測った距離だけでなく、店先の匂い、鳥の向く方、誰かの足音が、そこには残っていた。','数にできない記録もまた、帰る道を支えた。'),
         ('濡れた欄外','港に戻ると、空欄だった帰還日へ子供が今日の日付を書いた。トアは濡れた帳面を干し、余白に新しい呼び名を残した。','どの言葉が正しいかを一つに決めるのでなく、誰がどこで使ったかを書く。それが舟守の持ち帰った約束だった。')],
     'ending':'頁の端には、いまも塩の白い跡がある。その跡も取り去らず、次の航海へ渡す。'},
    {'id':'glasswell','title':'玻璃の深井戸','subtitle':'ヴァルネス遺聞・観測別巻','voice':'採集師ネリ','place':'玻璃井戸と地下の温室',
     'chapters':[
         ('光の降る井戸','採集師ネリが井戸へ降りたのは、水を求めたからではない。底から漏れる薄い光のなかで、地上から消えた植物が芽を出していた。','持ち帰った葉は、地上では光らなかった。ネリは失敗と書きかけて、その文字を観察へ置き換えた。'),
         ('名札のない芽','温室の鉢には、同じ名札が何枚も挿されていた。似た葉であっても、触れたときの硬さも、夜の開き方も違う。','ネリは一つの名に押し込めず、葉の裏側へ小さな印を付けた。違いを覚えることは、隔てることとは違った。'),
         ('薬師の留保','痛みを和らげたという葉を、薬師はすぐには配らなかった。誰に、どれだけ、いつ試したのかを尋ねた。物語の美しさと、確かめられたことは別だと言った。','ネリは答えられない欄を空白にした。知らないことを埋めない記録が、ここでは信頼を育てた。'),
         ('壁の呼吸','井戸の壁には細かな生き物が棲み、温室の根へ水を渡していた。葉だけを運べばよいと思っていたネリは、小さなつながりを見落としていた。','光は一つのものの力ではなかった。互いの働きが途切れないところに、光が生まれていた。'),
         ('割れた採集瓶','帰りの梯子で瓶が割れた。ネリは散った標本を拾い、無事だったものと、もう確かめられないものを分けた。','失われた標本の欄にも、採集した場所と割れた時刻を残した。失敗を消してしまえば、次に降りる者の足元まで暗くなる。'),
         ('地上の小さな井戸','庭に据えた浅い水鉢のそばで、一枚の葉が淡く光った。地下のものをそのまま移すのではなく、地上で支え合える形を探していたのだ。','ネリは新しい葉に名札を結んだ。その裏には、まだ分からないことが三つ書かれていた。')],
     'ending':'深さを競うために井戸は掘られない。帰ってきた者が地上を少し違って見るために、井戸は口を開けている。'},
    {'id':'lamptable','title':'灯守りの食卓','subtitle':'ヴァルネス遺聞・生活別巻','voice':'灯守セヴ','place':'城壁の共同炊事場と小さな工房',
     'chapters':[
         ('人数の増える鍋','共同炊事場の鍋は、いつも予定より一人分多く温められた。帰ってくる者がいる日にも、いない日にも、その決まりは変わらなかった。','セヴは物の名前を教えるとき、それを使った人の話も添えた。器は、置かれた場所だけでは覚えられない。'),
         ('継ぎ目のある椅子','工房へ運ばれた椅子は、どれも違う高さの脚を持っていた。職人は一度にそろえず、座る人を呼んだ。','直すことは、以前の形へ戻すことばかりではなかった。いま必要な形を、一緒に探すことだった。'),
         ('雨を干す窓','長雨の朝、窓際には衣服だけでなく、濡れた手紙や舟の帳面まで並んだ。誰かの旅と誰かの家事が、同じ紐に吊られていた。','紙を裏返すたび、セヴはまだ知らない土地の匂いを嗅いだ。'),
         ('足りない日の分け方','食材が足りない夕べ、誰も大きな声を出さなかった。一人が塩を持ち、一人が火を見た。食べ物の量は増えなくても、食卓を囲む時間は短くならなかった。','その晩の記録には、豊かという言葉の横に、分けたものを一つずつ書いた。'),
         ('言い直せる部屋','口論の翌日、セヴは片方の椅子だけを片付けなかった。戻って言い直せる場所まで失えば、残るのは最初の言葉だけになる。','窓を開け、湯を沸かし、返事を急がせない。そのための小さな動作にも、記しておく価値があった。'),
         ('最後ではない灯','ユラが帳面を綴じる夜、セヴは食卓へ新しい灯を置いた。原本ができたから暮らしが終わるわけではない。灯のそばでは、次の話がもう始まっていた。','セヴは余った椀をしまわなかった。誰かが遅れて帰る日のために。')],
     'ending':'灯を守るとは、燃え尽きさせないことだけではない。まだ名を知らない誰かの席を、暗くしないことである。'}]


def words():
    # Source fields match the actual Web dictionary, including merged senses.
    from studio_dictionary import dictionary_entries
    canon = json.loads((ROOT/'data/lexicon.json').read_text(encoding='utf-8'))['vocabulary']
    return dictionary_entries(canon)


def source_hash(row):
    fields = {k:row[k] for k in ['id','nrs','pos','meaningJa','meaningEn','category']}
    return hashlib.sha256(json.dumps(fields,ensure_ascii=False,sort_keys=True).encode()).hexdigest()


def work_for(row):
    category=row.get('category','')
    match=re.match(r'(\d+)\.',category)
    if match:
        n=int(match[1])
        if n in [5,6,10,16]:return 1
        if n in [4,7,8]:return 2
        if n in [11,12,13,15]:return 3
        return 0
    if any(k in category for k in ['身体','医療','植物','生態']):return 2
    if any(k in category for k in ['生活','衣飾','感情','日常']):return 3
    if any(k in category for k in ['地理','気象','時間','空間']):return 1
    return 0


def literary_usage(row, work):
    gloss=re.split(r'[、／/;；]',row['meaningJa'])[0].strip()
    term=f'{gloss}〈{row["nrs"]}〉'
    speaker=work['voice']
    n=row['id']
    pos=row['pos']
    if '動' in pos and '名' not in pos:
        choices=[f'{speaker}は、{term}ことを選んだ。迷いが消えたのではない。先に手を動かさなければ、朝が来ても何も変わらないと知っていた。',
                 f'「{term}」。{speaker}は作業の順を短く読み上げた。昨日できたことを、今日も確かめずに済ませてはならなかった。',
                 f'{speaker}は、{term}という仕事を一人で抱えなかった。隣へ道具を渡したとき、その動きは二人の記憶になった。',
                 f'{term}ことには、いつも小さなためらいが伴った。{speaker}はそのためらいも書き残した。次に同じ道を選ぶ人へ、勇ましい話だけを渡したくなかった。']
    elif any(p in pos for p in ['格','機能','接','助','相関','代名','接辞']):
        choices=[f'{speaker}は「{row["nrs"]}」の横に「{gloss}」と添えた。短い語を一つ落とすだけで、誰の言葉か、何と何が結ばれるのかが変わってしまう。',
                 f'読み違えた箇所は「{row["nrs"]}」だった。{speaker}は「{gloss}」という働きを確かめ、相手の返事を聞いてから行を写し直した。']
    elif '形' in pos:
        choices=[f'「{term}」。それが{speaker}の最初の書き付けだった。けれど、同じものを見た隣人は別の印象を語った。二つの記録は並べて残された。',
                 f'{speaker}は、目の前のものを「{term}」と書き留めた。たった一語で言い尽くしたつもりにはならず、見る角度と時刻も添えた。']
    elif '副' in pos:
        choices=[f'欄外の「{row["nrs"]}」には「{gloss}」とある。{speaker}はその一語を声に出し、同じ出来事でも語り方によって届くものが違うと気づいた。']
    else:
        choices=[f'{speaker}が最初に書き留めたのは、{term}のことだった。ありふれた名前ほど、失ってからでは取り戻しにくい。',
                 f'{term}をめぐる話は、人ごとに少しずつ違った。{speaker}は一つにまとめず、語った人の名を添えて残した。',
                 f'余白に{term}の名が加わった。{speaker}はその隣を一行あけた。まだ聞けていない話があると、分かるように。',
                 f'{speaker}は、{term}について古い記録と新しい記録を照らし合わせた。変わったものと、呼び方だけが変わったものを、急いで同じにしないためだった。',
                 f'{term}という言葉を、{speaker}は旅の相手から教わった。その日付を記したとき、帳面は初めて、持ち主一人のものではなくなった。',
                 f'失われた頁にも、{term}のことが書かれていたという。{speaker}は残った証言から行を起こし、確かでない箇所には線を引かなかった。']
    return choices[n%len(choices)]


def build_sourcebook():
    target=ROOT/'data/literary_sourcebook.json'
    old=json.loads(target.read_text(encoding='utf-8')) if target.exists() else {}
    existing={r['root']:r for r in old.get('entries',[])}
    rows=words()
    by_work={w['id']:[] for w in WORKS}
    for row in rows:by_work[WORKS[work_for(row)]['id']].append(row)
    entries=[]
    for work in WORKS:
        group=by_work[work['id']]
        # Chapter assignment is stored per entry: new words append; existing loci never renumber.
        for index,row in enumerate(group):
            prev=existing.get(row['nrs'])
            if prev:
                if prev['sourceHash']!=source_hash(row):
                    raise ValueError('Dictionary meaning changed; review its literary usage before rebuild: '+row['nrs'])
                prev=dict(prev)
                if row['nrs'] not in prev['quote']:
                    raise ValueError('Edited literary quote must retain its target word: '+row['nrs'])
                saved_work=next((w for w in old.get('works',[]) if w['id']==prev['work']),None)
                if saved_work:
                    prev['chapterTitle']=saved_work['chapters'][prev['chapter']-1]['title']
                entries.append(prev)
                continue
            chapter=(index*6//max(1,len(group)))+1
            if old:chapter=6
            locus=f'VL-{row["id"]:05d}'
            entries.append({'id':locus,'entryId':row['id'],'root':row['nrs'],'meaningJa':row['meaningJa'],
                'work':work['id'],'chapter':chapter,'chapterTitle':work['chapters'][chapter-1][0],
                'quote':literary_usage(row,work),'language':'ja-with-nebulith-term',
                'kind':'literary-usage','translationStatus':'not-an-NRS-translation',
                'sourceHash':source_hash(row),'dictionaryStatus':'canonical' if row['id']<=1008 else 'existing-extension-or-grammar',
                'anchor':locus.lower()})
    active={row['nrs'] for row in rows}
    retired=[r for r in old.get('entries',[]) if r['root'] not in active]+old.get('retiredEntries',[])
    result={'schemaVersion':1,'title':TITLE,'subtitle':SUBTITLE,'edition':'2026-10-16',
            'editorialNote':'本書は物語用例の編集原本。日本語の物語へNebulithの語を織り込む。歴史的語源やNRS全文の文法承認を意味しない。既存拡張語の審査状態は変更しない。',
            'properNameNote':'ヴァルネスは作品内の都市・書名の固有名。新しい語幹として登録しない。',
            'works':old.get('works') or [dict(w,chapters=[{'title':c[0],'opening':c[1],'continuation':c[2]} for c in w['chapters']]) for w in WORKS],
            'entries':entries,'retiredEntries':retired,'coverage':{'dictionaryEntries':len(rows),'coveredRoots':len(entries)}}
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return result


if __name__=='__main__':
    result=build_sourcebook()
    print(json.dumps(result['coverage']))
