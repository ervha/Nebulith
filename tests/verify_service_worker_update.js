const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
const handlers={},stored=new Map(),requests=[];
const origin='https://studio.example/web/';
class WorkerRequest extends Request {constructor(url,options){super(new URL(url,origin),options);}}
const cache={async addAll(batch){
 for(const request of batch){
  requests.push(request);
  // Emulate an old, still-fresh HTTP cache. A reload is required to obtain this release.
  stored.set(request.url,request.cache==='reload'?'new release':'old release');
 }
}};
const ctx={Request:WorkerRequest,caches:{open:async()=>cache},self:{
 addEventListener:(name,handler)=>handlers[name]=handler,
 skipWaiting:async()=>{},registration:{scope:origin}
}};
vm.createContext(ctx);vm.runInContext(fs.readFileSync('web/service-worker.js','utf8'),ctx);
(async()=>{
 let installed;handlers.install({waitUntil:p=>installed=p});await installed;
 assert.ok(requests.length>=10);
 for(const name of ['index.html','data.js','incremental.js','bidirectional.js','app.js']){
  assert.equal(stored.get(origin+name),'new release',name+' must not inherit the old HTTP cache');
 }
 assert.ok(requests.every(r=>r.cache==='reload'));
 console.log('PASS: all precache requests bypass an old HTTP cache, including data and translation scripts.');
})().catch(error=>{console.error(error);process.exitCode=1;});
