const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
const ctx={};vm.createContext(ctx);
for(const file of ['web/data.js','web/incremental.js'])vm.runInContext(fs.readFileSync(file,'utf8'),ctx);
vm.runInContext(`globalThis.engine=createIncrementalTranslator(VOCAB,GRAMMAR_FRAMES,INPUT_RULES.aliases,CANON.map(c=>({ja:c.ja,ja_variants:[c.ja],neb:c.neb})),TRANSLATION_EXTENSIONS)`,ctx);
for(const [source,expected] of [
  ['私は赤い星を観測します。','Vyrel el mi ia vyr pyrin.'],
  ['私はあなたの家へ歩く。','Poran el mi to govan en ti.'],
  ['私は星を観測しなかった。','Fe ne vyrel el mi ia vyr.'],
  ['私は星を観測しますか？','Vyrel el mi ia vyr ka?'],
  ['私は家で食べます。','Neran el mi uo govan.'],
  ['あなたたちは歩く。','Poran el tiin.'],
  ['彼らは歩く。','Poran el riin.']]){
  const actual=ctx.engine.analyze(source,{});
  assert.equal(actual.complete,true,source+': '+JSON.stringify(actual));
  assert.equal(actual.text,expected,source);
}
for(const source of ['私はテスト未知語を観測する。','私は家を歩く。','私は家へ食べる。','私は望遠鏡で星を観測する。','歩く。','私は家へ歩く。続く文は未対応のはず。']){
  assert.equal(ctx.engine.analyze(source,{}).complete,false,source);
}
console.log('PASS: Web grammar generation, pronouns, negation, question, frames and safe rejection');

const resolutions=JSON.parse(fs.readFileSync('data/feedback_resolutions.json','utf8'));
for(const item of resolutions.items){
  const initial=ctx.engine.analyze(item.input,{});
  assert.equal(initial.segments[0].state,item.initialState,item.input+' initial');
  assert.equal(initial.recordable,false,item.input);
  const actual=ctx.engine.analyze(item.input,item.choices||{});
  assert.equal(actual.segments[0].state,item.state,item.input);
  assert.equal(actual.text,item.output,item.input);
  assert.ok(actual.notes.some(n=>n.includes('未監査')||n.includes('追加')));
  assert.ok(actual.segments[0].alignment.length>0);
  if(item.newRoot)assert.ok(actual.segments[0].alignment.some(a=>a.dst===item.newRoot));
}
for(const [src,out] of [['私はあなたが嫌いではない','Ne nyrcan el mi ia ti.'],['私があなたを殺さなかった','Fe ne kyrdan el mi ia ti.']])assert.equal(ctx.engine.analyze(src,{}).text,out);
for(const src of ['私は殺す','私は家へ殺す','私はあなたが嫌いかもしれない'])assert.equal(ctx.engine.analyze(src,{}).complete,false);
const rows=ctx.engine.analyze('私は赤い星を観測した',{}).segments[0].alignment;
for(const [src,dst] of [['赤い','pyrin'],['星','vyr'],['を','ia'],['観測した','fe vyrel']])assert.ok(rows.some(a=>a.src===src&&a.dst===dst),src);
const possession=ctx.engine.analyze('私はあなたの家へ歩く',{}).segments[0].alignment;
assert.ok(possession.some(a=>a.src==='の'&&a.dst==='en'));
const draft=ctx.engine.analyze('赤い星を',{}).segments[0];
assert.equal(draft.state,'draft');assert.ok(draft.alignment.some(a=>a.src==='星'&&a.dst==='vyr'));
const inferred=ctx.engine.analyze('赤い星を見る',{subject:'私',verb:'観測する'}).segments[0];
assert.equal(inferred.state,'candidate');assert.ok(inferred.alignment.some(a=>a.src==='私'&&a.role.includes('補完')));
assert.ok(inferred.alignment.some(a=>a.src==='見る'&&a.dst==='vyrel'));
console.log('PASS: recovered requests, provisional vocabulary, morphology and word/phrase alignment');

for(const text of ['あなたが嫌い。','あなたとともに生きる','未来を見る','私は未来を見る','私とあなたの物語']){
  const result=ctx.engine.analyze(text,{});
  assert.equal(result.complete,false,text+' must wait for interpretation');
  assert.equal(result.recordable,false,text+' is now supported with choices');
}
const ownership=ctx.engine.analyze('私とあなたの物語',{possession:'shared'});
assert.equal(ownership.segments[0].state,'candidate');
assert.equal(ctx.engine.analyze('私とあなたの物語',{possession:'separate',confirmed:true}).text,'mi ul soralen en ti');
assert.equal(ctx.engine.analyze('未来を見る',{subject:'私',verb:'予見する'}).segments[0].state,'candidate');
assert.equal(ctx.engine.analyze('私は未来を見ない',{verb:'予見する',confirmed:true}).text,'Ne vyrcen el mi ia sehvan.');
assert.equal(ctx.engine.analyze('私は未来を見た',{verb:'展望する',confirmed:true}).text,'Fe valcyn el mi ia sehvan.');
assert.equal(ctx.engine.analyze('私は星を見る',{verb:'予見する',confirmed:true}).complete,false);
assert.equal(ctx.engine.analyze('あなたが嫌い。',{subject:'彼／彼女',confirmed:true}).text,'Nyrcan el ri ia ti.');
for(const text of ['私はあなたと共に生きる','私はあなたと一緒に生きる'])assert.equal(ctx.engine.analyze(text,{}).text,'Zyvel el mi ku ti.');
assert.equal(ctx.engine.analyze('私は過去を思い出さなかった',{}).text,'Fe ne sorvel el mi ia fehvan.');
assert.equal(ctx.engine.analyze('私は未知の過去を思い出す',{}).complete,false);
console.log('PASS: second feedback batch, explicit scope/subject/meaning choices and preserved tense/negation');
