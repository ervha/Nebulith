const fs=require('fs'),assert=require('node:assert/strict');
const ledger=JSON.parse(fs.readFileSync('data/emergent_lexicon_audit.json','utf8'));
assert.equal(ledger.summary.totalApproved,0);
assert.equal(ledger.approvedLexicon.length,0);
assert.equal(ledger.candidates.length,1020);
for(const row of ledger.candidates){assert.equal(row.approved,false);assert.equal(row.bookEligible,false);assert.equal(row.audit_status,'REVIEW_REQUIRED');assert.ok(row.previousAudit);}
const ext=JSON.parse(fs.readFileSync('data/translation_extensions.json','utf8')).entries;
assert.equal(ext.filter(e=>e.origin==='ai_emergent'||e.id>=40000).length,0);
console.log('PASS: unsupported approvals withdrawn; all 1020 candidates held with original evidence; no automatic promotion');
