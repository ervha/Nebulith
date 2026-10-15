const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
function start(storage){
  const dom={},downloads=[];let reloaded=false;
  function element(id){return dom[id]||=( {id,value:'',textContent:'',innerHTML:'',disabled:false,handlers:{},style:{setProperty(k,v){this[k]=v;}},classList:{add(){},remove(){}},setAttribute(){},addEventListener(name,fn){this.handlers[name]=fn;},click(){downloads.push(this);}} );}
  const ctx={localStorage:storage,document:{documentElement:element('html'),getElementById:element,querySelectorAll:()=>[],createElement:tag=>({tag,click(){downloads.push(this);}})},window:{location:{reload(){reloaded=true;}}},navigator:{clipboard:{writeText:()=>Promise.resolve()}},setTimeout:()=>0,clearTimeout(){},console,alert(){},confirm:()=>true,Blob,URL,TextEncoder,crypto:require('node:crypto').webcrypto};
  vm.createContext(ctx);for(const file of ['web/data.js','web/incremental.js','web/workspace.js','web/app.js'])vm.runInContext(fs.readFileSync(file,'utf8'),ctx);
  return {ctx,dom,eval:s=>vm.runInContext(s,ctx),event:(id,type)=>dom[id].handlers[type]?.({target:dom[id]}),reloaded:()=>reloaded};
}
(async()=>{
  const storage={data:{},getItem(k){return this.data[k]??null;},setItem(k,v){this.data[k]=v;}};
  let app=start(storage);
  app.dom.transInput.value='あなたが嫌い。';app.event('transInput','input');app.eval('doTranslate()');
  app.dom.inputSubject.value='私';app.event('inputSubject','change');app.event('confirmInputCandidate','click');
  assert.equal(app.dom.copyDstBtn.disabled,false);
  app.dom.fontSizeSlider.value='48';app.event('fontSizeSlider','input');
  app.dom.splitWidth.value='60';app.event('splitWidth','input');
  app.dom.editorInput.value='書きかけの筆記';app.event('editorInput','input');
  app.ctx.window.openWordModal('mi');
  app=start(storage);
  assert.equal(app.dom.transInput.value,'あなたが嫌い。');assert.equal(app.dom.inputSubject.value,'私');
  assert.equal(app.dom.copyDstBtn.disabled,true,'restored inference needs confirmation');
  assert.ok(app.dom.transOutputText.textContent.includes('Nyrcan'));assert.ok(app.dom.sessionStatus.textContent.includes('復元'));
  assert.equal(app.dom.fontSizeSlider.value,'48');assert.equal(app.dom.splitWidth.value,'60');assert.equal(app.dom.editorInput.value,'書きかけの筆記');
  assert.equal(app.eval('browsingHistory[0]'),'mi');
  app.dom.transInput.value='あなたが嫌い。未来を見る。';app.event('transInput','input');app.eval('doTranslate()');
  const selectSentence=index=>{app.dom.inputSentence.value=app.eval(`lastInputAnalysis.segments[${index}].key`);app.event('inputSentence','change');};
  selectSentence(0);app.dom.inputSubject.value='私';app.event('inputSubject','change');app.event('confirmInputCandidate','click');
  selectSentence(1);app.dom.inputSubject.value='あなた';app.event('inputSubject','change');app.dom.inputVerb.value='展望する';app.event('inputVerb','change');app.event('confirmInputCandidate','click');
  assert.equal(app.eval('lastInputAnalysis.complete'),true);assert.ok(app.dom.transOutputText.textContent.includes('Valcyn el ti'));
  app.dom.transInput.value='あなたが嫌い。星は赤い。';app.event('transInput','input');app.eval('doTranslate()');
  assert.equal(app.eval('lastInputAnalysis.segments[0].state'),'complete','unchanged unique sentence retains confirmed meaning');
  assert.ok(!app.dom.transOutputText.textContent.includes('Valcyn'),'edited sentence loses prior meaning');
  app.dom.transInput.value='あなたが嫌い。未来を見る。';app.event('transInput','input');app.eval('doTranslate()');
  assert.equal(app.eval('lastInputAnalysis.segments[1].state'),'draft');
  app=start(storage);assert.equal(app.eval('lastInputAnalysis.segments[0].state'),'candidate','restart resets sentence confirmation');
  assert.equal(app.eval('inputChoicesState.bySegment[lastInputAnalysis.segments[0].key].subject'),'私');
  const queue={queue:[{id:'request-original',type:'sentence',lang:'ja',text:'まだ未対応の文',count:2,context:'文型不足'}]};
  app.dom.importQueueFiles.files=[{name:'requests.json',size:300,text:async()=>JSON.stringify(queue)}];
  await app.event('importQueueFiles','change');assert.equal(app.dom.applyQueueImport.disabled,false);app.event('applyQueueImport','click');
  assert.equal(app.eval('feedbackQueue.length'),1);assert.equal(app.eval('feedbackQueue[0].count'),2);
  await app.event('importQueueFiles','change');app.event('applyQueueImport','click');assert.equal(app.eval('feedbackQueue[0].count'),2);
  app.dom.importQueueFiles.files=[{name:'bad.json',size:3,text:async()=>'{bad'}];await app.event('importQueueFiles','change');
  assert.equal(app.dom.applyQueueImport.disabled,true);assert.equal(app.eval('feedbackQueue.length'),1);
  const id=app.eval('feedbackQueue[0].id');app.ctx.window.setQueueField(id,'status','review');
  app=start(storage);assert.equal(app.eval('feedbackQueue[0].status'),'review');
  const backup=app.eval('safeStorage.snapshot()');
  app.dom.backupImport.files=[{size:300,name:'backup.json',text:async()=>JSON.stringify(backup)}];await app.event('backupImport','change');
  assert.equal(app.dom.backupApply.disabled,false);app.event('backupApply','click');assert.equal(app.reloaded(),true);
  storage.setItem=()=>{throw Error('quota-full');};
  assert.equal(app.eval(`addFeedbackItem('word','ja','別の語','検索なし')`),false);
  assert.equal(app.eval('feedbackQueue.length'),1);assert.ok(app.dom.storageStatus.textContent.includes('quota-full'));
  console.log('PASS: UI restart preserves source/choices/settings/history, confirmation is reset, JSON preview/merge/status/backup and quota failure');
})().catch(error=>{console.error(error);process.exitCode=1;});

