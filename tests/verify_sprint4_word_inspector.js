const fs = require('fs');
const vm = require('vm');
const assert = require('node:assert/strict');

console.log('=== Verifying Milestone 4 / Sprint 4: Dictionary Inspector & Astral Script ===\n');

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

// 1. 動詞の単語モーダル検査（Conjugations）
console.log('--- 1. Verb Word Detail Modal & Conjugation Generator ---');
{
  context.openWordModal('poran'); // 歩く
  assert.equal(dom.modalRoman.textContent, 'poran');
  assert.equal(dom.modalPos.textContent, '動');
  assert.equal(dom.wordModal.classList.contains('active'), true);
  assert.equal(dom.modalFormsField.style.display, 'block');

  const formsHtml = dom.modalFormsList.innerHTML;
  assert.ok(formsHtml.includes('fe poran'), 'Must include past fe poran');
  assert.ok(formsHtml.includes('ne poran'), 'Must include negative ne poran');
  assert.ok(formsHtml.includes('poranast'), 'Must include desiderative -ast');
  assert.ok(formsHtml.includes('poranar'), 'Must include potential -ar');
  assert.ok(formsHtml.includes('se poran'), 'Must include conjecture se-');
  console.log('PASS: poran (歩く) - 全活用形・モダリティバッジが動的に正常生成');
}

// 2. 形容詞の単語モーダル検査（Superlative & Comparison）
console.log('\n--- 2. Adjective Word Detail Modal ---');
{
  context.openWordModal('cylani'); // 美しい
  assert.equal(dom.modalRoman.textContent, 'cylani');
  assert.equal(dom.modalPos.textContent, '形');
  const formsHtml = dom.modalFormsList.innerHTML;
  assert.ok(formsHtml.includes('celcylani'), 'Must include superlative celcylani');
  console.log('PASS: cylani (美しい) - 最上級 celcylani が正常生成');
}

// 3. 名詞の単語モーダル検査（Plural & Case Forms）
console.log('\n--- 3. Noun Word Detail Modal ---');
{
  context.openWordModal('vyr'); // 星
  assert.equal(dom.modalRoman.textContent, 'vyr');
  assert.equal(dom.modalPos.textContent, '名');
  const formsHtml = dom.modalFormsList.innerHTML;
  assert.ok(formsHtml.includes('vyriin'), 'Must include plural -iin');
  assert.ok(formsHtml.includes('en vyr'), 'Must include genitive en vyr');
  console.log('PASS: vyr (星) - 複数形 vyriin および格助詞例が正常生成');
}

// 4. 共起例文の抽出と表示（Contextual Examples）
console.log('\n--- 4. Contextual Corpus Examples Extraction ---');
{
  context.openWordModal('falun'); // 輝く
  assert.equal(dom.modalExamplesField.style.display, 'block');
  const exHtml = dom.modalExamplesList.innerHTML;
  assert.ok(exHtml.includes('Falun') || exHtml.includes('falun'), 'Must include sentences containing falun');
  assert.ok(exHtml.includes('正本カノン') || exHtml.includes('拡張文') || exHtml.includes('学習例文'), 'Must show source tag');
  console.log('PASS: falun (輝く) - コーパス例文の自動抽出・出典表示が正常動作');
}

// 5. 例文クリックによる翻訳ボックス連動（loadExampleToTranslator）
console.log('\n--- 5. Load Example to Translator Interaction ---');
{
  context.loadExampleToTranslator('星は夜より美しい。');
  assert.equal(dom.transInput.value, '星は夜より美しい。');
  assert.equal(dom.translatorTab.classList.contains('active'), true);
  assert.equal(dom.wordModal.classList.contains('active'), false);
  console.log('PASS: loadExampleToTranslator - 翻訳タブへの例文ロードとモーダルクローズが正常連動');
}

// 6. 星文字フォント切替ボタンの整理・削除検証
console.log('\n--- 6. Font Toggle Button Cleaned ---');
{
  // Button logic removed to simplify UI as requested
  const appJsContent = fs.readFileSync('web/app.js', 'utf8');
  assert.ok(!appJsContent.includes('id="astralToggleBtn"'), 'astralToggleBtn must not be active in web/app.js');
  console.log('PASS: astralToggleBtn successfully cleaned and removed from UI');
}

// 7. アライメント表示での単語クリック連携（Interactive Alignment）
console.log('\n--- 7. Interactive Alignment Clickable Words ---');
{
  context.renderAlignments([
    { src: '星', dst: 'vyr', role: '主体' },
    { src: '輝く', dst: 'falun', role: '述語' }
  ]);
  const alignHtml = dom.transAlignmentBox.innerHTML;
  assert.ok(alignHtml.includes('class="align-dst has-word"'), 'Must add has-word class to known vocabulary');
  assert.ok(alignHtml.includes('onclick="openWordModal(\'vyr\')"'), 'Must attach openWordModal click handler for vyr');
  assert.ok(alignHtml.includes('onclick="openWordModal(\'falun\')"'), 'Must attach openWordModal click handler for falun');
  console.log('PASS: renderAlignments - アライメントチップから単語詳細モーダルへの直接起動連携が正常動作');
}

console.log('\n=== ALL SPRINT 4 DICTIONARY INSPECTOR & ASTRAL SCRIPT TESTS PASSED! ===\n');
