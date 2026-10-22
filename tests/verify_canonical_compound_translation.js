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
assert.equal(bi.translateNebulith('Relen el havsirin al mi.','ja').success,false,'missing ia and invalid al must not be accepted');

// 1. Nebulith -> Japanese compound sentence with 'Sen'
const r1 = bi.translateNebulith('Zen vyrel el mi ia darfalun ul darterin uo vorn, zensirin el mi.', 'ja');
assert.equal(r1.success, true);
assert.ok(r1.text.includes('露光'), 'Expected 露光 in ' + r1.text);
assert.ok(r1.text.includes('雫茶'), 'Expected 雫茶 in ' + r1.text);
assert.ok(r1.text.includes('ので'), 'Expected ので in ' + r1.text);

// 2. Nebulith -> English with prepositional phrases
const r2 = bi.translateNebulith('Cival el mi ku ti.', 'en');
assert.equal(r2.success, true);
assert.ok(r2.text.includes('with you'), 'Expected with you in ' + r2.text);

// 3. English -> Nebulith with 'Because'
const r4 = bi.translateEnglishToNebulith('Because stars shine, I see vyrcelar.');
assert.equal(r4.success, true);
assert.ok(r4.text.startsWith('Zen '), 'Expected Zen in ' + r4.text);
assert.ok(r4.text.toLowerCase().includes('vyrcelar'), 'Expected vyrcelar in ' + r4.text);

// 4. English -> Nebulith with aspect modal 'want to'
const r5 = bi.translateEnglishToNebulith('I want to observe darfalun.');
assert.equal(r5.success, true);
assert.ok(r5.text.toLowerCase().includes('vyrelast'), 'Expected vyrelast in ' + r5.text);
assert.ok(r5.text.toLowerCase().includes('darfalun'), 'Expected darfalun in ' + r5.text);

// 5. Advanced feature: Coordinated English sentence -> Coordinated Nebulith sentence
const r6 = bi.translateEnglishToNebulith('I observe water, and you walk to house.');
assert.equal(r6.success, true);
assert.ok(r6.text.includes('den Poran'), 'Expected den Poran in ' + r6.text);

const r6En = bi.translateNebulith('Vyrel el mi ia daris, den poran el ti to govan.', 'en');
assert.equal(r6En.success, true);
assert.ok(r6En.text.includes(', and '), 'Expected , and in ' + r6En.text);

// 6. Advanced feature: English coordination with ', and' -> Nebulith '..., den ...'
const r7 = bi.translateEnglishToNebulith('I observe water, and you walk to house.');
assert.equal(r7.success, true);
assert.ok(r7.text.includes('den Poran'), 'Expected den Poran in ' + r7.text);

// 7. Advanced feature: English prepositional phrases parsing -> Nebulith case markers
const r8 = bi.translateEnglishToNebulith('I walk to house with you.');
assert.equal(r8.success, false);
assert.match(r8.error,/許容格/); // Core ID902 does not allow ku; do not relax the source frame to fit an old test.

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
assert.ok(r10.text.includes('Poran el ti to govan ro?'), 'Expected Poran el ti to govan ro? in ' + r10.text);
assert.ok(!r10.text.includes('ka'), 'Expected NO ka in ' + r10.text);

// 10. Relative clause: 'ia govan en vyrel el mi' -> 'house that I observe' / '私が 観測する 家を'
const r11Ja = bi.translateNebulith('Vymin el ti ia govan en vyrel el mi.', 'ja');
assert.equal(r11Ja.success, true);
assert.ok(r11Ja.text.includes('家を'), 'Expected 家を in ' + r11Ja.text);

const r11En = bi.translateNebulith('Vymin el ti ia govan en vyrel el mi.', 'en');
assert.equal(r11En.success, true);
assert.ok(r11En.text.includes('that'), 'Expected that in ' + r11En.text);

// 11. Conditional clause: 'If you walk to house, then I observe water.' -> 'Zen Poran el ti to govan, Vyrel el mi ia daris.'
const r12 = bi.translateEnglishToNebulith('If you walk to house, then I observe water.');
assert.equal(r12.success, true);
assert.ok(r12.text.startsWith('Sen '), 'Expected Sen in ' + r12.text);
assert.ok(r12.text.includes('Poran el ti to govan'), 'Expected Poran el ti to govan in ' + r12.text);
assert.ok(r12.text.includes('Vyrel el mi ia daris'), 'Expected Vyrel el mi ia daris in ' + r12.text);

// 12. Concessive clause: 'Even if you walk to house, I observe water.' -> 'Tor Poran el ti to govan, Vyrel el mi ia daris.'
const r13 = bi.translateEnglishToNebulith('Even if you walk to house, I observe water.');
assert.equal(r13.success, true);
assert.ok(r13.text.startsWith('Tor '), 'Expected Tor in ' + r13.text);
assert.ok(r13.text.includes('Poran el ti to govan'), 'Expected Poran el ti to govan in ' + r13.text);
assert.ok(r13.text.includes('Vyrel el mi ia daris'), 'Expected Vyrel el mi ia daris in ' + r13.text);

const r13Ja = bi.translateNebulith('Tor Poran el ti to govan, Vyrel el mi ia daris.', 'ja');
assert.equal(r13Ja.success, true);
assert.ok(r13Ja.text.includes('けれど'), 'Expected けれど in ' + r13Ja.text);

const r13En = bi.translateNebulith('Tor Poran el ti to govan, Vyrel el mi ia daris.', 'en');
assert.equal(r13En.success, true);
assert.ok(r13En.text.includes('Although'), 'Expected Although in ' + r13En.text);

// 13. Temporal clause: 'When you walk to house, I observe water.' / 'While you walk to house, I observe water.' -> 'Hav Poran el ti to govan, Vyrel el mi ia daris.'
const r14 = bi.translateEnglishToNebulith('When you walk to house, I observe water.');
assert.equal(r14.success, true);
assert.ok(r14.text.startsWith('Hav '), 'Expected Hav in ' + r14.text);
assert.ok(r14.text.includes('Poran el ti to govan'), 'Expected Poran el ti to govan in ' + r14.text);
assert.ok(r14.text.includes('Vyrel el mi ia daris'), 'Expected Vyrel el mi ia daris in ' + r14.text);

const r14While = bi.translateEnglishToNebulith('While you walk to house, I observe water.');
assert.equal(r14While.success, true);
assert.ok(r14While.text.startsWith('Hav '), 'Expected Hav in ' + r14While.text);

const r14Ja = bi.translateNebulith('Hav Poran el ti to govan, Vyrel el mi ia daris.', 'ja');
assert.equal(r14Ja.success, true);
assert.ok(r14Ja.text.includes('とき'), 'Expected とき in ' + r14Ja.text);

const r14En = bi.translateNebulith('Hav Poran el ti to govan, Vyrel el mi ia daris.', 'en');
assert.equal(r14En.success, true);
assert.ok(r14En.text.includes('When'), 'Expected When in ' + r14En.text);

// 14. Purposive clause: 'So that you walk to house, I observe water.' / 'In order that you walk to house, I observe water.' -> 'Sol Poran el ti to govan, Vyrel el mi ia daris.'
const r15 = bi.translateEnglishToNebulith('So that you walk to house, I observe water.');
assert.equal(r15.success, true);
assert.ok(r15.text.startsWith('Sol '), 'Expected Sol in ' + r15.text);
assert.ok(r15.text.includes('Poran el ti to govan'), 'Expected Poran el ti to govan in ' + r15.text);
assert.ok(r15.text.includes('Vyrel el mi ia daris'), 'Expected Vyrel el mi ia daris in ' + r15.text);

const r15InOrder = bi.translateEnglishToNebulith('In order that you walk to house, I observe water.');
assert.equal(r15InOrder.success, true);
assert.ok(r15InOrder.text.startsWith('Sol '), 'Expected Sol in ' + r15InOrder.text);

const r15Ja = bi.translateNebulith('Sol Poran el ti to govan, Vyrel el mi ia daris.', 'ja');
assert.equal(r15Ja.success, true);
assert.ok(r15Ja.text.includes('ために'), 'Expected ために in ' + r15Ja.text);

const r15En = bi.translateNebulith('Sol Poran el ti to govan, Vyrel el mi ia daris.', 'en');
assert.equal(r15En.success, true);
assert.ok(r15En.text.includes('So that'), 'Expected So that in ' + r15En.text);

// 15. Comparative clause: 'Poran el mi va ti.' -> 'I walk more than you.' / '私は あなたより 歩く.'
const r16Ja = bi.translateNebulith('Poran el mi va ti.', 'ja');
assert.equal(r16Ja.success, false);
assert.match(r16Ja.error,/許容格/);

const r16En = bi.translateNebulith('Poran el mi va ti.', 'en');
assert.equal(r16En.success, false);
assert.match(r16En.error,/許容格/);

const r16 = bi.translateEnglishToNebulith('I walk more than you.');
assert.equal(r16.success, false);
assert.match(r16.error,/許容格/);

const r17 = bi.translateEnglishToNebulith('The sun is more bright than a star.');
assert.equal(r17.success, true);
assert.ok(r17.text.includes('Faluni el zohar va vyr'), 'Expected Faluni el zohar va vyr in ' + r17.text);

// 16. Reported speech: 'I say that you walk to house.' -> 'Fenor el mi ia Poran el ti to govan.'
const r18 = bi.translateEnglishToNebulith('I say that you walk to house.');
assert.equal(r18.success, true);
assert.ok(r18.text.includes('Fenor el mi ia Poran el ti to govan'), 'Expected Fenor el mi ia Poran el ti to govan in ' + r18.text);

const r18Ja = bi.translateNebulith('Fenor el mi ia Poran el ti to govan.', 'ja');
assert.equal(r18Ja.success, true);
assert.ok(r18Ja.text.includes('歩くと'), 'Expected 歩くと in ' + r18Ja.text);

const r18En = bi.translateNebulith('Fenor el mi ia Poran el ti to govan.', 'en');
assert.equal(r18En.success, true);
assert.ok(r18En.text.includes('that you walk'), 'Expected that you walk in ' + r18En.text);

// 17. Indirect question / Wh-clause: 'I know where you walk to house.' -> 'Velsen el mi ia kauo Poran el ti to govan.'
const r19 = bi.translateEnglishToNebulith('I know where you walk to house.');
assert.equal(r19.success, true);
assert.ok(r19.text.includes('Velsen el mi ia kauo Poran el ti to govan'), 'Expected Velsen el mi ia kauo Poran el ti to govan in ' + r19.text);

const r19Ja = bi.translateNebulith('Velsen el mi ia kauo Poran el ti to govan.', 'ja');
assert.equal(r19Ja.success, true);
assert.ok(r19Ja.text.includes('どこへ'), 'Expected どこへ in ' + r19Ja.text);
assert.ok(r19Ja.text.includes('か'), 'Expected か in ' + r19Ja.text);

const r19En = bi.translateNebulith('Velsen el mi ia kauo Poran el ti to govan.', 'en');
assert.equal(r19En.success, true);
assert.ok(r19En.text.includes('where you walk'), 'Expected where you walk in ' + r19En.text);

// 18. Incremental translator check
const inc = vm.runInContext(
  'createIncrementalTranslator(VOCAB, GRAMMAR_FRAMES, INPUT_RULES.aliases, [], TRANSLATION_EXTENSIONS)',
  ctx
);
const r3 = inc.analyze('私は露光を観測します。', {});
assert.ok(r3.text.toLowerCase().includes('darfalun'), 'Expected darfalun in ' + JSON.stringify(r3));

console.log(JSON.stringify({ r1, r2, r3Neb: r3.text, r3Complete: r3.complete, r4, r5, r6, r6En, r7, r8, r9Ja, r9En, r10, r11Ja, r11En, r12, r13, r13Ja, r13En, r14, r14While, r14Ja, r14En, r15, r15InOrder, r15Ja, r15En, r16Ja, r16En, r16, r17, r18, r18Ja, r18En, r19, r19Ja, r19En }));
