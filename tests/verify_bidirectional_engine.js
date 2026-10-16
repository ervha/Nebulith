const fs = require('fs');
const assert = require('node:assert/strict');
const bi = require('../web/bidirectional.js');

console.log('=== Verifying Nebulith Bidirectional Translation Engine (Sprint 6) ===\n');

// 1. Nebulith -> Japanese (SOV)
console.log('--- 1. Nebulith (VSO) -> Japanese (SOV) ---');
const nebToJa1 = bi.translateNebulith('Cynel el mi ia ti.', 'ja');
assert.equal(nebToJa1.success, true);
assert.ok(nebToJa1.text.includes('私') && nebToJa1.text.includes('あなた') && nebToJa1.text.includes('愛する'), 'Basic SVO should produce natural Japanese SOV');
assert.equal(nebToJa1.alignments.length, 3);
console.log('PASS [NEB -> JA Basic]: Cynel el mi ia ti. ->', nebToJa1.text);

const nebToJa2 = bi.translateNebulith('Cylani el vyr va valar.', 'ja');
assert.equal(nebToJa2.success, true);
assert.ok(nebToJa2.text.includes('星') && nebToJa2.text.includes('夜') && nebToJa2.text.includes('美しい'), 'Comparison should produce Japanese comparative clause');
console.log('PASS [NEB -> JA Comparison]: Cylani el vyr va valar. ->', nebToJa2.text);

// 2. Nebulith -> English (SVO)
console.log('\n--- 2. Nebulith (VSO) -> English (SVO) ---');
const nebToEn1 = bi.translateNebulith('Cynel el mi ia ti.', 'en');
assert.equal(nebToEn1.success, true);
assert.equal(nebToEn1.text, 'I like you.');
console.log('PASS [NEB -> EN Basic]: Cynel el mi ia ti. ->', nebToEn1.text);

const nebToEn2 = bi.translateNebulith('Ne cynel el mi ia ti.', 'en');
assert.equal(nebToEn2.success, true);
assert.ok(nebToEn2.text.includes('do not like'), 'Negation should be reflected in English');
console.log('PASS [NEB -> EN Negation]: Ne cynel el mi ia ti. ->', nebToEn2.text);

// 3. English -> Nebulith (SVO -> VSO)
console.log('\n--- 3. English (SVO) -> Nebulith (VSO) ---');
const enToNeb1 = bi.translateEnglishToNebulith('I like you');
assert.equal(enToNeb1.success, true);
assert.equal(enToNeb1.text, 'Cynel el mi ia ti.');
assert.equal(enToNeb1.alignment.length, 3);
console.log('PASS [EN -> NEB Basic]: I like you ->', enToNeb1.text);

const enToNeb2 = bi.translateEnglishToNebulith('If stars shine, I walk');
assert.equal(enToNeb2.success, true);
assert.equal(enToNeb2.text, 'Zen Falun el vyr, Poran el mi.');
console.log('PASS [EN -> NEB Conditional]: If stars shine, I walk ->', enToNeb2.text);

const enToNeb3 = bi.translateEnglishToNebulith('The star is more beautiful than the night');
assert.equal(enToNeb3.success, true);
assert.equal(enToNeb3.text, 'Cylani el vyr va valar.');
console.log('PASS [EN -> NEB Comparative]: The star is more beautiful than the night ->', enToNeb3.text);

const enToNeb4 = bi.translateEnglishToNebulith('The night is beautiful');
assert.equal(enToNeb4.success, true);
assert.equal(enToNeb4.text, 'Cylani el valar.');
console.log('PASS [EN -> NEB Adjective Predicate]: The night is beautiful ->', enToNeb4.text);

console.log('\n===============================================================');
console.log('ALL BIDIRECTIONAL ENGINE TESTS PASSED! (100% GREEN)');
console.log('===============================================================');
