const fs = require('fs');
const vm = require('vm');

const localStorage = {
  store: {},
  getItem(k) { return this.store[k] || null; },
  setItem(k, v) { this.store[k] = v; }
};

const dom = {};
function mockElement() {
  return {
    value: '',
    textContent: '',
    innerHTML: '',
    classList: { add() {}, remove() {} },
    addEventListener() {},
    setAttribute() {},
    style: {}
  };
}

const context = {
  document: {
    documentElement: mockElement(),
    getElementById(id) {
      if (!dom[id]) dom[id] = mockElement();
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
  alert: console.log
};

vm.createContext(context);

const dataCode = fs.readFileSync('web/data.js', 'utf8');
const appCode = fs.readFileSync('web/app.js', 'utf8');

vm.runInContext(dataCode, context);
vm.runInContext(appCode, context);

const testCode = `
console.log('Vocab count:', VOCAB.length);
console.log('Translation pairs count:', translationPairs.length);

const t1 = translateSingleSentence('私はあなたが好きです。', 'ja', 'neb');
console.log('Test 1 (JA -> NEB):', t1.text, '| Alignment count:', t1.alignment.length);
console.log('  Alignment:', JSON.stringify(t1.alignment));

const t2 = translateSingleSentence('I like you.', 'en', 'neb');
console.log('Test 2 (EN -> NEB):', t2.text, '| Alignment count:', t2.alignment.length);
console.log('  Alignment:', JSON.stringify(t2.alignment));

const t3 = translateSingleSentence('The star is more beautiful than the night.', 'en', 'neb');
console.log('Test 3 (EN -> NEB):', t3.text, '| Alignment count:', t3.alignment.length);

const t4 = translateSingleSentence('If stars shine, I walk.', 'en', 'neb');
console.log('Test 4 (EN -> NEB):', t4.text, '| Alignment count:', t4.alignment.length);

const t5 = translateSingleSentence('Cynel el mi ia ti.', 'neb', 'en');
console.log('Test 5 (NEB -> EN):', t5.text, '| Alignment count:', t5.alignment.length);

const t6 = translateSingleSentence('Cynel el mi ia ti.', 'neb', 'ja');
console.log('Test 6 (NEB -> JA):', t6.text);
`;

vm.runInContext(testCode, context);
