const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
const ctx={};vm.createContext(ctx);
for(const file of ['data','incremental','bidirectional'])vm.runInContext(fs.readFileSync('web/'+file+'.js','utf8'),ctx);
vm.runInContext('globalThis.engine=createIncrementalTranslator(VOCAB,GRAMMAR_FRAMES,INPUT_RULES.aliases,[],TRANSLATION_EXTENSIONS)',ctx);
// Expected translations are specified independently of conjugation-table generation.
const goldens=[
 ['私は水を飲んでる。','Di bion el mi ia daris.','progressive','unmarked'],
 ['あなたは水を飲んでた。','Fe di bion el ti ia daris.','progressive','past'],
 ['私は水を飲んでます。','Di bion el mi ia daris.','progressive','unmarked'],
 ['あなたは水を飲んでました。','Fe di bion el ti ia daris.','progressive','past'],
 ['私はスープを食べてる。','Di neran el mi ia darel.','progressive','unmarked'],
 ['あなたはスープを食べてた。','Fe di neran el ti ia darel.','progressive','past'],
 ['私は歩いてる。','Di poran el mi.','progressive','unmarked'],
 ['あなたは歩いてた。','Fe di poran el ti.','progressive','past'],
 ['私は星を観測してる。','Di vyrel el mi ia vyr.','progressive','unmarked'],
 ['あなたは星を観測してた。','Fe di vyrel el ti ia vyr.','progressive','past'],
 ['私はあなたに本を譲ってる。','Di renantal el mi ia pamel al ti.','progressive','unmarked'],
 ['あなたは私に本を譲ってた。','Fe di renantal el ti ia pamel al mi.','progressive','past'],
 ['私は水を飲みたくないです。','Ne bionast el mi ia daris.','desiderative','unmarked'],
 ['あなたは水を飲みたくなかったです。','Fe ne bionast el ti ia daris.','desiderative','past'],
 ['私はあなたに本を譲りたくないです。','Ne renantalast el mi ia pamel al ti.','desiderative','unmarked'],
 ['あなたは私に本を譲りたくなかったです。','Fe ne renantalast el ti ia pamel al mi.','desiderative','past']
];
for(const [source,expected,aspect,tense] of goldens){
 const pending=ctx.engine.analyze(source);assert.equal(pending.complete,false,source);
 assert.equal(pending.segments[0].state,'candidate',JSON.stringify(pending));
 const result=ctx.engine.analyze(source,{confirmed:true});
 assert.equal(result.complete,true,source+JSON.stringify(result));assert.equal(result.text,expected,source);
 const meaning=result.segments[0].meaning;assert.equal(meaning.aspect,aspect);assert.equal(meaning.tense,tense);
 if(aspect==='desiderative')assert.equal(meaning.modalities[0].negated,true,source);
 else assert.equal(meaning.negative,false,source);
 assert.equal(meaning.arguments.el.nrs,source.startsWith('私は')?'mi':'ti');
 for(const lang of ['ja','en'])assert.equal(ctx.NebulithBidirectionalEngine.translateNebulith(expected,lang).success,true,expected+' '+lang);
}
const examples=JSON.parse(fs.readFileSync('data/roadmap_lexical_rules.json','utf8')).examples.filter(row=>row.id.startsWith('CV-'));
assert.equal(examples.length,14);
for(const example of examples){
 assert.ok(goldens.some(([ja,neb])=>ja===example.ja&&neb===example.neb),'app example must have an independent golden');
 assert.equal(ctx.engine.analyze(example.ja,{confirmed:true}).text,example.neb,example.id);
}
for(const [source,expected] of [
 ['私はゆっくり水を飲んでる。','Moril di bion el mi ia daris.'],
 ['私は少し水を飲みたい。','Vyntul bionast el mi ia daris.']
]){
 const pending=ctx.engine.analyze(source);assert.equal(pending.complete,false,source);
 const r=ctx.engine.analyze(source,{confirmed:true});assert.equal(r.complete,true,JSON.stringify(r));assert.equal(r.text,expected);
 assert.ok(r.segments[0].alignment.some(row=>row.dst===expected.split(' ')[0].toLowerCase()),source);
}
const adverbScope=ctx.engine.analyze('私はゆっくり水を飲むなら、あなたは歩く。',{confirmed:true});
assert.equal(adverbScope.complete,false);assert.ok(adverbScope.notes.some(note=>note.includes('どの節')));
for(const source of ['あなたは水を飲んでください。','あなたは私に本を譲ってください。']){
 const r=ctx.engine.analyze(source,{confirmed:true});assert.equal(r.complete,false,source);
 assert.ok(r.notes.some(n=>n.includes('依頼')&&n.includes('未対応')),JSON.stringify(r));
 assert.equal(r.segments[0].meaning.modalities[0].kind,'request');
 assert.equal(r.segments[0].meaning.modalities[0].realization,'not-defined');
 assert.equal(r.segments[0].fragments.map(f=>f.source).join(''),source);
}
// Swapping a person into the transferred-object role remains ambiguous even with a recipient.
for(const source of ['Renantal el mi ia ti al ri.','Renantal el mi ia pamel ul ti al ri.','Renantal el mi ia ti ul pamel al ri.'])for(const lang of ['ja','en']){
 const r=ctx.NebulithBidirectionalEngine.translateNebulith(source,lang);assert.equal(r.success,false,source);assert.ok(r.error.includes('取引'));
}
for(const source of ['私は彼にあなたを譲る。','私は彼に本とあなたを譲る。','私は彼にあなたと本を譲る。'])assert.equal(ctx.engine.analyze(source,{confirmed:true}).complete,false,source);
for(const source of ['私はあなたから水を飲む。','私はあなたより水を飲む。','水はスープから冷たい。','私はあなたから歩く。','私はあなたより歩く。','太陽は星から輝く。']){
 const r=ctx.engine.analyze(source,{confirmed:true});assert.equal(r.complete,false,source);
 assert.ok(r.notes.some(note=>note.includes('項構造')),JSON.stringify(r));
}
const comparison=ctx.engine.analyze('水はスープより冷たい。',{confirmed:true});
assert.equal(comparison.complete,true,JSON.stringify(comparison));assert.equal(comparison.text,'Relen el daris ia kyrani va darel.');
const comparisonReverse=ctx.NebulithBidirectionalEngine.translateNebulith(comparison.text,'ja');
assert.equal(comparisonReverse.success,true,JSON.stringify(comparisonReverse));assert.equal(comparisonReverse.text,'水は スープより 冷たい.');
for(const [source,target] of [
 ['太陽は星より輝く。','Falun el zohar va vyr.'],
 ['太陽は星より輝いた。','Fe falun el zohar va vyr.'],
 ['太陽は星より輝かない。','Ne falun el zohar va vyr.']
]){
 const r=ctx.engine.analyze(source,{confirmed:true});assert.equal(r.complete,true,source);assert.equal(r.text,target);
 for(const lang of ['ja','en'])assert.equal(ctx.NebulithBidirectionalEngine.translateNebulith(target,lang).success,true,target);
}
assert.equal(ctx.NebulithBidirectionalEngine.translateEnglishToNebulith('The sun shines more than the star.').text,'Falun el zohar va vyr.');
for(const source of ['I walk more than you.','I walk from house.','The sun shines from the star.','I drink water more than you.'])assert.equal(ctx.NebulithBidirectionalEngine.translateEnglishToNebulith(source).success,false,source);
for(const [source,expected] of [
 ['私は水を飲むかもしれない。','Se bion el mi ia daris.'],
 ['私は水を飲んだかもしれない。','Se fe bion el mi ia daris.'],
 ['私は水を飲まないかもしれない。','Se ne bion el mi ia daris.']
]){
 const r=ctx.engine.analyze(source,{confirmed:true});assert.equal(r.complete,true,source);assert.equal(r.text,expected);
 assert.equal(r.segments[0].meaning.tense,source.includes('飲んだ')?'past':'unmarked','uncertainty must not invent future tense');
}
for(const source of ['私は水を飲んで','私は水を飲ん','私は水を飲みたく','あなたに本を','私は知らない物を飲んでる。']){
 const r=ctx.engine.analyze(source,{confirmed:true});assert.equal(r.complete,false,source);
 assert.equal(r.segments[0].fragments.map(f=>f.source).join(''),source);
}
// An exact-source key prevents a confirmed choice from leaking into re-edited text.
const initial='水を飲んでる。',key=JSON.stringify([initial,0]);
const choices={bySegment:{[key]:{subject:'あなた',confirmed:true}}};
assert.equal(ctx.engine.analyze(initial+'私は歩く。',choices).complete,true);
assert.equal(ctx.engine.analyze('水を飲んでた。私は歩く。',choices).complete,false);
console.log('PASS: 16 literal conversation goldens, pending/confirmed states, request retention, recipient-role swaps, uncertainty tense, partial input and stale-choice checks.');
