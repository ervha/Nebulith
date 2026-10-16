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

// 1. 局面相（Aspects: -far 完了相, -liv 継続相）
console.log('--- 1. Aspect Engine (-far / -liv) ---');
{
  // (a) 完了相（現在・基本形）
  const res = engine.analyze('私は歩き終える。', { confirmed: true });
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Poranfar el mi.');
  assert.equal(res.segments[0].meaning.predicate.suffix, 'far');
  assert.equal(res.segments[0].meaning.aspect, 'perfective');
  console.log('PASS: 「私は歩き終える。」 -> ' + res.text + ' (suffix: -far, aspect: perfective)');
}

{
  // (b) 完了相（過去形 fe- ... -far）
  const res = engine.analyze('私は歩き終えた。', { confirmed: true });
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Fe poranfar el mi.');
  assert.ok(res.segments[0].meaning.predicate.prefixes.includes('fe'));
  assert.equal(res.segments[0].meaning.predicate.suffix, 'far');
  console.log('PASS: 「私は歩き終えた。」 -> ' + res.text + ' (fe- + -far)');
}

{
  // (c) 完了相（第三者・自然現象）
  const res = engine.analyze('星は輝き終えた。', { confirmed: true });
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Fe falunfar el vyr.');
  console.log('PASS: 「星は輝き終えた。」 -> ' + res.text);
}

{
  // (d) 完了相（否定）
  const res = engine.analyze('私は歩き終えない。', { confirmed: true });
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Ne poranfar el mi.');
  console.log('PASS: 「私は歩き終えない。」 -> ' + res.text + ' (ne- + -far)');
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

// 2. 形態論派生と単語フォーム生成（Word Inspector Derivation Engine）
console.log('\n--- 2. Morphological Derivation in Word Inspector ---');
{
  // 動詞の派生形テスト（poran: 歩く）
  const forms = context.getWordForms({ r: 'poran', p: '動' });
  const formLabels = forms.map(f => f.label);
  const formNebs = forms.map(f => f.neb);
  
  assert.ok(formLabels.includes('完了相 (-far)'), 'Must include -far');
  assert.ok(formLabels.includes('継続維持相 (-liv)'), 'Must include -liv');
  assert.ok(formLabels.includes('派生名詞・抽象化 (-as)'), 'Must include -as');
  assert.ok(formLabels.includes('派生行為者 (-or)'), 'Must include -or');
  assert.ok(formLabels.includes('派生空間・施設 (-om)'), 'Must include -om');
  assert.ok(formLabels.includes('派生器具・装置 (-ik)'), 'Must include -ik');

  assert.ok(formNebs.includes('poranfar'));
  assert.ok(formNebs.includes('poranliv'));
  assert.ok(formNebs.includes('poranas'));
  assert.ok(formNebs.includes('poranor'));
  assert.ok(formNebs.includes('poranom'));
  assert.ok(formNebs.includes('poranik'));
  console.log('PASS: 動詞 poran からの 6大派生接尾辞 (-far, -liv, -as, -or, -om, -ik) の自動生成を確認');
}

{
  // 形容詞の派生形テスト（fal: 輝かしい）
  const forms = context.getWordForms({ r: 'fal', p: '形' });
  const formNebs = forms.map(f => f.neb);
  assert.ok(formNebs.includes('celfal'), 'Must include superlative cel-');
  assert.ok(formNebs.includes('falas'), 'Must include abstract -as');
  assert.ok(formNebs.includes('falin'), 'Must include adverbial -in');
  console.log('PASS: 形容詞 fal からの派生形 (celfal, falas, falin) の生成を確認');
}

{
  // 名詞の派生形テスト（vyr: 星）
  const forms = context.getWordForms({ r: 'vyr', p: '名' });
  const formNebs = forms.map(f => f.neb);
  assert.ok(formNebs.includes('vyriin'), 'Must include plural -iin');
  assert.ok(formNebs.includes('vyrik'), 'Must include adjectival -ik');
  assert.ok(formNebs.includes('vyrom'), 'Must include collective -om');
  console.log('PASS: 名詞 vyr からの派生形 (vyriin, vyrik, vyrom) の生成を確認');
}

// 3. 語彙規模と衝突検証（Zero Collisions & Scale: 1,350+ entries）
console.log('\n--- 3. Lexical Scale & Extended Categories ---');
{
  const totalVocab = vm.runInContext('VOCAB.length', context);
  assert.ok(totalVocab >= 1350, 'Total vocabulary must be at least 1,350 entries (Actual: ' + totalVocab + ')');
  console.log('PASS: 総語彙数 ' + totalVocab + ' 語（1,350語以上の文明・生活・精神語彙拡張を達成）');
}

console.log('\n=== ALL SPRINT 5 DERIVATIONS, ASPECTS & EXPANDED LEXICON TESTS PASSED! ===\n');
