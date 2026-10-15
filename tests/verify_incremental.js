const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
const ctx={};vm.createContext(ctx);
for(const file of ['web/data.js','web/incremental.js'])vm.runInContext(fs.readFileSync(file,'utf8'),ctx);
const fixtures=JSON.parse(fs.readFileSync('data/translation_input_fixtures.json','utf8'));
vm.runInContext(`globalThis.engine=createIncrementalTranslator(VOCAB,GRAMMAR_FRAMES,INPUT_RULES.aliases,CANON.map(c=>({ja:c.ja,ja_variants:[c.ja],neb:c.neb})),TRANSLATION_EXTENSIONS)`,ctx);
for(const f of fixtures){
  const actual=ctx.engine.analyze(f.input,f.choices);
  assert.deepEqual(Array.from(actual.segments,s=>s.state),f.states,f.input+': '+JSON.stringify(actual));
  assert.equal(actual.recordable,f.recordable,f.input);
  if(f.states.every(s=>s==='complete'))assert.equal(actual.complete,true,f.input);
}
const output=ctx.engine.analyze('私は星を見ない',{verb:'観測する',confirmed:true});
assert.match(output.text,/^Ne vyrel /,'negation must survive');
const hope=ctx.engine.analyze('赤い星を見ていたい',{subject:'私',verb:'観測する',confirmed:true});
assert.equal(hope.complete,false);assert(hope.notes.some(n=>n.includes('希望')));
assert.equal(ctx.engine.analyze('赤い星を').recordable,false);
console.log(`PASS: ${fixtures.length} shared incremental fixtures, negation, hope and draft queue policy`);

for (const [input, root] of [['私','mi'],['あなた','ti'],['彼女','ri'],['私たち二人','miel'],['私たち','miin'],['あなたたち','tiin'],['あの二人','riel'],['彼ら','riin']]) {
  const result=ctx.engine.analyze(input,{});
  assert.equal(result.text,root,input); assert.equal(result.segments[0].state,'phrase');
}
assert.equal(ctx.engine.analyze('私たちは歩く',{}).text,'Poran el miin.');
