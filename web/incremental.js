/* Offline interpretation: no network, no invisible subject/mood insertion. */
(function (global) {
  'use strict';
  function japaneseForms(lemma,kind) {
    let stem,past,te,negative,polite,potStem;
    if(kind==='kuru'){stem='来';past='来た';te='来て';negative='来ない';polite='来';potStem='来られ';}
    else if(kind==='suru'){stem=lemma.slice(0,-2);past=stem+'した';te=stem+'して';negative=stem+'しない';polite=stem+'し';potStem=stem+'でき';}
    else if(kind==='ichidan'){stem=lemma.slice(0,-1);past=stem+'た';te=stem+'て';negative=stem+'ない';polite=stem;potStem=stem+'られ';}
    else {
      const endings={'う':['わ','い','った','って','え'],'く':['か','き','いた','いて','け'],'ぐ':['が','ぎ','いだ','いで','げ'],'す':['さ','し','した','して','せ'],'つ':['た','ち','った','って','て'],'ぬ':['な','に','んだ','んで','ね'],'ぶ':['ば','び','んだ','んで','べ'],'む':['ま','み','んだ','んで','め'],'る':['ら','り','った','って','れ']};
      const table=endings[kind];if(!table || !lemma.endsWith(kind))throw Error('不正な動詞活用設定：'+lemma);
      stem=lemma.slice(0,-1);negative=stem+table[0]+'ない';polite=stem+table[1];past=stem+table[2];te=stem+table[3];potStem=stem+table[4];
    }
    const rows=[
      // 基本形・過去・否定・過去否定
      [lemma,[]],[past,['fe']],[negative,['ne']],[negative.slice(0,-1)+'かった',['fe','ne']],
      // 丁寧語
      [polite+'ます',[]],[polite+'ました',['fe']],[polite+'ません',['ne']],[polite+'ませんでした',['fe','ne']],
      // 進行相
      [te+'いる',['di']],[te+'います',['di']],[te+'いた',['fe','di']],[te+'いました',['fe','di']],
      [te+'いない',['ne','di']],[te+'いません',['ne','di']],[te+'いなかった',['fe','ne','di']],[te+'いませんでした',['fe','ne','di']],
      // 口語の「い」省略。否定形は完了否定とも読めるため、この追加には含めない。
      [te+'る',['di'],'','進行相（口語）'],[te+'た',['fe','di'],'','過去の進行相（口語）'],
      [te+'ます',['di'],'','進行相（口語）'],[te+'ました',['fe','di'],'','過去の進行相（口語）'],
      // 依頼の意味を認識して保持する。未定義の命令・依頼小詞は生成しない。
      [te+'ください',[],'','依頼'],
      // 始相。接辞はここでは埋めない。エンジンが言語データの始動相接辞を当て、無いときは未確認候補のままにする。
      [polite+'始める',[],'','始相'],[polite+'始めた',['fe'],'','始相'],[polite+'始めます',[],'','始相'],[polite+'始めました',['fe'],'','始相'],
      // 推量直接活用 (se-)
      [lemma+'だろう',['se']], [lemma+'でしょう',['se']],
      [past+'だろう',['se','fe']], [past+'でしょう',['se','fe']],
      [negative+'だろう',['se','ne']], [negative+'でしょう',['se','ne']],
      [negative.slice(0,-1)+'かっただろう',['se','fe','ne']],
      [polite+'ますでしょう',['se']],
      // 希望（Desiderative -ast）
      [polite+'たい',[],'ast','希望'],[polite+'たいです',[],'ast','希望'],
      [polite+'たかった',['fe'],'ast','過去の希望'],[polite+'たかったです',['fe'],'ast','過去の希望'],
      [polite+'たくない',['ne'],'ast','希望の否定'],[polite+'たくありません',['ne'],'ast','希望の否定'],
      [polite+'たくなかった',['fe','ne'],'ast','過去の希望の否定'],[polite+'たくありませんでした',['fe','ne'],'ast','過去の希望の否定'],
      [polite+'たくないです',['ne'],'ast','希望の否定'],[polite+'たくなかったです',['fe','ne'],'ast','過去の希望の否定'],
      // 可能（Potential -ar）
      [potStem+'る',[],'ar','可能'],[potStem+'ます',[],'ar','可能'],
      [potStem+'た',['fe'],'ar','過去の可能'],[potStem+'ました',['fe'],'ar','過去の可能'],
      [potStem+'ない',['ne'],'ar','可能の否定'],[potStem+'ません',['ne'],'ar','可能の否定'],
      [potStem+'なかった',['fe','ne'],'ar','過去の可能の否定'],[potStem+'ませんでした',['fe','ne'],'ar','過去の可能の否定'],
      [lemma+'ことができる',[],'ar','可能'],[lemma+'ことができます',[],'ar','可能'],[lemma+'ができます',[],'ar','可能'],
      [lemma+'ことができた',['fe'],'ar','過去の可能'],[lemma+'ができました',['fe'],'ar','過去の可能'],
      [lemma+'ことができない',['ne'],'ar','可能の否定'],[lemma+'ができません',['ne'],'ar','可能の否定'],
      [lemma+'ことができなかった',['fe','ne'],'ar','過去の可能の否定'],[lemma+'ができませんでした',['fe','ne'],'ar','過去の可能の否定'],
      // 推量モダリティ（Conjecture se- モダリティ候補）
      [lemma+'かもしれない',['se'],'','推量'],[lemma+'かも',['se'],'','推量'],
      [past+'かもしれない',['se','fe'],'','過去の推量'],[past+'かも',['se','fe'],'','過去の推量'],
      [negative+'かもしれない',['se','ne'],'','否定の推量'],[negative+'かも',['se','ne'],'','否定の推量'],
      [negative.slice(0,-1)+'かったかもしれない',['se','fe','ne'],'','過去否定の推量'],
      // 完了相（Perfective -far）
      [polite+'終える',[],'far','完了相'],[polite+'終えます',[],'far','完了相'],
      [polite+'終えた',['fe'],'far','過去の完了相'],[polite+'終えました',['fe'],'far','過去の完了相'],
      [polite+'終わる',[],'far','完了相'],[polite+'終わります',[],'far','完了相'],
      [polite+'終わった',['fe'],'far','過去の完了相'],[polite+'終わりました',['fe'],'far','過去の完了相'],
      [polite+'終えない',['ne'],'far','完了相の否定'],[polite+'終えません',['ne'],'far','完了相の否定'],
      [polite+'終えなかった',['fe','ne'],'far','過去の完了相の否定'],[polite+'終えませんでした',['fe','ne'],'far','過去の完了相の否定'],
      // 継続相（Durative / Continuative -liv）
      [polite+'続ける',[],'liv','継続相'],[polite+'続けます',[],'liv','継続相'],
      [polite+'続けた',['fe'],'liv','過去の継続相'],[polite+'続けました',['fe'],'liv','過去の継続相'],
      [polite+'続けない',['ne'],'liv','継続相の否定'],[polite+'続けません',['ne'],'liv','継続相の否定'],
      [polite+'続けなかった',['fe','ne'],'liv','過去の継続相の否定'],[polite+'続けませんでした',['fe','ne'],'liv','過去の継続相の否定']
    ];
    return rows.map(([ending,prefixes,suffix='',feature=''])=>({ending,prefixes,suffix,feature}));
  }
  function findInchoativeAffix(vocab) {
    const found = [];
    for (const entry of vocab || []) {
      const pos = String(entry.p || entry.pos || '');
      const meaning = String(entry.m || entry.meaningJa || '') + '\n' + String(entry.en || entry.meaningEn || '');
      if (!pos.includes('接')) continue;
      if (!/始動|し始める|inceptive|inchoative/.test(meaning)) continue;
      if (/希望|desider/.test(meaning)) continue;
      const suffix = String(entry.r || entry.nrs || '').replace(/^-/, '').trim();
      if (/^[a-z]+$/.test(suffix)) found.push(suffix);
    }
    const unique = [...new Set(found)];
    return unique.length === 1 ? unique[0] : null;
  }
  global.nebulithJapaneseForms=japaneseForms;
  global.createIncrementalTranslator = function (vocab, frames, aliases, pairs, extensions={}) {
    function splitSentences(input) {
      const parts = [], closing = [];
      let buffer = '';
      for (let i = 0; i < input.length; i++) {
        const c = input[i];
        buffer += c;
        if (c === '「' || c === '『') closing.push(c === '「' ? '」' : '』');
        else if (c === closing[closing.length - 1]) closing.pop();
        if (!closing.length && /[。！？!?\n]/.test(c) && !/[。！？!?\n]/.test(input[i + 1] || '')) {
          if (buffer.trim()) parts.push(buffer.trim());
          buffer = '';
        }
      }
      if (buffer.trim()) parts.push(buffer.trim());
      return parts;
    }
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
    const productive={...(extensions.productive||{}),verbs:[...(extensions.productive?.verbs||[]),...(extensions.compoundProductive?.verbs||[]),...(extensions.roadmapProductive?.verbs||[])]};
    for(const verb of productive.verbs||[])if(!frames[verb.id])frames[verb.id]=verb.frame;
    const placeRoots=new Set(['govan','vyrelar','nerar','celvan',...(productive.placeIds||[]).map(id=>byId.get(id)?.r).filter(Boolean)]);
    const argSources=new WeakMap();
    const gloss = e => e.m.split(/[、／]/).map(x => x.trim()).filter(Boolean);
    const pronouns = {'私':'mi','あなた':'ti','彼':'ri','彼女':'ri','彼／彼女':'ri',...(productive.pronounAliases||{})};
    const vccObj = typeof VERIFIED_CANONICAL_COMPOUNDS !== 'undefined' ? VERIFIED_CANONICAL_COMPOUNDS : (typeof globalThis !== 'undefined' ? globalThis.VERIFIED_CANONICAL_COMPOUNDS : null);
    const verifiedCompoundEntries = (vccObj && Array.isArray(vccObj.entries))
      ? vccObj.entries.map(c => ({
          id: c.id,
          r: c.nrs,
          p: c.pos,
          m: c.meaningJa,
          en: c.meaningEn,
          c: c.category || '',
          o: 'verified_compound',
          morphemes: c.morphemes
        }))
      : [];
    for (const ce of verifiedCompoundEntries) {
      if (!byId.has(ce.id)) byId.set(ce.id, ce);
      if (ce.c.includes('都市') || ce.c.includes('自然') || ce.r.endsWith('velar') || ce.r.endsWith('govan') || ce.r.endsWith('vorn') || ce.r.endsWith('domom') || ce.r.endsWith('nerar') || ce.r.endsWith('nerom') || ce.r.endsWith('renar') || ce.r.endsWith('livar') || ce.r.endsWith('larar') || ce.r.endsWith('calor') || ce.r.endsWith('talon') || ce.r.endsWith('velom') || ce.r.endsWith('daron')) {
        placeRoots.add(ce.r);
      }
    }
    const index = new Map();
    for (const e of vocab) for (const g of gloss(e)) { if (!index.has(g)) index.set(g, []); index.get(g).push(e); }
    for (const ce of verifiedCompoundEntries) {
      for (const g of gloss(ce)) {
        if (!index.has(g)) index.set(g, []);
        if(!index.get(g).some(e=>e.id===ce.id))index.get(g).push(ce);
      }
    }
    const heldIds = new Set((extensions.roadmapProductive?.held||[]).map(row=>row.id));
    const adjectives = [...vocab.filter(e => e.p.includes('形')&&!heldIds.has(e.id)).flatMap(e => gloss(e).map(g => [g,e])),...(extensions.roadmapProductive?.adjectives||[]).map(a=>[a.lemma,byId.get(a.id)])];
    const key = s => s.trim().replace(/\s+/g,'').replace(/？/g,'?').replace(/[。.]$/,'');
    let activeNounSenses={},activeNounOptions=new Map();
    const nounFailure=(e,source,notes=[])=>({source,text:'',state:'draft',nounOptions:[e.nounOptions],notes:[...notes,e.message]});
    function phrase(text, adj = false, depth = 0) {
      if (!text || depth > 2) throw Error('名詞句が未完成、または修飾が複雑です。');
      if (pronouns[text]) return pronouns[text];
      const found = [...new Map([...(index.get(text)||[]), ...(adj ? (index.get(text+'な')||[]) : [])].filter(e=>e.p.includes('名') || adj && e.p.includes('形')).map(e=>[e.id,e])).values()];
      if(found.some(e=>heldIds.has(e.id)))throw Error('語義・構成語の再整理待ちです。');
      if (found.length === 1) return found[0].r;
      if (found.length > 1) {
        activeNounOptions.set(text,{term:text,options:found.map(e=>({id:e.id,root:e.r,meaning:e.m}))});
        const selected=found.find(e=>e.id===activeNounSenses[text]);
        if(selected)return selected.r;
        throw Object.assign(Error(`「${text}」の語義候補が複数：`+found.slice(0,5).map(e=>e.r).join(' / ')),{code:'ambiguous_noun',nounOptions:{term:text,options:found.map(e=>({id:e.id,root:e.r,meaning:e.m}))}});
      }
      if(text.endsWith('こと')) {
        const v = text.slice(0, -2);
        const verbEntry = vocab.find(e => e.p.includes('動') && gloss(e).includes(v));
        if(verbEntry) return verbEntry.r;
      }
      const results = new Set();
      for (const [g,e] of adjectives) if(g.length>=2 && text.startsWith(g) && text.length>g.length) {
        try { results.add(phrase(text.slice(g.length),false,depth+1)+' '+e.r); } catch (_) {}
      }
      if(results.size===1) return [...results][0];
      if ((text.match(/の/g)||[]).length === 1) { const [a,b] = text.split('の'); return phrase(b,adj,depth+1)+' en '+phrase(a,false,depth+1); }
      if(!text.includes('の') && (text.match(/と/g)||[]).length===1) {
        const [a,b]=text.split('と');return phrase(a,false,depth+1)+' ul '+phrase(b,false,depth+1);
      }
      throw Error(`「${text}」の名詞・修飾語を確定できません。`);
    }
    const particles = [['によって','de'],['を使って','de'],['とともに','ku'],['と共に','ku'],['と一緒に','ku'],['よりも','va'],['より','va'],['から','va'],['が','el'],['は','el'],['を','ia'],['へ','to'],['に','to'],['で','uo'],['と','ku']];
    function argsOf(text,frame=null) {
      const found=[]; let budget=500,ambiguity=null;
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
            } catch (e) {if(e.code==='ambiguous_noun')ambiguity=e;}
            at=rest.indexOf(p,at+p.length);
          }
        }
      }
      parse(text,{});
      const unique = new Map(found.map(a=>[JSON.stringify(Object.entries(a.args).sort()),a]));
      const coordinated=[...unique.values()].filter(r=>r.args.el?.includes(' ul ') && /と.+[はが]/.test(text));
      if(unique.size===0 && ambiguity)throw ambiguity;
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
    for(const [id,s] of [[16,'輝く'],[902,'歩く'],[953,'観測する'],[972,'食べる']]) add(id,['繰り返し'+s],[],'cor');
    const inchoativeAffix = findInchoativeAffix(vocab);
    function adopt(row) {
      if ((row.feature || '').includes('始相')) row.suffix = inchoativeAffix || '';
      return row;
    }
    for(const [id,lemma,kind] of [[16,'輝く','く'],[16,'光る','る'],[902,'歩く','く'],[953,'観測する','suru'],[972,'食べる','ichidan']]) {
      for(const f of japaneseForms(lemma, kind)) forms.push(adopt({...f, id, passive: false}));
    }
    for(const f of extensions.forms||[])forms.push({...f,suffix:'',passive:false,extension:true});
    for(const verb of productive.verbs||[])for(const f of japaneseForms(verb.lemma,verb.conjugation))forms.push(adopt({...f,id:verb.id,passive:false,extension:true}));
    for(const e of vocab.filter(e=>e.p.includes('形')))for(const g of gloss(e)) {
      if(!g.endsWith('い') && !g.endsWith('な'))continue;
      const base=g.endsWith('な')?g.slice(0,-1):g;
      const variants=g.endsWith('な')?[[base,[]]]:[[base,[]],[base.slice(0,-1)+'かった',['fe']],[base.slice(0,-1)+'くない',['ne']],[base.slice(0,-1)+'くなかった',['fe','ne']],[base+'です',[]],[base.slice(0,-1)+'かったです',['fe']]];
      for(const [ending,prefixes] of variants)forms.push({id:906,ending,prefixes,suffix:'',passive:false,adjective:e.id,adjectiveSource:base,bareAdjective:true,extension:true});
    }
    for(const row of extensions.roadmapProductive?.adjectives||[])if(row.predicative) {
      const base=row.predicateLemma||(row.kind==='na'?row.lemma.slice(0,-1):row.lemma);
      const stem=base.endsWith('良い')?base.slice(0,-2)+'良':base.slice(0,-1);
      const variants=row.kind==='na'?[[base+'だ',[]],[base+'です',[]],[base+'だった',['fe']],[base+'ではない',['ne']],[base+'ではなかった',['fe','ne']]]:[[base,[]],[stem+'かった',['fe']],[stem+'くない',['ne']],[stem+'くなかった',['fe','ne']]];
      for(const [ending,prefixes] of variants)forms.push({id:906,ending,prefixes,suffix:'',passive:false,adjective:row.id,adjectiveSource:base,bareAdjective:true,extension:true});
    }
    const seenForms=new Set();
    const uniqueForms=forms.filter(f=>{const signature=JSON.stringify([f.id,f.ending,f.prefixes,f.suffix,f.adjective||0,f.feature||'']);if(seenForms.has(signature))return false;seenForms.add(signature);return true;});
    forms.splice(0,forms.length,...uniqueForms);
    forms.sort((a,b)=>b.ending.length-a.ending.length);
    const formsByEnding = new Map();
    for (const form of forms) {
      if (!formsByEnding.has(form.ending)) formsByEnding.set(form.ending, []);
      formsByEnding.get(form.ending).push(form);
    }
    function matchingForms(text) {
      const matched = [];
      // Longest suffix first, retaining the original order among equal endings.
      for (let start = 0; start < text.length; start++) {
        const rows = formsByEnding.get(text.slice(start));
        if (rows) matched.push(...rows);
      }
      return matched;
    }

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
    const roles={el:'主体',ia:'対象・補語',al:'受け手',uo:'場所',to:'目的地',va:'比較起点・起点',de:'動作主・道具',ku:'共同者'};
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
      const roles='述語'+(f.prefixes.includes('ne')?'・否定':'')+(f.prefixes.includes('fe')?'・過去':'')+(f.prefixes.includes('se')?'・推量':'')+(f.suffix==='ar'?'・可能':'')+(f.suffix==='ast'?(f.feature?.includes('希望')&&!String(f.feature).includes('始相')?'・希望':'・始相'):'')+(f.suffix==='far'?'・完了相':'')+(f.suffix==='liv'?'・継続相':'')+(f.suffix==='cor'?'・反復':'');
      return [...argumentRows(args),{src:f.bareAdjective?'断定の文法（日本語では省略）':f.ending,dst:verb,role:roles},
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
      const isRealizedModal = form && (form.suffix==='ar' || form.suffix==='ast' || form.suffix==='far' || form.suffix==='liv' || form.prefixes.includes('se') || feature.includes('進行相')&&form.prefixes.includes('di'));
      return {schemaVersion:1,kind:'clause',predicate:form?{entryId:form.id,root:byId.get(form.id).r,source:form.ending,prefixes:[...form.prefixes],suffix:form.suffix||'',passive:!!form.passive}:null,
        arguments:Object.fromEntries(Object.entries(args).map(([c,nrs])=>[c,{nrs,role:roles[c],source:sources[c]?.text||'',particle:sources[c]?.particle||'',inferred:!!sources[c]?.inferred}])),        tense:form?.prefixes.includes('fe')?'past':'unmarked',negative:!!form?.prefixes.includes('ne') && !(feature.includes('否定') && /希望|可能/.test(feature)),aspect:form?.prefixes.includes('di')?'progressive':form?.suffix==='far'?'perfective':form?.suffix==='liv'?'durative':form?.suffix==='ast'?((feature.includes('希望')||form?.feature?.includes('希望'))&&!feature.includes('始相')?'desiderative':'inceptive'):form?.suffix==='ar'?'potential':form?.suffix==='cor'?'iterative':'unmarked',question:!!question,
        modalities:feature?[{kind:feature.includes('希望')?'desire':feature.includes('推量')?'uncertainty':feature.includes('可能')?'possibility':feature.includes('相')?'aspect':feature.includes('依頼')?'request':feature.includes('意図')?'intention':feature.includes('必要')?'necessity':'thought',sourceFeature:feature,negated:feature.includes('否定'),past:feature.includes('過去'),scope:'clause',realization:isRealizedModal?'synthesized':'not-defined'}]:[],
        alignment:form?outputAlignment(form,args,question):argumentRows(args)};
    }
    function realize(meaning) {
      if(!meaning.predicate)throw Error('動作が未指定です。');
      if(meaning.modalities.some(m => m.realization === 'not-defined'))throw Error('ニュアンスの出力規則が未定義です。');
      const p=meaning.predicate,frame=frames[p.entryId];if(!frame)throw Error('動詞の項構造が未対応です。');
      const allowed=p.passive?frame.passiveAllowed||[]:frame.allowed;
      const adjectiveComparison = p.entryId===906 && ['より','よりも'].includes(meaning.arguments.va?.particle)&&[...byId.values()].some(e=>e.r===meaning.arguments.ia?.nrs&&e.p.includes('形')&&!heldIds.has(e.id));
      const verbComparison = (extensions.roadmapProductive?.comparativePredicateIds||[]).includes(p.entryId)&&['より','よりも'].includes(meaning.arguments.va?.particle);
      if(!frame.required.every(c=>meaning.arguments[c])||Object.keys(meaning.arguments).some(c=>!allowed.includes(c) && !(c==='va' && (adjectiveComparison||verbComparison))))throw Error('主語・補語の不足、または動詞の項構造に合わない格があります。');
      if(frame.recipientAmbiguity&&meaning.arguments.ia?.nrs.split(/\s+ul\s+/).some(group=>frame.recipientAmbiguity.roots.includes(group.split(' ')[0])))throw Error(frame.recipientAmbiguity.reason);
      for(const [role,rule] of Object.entries(frame.literalArguments||{})) {
        const argument=meaning.arguments[role];
        if(argument&&!argument.nrs.split(/\s+ul\s+/).every(group=>rule.roots.includes(group.split(' ')[0])))throw Error(rule.reason);
      }
      const words=[...p.prefixes,(p.passive?'re':'')+p.root+p.suffix];
      for(const c of caseOrder)if(meaning.arguments[c])words.push(c,meaning.arguments[c].nrs);
      if(meaning.question)words.push('ka');const out=words.join(' ');
      return out[0].toUpperCase()+out.slice(1)+(meaning.question?'?':'.');
    }
    function full(text) {
      if(/^(.+?)と(.+?)の(.+?)$/.test(key(text)))return null;
      let rawInput = text;
      let isSuperlative = false;
      if (/(最も|一番)/.test(text)) {
        text = text.replace(/(最も|一番)[\s\u3000]*/g, '');
        isSuperlative = true;
      }
      const exact = [...new Set(pairs.filter(p=>(p.ja_variants||[p.ja]).some(x=>key(x)===key(text))).map(p=>p.neb))];
      let body=key(text), question=body.endsWith('?');body=body.replace(/\?$/,'');
      if(body.endsWith('か')) {question=true;body=body.slice(0,-1);}
      const results=[];
      const matchedForms = matchingForms(body);
      const longestMatch = matchedForms.reduce((n,f)=>Math.max(n,f.ending.length),0);
      for(const f of matchedForms) if(!f.feature && f.ending.length === longestMatch) {
        try {
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
      }
      const unique=[...new Map(results.map(r=>[r.text,r])).values()];
      if(exact.length===1) {
        const generated=unique.find(r=>r.text.toLowerCase()===exact[0].toLowerCase());
        const pair=pairs.find(p=>p.neb===exact[0] && (p.ja_variants||[p.ja]).some(x=>key(x)===key(text)));
        const alignment=generated?.alignment || registeredRows(text,exact[0],pair);
        return {text:exact[0],state:'complete',notes:['登録対訳との一致'],alignment,meaning:generated?.meaning||{schemaVersion:1,kind:'registered',source:text,target:exact[0],analysis:'word-analysis-incomplete'}};
      }
      if(unique.length===1) {
        let res = unique[0];
        if (isSuperlative) {
          let updatedText = res.text.replace(/^((?:(?:Fe|Se|Ne|Di)\s+)*)([a-zA-Z]+)/i, (m, prefixes, verb) => {
            return prefixes + 'cel' + verb.toLowerCase();
          });
          updatedText = updatedText[0].toUpperCase() + updatedText.slice(1);
          res = {
            ...res,
            text: updatedText,
            alignment: [{src: '最も', dst: 'cel-', role: '最上級'}, ...(res.alignment || [])]
          };
        }
        return {...res,state:'complete',notes:['Nebulithの格・項構造を検証',...res.extensionNotes,...lexicalNotes(res.text)]};
      }
      try {if(!question){const target=phrase(body);return {text:target,state:'phrase',notes:['語句として変換。完成文ではありません。',...lexicalNotes(target)],alignment:phraseRows(body,target,'語句')};}}catch(_){}
      return null;
    }
    function restoreClauseVerb(text, conj) {
      if(conj==='だから') {
        if(!text.endsWith('だ') && !text.endsWith('である')) return text + 'だ';
        return text;
      }
      if(conj==='たら' || conj==='だら') {
        return text + (conj==='だら' ? 'だ' : 'た');
      }
      if(conj==='ば') {
        if(text.endsWith('なけれ')) return text.slice(0,-3) + 'ない';
        if(text.endsWith('すれ')) return text.slice(0,-2) + 'する';
        if(text.endsWith('くれ')) return text.slice(0,-2) + 'くる';
        const eToEnd = {'え':'う','け':'く','げ':'ぐ','せ':'す','て':'つ','ね':'ぬ','べ':'ぶ','め':'む','れ':'る'};
        const last = text.slice(-1);
        if(eToEnd[last]) return text.slice(0,-1) + eToEnd[last];
        return text;
      }
      if(conj==='ても' || conj==='でも') {
        if(text.endsWith('なく')) return text.slice(0,-2) + 'ない';
        if(conj==='でも') {
          if(text.endsWith('い')) return text.slice(0,-1) + 'ぐ';
          if(text.endsWith('ん')) return text.slice(0,-1) + 'む';
          return text + 'だ';
        }
        if(text.endsWith('し')) {
          return text.endsWith('愛し') ? text.slice(0,-1) + 'する' : text.slice(0,-1) + 'す';
        }
        if(text.endsWith('き')) return text.slice(0,-1) + 'くる';
        if(text.endsWith('い')) return text.slice(0,-1) + 'く';
        if(text.endsWith('っ')) return text.slice(0,-1) + 'る';
        return text + 'る';
      }
      return text;
    }
    function part(source,choices={},depth=0) {
      const prior=activeNounSenses,priorOptions=activeNounOptions;activeNounSenses=choices.nounSenses||{};activeNounOptions=new Map();
      try {
        let result=partImpl(source,choices,depth);
        if(!choices.confirmed) {
          const groups=new Map([...(result.nounOptions||[]).map(g=>[g.term,g]),...activeNounOptions]);
          if(groups.size)result={...result,nounOptions:[...groups.values()]};
        }
        if(Object.keys(activeNounSenses).length&&['complete','phrase'].includes(result.state)&&!choices.confirmed)return {...result,state:'candidate',candidate:result.text,notes:[...result.notes,'名詞の語義を確認して確定してください。']};
        return result;
      } finally {activeNounSenses=prior;activeNounOptions=priorOptions;}
    }
    function partImpl(source,choices,depth=0) {
      let cleanSource = source.trim();

      // --- Quote & Reported Speech / Thought Handling ---
      let quoteMatch = cleanSource.match(/^(?:(.+?)[はが])?[「『](.+?)[」』]と(言った|言いました|言う|言います|思った|思いました|思う|思います)[。.]?$/);
      if (!quoteMatch) {
        quoteMatch = cleanSource.match(/^[「『](.+?)[」』]と(?:(.+?)[はが])?(言った|言いました|言う|言います|思った|思いました|思う|思います)[。.]?$/);
        if (quoteMatch) {
          quoteMatch = [quoteMatch[0], quoteMatch[2], quoteMatch[1], quoteMatch[3]];
        }
      }
      if (!quoteMatch && depth === 0) {
        let indirect = cleanSource.match(/^(.+?)[は](.+?)と(言った|言いました|言う|言います|思った|思いました|思う|思います)[。.]?$/);
        if (!indirect) {
          indirect = cleanSource.match(/^(.+?)と(.+?)[はが](言った|言いました|言う|言います|思った|思いました|思う|思います)[。.]?$/);
          if (indirect) {
            indirect = [indirect[0], indirect[2], indirect[1], indirect[3]];
          }
        }
        if (!indirect) {
          const whole = cleanSource.match(/^(.+?)と(言った|言いました|言う|言います|思った|思いました|思う|思います)[。.]?$/);
          if (whole && !whole[1].includes('こと')) {
            indirect = [whole[0], null, whole[1], whole[2]];
          }
        }
        if (indirect && !indirect[2].includes('こと')) {
          quoteMatch = indirect;
        }
      }

      if (quoteMatch) {
        if (depth >= 2) return {source,text:'',state:'blocked',notes:['引用の入れ子が深すぎます。一文を分けてください。']};
        const speakerRaw = (quoteMatch[1] || choices.subject || '私').trim();
        const innerText = quoteMatch[2].trim();
        const verbType = quoteMatch[3];
        const isThought = verbType.startsWith('思');
        const isPast = verbType.includes('た') || verbType.includes('まし');
        
        let speakerNeb;
        try { speakerNeb = phrase(speakerRaw); }
        catch (e) { return {source,text:'',state:'blocked',notes:['引用の話者を確定できません。',e.message]}; }
        const innerResult = part(innerText, choices, depth + 1);
        if (!['complete', 'candidate'].includes(innerResult.state)) {
          return {source,text:'',state:innerResult.state === 'draft' ? 'draft' : 'blocked',
            verbOptions:innerResult.verbOptions,senseOptions:innerResult.senseOptions,scopeAmbiguous:innerResult.scopeAmbiguous,
            notes:['引用内の文を確定してください。',...(innerResult.notes || [])]};
        }
        let innerNeb = innerResult.text ? innerResult.text.replace(/^[〔\[].*?[〕\]]\s*/, '').trim() : '';
        if (!innerNeb && innerResult.candidate) innerNeb = innerResult.candidate.trim();
        const innerClean = innerNeb.replace(/[.?]+$/, '');
        const verbRoot = isThought ? 'memar' : 'fenor';
        const verbWord = (isPast ? 'Fe ' : '') + (isPast ? verbRoot : (verbRoot[0].toUpperCase() + verbRoot.slice(1)));
        const fullNeb = `${verbWord} el ${speakerNeb} ia \"${innerClean}.\"`;
        
        const alignment = [
          {src: speakerRaw, dst: 'el ' + speakerNeb, role: '主体'},
          {src: verbType, dst: (isPast ? 'Fe ' : '') + verbRoot, role: (isThought ? '思考述語' : '発話述語') + (isPast ? '・過去' : '')},
          {src: '「' + innerText + '」と', dst: 'ia \"' + innerClean + '.\"', role: '引用節（対格）'},
          ...(innerResult.alignment || []).map(a => ({...a, role: '引用内・' + a.role}))
        ];
        const meaning = {
          schemaVersion: 1,
          kind: 'reported_clause',
          predicate: {root: verbRoot, past: isPast, type: isThought ? 'thought' : 'speech'},
          arguments: {el: speakerNeb, ia: innerClean},
          innerMeaning: innerResult.meaning
        };
        const allConfirmed = innerResult.state === 'complete';
        return {
          source,
          text: fullNeb,
          state: allConfirmed ? 'complete' : 'candidate',
          candidate: fullNeb,
          verbOptions: innerResult.verbOptions,
          senseOptions: innerResult.senseOptions,
          scopeAmbiguous: innerResult.scopeAmbiguous,
          meaning,
          alignment,
          notes: ['引用構文（' + (isThought ? '思考節' : '発話節') + '）として解析。', ...(innerResult.notes || [])]
        };
      }

      // --- Superlative Prefix Handling (最も / 一番) ---
      let isSuperlative = false;
      if (/(最も|一番)/.test(cleanSource)) {
        cleanSource = cleanSource.replace(/(最も|一番)[\s\u3000]*/g, '');
        isSuperlative = true;
      }

      // --- Adverb Modification Handling (時間・頻度・程度・様態) ---
      const adverbList = [
        { ja: 'いつも', neb: 'havon', role: '頻度副詞（恒常）' },
        { ja: '常に', neb: 'havon', role: '頻度副詞（恒常）' },
        { ja: '時々', neb: 'havtul', role: '頻度副詞（断続）' },
        { ja: 'たまに', neb: 'havtul', role: '頻度副詞（断続）' },
        { ja: 'すでに', neb: 'feval', role: '時間副詞（完了）' },
        { ja: 'もう', neb: 'feval', role: '時間副詞（完了）' },
        { ja: 'まだ', neb: 'divan', role: '時間副詞（継続）' },
        { ja: 'すぐに', neb: 'tasik', role: '時間副詞（即時）' },
        { ja: '直ちに', neb: 'tasik', role: '時間副詞（即時）' },
        { ja: 'とても', neb: 'solpar', role: '程度副詞（極大）' },
        { ja: '非常に', neb: 'solpar', role: '程度副詞（極大）' },
        { ja: 'たいへん', neb: 'solpar', role: '程度副詞（極大）' },
        { ja: '少し', neb: 'vyntul', role: '程度副詞（極小）' },
        { ja: 'わずかに', neb: 'vyntul', role: '程度副詞（極小）' },
        { ja: '全く', neb: 'narval', role: '程度副詞（全否定）' },
        { ja: 'かなり', neb: 'radon', role: '程度副詞（中庸）' },
        { ja: 'ゆっくり', neb: 'moril', role: '様態副詞（緩慢）' },
        { ja: '早く', neb: 'tasin', role: '様態副詞（迅速）' },
        { ja: '速く', neb: 'tasin', role: '様態副詞（迅速）' },
        { ja: '静かに', neb: 'sirik', role: '様態副詞（沈黙）' },
        { ja: '共に', neb: 'kulen', role: '様態副詞（協調）' },
        { ja: '一緒に', neb: 'kulen', role: '様態副詞（協調）' },
        { ja: '独りで', neb: 'minkir', role: '様態副詞（単独）' }
      ];

      let matchedAdverb = null;
      if (depth === 0) {
        for (const adv of adverbList) {
          if (cleanSource.includes(adv.ja)) {
            // Remove adverb from cleanSource
            cleanSource = cleanSource.replace(new RegExp(adv.ja + '[\\s\\u3000]*'), '');
            matchedAdverb = adv;
            break;
          }
        }
      }

      function withModalAdverb(result) {
        if(!matchedAdverb)return result;
        const text=matchedAdverb.neb[0].toUpperCase()+matchedAdverb.neb.slice(1)+' '+result.text.replace(/^./,c=>c.toLowerCase());
        return {...result,text,candidate:text,meaning:{...result.meaning,adverb:matchedAdverb},
          alignment:[{src:matchedAdverb.ja,dst:matchedAdverb.neb,role:matchedAdverb.role},...(result.alignment||[])]};
      }

      let moshi = false;
      if (/^もし[\s\u3000]*/.test(cleanSource)) {
        cleanSource = cleanSource.replace(/^もし[\s\u3000]*/, '');
        moshi = true;
      }
      const compound=cleanSource.match(/^(.+?)(ならば|なら|ので|から|だから|けれども|けれど|ときに|とき|時に|時|たら|だら|ば|ても|でも)(?:[、,]|\s+)(.+)$/);
      if(compound){
        if(matchedAdverb)return {source,text:'',state:'blocked',notes:['副詞がどの節にかかるか未確定です。意味を省略せず、一節ずつ入力してください。']};
        if((cleanSource.match(/(?:ならば|なら|ので|から|だから|けれども|けれど|ときに|とき|時に|時|たら|だら|ば|ても|でも)[、,]/g)||[]).length>1)return {source,text:'',state:'blocked',notes:['接続する節の範囲が複数あります。入れ子を推測せず、一節ずつ確認してください。']};
        if(depth>=2)return {source,text:'',state:'blocked',notes:['節の入れ子が深すぎます。一文を分けてください。']};
        const relation={
          'なら':['sen','条件'],'ならば':['sen','条件'],'たら':['sen','条件'],'だら':['sen','条件'],'ば':['sen','条件'],
          'ので':['zen','理由'],'から':['zen','理由'],'だから':['zen','理由'],
          'けれど':['tor','譲歩'],'けれども':['tor','譲歩'],'ても':['tor','譲歩'],'でも':['tor','譲歩'],
          'とき':['hav','時間'],'ときに':['hav','時間'],'時':['hav','時間'],'時に':['hav','時間']
        }[compound[2]];
        let firstClauseText = restoreClauseVerb(compound[1].trim(), compound[2]);
        const clauses=[part(firstClauseText,{},depth+1),part(compound[3].trim(),{},depth+1)];
        const meaning={schemaVersion:1,kind:'compound',relation:relation[0],clauses:clauses.map(c=>c.meaning||{kind:'unresolved',source:c.source})};
        if(clauses.some(c=>!['complete','candidate'].includes(c.state)||c.meaning?.question))return {source,text:'',state:clauses.some(c=>c.state==='blocked')?'blocked':'draft',meaning,notes:[relation[1]+'節の未確定部分を保持。節ごとに主体・解釈を明示してください。',...clauses.flatMap(c=>c.notes)]};
        const bare=t=>t.replace(/[.?]+$/,'').replace(/^./,c=>c.toLowerCase());
        const text=relation[0][0].toUpperCase()+relation[0].slice(1)+' '+bare(clauses[0].text)+', '+bare(clauses[1].text)+(clauses[1].text.endsWith('?')?'?':'.');
        const allConfirmed = clauses.every(c => c.state === 'complete');
        const extraNotes = moshi ? ['仮定・条件（もし〜なら）を認識。'] : [];
        return {source,text,state:allConfirmed?'complete':'candidate',candidate:text,meaning,alignment:[...clauses.flatMap((c,i)=>(c.alignment||[]).map(a=>({...a,role:(i?'主節':'従属節')+'・'+a.role}))),{src:(moshi?'もし... ':'')+compound[2],dst:relation[0],role:relation[1]+'接続'}],notes:['節ごとの意味を保持して生成。追加複文規則（未監査）。',...extraNotes,...clauses.flatMap(c=>c.notes)]};
      }
      const ownership=key(cleanSource).match(/^(.+?)と(.+?)の(.+?)$/);
      if(ownership)try {
        const [,a,b,thing]=ownership,ar=phrase(a),br=phrase(b),tr=phrase(thing);
        const notes=['所有範囲を選択：「（AとB）のC」または「Aと（BのC）」。追加の並列・所有文型案です。'];
        if(!['shared','separate'].includes(choices.possession))return {source,text:'',state:'draft',notes,scopeAmbiguous:true};
        const shared=choices.possession==='shared';
        const target=shared?tr+' en '+ar+' ul '+br:ar+' ul '+tr+' en '+br;
        const alignment=[...phraseRows(a,ar,shared?'共有所有者':'並列項'),{src:'と',dst:'ul',role:'並列'},...phraseRows(b,br,'所有者'),{src:'の',dst:'en',role:'属格（範囲を選択）'},...phraseRows(thing,tr,'所有物')];
        return {source,text:target,state:choices.confirmed?'phrase':'candidate',candidate:choices.confirmed?'':target,notes:[...notes,shared?'共有所有を選択':'別々の並列項を選択',...lexicalNotes(target)],scopeAmbiguous:true,alignment};
      }catch(_){}
      const trailingCompound = key(cleanSource).match(/^(.+?)(ならば|なら|ので|から|だから|けれども|けれど|ときに|とき|時に|時|たら|だら|ば|ても|でも)$/);
      if(trailingCompound) {
        let subText = restoreClauseVerb(trailingCompound[1].trim(), trailingCompound[2]);
        const relation = {
          'なら':['sen','条件'],'ならば':['sen','条件'],'たら':['sen','条件'],'だら':['sen','条件'],'ば':['sen','条件'],
          'ので':['zen','理由'],'から':['zen','理由'],'だから':['zen','理由'],
          'けれど':['tor','譲歩'],'けれども':['tor','譲歩'],'ても':['tor','譲歩'],'でも':['tor','譲歩'],
          'とき':['hav','時間'],'ときに':['hav','時間'],'時':['hav','時間'],'時に':['hav','時間']
        }[trailingCompound[2]];
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
          notes: [relation[1] + '節として解釈。続く主節の入力待ちです。', ...(moshi ? ['仮定・条件（もし〜なら）を認識。'] : []), ...subClause.notes],
          alignment: [...(subClause.alignment || []).map(a => ({...a, role: '従属節・' + a.role})), {src: (moshi ? 'もし... ' : '') + trailingCompound[2], dst: relation[0], role: relation[1] + '接続'}]
        };
      }
      const direct=full(cleanSource);if(direct) {
        let dText = direct.text;
        let dAlign = direct.alignment || [];
        if (isSuperlative) {
          dText = dText.replace(/^((?:(?:Fe|Se|Ne|Di)\s+)*)([a-zA-Z]+)/i, (m, prefixes, verb) => {
            return prefixes + 'cel' + verb.toLowerCase();
          });
          dText = dText[0].toUpperCase() + dText.slice(1);
          dAlign = [{src: '最も', dst: 'cel-', role: '最上級'}, ...dAlign];
        }
        if (matchedAdverb) {
          const advPrefix = matchedAdverb.neb[0].toUpperCase() + matchedAdverb.neb.slice(1);
          dText = advPrefix + ' ' + dText.replace(/^[A-Z]/, c => c.toLowerCase());
          dAlign = [{src: matchedAdverb.ja, dst: matchedAdverb.neb, role: matchedAdverb.role}, ...dAlign];
        }
        return {...direct, text: dText, candidate: dText, alignment: dAlign, source};
      }
      let text=key(cleanSource), question=text.endsWith('?');text=text.replace(/\?$/,'');if(text.endsWith('か')){question=true;text=text.slice(0,-1);}
      const notes=[];let feature='';
      for(const [tail,label] of [['ことができなかった','過去の可能の否定'],['ことである','指針'],['ことです','指針'],['ことだ','指針'],['こと','行為'],['ことができない','可能の否定'],['ことができる','可能'],['必要がある','必要'],['つもりだ','意図'],['かもしれない','推量'],['と思う','思考'],['かも','推量']])if(text.endsWith(tail)){text=text.slice(0,-tail.length);feature=label;break;}
      let alias=[...aliases].sort((a,b)=>b.ending.length-a.ending.length).find(a=>text.endsWith(a.ending));
      if(alias&&(matchingForms(text)[0]?.ending.length||0)>alias.ending.length)alias=null;
      let form=alias ? formsByEnding.get(alias.replacement)?.[0] : matchingForms(text)[0];
      const ending=alias?.ending || form?.ending;
      let senseOptions=[];
      if(!alias && form) {
        const options=[...new Map(formsByEnding.get(form.ending).map(f=>[f.id+':'+(f.adjective||0),f])).values()];
        if(options.length>1) {
          senseOptions=options.map(f=>{const e=byId.get(f.adjective||f.id);return {value:f.id+':'+(f.adjective||0),root:e.r,meaning:e.m};});
          const selected=options.find(f=>f.id+':'+(f.adjective||0)===choices.sense);
          if(!selected)return {source,text:'',state:'draft',senseOptions,notes:['語義候補が複数あります。対応するNebulith語を選択してください。']};
          form=selected;notes.push('語義＝'+byId.get(form.adjective||form.id).r+'（利用者が選択）');
        }
      }
      if(!ending) {
        try {const args=argsOf(text);return {source,text:caseOrder.filter(c=>args[c]).map(c=>c+' '+args[c]).join(' '),state:'draft',notes:['動詞の入力待ち'],alignment:argumentRows(args)};}catch(e){if(e.code==='ambiguous_noun')return nounFailure(e,source);}
        try{return {source,text:phrase(text),state:'phrase',notes:['語句として変換']};}catch(e){if(e.code==='ambiguous_noun')return nounFailure(e,source);}
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
      if(feature && !['行為','指針'].includes(feature)) {
        const isSupportedModal = ['希望','可能','推量','完了相','継続相','始相','進行相'].some(m => feature.includes(m));
        if(!isSupportedModal) notes.push(feature+'の表現は未対応。意味を省略せず保持します。');
      }
      if(verbGroup && verbChoiceMap[verbGroup] && choices.verb) {
        const selectedOpt = verbChoiceMap[verbGroup].find(o => o.label === choices.verb);
        if(!selectedOpt) {
          return {source,text:'',state:'blocked',notes:[...notes,'未対応の動作の解釈です。']};
        }
        const selectedForm = forms.find(f => f.id === selectedOpt.id && !f.feature && f.suffix === (form?.suffix || '') && JSON.stringify(f.prefixes) === JSON.stringify(form?.prefixes || []));
        if(selectedForm) {
          form = selectedForm;
          notes.push('動作の解釈＝'+choices.verb+'（利用者が選択）');
        }
      }
      try {args=parsedArgs(body,form||{});}catch(_) {
        if(_.code==='ambiguous_noun')return nounFailure(_,source,notes);
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
        if(selectedOpt && selectedOpt.targetIa && args.ia !== selectedOpt.targetIa) {
          return {source,text:'',state:'blocked',notes:[...notes,selectedOpt.label+'への読み替えは未来を対象とする場合だけ対応しています。']};
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
          return withModalAdverb({
            source,
            text: candidate,
            state: choices.confirmed ? 'complete' : 'candidate',
            candidate,
            meaning,
            senseOptions,
            alignment: meaning.alignment,
            notes: [...notes, (feature==='行為'?'行為の叙述':'指針') + 'として変換。Nebulithの格・項構造を検証。', ...extensionNotes(form)]
          });
        } catch(e) {
          return {source, text: fragments, state: 'blocked', notes: [...notes, e.message]};
        }
      }
      if(feature && form) {
        if(feature.includes('可能') && !form.suffix) {
          form = {...form, suffix: 'ar', prefixes: feature.includes('過去') ? [...form.prefixes, 'fe'] : form.prefixes};
          if(feature.includes('否定') && !form.prefixes.includes('ne')) form.prefixes = [...form.prefixes, 'ne'];
        } else if(feature.includes('希望') && !feature.includes('始相') && !form.suffix) {
          form = {...form, suffix: 'ast', feature: form.feature?.includes('希望') ? form.feature : [form.feature, '希望'].filter(Boolean).join('・'), prefixes: feature.includes('過去') ? [...form.prefixes, 'fe'] : form.prefixes};
          if(feature.includes('否定') && !form.prefixes.includes('ne')) form.prefixes = [...form.prefixes, 'ne'];
        } else if(feature.includes('完了相') && !form.suffix) {
          form = {...form, suffix: 'far', prefixes: feature.includes('過去') ? [...form.prefixes, 'fe'] : form.prefixes};
          if(feature.includes('否定') && !form.prefixes.includes('ne')) form.prefixes = [...form.prefixes, 'ne'];
        } else if(feature.includes('継続相') && !form.suffix) {
          form = {...form, suffix: 'liv', prefixes: feature.includes('過去') ? [...form.prefixes, 'fe'] : form.prefixes};
          if(feature.includes('否定') && !form.prefixes.includes('ne')) form.prefixes = [...form.prefixes, 'ne'];
        } else if(feature.includes('推量') && !form.prefixes.includes('se')) {
          form = {...form, prefixes: ['se', ...form.prefixes]};
          if(feature.includes('過去') && !form.prefixes.includes('fe')) form.prefixes = [...form.prefixes, 'fe'];
          if(feature.includes('否定') && !form.prefixes.includes('ne')) form.prefixes = [...form.prefixes, 'ne'];
        }
      }
      if(feature.includes('始相') && form) {
        const aspectNotes = ['始相（〜始める）は希望法とは別の候補です。未確認の形は自動では確定しません。'];
        if(!form.suffix) {
          aspectNotes.push('言語データに始動相の接辞が無いため、別の接尾辞へは読み替えません。');
          try {
            const base = {...form, suffix:'', feature:''};
            const baseMeaning = meaningOf({...base, ending}, args, question, '');
            const candidate = realize(baseMeaning);
            return {source, text:candidate, state:'candidate', candidate, meaning:baseMeaning, senseOptions, verbOptions, alignment:baseMeaning.alignment, notes:[...notes, ...aspectNotes]};
          } catch(e) {
            return {source, text:fragments, state:'candidate', candidate:'', meaning, senseOptions, verbOptions, notes:[...notes, ...aspectNotes, e.message], alignment:argumentRows(args)};
          }
        }
        try {
          const updatedMeaning = meaningOf({...form, ending}, args, question, feature);
          const candidate = realize(updatedMeaning);
          return withModalAdverb({
            source,
            text: candidate,
            state: choices.confirmed ? 'complete' : 'candidate',
            candidate,
            meaning: updatedMeaning,
            senseOptions,
            verbOptions,
            alignment: updatedMeaning.alignment,
            notes: [...notes, ...aspectNotes, '始相の接辞「'+form.suffix+'」を言語データから適用。確認後に確定します。']
          });
        } catch(e) {
          return {source, text:fragments, state:'blocked', notes:[...notes, ...aspectNotes, e.message]};
        }
      }
      const isModal = ['希望','可能','推量','完了相','継続相','進行相'].some(m => feature.includes(m));
      if(isModal && form) {
        try {
          const updatedMeaning = meaningOf(form ? {...form, ending} : null, args, question, feature);
          const candidate = realize(updatedMeaning);
          return withModalAdverb({
            source,
            text: candidate,
            state: choices.confirmed ? 'complete' : 'candidate',
            candidate,
            meaning: updatedMeaning,
            senseOptions,
            verbOptions,
            alignment: updatedMeaning.alignment,
            notes: [...notes, feature + 'のモダリティ表現を適用。Nebulithの格・項構造を検証。', ...extensionNotes(form)]
          });
        } catch(e) {
          return {source, text: fragments, state: 'blocked', notes: [...notes, e.message]};
        }
      }
      if(feature || !form)return {source,text:fragments,state:'blocked',meaning,notes:[...notes,...(!form?['時制・相の組み合わせは未対応です。']:[])],alignment:argumentRows(args)};
      if(!args.el || alias && !alias.complete || verbGroup && !choices.verb)return {source,text:fragments,state:'draft',meaning,verbOptions,notes,alignment:argumentRows(args)};
      try {
        let candidate=realize(meaning);
        let alignment=meaning.alignment;
        if(isSuperlative) {
          if(form && form.adjective) {
            const adjRoot = byId.get(form.adjective).r;
            candidate = candidate.replace(new RegExp('\\b' + adjRoot + '\\b', 'i'), 'cel' + adjRoot);
          } else {
            candidate = candidate.replace(/^((?:(?:Fe|Se|Ne|Di)\\s+)*)([a-zA-Z]+)/i, (m, prefixes, verb) => {
              return prefixes + 'cel' + verb.toLowerCase();
            });
            candidate = candidate[0].toUpperCase() + candidate.slice(1);
          }
          meaning.superlative = true;
          alignment = [{src: '最も', dst: 'cel-', role: '最上級'}, ...(alignment || [])];
        }
        if (matchedAdverb) {

          const advPrefix = matchedAdverb.neb[0].toUpperCase() + matchedAdverb.neb.slice(1);

          const bareCandidate = candidate.replace(/^[A-Z]/, c => c.toLowerCase());

          const fullCandidate = advPrefix + ' ' + bareCandidate;

          alignment = [

            { src: matchedAdverb.ja, dst: matchedAdverb.neb, role: matchedAdverb.role },

            ...alignment

          ];

          return {

            source,

            text: fullCandidate,

            state: 'complete',

            candidate: fullCandidate,

            meaning: { ...meaning, adverb: matchedAdverb },

            senseOptions,

            verbOptions,

            alignment,

            notes: [...notes, matchedAdverb.ja + '（' + matchedAdverb.role + '）の副詞修飾を適用。']

          };

        }

        return {source,text:candidate,state:choices.confirmed?'complete':'candidate',candidate,meaning,senseOptions,verbOptions,alignment,notes:[...notes,'Nebulithの格・項構造を検証。解釈を確認して確定してください。',...extensionNotes(form)]};
      }catch(e){return {source,text:fragments,state:'blocked',notes:[...notes,e.message]};}
    }
    const coveredIds=new Set(forms.filter(f=>!f.adjective).map(f=>f.id));
    const fragmentTerms=new Map();
    for(const term of [...index.keys()].filter(t=>t.length>=2).sort((a,b)=>b.length-a.length)) {
      if(!fragmentTerms.has(term[0]))fragmentTerms.set(term[0],[]);
      fragmentTerms.get(term[0]).push(term);
    }
    function fragmentsOf(source) {
      const fragments=[];let at=0,start=0;
      while(at<source.length) {
        const term=(fragmentTerms.get(source[at])||[]).find(t=>source.startsWith(t,at));
        if(!term){at++;continue;}
        if(start<at)fragments.push({source:source.slice(start,at),start,end:at,known:false});
        fragments.push({source:term,start:at,end:at+term.length,known:true,roots:[...new Set(index.get(term).map(e=>e.r))]});
        at+=term.length;start=at;
      }
      if(start<source.length)fragments.push({source:source.slice(start),start,end:source.length,known:false});
      return fragments;
    }
    return { splitSentences, coverage() {
      return {predicates:coveredIds.size,productiveLemmas:(productive.verbs||[]).length,verbForms:forms.filter(f=>!f.adjective && !f.feature).length,
        adjectiveForms:forms.filter(f=>f.adjective).length,places:placeRoots.size,
        verbs:(productive.verbs||[]).map(v=>({id:v.id,lemma:v.lemma,root:byId.get(v.id).r})),
        unsupportedVerbs:[...vocab,...verifiedCompoundEntries].filter(e=>e.p.includes('動')&&!coveredIds.has(e.id)).map(e=>({id:e.id,root:e.r,meaning:e.m,reason:'項構造・日本語活用の未整備。自動で意味を推測しません。'}))};
    }, analyze(input,choices={}) {
      if(!input.trim())return {segments:[],complete:false,text:'',notes:[],recordable:false};
      if(input.length>4000)return {segments:[],complete:false,text:'',notes:['4,000文字以内で入力してください。'],recordable:true};
      const direct=full(input);
      const parts=direct ? [{...direct,source:input}] : splitSentences(input);
      const occurrences=new Map();
      const segments=direct?parts.map(p=>({...p,key:JSON.stringify([p.source,0])})):parts.map(p=>{
        const occurrence=occurrences.get(p)||0;occurrences.set(p,occurrence+1);const segmentKey=JSON.stringify([p,occurrence]);
        const selected=parts.length===1?choices:choices.bySegment?.[segmentKey]||{};
        return {...(p.length>240?{source:p,text:'',state:'blocked',notes:['1文240文字以内で入力してください。']}:part(p,selected)),key:segmentKey};
      });
      let contextSubject=null;
      for(const segment of segments) {
        segment.fragments=['complete','phrase'].includes(segment.state)?[]:fragmentsOf(segment.source);
        const subject=segment.meaning?.arguments?.el;
        if(contextSubject&&(!subject||subject.inferred))segment.contextSubject=contextSubject;
        if(subject&&!subject.inferred)contextSubject={source:subject.source,nrs:subject.nrs};
      }
      return {segments,complete:segments.length>0 && segments.every(s=>s.state==='complete'),
        text:segments.map(s=>(['complete','phrase'].includes(s.state)?'':s.state==='blocked'?'〔要対応〕 ':'〔途中案〕 ')+s.text).join('\n'),
        notes:[...new Set(segments.flatMap(s=>s.notes))],recordable:segments.some(s=>s.state==='blocked'),candidate:segments.length===1?segments[0].candidate||'':''};
    }};
  };
})(globalThis);

