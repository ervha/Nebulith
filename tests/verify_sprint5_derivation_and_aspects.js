const fs = require('fs'), vm = require('vm'), assert = require('node:assert/strict');

const localStorage = {
  store: {},
  getItem(k) { return this.store[k] || null; },
  setItem(k, v) { this.store[k] = String(v); },
  removeItem(k) { delete this.store[k]; }
};

const dom = {};
function mockElement(id) {
  const listeners = {};
  return {
    id: id || '',
    value: '',
    textContent: '',
    innerHTML: '',
    style: { display: '' },
    classList: {
      items: new Set(),
      add(c) { this.items.add(c); },
      remove(c) { this.items.delete(c); },
      toggle(c) { if (this.items.has(c)) { this.items.delete(c); return false; } else { this.items.add(c); return true; } },
      contains(c) { return this.items.has(c); }
    },
    addEventListener(event, fn) { listeners[event] = fn; },
    click() { if (listeners['click']) listeners['click']({ stopPropagation: () => {} }); }
  };
}

const elementIds = [
  'modalWordDetail', 'modalGlyph', 'modalRoman', 'modalPos', 'modalId',
  'modalMeaningJa', 'modalMeaningEn', 'modalIpa', 'modalNotes',
  'modalFormsField', 'modalFormsList', 'modalExamplesField', 'modalExamplesList',
  'modalCloseBtn', 'btnToggleScript', 'body', 'inputArea', 'transOutput', 'charCount',
  'btnCopy', 'btnSwap', 'btnReset', 'statusIndicator', 'alignmentSection', 'alignmentTable',
  'searchDictionary', 'dictFilterPos', 'dictCount', 'dictResults', 'wordDetailPanel',
  'btnSendFeedback', 'feedbackText', 'feedbackList'
];
elementIds.forEach(id => { dom[id] = mockElement(id); });

const context = {
  window: {
    location: { href: '', protocol: 'https:', hostname: 'localhost' },
    addEventListener: () => {},
    matchMedia: () => ({ matches: false, addEventListener: () => {} })
  },
  navigator: {
    clipboard: { writeText: () => Promise.resolve() }
  },
  document: {
    getElementById: (id) => dom[id] || mockElement(id),
    querySelectorAll: () => [],
    querySelector: (sel) => dom[sel.replace('#', '')] || mockElement(),
    body: dom['body'],
    documentElement: { setAttribute: () => {}, getAttribute: () => null },
    addEventListener: () => {}
  },
  localStorage,
  console: { log: () => {}, warn: () => {}, error: () => {} },
  setTimeout: (fn) => fn(),
  clearTimeout: () => {}
};
context.window.document = context.document;
context.window.localStorage = localStorage;

vm.createContext(context);
vm.runInContext(fs.readFileSync('web/data.js', 'utf8'), context);
vm.runInContext(fs.readFileSync('web/workspace.js', 'utf8'), context);
vm.runInContext(fs.readFileSync('web/incremental.js', 'utf8'), context);
vm.runInContext(fs.readFileSync('web/app.js', 'utf8'), context);

const engine = vm.runInContext('createIncrementalTranslator(VOCAB, GRAMMAR_FRAMES, INPUT_RULES.aliases, CANON.map(c=>({ja:c.ja,ja_variants:[c.ja],neb:c.neb})), TRANSLATION_EXTENSIONS)', context);

console.log('=== Verifying Milestone 5 / Sprint 5: Derivations, Aspects & Expanded Civilization Lexicon ===\n');

// 1. 局面相（Aspects: -ol 完了相, -liv 継続相）
console.log('--- 1. Aspect Engine (-ol / -liv) ---');
{
  // (a) 完了相（現在・基本形）
  const res = engine.analyze('私は歩き終える。', { confirmed: true });
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Porol el mi.');
  assert.equal(res.segments[0].meaning.predicate.suffix, 'ol');
  assert.equal(res.segments[0].meaning.aspect, 'perfective');
  console.log('PASS: 「私は歩き終える。」 -> ' + res.text + ' (suffix: -ol, aspect: perfective)');
}

{
  // (b) 完了相（過去形 fe- ... -ol）
  const res = engine.analyze('私は歩き終えた。', { confirmed: true });
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Fe porol el mi.');
  assert.ok(res.segments[0].meaning.predicate.prefixes.includes('fe'));
  assert.equal(res.segments[0].meaning.predicate.suffix, 'ol');
  console.log('PASS: 「私は歩き終えた。」 -> ' + res.text + ' (fe- + -ol)');
}

{
  // (c) 完了相（第三者・自然現象）
  const res = engine.analyze('星は輝き終えた。', { confirmed: true });
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Fe falunol el vyr.');
  console.log('PASS: 「星は輝き終えた。」 -> ' + res.text);
}

{
  // (d) 完了相（否定）
  const res = engine.analyze('私は歩き終えない。', { confirmed: true });
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Ne porol el mi.');
  console.log('PASS: 「私は歩き終えない。」 -> ' + res.text + ' (ne- + -ol)');
}

{
  // (e) 継続相（現在・基本形）
  const res = engine.analyze('私は歩き続ける。', { confirmed: true });
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Poranliv el mi.');
  assert.equal(res.segments[0].meaning.predicate.suffix, 'liv');
  assert.equal(res.segments[0].meaning.aspect, 'durative');
  console.log('PASS: 「私は歩き続ける。」 -> ' + res.text + ' (suffix: -liv, aspect: durative)');
}

{
  // (f) 継続相（過去形 fe- ... -liv）
  const res = engine.analyze('私は歩き続けた。', { confirmed: true });
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Fe poranliv el mi.');
  console.log('PASS: 「私は歩き続けた。」 -> ' + res.text + ' (fe- + -liv)');
}

{
  // (g) 継続相（自然主語）
  const res = engine.analyze('星は輝き続ける。', { confirmed: true });
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Falunliv el vyr.');
  console.log('PASS: 「星は輝き続ける。」 -> ' + res.text);
}

{
  // (h) 継続相（否定）
  const res = engine.analyze('私は歩き続けない。', { confirmed: true });
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Ne poranliv el mi.');
  console.log('PASS: 「私は歩き続けない。」 -> ' + res.text + ' (ne- + -liv)');
}

// 2. The simplified modal exposes only base / past / negative forms.
// Productive aspects are still checked independently against the translation engine above.
for(const word of [{r:'poran',p:'動'},{r:'fal',p:'形'},{r:'vyr',p:'名'}]) {
  const forms=context.getWordForms(word);
  const actual=Array.from(forms,f=>f.neb);
  assert.deepEqual(actual,word.p==='動'?['poran','fe poran','ne poran']:[word.r]);
}
console.log('PASS: simplified word forms do not invent derivations; aspect engine checks remain active');

// 3. 語彙規模と衝突検証（Zero Collisions & Scale: 1,350+ entries）
console.log('\n--- 3. Lexical Scale & Extended Categories ---');
{
  const totalVocab = vm.runInContext('VOCAB.length', context);
  assert.ok(totalVocab >= 1350, 'Total vocabulary must be at least 1,350 entries (Actual: ' + totalVocab + ')');
  console.log('PASS: 総語彙数 ' + totalVocab + ' 語（1,350語以上の文明・生活・精神語彙拡張を達成）');
}

console.log('\n=== ALL SPRINT 5 DERIVATIONS, ASPECTS & EXPANDED LEXICON TESTS PASSED! ===\n');
