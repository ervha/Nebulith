const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
const ctx={};vm.createContext(ctx);for(const file of ['web/data.js','web/incremental.js'])vm.runInContext(fs.readFileSync(file,'utf8'),ctx);
vm.runInContext('globalThis.engine=createIncrementalTranslator(VOCAB,GRAMMAR_FRAMES,INPUT_RULES.aliases,[],TRANSLATION_EXTENSIONS)',ctx);
let r=ctx.engine.analyze('私は水を飲みませんでした',{}),m=r.segments[0].meaning;
assert.equal(m.schemaVersion,1);assert.equal(m.kind,'clause');assert.equal(m.tense,'past');assert.equal(m.negative,true);assert.equal(m.arguments.el.nrs,'mi');assert.equal(m.arguments.ia.source,'水');assert.deepEqual(Array.from(m.predicate.prefixes),['fe','ne']);
for(const [source,kind,actionNeg,modalNeg] of [['私は水を飲みたくない','desire',false,true],['私は水を飲まないかも','uncertainty',true,false],['私は水を飲むことができない','possibility',false,true],['私は水を飲むつもりだ','intention',false,false],['私は水を飲む必要がある','necessity',false,false],['私は水を飲んだと思う','thought',false,false]]){
  const result=ctx.engine.analyze(source,{});assert.equal(result.complete,false,source);const meaning=result.segments[0].meaning;
  assert.ok(meaning,source);assert.equal(meaning.negative,actionNeg,source);assert.equal(meaning.modalities[0].kind,kind,source);assert.equal(meaning.modalities[0].negated,modalNeg,source);assert.equal(meaning.modalities[0].realization,'not-defined');
}
for(const [source,target,relation] of [
 ['星が輝くなら、私は走る。','Sen falun el vyr, kupan el mi.','sen'],
 ['私は働いたので、私は家で眠る。','Zen fe dolar el mi, tymis el mi uo govan.','zen'],
 ['私は働くけれど、あなたは眠る。','Tor dolar el mi, tymis el ti.','tor'],
 ['私は歌うとき、あなたは踊る。','Hav cival el mi, spilan el ti.','hav']]){
  const result=ctx.engine.analyze(source,{});assert.equal(result.complete,true,source+JSON.stringify(result));assert.equal(result.text,target);const meaning=result.segments[0].meaning;assert.equal(meaning.relation,relation);assert.equal(meaning.clauses.length,2);
  if(relation==='zen'){assert.equal(meaning.clauses[0].tense,'past');assert.equal(meaning.clauses[1].tense,'unmarked','do not inherit past tense');}
}
for(const source of ['私は歌うなら、走る。','私は水を飲みたいので、あなたは待つ。','私は歌うなら、あなたは踊るので、彼は眠る。'])assert.equal(ctx.engine.analyze(source,{}).complete,false,source);
const sources=['あなたが嫌い。','未来を見る。'];const bySegment={};
for(const source of sources)bySegment[JSON.stringify([source,0])]={subject:'私',...(source.startsWith('未来')?{verb:'展望する'}:{}),confirmed:true};
r=ctx.engine.analyze(sources.join(''),{bySegment});assert.equal(r.complete,true);assert.ok(r.text.includes('Nyrcan'));assert.ok(r.text.includes('Valcyn'));
assert.equal(r.segments[0].meaning.arguments.el.inferred,true);
const changed=ctx.engine.analyze('あなたが嫌い。星は赤い。',{bySegment});assert.equal(changed.complete,true);assert.ok(!changed.text.includes('Valcyn'),'old selection must not affect another source');
console.log('PASS: shared meaning representation, modality/negation scope, four compositional conjunctions, no tense inheritance, per-sentence choices');
