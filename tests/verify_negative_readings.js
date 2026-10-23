const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
const ctx={};vm.createContext(ctx);
for(const file of ['data','incremental','workspace'])vm.runInContext(fs.readFileSync(`web/${file}.js`,'utf8'),ctx);
vm.runInContext('globalThis.engine=createIncrementalTranslator(VOCAB,GRAMMAR_FRAMES,INPUT_RULES.aliases,[],TRANSLATION_EXTENSIONS)',ctx);
const analyze=(source,choices={})=>ctx.engine.analyze(source,choices);
const reading='progressive-negative';
// Literal expectations: role, polarity, aspect and tense are independent of generated form tables.
const fixtures=[
 ['私は水を飲んでない。','Ne di bion el mi ia daris.','飲んでない','mi','daris',false],
 ['あなたは水を飲んでなかった。','Fe ne di bion el ti ia daris.','飲んでなかった','ti','daris',true],
 ['私は水を飲んでないです。','Ne di bion el mi ia daris.','飲んでないです','mi','daris',false],
 ['私は水を飲んでなかったです。','Fe ne di bion el mi ia daris.','飲んでなかったです','mi','daris',true],
 ['私はスープを食べてない。','Ne di neran el mi ia darel.','食べてない','mi','darel',false],
 ['私は歩いてない。','Ne di poran el mi.','歩いてない','mi',null,false],
 ['私は星を観測してない。','Ne di vyrel el mi ia vyr.','観測してない','mi','vyr',false],
 ['私はあなたに本を譲ってない。','Ne di renantal el mi ia pamel al ti.','譲ってない','mi','pamel',false],
 ['私はゆっくり水を飲んでない。','Moril ne di bion el mi ia daris.','飲んでない','mi','daris',false],
 ['私はまだ水を飲んでない。','Divan ne di bion el mi ia daris.','飲んでない','mi','daris',false],
 ['あなたは水を飲んでないか？','Ne di bion el ti ia daris ka?','飲んでない','ti','daris',false]
];
for(const [source,target,ending,subject,object,past] of fixtures){
 const pending=analyze(source,{confirmed:true});
 assert.equal(pending.complete,false,source);assert.equal(pending.segments[0].state,'draft');
 assert.equal(pending.segments[0].readingOptions.length,2);
 const candidate=analyze(source,{reading});assert.equal(candidate.complete,false,source);
 assert.equal(candidate.segments[0].state,'candidate');assert.equal(candidate.segments[0].candidate,target);
 const result=analyze(source,{reading,confirmed:true});assert.equal(result.complete,true,source+JSON.stringify(result));assert.equal(result.text,target);
 const segment=result.segments[0],meaning=segment.meaning;
 assert.equal(segment.source,source);assert.equal(meaning.negative,true);assert.equal(meaning.aspect,'progressive');
 assert.equal(meaning.tense,past?'past':'unmarked');assert.equal(meaning.arguments.el.nrs,subject);
 if(object)assert.equal(meaning.arguments.ia.nrs,object);
 assert.equal(meaning.predicate.source,ending);assert.equal(meaning.interpretation.source,ending);
 assert.ok(segment.alignment.some(row=>row.src===ending),'original contracted Japanese stays visible');
 assert.equal(meaning.modalities.length,0,'noncompletion must not be invented');
 const unresolved=analyze(source,{reading:'unrealized-negative',confirmed:true});
 assert.equal(unresolved.complete,false);assert.equal(unresolved.segments[0].text,'');assert.equal(unresolved.segments[0].state,'blocked');
 assert.equal(unresolved.segments[0].meaning.modalities[0].realization,'not-defined');assert.equal(unresolved.recordable,true);
}
assert.equal(analyze('あなたは水を飲んでないか？',{reading,confirmed:true}).segments[0].meaning.question,true);
assert.equal(analyze('私はあなたに本を譲ってない。',{reading,confirmed:true}).segments[0].meaning.arguments.al.nrs,'ti');
assert.equal(analyze('私は水を飲んでない。',{reading:'bad',confirmed:true}).complete,false);
for(const source of ['私は未知の飲み物を飲んでない。','私は星を歩いてない。','私は水を飲んでないかもしれない。','私は水を飲んでないこと。','私は水を飲んでない必要がある。','私は水を飲んでないので、あなたは歩く。'])
 assert.equal(analyze(source,{reading,confirmed:true}).complete,false,source);
for(const [lemma,kind,contraction] of [['書く','く','書いて'],['泳ぐ','ぐ','泳いで'],['話す','す','話して'],['待つ','つ','待って'],['飛ぶ','ぶ','飛んで'],['飲む','む','飲んで'],['走る','る','走って'],['歌う','う','歌って'],['食べる','ichidan','食べて'],['観測する','suru','観測して'],['来る','kuru','来て']]){
 const forms=ctx.nebulithJapaneseForms(lemma,kind);
 for(const tail of ['ない','なかった','ないです','なかったです'])assert.ok(forms.some(f=>f.ending===contraction+tail&&f.feature==='口語否定'),lemma+tail);
}
const ambiguous='私は包帯を観測してない。';
assert.equal(analyze(ambiguous,{reading,confirmed:true}).complete,false,'noun sense is still required');
const options=analyze(ambiguous,{reading}).segments[0].nounOptions[0].options;
for(const option of options)assert.equal(analyze(ambiguous,{reading,nounSenses:{包帯:option.id},confirmed:true}).text,`Ne di vyrel el mi ia ${option.root}.`);
const quote='私は「あなたは水を飲んでない」と言う。';
assert.equal(analyze(quote).segments[0].readingOptions.length,2);
assert.equal(analyze(quote,{reading}).segments[0].state,'candidate');
assert.equal(analyze(quote,{reading,confirmed:true}).text,'Fenor el mi ia "Ne di bion el ti ia daris."');
assert.equal(analyze(quote,{reading:'unrealized-negative',confirmed:true}).complete,false);
const multiple='私は水を飲んでない。あなたは歩いてない。';
const initial=analyze(multiple),bySegment={[initial.segments[0].key]:{reading,confirmed:true}};
assert.equal(analyze(multiple,{bySegment}).segments[1].state,'draft','meaning does not leak across sentences');
bySegment[initial.segments[1].key]={reading:'unrealized-negative',confirmed:true};
assert.equal(analyze(multiple,{bySegment}).complete,false);
assert.equal(analyze('あなたは歩く。水を飲んでない。',{reading,confirmed:true}).segments[1].state,'draft','global choice is not applied to later sentences');
assert.equal(analyze('私は水を飲んでいない。').text,'Ne di bion el mi ia daris.','explicit progressive keeps its established behavior');
console.log(`PASS: ${fixtures.length} literal negative-reading fixtures, confirmation, source alignment, roles, ambiguity, quotes, isolation and unsupported noncompletion`);
