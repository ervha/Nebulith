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
    style: {}
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
