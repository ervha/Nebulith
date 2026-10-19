const fs = require('fs');
const vm = require('vm');
const assert = require('node:assert/strict');

const ctx = {};
vm.createContext(ctx);
for (const file of ['web/data.js', 'web/incremental.js', 'web/bidirectional.js']) {
  vm.runInContext(fs.readFileSync(file, 'utf8'), ctx);
}
const bi = ctx.NebulithBidirectionalEngine;

function verbOf(sentence) {
  const result = bi.translateNebulith(sentence, 'ja');
  assert.equal(result.success, true, sentence + ' ' + JSON.stringify(result));
  return result.text;
}

assert.ok(verbOf('Fe vyrel el mi ia vyr.').includes('観測した'), verbOf('Fe vyrel el mi ia vyr.'));
assert.ok(!verbOf('Fe vyrel el mi ia vyr.').includes('観測すた'), verbOf('Fe vyrel el mi ia vyr.'));
assert.ok(verbOf('Vyrelast el mi ia vyr.').includes('観測したい'), verbOf('Vyrelast el mi ia vyr.'));
assert.ok(verbOf('Ne poran el mi.').includes('歩かない'), verbOf('Ne poran el mi.'));
assert.ok(verbOf('Fe cynel el mi ia ti.').includes('愛した'), verbOf('Fe cynel el mi ia ti.'));
assert.ok(verbOf('Poranast el mi.').includes('歩きたい'), verbOf('Poranast el mi.'));

const direct = require('../web/bidirectional.js');
for (const [input, output] of [
  ['I like the stars', 'Cynel el mi ia vyr.'],
  ['I like beautiful stars', 'Cynel el mi ia vyr cylani.'],
  ['We see the star', 'Vyrel el miin ia vyr.'],
  ['I like stars', 'Cynel el mi ia vyr.']
]) {
  const result = direct.translateEnglishToNebulith(input);
  assert.equal(result.success, true, input);
  assert.equal(result.text, output, input);
}

const app = fs.readFileSync('web/app.js', 'utf8');
assert.ok(app.includes('function activateTab('));
assert.ok(!app.includes("getElementById('translatorTab')"));
assert.ok(app.includes('aria-pressed'));
assert.ok(app.includes('aria-label="この記録を削除"'));
assert.ok(app.includes('ライトテーマに切り替え'));

console.log('PASS: Japanese conjugation, English objects, tab id, and icon labels');
