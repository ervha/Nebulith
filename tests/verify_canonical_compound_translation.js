const fs = require('fs');
const vm = require('vm');
const assert = require('node:assert/strict');

const ctx = { console };
vm.createContext(ctx);
vm.runInContext(fs.readFileSync('web/data.js', 'utf8'), ctx);
vm.runInContext(fs.readFileSync('web/bidirectional.js', 'utf8'), ctx);
vm.runInContext(fs.readFileSync('web/incremental.js', 'utf8'), ctx);
vm.runInContext(
  'NebulithBidirectionalEngine.configure(VOCAB, VERIFIED_CANONICAL_COMPOUNDS); globalThis.VERIFIED_CANONICAL_COMPOUNDS = VERIFIED_CANONICAL_COMPOUNDS;',
  ctx
);

const bi = ctx.NebulithBidirectionalEngine;

// 1. Nebulith -> Japanese compound sentence with 'Sen'
const r1 = bi.translateNebulith('Sen vyrel el mi ia darfalun ul darterin uo vorn, relen el havsirin al mi.', 'ja');
assert.equal(r1.success, true);
assert.ok(r1.text.includes('露光'), 'Expected 露光 in ' + r1.text);
assert.ok(r1.text.includes('雫茶'), 'Expected 雫茶 in ' + r1.text);
assert.ok(r1.text.includes('ので'), 'Expected ので in ' + r1.text);

// 2. Nebulith -> English with prepositional phrases
const r2 = bi.translateNebulith('Poran el mi to govan ku ti.', 'en');
assert.equal(r2.success, true);
assert.ok(r2.text.includes('with you'), 'Expected with you in ' + r2.text);

// 3. English -> Nebulith with 'Because'
const r4 = bi.translateEnglishToNebulith('Because stars shine, I see vyrcelar.');
assert.equal(r4.success, true);
assert.ok(r4.text.startsWith('Sen '), 'Expected Sen in ' + r4.text);
assert.ok(r4.text.toLowerCase().includes('vyrcelar'), 'Expected vyrcelar in ' + r4.text);

// 4. English -> Nebulith with aspect modal 'want to'
const r5 = bi.translateEnglishToNebulith('I want to observe darfalun.');
assert.equal(r5.success, true);
assert.ok(r5.text.toLowerCase().includes('vyrelast'), 'Expected vyrelast in ' + r5.text);
assert.ok(r5.text.toLowerCase().includes('darfalun'), 'Expected darfalun in ' + r5.text);

// 5. Advanced feature: Nebulith coordinating conjunction 'den' (mid-sentence)
const r6 = bi.translateNebulith('Vyrel el mi ia daris, den poran el ti to govan.', 'ja');
assert.equal(r6.success, true);
assert.ok(r6.text.includes('、そして'), 'Expected 、そして in ' + r6.text);

const r6En = bi.translateNebulith('Vyrel el mi ia daris, den poran el ti to govan.', 'en');
assert.equal(r6En.success, true);
assert.ok(r6En.text.includes(', and '), 'Expected , and in ' + r6En.text);

// 6. Advanced feature: English coordination with ', and' -> Nebulith '..., den ...'
const r7 = bi.translateEnglishToNebulith('I observe water, and you walk to house.');
assert.equal(r7.success, true);
assert.ok(r7.text.includes('den Poran'), 'Expected den Poran in ' + r7.text);

// 7. Advanced feature: English prepositional phrases parsing -> Nebulith case markers
const r8 = bi.translateEnglishToNebulith('I walk to house with you.');
assert.equal(r8.success, true);
assert.ok(r8.text.includes('to govan ku ti'), 'Expected to govan ku ti in ' + r8.text);

// 8. Interrogative Particle 'ro' (Nebulith -> Japanese & English)
const r9Ja = bi.translateNebulith('Poran el ti to govan ro?', 'ja');
assert.equal(r9Ja.success, true);
assert.ok(r9Ja.text.includes('歩くか？'), 'Expected 歩くか？ in ' + r9Ja.text);

const r9En = bi.translateNebulith('Poran el ti to govan ro?', 'en');
assert.equal(r9En.success, true);
assert.ok(r9En.text.startsWith('Do you walk'), 'Expected Do you walk in ' + r9En.text);
assert.ok(r9En.text.endsWith('?'), 'Expected ? in ' + r9En.text);

// 9. English Question -> Nebulith with 'ro?' (No 'ka')
const r10 = bi.translateEnglishToNebulith('Do you walk to house?');
assert.equal(r10.success, true);
assert.ok(r10.text.includes('ro?'), 'Expected ro? in ' + r10.text);
assert.ok(!r10.text.includes('ka'), 'Expected NO ka in ' + r10.text);

// 10. Relative clause: 'ia govan en vyrel el mi' -> 'house that I observe' / '私が 観測する 家を'
const r11Ja = bi.translateNebulith('Vymin el ti ia govan en vyrel el mi.', 'ja');
assert.equal(r11Ja.success, true);
assert.ok(r11Ja.text.includes('家を'), 'Expected 家を in ' + r11Ja.text);

const r11En = bi.translateNebulith('Vymin el ti ia govan en vyrel el mi.', 'en');
assert.equal(r11En.success, true);
assert.ok(r11En.text.includes('that'), 'Expected that in ' + r11En.text);

// 11. Incremental translator check
const inc = vm.runInContext(
  'createIncrementalTranslator(VOCAB, GRAMMAR_FRAMES, INPUT_RULES.aliases, [], TRANSLATION_EXTENSIONS)',
  ctx
);
const r3 = inc.analyze('私は露光を観測します。', {});
assert.ok(r3.text.toLowerCase().includes('darfalun'), 'Expected darfalun in ' + JSON.stringify(r3));

console.log(JSON.stringify({ r1, r2, r3Neb: r3.text, r3Complete: r3.complete, r4, r5, r6, r6En, r7, r8, r9Ja, r9En, r10, r11Ja, r11En }));
