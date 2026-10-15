/* Offline interpretation: no network, no invisible subject/mood insertion. */
(function (global) {
  'use strict';
  function japaneseForms(lemma,kind) {
    let stem,past,te,negative,polite;
    if(kind==='kuru'){stem='来';past='来た';te='来て';negative='来ない';polite='来';}
    else if(kind==='suru'){stem=lemma.slice(0,-2);past=stem+'した';te=stem+'して';negative=stem+'しない';polite=stem+'し';}
    else if(kind==='ichidan'){stem=lemma.slice(0,-1);past=stem+'た';te=stem+'て';negative=stem+'ない';polite=stem;}
    else {
      const endings={'う':['わ','い','った','って'],'く':['か','き','いた','いて'],'ぐ':['が','ぎ','いだ','いで'],'す':['さ','し','した','して'],'つ':['た','ち','った','って'],'ぬ':['な','に','んだ','んで'],'ぶ':['ば','び','んだ','んで'],'む':['ま','み','んだ','んで'],'る':['ら','り','った','って']};
      const table=endings[kind];if(!table || !lemma.endsWith(kind))throw Error('不正な動詞活用設定：'+lemma);
      stem=lemma.slice(0,-1);negative=stem+table[0]+'ない';polite=stem+table[1];past=stem+table[2];te=stem+table[3];
    }
    const rows=[
      [lemma,[]],[past,['fe']],[negative,['ne']],[negative.slice(0,-1)+'かった',['fe','ne']],
      [polite+'ます',[]],[polite+'ました',['fe']],[polite+'ません',['ne']],[polite+'ませんでした',['fe','ne']],
      [te+'いる',['di']],[te+'います',['di']],[te+'いた',['fe','di']],[te+'いました',['fe','di']],
      [te+'いない',['ne','di']],[te+'いません',['ne','di']],[te+'いなかった',['fe','ne','di']],[te+'いませんでした',['fe','ne','di']],
      [polite+'始める',[],'ast'],[polite+'始めた',['fe'],'ast'],[polite+'始めます',[],'ast'],
      [polite+'たい',[],'','希望'],[polite+'たいです',[],'','希望'],[polite+'たくない',[],'','希望の否定'],[polite+'たかった',[],'','過去の希望']
    ];
    return rows.map(([ending,prefixes,suffix='',feature=''])=>({ending,prefixes,suffix,feature}));
  }
  global.nebulithJapaneseForms=japaneseForms;
  global.createIncrementalTranslator = function (vocab, frames, aliases, pairs, extensions={}) {
    frames={...frames};
    for(const [id,frame] of Object.entries(extensions.frames||{})) {
      if(frames[id])throw Error('追加文型が正本文型と競合しています。');
      frames[id]=frame;
    }
    const byId = new Map(vocab.map(e => [e.id, e]));
    const defaultAliases = [
      // 話す系
      {ending:'語り合う',replacement:'話す',complete:true,chooseGroup:'話す'},
      {ending:'告げる',replacement:'話す',complete:true,chooseGroup:'話す'},
      {ending:'ささやく',replacement:'話す',complete:true,chooseGroup:'話す'},
      {ending:'話している',replacement:'話す',complete:true,chooseGroup:'話す'},
      {ending:'話した',replacement:'話す',complete:true,chooseGroup:'話す'},
      {ending:'話す',replacement:'話す',complete:true,chooseGroup:'話す'},
      {ending:'話して',replacement:'話す',complete:false,chooseGroup:'話す'},
      {ending:'言っている',replacement:'話す',complete:true,chooseGroup:'話す'},
      {ending:'言った',replacement:'話す',complete:true,chooseGroup:'話す'},
      {ending:'言う',replacement:'話す',complete:true,chooseGroup:'話す'},
      {ending:'言って',replacement:'話す',complete:false,chooseGroup:'話す'},
      // 行く系
      {ending:'行進する',replacement:'歩く',complete:true,chooseGroup:'行く'},
      {ending:'滑空する',replacement:'歩く',complete:true,chooseGroup:'行く'},
      {ending:'走る',replacement:'歩く',complete:true,chooseGroup:'行く'},
      {ending:'行っている',replacement:'歩く',complete:true,chooseGroup:'行く'},
      {ending:'行った',replacement:'歩く',complete:true,chooseGroup:'行く'},
      {ending:'行く',replacement:'歩く',complete:true,chooseGroup:'行く'},
      {ending:'行って',replacement:'歩く',complete:false,chooseGroup:'行く'},
      {ending:'進んでいる',replacement:'歩く',complete:true,chooseGroup:'行く'},
      {ending:'進んだ',replacement:'歩く',complete:true,chooseGroup:'行く'},
      {ending:'進む',replacement:'歩く',complete:true,chooseGroup:'行く'},
      // 思う系
      {ending:'思索する',replacement:'信じる',complete:true,chooseGroup:'思う'},
      {ending:'決断する',replacement:'信じる',complete:true,chooseGroup:'思う'},
      {ending:'尊ぶ',replacement:'信じる',complete:true,chooseGroup:'思う'},
      {ending:'思っている',replacement:'信じる',complete:true,chooseGroup:'思う'},
      {ending:'思った',replacement:'信じる',complete:true,chooseGroup:'思う'},
      {ending:'思う',replacement:'信じる',complete:true,chooseGroup:'思う'},
      {ending:'思って',replacement:'信じる',complete:false,chooseGroup:'思う'},
      {ending:'考えている',replacement:'信じる',complete:true,chooseGroup:'思う'},
      {ending:'考えた',replacement:'信じる',complete:true,chooseGroup:'思う'},
      {ending:'考える',replacement:'信じる',complete:true,chooseGroup:'思う'},
      {ending:'考えて',replacement:'信じる',complete:false,chooseGroup:'思う'},
      // 聞く系（意図・状況に応じた解釈グループ化）
      {ending:'聞き入れる',replacement:'聴く',complete:true,chooseGroup:'聞く'},
      {ending:'聞き入れた',replacement:'聴く',complete:true,chooseGroup:'聞く'},
      {ending:'聞き及ぶ',replacement:'聴く',complete:true,chooseGroup:'聞く'},
      {ending:'聞き及んだ',replacement:'聴く',complete:true,chooseGroup:'聞く'},
      {ending:'聞き知る',replacement:'聴く',complete:true,chooseGroup:'聞く'},
      {ending:'聞き知った',replacement:'聴く',complete:true,chooseGroup:'聞く'},
      {ending:'聞こえている',replacement:'聴く',complete:true,chooseGroup:'聞く'},
      {ending:'聞こえた',replacement:'聴く',complete:true,chooseGroup:'聞く'},
      {ending:'聞こえる',replacement:'聴く',complete:true,chooseGroup:'聞く'},
      {ending:'質問している',replacement:'聴く',complete:true,chooseGroup:'聞く'},
      {ending:'質問した',replacement:'聴く',complete:true,chooseGroup:'聞く'},
      {ending:'質問する',replacement:'聴く',complete:true,chooseGroup:'聞く'},
      {ending:'尋ねている',replacement:'聴く',complete:true,chooseGroup:'聞く'},
      {ending:'尋ねた',replacement:'聴く',complete:true,chooseGroup:'聞く'},
      {ending:'尋ねる',replacement:'聴く',complete:true,chooseGroup:'聞く'},
      {ending:'尋ねて',replacement:'聴く',complete:false,chooseGroup:'聞く'},
      {ending:'耳を澄ます',replacement:'聴く',complete:true,chooseGroup:'聞く'},
      {ending:'耳を澄ませる',replacement:'聴く',complete:true,chooseGroup:'聞く'},
      {ending:'耳を傾ける',replacement:'聴く',complete:true,chooseGroup:'聞く'},
      {ending:'聞いている',replacement:'聴く',complete:true,chooseGroup:'聞く'},
      {ending:'聞いた',replacement:'聴く',complete:true,chooseGroup:'聞く'},
      {ending:'聞く',replacement:'聴く',complete:true,chooseGroup:'聞く'},
      {ending:'聞いて',replacement:'聴く',complete:false,chooseGroup:'聞く'},
      // 作る系（意図・状況に応じた解釈グループ化）
      {ending:'組み立てている',replacement:'書く',complete:true,chooseGroup:'作る'},
      {ending:'組み立てた',replacement:'書く',complete:true,chooseGroup:'作る'},
      {ending:'組み立てる',replacement:'書く',complete:true,chooseGroup:'作る'},
      {ending:'生み出す',replacement:'書く',complete:true,chooseGroup:'作る'},
      {ending:'創出する',replacement:'書く',complete:true,chooseGroup:'作る'},
      {ending:'作っている',replacement:'書く',complete:true,chooseGroup:'作る'},
      {ending:'作った',replacement:'書く',complete:true,chooseGroup:'作る'},
      {ending:'作る',replacement:'書く',complete:true,chooseGroup:'作る'},
      {ending:'作って',replacement:'書く',complete:false,chooseGroup:'作る'},
      {ending:'創る',replacement:'書く',complete:true,chooseGroup:'作る'},
      // 行く・動く系の細分化
      {ending:'急いでいる',replacement:'歩く',complete:true,chooseGroup:'行く'},
      {ending:'急いだ',replacement:'歩く',complete:true,chooseGroup:'行く'},
      {ending:'急ぐ',replacement:'歩く',complete:true,chooseGroup:'行く'},
      {ending:'急いで',replacement:'歩く',complete:false,chooseGroup:'行く'},
      {ending:'帰っている',replacement:'歩く',complete:true,chooseGroup:'行く'},
      {ending:'帰った',replacement:'歩く',complete:true,chooseGroup:'行く'},
      {ending:'帰る',replacement:'歩く',complete:true,chooseGroup:'行く'},
      {ending:'戻っている',replacement:'歩く',complete:true,chooseGroup:'行く'},
      {ending:'戻った',replacement:'歩く',complete:true,chooseGroup:'行く'},
      {ending:'戻る',replacement:'歩く',complete:true,chooseGroup:'行く'},
      {ending:'旅立っている',replacement:'歩く',complete:true,chooseGroup:'行く'},
      {ending:'旅立った',replacement:'歩く',complete:true,chooseGroup:'行く'},
      {ending:'旅立つ',replacement:'歩く',complete:true,chooseGroup:'行く'},
      {ending:'立ち止まる',replacement:'歩く',complete:true,chooseGroup:'行く'},
      {ending:'留まっている',replacement:'歩く',complete:true,chooseGroup:'行く'},
      {ending:'留まった',replacement:'歩く',complete:true,chooseGroup:'行く'},
      {ending:'留まる',replacement:'歩く',complete:true,chooseGroup:'行く'},
      // 感じる・触れる系
      {ending:'感じている',replacement:'愛する',complete:true,chooseGroup:'感じる'},
      {ending:'感じた',replacement:'愛する',complete:true,chooseGroup:'感じる'},
      {ending:'感じる',replacement:'愛する',complete:true,chooseGroup:'感じる'},
      {ending:'触っている',replacement:'愛する',complete:true,chooseGroup:'感じる'},
      {ending:'触った',replacement:'愛する',complete:true,chooseGroup:'感じる'},
      {ending:'触る',replacement:'愛する',complete:true,chooseGroup:'感じる'},
      {ending:'握っている',replacement:'愛する',complete:true,chooseGroup:'感じる'},
      {ending:'握った',replacement:'愛する',complete:true,chooseGroup:'感じる'},
      {ending:'握る',replacement:'愛する',complete:true,chooseGroup:'感じる'},
      {ending:'撫でている',replacement:'愛する',complete:true,chooseGroup:'感じる'},
      {ending:'撫でた',replacement:'愛する',complete:true,chooseGroup:'感じる'},
      {ending:'撫でる',replacement:'愛する',complete:true,chooseGroup:'感じる'},
      // 取引・売買系
      {ending:'買っている',replacement:'取引する',complete:true},
      {ending:'買った',replacement:'取引する',complete:true},
      {ending:'買う',replacement:'取引する',complete:true},
      {ending:'売っている',replacement:'取引する',complete:true},
      {ending:'売った',replacement:'取引する',complete:true},
      {ending:'売る',replacement:'取引する',complete:true},
      // 好む系
      {ending:'好んでいる',replacement:'愛する',complete:true},
      {ending:'好んだ',replacement:'愛する',complete:true},
      {ending:'好む',replacement:'愛する',complete:true},
      {ending:'愛好する',replacement:'愛する',complete:true}
    ];
    aliases = [...(aliases||[]).map(a => a.chooseVerb ? {...a, chooseGroup: '見る'} : a), ...defaultAliases];
    const productive=extensions.productive||{};
    for(const verb of productive.verbs||[])if(!frames[verb.id])frames[verb.id]=verb.frame;
    const placeRoots=new Set(['govan','vyrelar','nerar','celvan',...(productive.placeIds||[]).map(id=>byId.get(id)?.r).filter(Boolean)]);
    const argSources=new WeakMap();
    const gloss = e => e.m.split(/[、／]/).map(x => x.trim()).filter(Boolean);
    const pronouns = {'私':'mi','あなた':'ti','彼':'ri','彼女':'ri','彼／彼女':'ri',...(productive.pronounAliases||{})};
    const index = new Map();
    for (const e of vocab) for (const g of gloss(e)) { if (!index.has(g)) index.set(g, []); index.get(g).push(e); }
    const adjectives = vocab.filter(e => e.p.includes('形')).flatMap(e => gloss(e).map(g => [g,e]));
    const key = s => s.trim().replace(/\s+/g,'').replace(/？/g,'?').replace(/[。.]$/,'');
    function phrase(text, adj = false, depth = 0) {
      if (!text || depth > 2) throw Error('名詞句が未完成、または修飾が複雑です。');
      if (pronouns[text]) return pronouns[text];
      const found = [...new Map([...(index.get(text)||[]), ...(adj ? (index.get(text+'な')||[]) : [])].filter(e=>e.p.includes('名') || adj && e.p.includes('形')).map(e=>[e.id,e])).values()];
      if (found.length === 1) return found[0].r;
      if (found.length > 1) throw Error(`「${text}」の語義候補が複数：`+found.slice(0,5).map(e=>e.r).join(' / '));
      if(text.endsWith('こと')) {
        const v = text.slice(0, -2);
        const verbEntry = vocab.find(e => e.p.includes('動') && gloss(e).includes(v));
        if(verbEntry) return verbEntry.r;
      }
      if ((text.match(/の/g)||[]).length === 1) { const [a,b] = text.split('の'); return phrase(b,adj,depth+1)+' en '+phrase(a,false,depth+1); }
      if(!text.includes('の') && (text.match(/と/g)||[]).length===1) {
        const [a,b]=text.split('と');return phrase(a,false,depth+1)+' ul '+phrase(b,false,depth+1);
      }
      const results = new Set();
      for (const [g,e] of adjectives) if(g.length>=2 && text.startsWith(g) && text.length>g.length) {
        try { results.add(phrase(text.slice(g.length),false,depth+1)+' '+e.r); } catch (_) {}
      }
      if(results.size===1) return [...results][0];
      throw Error(`「${text}」の名詞・修飾語を確定できません。`);
    }
    const particles = [['によって','de'],['を使って','de'],['とともに','ku'],['と共に','ku'],['と一緒に','ku'],['から','va'],['が','el'],['は','el'],['を','ia'],['へ','to'],['に','to'],['で','uo'],['と','ku']];
    function argsOf(text,frame=null) {
      const found=[]; let budget=500;
      function parse(rest,args,sources={}) {
        if(!rest) {found.push({args,sources});return;}
        if(found.length>10)return;
        for(const [p,defaultCase] of particles) {
          let at=rest.indexOf(p);
          while(at>=0) {
            if(--budget<0) throw Error('解釈候補が多すぎます。');
            try {
              const value=phrase(rest.slice(0,at));
              let c=defaultCase;
              if(p==='に' && frame)c=['al','to','uo'].find(k=>frame.allowed.includes(k))||'to';
              if(p==='で' && !placeRoots.has(value.split(' ')[0]) && frame?.allowed.includes('de'))c='de';
              if(Object.hasOwn(args,c))throw Error('格の重複');
              if(c==='uo' && !placeRoots.has(value.split(' ')[0]))throw Error('場所と道具を区別できません。');
              parse(rest.slice(at+p.length),{...args,[c]:value},{...sources,[c]:{text:rest.slice(0,at),particle:p}});
            } catch (_) {}
            at=rest.indexOf(p,at+p.length);
          }
        }
      }
      parse(text,{});
      const unique = new Map(found.map(a=>[JSON.stringify(Object.entries(a.args).sort()),a]));
      const coordinated=[...unique.values()].filter(r=>r.args.el?.includes(' ul ') && /と.+[はが]/.test(text));
      if(unique.size!==1 && coordinated.length!==1) throw Error('語句や助詞の解釈が未確定です。');
      const result=coordinated.length===1?coordinated[0]:[...unique.values()][0];argSources.set(result.args,result.sources);return result.args;
    }
    const forms=[];
    function add(id, words, prefixes=[], suffix='', passive=false) { for(const ending of words) forms.push({id,ending,prefixes,suffix,passive}); }
    for(const [id,base,past,progress,neg,negPast,polite,politePast,politeNeg] of [
      [16,'輝く','輝いた','輝いている','輝かない','輝かなかった','輝きます','輝きました','輝きません'],
      [16,'光る','光った','光っている','光らない','光らなかった','光ります','光りました','光りません'],
      [902,'歩く','歩いた','歩いている','歩かない','歩かなかった','歩きます','歩きました','歩きません'],
      [953,'観測する','観測した','観測している','観測しない','観測しなかった','観測します','観測しました','観測しません'],
      [972,'食べる','食べた','食べている','食べない','食べなかった','食べます','食べました','食べません']]) {
      add(id,[base,polite]);add(id,[past,politePast],['fe']);add(id,[progress],['di']);add(id,[neg,politeNeg],['ne']);
      add(id,[negPast],['fe','ne']);add(id,[base+'だろう'],['se']);
    }
    add(906,['である','です','だ']);add(906,['だった','でした','であった'],['fe']);add(906,['ではない'],['ne']);add(906,['ではなかった'],['fe','ne']);add(906,['でしょう','であろう'],['se']);
    add(953,['観測される'],[],'',true);add(953,['観測された'],['fe'],'',true);add(953,['観測されない'],['ne'],'',true);
    add(16,['輝き始める'],[],'ast');add(902,['歩き始める'],[],'ast');add(972,['食べ始める'],[],'ast');
    for(const [id,s] of [[16,'輝く'],[902,'歩く'],[953,'観測する'],[972,'食べる']]) add(id,['繰り返し'+s],[],'cor');
    for(const f of extensions.forms||[])forms.push({...f,suffix:'',passive:false,extension:true});
    for(const verb of productive.verbs||[])for(const f of japaneseForms(verb.lemma,verb.conjugation))forms.push({...f,id:verb.id,passive:false,extension:true});
    for(const e of vocab.filter(e=>e.p.includes('形')))for(const g of gloss(e)) {
      if(!g.endsWith('い') && !g.endsWith('な'))continue;
      const base=g.endsWith('な')?g.slice(0,-1):g;
      const variants=g.endsWith('な')?[[base,[]]]:[[base,[]],[base.slice(0,-1)+'かった',['fe']],[base.slice(0,-1)+'くない',['ne']],[base.slice(0,-1)+'くなかった',['fe','ne']],[base+'です',[]],[base.slice(0,-1)+'かったです',['fe']]];
      for(const [ending,prefixes] of variants)forms.push({id:906,ending,prefixes,suffix:'',passive:false,adjective:e.id,adjectiveSource:base,bareAdjective:true,extension:true});
    }
    const seenForms=new Set();
    const uniqueForms=forms.filter(f=>{const signature=JSON.stringify([f.id,f.ending,f.prefixes,f.suffix,f.adjective||0,f.feature||'']);if(seenForms.has(signature))return false;seenForms.add(signature);return true;});
    forms.splice(0,forms.length,...uniqueForms);
    forms.sort((a,b)=>b.ending.length-a.ending.length);

    const verbChoiceMap = {
      '見る': [
        {label: '観測する', id: 953},
        {label: '仰ぎ見る', id: 841},
        {label: '見上げる', id: 841},
        {label: '展望する', id: 30007, targetIa: 'sehvan'},
        {label: '予見する', id: 30008, targetIa: 'sehvan'}
      ],
      '話す': [
        {label: '話す', id: 860},
        {label: '語り合う', id: 840},
        {label: '告げる', id: 858},
        {label: 'ささやく', id: 861},
        {label: '叫ぶ', id: 30047},
        {label: '教える', id: 30021},
        {label: '問う', id: 753}
      ],
      '聞く': [
        {label: '聴く（耳を澄ます・傾聴）', id: 866},
        {label: '聞こえる（自然に耳に入る）', id: 30035},
        {label: '尋ねる（質問する・問う）', id: 30036},
        {label: '聞き知る（噂や情報を耳にする）', id: 30037},
        {label: '聞き入れる（言いつけに従う）', id: 30038}
      ],
      '行く': [
        {label: '歩く', id: 902},
        {label: '走る', id: 879},
        {label: '急ぐ', id: 30041},
        {label: '帰る・戻る', id: 30042},
        {label: '旅立つ・出発する', id: 30044},
        {label: '留まる・立ち止まる', id: 30043},
        {label: '行進する', id: 903},
        {label: '滑空する', id: 946},
        {label: '跳ぶ', id: 947},
        {label: '飛ぶ', id: 945},
        {label: '迂回する', id: 888},
        {label: '航路変更する', id: 36}
      ],
      '思う': [
        {label: '信じる', id: 705},
        {label: '理解する', id: 30010},
        {label: '思索する', id: 721},
        {label: '決断する', id: 726},
        {label: '幻視する', id: 743},
        {label: '尊ぶ', id: 732},
        {label: '思い出す', id: 30006},
        {label: '覚える', id: 30011}
      ],
      '作る': [
        {label: '創る・書く（文章・工作）', id: 875},
        {label: '建てる（家・落成上棟）', id: 599},
        {label: '組み立てる（構成・結合）', id: 30039},
        {label: '創出する（根源から生み出す）', id: 30040},
        {label: '築く（城壁・要塞化）', id: 609},
        {label: '鍛造する（打刻精錬）', id: 542},
        {label: '鋳造する（鋳型成型）', id: 548}
      ],
      '感じる': [
        {label: '感じる（心身で知覚）', id: 30045},
        {label: '触れる（手渡し・軽く接触）', id: 913},
        {label: '撫でる（優しくいたわる）', id: 914},
        {label: '握る（しっかりと掴む）', id: 30046}
      ]
    };

    const caseOrder=['el','ia','al','uo','to','va','de','ku'];
    const extensionNotes=f=>f.extension?[(byId.get(f.id).c.includes('未監査')?'追加語彙案':'追加文型案')+'（未監査）を使用']:[];
    const provisionalRoots=new Set((extensions.entries||[]).map(e=>e.nrs));
    const lexicalNotes=target=>target.toLowerCase().split(/\W+/).some(w=>provisionalRoots.has(w))?['追加語彙案（未監査）を使用']:[];
    const roles={el:'主体',ia:'対象・補語',al:'受け手',uo:'場所',to:'目的地',va:'起点',de:'動作主・道具',ku:'共同者'};
    function phraseRows(source,target,role) {
      if(!source.includes('の') && source.includes('と') && target.includes(' ul ')) {
        const [a,b]=source.split('と'),[left,right]=target.split(' ul ');
        return [...phraseRows(a,left,role),{src:'と',dst:'ul',role:'並列'},...phraseRows(b,right,role)];
      }
      if((source.match(/の/g)||[]).length===1 && target.includes(' en ')) {
        const [owner,thing]=source.split('の'),[head,tail]=target.split(' en ');
        return [...phraseRows(owner,tail,'所有者'),{src:'の',dst:'en',role:'属格'},...phraseRows(thing,head,role)];
      }
      for(const [g,e] of adjectives)if(g.length>=2 && source.startsWith(g) && source.length>g.length && target.endsWith(' '+e.r)) {
        return [{src:g,dst:e.r,role:'修飾語'},...phraseRows(source.slice(g.length),target.slice(0,-e.r.length-1),role)];
      }
      return [{src:source,dst:target,role}];
    }
    function argumentRows(args) {
      const sources=argSources.get(args)||{};
      return caseOrder.filter(c=>args[c]).flatMap(c=>{
        const s=sources[c];
        if(!s)return [{src:'原文から役割を推定',dst:c+' '+args[c],role:roles[c]+'（推定）'}];
        return [...phraseRows(s.text,args[c],roles[c]).map(r=>({...r,role:r.role+(s.inferred?'（補完）':'' )})),
          {src:s.particle||'文法上の補完',dst:c,role:'格標識'+(s.inferred?'（補完）':'')}];
      });
    }
    function outputAlignment(f,args,question) {
      const verb=[...f.prefixes,(f.passive?'re':'')+byId.get(f.id).r+f.suffix].join(' ');
      return [...argumentRows(args),{src:f.bareAdjective?'断定の文法（日本語では省略）':f.ending,dst:verb,role:'述語'+(f.prefixes.includes('ne')?'・否定':'')+(f.prefixes.includes('fe')?'・過去':'')},
        ...(question?[{src:'か／疑問符',dst:'ka',role:'疑問'}]:[])];
    }
    function registeredRows(source,target,pair) {
      const rows=[];
      for(const row of pair?.alignment||[]) {
        let src=source.includes(row.src)?row.src:'';
        if(!src) {
          const stem=row.src.replace(/(?:です|だ)$/,'');
          const at=source.indexOf(stem);
          if(stem.length>=2 && at>=0)src=stem+(source.slice(at+stem.length).match(/^(?:でした|だった|です|だ)/)?.[0]||'');
        }
        if(src && target.toLowerCase().includes(row.dst.toLowerCase()))rows.push({...row,src});
      }
      const accounted=rows.flatMap(r=>r.dst.toLowerCase().split(/\s+/));
      const missing=target.replace(/[.?!]/g,'').split(/\s+/).filter(w=>!accounted.includes(w.toLowerCase()));
      if(missing.length)rows.push({src:source,dst:missing.join(' '),role:'登録対訳の残り（文単位・語別未解析）'});
      return rows;
    }
    function parsedArgs(head,f) {
      if(f.adjective) {
        const args=argsOf(head,frames[f.id]);args.ia=byId.get(f.adjective).r;
        argSources.set(args,{...(argSources.get(args)||{}),ia:{text:f.ending,particle:'性質の補語'}});return args;
      }
      if(f.emotion) {
        const match=head.match(/^(.+?)は(.+?)が$/);
        if(match) {const args={el:phrase(match[1]),ia:phrase(match[2])};argSources.set(args,{el:{text:match[1],particle:'は'},ia:{text:match[2],particle:'が'}});return args;}
        const omitted=head.match(/^(.+?)が$/);
        if(omitted) {const args={ia:phrase(omitted[1])};argSources.set(args,{ia:{text:omitted[1],particle:'が'}});return args;}
      }
      return argsOf(head,frames[f.id]);
    }
    function meaningOf(form,args,question,feature='') {
      const sources=argSources.get(args)||{};
      return {schemaVersion:1,kind:'clause',predicate:form?{entryId:form.id,root:byId.get(form.id).r,source:form.ending,prefixes:[...form.prefixes],suffix:form.suffix||'',passive:!!form.passive}:null,
        arguments:Object.fromEntries(Object.entries(args).map(([c,nrs])=>[c,{nrs,role:roles[c],source:sources[c]?.text||'',particle:sources[c]?.particle||'',inferred:!!sources[c]?.inferred}])),
        tense:form?.prefixes.includes('fe')?'past':form?.prefixes.includes('se')?'future':'unmarked',negative:!!form?.prefixes.includes('ne'),aspect:form?.prefixes.includes('di')?'progressive':form?.suffix==='ast'?'inceptive':form?.suffix==='cor'?'iterative':'unmarked',question:!!question,
        modalities:feature?[{kind:feature.includes('希望')?'desire':feature.includes('推量')?'uncertainty':feature.includes('可能')?'possibility':feature.includes('意図')?'intention':feature.includes('必要')?'necessity':'thought',sourceFeature:feature,negated:feature.includes('否定'),past:feature.includes('過去'),scope:'clause',realization:'not-defined'}]:[],
        alignment:form?outputAlignment(form,args,question):argumentRows(args)};
    }
    function realize(meaning) {
      if(!meaning.predicate)throw Error('動作が未指定です。');
      if(meaning.modalities.length)throw Error('ニュアンスの出力規則が未定義です。');
      const p=meaning.predicate,frame=frames[p.entryId];if(!frame)throw Error('動詞の項構造が未対応です。');
      const allowed=p.passive?frame.passiveAllowed||[]:frame.allowed;
      if(!frame.required.every(c=>meaning.arguments[c])||Object.keys(meaning.arguments).some(c=>!allowed.includes(c)))throw Error('主語・補語の不足、または動詞の項構造に合わない格があります。');
      const words=[...p.prefixes,(p.passive?'re':'')+p.root+p.suffix];
      for(const c of caseOrder)if(meaning.arguments[c])words.push(c,meaning.arguments[c].nrs);
      if(meaning.question)words.push('ka');const out=words.join(' ');
      return out[0].toUpperCase()+out.slice(1)+(meaning.question?'?':'.');
    }
    function full(text) {
      if(/^(.+?)と(.+?)の(.+?)$/.test(key(text)))return null;
      const exact = [...new Set(pairs.filter(p=>(p.ja_variants||[p.ja]).some(x=>key(x)===key(text))).map(p=>p.neb))];
      let body=key(text), question=body.endsWith('?');body=body.replace(/\?$/,'');
      if(body.endsWith('か')) {question=true;body=body.slice(0,-1);}
      const results=[];
      for(const f of forms) if(!f.feature && body.endsWith(f.ending)) try {
        const head=body.slice(0,-f.ending.length);let args;
        if(f.id===906 && !f.adjective) {
          const possible=[];for(let i=1;i<head.length;i++)if('はが'.includes(head[i]))try{possible.push({el:phrase(head.slice(0,i)),ia:phrase(head.slice(i+1),true)});}catch(_){}
          if(possible.length!==1)continue;args=possible[0];
          const i=[...head].findIndex((c,i)=>i>0 && 'はが'.includes(c) && (()=>{try{return phrase(head.slice(0,i))===args.el && phrase(head.slice(i+1),true)===args.ia;}catch(_){return false;}})());
          argSources.set(args,{el:{text:head.slice(0,i),particle:head[i]},ia:{text:head.slice(i+1),particle:'コピュラ補語'}});
        } else args=parsedArgs(head,f);
        const meaning=meaningOf(f,args,question);
        results.push({text:realize(meaning),meaning,alignment:meaning.alignment,extension:f.extension,extensionNotes:extensionNotes(f)});
      }catch(_){}
      const unique=[...new Map(results.map(r=>[r.text,r])).values()];
      if(exact.length===1) {
        const generated=unique.find(r=>r.text.toLowerCase()===exact[0].toLowerCase());
        const pair=pairs.find(p=>p.neb===exact[0] && (p.ja_variants||[p.ja]).some(x=>key(x)===key(text)));
        const alignment=generated?.alignment || registeredRows(text,exact[0],pair);
        return {text:exact[0],state:'complete',notes:['登録対訳との一致'],alignment,meaning:generated?.meaning||{schemaVersion:1,kind:'registered',source:text,target:exact[0],analysis:'word-analysis-incomplete'}};
      }
      if(unique.length===1)return {...unique[0],state:'complete',notes:['Nebulithの格・項構造を検証',...unique[0].extensionNotes,...lexicalNotes(unique[0].text)]};
      try {if(!question){const target=phrase(body);return {text:target,state:'phrase',notes:['語句として変換。完成文ではありません。',...lexicalNotes(target)],alignment:phraseRows(body,target,'語句')};}}catch(_){}
      return null;
    }
    function part(source,choices,depth=0) {
      const compound=source.match(/^(.+?)(なら|ので|から|だから|けれど|けれども|とき)(?:[、,]|\s+)(.+)$/);
      if(compound){
        if((source.match(/(?:なら|ので|けれど|とき)[、,]/g)||[]).length>1)return {source,text:'',state:'blocked',notes:['接続する節の範囲が複数あります。入れ子を推測せず、一節ずつ確認してください。']};
        if(depth>=2)return {source,text:'',state:'blocked',notes:['節の入れ子が深すぎます。一文を分けてください。']};
        const relation={なら:['sen','条件'],ので:['zen','理由'],から:['zen','理由'],だから:['zen','理由'],けれど:['tor','譲歩'],けれども:['tor','譲歩'],とき:['hav','時間']}[compound[2]];
        let firstClauseText = compound[1].trim();
        if(compound[2]==='だから' && !firstClauseText.endsWith('だ') && !firstClauseText.endsWith('である')) {
          firstClauseText += 'だ';
        }
        const clauses=[part(firstClauseText,{},depth+1),part(compound[3].trim(),{},depth+1)];
        const meaning={schemaVersion:1,kind:'compound',relation:relation[0],clauses:clauses.map(c=>c.meaning||{kind:'unresolved',source:c.source})};
        if(clauses.some(c=>!['complete','candidate'].includes(c.state)||c.meaning?.question))return {source,text:'',state:clauses.some(c=>c.state==='blocked')?'blocked':'draft',meaning,notes:[relation[1]+'節の未確定部分を保持。節ごとに主体・解釈を明示してください。',...clauses.flatMap(c=>c.notes)]};
        const bare=t=>t.replace(/[.?]+$/,'').replace(/^./,c=>c.toLowerCase());
        const text=relation[0][0].toUpperCase()+relation[0].slice(1)+' '+bare(clauses[0].text)+', '+bare(clauses[1].text)+(clauses[1].text.endsWith('?')?'?':'.');
        const allConfirmed = clauses.every(c => c.state === 'complete');
        return {source,text,state:allConfirmed?'complete':'candidate',candidate:text,meaning,alignment:[...clauses.flatMap((c,i)=>(c.alignment||[]).map(a=>({...a,role:(i?'主節':'従属節')+'・'+a.role}))),{src:compound[2],dst:relation[0],role:relation[1]+'接続'}],notes:['節ごとの意味を保持して生成。追加複文規則（未監査）。',...clauses.flatMap(c=>c.notes)]};
      }
      const ownership=key(source).match(/^(.+?)と(.+?)の(.+?)$/);
      if(ownership)try {
        const [,a,b,thing]=ownership,ar=phrase(a),br=phrase(b),tr=phrase(thing);
        const notes=['所有範囲を選択：「（AとB）のC」または「Aと（BのC）」。追加の並列・所有文型案です。'];
        if(!['shared','separate'].includes(choices.possession))return {source,text:'',state:'draft',notes,scopeAmbiguous:true};
        const shared=choices.possession==='shared';
        const target=shared?tr+' en '+ar+' ul '+br:ar+' ul '+tr+' en '+br;
        const alignment=[...phraseRows(a,ar,shared?'共有所有者':'並列項'),{src:'と',dst:'ul',role:'並列'},...phraseRows(b,br,'所有者'),{src:'の',dst:'en',role:'属格（範囲を選択）'},...phraseRows(thing,tr,'所有物')];
        return {source,text:target,state:choices.confirmed?'phrase':'candidate',candidate:choices.confirmed?'':target,notes:[...notes,shared?'共有所有を選択':'別々の並列項を選択',...lexicalNotes(target)],scopeAmbiguous:true,alignment};
      }catch(_){}
      const trailingCompound = key(source).match(/^(.+?)(なら|ので|から|だから|けれど|けれども|とき)$/);
      if(trailingCompound) {
        let subText = trailingCompound[1].trim();
        if(trailingCompound[2]==='だから' && !subText.endsWith('だ') && !subText.endsWith('である')) subText += 'だ';
        const relation = {なら:['sen','条件'],ので:['zen','理由'],から:['zen','理由'],だから:['zen','理由'],けれど:['tor','譲歩'],けれども:['tor','譲歩'],とき:['hav','時間']}[trailingCompound[2]];
        const subClause = part(subText, choices, depth + 1);
        const prefix = relation[0][0].toUpperCase() + relation[0].slice(1);
        const bare = t => t.replace(/[.?]+$/, '').replace(/^./, c => c.toLowerCase());
        const clauseText = subClause.text ? prefix + ' ' + bare(subClause.text) : prefix;
        const meaning = {schemaVersion: 1, kind: 'compound_incomplete', relation: relation[0], clause: subClause.meaning || {kind: 'unresolved', source: subText}};
        return {
          source,
          text: clauseText,
          state: 'draft',
          meaning,
          notes: [relation[1] + '節として解釈。続く主節の入力待ちです。', ...subClause.notes],
          alignment: [...(subClause.alignment || []).map(a => ({...a, role: '従属節・' + a.role})), {src: trailingCompound[2], dst: relation[0], role: relation[1] + '接続'}]
        };
      }
      const direct=full(source);if(direct)return {...direct,source};
      let text=key(source), question=text.endsWith('?');text=text.replace(/\?$/,'');if(text.endsWith('か')){question=true;text=text.slice(0,-1);}
      const notes=[];let feature='';
      for(const [tail,label] of [['ことができなかった','過去の可能の否定'],['ことである','指針'],['ことです','指針'],['ことだ','指針'],['こと','行為'],['ことができない','可能の否定'],['ことができる','可能'],['必要がある','必要'],['つもりだ','意図'],['かもしれない','推量'],['と思う','思考'],['かも','推量']])if(text.endsWith(tail)){text=text.slice(0,-tail.length);feature=label;break;}
      const alias=[...aliases].sort((a,b)=>b.ending.length-a.ending.length).find(a=>text.endsWith(a.ending));
      let form=alias ? forms.find(f=>f.ending===alias.replacement) : forms.find(f=>text.endsWith(f.ending));
      const ending=alias?.ending || form?.ending;
      let senseOptions=[];
      if(!alias && form) {
        const options=[...new Map(forms.filter(f=>f.ending===form.ending).map(f=>[f.id+':'+(f.adjective||0),f])).values()];
        if(options.length>1) {
          senseOptions=options.map(f=>{const e=byId.get(f.adjective||f.id);return {value:f.id+':'+(f.adjective||0),root:e.r,meaning:e.m};});
          const selected=options.find(f=>f.id+':'+(f.adjective||0)===choices.sense);
          if(!selected)return {source,text:'',state:'draft',senseOptions,notes:['語義候補が複数あります。対応するNebulith語を選択してください。']};
          form=selected;notes.push('語義＝'+byId.get(form.adjective||form.id).r+'（利用者が選択）');
        }
      }
      if(!ending) {
        try {const args=argsOf(text);return {source,text:caseOrder.filter(c=>args[c]).map(c=>c+' '+args[c]).join(' '),state:'draft',notes:['動詞の入力待ち'],alignment:argumentRows(args)};}catch(_){}
        try{return {source,text:phrase(text),state:'phrase',notes:['語句として変換']};}catch(_){}
        const prefix=text && vocab.some(e=>gloss(e).some(g=>g.startsWith(text)));
        return {source,text:'',state:prefix?'draft':'blocked',notes:[prefix?'語の入力待ち':'語句・構文を確定できません。原文全体を保持しています。']};
      }
      const body=text.slice(0,-ending.length);let args;
      let verbOptions=[];
      const verbGroup=alias?.chooseGroup || (alias?.chooseVerb ? '見る' : null);
      if(verbGroup && verbChoiceMap[verbGroup]) {
        verbOptions = verbChoiceMap[verbGroup].map(o => o.label);
        notes.push('動作候補（' + verbGroup + '）：' + verbOptions.slice(0, 4).join('／') + (verbOptions.length > 4 ? 'など' : '') + 'を選択できます。');
      }
      if(alias?.feature)feature=[feature,alias.feature].filter(Boolean).join('・');
      if(form?.feature)feature=[feature,form.feature].filter(Boolean).join('・');
      if(feature && !['行為','指針'].includes(feature))notes.push(feature+'の表現は未対応。意味を省略せず保持します。');
      try {args=parsedArgs(body,form||{});}catch(_) {
        try {
          const split=body.match(/^(.+?)[はが、,](.+)$/);
          if(split) {try{args=argsOf(split[2]);}catch(_){args={ia:phrase(split[2])};argSources.set(args,{ia:{text:split[2],inferred:true}});}}
          else {args={ia:phrase(body)};argSources.set(args,{ia:{text:body,inferred:true}});}
          if(split){args.el=phrase(split[1]);argSources.set(args,{...(argSources.get(args)||{}),el:{text:split[1],particle:body[split[1].length],inferred:true}});}notes.push('対象の役割を推定。確認してください。');
        }catch(_){return {source,text:'',state:'blocked',notes:[...notes,'語句・助詞の解釈が未対応です。']};}
      }
      if(choices.subject) {try{args.el=phrase(choices.subject);argSources.set(args,{...(argSources.get(args)||{}),el:{text:choices.subject,inferred:true}});notes.push('主体＝'+choices.subject+'（利用者が補完）');}catch(_){} }
      if(form?.emotion && !args.el)notes.push('感情の対象は指定済み。嫌う主体は未指定です。');
      if(verbGroup && verbChoiceMap[verbGroup] && choices.verb) {
        const selectedOpt = verbChoiceMap[verbGroup].find(o => o.label === choices.verb);
        if(!selectedOpt) {
          return {source,text:fragments,state:'blocked',notes:[...notes,'未対応の動作の解釈です。']};
        }
        if(selectedOpt.targetIa && args.ia !== selectedOpt.targetIa) {
          return {source,text:'',state:'blocked',notes:[...notes,selectedOpt.label+'への読み替えは未来を対象とする場合だけ対応しています。']};
        }
        const selectedForm = forms.find(f => f.id === selectedOpt.id && !f.feature && f.suffix === (form?.suffix || '') && JSON.stringify(f.prefixes) === JSON.stringify(form?.prefixes || []));
        if(selectedForm) {
          form = selectedForm;
          notes.push('動作の解釈＝'+choices.verb+'（利用者が選択）');
        }
      }
      const fragments=caseOrder.filter(c=>args[c]).map(c=>c+' '+args[c]).join(' ');
      notes.push(...lexicalNotes(fragments));
      if(!args.el && feature !== '行為') {
        args.el = 'mi';
        argSources.set(args, {
          ...(argSources.get(args)||{}),
          el: { text: '私', particle: '（自動補完）', inferred: true }
        });
        notes.push('主語未指定のため「私」を自動補完しました。');
      }
      if(alias && !alias.complete)notes.push('動作の続きの入力待ち');
      if(verbGroup && choices.verb && !verbOptions.includes(choices.verb))return {source,text:fragments,state:'blocked',notes:[...notes,'未対応の動作の解釈です。']};
      const meaning=meaningOf(form?{...form,ending}:null,args,question,feature);
      if(feature==='行為' || feature==='指針') {
        if(!args.el) {
          const p = form ? (byId.get(form.id).r + (form.suffix || '')) : '';
          const words = [p];
          for(const c of caseOrder) if(c!=='el' && args[c]) words.push(c, args[c]);
          const phraseText = words.join(' ');
          return {
            source,
            text: phraseText,
            state: 'phrase',
            meaning,
            alignment: meaning.alignment,
            notes: [...notes, (feature==='行為'?'行為（動名詞句）':'指針') + 'として変換。Nebulithの語順・格標識を適用。', ...extensionNotes(form)]
          };
        }
        try {
          const words = [...form.prefixes, (form.passive ? 're' : '') + byId.get(form.id).r + (form.suffix || '')];
          for(const c of caseOrder) if(args[c]) words.push(c, args[c]);
          const candidate = words[0][0].toUpperCase() + words[0].slice(1) + (words.length > 1 ? ' ' + words.slice(1).join(' ') : '') + '.';
          return {
            source,
            text: candidate,
            state: choices.confirmed ? 'complete' : 'candidate',
            candidate,
            meaning,
            senseOptions,
            alignment: meaning.alignment,
            notes: [...notes, (feature==='行為'?'行為の叙述':'指針') + 'として変換。Nebulithの格・項構造を検証。', ...extensionNotes(form)]
          };
        } catch(e) {
          return {source, text: fragments, state: 'blocked', notes: [...notes, e.message]};
        }
      }
      if(feature || !form)return {source,text:fragments,state:'blocked',meaning,notes:[...notes,...(!form?['時制・相の組み合わせは未対応です。']:[])],alignment:argumentRows(args)};
      if(!args.el || alias && !alias.complete || verbGroup && !choices.verb)return {source,text:fragments,state:'draft',meaning,verbOptions,notes,alignment:argumentRows(args)};
      try {
        const candidate=realize(meaning);
        return {source,text:candidate,state:choices.confirmed?'complete':'candidate',candidate,meaning,senseOptions,verbOptions,alignment:meaning.alignment,notes:[...notes,'Nebulithの格・項構造を検証。解釈を確認して確定してください。',...extensionNotes(form)]};
      }catch(e){return {source,text:fragments,state:'blocked',notes:[...notes,e.message]};}
    }
    const coveredIds=new Set(forms.filter(f=>!f.adjective).map(f=>f.id));
    return { coverage() {
      return {predicates:coveredIds.size,productiveLemmas:(productive.verbs||[]).length,verbForms:forms.filter(f=>!f.adjective && !f.feature).length,
        adjectiveForms:forms.filter(f=>f.adjective).length,places:placeRoots.size,
        verbs:(productive.verbs||[]).map(v=>({id:v.id,lemma:v.lemma,root:byId.get(v.id).r})),
        unsupportedVerbs:vocab.filter(e=>e.p.includes('動')&&!coveredIds.has(e.id)).map(e=>({id:e.id,root:e.r,meaning:e.m,reason:'項構造・日本語活用の未整備。自動で意味を推測しません。'}))};
    }, analyze(input,choices={}) {
      if(!input.trim())return {segments:[],complete:false,text:'',notes:[],recordable:false};
      if(input.length>4000)return {segments:[],complete:false,text:'',notes:['4,000文字以内で入力してください。'],recordable:true};
      const direct=full(input);
      const parts=direct ? [{...direct,source:input}] : (input.match(/[^。！？!?\n]+[。！？!?]*/g)||[]).filter(x=>x.trim()).map(x=>x.trim());
      const occurrences=new Map();
      const segments=direct?parts.map(p=>({...p,key:JSON.stringify([p.source,0])})):parts.map(p=>{
        const occurrence=occurrences.get(p)||0;occurrences.set(p,occurrence+1);const segmentKey=JSON.stringify([p,occurrence]);
        const selected=parts.length===1?choices:choices.bySegment?.[segmentKey]||{};
        return {...(p.length>240?{source:p,text:'',state:'blocked',notes:['1文240文字以内で入力してください。']}:part(p,selected)),key:segmentKey};
      });
      return {segments,complete:segments.length>0 && segments.every(s=>s.state==='complete'),
        text:segments.map(s=>(['complete','phrase'].includes(s.state)?'':s.state==='blocked'?'〔要対応〕 ':'〔途中案〕 ')+s.text).join('\n'),
        notes:[...new Set(segments.flatMap(s=>s.notes))],recordable:segments.some(s=>s.state==='blocked'),candidate:segments.length===1?segments[0].candidate||'':''};
    }};
  };
})(globalThis);
