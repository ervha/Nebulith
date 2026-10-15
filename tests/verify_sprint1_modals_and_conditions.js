const fs = require('fs'), vm = require('vm'), assert = require('node:assert/strict');

const ctx = {};
vm.createContext(ctx);
vm.runInContext(fs.readFileSync('web/data.js', 'utf8'), ctx);
vm.runInContext(fs.readFileSync('web/incremental.js', 'utf8'), ctx);
const engine = vm.runInContext('createIncrementalTranslator(VOCAB, GRAMMAR_FRAMES, INPUT_RULES.aliases, CANON.map(c=>({ja:c.ja,ja_variants:[c.ja],neb:c.neb})), TRANSLATION_EXTENSIONS)', ctx);

console.log('=== Verifying Milestone 1 / Sprint 1: Modals & Conditional Clauses ===\n');

// 1. 条件節（Sen ...: 〜ば、〜たら、〜なら、もし〜）
console.log('--- 1. Conditional Clauses (Sen) ---');
{
  // (a) 仮定形「〜ば」
  const res = engine.analyze('星が輝けば、私は家へ歩く。');
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Sen falun el vyr, poran el mi to govan.');
  console.log('PASS: 「星が輝けば、私は家へ歩く。」 -> ' + res.text + ' (正本文型と完全合致)');
}

{
  // (b) 完了条件「〜たら」
  const res = engine.analyze('星が輝いたら、私は歩く。');
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Sen fe falun el vyr, poran el mi.');
  console.log('PASS: 「星が輝いたら、私は歩く。」 -> ' + res.text);
}

{
  // (c) 条件接頭辞「もし〜なら」
  const res = engine.analyze('もし星が輝くなら、私は歩く。');
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Sen falun el vyr, poran el mi.');
  assert.ok(res.notes.some(n => n.includes('もし')));
  console.log('PASS: 「もし星が輝くなら、私は歩く。」 -> ' + res.text + ' (「もし」装飾認識)');
}

{
  // (d) 途中入力ドラフト「星が輝けば」
  const res = engine.analyze('星が輝けば');
  assert.equal(res.segments[0].state, 'draft');
  assert.equal(res.segments[0].text, 'Sen falun el vyr');
  assert.ok(res.text.includes('Sen falun el vyr'));
  assert.ok(res.notes.some(n => n.includes('条件節として解釈')));
  console.log('PASS: ドラフト「星が輝けば」 -> ' + res.segments[0].text + ' (主節待ちドラフト)');
}

// 2. 譲歩節（Tor ...: 〜ても、〜でも、〜けれど）
console.log('\n--- 2. Concessive Clauses (Tor) ---');
{
  // (a) 否定譲歩「〜なくても」
  const res = engine.analyze('星が輝かなくても、私は家へ歩く。');
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Tor ne falun el vyr, poran el mi to govan.');
  console.log('PASS: 「星が輝かなくても、私は家へ歩く。」 -> ' + res.text + ' (正本文型と完全合致)');
}

{
  // (b) 肯定譲歩「〜ても」
  const res = engine.analyze('星が輝いても、私は眠る。');
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Tor falun el vyr, tymis el mi.');
  console.log('PASS: 「星が輝いても、私は眠る。」 -> ' + res.text);
}

// 3. 時間節（Hav ...: 〜とき、〜ときに）
console.log('\n--- 3. Temporal Clauses (Hav) ---');
{
  const res = engine.analyze('星が輝くとき、私は星を観測する。');
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Hav falun el vyr, vyrel el mi ia vyr.');
  console.log('PASS: 「星が輝くとき、私は星を観測する。」 -> ' + res.text + ' (正本文型と完全合致)');
}

{
  const res = engine.analyze('星が輝くときに、私は星を観測する。');
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Hav falun el vyr, vyrel el mi ia vyr.');
  console.log('PASS: 「星が輝くときに、私は星を観測する。」 -> ' + res.text);
}

// 4. モダリティ体系（希望 -ast、可能 -ar、推量 se-）
console.log('\n--- 4. Modality System ---');

// (a) 希望（Desiderative -ast）
{
  // 候補プレビュー
  const cand = engine.analyze('私は歩きたい');
  assert.equal(cand.complete, false);
  assert.equal(cand.candidate, 'Poranast el mi.');
  assert.ok(cand.notes.some(n => n.includes('希望')));
  // 確定
  const conf = engine.analyze('私は歩きたい', { confirmed: true });
  assert.equal(conf.complete, true);
  assert.equal(conf.text, 'Poranast el mi.');
  console.log('PASS: 「私は歩きたい」 -> ' + conf.text + ' (確定時complete: true)');
}

{
  const conf = engine.analyze('私は水を飲みたい', { confirmed: true });
  assert.equal(conf.complete, true);
  assert.equal(conf.text, 'Bionast el mi ia daris.');
  console.log('PASS: 「私は水を飲みたい」 -> ' + conf.text);
}

{
  const conf = engine.analyze('私は歩きたかった', { confirmed: true });
  assert.equal(conf.complete, true);
  assert.equal(conf.text, 'Fe poranast el mi.');
  console.log('PASS: 「私は歩きたかった」 -> ' + conf.text + ' (過去希望 fe ... -ast)');
}

{
  const conf = engine.analyze('私は歩きたくない', { confirmed: true });
  assert.equal(conf.complete, true);
  assert.equal(conf.text, 'Ne poranast el mi.');
  console.log('PASS: 「私は歩きたくない」 -> ' + conf.text + ' (否定希望 ne ... -ast)');
}

// (b) 可能（Potential -ar）
{
  // 活用形「歩ける」
  const conf = engine.analyze('私は歩ける', { confirmed: true });
  assert.equal(conf.complete, true);
  assert.equal(conf.text, 'Poranar el mi.');
  console.log('PASS: 活用可能形「私は歩ける」 -> ' + conf.text + ' (可能接尾辞 -ar)');
}

{
  // 句形式「歩くことができる」
  const conf = engine.analyze('私は歩くことができる', { confirmed: true });
  assert.equal(conf.complete, true);
  assert.equal(conf.text, 'Poranar el mi.');
  console.log('PASS: 句可能形「私は歩くことができる」 -> ' + conf.text);
}

{
  // 可能過去「歩くことができた」
  const conf = engine.analyze('私は歩くことができた', { confirmed: true });
  assert.equal(conf.complete, true);
  assert.equal(conf.text, 'Fe poranar el mi.');
  console.log('PASS: 可能過去「私は歩くことができた」 -> ' + conf.text + ' (過去可能 fe ... -ar)');
}

{
  // 可能否定「歩けない」
  const conf = engine.analyze('私は歩けない', { confirmed: true });
  assert.equal(conf.complete, true);
  assert.equal(conf.text, 'Ne poranar el mi.');
  console.log('PASS: 可能否定「私は歩けない」 -> ' + conf.text + ' (否定可能 ne ... -ar)');
}

{
  // 他動詞の可能表現
  const conf = engine.analyze('私は星を観測できる', { confirmed: true });
  assert.equal(conf.complete, true);
  assert.equal(conf.text, 'Vyrelar el mi ia vyr.');
  console.log('PASS: 他動詞可能「私は星を観測できる」 -> ' + conf.text);
}

// (c) 推量（Conjecture se-）
{
  // 「〜だろう」
  const res = engine.analyze('星が輝くだろう');
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Se falun el vyr.');
  console.log('PASS: 推量直接形「星が輝くだろう」 -> ' + res.text + ' (接頭辞 se-)');
}

{
  // 過去推量「〜ただろう」
  const res = engine.analyze('星が輝いただろう');
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Se fe falun el vyr.');
  console.log('PASS: 過去推量「星が輝いただろう」 -> ' + res.text + ' (se fe ...)');
}

{
  // 否定推量「〜ないだろう」
  const res = engine.analyze('星は輝かないだろう');
  assert.equal(res.complete, true);
  assert.equal(res.text, 'Se ne falun el vyr.');
  console.log('PASS: 否定推量「星は輝かないだろう」 -> ' + res.text + ' (se ne ...)');
}

{
  // 認識的推量「〜かもしれない」
  const conf = engine.analyze('星が輝くかもしれない', { confirmed: true });
  assert.equal(conf.complete, true);
  assert.equal(conf.text, 'Se falun el vyr.');
  console.log('PASS: 認識推量「星が輝くかもしれない」 -> ' + conf.text);
}

console.log('\n=== ALL SPRINT 1 MODAL & CONDITIONAL CLAUSE TESTS PASSED! ===');
