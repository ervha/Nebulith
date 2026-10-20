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
const r1 = bi.translateNebulith('Sen vyrel el mi ia darfalun ul darterin uo vorn, relen el havsirin al mi.', 'ja');
assert.equal(r1.success, true);
assert.ok(r1.text.includes('露光'), 'Expected 露光 in ' + r1.text);
assert.ok(r1.text.includes('雫茶'), 'Expected 雫茶 in ' + r1.text);
assert.ok(r1.text.includes('ので'), 'Expected ので in ' + r1.text);

const r2 = bi.translateNebulith('Poran el mi to govan ku ti.', 'en');
assert.equal(r2.success, true);
assert.ok(r2.text.includes('with you'), 'Expected with you in ' + r2.text);

const r4 = bi.translateEnglishToNebulith('Because stars shine, I see vyrcelar.');
assert.equal(r4.success, true);
assert.ok(r4.text.startsWith('Sen '), 'Expected Sen in ' + r4.text);
assert.ok(r4.text.toLowerCase().includes('vyrcelar'), 'Expected vyrcelar in ' + r4.text);

const r5 = bi.translateEnglishToNebulith('I want to observe darfalun.');
assert.equal(r5.success, true);
assert.ok(r5.text.toLowerCase().includes('vyrelast'), 'Expected vyrelast in ' + r5.text);
assert.ok(r5.text.toLowerCase().includes('darfalun'), 'Expected darfalun in ' + r5.text);

const inc = vm.runInContext(
  'createIncrementalTranslator(VOCAB, GRAMMAR_FRAMES, INPUT_RULES.aliases, [], TRANSLATION_EXTENSIONS)',
  ctx
);
const r3 = inc.analyze('私は露光を観測します。', {});
assert.ok(r3.text.toLowerCase().includes('darfalun'), 'Expected darfalun in ' + JSON.stringify(r3));

console.log(JSON.stringify({ r1, r2, r3Neb: r3.text, r3Complete: r3.complete, r4, r5 }));
