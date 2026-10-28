const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
function context(incremental=true){const c={};vm.createContext(c);for(const f of ['data','bidirectional',...(incremental?['incremental']:[])])vm.runInContext(fs.readFileSync(`web/${f}.js`,'utf8'),c);if(incremental)vm.runInContext('globalThis.engine=createIncrementalTranslator(VOCAB,GRAMMAR_FRAMES,INPUT_RULES.aliases,[],TRANSLATION_EXTENSIONS)',c);return c;}
const c=context(),bi=c.NebulithBidirectionalEngine;
// Independent literal expectations from specification 6.2, not generated round trips.
for(const [surface,root] of [['kirol','kiran'],['klovol','klovan'],['porol','poran'],['syndirol','syndir'],['kylol','kylen'],['falunol','falun']]){
 const parsed=bi.parseNebulithClause(surface+' el mi');assert.equal(parsed.verbInfo.r,root);assert.equal(parsed.aspectSuffix.suffix,'ol');
}
for(const [source,target] of [['私は歩き終える。','Porol el mi.'],['私は歩き終えた。','Fe porol el mi.'],['私は歩き終えない。','Ne porol el mi.'],['私は歩き終えなかった。','Fe ne porol el mi.']]){
 const r=c.engine.analyze(source,{confirmed:true});assert.equal(r.complete,true,JSON.stringify(r));assert.equal(r.text,target);assert.equal(r.segments[0].meaning.predicate.root,'poran');assert.ok(r.segments[0].alignment.some(a=>a.dst.toLowerCase().includes('porol')));
}
for(const instance of [c,context(false)]){
 const b=instance.NebulithBidirectionalEngine;
 assert.equal(b.translateNebulith('Porol el mi.','ja').text,'私は 歩き終える.');
 assert.equal(b.translateNebulith('Fe ne porol el mi.','en').text,'I did not finish walking.');
 assert.equal(b.translateEnglishToNebulith('I finish walking').text,'Porol el mi.');
 assert.equal(b.translateNebulith('Poranfar el mi.','ja').success,false);
}
// Lexical far strings are genuine roots, not obsolete aspect markers.
for(const root of ['farven','novfar'])assert.equal(bi.parseNebulithClause(root+' el mi').verbInfo.r,root);
for(const [source,kind] of [['私は水を飲み終えていない。','noncompletion'],['私は水を飲み終わっていない。','noncompletion'],['私は水を飲んだことがない。','experiential-negative'],['私は水を飲んだことがありません。','experiential-negative'],['私は水を飲んだことがなかった。','experiential-negative']]){
 const r=c.engine.analyze(source,{confirmed:true});assert.equal(r.complete,false);assert.equal(r.recordable,true);assert.equal(r.segments[0].text,'');assert.equal(r.segments[0].source,source);assert.equal(r.segments[0].meaning.modalities[0].kind,kind);
}
for(const source of ['私は水を飲んだことがないかもしれない。','私は水を飲み終えていない必要がある。'])assert.equal(c.engine.analyze(source,{confirmed:true}).complete,false);
const source='私はまだ水を飲んでいない。';
assert.equal(c.engine.analyze(source,{confirmed:true}).complete,false);
assert.equal(c.engine.analyze(source,{reading:'progressive-negative'}).segments[0].state,'candidate');
const chosen=c.engine.analyze(source,{reading:'progressive-negative',confirmed:true});assert.equal(chosen.text,'Divan ne di bion el mi ia daris.');assert.equal(chosen.segments[0].source,source);assert.ok(chosen.segments[0].alignment.some(a=>a.src==='飲んでいない'));
assert.equal(c.engine.analyze(source,{reading:'unrealized-negative',confirmed:true}).complete,false);
// Actual dictionary collisions cannot be inverted safely.
for(const word of ['zyvelol','dolarol','kirasol','morkol'])assert.equal(bi.translateNebulith(word+' el mi.','ja').success,false,word);
// Synthetic vowel and collision/shadow fixtures protect future dictionary additions.
for(const [root,surface] of [['testa','testol'],['teste','testol'],['testi','testol'],['testo','testol'],['testu','testol'],['testy','testol']]){
 bi.configure([{id:99001,r:root,p:'動',m:'歩く',en:'walk'}],[]);assert.equal(bi.parseNebulithClause(surface+' el mi').verbInfo.r,root);
}
for(const extra of [{id:99001,r:'poren',p:'動',m:'架空動作',en:'test'},{id:99002,r:'porol',p:'名',m:'架空名詞',en:'test'}]){
 c.extra=extra;vm.runInContext('globalThis.modified=[...VOCAB,extra];NebulithBidirectionalEngine.configure(modified,[]);globalThis.collisionEngine=createIncrementalTranslator(modified,GRAMMAR_FRAMES,INPUT_RULES.aliases,[],TRANSLATION_EXTENSIONS)',c);
 assert.equal(bi.translateNebulith('Porol el mi.','ja').success,false);
 assert.equal(bi.translateEnglishToNebulith('I finish walking').success,false);
 assert.equal(c.collisionEngine.analyze('私は歩き終える。',{confirmed:true}).complete,false);
}
console.log('PASS: specification perfective forms, tense/polarity, reverse fallback, lexical/collision safety, incomplete and experiential negatives');
