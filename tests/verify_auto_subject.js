const fs = require('fs'), vm = require('vm'), assert = require('node:assert/strict');

const ctx = {};
vm.createContext(ctx);
vm.runInContext(fs.readFileSync('web/data.js', 'utf8'), ctx);
vm.runInContext(fs.readFileSync('web/incremental.js', 'utf8'), ctx);
const engine = vm.runInContext('createIncrementalTranslator(VOCAB, GRAMMAR_FRAMES, INPUT_RULES.aliases, CANON.map(c=>({ja:c.ja,ja_variants:[c.ja],neb:c.neb})), TRANSLATION_EXTENSIONS)', ctx);

console.log('=== Verifying Auto Subject (私) Insertion ===');

// 1. 自動詞単体
{
  const res = engine.analyze('歩く');
  assert.equal(res.segments[0].state, 'candidate');
  assert.equal(res.segments[0].candidate, 'Poran el mi.');
  assert.ok(res.notes.some(n => n.includes('主語未指定のため「私」を自動補完')));
  console.log('PASS: 「歩く」 -> Poran el mi. (自動補完)');
}

// 2. 場所格を伴う自動詞
{
  const res = engine.analyze('家で眠る');
  assert.equal(res.segments[0].state, 'candidate');
  assert.equal(res.segments[0].candidate, 'Tymis el mi uo govan.');
  console.log('PASS: 「家で眠る」 -> Tymis el mi uo govan. (自動補完)');
}

// 3. 目的語（対象格）を伴う他動詞
{
  const res = engine.analyze('星を観測する');
  assert.equal(res.segments[0].state, 'candidate');
  assert.equal(res.segments[0].candidate, 'Vyrel el mi ia vyr.');
  console.log('PASS: 「星を観測する」 -> Vyrel el mi ia vyr. (自動補完)');
}

// 4. 感情構文（対象格指定・主語未指定）
{
  const res = engine.analyze('あなたが嫌い');
  assert.equal(res.segments[0].state, 'candidate');
  assert.equal(res.segments[0].candidate, 'Nyrcan el mi ia ti.');
  console.log('PASS: 「あなたが嫌い」 -> Nyrcan el mi ia ti. (自動補完)');
}

// 5. 主語省略の複文（両節ともに「私」を補完）
{
  const res = engine.analyze('働いたから、眠る。');
  assert.equal(res.segments[0].state, 'candidate');
  assert.equal(res.segments[0].candidate, 'Zen fe dolar el mi, tymis el mi.');
  console.log('PASS: 「働いたから、眠る。」 -> Zen fe dolar el mi, tymis el mi. (両節自動補完)');
}

// 6. ユーザーが明示的に別主語を指定した場合はそれを尊重
{
  const res = engine.analyze('歩く', {subject: 'あなた', confirmed: true});
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Poran el ti.');
  console.log('PASS: 「歩く」 + choices.subject="あなた" -> Poran el ti. (明示指定を優先)');
}

console.log('ALL AUTO SUBJECT TESTS PASSED SUCCESSFULLY!');
