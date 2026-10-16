const fs = require('fs');
const vm = require('vm');
const assert = require('node:assert/strict');

console.log('=== Verifying Nebulith 6-Gate Strict Audit & Provenance Separation ===\n');

const auditPath = 'data/emergent_lexicon_audit.json';
assert.ok(fs.existsSync(auditPath), 'emergent_lexicon_audit.json must exist');

const audit = JSON.parse(fs.readFileSync(auditPath, 'utf8'));

// 1. シチュエーション構成検証
console.log('--- 1. Universal Everyday & Specialized Scenarios ---');
assert.ok(audit.summary.totalScenarios >= 11, 'Total scenarios must be >= 11');
assert.ok(audit.summary.universalScenarios >= 9, 'Universal scenarios must be >= 9');
assert.equal(audit.summary.specializedScenarios, 2);
console.log(`PASS: 全 ${audit.summary.totalScenarios} シナリオ（汎用日常: ${audit.summary.universalScenarios}件、専門星辰: 2件）を確認`);

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
assert.ok(audit.summary.totalRejected >= 5);
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

// 4. 正本・体系拡張の厳格保全とAI創発語彙の監査後組み込み方針の検証
console.log('\n--- 4. Provenance Protection & Human Audit Gate Verification ---');
const ext = JSON.parse(fs.readFileSync('data/translation_extensions.json', 'utf8'));
const emergentInExt = ext.entries.filter(e => e.origin === 'ai_emergent' || e.id >= 40000);
const curatedEntries = ext.entries.filter(e => e.origin !== 'ai_emergent');

// 実際の単語辞書には、人間の本番監査前のAI創発語は一切自動混入しないこと
assert.equal(emergentInExt.length, 0, 'Un-audited AI emergent words must NOT be incorporated into translation_extensions.json');
assert.ok(curatedEntries.length >= 370, 'Curated extension entries must be safely preserved');

// AI創発語彙は監査待ち候補台帳（emergent_lexicon_audit.json）に保持されていること
assert.ok(audit.approvedLexicon.length >= 30, 'Emergent words must be held in audit ledger pending human approval');

// Web StudioのVOCABにも混入せず、Webダッシュボードが除去されていること
const ctx = {};
vm.createContext(ctx);
vm.runInContext(fs.readFileSync('web/data.js', 'utf8'), ctx);
const studioVocab = vm.runInContext('VOCAB', ctx);
const studioCanon = studioVocab.filter(w => w.o === 'canon');
const studioCurated = studioVocab.filter(w => w.o === 'curated_ext');
const studioEmergent = studioVocab.filter(w => w.o === 'ai_emergent');

assert.equal(studioCanon.length, 1008, 'Canon root count must be 1008');
assert.equal(studioEmergent.length, 0, 'Studio VOCAB must NOT contain un-audited AI emergent words');

const indexHtml = fs.readFileSync('web/index.html', 'utf8');
assert.ok(!indexHtml.includes('id="tab-emergentAudit"'), 'Web dashboard must be removed from web/index.html');
assert.ok(!indexHtml.includes('data-tab="emergentAudit"'), 'emergentAudit tab button must be removed');

console.log(`PASS: 実際の単語への自動組み込み遮断＆監査後組み込み方針を確認 -> 正本: ${studioCanon.length}語 / 体系拡張: ${studioCurated.length}語 / Webダッシュボード撤廃確認済`);

console.log('\n===============================================================');
console.log('ALL 6-GATE STRICT AUDIT & PROVENANCE TESTS PASSED! (100% GREEN)');
console.log('===============================================================');
