const fs = require('fs');
const vm = require('vm');
const assert = require('node:assert/strict');

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

console.log('=== Verifying Milestone 2 / Sprint 3: Lexicon & Adverbs Expansion ===\n');

// 1. 副詞修飾構文の検証（Adverbial Modification）
console.log('--- 1. Adverbial Modification (Frequency, Degree, Manner, Time) ---');

// 頻度副詞 (Frequency)
{
  const res = engine.analyze('星はいつも輝く。');
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Havon falun el vyr.');
  console.log('PASS: 「星はいつも輝く。」 -> ' + res.text + ' (頻度副詞 havon)');
}

{
  const res = engine.analyze('星は時々輝く。');
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Havtul falun el vyr.');
  console.log('PASS: 「星は時々輝く。」 -> ' + res.text + ' (頻度副詞 havtul)');
}

// 程度副詞 (Degree)
{
  const res = engine.analyze('星はとても輝く。');
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Solpar falun el vyr.');
  console.log('PASS: 「星はとても輝く。」 -> ' + res.text + ' (程度副詞 solpar)');
}

{
  const res = engine.analyze('太陽は少し輝く。');
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Vyntul falun el zohar.');
  console.log('PASS: 「太陽は少し輝く。」 -> ' + res.text + ' (程度副詞 vyntul)');
}

// 様態副詞 (Manner)
{
  const res = engine.analyze('私はゆっくり歩く。');
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Moril poran el mi.');
  console.log('PASS: 「私はゆっくり歩く。」 -> ' + res.text + ' (様態副詞 moril)');
}

{
  const res = engine.analyze('静かに星を観測する。');
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Sirik vyrel el mi ia vyr.');
  console.log('PASS: 「静かに星を観測する。」 -> ' + res.text + ' (様態副詞 sirik)');
}

{
  const res = engine.analyze('共に歩く。');
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Kulen poran el mi.');
  console.log('PASS: 「共に歩く。」 -> ' + res.text + ' (様態副詞 kulen)');
}

{
  const res = engine.analyze('早く走る。', { verb: '走る', confirmed: true });
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Tasin kupan el mi.');
  console.log('PASS: 「早く走る。」 -> ' + res.text + ' (様態副詞 tasin 迅速)');
}

{
  const res = engine.analyze('独りで思索する。', { verb: '思索する', confirmed: true });
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Minkir memar el mi.');
  console.log('PASS: 「独りで思索する。」 -> ' + res.text + ' (様態副詞 minkir 孤独・単独)');
}

// 時間副詞 (Time)
{
  const res = engine.analyze('すでに星は輝く。');
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Feval falun el vyr.');
  console.log('PASS: 「すでに星は輝く。」 -> ' + res.text + ' (時間副詞 feval 既に)');
}

{
  const res = engine.analyze('すぐに星を観測する。');
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Tasik vyrel el mi ia vyr.');
  console.log('PASS: 「すぐに星を観測する。」 -> ' + res.text + ' (時間副詞 tasik 直ちに)');
}

// 2. 気象・自然動詞と名詞の検証
console.log('\n--- 2. Weather & Natural Verbs/Nouns ---');
{
  const res = engine.analyze('雨が降る。');
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Toren el darlen.');
  console.log('PASS: 「雨が降る。」 -> ' + res.text + ' (正本雨 darlen + 降る toren)');
}

{
  const res = engine.analyze('雪が降る。');
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Toren el kyrlen.');
  console.log('PASS: 「雪が降る。」 -> ' + res.text + ' (正本雪 kyrlen + 降る toren)');
}

{
  const res = engine.analyze('慈雨が降る。');
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Toren el darlan.');
  console.log('PASS: 「慈雨が降る。」 -> ' + res.text + ' (新造慈雨 darlan + 降る toren)');
}

{
  const res = engine.analyze('大雪が降る。');
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Toren el kyrlan.');
  console.log('PASS: 「大雪が降る。」 -> ' + res.text + ' (新造大雪 kyrlan + 降る toren)');
}

// 3. 生活・感情・身体名詞と格助詞の検証
console.log('\n--- 3. Expanded Daily/Emotional Nouns & Case Particles ---');
{
  const res = engine.analyze('まなざしが輝く。');
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Falun el celmir.');
  console.log('PASS: 「まなざしが輝く。」 -> ' + res.text + ' (新造身体名詞 celmir 瞳・まなざし)');
}

{
  const res = engine.analyze('胸の内で感じる。', { verb: '感じる（心身で知覚）', confirmed: true });
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Velrin el mi de civtor.');
  console.log('PASS: 「胸の内で感じる。」 -> ' + res.text + ' (新造心身名詞 civtor + de格)');
}

{
  const res = engine.analyze('心で感じる。', { verb: '感じる（心身で知覚）', confirmed: true });
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Velrin el mi de sylim.');
  console.log('PASS: 「心で感じる。」 -> ' + res.text + ' (正本名詞 sylim + de格)');
}

// 4. 正本語根と新造語の意味重複（Collision）ゼロ検証
console.log('\n--- 4. Lexical Integrity: Zero Collisions Across Lexicon ---');
{
  const vocab = vm.runInContext('VOCAB', ctx);
  const gloss = e => (e.m || '').split(/[、／]/).map(x => x.trim()).filter(Boolean);
  const glossMap = new Map();
  for (const e of vocab) {
    for (const g of gloss(e)) {
      if (!glossMap.has(g)) glossMap.set(g, []);
      glossMap.get(g).push(e);
    }
  }

  const collisions = [];
  for (const [g, list] of glossMap.entries()) {
    const nounOrAdj = list.filter(e => e.p.includes('名') || e.p.includes('形'));
    if (nounOrAdj.length > 1 && nounOrAdj.some(e => e.id >= 30000)) {
      collisions.push({ gloss: g, entries: nounOrAdj.map(e => e.r) });
    }
  }

  assert.equal(collisions.length, 0, 'No collisions should exist between canon roots and extensions!');
  console.log('PASS: Total collisions between canon roots and extended lexicon = 0');
}

console.log('\n=== ALL SPRINT 3 LEXICON & ADVERBS TESTS PASSED! ===\n');
