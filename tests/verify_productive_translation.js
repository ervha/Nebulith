const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
const ctx={};vm.createContext(ctx);
for(const f of ['web/data.js','web/incremental.js'])vm.runInContext(fs.readFileSync(f,'utf8'),ctx);
vm.runInContext('globalThis.engine=createIncrementalTranslator(VOCAB,GRAMMAR_FRAMES,INPUT_RULES.aliases,[],TRANSLATION_EXTENSIONS)',ctx);
const fixtures=[
 ['私は水を飲んだ','Fe bion el mi ia daris.'],
 ['私は水を飲みませんでした','Fe ne bion el mi ia daris.'],
 ['あなたは物語を書いている','Di kiras el ti ia soralen.'],
 ['私は書いていなかった','Fe ne di kiras el mi.'],
 ['私たちは森で働きます','Dolar el miin uo velom.'],
 ['私はあなたに物語を贈った','Fe zelvan el mi ia soralen al ti.'],
 ['私はあなたから物語を受け取る','Martan el mi ia soralen va ti.'],
 ['私は家に暮らす','Taran el mi uo govan.'],
 ['私は家から走る','Kupan el mi va govan.'],
 ['私はあなたと歌う','Cival el mi ku ti.'],
 ['私は水で家を洗う','Serdar el mi ia govan de daris.'],
 ['私は家へ走り始める','Kupanast el mi to govan.'],
 ['私とあなたは走る','Kupan el mi ul ti.'],
 ['星は赤い','Relen el vyr ia pyrin.'],
 ['水は冷たかった','Fe relen el daris ia kyrani.'],
 ['水は冷たくない','Ne relen el daris ia kyrani.'],
 ['わたしは眠ります','Tymis el mi.']
];
for(const [input,output] of fixtures){const r=ctx.engine.analyze(input,{});assert.equal(r.complete,true,input+': '+JSON.stringify(r));assert.equal(r.text,output,input);}
// Independent Japanese inflection witnesses, covering every configured conjugation family.
for(const [lemma,kind,past,progress,negative] of [['書く','く','書いた','書いている','書かない'],['泳ぐ','ぐ','泳いだ','泳いでいる','泳がない'],['話す','す','話した','話している','話さない'],['待つ','つ','待った','待っている','待たない'],['飛ぶ','ぶ','飛んだ','飛んでいる','飛ばない'],['飲む','む','飲んだ','飲んでいる','飲まない'],['走る','る','走った','走っている','走らない'],['歌う','う','歌った','歌っている','歌わない'],['食べる','ichidan','食べた','食べている','食べない'],['同期する','suru','同期した','同期している','同期しない'],['来る','kuru','来た','来ている','来ない']]){
  const forms=ctx.nebulithJapaneseForms(lemma,kind).map(f=>f.ending);for(const word of [past,progress,negative])assert.ok(forms.includes(word),word);
}
const patterns=JSON.parse(fs.readFileSync('data/translation_patterns.json','utf8'));
let combinations=0;
for(const v of patterns.verbs)for(const form of ctx.nebulithJapaneseForms(v.lemma,v.conjugation))for(const subject of ['私','あなた','私たち']){
  const object=v.id===30006?'過去を':[30007,30008].includes(v.id)?'未来を':'';
  const input=subject+'は'+object+form.ending;
  const result=ctx.engine.analyze(input,{});
  if(form.feature){assert.equal(result.complete,false,input+' must preserve desire');assert.ok(result.notes.some(n=>n.includes('希望')),input);}
  else {assert.equal(result.complete,true,input+': '+JSON.stringify(result));assert.ok(result.segments[0].alignment.length,input);}
  combinations++;
}
const ambiguous=ctx.engine.analyze('空は美しい',{});assert.equal(ambiguous.complete,false);assert.equal(ambiguous.recordable,false);
assert.ok(ambiguous.segments[0].senseOptions.length>1);
for(const option of ambiguous.segments[0].senseOptions){
  assert.equal(ctx.engine.analyze('空は美しい',{sense:option.value}).segments[0].state,'candidate');
  const selected=ctx.engine.analyze('空は美しい',{sense:option.value,confirmed:true});
  assert.equal(selected.complete,true);assert.ok(selected.text.includes('ia '+option.root));
}
for(const input of ['私は未知語を飲む','私は水を飲みたい','私は水を飲むかもしれない','私は物語を読む','水は冷たくて赤い'])assert.equal(ctx.engine.analyze(input,{}).complete,false,input);
console.log(`PASS: ${fixtures.length} independent sentences, 11 conjugation families, ${combinations} productive combinations, sense selection and refusal to discard meaning`);
const examples=JSON.parse(fs.readFileSync('data/usage_examples.json','utf8')).examples;
assert.equal(examples.length,24);
assert.equal(new Set(examples.map(e=>e.id)).size,examples.length);
for(const example of examples){
  const result=ctx.engine.analyze(example.japanese,example.choices);
  assert.equal(result.text,example.nebulith,example.id+': '+JSON.stringify(result));
  assert.equal(result.segments[0].state,example.state,example.id);
  assert.ok(example.english&&example.title&&example.note,example.id);
  if(Object.keys(example.choices).length)assert.equal(ctx.engine.analyze(example.japanese,{}).complete,false,example.id+' must not bypass choices');
}
console.log('PASS: 24 displayed learning examples and explicit interpretation conditions');
