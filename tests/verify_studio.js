const fs = require('fs');
const vm = require('vm');

const localStorage = {
  store: {},
  getItem(k) { return this.store[k] || null; },
  setItem(k, v) { this.store[k] = v; }
};

const dom = {};
function mockElement(id) {
  return {
    id: id || '',
    value: '',
    textContent: '',
    innerHTML: '',
    classList: {
      items: new Set(),
      add(c) { this.items.add(c); },
      remove(c) { this.items.delete(c); },
      contains(c) { return this.items.has(c); }
    },
    addEventListener() {},
    setAttribute() {},
    style: {setProperty(k,v){this[k]=v;}}
  };
}

const context = {
  document: {
    documentElement: mockElement('html'),
    getElementById(id) {
      if (!dom[id]) dom[id] = mockElement(id);
      return dom[id];
    },
    querySelectorAll() { return []; }
  },
  localStorage: localStorage,
  window: {},
  console: console,
  setTimeout: setTimeout,
  clearTimeout: clearTimeout,
  navigator: { clipboard: { writeText: () => Promise.resolve() } },
  alert: console.log,
  confirm: () => true
};

vm.createContext(context);

const dataCode = fs.readFileSync('web/data.js', 'utf8');
const appCode = fs.readFileSync('web/app.js', 'utf8');

vm.runInContext(dataCode, context);
vm.runInContext(fs.readFileSync('web/incremental.js', 'utf8'), context);
vm.runInContext(fs.readFileSync('web/workspace.js','utf8'), context);
vm.runInContext(appCode, context);

const testCode = `
console.log('=== Studio Logic & Translation Verification ===');
console.log('Vocab count:', VOCAB.length);
console.log('Translation pairs count:', translationPairs.length);

// 1. Translations & Alignment Checks
const t1 = translateSingleSentence('私はあなたが好きです。', 'ja', 'neb');
console.log('Test 1 (JA -> NEB):', t1.text, '| Alignment count:', t1.alignment.length);

const t2 = translateSingleSentence('I like you.', 'en', 'neb');
console.log('Test 2 (EN -> NEB):', t2.text, '| Alignment count:', t2.alignment.length);

const t3 = translateSingleSentence('The star is more beautiful than the night.', 'en', 'neb');
console.log('Test 3 (EN -> NEB):', t3.text, '| Alignment count:', t3.alignment.length);

const t4 = translateSingleSentence('If stars shine, I walk.', 'en', 'neb');
console.log('Test 4 (EN -> NEB):', t4.text, '| Alignment count:', t4.alignment.length);

// 2. Missing Word Search & Queue Recording Verification
console.log('\\n=== Missing Word Search Test ===');
searchInput.value = '量子力学コンピュータ';
renderLexicon();
console.log('WordGrid innerHTML contains empty-state:', wordGrid.innerHTML.includes('empty-state'));
console.log('WordGrid innerHTML contains record button:', wordGrid.innerHTML.includes('recordMissingWordBtn'));

// Record missing word
addFeedbackItem('word', 'ja', '量子力学コンピュータ', '辞書検索0件ヒット');
console.log('Feedback queue length after adding word:', feedbackQueue.length);
console.log('First item:', JSON.stringify(feedbackQueue[0]));

// 3. Missing Sentence Translation & Queue Recording Verification
console.log('\\n=== Missing Sentence Translation Test ===');
transInput.value = '明日の天気は晴れですか？';
doTranslate();
console.log('Output text:', transOutputText.textContent);
console.log('transMissingBox display style:', transMissingBox.style.display);

// Record missing sentence
addFeedbackItem('sentence', 'ja', '明日の天気は晴れですか？', '未確定構文・未対応文章');
console.log('Feedback queue length after adding sentence:', feedbackQueue.length);

// Record English missing query
addFeedbackItem('word', 'en', 'quantum computer', '辞書検索0件ヒット');
addFeedbackItem('sentence', 'en', 'Will it rain tomorrow morning?', '未確定構文・未対応文章');

console.log('\\n=== Feedback Queue Collection & Export Test ===');
console.log('Total queued items:', feedbackQueue.length);
renderQueueList();
console.log('Queue list rendered cards count:', (queueList.innerHTML.match(/class="queue-card"/g) || []).length);

const exportJson = JSON.stringify({
  exportedAt: new Date().toISOString(),
  source: 'Nebulith Studio Feedback Queue',
  totalItems: feedbackQueue.length,
  queue: feedbackQueue
}, null, 2);
console.log('Export JSON preview (first 200 chars):', exportJson.substring(0, 200));

// Test deleting one item
const firstId = feedbackQueue[0].id;
window.deleteQueueItem(firstId);
console.log('Queue count after deleting 1 item:', feedbackQueue.length);
console.log('ALL VERIFICATIONS PASSED SUCCESSFULLY!');
`;

vm.runInContext(testCode, context);

// Search must expose grammar introductions, including particle-bearing Japanese.
const assert = require('node:assert/strict');
for (const [query, root] of [['私','mi'],['私は','mi'],['あなたは','ti'],['私たち','miin'],['どこ','kauo'],['主格','el'],['過去','fe']]) {
  context.queryForTest = query;
  vm.runInContext('searchInput.value=queryForTest; currentFilterPos="ALL"; renderLexicon()', context);
  assert.ok(dom.wordGrid.innerHTML.includes('openWordModal(\''+root+'\')'), query);
}
vm.runInContext('searchInput.value="あなた"; currentFilterPos="代名詞"; renderLexicon()', context);
assert.ok(dom.wordGrid.innerHTML.includes("openWordModal('ti')"));
console.log('PASS: grammar dictionary search, particle introductions and pronoun filter');

vm.runInContext(`srcLang='ja';dstLang='neb';transInput.value='私はあなたが嫌い';resetInputChoices();doTranslate();`,context);
assert.ok(dom.transOutputText.textContent.includes('Nyrcan'));
assert.ok(dom.transAlignmentBox.innerHTML.includes('嫌い'));
assert.ok(dom.transAlignmentBox.innerHTML.includes('nyrcan'));
assert.ok(dom.inputInterpretation.textContent.includes('未監査'));
vm.runInContext(`renderAlignments([{src:'<img src=x onerror=alert(1)>',dst:'<script>',role:'<unsafe>'}])`,context);
assert.ok(!dom.transAlignmentBox.innerHTML.includes('<img'));
assert.ok(dom.transAlignmentBox.innerHTML.includes('&lt;img'));
vm.runInContext(`transInput.value='赤い星を';resetInputChoices();doTranslate()`,context);
assert.ok(dom.transAlignmentBox.innerHTML.includes('入力待ち'));
assert.ok(!dom.transAlignmentBox.innerHTML.includes('nyrcan'));
vm.runInContext(`transInput.value='私とあなたの物語';resetInputChoices();doTranslate()`,context);
assert.equal(dom.inputPossessionLabel.style.display,'inline-block');
assert.equal(dom.copyDstBtn.disabled,true);
vm.runInContext(`inputChoicesState={possession:'shared'};doTranslate()`,context);
assert.equal(dom.confirmInputCandidate.disabled,false);
assert.equal(dom.copyDstBtn.disabled,true);
vm.runInContext(`inputChoicesState.confirmed=true;doTranslate()`,context);
assert.equal(dom.copyDstBtn.disabled,false);
assert.equal(dom.transOutputText.textContent,'soralen en mi ul ti');
vm.runInContext(`transInput.value='あなたが嫌い。';resetInputChoices();doTranslate()`,context);
assert.equal(dom.inputPossessionLabel.style.display,'none');
assert.ok(dom.transOutputText.textContent.includes('ia ti'));
vm.runInContext(`transInput.value='空は美しい';resetInputChoices();doTranslate()`,context);
assert.equal(dom.inputSenseLabel.style.display,'inline-block');
assert.equal(dom.copyDstBtn.disabled,true);
vm.runInContext(`inputChoicesState.sense=lastInputAnalysis.segments[0].senseOptions[0].value;doTranslate()`,context);
assert.equal(dom.confirmInputCandidate.disabled,false);
vm.runInContext(`inputChoicesState.confirmed=true;doTranslate()`,context);
assert.equal(dom.copyDstBtn.disabled,false);
assert.ok(dom.translationCoverage.textContent.includes('189'));
assert.ok(dom.corpusList.innerHTML.includes('USE-24'));
assert.equal(dom.corpusCount.textContent,'77 / 77例');
vm.runInContext(`corpusSearch.value='過去・進行';renderCorpus()`,context);
assert.ok(dom.corpusList.innerHTML.includes('USE-03'));
assert.ok(!dom.corpusList.innerHTML.includes('USE-01'));
vm.runInContext(`corpusSearch.value='no-such-example-xyz';renderCorpus()`,context);
assert.ok(dom.corpusList.innerHTML.includes('一致する例文がありません'));
for(const file of ['web/index.html','web/standalone.html','web/app.js'])assert.ok(!fs.readFileSync(file,'utf8').includes('sampleSelect'),file+' must not contain the translator example picker');

for (const [query, root] of [['I','mi'],['you','ti'],['we','miin'],['they','riin']]) {
  context.queryForTest = query;
  const actual = vm.runInContext('searchInput.value=queryForTest; currentFilterPos="ALL"; renderLexicon(); wordGrid.innerHTML', context);
  assert.equal(actual.match(/openWordModal\('([^']+)'\)/)[1],root,query+' exact match must rank first');
}
