const fs = require('fs'), vm = require('vm'), assert = require('node:assert/strict');

const ctx = {};
vm.createContext(ctx);
vm.runInContext(fs.readFileSync('web/data.js', 'utf8'), ctx);
vm.runInContext(fs.readFileSync('web/incremental.js', 'utf8'), ctx);
const engine = vm.runInContext('createIncrementalTranslator(VOCAB, GRAMMAR_FRAMES, INPUT_RULES.aliases, CANON.map(c=>({ja:c.ja,ja_variants:[c.ja],neb:c.neb})), TRANSLATION_EXTENSIONS)', ctx);

console.log('=== Verifying Expanded Verb Interpretation ===');

// 1. 「見る」グループの解釈切り替え
{
  // 観測する
  const r1 = engine.analyze('私は星を見る', {verb: '観測する', confirmed: true});
  assert.equal(r1.complete, true);
  assert.equal(r1.text, 'Vyrel el mi ia vyr.');
  console.log('PASS: 私は星を見る (観測する) -> Vyrel el mi ia vyr.');

  // 仰ぎ見る
  const r2 = engine.analyze('私は星を見る', {verb: '仰ぎ見る', confirmed: true});
  assert.equal(r2.complete, true);
  assert.equal(r2.text, 'Celan el mi ia vyr.');
  console.log('PASS: 私は星を見る (仰ぎ見る) -> Celan el mi ia vyr.');
}

// 2. 「話す」グループの解釈切り替え
{
  // ささやく
  const r1 = engine.analyze('私は話す', {verb: 'ささやく', confirmed: true});
  assert.equal(r1.complete, true);
  assert.equal(r1.text, 'Fenor el mi.');
  console.log('PASS: 私は話す (ささやく) -> Fenor el mi.');

  // 語り合う
  const r2 = engine.analyze('私は話す', {verb: '語り合う', confirmed: true});
  assert.equal(r2.complete, true);
  assert.equal(r2.text, 'Fenor el mi.');
  console.log('PASS: 私は話す (語り合う) -> Fenor el mi.');
}

// 3. 「行く」グループの解釈切り替え
{
  // 行進する
  const r1 = engine.analyze('私は行く', {verb: '行進する', confirmed: true});
  assert.equal(r1.complete, true);
  assert.equal(r1.text, 'Porcon el mi.');
  console.log('PASS: 私は行く (行進する) -> Porcon el mi.');

  // 歩く
  const r2 = engine.analyze('私は行く', {verb: '歩く', confirmed: true});
  assert.equal(r2.complete, true);
  assert.equal(r2.text, 'Poran el mi.');
  console.log('PASS: 私は行く (歩く) -> Poran el mi.');
}

// 4. 「思う」グループの解釈切り替え
{
  // 信じる
  const r1 = engine.analyze('私は思う', {verb: '信じる', confirmed: true});
  assert.equal(r1.complete, true);
  assert.equal(r1.text, 'Fevas el mi.');
  console.log('PASS: 私は思う (信じる) -> Fevas el mi.');

  // 決断する
  const r2 = engine.analyze('私は思う', {verb: '決断する', confirmed: true});
  assert.equal(r2.complete, true);
  assert.equal(r2.text, 'Minpan el mi.');
  console.log('PASS: 私は思う (決断する) -> Minpan el mi.');
}

console.log('ALL VERB INTERPRETATION TESTS PASSED!');
