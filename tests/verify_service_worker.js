const fs = require('fs'), vm = require('vm'), assert = require('node:assert/strict');
const script = fs.readFileSync('web/service-worker.js', 'utf8');
const scope = 'https://example.test/Nebulith/';
const stores = new Map(), listeners = {};
let networkVersion = 'first', online = true, fetches = 0;
const key = request => new URL(typeof request === 'string' ? request : request.url, scope).href;
class WorkerRequest extends Request {
  constructor(url, options) { super(new URL(url, scope), options); }
}
const caches = {
  async open(name) {
    if (!stores.has(name)) stores.set(name, new Map());
    const rows = stores.get(name);
    return {
      async addAll(assets) { for (const asset of assets) rows.set(key(asset), new Response(networkVersion)); },
      async match(request) { return rows.get(key(request))?.clone(); },
      async put(request, response) { rows.set(key(request), response); }
    };
  },
  async keys() { return [...stores.keys()]; },
  async delete(name) { return stores.delete(name); }
};
function load(code) {
  vm.runInNewContext(code, {
    self: {registration: {scope}, addEventListener(name, fn) {listeners[name] = fn;}, skipWaiting: async () => {}, clients: {claim: async () => {}}},
    caches, Response, Request: WorkerRequest,
    fetch: async () => {
      fetches++;
      if (!online) throw Error('offline');
      return {status: 200, type: 'basic', clone: () => new Response(networkVersion)};
    }
  });
}
async function lifecycle(type) {
  const pending = []; listeners[type]({waitUntil: p => pending.push(p)}); await Promise.all(pending);
}
async function request(path, mode = 'navigate') {
  let response;
  const pending = [];
  listeners.fetch({request: {url: key(path), method: 'GET', mode}, respondWith: p => {response = p;}, waitUntil: p => pending.push(p)});
  const result = await response; await Promise.all(pending); return result;
}
(async () => {
  stores.set('another-app-cache', new Map());
  load(script); await lifecycle('install'); await lifecycle('activate');
  assert.equal(await (await request('./app.js')).text(), 'first');
  assert.equal(fetches, 0);
  networkVersion = 'second';
  load(script.replace(/nebulith-studio-[a-f0-9]{20}/, 'nebulith-studio-00000000000000000000'));
  await lifecycle('install'); await lifecycle('activate');
  assert.equal(await (await request('./app.js')).text(), 'second', 'new worker serves its new asset cache');
  assert.equal(stores.size, 2, 'only the prior Nebulith cache is removed');
  assert.ok(stores.has('another-app-cache'));
  online = false;
  const current = stores.get('nebulith-studio-00000000000000000000');
  current.delete(key('./index.html'));
  assert.equal(await (await request('./missing-page')).text(), 'second', 'standalone fallback is awaited when index is absent');
  current.delete(key('./standalone.html'));
  assert.equal((await request('./missing-page')).status, 503);
  assert.equal(await request('https://another.test/asset'), undefined, 'external requests are not intercepted');
  console.log('PASS: offline cache replacement, isolation, fallback and external requests');
})().catch(error => {console.error(error); process.exitCode = 1;});
