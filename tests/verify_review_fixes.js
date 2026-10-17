const fs = require('fs'), vm = require('vm'), assert = require('node:assert/strict');

function start() {
  const dom = {}, values = {};
  const element = id => dom[id] ||= {
    value: '', textContent: '', innerHTML: '', disabled: false, handlers: {},
    style: {setProperty() {}}, classList: {add() {}, remove() {}}, setAttribute() {},
    addEventListener(name, fn) { this.handlers[name] = fn; }
  };
  const ctx = {
    document: {documentElement: element('html'), getElementById: element, querySelectorAll: () => []},
    localStorage: {getItem: k => values[k] ?? null, setItem(k, v) { values[k] = v; }},
    window: {}, navigator: {clipboard: {writeText: () => Promise.resolve()}},
    setTimeout: () => 0, clearTimeout() {}, console, alert() {}, confirm: () => true
  };
  vm.createContext(ctx);
  for (const file of ['data', 'bidirectional', 'incremental', 'workspace', 'app']) {
    vm.runInContext(fs.readFileSync('web/' + file + '.js', 'utf8'), ctx);
  }
  return {dom, run: source => vm.runInContext(source, ctx), event: (id, type) => dom[id].handlers[type]({target: dom[id]})};
}

const app = start();
for (const [input, expected] of [
  ['The night is not beautiful.', 'Ne cylani el valar.'],
  ['You like me.', 'Cynel el ti ia mi.'],
  ['We walk.', 'Poran el miin.'],
  ['I did not like you.', 'Fe ne cynel el mi ia ti.'],
  ['The sun is more beautiful than the star.', 'Cylani el zohar va vyr.']
]) {
  app.run(`srcLang='en';dstLang='neb';transInput.value=${JSON.stringify(input)};doTranslate()`);
  assert.equal(app.dom.transOutputText.textContent, expected, input);
  assert.equal(app.dom.copyDstBtn.disabled, false, input);
}
for (const input of ['I like quantum computers.', 'Alice walks.', 'I like you and water.', 'I walk on the moon.', 'The night is beautiful and warm.']) {
  app.run(`srcLang='en';dstLang='neb';transInput.value=${JSON.stringify(input)};doTranslate()`);
  assert.equal(app.dom.copyDstBtn.disabled, true, input);
  assert.equal(app.dom.transMissingBox.style.display, 'flex', input);
}

for (const input of ['太郎は「私は歩く」と言った', '私は「未知の量子機械」と言った']) {
  app.run(`srcLang='ja';dstLang='neb';transInput.value=${JSON.stringify(input)};resetInputChoices();doTranslate()`);
  assert.equal(app.run('lastInputAnalysis.segments[0].state'), 'blocked', input);
  assert.equal(app.dom.copyDstBtn.disabled, true, input);
  assert.equal(app.dom.transMissingBox.style.display, 'flex', input);
}
app.run(`transInput.value='私は「星を見る」と言った。';resetInputChoices();doTranslate()`);
assert.equal(app.dom.copyDstBtn.disabled, true);
app.dom.inputSubject.value = '私'; app.event('inputSubject', 'change');
app.dom.inputVerb.value = '観測する'; app.event('inputVerb', 'change');
assert.equal(app.dom.confirmInputCandidate.disabled, false);
app.event('confirmInputCandidate', 'click');
assert.equal(app.dom.copyDstBtn.disabled, false);
assert.equal(app.dom.transOutputText.textContent, 'Fe fenor el mi ia "Vyrel el mi ia vyr."');
app.run(`transInput.value='私は「星を見る」と言った。私は歩く。';resetInputChoices(true);doTranslate()`);
assert.equal(app.run('lastInputAnalysis.complete'), true, 'unchanged quote keeps its interpretation');
assert.equal(app.run(`inputEngine.analyze('私は「星が輝く？」と言った').segments.length`), 1, 'quoted punctuation stays inside its clause');
console.log('PASS: English negation, subjects and full consumption; unknown speakers, blocked quotes and UI confirmation');
