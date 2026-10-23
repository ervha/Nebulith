const fs=require('fs'),vm=require('vm'),path=require('path'),assert=require('node:assert/strict');
const dom={};
function element(id){return dom[id]||=( {value:'',textContent:'',innerHTML:'',disabled:false,handlers:{},style:{setProperty(k,v){this[k]=v;}},classList:{values:new Set(),add(v){this.values.add(v);},remove(v){this.values.delete(v);},contains(v){return this.values.has(v);},toggle(v){this.values.has(v)?this.values.delete(v):this.values.add(v);}},setAttribute(){},addEventListener(k,f){this.handlers[k]=f;}} );}
const ctx={console,document:{documentElement:element('html'),getElementById:element,querySelectorAll:()=>[],createElement:()=>({click(){}})},window:{},localStorage:{getItem:()=>null,setItem(){}},navigator:{clipboard:{writeText:()=>Promise.resolve()}},setTimeout:()=>0,clearTimeout(){},alert(){},confirm:()=>true};
vm.createContext(ctx);
for(const file of ['data','bidirectional','incremental','workspace','app'])vm.runInContext(fs.readFileSync('web/'+file+'.js','utf8'),ctx);
const run=s=>vm.runInContext(s,ctx),event=(id,type)=>dom[id].handlers[type]({target:dom[id]});
const roots=()=>Array.from(dom.wordGrid.innerHTML.matchAll(/onclick="openWordModal\('([^']+)'\)"/g),m=>m[1]);
const total=run('dictionaryCatalog.length');assert.equal(total,2483);
const seen=new Set();let pages=0;
do{for(const root of roots()){assert.ok(!seen.has(root),'duplicate page entry '+root);seen.add(root);}pages++;if(dom.lexNextPage.disabled)break;event('lexNextPage','click');}while(pages<100);
assert.equal(seen.size,total,'every dictionary word is reachable through paging');assert.equal(pages,42);
dom.lexSearchInput.value='雫茶';event('lexSearchInput','input');assert.ok(roots().includes('darterin'),'ordinary search includes compounds');assert.ok(dom.lexPageInfo.textContent.startsWith('1 /'));
const target=run("VERIFIED_CANONICAL_COMPOUNDS.entries.find(e=>e.nrs==='nerkirel')");
dom.lexSearchInput.value='味見';dom.lexCategoryFilter.value=target.category;dom.lexBatchFilter.value=target.batch;event('lexBatchFilter','change');assert.deepEqual(roots(),['nerkirel']);
run("currentFilterPos='CANON';renderLexicon()");assert.ok(!dom.wordGrid.innerHTML.includes('recordMissingWordBtn'),'a filtered-out known word is not recorded as unknown');
event('lexResetFilters','click');assert.equal(roots().length,60);assert.equal(dom.lexBatchFilter.value,'');
dom.lexSearchInput.value='ＤＡＲＴＥＲＩＮ';event('lexSearchInput','input');assert.deepEqual(roots(),['darterin'],'full-width NRS normalizes for search');
ctx.window.toggleFav(null,'darterin');run("currentFilterPos='FAV';searchInput.value='';renderLexicon()");assert.deepEqual(roots(),['darterin']);
ctx.window.openWordModal('darterin');run("currentFilterPos='HISTORY';renderLexicon()");assert.deepEqual(roots(),['darterin']);
const fixtures=JSON.parse(fs.readFileSync('tests/fixtures/practical_compound_sentences.json','utf8'));
for(const fixture of fixtures.complete){
  const result=run(`inputEngine.analyze(${JSON.stringify(fixture.source)},{confirmed:true})`);
  assert.equal(result.complete,true,fixture.source+JSON.stringify(result));assert.equal(result.text,fixture.target,fixture.source);
  const meaning=result.segments[0].meaning;assert.equal(meaning.predicate.root,fixture.root);
  for(const [role,value] of Object.entries(fixture.args))assert.equal(meaning.arguments[role]?.nrs,value,fixture.source+' '+role);
  for(const key of ['tense','negative','aspect'])if(key in fixture)assert.equal(meaning[key],fixture[key],fixture.source+' '+key);
}
for(const fixture of fixtures.notComplete){
  const result=run(`inputEngine.analyze(${JSON.stringify(fixture.source)},{confirmed:true})`);
  assert.equal(result.complete,false,fixture.source+' / '+fixture.reason);
  assert.equal(result.segments[0].source,fixture.source);
  assert.equal(result.segments[0].state,fixture.state,fixture.source);
  assert.ok(result.notes.some(note=>note.includes(fixture.note)),fixture.source+' / '+result.notes.join(' '));
}
const inference=run("inputEngine.analyze('スープを味見する。',{})");assert.equal(inference.complete,false);assert.equal(inference.segments[0].state,'candidate');assert.equal(inference.segments[0].meaning.arguments.el.inferred,true);
run('NebulithBidirectionalEngine.configure(VOCAB,VERIFIED_CANONICAL_COMPOUNDS)');
for(const source of fixtures.invalidNebulith)for(const lang of ['ja','en']){
  const result=ctx.NebulithBidirectionalEngine.translateNebulith(source,lang);assert.equal(result.success,false,source+' '+lang);assert.ok(result.error);
  const appResult=run(`translateSingleSentence(${JSON.stringify(source)},'neb',${JSON.stringify(lang)})`);
  assert.equal(appResult.success,false,'the app must preserve rejection: '+source+' '+lang);
}
assert.equal(ctx.NebulithBidirectionalEngine.translateNebulith('Nerkirel el mi ia darel.','ja').text,'私は スープを 味見する.');
assert.equal(ctx.NebulithBidirectionalEngine.translateNebulith('Nerkirel el mi ia darel.','en').text,'I taste-test soup.');
const pending=run("inputEngine.analyze('私は雫茶を見る。',{})");assert.equal(pending.complete,false);
const selected=run("inputEngine.analyze('私は雫茶を見る。',{verb:'観測する',confirmed:true})");assert.equal(selected.text,'Vyrel el mi ia darterin.');assert.equal(selected.complete,true);
// Construct a future same-gloss import to make sure ordinary nouns cannot hide a new compound sense.
run("VERIFIED_CANONICAL_COMPOUNDS.entries.push({id:99802,nrs:'fixturecompound',pos:'名',meaningJa:'曖昧試験語',meaningEn:'fixture compound'});globalThis.ambiguousEngine=createIncrementalTranslator([...VOCAB,{id:99801,r:'fixturebase',p:'名',m:'曖昧試験語',en:'fixture noun'}],GRAMMAR_FRAMES,INPUT_RULES.aliases,[],TRANSLATION_EXTENSIONS)");
const ambiguous=run("ambiguousEngine.analyze('私は曖昧試験語を観測する。',{confirmed:true})");assert.equal(ambiguous.complete,false);assert.ok(ambiguous.notes.join(' ').includes('語義候補が複数'));
assert.doesNotThrow(()=>run("inputEngine.analyze('私は星を見る。',{verb:'存在しない解釈',confirmed:true})"));
const report={catalogEntries:total,uniquePagedEntries:seen.size,pages,completeGoldenSentences:fixtures.complete.length,rejectedJapaneseCases:fixtures.notComplete.length,rejectedNebulithCases:fixtures.invalidNebulith.length*2,autoSubjectNeedsConfirmation:true,ambiguousImportedGlossBlocked:true,wordLookupIsNotSentenceSuccess:true};
if(process.argv[2]){const dest=path.resolve(process.argv[2]);assert.ok(dest.startsWith(path.resolve('audit')+path.sep));fs.mkdirSync(path.dirname(dest),{recursive:true});fs.writeFileSync(dest,JSON.stringify(report,null,2)+'\n');}
console.log('PASS: practical development checks '+JSON.stringify(report));
