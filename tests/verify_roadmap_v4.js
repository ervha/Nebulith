const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
const dom={};function el(id){return dom[id]||=({value:'',innerHTML:'',textContent:'',disabled:false,handlers:{},style:{setProperty(){}},classList:{add(){},remove(){},contains(){return false},toggle(){}},setAttribute(){},addEventListener(k,f){this.handlers[k]=f;}});}
const ctx={console,document:{documentElement:el('html'),getElementById:el,querySelectorAll:()=>[]},window:{},localStorage:{getItem:()=>null,setItem(){}},navigator:{clipboard:{writeText:()=>Promise.resolve()}},setTimeout:()=>0,clearTimeout(){},alert(){},confirm:()=>true};vm.createContext(ctx);
for(const file of ['data','bidirectional','incremental','workspace','app'])vm.runInContext(fs.readFileSync('web/'+file+'.js','utf8'),ctx);
const run=s=>vm.runInContext(s,ctx),analyze=(s,c={})=>run(`inputEngine.analyze(${JSON.stringify(s)},${JSON.stringify(c)})`);
const lexical=JSON.parse(fs.readFileSync('tests/fixtures/roadmap_lexical_goldens.json','utf8'));
let goldens=0;
for(const row of lexical.verbs){
  for(const [source,target,past,negative] of [[row.source,row.target,false,false],[row.pastSource,row.pastTarget,true,false],[row.negativeSource,row.negativeTarget,false,true]]){
    const result=analyze(source,{confirmed:true});assert.equal(result.complete,true,source+JSON.stringify(result));assert.equal(result.text,target,source);
    assert.equal(result.segments[0].meaning.predicate.entryId,row.id);
    assert.equal(result.segments[0].meaning.tense,past?'past':'unmarked');
    assert.equal(result.segments[0].meaning.negative,negative);
    for(const [role,nrs] of Object.entries(row.args))assert.equal(result.segments[0].meaning.arguments[role].nrs,nrs,source+' '+role);
    goldens++;
  }
  const reversed=ctx.NebulithBidirectionalEngine.translateNebulith(row.pastTarget,'ja');assert.equal(reversed.success,true,row.root+' '+JSON.stringify(reversed));
  assert.ok(reversed.text.endsWith(row.pastLemma+'.'),row.root+' '+reversed.text);
  const invalid=analyze(row.invalidSource,{confirmed:true});assert.equal(invalid.complete,false,row.invalidSource);assert.ok(invalid.notes.join(' ').includes('項構造'),row.invalidSource+' '+invalid.notes);
}
for(const row of lexical.adjectives)for(const fixture of row.examples){
  const r=analyze(fixture.source,{confirmed:true});assert.equal(r.complete,true,fixture.source+JSON.stringify(r));assert.equal(r.text,fixture.target);goldens++;
}
const rules=JSON.parse(fs.readFileSync('data/roadmap_lexical_rules.json','utf8'));
assert.equal(rules.verbs.length,43);assert.equal(rules.adjectives.length,8);assert.equal(rules.held.length,6);
assert.equal(run('inputEngine.coverage().unsupportedVerbs.length'),0);
const noun=analyze('私は包帯を観測する。');assert.equal(noun.complete,false);const group=noun.segments[0].nounOptions[0];assert.equal(group.term,'包帯');assert.equal(group.options.length,2);
for(const choice of group.options){
  const opts={nounSenses:{'包帯':choice.id}};const r=analyze('私は包帯を観測する。',opts);assert.equal(r.complete,false);assert.equal(r.segments[0].state,'candidate');
  const confirmed=analyze('私は包帯を観測する。',{...opts,confirmed:true});assert.equal(confirmed.complete,true);assert.equal(confirmed.text,`Vyrel el mi ia ${choice.root}.`);
}
assert.equal(analyze('私は包帯を観測する。',{nounSenses:{'包帯':999999},confirmed:true}).complete,false);
assert.equal(analyze('私は包帯を観測する。').complete,false,'selections cannot leak to the next analysis');
const input='あなたは家でくつろぐ。スープを味見する。';const conversation=analyze(input);assert.equal(conversation.complete,false);
assert.equal(conversation.segments[1].contextSubject.nrs,'ti');assert.equal(conversation.segments[1].meaning.arguments.el.nrs,'mi','context is a suggestion, not a silent rewrite');
const bySegment={[conversation.segments[1].key]:{subject:'あなた',confirmed:true}};
assert.equal(analyze(input,{bySegment}).text,'Zensirin el ti uo govan.\nNerkirel el ti ia darel.');
for(const source of ['私は','家で','私は知らない料理を味見する。']){
  const r=analyze(source);assert.equal(r.complete,false);assert.equal(r.segments[0].fragments.map(f=>f.source).join(''),source);
  for(const f of r.segments[0].fragments)assert.equal(source.slice(f.start,f.end),f.source);
}
const invalid=[
  ['Renantal el mi al ti.','必須'],['Renantal el mi ia pamel to ti.','許容格'],['Renantal el mi ia nonsense.','未知の引数'],
  ['Zensirin el mi ia pamel.','許容格'],['Nerkirel el mi ia darel nonsense.','未知の引数'],['Nerkirel el mi ia darel pamel.','修飾'],
  ['Vyrel el mi ia darel pyrin tyni.','複雑'],['Fe fe nerkirel el mi ia darel.','重複'],['Zen nerkirel el mi, poran el ti.','']
];
for(const [source,reason] of invalid)for(const lang of ['ja','en']){
  const result=ctx.NebulithBidirectionalEngine.translateNebulith(source,lang);assert.equal(result.success,false,source+' '+JSON.stringify(result));if(reason)assert.ok(result.error.includes(reason));
  assert.equal(run(`translateSingleSentence(${JSON.stringify(source)},'neb','${lang}')`).success,false);
}
for(const [source,expected] of [['Renantal el mi ia pamel al ti.','私は あなたに 本を 譲る.'],['Fe ne renantal el ti ia pamel al mi.','あなたは 私に 本を 譲らなかった.'],['Fe ne di nerkirel el mi ia darel.','私は スープを 味見していなかった.']]){
  const r=ctx.NebulithBidirectionalEngine.translateNebulith(source,'ja');assert.equal(r.success,true);assert.equal(r.text,expected);
}
for(const [source,target] of [['The star is blue.','Zylin el vyr.'],['The star is green.','Velini el vyr.'],['The sun is bright.','Faluni el zohar.'],['The star is golden.','Valin el vyr.'],['If stars shine, I walk.','Sen Falun el vyr, Poran el mi.'],['Because stars shine, I walk.','Zen Falun el vyr, Poran el mi.']]){
  const r=ctx.NebulithBidirectionalEngine.translateEnglishToNebulith(source);assert.equal(r.success,true,source+JSON.stringify(r));assert.equal(r.text,target);
}
const morphology=[
 ['Fe ne di nerkirel el mi ia darel.','en','I was not taste-testing soup.'],
 ['Fe neran el ti ia darel.','en','you ate soup.'],
 ['Fe ne neran el ti ia darel.','en','you did not eat soup.'],
 ['Poran el ri.','en','he walks.'],
 ['Fe relen el valis ia zendarini.','ja','衣服は 肌馴染みが良かった.'],
 ['Ne relen el doran ia bionvyri.','ja','惑星は ハビタブルではない.'],
 ['Fe ne relen el sylim ia zenalin.','ja','心は 明晰判明ではなかった.'],
 ['Relen el doran ia bionvyri.','en','planet is habitable.'],
 ['Poran el ti to govan ka?','ja','あなたは 家へ 歩くか？']
 ,['Martan el mi ia pamel va ti.','ja','私は あなたから 本を 受け取る.']
 ,['Martan el mi ia pamel va ti.','en','I receive book from you.']
 ,['Zelvan el ti ia pamel al mi.','en','you give book to me.']
];
for(const [source,lang,target] of morphology){const r=ctx.NebulithBidirectionalEngine.translateNebulith(source,lang);assert.equal(r.success,true,JSON.stringify(r));assert.equal(r.text,target);}
for(const source of ['The star is deep.','I walk to house with you.','I observe nonsense.'])assert.equal(ctx.NebulithBidirectionalEngine.translateEnglishToNebulith(source).success,false,source);
for(const lang of ['ja','en']){const r=ctx.NebulithBidirectionalEngine.translateNebulith('Renantal el mi ia ti.',lang);assert.equal(r.success,false);assert.ok(r.error.includes('取引'));}
assert.equal(analyze('私はあなたを譲る。',{confirmed:true}).complete,false);
run("transInput.value='私は包帯を観測する。';resetInputChoices();doTranslate()");assert.ok(dom.inputNounChoices.innerHTML.includes('包帯'));assert.equal(dom.copyDstBtn.disabled,true);
run(`inputChoicesState={nounSenses:{'包帯':${group.options[0].id}},confirmed:true};doTranslate()`);assert.equal(dom.copyDstBtn.disabled,false);
const saved=ctx.NebulithWorkspace.session({text:'私は包帯を観測する。',srcLang:'ja',dstLang:'neb',choices:{nounSenses:{'包帯':group.options[0].id},confirmed:true}});
assert.equal(saved.choices.nounSenses['包帯'],group.options[0].id);assert.equal(saved.choices.confirmed,false);
const catalog=run('dictionaryCatalog');assert.equal(catalog.length,2483);assert.ok(catalog.every(w=>w.displayCategory));
assert.ok(run('new Set(dictionaryCatalog.map(w=>w.displayCategory)).size')<run('new Set(dictionaryCatalog.map(w=>w.c)).size'));
assert.ok(dom.wordGrid.innerHTML.includes('class="word-roman word-open"'));
run("renderAlignments([{src:'雫茶',dst:'darterin',role:'対象'}])");assert.ok(dom.transAlignmentBox.innerHTML.includes('<button type="button" class="align-dst has-word"'));
const report={lexicalGoldenSentences:goldens,additionalVerbRoots:43,verbArgumentRejections:43,verbPastReverseWitnesses:43,adjectiveRules:8,heldAdjectives:6,attributiveOnly:3,reverseRejectedCases:invalid.length*2,reverseMorphologyGoldens:morphology.length,recipientAmbiguityRejected:true,nounChoices:group.options.length,contextRequiresConfirmation:true,fragmentSourceReconstruction:true};
if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(report,null,2)+'\n');
console.log('PASS: roadmap v4 '+JSON.stringify(report));
