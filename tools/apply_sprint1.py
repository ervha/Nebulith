# Sprint 1 Implementation: Conditional Clauses & Modalities
import re

with open('web/incremental.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update japaneseForms
old_jf_start = content.find('function japaneseForms(lemma,kind) {')
old_jf_end = content.find('global.nebulithJapaneseForms=japaneseForms;')
assert old_jf_start != -1 and old_jf_end != -1, 'japaneseForms boundaries not found'

new_jf = '''function japaneseForms(lemma,kind) {
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
      // 始相
      [polite+'始める',[],'ast'],[polite+'始めた',['fe'],'ast'],[polite+'始めます',[],'ast'],[polite+'始めました',['fe'],'ast'],
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
      [negative.slice(0,-1)+'かったかもしれない',['se','fe','ne'],'','過去否定の推量']
    ];
    return rows.map(([ending,prefixes,suffix='',feature=''])=>({ending,prefixes,suffix,feature}));
  }
  '''

content = content[:old_jf_start] + new_jf + content[old_jf_end:]

# 2. Update outputAlignment to include potential/desire/conjecture
align_start = content.find('function outputAlignment(f,args,question) {')
align_end = content.find('function registeredRows(source,target,pair) {')
assert align_start != -1 and align_end != -1, 'outputAlignment boundaries not found'

new_align = '''function outputAlignment(f,args,question) {
      const verb=[...f.prefixes,(f.passive?'re':'')+byId.get(f.id).r+f.suffix].join(' ');
      const roles='述語'+(f.prefixes.includes('ne')?'・否定':'')+(f.prefixes.includes('fe')?'・過去':'')+(f.prefixes.includes('se')?'・推量':'')+(f.suffix==='ar'?'・可能':'')+(f.suffix==='ast'?(f.feature?.includes('希望')?'・希望':'・始相'):'')+(f.suffix==='cor'?'・反復':'');
      return [...argumentRows(args),{src:f.bareAdjective?'断定の文法（日本語では省略）':f.ending,dst:verb,role:roles},
        ...(question?[{src:'か／疑問符',dst:'ka',role:'疑問'}]:[])];
    }
    '''

content = content[:align_start] + new_align + content[align_end:]

# 3. Update meaningOf & realize
meaning_start = content.find('function meaningOf(form,args,question,feature=\'\') {')
meaning_end = content.find('const p=meaning.predicate,frame=frames[p.entryId];')
assert meaning_start != -1 and meaning_end != -1, 'meaningOf boundaries not found'

new_meaning = '''function meaningOf(form,args,question,feature='') {
      const sources=argSources.get(args)||{};
      const isRealizedModal = form && (form.suffix==='ar' || form.suffix==='ast' || form.prefixes.includes('se'));
      return {schemaVersion:1,kind:'clause',predicate:form?{entryId:form.id,root:byId.get(form.id).r,source:form.ending,prefixes:[...form.prefixes],suffix:form.suffix||'',passive:!!form.passive}:null,
        arguments:Object.fromEntries(Object.entries(args).map(([c,nrs])=>[c,{nrs,role:roles[c],source:sources[c]?.text||'',particle:sources[c]?.particle||'',inferred:!!sources[c]?.inferred}])),\
        tense:form?.prefixes.includes('fe')?'past':form?.prefixes.includes('se')?'future':'unmarked',negative:!!form?.prefixes.includes('ne'),aspect:form?.prefixes.includes('di')?'progressive':form?.suffix==='ast'?(form?.feature?.includes('希望')?'desiderative':'inceptive'):form?.suffix==='ar'?'potential':form?.suffix==='cor'?'iterative':'unmarked',question:!!question,
        modalities:feature?[{kind:feature.includes('希望')?'desire':feature.includes('推量')?'uncertainty':feature.includes('可能')?'possibility':feature.includes('意図')?'intention':feature.includes('必要')?'necessity':'thought',sourceFeature:feature,negated:feature.includes('否定'),past:feature.includes('過去'),scope:'clause',realization:isRealizedModal?'synthesized':'not-defined'}]:[],
        alignment:form?outputAlignment(form,args,question):argumentRows(args)};
    }
    function realize(meaning) {
      if(!meaning.predicate)throw Error('動作が未指定です。');
      if(meaning.modalities.some(m => m.realization === 'not-defined'))throw Error('ニュアンスの出力規則が未定義です。');
      '''

content = content[:meaning_start] + new_meaning + content[meaning_end:]

# 3.5 Update full with longest match preference
loop_start = content.find('for(const f of forms) if(!f.feature && body.endsWith(f.ending)) try {')
loop_end = content.find('const unique=[...new Map(results.map(r=>[r.text,r])).values()];', loop_start)
assert loop_start != -1 and loop_end != -1, 'full loop boundaries not found'

full_loop = content[loop_start:loop_end]
new_full_loop = '''let maxMatchLen = 0;
      for(const f of forms) if(!f.feature && body.endsWith(f.ending)) {
        if(maxMatchLen && f.ending.length < maxMatchLen) continue;
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
          maxMatchLen = Math.max(maxMatchLen, f.ending.length);
        }catch(_){}
      }
      '''

content = content[:loop_start] + new_full_loop + content[loop_end:]

# 4. Update part compound splitting & trailingCompound with restoreClauseVerb
part_start = content.find('function part(source,choices,depth=0) {')
part_tail = content.find('const ownership=key(source).match(/^(.+?)と(.+?)の(.+?)$/);')
assert part_start != -1 and part_tail != -1, 'part compound boundaries not found'

new_compound = '''function restoreClauseVerb(text, conj) {
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
          if(text.endsWith('いだ')) return text.slice(0,-2) + 'ぐ';
          if(text.endsWith('んだ')) return text.slice(0,-2) + 'む';
          return text + 'だ';
        }
        if(text.endsWith('して')) return text.slice(0,-2) + 'する';
        if(text.endsWith('きて')) return text.slice(0,-2) + 'くる';
        if(text.endsWith('いて')) return text.slice(0,-2) + 'く';
        if(text.endsWith('って')) return text.slice(0,-2) + 'る';
        return text;
      }
      return text;
    }
    function part(source,choices,depth=0) {
      let cleanSource = source.trim();
      let moshi = false;
      if (/^もし[\\s\\u3000]*/.test(cleanSource)) {
        cleanSource = cleanSource.replace(/^もし[\\s\\u3000]*/, '');
        moshi = true;
      }
      const compound=cleanSource.match(/^(.+?)(ならば|なら|ので|から|だから|けれども|けれど|ときに|とき|時に|時|たら|だら|ば|ても|でも)(?:[、,]|\\s+)(.+)$/);
      if(compound){
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
      '''

content = content[:part_start] + new_compound + content[part_tail:]

# 5. Update trailingCompound
trailing_start = content.find('const trailingCompound = key(cleanSource).match(/^(.+?)(なら')
if trailing_start == -1:
    trailing_start = content.find('const trailingCompound = key(source).match(/^(.+?)(なら')
trailing_end = content.find('const direct=full(source);if(direct)return {...direct,source};')
assert trailing_start != -1 and trailing_end != -1, 'trailingCompound boundaries not found'

new_trailing = '''const trailingCompound = key(cleanSource).match(/^(.+?)(ならば|なら|ので|から|だから|けれども|けれど|ときに|とき|時に|時|たら|だら|ば|ても|でも)$/);
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
      '''

content = content[:trailing_start] + new_trailing + content[trailing_end:]

# 6. Update modal notes and modal realization in part
notes_check_start = content.find('if(feature && ![\'行為\',\'指針\'].includes(feature))')
assert notes_check_start != -1, 'notes_check not found'
notes_check_end = content.find('try {args=parsedArgs(body,form||{});}', notes_check_start)

new_notes_check = '''if(feature && !['行為','指針'].includes(feature)) {
        const isSupportedModal = ['希望','可能','推量'].some(m => feature.includes(m));
        if(!isSupportedModal) notes.push(feature+'の表現は未対応。意味を省略せず保持します。');
      }
      '''

content = content[:notes_check_start] + new_notes_check + content[notes_check_end:]

blocked_start = content.find('if(feature && form) {')
if blocked_start == -1:
    blocked_start = content.find('const isModal = [\'希望\',\'可能\',\'推量\'].some(m => feature.includes(m));')
if blocked_start == -1:
    blocked_start = content.find('if(feature || !form)return {source,text:fragments,state:\'blocked\',meaning,notes:[...notes,...(!form?[\'時制・相の組み合わせは未対応です。\']:[]')
blocked_end = content.find('if(!args.el || alias && !alias.complete', blocked_start)
assert blocked_start != -1 and blocked_end != -1, 'blocked boundaries not found'

new_blocked = '''if(feature && form) {
        if(feature.includes('可能') && !form.suffix) {
          form = {...form, suffix: 'ar', prefixes: feature.includes('過去') ? [...form.prefixes, 'fe'] : form.prefixes};
          if(feature.includes('否定') && !form.prefixes.includes('ne')) form.prefixes = [...form.prefixes, 'ne'];
        } else if(feature.includes('希望') && !form.suffix) {
          form = {...form, suffix: 'ast', prefixes: feature.includes('過去') ? [...form.prefixes, 'fe'] : form.prefixes};
          if(feature.includes('否定') && !form.prefixes.includes('ne')) form.prefixes = [...form.prefixes, 'ne'];
        } else if(feature.includes('推量') && !form.prefixes.includes('se')) {
          form = {...form, prefixes: ['se', ...form.prefixes]};
          if(feature.includes('過去') && !form.prefixes.includes('fe')) form.prefixes = [...form.prefixes, 'fe'];
          if(feature.includes('否定') && !form.prefixes.includes('ne')) form.prefixes = [...form.prefixes, 'ne'];
        }
      }
      const isModal = ['希望','可能','推量'].some(m => feature.includes(m));
      if(isModal && form) {
        try {
          const updatedMeaning = meaningOf(form ? {...form, ending} : null, args, question, feature);
          const candidate = realize(updatedMeaning);
          return {
            source,
            text: candidate,
            state: choices.confirmed ? 'complete' : 'candidate',
            candidate,
            meaning: updatedMeaning,
            senseOptions,
            verbOptions,
            alignment: updatedMeaning.alignment,
            notes: [...notes, feature + 'のモダリティ表現を適用。Nebulithの格・項構造を検証。', ...extensionNotes(form)]
          };
        } catch(e) {
          return {source, text: fragments, state: 'blocked', notes: [...notes, e.message]};
        }
      }
      if(feature || !form)return {source,text:fragments,state:'blocked',meaning,notes:[...notes,...(!form?['時制・相の組み合わせは未対応です。']:[]奋)],alignment:argumentRows(args)};
      '''.replace('奋', '')

content = content[:blocked_start] + new_blocked + content[blocked_end:]

with open('web/incremental.js', 'w', encoding='utf-8') as f:
    f.write(content)

print('Successfully applied Sprint 1 enhancements with longest-match preference!')
