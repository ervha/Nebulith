const fs = require('fs');
const vm = require('vm');
const assert = require('node:assert/strict');

console.log('=== Verifying Simple Dictionary Details and Sourced Examples ===\n');

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
    classList: {
      items: new Set(),
      add(c) { this.items.add(c); },
      remove(c) { this.items.delete(c); },
      toggle(c) { if (this.items.has(c)) { this.items.delete(c); return false; } else { this.items.add(c); return true; } },
      contains(c) { return this.items.has(c); }
    },
    addEventListener(event, fn) { listeners[event] = fn; },
    click() { if (listeners['click']) listeners['click']({ stopPropagation: () => {} }); },
    setAttribute() {},
    getAttribute() { return ''; },
    style: { setProperty(k, v) { this[k] = v; } }
  };
}

const context = {
  document: {
    documentElement: mockElement('html'),
    body: mockElement('body'),
    getElementById(id) {
      if (!dom[id]) dom[id] = mockElement(id);
      return dom[id];
    },
    querySelector(sel) {
      if (sel === '[data-tab="translator"]') return this.getElementById('translatorTab');
      if (sel === '[data-tab="lexicon"]') return this.getElementById('lexiconTab');
      return mockElement(sel);
    },
    querySelectorAll(sel) {
      return [this.getElementById('translatorTab'), this.getElementById('lexiconTab')];
    }
  },
  localStorage: localStorage,
  window: {},
  console: console,
  setTimeout: (fn) => fn(),
  clearTimeout: () => {},
  navigator: { clipboard: { writeText: () => Promise.resolve() } },
  alert: () => {},
  confirm: () => true
};
context.window = context;

vm.createContext(context);
vm.runInContext(fs.readFileSync('web/data.js', 'utf8'), context);
vm.runInContext(fs.readFileSync('web/workspace.js', 'utf8'), context);
vm.runInContext(fs.readFileSync('web/incremental.js', 'utf8'), context);
vm.runInContext(fs.readFileSync('web/app.js', 'utf8'), context);

const vocab = vm.runInContext('VOCAB', context);
console.log(`Checking modal enrichment for ALL ${vocab.length} words in dictionary...`);

let missingForms = 0;
let missingExamples = 0;
let missingKana = 0;
let missingPronGuide = 0;
let missingSyntaxRole = 0;

for (let i = 0; i < vocab.length; i++) {
  const w = vocab[i];
  context.openWordModal(w.r);

  assert.equal(dom.modalLiteraryField.style.display,'block');
  assert.ok(dom.modalLiteraryQuote.textContent.includes(w.r));
  assert.ok(dom.modalLiterarySource.innerHTML.includes('VL-'));

  // Check Kana
  if (!dom.modalKana.textContent || dom.modalKana.textContent.trim() === '') {
    missingKana++;
  }

  // Check Pronunciation Guide
  if (!dom.modalPronGuide.textContent || dom.modalPronGuide.textContent.trim() === '') {
    missingPronGuide++;
  }

  // Check Syntax Role
  if (!dom.modalSyntaxRole.textContent || dom.modalSyntaxRole.textContent.trim() === '') {
    missingSyntaxRole++;
  }

  // Check Forms (must be visible and have children)
  if (dom.modalFormsField.style.display !== 'block' || !dom.modalFormsList.innerHTML.includes('modal-form-chip')) {
    missingForms++;
  }

  const expected=vm.runInContext(`getWordCorpusExamples(${JSON.stringify(w.r)},VOCAB.find(w=>w.r===${JSON.stringify(w.r)}))`,context);
  assert.equal(dom.modalExamplesField.style.display,expected.length?'block':'none');
  if (!expected.length) missingExamples++;

}

console.log(`\nAudit Results across ${vocab.length} words:`);
console.log(`- Missing Kana Pronunciation: ${missingKana} (Target: 0)`);
console.log(`- Missing Phonetics Guide: ${missingPronGuide} (Target: 0)`);
console.log(`- Missing Syntax Role: ${missingSyntaxRole} (Target: 0)`);
console.log(`- Missing Conjugations / Forms: ${missingForms} (Target: 0)`);
console.log(`- Missing Exemplary Usages: ${missingExamples} (expected for words without sourced examples)`);

assert.equal(missingKana, 0, 'Every word must have katakana pronunciation guide');
assert.equal(missingPronGuide, 0, 'Every word must have phonetics guide');
assert.equal(missingSyntaxRole, 0, 'Every word must have syntax role description');
assert.equal(missingForms, 0, 'Every word must have forms / conjugations / syntax chips');
assert.ok(missingExamples>0,'Do not invent examples to fill missing coverage');
assert.ok(!fs.readFileSync('web/index.html','utf8').includes('modalAuditBadge'));
assert.ok(!fs.readFileSync('web/index.html','utf8').includes('modalProvenance'));

console.log('PASS: all word modals open; source-backed examples only; audit/provenance badges removed');
