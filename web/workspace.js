/* Local data only. All profile writes use one localStorage key. */
(function(global){
  'use strict';
  const PROFILE='neb_profile_v1';
  const KEYS=['neb_theme','neb_favorites','neb_feedback_queue','neb_editor_draft','neb_session_v1','neb_font_size','neb_split','neb_history','neb_astral_font'];
  const statuses=['untriaged','investigating','implemented','review','held'];
  const causes=['unknown','vocabulary','inflection','syntax','meaning','incomplete'];
  const stable=v=>Array.isArray(v)?v.map(stable):v&&typeof v==='object'?Object.fromEntries(Object.keys(v).sort().filter(k=>!['__proto__','constructor','prototype'].includes(k)).map(k=>[k,stable(v[k])])):v;
  function hash(text){let n=2166136261;for(const c of text)n=Math.imul(n^c.charCodeAt(0),16777619);return (n>>>0).toString(16);}
  function choices(raw={},allowSegments=true) {
    if(!raw||typeof raw!=='object'||Array.isArray(raw))throw Error('解釈情報が不正です。');
    const result={};
    for(const k of ['subject','verb','possession','sense'])if(typeof raw[k]==='string'&&raw[k].length<=200)result[k]=raw[k];
    if(allowSegments&&raw.bySegment&&typeof raw.bySegment==='object'&&!Array.isArray(raw.bySegment)){
      const entries=Object.entries(raw.bySegment);if(entries.length>100)throw Error('保存する文の選択が多すぎます。');
      result.bySegment=Object.fromEntries(entries.filter(([k])=>k.length<=5000&&!['__proto__','constructor','prototype'].includes(k)).map(([k,v])=>[k,choices(v,false)]));
    }
    result.confirmed=false;return result;
  }
  function session(raw={}) {
    if(raw.schemaVersion!==undefined&&raw.schemaVersion!==1)throw Error('未対応の下書き形式です。');
    if(typeof raw.text!=='string'||raw.text.length>1000000)throw Error('翻訳下書きが不正です。');
    if(!['ja','en','neb'].includes(raw.srcLang)||!['ja','en','neb'].includes(raw.dstLang))throw Error('翻訳方向が不正です。');
    return {schemaVersion:1,text:raw.text,srcLang:raw.srcLang,dstLang:raw.dstLang,choices:choices(raw.choices),updatedAt:raw.updatedAt||''};
  }
  function classify(item){
    const text=item.context||'';
    if(/入力待ち|主語未指定|続きの入力/.test(text))return 'incomplete';
    if(/候補|解釈|語義|選択/.test(text))return 'meaning';
    if(item.type==='word'||/未知語/.test(text))return 'vocabulary';
    if(/時制|活用|相の組み合わせ/.test(text))return 'inflection';
    if(/文型|項構造|構文/.test(text))return 'syntax';return 'unknown';
  }
  function feedbackKey(r){
    const withoutConfirmation=v=>v&&typeof v==='object'?Object.fromEntries(Object.entries(v).filter(([k])=>k!=='confirmed').map(([k,value])=>[k,withoutConfirmation(value)])):v;
    const semantic=withoutConfirmation(r.interpretation?.choices||{});
    return JSON.stringify([r.type,r.lang,r.text.trim(),stable(semantic)]);
  }
  function normalizeQueue(raw,source={name:'取込'}) {
    if(raw?.schemaVersion!==undefined&&raw.schemaVersion!==1)throw Error('未対応の記録形式です。');
    const rows=Array.isArray(raw)?raw:raw?.queue;
    if(!Array.isArray(rows)||rows.length>5000)throw Error('記録は5,000件以内の配列にしてください。');
    return rows.map((r,index)=>{
      if(!r||!['word','sentence'].includes(r.type)||!['ja','en','neb','search'].includes(r.lang)||typeof r.text!=='string'||!r.text.trim()||r.text.length>20000)throw Error((index+1)+'件目の記録が不正です。');
      if(r.count!==undefined&&(!Number.isSafeInteger(r.count)||r.count<1||r.count>5000000000))throw Error('記録回数が不正です。');
      if(r.interpretation!==undefined&&(!r.interpretation||typeof r.interpretation!=='object'||Array.isArray(r.interpretation)))throw Error('解釈情報が不正です。');
      const originalId=typeof r.id==='string'?r.id.slice(0,300):hash(JSON.stringify([source,index,r.text]));
      const identity=feedbackKey(r);
      if(r.origins!==undefined&&(!Array.isArray(r.origins)||r.origins.length>5000))throw Error('元記録情報が不正です。');
      const origins=Array.isArray(r.origins)&&r.origins.length?r.origins.map(o=>{
        if(!o||typeof o.key!=='string'||o.key.length>1000||!Number.isSafeInteger(o.count)||o.count<1||o.count>1000000)throw Error('元記録情報が不正です。');
        return {key:o.key,count:o.count,requestId:String(o.requestId||'').slice(0,300),source:typeof o.source==='object'&&o.source?{name:String(o.source.name||'').slice(0,300),sha256:String(o.source.sha256||'').slice(0,64)}:source};
      }):[{key:JSON.stringify([r.type,r.lang,originalId]),count:r.count||1,requestId:originalId,source}];
      return {id:'req_'+hash(identity)+'_'+hash(identity.split('').reverse().join('')),type:r.type,lang:r.lang,text:r.text.trim(),context:typeof r.context==='string'?r.context.slice(0,20000):'',
        ...(r.interpretation?{interpretation:stable(r.interpretation)}:{}),origins,count:origins.reduce((n,o)=>n+o.count,0),createdAt:typeof r.createdAt==='string'?r.createdAt:new Date().toISOString(),
        status:statuses.includes(r.status)?r.status:'untriaged',cause:causes.includes(r.cause)?r.cause:classify(r)};
    });
  }
  function mergeQueue(existing,incoming,source){
    const rows=normalizeQueue(existing,{name:'既存記録'}),added=normalizeQueue(incoming,source);const result=[];
    const index=new Map();let newItems=0;
    for(const r of [...rows,...added]){
      const identity=feedbackKey(r);
      const target=index.get(identity);
      if(!target){const copy=JSON.parse(JSON.stringify(r));index.set(identity,copy);result.push(copy);if(result.length>rows.length||!rows.some(x=>x.id===r.id))newItems++;continue;}
      const origins=new Map(target.origins.map(o=>[o.key,o]));
      for(const o of r.origins){const old=origins.get(o.key);if(!old||o.count>old.count)origins.set(o.key,o);}
      target.origins=[...origins.values()];target.count=target.origins.reduce((n,o)=>n+o.count,0);
      if(!target.context)target.context=r.context;
    }
    if(result.length>5000)throw Error('統合後の記録が5,000件を超えます。');
    return {queue:result,newItems,imported:added.length};
  }
  function validateValues(values){
    if(!values||typeof values!=='object'||Array.isArray(values))throw Error('保存データが不正です。');
    for(const [k,v] of Object.entries(values))if(!KEYS.includes(k)||v!==null&&typeof v!=='string')throw Error('未対応の保存項目です。');
    if(values.neb_theme&&!['light','dark'].includes(values.neb_theme))throw Error('テーマが不正です。');
    for(const key of ['neb_favorites','neb_history'])if(values[key]){const a=JSON.parse(values[key]);if(!Array.isArray(a)||a.length>10000||a.some(x=>typeof x!=='string'||x.length>200))throw Error('語の一覧が不正です。');}
    if(values.neb_feedback_queue)normalizeQueue(JSON.parse(values.neb_feedback_queue));
    if(values.neb_session_v1)session(JSON.parse(values.neb_session_v1));
    for(const [key,min,max] of [['neb_font_size',20,64],['neb_split',25,75]])if(values[key]&&(!Number.isFinite(Number(values[key]))||Number(values[key])<min||Number(values[key])>max))throw Error('表示設定が不正です。');
    if(values.neb_editor_draft&&values.neb_editor_draft.length>1000000)throw Error('筆記下書きが大きすぎます。');
    return values;
  }
  function backup(raw){
    if(raw?.schemaVersion!==1||raw?.source!=='Nebulith Studio Backup')throw Error('未対応のバックアップ形式です。');
    return validateValues(raw.values);
  }
  function createStore(getStorage,onError=()=>{}){
    let loaded=false,values={},revision=0,recovery={},blocked=false;
    function load(){if(loaded)return;loaded=true;try{
      const storage=getStorage(),raw=storage.getItem(PROFILE);
      if(raw){try{const p=JSON.parse(raw);if(p.schemaVersion!==1||!Number.isSafeInteger(p.revision)||p.revision<0||!p.values)throw Error('保存形式が未対応です。');values=p.values;revision=p.revision;recovery=p.recovery||{};validateValues(values);}catch(e){blocked=true;recovery.profile=raw;throw e;}}
      else for(const key of KEYS){const v=storage.getItem(key);if(v!==null)values[key]=v;}
    }catch(e){onError('保存データを読み込めません：'+e.message);}}
    function commit(next,repair=false){load();try{
      if(blocked&&!repair)throw Error('保存データに問題があります。バックアップ後に有効なデータを復元してください。');
      const storage=getStorage(),raw=storage.getItem(PROFILE);
      if(!repair&&!raw&&revision>0)throw Error('別のタブで保存データが削除されました。再読込してください。');
      if(!repair&&raw&&JSON.parse(raw).revision!==revision)throw Error('別のタブで保存されました。入力をバックアップしてから再読込してください。');
      const profile={schemaVersion:1,revision:revision+1,values:next,recovery};
      storage.setItem(PROFILE,JSON.stringify(profile));values=next;revision++;blocked=false;return true;
    }catch(e){onError('保存できません：'+e.message);return false;}}
    return {getItem(key){load();return typeof values[key]==='string'?values[key]:null;},setItem(key,value){if(!KEYS.includes(key))throw Error('保存キーが不正です。');load();return commit({...values,[key]:String(value)});},removeItem(key){load();return commit({...values,[key]:null});},
      json(key,fallback){load();try{const raw=values[key];return raw?JSON.parse(raw):fallback;}catch(e){recovery[key]=values[key];onError('保存データが破損しています：'+key+'。元データは保持します。');return fallback;}},
      snapshot(){load();return {schemaVersion:1,source:'Nebulith Studio Backup',values:{...values},recovery:{...recovery},exportedAt:new Date().toISOString()};},
      restore(next){validateValues(next);return commit({...next},true);}};
  }
  global.NebulithWorkspace={choices,session,normalizeQueue,mergeQueue,feedbackKey,classify,backup,createStore,statuses,causes};
})(globalThis);
