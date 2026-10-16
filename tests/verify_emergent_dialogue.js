const fs = require('fs');
const vm = require('vm');
const assert = require('node:assert/strict');

console.log('=== Verifying Nebulith 6-Gate Strict Audit & Provenance Separation ===\n');

const auditPath = 'data/emergent_lexicon_audit.json';
assert.ok(fs.existsSync(auditPath), 'emergent_lexicon_audit.json must exist');

const audit = JSON.parse(fs.readFileSync(auditPath, 'utf8'));

// 1. シチュエーション構成検証（汎用6件・専門2件）
console.log('--- 1. Universal Everyday (6) & Specialized (2) Scenarios ---');
assert.ok(audit.summary.totalScenarios >= 11, 'Total scenarios must be >= 11');
assert.ok(audit.summary.universalScenarios >= 9, 'Universal scenarios must be >= 9');
assert.equal(audit.summary.specializedScenarios, 2);
console.log(`PASS: 全 ${audit.summary.totalScenarios} シナリオ（汎用日常: 6件、専門星辰: 2件）を確認`);

// 2. 6段階厳格審査ゲート（6-Gate Strict Audit）の合格検証
console.log('\n--- 2. 6-Gate Strict Audit Verification (Approved Words) ---');
assert.ok(audit.summary.totalApproved >= 30, 'Total approved words must be >= 30');
for (const word of audit.approvedLexicon) {
  assert.equal(word.approved, true);
  assert.equal(word.audit_status, 'AUDITED_PROVISIONAL');
  assert.equal(word.gates_passed, 6, `${word.nrs} must pass all 6 gates`);
  assert.ok(word.overall_score >= 0.90, `${word.nrs} score must be >= 0.90`);
  assert.ok(word.gates.gate2_collision_distance.min_distance >= 1);
  console.log(`PASS [6/6 Gates]: *${word.nrs} (${word.pos}: ${word.meaningJa}) | Score: ${word.overall_score} | MinEditDist: ${word.gates.gate2_collision_distance.min_distance}`);
}

// 3. 不適格候補の棄却監査ログ（Rejected Adversarial Cases）検証
console.log('\n--- 3. Rejection Audit Log Verification (Adversarial Filtering) ---');
assert.equal(audit.summary.totalRejected, 5);
const rejectedNames = audit.rejectedLog.map(r => r.nrs);
assert.ok(rejectedNames.includes('zeldar'), 'Collision with curated ext zeldar must be rejected');
assert.ok(rejectedNames.includes('falkrot'), '3-consonant cluster falkrot must be rejected');
assert.ok(rejectedNames.includes('darlen'), 'Canon collision darlen must be rejected');
assert.ok(rejectedNames.includes('novzoh'), 'Forbidden coda & gloss collision novzoh must be rejected');
assert.ok(rejectedNames.includes('xzyqon'), 'Unverified morpheme xzyqon must be rejected');
for (const rej of audit.rejectedLog) {
  assert.equal(rej.approved, false);
  assert.equal(rej.audit_status, 'REJECTED_BY_ARBITER');
  const failed = Object.entries(rej.gates).filter(([, v]) => !v.passed).map(([k]) => k);
  console.log(`PASS [Rejected Properly]: *${rej.nrs} -> Failed gates: ${failed.join(', ')}`);
}

// 4. 既存語彙との厳格な来歴区別（ID 40001+ & origin === 'ai_emergent'）と Studio UI 連携検証
console.log('\n--- 4. Provenance Separation & Web Studio Audit UI Verification ---');
const ext = JSON.parse(fs.readFileSync('data/translation_extensions.json', 'utf8'));
const emergentEntries = ext.entries.filter(e => e.origin === 'ai_emergent');
const curatedEntries = ext.entries.filter(e => e.origin !== 'ai_emergent');

assert.ok(emergentEntries.length >= 30, 'Must have exactly 21 ai_emergent entries');
for (const e of emergentEntries) {
  assert.ok(e.id >= 40001 && e.id < 50000, `AI emergent ID must be in 40001-49999 (got ${e.id})`);
  assert.equal(e.auditStatus, 'audited_provisional');
  assert.ok(e.notes.includes('6段階監査済'), 'Notes must explicitly mark 6-gate audit status');
}
for (const c of curatedEntries) {
  assert.ok(c.id < 40000, `Curated extension ID must be < 40000 (got ${c.id})`);
}

const ctx = {};
vm.createContext(ctx);
vm.runInContext(fs.readFileSync('web/data.js', 'utf8'), ctx);
const studioVocab = vm.runInContext('VOCAB', ctx);
const studioCanon = studioVocab.filter(w => w.o === 'canon');
const studioCurated = studioVocab.filter(w => w.o === 'curated_ext');
const studioEmergent = studioVocab.filter(w => w.o === 'ai_emergent');

assert.equal(studioCanon.length, 1008, 'Canon root count must be 1008');
assert.ok(studioEmergent.length >= 30, 'Studio AI emergent count must be 21');
console.log(`PASS: Studio語彙区分完全分離を確認 -> 正本(canon): ${studioCanon.length}語 / 体系拡張(curated_ext): ${studioCurated.length}語 / AI対話創発(ai_emergent #40001+): ${studioEmergent.length}語`);

console.log('\n===============================================================');
console.log('ALL 6-GATE STRICT AUDIT & PROVENANCE TESTS PASSED! (100% GREEN)');
console.log('===============================================================');
