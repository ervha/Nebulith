const fs = require('fs'), vm = require('vm'), assert = require('node:assert/strict');

const ctx = {};
vm.createContext(ctx);
vm.runInContext(fs.readFileSync('web/data.js', 'utf8'), ctx);
vm.runInContext(fs.readFileSync('web/incremental.js', 'utf8'), ctx);

const pairs = vm.runInContext(
  'CANON.map(c=>({ja:c.ja,ja_variants:[c.ja],neb:c.neb})).concat(EXT_SENTENCES.map(e=>({ja:e.japanese,ja_variants:(e.japanese_variants||[]).concat([e.japanese]),neb:e.nebulith,alignment:e.alignment||[]})))',
  ctx
);
const engine = vm.runInContext(
  'createIncrementalTranslator(VOCAB, GRAMMAR_FRAMES, INPUT_RULES.aliases, ' + JSON.stringify(pairs) + ', TRANSLATION_EXTENSIONS)',
  ctx
);

console.log('=== Verifying Milestone 1 / Sprint 2: Comparison & Reported Clauses ===\n');

// 1. 比較構文（Ablative Comparison / va）
console.log('--- 1. Comparative Clauses (va) ---');
{
  const res = engine.analyze('星は夜より美しい。');
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Cylani el vyr va valar.');
  console.log('PASS: 「星は夜より美しい。」 -> ' + res.text + ' (EXT-15 カノン文型)');
}

{
  const res = engine.analyze('太陽は星より輝く。');
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Falun el zohar va vyr.');
  console.log('PASS: 「太陽は星より輝く。」 -> ' + res.text + ' (EXT-16 カノン文型)');
}

{
  const res = engine.analyze('私はあなたより歩く。');
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Poran el mi va ti.');
  console.log('PASS: 「私はあなたより歩く。」 -> ' + res.text + ' (任意動詞比較構文)');
}

{
  const res = engine.analyze('太陽は星より輝いた。');
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Fe falun el zohar va vyr.');
  console.log('PASS: 「太陽は星より輝いた。」 -> ' + res.text + ' (過去比較構文)');
}

{
  const res = engine.analyze('太陽は星より輝かない。');
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Ne falun el zohar va vyr.');
  console.log('PASS: 「太陽は星より輝かない。」 -> ' + res.text + ' (否定比較構文)');
}

// 2. 最上級構文（Superlative / cel-）
console.log('\n--- 2. Superlative Expressions (cel-) ---');
{
  const res = engine.analyze('太陽は最も輝く。');
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Celfalun el zohar.');
  console.log('PASS: 「太陽は最も輝く。」 -> ' + res.text + ' (動詞最上級 celfalun)');
}

{
  const res = engine.analyze('星は最も美しい。', { sense: '906:764', confirmed: true });
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Relen el vyr ia celcylani.');
  console.log('PASS: 「星は最も美しい。」 -> ' + res.text + ' (形容詞最上級 celcylani)');
}

{
  const res = engine.analyze('太陽は最も輝いた。');
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Fe celfalun el zohar.');
  console.log('PASS: 「太陽は最も輝いた。」 -> ' + res.text + ' (過去最上級)');
}

{
  const res = engine.analyze('太陽は最も輝かない。');
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Ne celfalun el zohar.');
  console.log('PASS: 「太陽は最も輝かない。」 -> ' + res.text + ' (否定最上級)');
}

// 3. 引用節・思考節（Reported Speech & Thought）
console.log('\n--- 3. Reported Speech & Thought Clauses ---');
{
  const res = engine.analyze('私は「星が輝く」と言った。');
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Fe fenor el mi ia "Falun el vyr."');
  console.log('PASS: 「私は「星が輝く」と言った。」 -> ' + res.text);
}

{
  const res = engine.analyze('私は「星が輝く」と思った。');
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Fe memar el mi ia "Falun el vyr."');
  console.log('PASS: 「私は「星が輝く」と思った。」 -> ' + res.text);
}

{
  const res = engine.analyze('彼が「星が輝く」と言った。');
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Fe fenor el ri ia "Falun el vyr."');
  console.log('PASS: 「彼が「星が輝く」と言った。」 -> ' + res.text + ' (三人称主語 ri)');
}

{
  const res = engine.analyze('星が輝くと言った。');
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Fe fenor el mi ia "Falun el vyr."');
  console.log('PASS: 「星が輝くと言った。」 -> ' + res.text + ' (間接引用・主語自動補完)');
}

{
  const res = engine.analyze('星が輝くと私は言う。');
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Fenor el mi ia "Falun el vyr."');
  console.log('PASS: 「星が輝くと私は言う。」 -> ' + res.text + ' (現在発話間接引用)');
}

console.log('\n=== ALL SPRINT 2 COMPARISON & QUOTE TESTS PASSED! ===\n');
