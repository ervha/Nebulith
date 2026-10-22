// Optional real-browser acceptance checks. See web/README.md for local setup.
const fs=require('fs'),path=require('path'),http=require('http'),assert=require('node:assert/strict');
const {pathToFileURL}=require('url');
const {chromium}=require(process.env.NEBULITH_PLAYWRIGHT_PATH||'playwright');
const root=path.resolve(__dirname,'..'),out=path.resolve(process.argv[3]||'audit/maintenance/roadmap-v4-20261022');
assert.ok(out.startsWith(path.join(root,'audit')+path.sep));fs.mkdirSync(out,{recursive:true});
const base=process.argv[2]||'http://127.0.0.1:8877/web/';assert.match(base,/^http:\/\/(127\.0\.0\.1|localhost):\d+\//);
const report={startedAt:new Date().toISOString(),base,checks:{},limitations:['Composition events are synthetic; Microsoft IME input was not tested.','Viewport tests use desktop Chromium, not a physical mobile device.']};
const executablePath=process.env.NEBULITH_BROWSER_EXE||'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
(async()=>{
  const browser=await chromium.launch({headless:true,executablePath});let fixture;
  try {
    const context=await browser.newContext({viewport:{width:1280,height:800},acceptDownloads:true});
    const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
    await page.goto(base+'index.html');await page.locator('#wordGrid .word-open').first().waitFor();
    assert.equal(await page.locator('#pwaReload').isVisible(),false);
    await page.locator('#lexSearchInput').fill('味見');await page.locator('.word-open').first().focus();await page.keyboard.press('Enter');
    await page.waitForFunction(()=>document.getElementById('wordModal').classList.contains('active'));
    assert.equal(await page.evaluate(()=>document.activeElement.id),'modalCloseBtn');
    await page.keyboard.press('Shift+Tab');assert.ok(await page.evaluate(()=>document.getElementById('wordModal').contains(document.activeElement)));
    await page.keyboard.press('Escape');assert.equal(await page.locator('#wordModal').evaluate(e=>e.classList.contains('active')),false);
    assert.equal(await page.evaluate(()=>document.activeElement.classList.contains('word-open')),true);report.checks.keyboardModalAndFocus=true;
    await page.locator('[data-tab="translator"]').click();await page.locator('#transInput').fill('私は包帯を観測する。');
    await page.locator('#inputNounChoices select').waitFor();const selector=page.locator('#inputNounChoices select');const options=await selector.locator('option').allTextContents();assert.equal(options.length,3);
    await selector.selectOption('260');await page.locator('#confirmInputCandidate').click();await page.waitForFunction(()=>!document.getElementById('copyDstBtn').disabled);
    assert.equal(await page.locator('#transOutputText').textContent(),'Vyrel el mi ia valmik.');report.checks.nounSelection={options,text:'Vyrel el mi ia valmik.'};
    await page.reload();assert.equal(await page.locator('#transInput').inputValue(),'私は包帯を観測する。');assert.equal(await page.locator('#copyDstBtn').isDisabled(),true);report.checks.restoreRequiresConfirmation=true;
    await page.locator('[data-tab="translator"]').click();await page.locator('#confirmInputCandidate').click();
    await page.locator('#transInput').fill('あなたは家でくつろぐ。スープを味見する。');
    await page.locator('#inputSubject').selectOption({label:'前文の主体：あなた（確認が必要）'});
    await page.locator('#confirmInputCandidate').click();
    assert.equal(await page.locator('#transOutputText').textContent(),'Zensirin el ti uo govan.\nNerkirel el ti ia darel.');report.checks.explicitContextSelection=true;
    const ime=await page.evaluate(()=>{const before=transOutputText.textContent;transInput.dispatchEvent(new CompositionEvent('compositionstart'));transInput.value='私はあなたと仲直りする。';transInput.dispatchEvent(new InputEvent('input',{isComposing:true}));doTranslate();const held=copyDstBtn.disabled&&transOutputText.textContent===before;transInput.dispatchEvent(new CompositionEvent('compositionend'));return {held,text:transOutputText.textContent}});
    assert.equal(ime.held,true);assert.equal(ime.text,'Jylfen el mi ku ti.');report.checks.compositionEvents=ime;
    await page.locator('#srcLangSelect').selectOption('neb');await page.locator('#dstLangSelect').selectOption('ja');await page.locator('#transInput').fill('Renantal el mi ia ti.');
    await page.waitForFunction(()=>document.getElementById('inputInterpretation').textContent.includes('取引'));assert.equal(await page.locator('#copyDstBtn').isDisabled(),true);report.checks.ambiguousReverseReasonVisible=true;
    await page.locator('#srcLangSelect').selectOption('ja');await page.locator('#dstLangSelect').selectOption('neb');await page.locator('#transInput').fill('私はあなたと仲直りする。');
    await page.waitForFunction(()=>document.getElementById('transOutputText').textContent==='Jylfen el mi ku ti.');
    await page.locator('summary').filter({hasText:'保存・バックアップ'}).click();
    const downloadWait=page.waitForEvent('download');await page.locator('#backupExport').click();const download=await downloadWait;const backup=path.join(out,'browser-backup.json');await download.saveAs(backup);
    const saved=JSON.parse(fs.readFileSync(backup,'utf8'));assert.equal(saved.source,'Nebulith Studio Backup');
    await page.locator('#transInput').fill('私は家でくつろぐ。');await page.waitForFunction(()=>document.getElementById('transOutputText').textContent==='Zensirin el mi uo govan.');
    await page.locator('#backupImport').setInputFiles(backup);await page.locator('#backupApply').click();await page.waitForLoadState('load');
    await page.waitForFunction(()=>document.getElementById('transInput').value==='私はあなたと仲直りする。');report.checks.backupRoundTrip=true;
    const layouts=[];
    for(const width of [1280,390,360])for(const theme of ['dark','light']){
      await page.setViewportSize({width,height:844});await page.evaluate(t=>{document.documentElement.setAttribute('data-theme',t);},theme);
      for(const tab of ['lexicon','translator']){
        await page.locator(`[data-tab="${tab}"]`).click();const state=await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth}));
        assert.ok(state.scrollWidth<=state.width,JSON.stringify({theme,tab,...state}));layouts.push({theme,tab,...state});
      }
    }
    report.checks.layouts=layouts;await page.screenshot({path:path.join(out,'mobile-layout.png'),fullPage:false,animations:'disabled'});
    // An isolated HTTP fixture serves the exact Web assets. Only a cache suffix
    // and an inert app comment change, so update testing never mutates the repo.
    let version=0;const sw=fs.readFileSync(path.join(root,'web/service-worker.js'),'utf8');const originalCache=/const CACHE_NAME = '([^']+)'/.exec(sw)[1];
    fixture=http.createServer((req,res)=>{const name=new URL(req.url,'http://localhost').pathname.replace(/^\//,'')||'index.html';const filename=path.resolve(root,'web',name);if(!filename.startsWith(path.join(root,'web')+path.sep)){res.writeHead(403).end();return;}try{let buffer=fs.readFileSync(filename);if(name==='service-worker.js')buffer=Buffer.from(sw.replace(originalCache,originalCache+'-qa-'+version));if(name==='app.js')buffer=Buffer.concat([buffer,Buffer.from('\n// roadmap cache generation '+version)]);res.setHeader('Cache-Control','no-store');res.setHeader('Content-Type',name.endsWith('.js')?'application/javascript':name.endsWith('.html')?'text/html':name.endsWith('.json')?'application/json':'image/svg+xml');res.end(buffer);}catch{res.writeHead(404).end();}});
    await new Promise(resolve=>fixture.listen(0,'127.0.0.1',resolve));const updateUrl=`http://127.0.0.1:${fixture.address().port}/`;
    context.on('page',p=>p.on('pageerror',e=>errors.push(e.message)));
    const updatePage=await context.newPage();await updatePage.goto(updateUrl);await updatePage.evaluate(async()=>{const r=await navigator.serviceWorker.ready;if(r.active.state!=='activated')await new Promise(resolve=>r.active.addEventListener('statechange',()=>{if(r.active.state==='activated')resolve();}));});
    await updatePage.waitForFunction(()=>!!navigator.serviceWorker.controller);
    await updatePage.locator('[data-tab="translator"]').click();await updatePage.locator('#transInput').fill('私はあなたと仲直りした。');
    await updatePage.waitForFunction(()=>document.getElementById('transOutputText').textContent==='Fe jylfen el mi ku ti.');
    version=1;await updatePage.evaluate(async()=>{window.qaControllerChanged=false;navigator.serviceWorker.addEventListener('controllerchange',()=>{window.qaControllerChanged=true;},{once:true});const registration=await navigator.serviceWorker.getRegistration();await registration.update();});
    await updatePage.waitForFunction(async name=>{const r=await navigator.serviceWorker.getRegistration();const keys=await caches.keys();if(r?.active?.state!=='activated'||!keys.includes(name+'-qa-1')||keys.includes(name+'-qa-0'))return false;const response=await(await caches.open(name+'-qa-1')).match(new URL('app.js',location.href).href);return response&&(await response.text()).endsWith('// roadmap cache generation 1');},originalCache,{timeout:20000});
    await updatePage.waitForFunction(()=>window.qaControllerChanged===true);
    report.beforeOffline=await updatePage.evaluate(async()=>({url:location.href,keys:await caches.keys(),tail:(await(await fetch('app.js')).text()).slice(-40)}));
    await updatePage.locator('#pwaReload').waitFor({state:'visible'});
    await context.setOffline(true);await updatePage.locator('#pwaReload').click();await updatePage.waitForLoadState('load');await updatePage.locator('#wordGrid .word-open').first().waitFor();
    assert.equal(await updatePage.locator('#transInput').inputValue(),'私はあなたと仲直りした。');
    const generation=await updatePage.evaluate(async()=>{const response=await fetch('app.js');const source=await response.text();const cachesInfo=[];for(const key of await caches.keys()){const r=await(await caches.open(key)).match(new URL('app.js',location.href).href);cachesInfo.push({key,tail:r?(await r.text()).slice(-100):null});}return {status:response.status,tail:source.slice(-100),cachesInfo};});report.updateProbe=generation;assert.ok(generation.tail.endsWith('// roadmap cache generation 1'),JSON.stringify(generation));
    report.checks.serviceWorkerUpdateAndOfflineRestart={generation:1,draftPreserved:true,cacheKeys:await updatePage.evaluate(()=>caches.keys())};
    const standalone=await context.newPage();await standalone.goto(pathToFileURL(path.join(root,'web/standalone.html')).href);await standalone.locator('#wordGrid .word-open').first().waitFor();
    await standalone.locator('[data-tab="translator"]').click();await standalone.locator('#transInput').fill('私はあなたと仲直りする。');
    await standalone.waitForFunction(()=>document.getElementById('transOutputText').textContent==='Jylfen el mi ku ti.');report.checks.standaloneFileOffline=true;
    report.pageErrors=errors;assert.deepEqual(errors,[]);report.finishedAt=new Date().toISOString();report.browserVersion=browser.version();report.playwrightVersion=require(path.join(path.dirname(require.resolve(process.env.NEBULITH_PLAYWRIGHT_PATH||'playwright')),'package.json')).version;
    fs.writeFileSync(path.join(out,'browser-results.json'),JSON.stringify(report,null,2)+'\n');console.log('PASS: browser keyboard, noun choices, backup, responsive layouts, SW update/offline restart and file standalone');
  }catch(error){report.failure=String(error.stack||error);fs.writeFileSync(path.join(out,'browser-failure-'+Date.now()+'.json'),JSON.stringify(report,null,2)+'\n');throw error;}
  finally{await browser.close();if(fixture)await new Promise(resolve=>fixture.close(resolve));}
})().catch(e=>{console.error(e);process.exitCode=1;});
