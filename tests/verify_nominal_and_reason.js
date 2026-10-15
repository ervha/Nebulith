const fs = require('fs'), vm = require('vm'), assert = require('node:assert/strict');

const ctx = {};
vm.createContext(ctx);
vm.runInContext(fs.readFileSync('web/data.js', 'utf8'), ctx);
vm.runInContext(fs.readFileSync('web/incremental.js', 'utf8'), ctx);
const engine = vm.runInContext('createIncrementalTranslator(VOCAB, GRAMMAR_FRAMES, INPUT_RULES.aliases, CANON.map(c=>({ja:c.ja,ja_variants:[c.ja],neb:c.neb})), TRANSLATION_EXTENSIONS)', ctx);

console.log('=== Verifying Nominal and Reason Clause Extensions ===');

// 1. 動名詞・行為句（「〜すること」）
{
  const res = engine.analyze('歩くこと');
  assert.equal(res.segments[0].state, 'phrase');
  assert.equal(res.text, 'poran');
  console.log('PASS: 「歩くこと」 -> poran');
}

{
  const res = engine.analyze('星を観測すること');
  assert.equal(res.segments[0].state, 'phrase');
  assert.equal(res.text, 'vyrel ia vyr');
  console.log('PASS: 「星を観測すること」 -> vyrel ia vyr');
}

// 2. 指針・叙述としての「〜することだ」
{
  const res = engine.analyze('歩くことだ');
  assert.equal(res.segments[0].state, 'phrase');
  assert.equal(res.text, 'poran');
  console.log('PASS: 「歩くことだ」（主語なし） -> poran');
}

// 3. 理由節の途中段階（主節待ちの「〜から」「〜だから」）
{
  const res = engine.analyze('星が輝くから');
  assert.equal(res.segments[0].state, 'draft');
  assert.ok(res.text.includes('Zen falun el vyr'));
  assert.ok(res.notes.some(n => n.includes('理由節として解釈')));
  console.log('PASS: 途中案「星が輝くから」 -> Zen falun el vyr (ドラフト保持)');
}

// 4. 「〜から、」「〜だから、」による複文合成
{
  const res = engine.analyze('私は働いたから、私は家で眠る。');
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Zen fe dolar el mi, tymis el mi uo govan.');
  console.log('PASS: 複文「私は働いたから、私は家で眠る。」 -> ' + res.text);
}

{
  const res = engine.analyze('星が輝くから、私は歩く。');
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Zen falun el vyr, poran el mi.');
  console.log('PASS: 複文「星が輝くから、私は歩く。」 -> ' + res.text);
}

{
  // 主語未指定の節を含む場合は安全にドラフト保持
  const res = engine.analyze('夜だから、私は眠る。');
  assert.equal(res.segments[0].state, 'draft');
  assert.ok(res.notes.some(n => n.includes('理由節の未確定部分を保持')));
  console.log('PASS: 主語未指定を含む複文「夜だから、私は眠る。」 -> 安全にドラフト保持');
}

console.log('ALL NOMINAL AND REASON VERIFICATIONS PASSED SUCCESSFULLY!');
