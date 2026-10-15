"""Add 25 explicitly scoped examples; new approvals require a separate pinned batch."""
import json,re
from nebulith_data import ROOT,dump,reference,corpus_markdown

EXAMPLES=[
 ('present','Falun el vyr.','星は輝く。','無標の現在・一般叙述。falunの主体をelで示す。'),
 ('past','Fe falun el vyr.','星は輝いた。','feはこの独立節の過去。'),
 ('future','Se falun el vyr.','星は輝くだろう。','seは未来であり願望の意味を加えない。'),
 ('progress','Di falun el vyr.','星は輝いている。','進行はdiで明示し、名詞複数の-inと混同しない。'),
 ('negative','Ne falun el vyr.','星は輝かない。','neによる通常否定。'),
 ('question','Falun el vyr ka?','星は輝くか。','文末kaの疑問。'),
 ('inceptive','Falunast el vyr.','星は輝き始める。','始動相-ast。'),
 ('repeated','Faluncor el vyr.','星は繰り返し輝く。','反復相-corで、連続的進行とは分ける。'),
 ('walk','Poran el mi to govan.','私は家へ歩く。','主体mi、向格to、目的地govan。'),
 ('walk-past','Fe poran el mi to govan.','私は家へ歩いた。','歩行の過去をfeで明示。'),
 ('walk-future','Se poran el mi to govan.','私は家へ歩くだろう。','歩行の未来をseで明示。'),
 ('walk-progress','Di poran el mi to govan.','私は家へ歩いている。','diによる進行とtoの目的地。'),
 ('walk-negative','Ne poran el mi to govan.','私は家へ歩かない。','歩くという述語の通常否定。'),
 ('eat','Neran el mi ia nyrat.','私は主食を食べる。','el主体とia食物を分ける。'),
 ('eat-place','Neran el mi ia nyrat uo nerar.','私は食堂で主食を食べる。','uoは場所であり、食物iaとは別の項。'),
 ('eat-repeated','Nerancor el mi ia nyrat.','私は普段、主食を食べる。','反復・習慣の-cor。'),
 ('observe','Vyrel el vyrelor ia vyr uo vyrelar.','天文学者は天文台で星を観測する。','主体・被観測対象・場所の3項を照合。'),
 ('observe-past','Fe vyrel el vyrelor ia vyr.','天文学者は星を観測した。','能動態の過去。'),
 ('passive','Revyrel el vyr de vyrelor.','星は天文学者によって観測される。','re-で対象をelへ昇格。動作主はde。'),
 ('passive-past','Fe revyrel el vyr de vyrelor.','星は天文学者によって観測された。','過去feと受動re-。iaを残さない。'),
 ('copula','Relen el mi ia vyrelor.','私は天文学者である。','relenの主語miと名詞補語vyrelor。'),
 ('conditional','Sen falun el vyr, poran el mi to govan.','星が輝けば、私は家へ歩く。','sen条件節と後続主節。単なる未来と混同しない。'),
 ('reason','Zen falun el vyr, vyrel el mi ia vyr.','星が輝くので、私は星を観測する。','zen理由節と能動の主節。'),
 ('time','Hav falun el vyr, vyrel el mi ia vyr.','星が輝くとき、私は星を観測する。','hav時間節。因果や願望を加えない。'),
 ('concession','Tor ne falun el vyr, poran el mi to govan.','星が輝かなくても、私は家へ歩く。','tor譲歩節とne否定、後続の歩行主節。')]


def main():
    p=ROOT/'data/canon_corpus.json';data=json.loads(p.read_text(encoding='utf-8'))
    if len(data['units'])==30:return
    if len(data['units'])!=5:raise ValueError('Unexpected corpus inventory')
    vocab=json.loads((ROOT/'data/lexicon.json').read_text(encoding='utf-8'))['vocabulary'];roots={r['nrs']:r for r in vocab}
    for label,nrs,ja,note in EXAMPLES:
        id_='usage-'+label
        data['units'].append({'id':id_,'title':'用例：'+label,'label':'NRS','nrs':nrs,'translationJa':ja,
           'tokens':[{'id':f'{id_}:t{i:02d}','surface':word,**reference(word,roots)} for i,word in enumerate(re.findall(r"[a-z']+",nrs.lower()),1)],
           'review':{'status':'pending','note':note}})
    data['version']='23.4';dump(p,data)
    print('Added 25 examples; semantic approval still pending.')


if __name__=='__main__':main()
