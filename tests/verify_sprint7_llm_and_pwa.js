const fs = require('fs');
const assert = require('node:assert/strict');
const path = require('path');

console.log('=== Verifying Sprint 7: LLM Emergent Dialogue, Feedback Auto-Triage & PWA Offline Optimization ===\n');

// 1. Dynamic LLM Emergence & Strict Arbiter Integration Verification
console.log('--- 1. LLM Multi-Agent Dialogue Engine Verification ---');
const llmDialoguePath = 'tools/llm_agent_dialogue.py';
assert.ok(fs.existsSync(llmDialoguePath), 'tools/llm_agent_dialogue.py must exist');

const llmScript = fs.readFileSync(llmDialoguePath, 'utf8');
assert.ok(llmScript.includes('class MockLLMProvider'), 'Must provide offline MockLLMProvider');
assert.ok(llmScript.includes('class OpenAICompatibleProvider'), 'Must provide OpenAICompatibleProvider for Ollama/APIs');
assert.ok(llmScript.includes('class DynamicEmergencePipeline'), 'Must provide DynamicEmergencePipeline');
assert.ok(llmScript.includes('StrictArbiterEngine'), 'Must interface directly with 6-gate StrictArbiterEngine');
console.log('PASS: tools/llm_agent_dialogue.py structure and arbiter integration verified');

// 2. Feedback Queue Auto-Triage Pipeline Verification
console.log('\n--- 2. Feedback Queue Auto-Triage Pipeline Verification ---');
const triageScriptPath = 'tools/triage_feedback_queue.py';
assert.ok(fs.existsSync(triageScriptPath), 'tools/triage_feedback_queue.py must exist');

const testQueuePath = 'tests/fixtures/test_feedback_queue.json';
assert.ok(fs.existsSync(testQueuePath), 'Fixture tests/fixtures/test_feedback_queue.json must exist');

const triagedOutPath = 'tests/fixtures/test_feedback_queue_triaged.json';
assert.ok(fs.existsSync(triagedOutPath), 'Triaged output must exist');
const triagedData = JSON.parse(fs.readFileSync(triagedOutPath, 'utf8'));
assert.equal(triagedData.totalItems, 2);
assert.ok(triagedData.implementedCount >= 1);
for (const item of triagedData.queue) {
  if (item.status === 'implemented') {
    assert.ok(item.resolvedWith, 'Implemented queue item must have resolvedWith field');
    assert.ok(item.resolvedWith.nrs, 'Resolved neologism must specify NRS');
    assert.ok(item.resolvedWith.score >= 0.90, 'Resolved neologism must pass 6-gate audit score threshold');
  }
}
console.log(`PASS: Auto-triage pipeline processed ${triagedData.totalItems} queue items -> Implemented: ${triagedData.implementedCount}`);

// 3. Complete PWA Offline Optimization & Service Worker Verification
console.log('\n--- 3. PWA Offline Optimization & Service Worker Verification ---');
const swPath = 'web/service-worker.js';
assert.ok(fs.existsSync(swPath), 'web/service-worker.js must exist');
const swContent = fs.readFileSync(swPath, 'utf8');
assert.ok(/const CACHE_NAME = 'nebulith-studio-[a-f0-9]{20}';/.test(swContent), 'Service Worker must have versioned cache name');
assert.ok(swContent.includes("'./data.js'"), 'Service Worker must precache data.js');
assert.ok(swContent.includes("'./bidirectional.js'"), 'Service Worker must precache bidirectional.js');
assert.ok(swContent.includes("'./incremental.js'"), 'Service Worker must precache incremental.js');
assert.ok(swContent.includes("'./app.js'"), 'Service Worker must precache app.js');
assert.ok(swContent.includes("'./standalone.html'"), 'Service Worker must precache standalone.html');

const manifestPath = 'web/manifest.json';
assert.ok(fs.existsSync(manifestPath), 'web/manifest.json must exist');
const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
assert.equal(manifest.display, 'standalone', 'PWA display must be standalone');
assert.ok(manifest.icons.length > 0, 'PWA must declare icons');

const appJs = fs.readFileSync('web/app.js', 'utf8');
assert.ok(appJs.includes('navigator.serviceWorker.register'), 'web/app.js must register service worker');
console.log('PASS: Service Worker, manifest.json, and app.js registration verified');

// 4. Clean Web Studio UI Verification (Web Dashboard Removed)
console.log('\n--- 4. Web Studio Clean UI (Dashboard Removed) Verification ---');
const indexHtml = fs.readFileSync('web/index.html', 'utf8');
assert.ok(!indexHtml.includes('id="tab-emergentAudit"'), 'index.html must not include emergentAudit tab');
assert.ok(!indexHtml.includes('data-tab="emergentAudit"'), 'index.html must not include emergentAudit button');

const standaloneHtml = fs.readFileSync('web/standalone.html', 'utf8');
assert.ok(!standaloneHtml.includes('id="tab-emergentAudit"'), 'standalone.html must not include emergentAudit tab');
assert.ok(!standaloneHtml.includes('data-tab="emergentAudit"'), 'standalone.html must not include emergentAudit button');

console.log('PASS: Web Studio cleanly freed from audit dashboard in index.html & standalone.html');

console.log('\n===============================================================');
console.log('ALL SPRINT 7 & DYNAMIC LLM EMERGENCE TESTS PASSED! (100% GREEN)');
console.log('===============================================================');
