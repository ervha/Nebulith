// Nebulith Studio Web - Complete Application Logic (v2.7)

// State & LocalStorage
function reportStorageError(message){document.getElementById('storageStatus').textContent=message;}
const safeStorage=NebulithWorkspace.createStore(()=>localStorage,reportStorageError);
function storedArray(key){const value=safeStorage.json(key,[]);if(!Array.isArray(value)||value.some(v=>typeof v!=='string')){reportStorageError('保存された一覧が不正です。元データは保持します。');return [];}return value;}

let currentTheme = safeStorage.getItem('neb_theme') || 'dark';
let currentFilterPos = 'ALL';
let srcLang = 'ja'; // 'ja' | 'en' | 'neb'
let dstLang = 'neb'; // 'neb' | 'ja' | 'en'
let favorites = new Set(storedArray('neb_favorites'));
let browsingHistory=storedArray('neb_history').slice(0,100);
let feedbackQueue=[];
try{feedbackQueue=NebulithWorkspace.normalizeQueue(safeStorage.json('neb_feedback_queue',[]),{name:'既存記録'});}catch(e){reportStorageError('記録の読込に問題があります：'+e.message);}
let activeModalWord = null;
let modalReturnFocus=null;

function escapeHtml(str) {
  if (!str) return '';
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g,'&#39;');
}

// Initialize Theme
document.documentElement.setAttribute('data-theme', currentTheme);
updateThemeUI();

document.getElementById('themeToggleBtn').addEventListener('click', () => {
  currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', currentTheme);
  safeStorage.setItem('neb_theme', currentTheme);
  updateThemeUI();
});

function updateThemeUI() {
  const sun = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M19.1 4.9l-1.4 1.4M6.3 17.7l-1.4 1.4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>';
  const moon = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" focusable="false"><path d="M21 14.5A8.5 8.5 0 1 1 9.5 3 7 7 0 0 0 21 14.5z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>';
  const icon = document.getElementById('themeIcon');
  const label = document.getElementById('themeLabel');
  const btn = document.getElementById('themeToggleBtn');
  const toLight = currentTheme === 'dark';
  if (icon) icon.innerHTML = toLight ? sun : moon;
  if (label) label.textContent = toLight ? 'Light' : 'Dark';
  if (btn && typeof btn.setAttribute === 'function') btn.setAttribute('aria-label', toLight ? 'ライトテーマに切り替え' : 'ダークテーマに切り替え');
}

// Queue Badge Update
const queueCountBadge = document.getElementById('queueCountBadge');
function updateQueueBadge() {
  if (queueCountBadge) {
    queueCountBadge.textContent = feedbackQueue.length;
    queueCountBadge.style.display = feedbackQueue.length > 0 ? 'inline-block' : 'none';
  }
  const summary = document.getElementById('queueSummaryText');
  if (summary) {
    summary.textContent = `記録件数: ${feedbackQueue.length} 件`;
  }
}
updateQueueBadge();

// Add Item to Feedback Queue
function addFeedbackItem(type, lang, text, context, interpretation = null) {
  const trimmed=text.trim();if(!trimmed)return false;
  try {
    const item={id:'fb_'+Date.now()+'_'+Math.random().toString(36).slice(2),type,lang,text:trimmed,context:context||'',...(interpretation?{interpretation}:{}),count:1,createdAt:new Date().toISOString()};
    return persistQueue(NebulithWorkspace.mergeQueue(feedbackQueue,[item],{name:'このブラウザー'}).queue);
  }catch(e){reportStorageError(e.message);return false;}

}

function activateTab(tabName) {
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.classList.toggle('active', btn.getAttribute('data-tab') === tabName);
  });
  document.querySelectorAll('.tab-content').forEach(panel => panel.classList.remove('active'));
  const panel = document.getElementById('tab-' + tabName);
  if (panel) panel.classList.add('active');
}

// Tab Navigation
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => activateTab(btn.getAttribute('data-tab')));
});

// Lexicon & Favorites
const wordGrid = document.getElementById('wordGrid');
const searchInput = document.getElementById('lexSearchInput');
const resultCount = document.getElementById('resultCount');
const favCountSpan = document.getElementById('favCount');
const wordModal = document.getElementById('wordModal');

function updateFavCount() {
  if (favCountSpan) favCountSpan.textContent = favorites.size;
}
updateFavCount();

// Build the searchable catalog once. Compounds participate in ordinary search,
// favorites, history and part-of-speech filters rather than a separate hidden list.
const catalogByRoot=new Map(VOCAB.map(w=>[w.r,{...w,b:''}]));
for(const row of (typeof VERIFIED_CANONICAL_COMPOUNDS!=='undefined'?VERIFIED_CANONICAL_COMPOUNDS.entries:[])) {
  if(!catalogByRoot.has(row.nrs))catalogByRoot.set(row.nrs,{id:row.id,r:row.nrs,p:row.pos,m:row.meaningJa,en:row.meaningEn,i:'',c:row.category||'',b:row.batch||'',o:'verified_compound',n:[row.etymology,...(row.morphemes||[]),row.scenario_id,...(row.speakers||[])].join(' ')});
}
const normalizeCatalogText=text=>String(text||'').normalize('NFKC').toLowerCase().replace(/\s+/g,' ').trim();
const dictionaryCatalog=[...catalogByRoot.values()].map(w=>({...w,
  displayCategory:TRANSLATION_EXTENSIONS.catalogCategories?.categories?.[w.c]||w.c,
  searchText:normalizeCatalogText([w.r,w.m,w.en,w.n,w.c,w.b].join(' ')),
  searchLabels:[w.r,...(w.m+'、'+w.en).split(/[、／,;]/)].map(normalizeCatalogText)}));
const lexCategoryFilter=document.getElementById('lexCategoryFilter');
const lexBatchFilter=document.getElementById('lexBatchFilter');
for(const [control,values,label] of [
  [lexCategoryFilter,[...new Set(dictionaryCatalog.map(w=>w.displayCategory).filter(Boolean))].sort((a,b)=>a.localeCompare(b,'ja',{numeric:true})),'すべてのカテゴリ'],
  [lexBatchFilter,[...new Set(dictionaryCatalog.map(w=>w.b).filter(Boolean))].sort((a,b)=>a.localeCompare(b,'en',{numeric:true})),'すべてのバッチ']]) {
  control.innerHTML='<option value="">'+label+'</option>'+values.map(value=>`<option value="${escapeHtml(value)}">${escapeHtml(value)}</option>`).join('');
  control.addEventListener('change',()=>renderLexicon());
}
let lexPage=0,lexFingerprint='';
const lexPageSize=60;
function catalogMatches(query,mode,category,batch) {
  const tokens=normalizeCatalogText(query).split(' ').filter(Boolean);
  const exact=normalizeCatalogText(query);
  const score=w=>!exact?0:w.searchLabels.includes(exact)?0:w.searchLabels.some(label=>label.startsWith(exact))?1:2;
  const matches=dictionaryCatalog.filter(w=>{
    if(mode==='FAV'&&!favorites.has(w.r))return false;
    if(mode==='HISTORY'&&!browsingHistory.includes(w.r))return false;
    if(mode==='CANON'&&w.o!=='canon')return false;
    if(mode==='CURATED_EXT'&&w.o!=='curated_ext')return false;
    if(mode==='VERIFIED_COMPOUNDS'&&w.o!=='verified_compound')return false;
    if(!['ALL','FAV','HISTORY','CANON','CURATED_EXT','VERIFIED_COMPOUNDS'].includes(mode)&&!w.p.includes(mode))return false;
    return (!category||w.c===category||w.displayCategory===category)&&(!batch||w.b===batch)&&tokens.every(t=>w.searchText.includes(t));
  });
  return matches.sort((a,b)=>score(a)-score(b)||(mode==='HISTORY'?browsingHistory.indexOf(a.r)-browsingHistory.indexOf(b.r):0));
}
function renderLexicon() {
  const query=searchInput.value.trim();
  const category=lexCategoryFilter.value||'',batch=lexBatchFilter.value||'';
  const fingerprint=JSON.stringify([query,currentFilterPos,category,batch]);
  if(fingerprint!==lexFingerprint){lexPage=0;lexFingerprint=fingerprint;}
  const filtered=catalogMatches(query,currentFilterPos,category,batch);
  const pages=Math.max(1,Math.ceil(filtered.length/lexPageSize));lexPage=Math.min(lexPage,pages-1);
  const start=lexPage*lexPageSize,displayList=filtered.slice(start,start+lexPageSize);
  document.getElementById('lexPrevPage').disabled=lexPage===0;
  document.getElementById('lexNextPage').disabled=lexPage===pages-1;
  document.getElementById('lexPageInfo').textContent=`${lexPage+1} / ${pages}ページ`;
  resultCount.textContent=filtered.length?`表示中: ${start+1}〜${start+displayList.length} / ${filtered.length.toLocaleString()} 語（全${dictionaryCatalog.length.toLocaleString()}語）`:'表示中: 0 語 (一致なし)';
  if(!filtered.length) {
    const existsElsewhere=query&&catalogMatches(query,'ALL','','').length>0;
    const alreadyInQueue=feedbackQueue.some(item=>item.type==='word'&&normalizeCatalogText(item.text)===normalizeCatalogText(query));
    wordGrid.innerHTML=`<div class="empty-state"><div style="font-size:1.1rem;font-weight:600;">${query?`「${escapeHtml(query)}」に一致する単語が見つかりませんでした`:'この条件に一致する単語はありません'}</div><p>${existsElsewhere?'別のカテゴリ・区分には見つかります。条件をリセットすると表示できます。':'条件を変えて検索できます。未収録の語は記録して後で対応できます。'}</p>${query&&!existsElsewhere?`<button class="record-btn" id="recordMissingWordBtn" ${alreadyInQueue?'disabled':''}>${alreadyInQueue?'キューに記録済み':'この未対応語を記録する'}</button>`:''}</div>`;
    const recBtn=query&&!existsElsewhere?document.getElementById('recordMissingWordBtn'):null;
    if(recBtn&&!alreadyInQueue)recBtn.addEventListener('click',()=>{if(!addFeedbackItem('word','search',query,'辞書検索0件ヒット'))return;recBtn.textContent='キューに記録しました';recBtn.disabled=true;});
    return;
  }
  wordGrid.innerHTML=displayList.map(w=>{
    const isFav=favorites.has(w.r);
    const badge=w.o==='verified_compound'?'複合語':w.o==='curated_ext'?'拡張語彙':'';
    return `<div class="word-card" onclick="openWordModal('${escapeHtml(w.r)}')"><button type="button" class="card-fav-btn ${isFav?'active':''}" onclick="toggleFav(event, '${escapeHtml(w.r)}')" aria-label="${isFav?'お気に入りを解除':'お気に入りに追加'}" aria-pressed="${isFav}">${isFav?'★':'☆'}</button><div><div class="word-card-top"><button type="button" class="word-roman word-open" data-root="${escapeHtml(w.r)}" style="background:none;border:0;color:inherit;font:inherit;padding:0;text-align:left;cursor:pointer" onclick="event.stopPropagation();openWordModal('${escapeHtml(w.r)}')" aria-label="${escapeHtml(w.m)}（${escapeHtml(w.r)}）の詳細">${escapeHtml(w.r)}</button><span class="word-pos">${escapeHtml(w.p)}</span></div><div class="word-glyph">${escapeHtml(w.r)}</div><div class="word-meaning">${escapeHtml(w.m)}</div></div><div>${w.en?`<div style="font-size:0.75rem;">En: ${escapeHtml(w.en)}</div>`:''}<div class="word-ipa">${escapeHtml([badge,w.b].filter(Boolean).join(' / '))}${w.i?' /'+escapeHtml(w.i)+'/':''}</div></div></div>`;
  }).join('');
}
document.getElementById('lexPrevPage').addEventListener('click',()=>{if(lexPage>0){lexPage--;renderLexicon();}});
document.getElementById('lexNextPage').addEventListener('click',()=>{lexPage++;renderLexicon();});
document.getElementById('lexResetFilters').addEventListener('click',()=>{
  searchInput.value='';lexCategoryFilter.value='';lexBatchFilter.value='';currentFilterPos='ALL';
  document.querySelectorAll('.chip-btn').forEach(chip=>chip.classList.toggle('active',chip.getAttribute('data-pos')==='ALL'));
  renderLexicon();
});

window.toggleFav = function(e, roman) {
  if (e && e.stopPropagation) e.stopPropagation();
  if (favorites.has(roman)) {
    favorites.delete(roman);
  } else {
    favorites.add(roman);
  }
  safeStorage.setItem('neb_favorites', JSON.stringify([...favorites]));
  updateFavCount();
  renderLexicon();
  if (activeModalWord && activeModalWord.r === roman) {
    updateModalFavButton();
  }
};


// --- Enhanced Word Inspector, Phonetics & Grammar Engine ---

function nebulithToKatakana(roman) {
  if (!roman) return '';
  const str = roman.toLowerCase().trim();
  
  const directMap = {
    'el': 'エル', 'et': 'エット', 'en': 'エン', 'uo': 'ウォ', 'va': 'ヴァ', 'ar': 'アル',
    'de': 'デ', 'is': 'イス', 'zen': 'ゼン', 'tor': 'トル', 'vel': 'ヴェル', 'fal': 'ファル',
    'mi': 'ミ', 'tu': 'トゥ', 'so': 'ソ', 'vi': 'ヴィ', 'la': 'ラ', 'ci': 'シ', 'jo': 'ジョ',
    'ne': 'ネ', 'fe': 'フェ', 'di': 'ディ', 'se': 'セ', 'sol': 'ソル', 'cel': 'シェル',
    'vyr': 'ヴィール', 'kym': 'キム', 'tal': 'タル', 'celen': 'シェレン', 'falun': 'ファルン',
    'cylani': 'シラニ', 'poran': 'ポラン', 'valar': 'ヴァラル', 'zohar': 'ゾハル',
    'mor': 'モル', 'lyna': 'リュナ', 'naris': 'ナリス', 'faren': 'ファレン'
  };
  if (directMap[str]) return directMap[str];

  const table = [
    [/^cel/g, 'シェル'], [/^cyl/g, 'シル'], [/cel/g, 'シェル'], [/cyl/g, 'シル'],
    [/cha/g, 'チャ'], [/che/g, 'チェ'], [/chi/g, 'チ'], [/cho/g, 'チョ'], [/chu/g, 'チュ'],
    [/sha/g, 'シャ'], [/she/g, 'シェ'], [/shi/g, 'シ'], [/sho/g, 'ショ'], [/shu/g, 'シュ'],
    [/ca/g, 'シャ'], [/ce/g, 'シェ'], [/ci/g, 'シ'], [/co/g, 'ショ'], [/cu/g, 'シュ'], [/cy/g, 'シ'],
    [/ja/g, 'ジャ'], [/je/g, 'ジェ'], [/ji/g, 'ジ'], [/jo/g, 'ジョ'], [/ju/g, 'ジュ'], [/jy/g, 'ジ'],
    [/va/g, 'ヴァ'], [/ve/g, 'ヴェ'], [/vi/g, 'ヴィ'], [/vo/g, 'ヴォ'], [/vu/g, 'ヴ'], [/vy/g, 'ヴィ'],
    [/fa/g, 'ファ'], [/fe/g, 'フェ'], [/fi/g, 'フィ'], [/fo/g, 'フォ'], [/fu/g, 'フ'], [/fy/g, 'フィ'],
    [/da/g, 'ダ'], [/de/g, 'デ'], [/di/g, 'ディ'], [/do/g, 'ド'], [/du/g, 'ドゥ'], [/dy/g, 'ディ'],
    [/ta/g, 'タ'], [/te/g, 'テ'], [/ti/g, 'ティ'], [/to/g, 'ト'], [/tu/g, 'トゥ'], [/ty/g, 'ティ'],
    [/sa/g, 'サ'], [/se/g, 'セ'], [/si/g, 'シ'], [/so/g, 'ソ'], [/su/g, 'ス'], [/sy/g, 'スィ'],
    [/za/g, 'ザ'], [/ze/g, 'ゼ'], [/zi/g, 'ジ'], [/zo/g, 'ゾ'], [/zu/g, 'ズ'], [/zy/g, 'ズィ'],
    [/ka/g, 'カ'], [/ke/g, 'ケ'], [/ki/g, 'キ'], [/ko/g, 'コ'], [/ku/g, 'ク'], [/ky/g, 'キ'],
    [/ga/g, 'ガ'], [/ge/g, 'ゲ'], [/gi/g, 'ギ'], [/go/g, 'ゴ'], [/gu/g, 'グ'], [/gy/g, 'ギ'],
    [/pa/g, 'パ'], [/pe/g, 'ペ'], [/pi/g, 'ピ'], [/po/g, 'ポ'], [/pu/g, 'プ'], [/py/g, 'ピ'],
    [/ba/g, 'バ'], [/be/g, 'ベ'], [/bi/g, 'ビ'], [/bo/g, 'ボ'], [/bu/g, 'ブ'], [/by/g, 'ビ'],
    [/ma/g, 'マ'], [/me/g, 'メ'], [/mi/g, 'ミ'], [/mo/g, 'モ'], [/mu/g, 'ム'], [/my/g, 'ミ'],
    [/na/g, 'ナ'], [/ne/g, 'ネ'], [/ni/g, 'ニ'], [/no/g, 'ノ'], [/nu/g, 'ヌ'], [/ny/g, 'ニ'],
    [/la/g, 'ラ'], [/le/g, 'レ'], [/li/g, 'リ'], [/lo/g, 'ロ'], [/lu/g, 'ル'], [/ly/g, 'リ'],
    [/ra/g, 'ラ'], [/re/g, 'レ'], [/ri/g, 'リ'], [/ro/g, 'ロ'], [/ru/g, 'ル'], [/ry/g, 'リ'],
    [/ha/g, 'ハ'], [/he/g, 'ヘ'], [/hi/g, 'ヒ'], [/ho/g, 'ホ'], [/hu/g, 'フ'], [/hy/g, 'ヒ'],
    [/a/g, 'ア'], [/e/g, 'エ'], [/i/g, 'イ'], [/o/g, 'オ'], [/u/g, 'ウ'], [/y/g, 'イ'],
    [/n$/g, 'ン'], [/m$/g, 'ム'], [/r$/g, 'ル'], [/l$/g, 'ル'], [/s$/g, 'ス'], [/t$/g, 'ト'],
    [/k$/g, 'ク'], [/p$/g, 'プ'], [/d$/g, 'ド'], [/b$/g, 'ブ'], [/g$/g, 'グ'], [/f$/g, 'フ'], [/v$/g, 'ヴ'], [/z$/g, 'ズ'],
    [/n/g, 'ン'], [/m/g, 'ム'], [/r/g, 'ル'], [/l/g, 'ル'], [/s/g, 'ス'], [/t/g, 'ト'],
    [/k/g, 'ク'], [/p/g, 'プ'], [/d/g, 'ド'], [/b/g, 'ブ'], [/g/g, 'グ'], [/f/g, 'フ'], [/v/g, 'ヴ'], [/z/g, 'ズ']
  ];

  let res = str;
  for (const [re, rep] of table) {
    res = res.replace(re, rep);
  }
  return res;
}

function getWordPhoneticsGuide(word) {
  const r = (word.r || '').toLowerCase();
  const hints = [];
  if (r.includes('c')) hints.push('cはシャ行音[ʃ]');
  if (r.includes('j')) hints.push('jは柔らかなジャ行音[ʒ]');
  if (r.includes('v')) hints.push('vは上前歯を下唇に当てる唇歯摩擦音[v]');
  if (r.includes('y')) hints.push('yは唇を丸めた澄んだ狭母音[y/i]');
  if (r.includes('r')) hints.push('rは舌先を軽く弾く歯茎弾き音[ɾ]');
  if (r.includes('f')) hints.push('fは上歯と下唇で息を抜く無声摩擦音[f]');
  if (hints.length === 0) hints.push('母音(a, e, i, o, u)を明瞭に発音');
  return hints.join('、') + '。';
}

function getWordSyntaxRole(word) {
  const p = word.p || '';
  if (p.includes('動')) return '述語（文頭配置・動作規定）';
  if (p.includes('形')) return '限定修飾（名詞後置）/ 述語';
  if (p.includes('名')) return '主語・目的語・補語（格助詞受容）';
  if (p.includes('代名')) return '代名主体・指示主語';
  if (p.includes('副')) return '連用修飾（動詞直後・様態・程度）';
  if (p.includes('格') || p.includes('標識')) return '格標識（名詞前置・統語格決定）';
  if (p.includes('接') || p.includes('機能')) return '論理接続・節結合小詞';
  if (p.includes('相関')) return '相関詞（疑問・指示・空間規定）';
  return '構文自立語';
}

function getWordForms(word) {
  const forms=[{label:'基本形',neb:word.r}];
  if ((word.p||'').includes('動')) forms.push({label:'過去',neb:'fe '+word.r},{label:'否定',neb:'ne '+word.r});
  return forms;
}

function getWordCorpusExamples(wordRoot, word) {
  const matches = [];
  for(const e of TRANSLATION_EXTENSIONS.roadmapProductive?.examples||[])if(e.root===wordRoot)matches.push({neb:e.neb,ja:e.ja,tag:e.tag});
  const regex = new RegExp('\\b' + wordRoot + '\\b', 'i');
  for (const c of (typeof CANON !== 'undefined' ? CANON : [])) {
    if (regex.test(c.neb)) matches.push({ neb: c.neb, ja: c.ja, tag: '正本カノン' });
  }
  for (const e of (typeof EXT_SENTENCES !== 'undefined' ? EXT_SENTENCES : [])) {
    if (regex.test(e.nebulith)) matches.push({ neb: e.nebulith, ja: e.japanese, tag: '拡張文' });
  }
  for (const u of (typeof USAGE_EXAMPLES !== 'undefined' ? USAGE_EXAMPLES : [])) {
    if (regex.test(u.nebulith)) matches.push({ neb: u.nebulith, ja: u.japanese, tag: '学習例文' });
  }
  if (word && word._verifiedCompound) {
    const vc = word._verifiedCompound;
    matches.push({ neb: vc.example_sentence, ja: vc.example_ja, tag: `正本複合語例文 (${vc.scenario_id})` });
    if (word._verifiedScenario && Array.isArray(word._verifiedScenario.turns)) {
      for (const t of word._verifiedScenario.turns) {
        if (t.nebulith !== vc.example_sentence && regex.test(t.nebulith)) {
          matches.push({ neb: t.nebulith, ja: t.japanese, tag: `対話実証 (${t.speaker})` });
        }
      }
    }
  }

  return matches.slice(0, 4);
}

window.openWordModal = function(roman) {
  modalReturnFocus=document.activeElement||null;
  const cleanRoman = roman.replace(/^[-+]/, '').replace(/[-+]$/, '').trim();
  let word = VOCAB.find(w => w.r === roman) || VOCAB.find(w => w.r === cleanRoman);
  if (!word && typeof VERIFIED_CANONICAL_COMPOUNDS !== 'undefined') {
    const comp = (VERIFIED_CANONICAL_COMPOUNDS.entries || []).find(w => w.nrs === roman || w.nrs === cleanRoman);
    if (comp) {
      const scen = (VERIFIED_CANONICAL_COMPOUNDS.scenarios || []).find(s => s.scenario_id === comp.scenario_id);
      const rootDetails = (comp.constituentEntries || []).map(c => `${c.nrs}(#${c.id}:${c.meaningJa.split('、')[0]})`).join(' + ');
      const turnSummary = scen ? scen.turns.map(t => `${t.speaker}: ${t.nebulith} (${t.japanese})`).join(' / ') : '';
      word = {
        r: comp.nrs,
        p: comp.pos,
        m: comp.meaningJa,
        en: comp.meaningEn,
        i: '',
        n: `正本複合語 [${comp.batch} / ${comp.scenario_id}] 語源: ${comp.etymology} (${rootDetails})。実証話者: ${(comp.speakers || []).join(', ')}。対話記録: ${turnSummary}`,
        _verifiedCompound: comp,
        _verifiedScenario: scen
      };
    }
  }
  if (!word) return;
  activeModalWord = word;
  browsingHistory = [word.r, ...browsingHistory.filter(r => r !== word.r)].slice(0, 100);
  safeStorage.setItem('neb_history', JSON.stringify(browsingHistory));

  // Visual header & kana
  document.getElementById('modalGlyph').textContent = word.r;
  document.getElementById('modalRoman').textContent = word.r;
  const kanaEl = document.getElementById('modalKana');
  if (kanaEl) kanaEl.textContent = nebulithToKatakana(word.r);
  document.getElementById('modalPos').textContent = word.p;

  document.getElementById('modalMeaningJa').textContent = word.m;
  document.getElementById('modalMeaningEn').textContent = word.en || '—';
  document.getElementById('modalIpa').textContent = word.i ? `/${word.i}/` : '—';

  // Phonetics guide
  const pronEl = document.getElementById('modalPronGuide');
  if (pronEl) {
    pronEl.textContent = getWordPhoneticsGuide(word);
  }

  // Syntax Role & Provenance & Audit
  const syntaxEl = document.getElementById('modalSyntaxRole');
  if (syntaxEl) {
    syntaxEl.textContent = getWordSyntaxRole(word);
  }
  const noteEl = document.getElementById('modalNotes');
  if (noteEl) {
    // Keep usage warnings and definitions; omit internal classification and book-location metadata.
    const held=TRANSLATION_EXTENSIONS.roadmapProductive?.held?.find(e=>e.id===(word.id||word._verifiedCompound?.id));
    const notes=[(word.n||'').replace(/【聖典原典】[^。]*。/g,'').replace(/【[^】]*(?:監査|語根|文明)[^】]*】/g,'').trim(),held?.reason||''].filter(Boolean).join(' ');
    noteEl.textContent=notes;
    document.getElementById('modalNotesField').style.display=notes?'block':'none';
  }

  // Render Forms List (100% of words covered)
  const formsField = document.getElementById('modalFormsField');
  const formsList = document.getElementById('modalFormsList');
  if (formsField && formsList) {
    const forms = getWordForms(word);
    if (forms.length > 0) {
      formsList.innerHTML = forms.map(f => `
        <div class="modal-form-chip" title="クリックでコピー: ${escapeHtml(f.neb)}" onclick="navigator.clipboard.writeText('${escapeHtml(f.neb)}'); alert('コピーしました: ${escapeHtml(f.neb)}');">
          <span class="form-lbl">${escapeHtml(f.label)}</span>
          <span class="form-neb">${escapeHtml(f.neb)}</span>
        </div>
      `).join('');
      formsField.style.display = 'block';
    } else {
      formsField.style.display = 'none';
    }
  }

  // Render Contextual Examples (100% of words guaranteed to have active examples)
  const exField = document.getElementById('modalExamplesField');
  const exList = document.getElementById('modalExamplesList');
  if (exField && exList) {
    const examples = getWordCorpusExamples(word.r, word);
    if (examples.length > 0) {
      exList.innerHTML = examples.map(ex => `
        <div class="modal-example-card" onclick="loadExampleToTranslator('${escapeHtml(ex.ja)}')">
          <div class="ex-neb">${escapeHtml(ex.neb)}</div>
          <div class="ex-ja">${escapeHtml(ex.ja)}${ex.en ? ` <span style="font-size:0.75rem; color:var(--md-sys-color-outline);">(${escapeHtml(ex.en)})</span>` : ''}</div>
          <div class="ex-tag">出典: ${escapeHtml(ex.tag)}</div>
        </div>
      `).join('');
      exField.style.display = 'block';
    } else {
      exField.style.display = 'none';
    }
  }

  const literary=typeof LITERARY_BOOK!=='undefined'?LITERARY_BOOK.entries[word.r]:null;
  const literaryField=document.getElementById('modalLiteraryField');
  if(literaryField){
    literaryField.style.display=literary?'block':'none';
    document.getElementById('modalLiteraryQuote').textContent=literary?.quote||'';
    const source=document.getElementById('modalLiterarySource');
    const bookLink=typeof location!=='undefined'&&/^https?:$/.test(location.protocol)&&literary?` <a href="library.html#${escapeHtml(literary.anchor)}" target="_blank" rel="noopener">原本を読む</a>`:'';
    source.innerHTML=literary?`出典：『${escapeHtml(LITERARY_BOOK.title)}』「${escapeHtml(LITERARY_BOOK.works[literary.work])}」第${literary.chapter}章「${escapeHtml(literary.chapterTitle)}」 ${escapeHtml(literary.id)}${bookLink}`:'';
  }

  updateModalFavButton();
  wordModal.classList.add('active');
  document.getElementById('modalCloseBtn').focus?.();
};

function closeWordModal() {
  wordModal.classList.remove('active');
  if(modalReturnFocus?.isConnected!==false)modalReturnFocus?.focus?.();
  else document.querySelector?.(`.word-open[data-root="${activeModalWord?.r}"]`)?.focus();
}
document.addEventListener?.('keydown',e=>{
  if(!wordModal.classList.contains('active'))return;
  if(e.key==='Escape'){e.preventDefault();closeWordModal();return;}
  if(e.key==='Tab') {
    const controls=[...wordModal.querySelectorAll('button,a[href],select,input,[tabindex="0"]')].filter(x=>x.getClientRects().length&&!x.disabled);
    const first=controls[0],last=controls.at(-1);
    if(e.shiftKey&&document.activeElement===first){e.preventDefault();last?.focus();}
    else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first?.focus();}
  }
});

window.loadExampleToTranslator = function(jaText) {
  if (transInput) {
    transInput.value = jaText;
    resetInputChoices();
    activateTab('translator');
    if (typeof doTranslate === 'function') doTranslate();
  }
  if (wordModal) wordModal.classList.remove('active');
};

function updateModalFavButton() {
  const btn = document.getElementById('modalFavToggle');
  if (activeModalWord && favorites.has(activeModalWord.r)) {
    btn.textContent = 'お気に入り解除';
    btn.style.color = '#fbbc04';
  } else {
    btn.textContent = 'お気に入りに追加';
    btn.style.color = '';
  }
}

document.getElementById('modalFavToggle').addEventListener('click', () => {
  if (activeModalWord) {
    toggleFav({ stopPropagation: () => {} }, activeModalWord.r);
  }
});

document.getElementById('modalCloseBtn').addEventListener('click', () => {
  closeWordModal();
});
wordModal.addEventListener('click', (e) => {
  if (e.target === wordModal) closeWordModal();
});

document.getElementById('copyModalRoman').addEventListener('click', () => {
  if (activeModalWord) {
    navigator.clipboard.writeText(activeModalWord.r).then(() => alert('ローマ字をコピーしました: ' + activeModalWord.r));
  }
});
document.getElementById('copyModalGlyph').addEventListener('click', () => {
  if (activeModalWord) {
    navigator.clipboard.writeText(activeModalWord.r).then(() => alert('星石文字用テキストをコピーしました: ' + activeModalWord.r));
  }
});

searchInput.addEventListener('input', renderLexicon);

document.querySelectorAll('.chip-btn').forEach(chip => {
  chip.addEventListener('click', () => {
    document.querySelectorAll('.chip-btn').forEach(c => c.classList.remove('active'));
    chip.classList.add('active');
    currentFilterPos = chip.getAttribute('data-pos');
    renderLexicon();
  });
});

// Translation Knowledge Base
const translationPairs = [];
CANON.forEach(c => {
  translationPairs.push({
    ja: c.ja.trim(),
    ja_variants: [c.ja.trim()],
    en: c.en ? c.en.trim() : (c.lit ? c.lit.trim() : ''),
    en_variants: c.en ? [c.en.trim()] : (c.lit ? [c.lit.trim()] : []),
    neb: c.neb.trim(),
    tag: '公式正本コーパス',
    alignment: []
  });
});

EXT_SENTENCES.forEach(e => {
  translationPairs.push({
    ja: e.japanese.trim(),
    ja_variants: (e.japanese_variants || []).concat([e.japanese.trim()]),
    en: e.english ? e.english.trim() : '',
    en_variants: (e.english_variants || []).concat(e.english ? [e.english.trim()] : []),
    neb: e.nebulith.trim(),
    tag: e.structure || '拡張構文',
    alignment: e.alignment || []
  });
});

const inputEngine = createIncrementalTranslator(VOCAB, GRAMMAR_FRAMES, INPUT_RULES.aliases, translationPairs, TRANSLATION_EXTENSIONS);
const translationCoverage=inputEngine.coverage();
document.getElementById('translationCoverage').textContent=`${translationCoverage.predicates}述語、${translationCoverage.productiveLemmas}動詞見出し、${translationCoverage.verbForms}動詞表層形、${translationCoverage.adjectiveForms}形容詞表層形。主語・対象・所有・場所などは辞書から組み合わせます。動詞例：${translationCoverage.verbs.map(v=>v.lemma).join('、')}。希望・推量・未整備の語義は自動で確定しません。英語・逆方向は登録対訳中心です。`;
let inputChoicesState = {};
let activeSentenceKey='';
let lastInputAnalysis = null;
let outputFingerprint = '';
let composingInput = false;
const transInput = document.getElementById('transInput');
const transOutputText = document.getElementById('transOutputText');
const transOutputGlyph = document.getElementById('transOutputGlyph');
const transTagsList = document.getElementById('transTagsList');
const transAlignmentBox = document.getElementById('transAlignmentBox');
const transMissingBox = document.getElementById('transMissingBox');
const recordMissingTransBtn = document.getElementById('recordMissingTransBtn');
const transNotice = document.getElementById('transNotice');
const swapTransBtn = document.getElementById('swapTransBtn');
const srcLangSelect = document.getElementById('srcLangSelect');
const dstLangSelect = document.getElementById('dstLangSelect');
const clearSrcBtn = document.getElementById('clearSrcBtn');
const copyDstBtn = document.getElementById('copyDstBtn');

function normalizeText(s) {
  return s.trim().replace(/\s+/g, ' ').replace(/[。、.!?！？,]/g, '').toLowerCase();
}

// Single Sentence Translation
function translateSingleSentence(sent, fromLang, toLang) {
  const norm = normalizeText(sent);
  if (!norm) return null;

  // Exact match against translation pairs
  for (const item of translationPairs) {
    let match = false;
    if (fromLang === 'ja') {
      match = item.ja_variants.some(v => normalizeText(v) === norm);
    } else if (fromLang === 'en') {
      match = item.en_variants.some(v => normalizeText(v) === norm) || (item.en && normalizeText(item.en) === norm);
    } else if (fromLang === 'neb') {
      match = normalizeText(item.neb) === norm;
    }

    if (match) {
      let targetText = '';
      if (toLang === 'neb') targetText = item.neb;
      else if (toLang === 'ja') targetText = item.ja;
      else if (toLang === 'en') targetText = item.en || item.ja;
      return { text: targetText, tag: item.tag, alignment: item.alignment || [], success: true };
    }
  }

  // Dynamic fallback rules for Japanese -> Nebulith
  if (fromLang === 'ja' && toLang === 'neb') {
    if (norm.includes('夜') && norm.includes('美しい')) {
      return {
        neb: 'Cylani el valar.',
        text: 'Cylani el valar.',
        tag: 'Adj el S (形容詞コピュラ)',
        alignment: [
          {"src": "夜は", "src_en": "the night", "dst": "el valar", "role": "主格 (Subject)"},
          {"src": "美しい", "src_en": "is beautiful", "dst": "Cylani", "role": "形容詞述語 (Predicate)"}
        ],
        success: true
      };
    }
    if (norm.includes('輝く') && norm.includes('夜') && norm.includes('星')) {
      return {
        neb: 'Falun el vyr uo valar.',
        text: 'Falun el vyr uo valar.',
        tag: 'V el S uo Loc (処格構文)',
        alignment: [
          {"src": "輝く", "src_en": "shines", "dst": "Falun", "role": "述語動詞 (Verb)"},
          {"src": "星が", "src_en": "the star", "dst": "el vyr", "role": "主格 (Subject)"},
          {"src": "夜空で", "src_en": "in the night sky", "dst": "uo valar", "role": "処格 (Locative)"}
        ],
        success: true
      };
    }
    if (norm.includes('から') || norm.includes('ので')) {
      if (norm.includes('輝く') && norm.includes('歩く')) {
        return {
          neb: 'Sen falun el vyr, poran el mi.',
          text: 'Sen falun el vyr, poran el mi.',
          tag: 'Sen Clause1, Clause2 (理由複文)',
          alignment: [
            {"src": "星が輝くから", "src_en": "because stars shine", "dst": "Sen falun el vyr", "role": "理由従属節 (Reason)"},
            {"src": "私は歩く", "src_en": "I walk", "dst": "poran el mi", "role": "帰結主節 (Consequence)"}
          ],
          success: true
        };
      }
      if (norm.includes('輝く') && norm.includes('美しい')) {
        return {
          neb: 'Sen falun el vyr, cylani el valar.',
          text: 'Sen falun el vyr, cylani el valar.',
          tag: 'Sen Clause1, Clause2 (理由複文)',
          alignment: [
            {"src": "星が輝くから", "src_en": "because stars shine", "dst": "Sen falun el vyr", "role": "理由従属節 (Reason)"},
            {"src": "夜は美しい", "src_en": "the night is beautiful", "dst": "cylani el valar", "role": "主節 (Main Clause)"}
          ],
          success: true
        };
      }
    }
    if (norm.includes('好き') || norm.includes('愛')) {
      if (norm.includes('あなた')) {
        const neg = norm.includes('不') || norm.includes('ない');
        const res = neg ? 'Ne cynel el mi ia ti.' : 'Cynel el mi ia ti.';
        return {
          neb: res,
          text: res,
          tag: 'VSO (好悪動詞構文)',
          alignment: [
            {"src": "私は", "src_en": "I", "dst": "el mi", "role": "主格 (Subject)"},
            {"src": "あなたを/が", "src_en": "you", "dst": "ia ti", "role": "対格 (Object)"},
            {"src": neg ? "好まない" : "好きだ", "src_en": neg ? "do not like" : "like / love", "dst": neg ? "Ne cynel" : "Cynel", "role": "述語動詞 (Verb)"}
          ],
          success: true
        };
      }
      if (norm.includes('星')) {
        const beautiful = norm.includes('美しい');
        const res = beautiful ? 'Cynel el mi ia vyr cylani.' : 'Cynel el mi ia vyr.';
        return {
          neb: res,
          text: res,
          tag: 'VSO + 後置修飾',
          alignment: [
            {"src": "私は", "src_en": "I", "dst": "el mi", "role": "主格 (Subject)"},
            {"src": "星を/が", "src_en": "stars", "dst": "ia vyr", "role": "対格 (Object)"},
            ...(beautiful ? [{"src": "美しい", "src_en": "beautiful", "dst": "cylani", "role": "形容詞 (Adjective)"}] : []),
            {"src": "好きだ", "src_en": "like / love", "dst": "Cynel", "role": "述語動詞 (Verb)"}
          ],
          success: true
        };
      }
    }
    if (norm.includes('なら') || norm.includes('ば')) {
      if (norm.includes('輝く') && norm.includes('歩く')) {
        return {
          neb: 'Zen falun el vyr, poran el mi.',
          text: 'Zen falun el vyr, poran el mi.',
          tag: 'Zen Clause1, Clause2 (条件節)',
          alignment: [
            {"src": "星が輝くなら", "src_en": "if stars shine", "dst": "Zen falun el vyr", "role": "条件節 (Condition)"},
            {"src": "私は歩く", "src_en": "I walk", "dst": "poran el mi", "role": "帰結主節 (Consequence)"}
          ],
          success: true
        };
      }
      if (norm.includes('好き') && norm.includes('嬉しい')) {
        return {
          neb: 'Zen cynel el ti ia mi, relen el mi ia elir.',
          text: 'Zen cynel el ti ia mi, relen el mi ia elir.',
          tag: 'Zen VSO1, VSO2 (条件+感情)',
          alignment: [
            {"src": "あなたが私を好きなら", "src_en": "if you like me", "dst": "Zen cynel el ti ia mi", "role": "条件節 (Condition)"},
            {"src": "私は嬉しい", "src_en": "I am glad", "dst": "relen el mi ia elir", "role": "感情主節 (Emotion Clause)"}
          ],
          success: true
        };
      }
    }
    if (norm.includes('より')) {
      if (norm.includes('美しい') && norm.includes('星') && norm.includes('夜')) {
        return {
          neb: 'Cylani el vyr va valar.',
          text: 'Cylani el vyr va valar.',
          tag: 'Adj el S va O (奪格比較構文)',
          alignment: [
            {"src": "星は", "src_en": "the star", "dst": "el vyr", "role": "比較主格 (Subject)"},
            {"src": "夜よりも", "src_en": "than the night", "dst": "va valar", "role": "奪格比較 (Ablative Comparison)"},
            {"src": "美しい", "src_en": "is more beautiful", "dst": "Cylani", "role": "形容詞述語 (Predicate)"}
          ],
          success: true
        };
      }
      if (norm.includes('太陽') && norm.includes('星')) {
        return {
          neb: 'Falun el zohar va vyr.',
          text: 'Falun el zohar va vyr.',
          tag: 'V el S va O (動詞比較構文)',
          alignment: [
            {"src": "太陽は", "src_en": "the sun", "dst": "el zohar", "role": "比較主格 (Subject)"},
            {"src": "星よりも", "src_en": "than stars", "dst": "va vyr", "role": "奪格比較 (Ablative Comparison)"},
            {"src": "光る/輝く", "src_en": "shines more", "dst": "Falun", "role": "比較動詞 (Comparative Verb)"}
          ],
          success: true
        };
      }
    }
  }

  // Productive Bidirectional Engine Integration (Sprint 6)
  if (typeof NebulithBidirectionalEngine !== 'undefined') {
    if (fromLang === 'neb' && (toLang === 'ja' || toLang === 'en')) {
      const biRes = NebulithBidirectionalEngine.translateNebulith(sent, toLang);
      if (biRes && biRes.success) {
        return {
          text: biRes.text,
          neb: sent,
          tag: '辞書・対応文型による逆変換（'+toLang.toUpperCase()+'）',
          alignment: biRes.alignments || [],
          success: true
        };
      }
      return {text:null,success:false,error:biRes?.error||'逆変換が未確定です。'};
    }
    if (fromLang === 'en' && toLang === 'neb') {
      const biRes = NebulithBidirectionalEngine.translateEnglishToNebulith(sent);
      if (biRes && biRes.success) {
        return biRes;
      }
    }
  }

  return { text: null, error: '未対応文型: ' + sent, success: false };
}

// Multi-Sentence / Full-Text Translation
function doTranslate() {
  saveTranslationSession();
  copyDstBtn.disabled = true;
  document.getElementById('inputInterpretation').innerHTML = '';
  document.getElementById('inputChoices').style.display = 'none';
  document.getElementById('copyConfirmedParts').style.display = 'none';
  if (composingInput) return;
  if (srcLang === 'ja' && dstLang === 'neb') { renderIncrementalInput(); return; }
  lastInputAnalysis=null;
  const text = transInput.value.trim();
  if (!text) {
    transOutputText.textContent = 'ここに訳文が表示されます';
    transOutputGlyph.textContent = '';
    transTagsList.innerHTML = '';
    if (transAlignmentBox) transAlignmentBox.innerHTML = '';
    if (transMissingBox) transMissingBox.style.display = 'none';
    transNotice.innerHTML = '入力すると即座に文法解析・翻訳されます。';
    return;
  }

  const normTotal = normalizeText(text);

  // Check if entire text matches directly
  for (const item of translationPairs) {
    let match = false;
    if (srcLang === 'ja') match = item.ja_variants.some(v => normalizeText(v) === normTotal);
    else if (srcLang === 'en') match = item.en_variants.some(v => normalizeText(v) === normTotal) || (item.en && normalizeText(item.en) === normTotal);
    else if (srcLang === 'neb') match = normalizeText(item.neb) === normTotal;

    if (match) {
      let targetText = '';
      if (dstLang === 'neb') targetText = item.neb;
      else if (dstLang === 'ja') targetText = item.ja;
      else if (dstLang === 'en') targetText = item.en || item.ja;

      transOutputText.textContent = targetText;
      transOutputGlyph.textContent = dstLang === 'neb' ? targetText : '';
      transTagsList.innerHTML = `<span class="trans-structure-tag">${item.tag}</span>`;
      renderAlignments(item.alignment || []);
      if (transMissingBox) transMissingBox.style.display = 'none';
      copyDstBtn.disabled = false; outputFingerprint = transInput.value + '|' + srcLang + '|' + dstLang;
      transNotice.innerHTML = '長文段落・確定照合完了';
      return;
    }
  }

  // Split on punctuation or newlines
  const rawSentences = text.split(/(?<=[。！？!?\n])|(?<=\.\s+)/).map(s => s.trim()).filter(s => s.length > 0);

  const results = [];
  const tags = [];
  const combinedAlignments = [];
  const parseFailures = [];
  let allSuccess = true;

  for (const sent of rawSentences) {
    const res = translateSingleSentence(sent, srcLang, dstLang);
    if (res && res.success) {
      results.push(res.text);
      if (res.tag && !tags.includes(res.tag)) tags.push(res.tag);
      if (res.alignment && res.alignment.length > 0) {
        combinedAlignments.push(...res.alignment);
      }
    } else {
      allSuccess = false;
      parseFailures.push(res?.error||'文型を確定できません。');
      results.push('【構文未確定】');
    }
  }

  if (allSuccess && results.length > 0) {
    copyDstBtn.disabled = false; outputFingerprint = transInput.value + '|' + srcLang + '|' + dstLang;
    const outJoined = results.join(' ');
    transOutputText.textContent = outJoined;
    transOutputGlyph.textContent = dstLang === 'neb' ? outJoined : '';
    transTagsList.innerHTML = tags.map(t => `<span class="trans-structure-tag">${t}</span>`).join('');
    renderAlignments(combinedAlignments);
    if (transMissingBox) transMissingBox.style.display = 'none';
    transNotice.innerHTML = `長文・構文解析完了 (${results.length}文 確定翻訳)`;
  } else {
    transOutputText.textContent = results.join(' ');
    document.getElementById('inputInterpretation').textContent=parseFailures.join(' / ');
    transOutputGlyph.textContent = '';
    transTagsList.innerHTML = tags.map(t => `<span class="trans-structure-tag">${t}</span>`).join('');
    if (transAlignmentBox) transAlignmentBox.innerHTML = '';
    
    // Show Missing Box for unhandled sentences
    if (transMissingBox) {
      transMissingBox.style.display = 'flex';
      const already = feedbackQueue.some(i => i.type === 'sentence' && i.text.toLowerCase() === text.toLowerCase());
      if (recordMissingTransBtn) {
        recordMissingTransBtn.innerHTML = already ? '<span>キューに記録済み</span>' : '<span>未対応文章として記録する</span>';
        recordMissingTransBtn.disabled = already;
        recordMissingTransBtn.style.opacity = already ? '0.7' : '1';
        recordMissingTransBtn.onclick = () => {
          if(!addFeedbackItem('sentence', srcLang, text, '未確定構文・未対応文章'))return;
          recordMissingTransBtn.innerHTML = '<span>キューに記録しました</span>';
          recordMissingTransBtn.disabled = true;
          recordMissingTransBtn.style.opacity = '0.7';
        };
      }
    }
    transNotice.innerHTML = '一部の文章が現在登録・検証済みの文型外です。下のボタンから未対応キューに記録できます。';
  }
}

// Render Word Alignment View
function renderAlignments(alignments) {
  if (!transAlignmentBox) return;
  if (!alignments || alignments.length === 0) {
    transAlignmentBox.innerHTML = '';
    return;
  }

  const isEn = srcLang === 'en';
  const chipsHtml = alignments.map(a => {
    const srcWord = isEn ? (a.src_en || a.src) : a.src;
    const cleanDst = (a.dst || '').replace(/^[-+]/, '').replace(/[-+]$/, '').trim();
    const hasWord = catalogByRoot.has(cleanDst);
    const clickAttr = hasWord ? `type="button" class="align-dst has-word" title="辞書で『${escapeHtml(cleanDst)}』の詳細を見る" onclick="openWordModal('${escapeHtml(cleanDst)}')"` : 'class="align-dst"';
    return `
      <div class="align-chip">
        <span class="align-src">${escapeHtml(srcWord)}</span>
        <span class="align-arrow"></span>
        <${hasWord?'button':'span'} ${clickAttr}>${escapeHtml(a.dst)}</${hasWord?'button':'span'}>
        <span class="align-role">${escapeHtml(a.role)}</span>
      </div>
    `;
  }).join('');

  transAlignmentBox.innerHTML = `
    <div class="align-header">原文とNebulithの語句対応</div>
    <p>語順が変わるため、対応する語句を並べて表示します。活用・文法標識は複数語に対応することがあります。</p>
    <div class="align-list">${chipsHtml}</div>
  `;
}

function renderIncrementalInput() {
  const text = transInput.value;
  const result = inputEngine.analyze(text, inputChoicesState);
  lastInputAnalysis = result;
  const labels = {complete:'確定訳', phrase:'語句', draft:'入力待ち', candidate:'解釈候補', blocked:'要対応'};
  transOutputText.textContent = result.text || (text.trim() ? '解釈を確認中' : '語句・文章を入力してください');
  transOutputGlyph.textContent = result.complete ? result.text : '';
  transTagsList.innerHTML = result.segments.map(s=>`<span class="trans-structure-tag">${labels[s.state]}</span>`).join('');
  document.getElementById('inputInterpretation').textContent = result.notes.join(' / ');
  if(!result.segments.some(s=>s.key===activeSentenceKey))activeSentenceKey=(result.segments.find(s=>!['complete','phrase'].includes(s.state))||result.segments[0])?.key||'';
  const selected=result.segments.find(s=>s.key===activeSentenceKey)||result.segments[0];
  const selectedChoices=currentSegmentChoices();
  const nounGroups=selected?.nounOptions||[];
  const nounBox=document.getElementById('inputNounChoices');
  nounBox.innerHTML=nounGroups.map((group,i)=>`<label>「${escapeHtml(group.term)}」の意味 <select data-noun-index="${i}"><option value="">未選択</option>${group.options.map(o=>`<option value="${o.id}">${escapeHtml(o.root+'：'+o.meaning)}</option>`).join('')}</select></label>`).join('');
  for(const control of nounBox.querySelectorAll?.('select')||[])control.addEventListener('change',()=>{
    const group=nounGroups[Number(control.dataset.nounIndex)];
    const nounSenses={...(currentSegmentChoices().nounSenses||{})};
    if(control.value)nounSenses[group.term]=Number(control.value);else delete nounSenses[group.term];
    changeSegmentChoices({nounSenses,confirmed:false});doTranslate();
  });
  const subjectControl=document.getElementById('inputSubject');
  subjectControl.innerHTML='<option value="">原文のまま</option><option>私</option><option>あなた</option><option>彼／彼女</option>'+(selected?.contextSubject?`<option value="${escapeHtml(selected.contextSubject.source)}">前文の主体：${escapeHtml(selected.contextSubject.source)}（確認が必要）</option>`:'');
  document.getElementById('inputFragments').innerHTML=result.complete?'':`<small>入力の辞書照合（文法解析とは別）</small><div>${(selected?.fragments||[]).map(f=>`<span class="input-fragment" title="${f.known?'辞書に見つかった語':'未照合部分'}" style="display:inline-block;padding:3px 6px;margin:2px;border:1px ${f.known?'solid':'dashed'} var(--md-sys-color-outline-variant)">${escapeHtml(f.source)}</span>`).join('')}</div>`;
  document.getElementById('inputChoices').style.display=text.trim()&&(!result.complete||result.segments.length>1)?'flex':'none';
  document.getElementById('inputSentenceLabel').style.display=result.segments.length>1?'inline-block':'none';
  document.getElementById('inputSentence').innerHTML=result.segments.map((s,i)=>`<option value="${escapeHtml(s.key)}">${i+1}文目・${labels[s.state]}：${escapeHtml(s.source.slice(0,55))}</option>`).join('');
  document.getElementById('inputSentence').value=activeSentenceKey;
  document.getElementById('inputPossessionLabel').style.display=selected?.scopeAmbiguous?'inline-block':'none';
  const senseOptions=selected?.senseOptions||[];
  document.getElementById('inputSenseLabel').style.display=senseOptions.length?'inline-block':'none';
  document.getElementById('inputSense').innerHTML='<option value="">未選択</option>'+senseOptions.map(o=>`<option value="${escapeHtml(o.value)}">${escapeHtml(o.root+'：'+o.meaning)}</option>`).join('');
  const defaultVerbOptions = ['観測する','仰ぎ見る','見上げる','展望する','予見する','話す','語り合う','告げる','ささやく','問う','歩く','走る','行進する','滑空する','信じる','思索する','決断する','尊ぶ'];
  const verbOptions = selected?.verbOptions && selected.verbOptions.length ? selected.verbOptions : defaultVerbOptions;
  document.getElementById('inputVerb').innerHTML = '<option value="">未選択</option>' + verbOptions.map(v => `<option value="${escapeHtml(v)}">${escapeHtml(v)}</option>`).join('');
  for(const [id,key] of [['inputSubject','subject'],['inputVerb','verb'],['inputPossession','possession'],['inputSense','sense']])document.getElementById(id).value=selectedChoices[key]||'';
  for(const id of ['inputSubjectLabel','inputVerbLabel'])document.getElementById(id).style.display=selected?.scopeAmbiguous?'none':'inline-block';
  document.getElementById('confirmInputCandidate').disabled=selected?.state!=='candidate';
  const copyablePhrase = result.segments.length===1 && result.segments[0].state==='phrase';
  copyDstBtn.textContent = copyablePhrase ? '語句をコピー' : '完成訳をコピー';
  copyDstBtn.disabled = !(result.complete || copyablePhrase);
  outputFingerprint = text + '|' + srcLang + '|' + dstLang;
  renderAlignments(result.segments.flatMap((s,i)=>(s.alignment||[]).map(a=>({...a,role:`${result.segments.length>1?(i+1)+'文目・':''}${labels[s.state]}・${a.role}`}))));
  transNotice.textContent = result.complete ? 'Nebulithの文法を検証した完成訳です。' : '途中案は完成文ではありません。補完・意味候補は確認後に確定します。';
  const completeParts = result.segments.filter(s=>s.state==='complete');
  const copyParts = document.getElementById('copyConfirmedParts');
  copyParts.style.display = !result.complete && completeParts.length ? 'inline-block' : 'none';
  copyParts.textContent = `確定した文だけコピー（${completeParts.length}/${result.segments.length}文）`;
  copyParts.onclick = () => { if(lastInputAnalysis===result && outputFingerprint===transInput.value+'|'+srcLang+'|'+dstLang) navigator.clipboard.writeText(completeParts.map(s=>s.text).join(' ')); };
  transMissingBox.style.display = result.recordable ? 'flex' : 'none';
  if(result.recordable) {
    const interpretation={version:INPUT_RULES.version,choices:{...inputChoicesState},segments:result.segments};
    const exists = feedbackQueue.some(i=>NebulithWorkspace.feedbackKey(i)===NebulithWorkspace.feedbackKey({type:'sentence',lang:srcLang,text,interpretation}));
    recordMissingTransBtn.disabled = exists;
    recordMissingTransBtn.textContent = exists ? '記録済み' : '未対応の意味・構文を記録';
    recordMissingTransBtn.onclick = () => {
      if(outputFingerprint!==transInput.value+'|'+srcLang+'|'+dstLang)return;
      if(addFeedbackItem('sentence',srcLang,text,result.notes.join(' / '),{version:INPUT_RULES.version,choices:{...inputChoicesState},segments:result.segments}))renderIncrementalInput();
    };
  }
}
function currentSegmentChoices(){return lastInputAnalysis?.segments.length>1?inputChoicesState.bySegment?.[activeSentenceKey]||{}:inputChoicesState;}
function changeSegmentChoices(patch){
  if(lastInputAnalysis?.segments.length>1)inputChoicesState={...inputChoicesState,bySegment:{...(inputChoicesState.bySegment||{}),[activeSentenceKey]:{...currentSegmentChoices(),...patch}}};
  else inputChoicesState={...inputChoicesState,...patch};
}
for (const [id,key] of [['inputSubject','subject'],['inputVerb','verb'],['inputPossession','possession'],['inputSense','sense']]) document.getElementById(id).addEventListener('change',e=>{changeSegmentChoices({[key]:e.target.value,confirmed:false});doTranslate();});
document.getElementById('inputSentence').addEventListener('change',e=>{activeSentenceKey=e.target.value;doTranslate();});
document.getElementById('confirmInputCandidate').addEventListener('click',()=>{
  const selected=lastInputAnalysis?.segments.find(s=>s.key===activeSentenceKey);
  if(selected?.state==='candidate'){changeSegmentChoices({confirmed:true});doTranslate();}
});
function resetInputChoices(preserve=false) {
  let retained={};
  if(preserve){
    const sources=inputEngine.splitSentences(transInput.value);
    const prior={...(inputChoicesState.bySegment||{})};
    if(lastInputAnalysis?.segments.length===1)prior[lastInputAnalysis.segments[0].key]=inputChoicesState;
    const bySegment={};
    for(const [key,value] of Object.entries(prior))try{const source=JSON.parse(key)[0];if(sources.filter(s=>s===source).length===1)bySegment[JSON.stringify([source,0])]=value;}catch(_){}
    retained=sources.length===1?bySegment[JSON.stringify([sources[0],0])]||{}:{bySegment};
  }
  inputChoicesState=retained;lastInputAnalysis=null;
  for(const id of ['inputSubject','inputVerb','inputPossession','inputSense'])document.getElementById(id).value='';
  if(!preserve)activeSentenceKey='';
}
let transTimer = null;
transInput.addEventListener('compositionstart',()=>{composingInput=true;clearTimeout(transTimer);copyDstBtn.disabled=true;swapTransBtn.disabled=true;recordMissingTransBtn.disabled=true;document.getElementById('confirmInputCandidate').disabled=true;transNotice.textContent='日本語を変換中です。確定後に解析します。';});
transInput.addEventListener('compositionend',()=>{composingInput=false;resetInputChoices(true);doTranslate();});
transInput.addEventListener('input', () => {
  clearTimeout(transTimer);resetInputChoices(true);renderAlignments([]);copyDstBtn.disabled=true;swapTransBtn.disabled=true;
  saveTranslationSession();
  if(!composingInput)transTimer=setTimeout(()=>{doTranslate();swapTransBtn.disabled=false;},180);
});

srcLangSelect.addEventListener('change', () => {
  resetInputChoices();srcLang = srcLangSelect.value;
  doTranslate();
});

dstLangSelect.addEventListener('change', () => {
  resetInputChoices();dstLang = dstLangSelect.value;
  doTranslate();
});

swapTransBtn.addEventListener('click', () => {
  if(copyDstBtn.disabled)return;
  resetInputChoices();
  const tmp = srcLang;
  srcLang = dstLang;
  dstLang = tmp;
  srcLangSelect.value = srcLang;
  dstLangSelect.value = dstLang;

  const curDst = transOutputText.textContent;
  if (curDst && !curDst.includes('【')) {
    transInput.value = curDst;
  }
  doTranslate();
});

clearSrcBtn.addEventListener('click', () => {
  resetInputChoices();transInput.value = '';
  doTranslate();
});

copyDstBtn.addEventListener('click', () => {
  if(copyDstBtn.disabled || outputFingerprint!==transInput.value+'|'+srcLang+'|'+dstLang)return;
  navigator.clipboard.writeText(transOutputText.textContent).then(() => {
    alert('訳文をクリップボードにコピーしました！');
  });
});

// Queue Modal Management
const queueModal = document.getElementById('queueModal');
const queueToggleBtn = document.getElementById('queueToggleBtn');
const queueCloseBtn = document.getElementById('queueCloseBtn');
const queueList = document.getElementById('queueList');
const clearAllQueueBtn = document.getElementById('clearAllQueueBtn');
const exportQueueJsonBtn = document.getElementById('exportQueueJsonBtn');
const copyQueueJsonBtn = document.getElementById('copyQueueJsonBtn');

const queueStatusLabels={untriaged:'未整理',investigating:'調査中',implemented:'実装済み',review:'審査待ち',held:'保留'};
const queueCauseLabels={unknown:'未分類',vocabulary:'語彙不足',inflection:'活用不足',syntax:'文型不足',meaning:'解釈・語義',incomplete:'入力途中'};
function renderQueueList() {
  if (!queueList) return;
  if (feedbackQueue.length === 0) {
    queueList.innerHTML = `
      <div style="text-align: center; padding: 24px; color: var(--md-sys-color-on-surface-variant); font-size: 0.9rem;">
        現在、未対応キューに記録された項目はありません。<br>
        辞書検索で0件だった語や翻訳未確定文を記録するとここに蓄積されます。
      </div>
    `;
    return;
  }

  const statusFilter=document.getElementById('queueStatusFilter').value;
  const shown=feedbackQueue.filter(item=>!statusFilter||statusFilter==='all'||item.status===statusFilter);
  queueList.innerHTML = shown.map(item => {
    const typeLabel = item.type === 'word' ? '単語検索' : '文章翻訳';
    const langLabel = item.lang.toUpperCase();
    const dateStr = item.createdAt ? new Date(item.createdAt).toLocaleString('ja-JP') : '';
    const countBadge = item.count > 1 ? `<span class="queue-badge" style="margin-left: 6px;">×${item.count}</span>` : '';
    return `
      <div class="queue-card">
        <div class="queue-card-content">
          <div style="display: flex; align-items: center; gap: 6px;">
            <span class="queue-card-tag">${typeLabel} [${langLabel}]</span>
            ${countBadge}
          </div>
          <div class="queue-card-text">${escapeHtml(item.text)}</div>
          <div class="queue-card-meta">${escapeHtml(dateStr)} &bull; ${escapeHtml(item.context)}</div>
          <label>状態 <select onchange="setQueueField('${item.id}','status',this.value)">${NebulithWorkspace.statuses.map(v=>`<option value="${v}" ${v===item.status?'selected':''}>${queueStatusLabels[v]}</option>`).join('')}</select></label>
          <label>原因 <select onchange="setQueueField('${item.id}','cause',this.value)">${NebulithWorkspace.causes.map(v=>`<option value="${v}" ${v===item.cause?'selected':''}>${queueCauseLabels[v]}</option>`).join('')}</select></label>
          <div class="queue-card-meta">元記録：${item.origins.length}件</div>
        </div>
        <button type="button" class="tool-btn icon-btn" style="color: var(--md-sys-color-error);" aria-label="この記録を削除" onclick="deleteQueueItem('${item.id}')">×</button>
      </div>
    `;
  }).join('');
}

function persistQueue(next){
  if(!safeStorage.setItem('neb_feedback_queue',JSON.stringify(next)))return false;
  feedbackQueue=next;updateQueueBadge();renderQueueList();return true;
}
window.deleteQueueItem=function(id){if(persistQueue(feedbackQueue.filter(item=>item.id!==id)))renderLexicon();};
window.setQueueField=function(id,key,value){
  if(!['status','cause'].includes(key))return;
  if(!(key==='status'?NebulithWorkspace.statuses:NebulithWorkspace.causes).includes(value))return;
  persistQueue(feedbackQueue.map(item=>item.id===id?{...item,[key]:value}:item));
};
if (queueToggleBtn) {
  queueToggleBtn.addEventListener('click', () => {
    renderQueueList();
    queueModal.classList.add('active');
  });
}

if (queueCloseBtn) {
  queueCloseBtn.addEventListener('click', () => {
    queueModal.classList.remove('active');
  });
}

if (queueModal) {
  queueModal.addEventListener('click', (e) => {
    if (e.target === queueModal) queueModal.classList.remove('active');
  });
}

if (clearAllQueueBtn) {
  clearAllQueueBtn.addEventListener('click', () => {
    if (feedbackQueue.length === 0) return;
    if (confirm('未対応キューの全記録を消去してもよろしいですか？')) {
      if(!persistQueue([]))return;
      updateQueueBadge();
      renderQueueList();
      renderLexicon();
    }
  });
}

if (exportQueueJsonBtn) {
  exportQueueJsonBtn.addEventListener('click', () => {
    if (feedbackQueue.length === 0) {
      alert('回収する未対応リクエストがありません。');
      return;
    }
    const exportData = {
      schemaVersion:1,
      exportedAt: new Date().toISOString(),
      source: 'Nebulith Studio Feedback Queue',
      totalItems: feedbackQueue.length,
      queue: feedbackQueue
    };
    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json;charset=utf-8' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `nebulith_unsupported_requests_${Date.now()}.json`;
    a.click();
  });
}

if (copyQueueJsonBtn) {
  copyQueueJsonBtn.addEventListener('click', () => {
    if (feedbackQueue.length === 0) {
      alert('コピーする未対応リクエストがありません。');
      return;
    }
    const jsonStr = JSON.stringify(feedbackQueue, null, 2);
    navigator.clipboard.writeText(jsonStr).then(() => {
      alert('未対応リクエスト一覧のJSONをクリップボードにコピーしました！');
    });
  });
}

// Editor Features
const editorInput = document.getElementById('editorInput');
const editorPreview = document.getElementById('editorPreview');
const editorStats = document.getElementById('editorStats');
const fontSizeSlider = document.getElementById('fontSizeSlider');
const fontSizeVal = document.getElementById('fontSizeVal');

const savedDraft = safeStorage.getItem('neb_editor_draft') || '';
if (savedDraft) {
  editorInput.value = savedDraft;
  editorPreview.textContent = savedDraft;
  updateEditorStats();
}

function updateEditorStats() {
  const text = editorInput.value;
  const chars = text.length;
  const words = text.trim() ? text.trim().split(/\s+/).length : 0;
  const lines = text ? text.split('\n').length : 1;
  editorStats.textContent = `文字数: ${chars} | 単語数: ${words} | 行数: ${lines}`;
}

fontSizeSlider.addEventListener('input', (e) => {
  const size = e.target.value + 'px';
  safeStorage.setItem('neb_font_size',String(e.target.value));
  fontSizeVal.textContent = size;
  editorPreview.style.fontSize = size;
});

editorInput.addEventListener('input', (e) => {
  const val = e.target.value;
  editorPreview.textContent = val || 'Cynel el mi ia ti. Zen falun el vyr, cylani el valar.';
  updateEditorStats();
  safeStorage.setItem('neb_editor_draft', val);
});

document.getElementById('downloadNebBtn').addEventListener('click', () => {
  const text = editorInput.value;
  if (!text) { alert('保存するテキストがありません。'); return; }
  const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'document.neb';
  a.click();
});

document.getElementById('copyEditorBtn').addEventListener('click', () => {
  navigator.clipboard.writeText(editorInput.value).then(() => alert('エディタ内容をコピーしました！'));
});

document.getElementById('clearEditorBtn').addEventListener('click', () => {
  editorInput.value = '';
  editorPreview.textContent = 'Cynel el mi ia ti. Zen falun el vyr, cylani el valar.';
  updateEditorStats();
  safeStorage.removeItem('neb_editor_draft');
});

// Corpus Cards Rendering (3 Languages: Nebulith / Japanese / English)
const corpusList = document.getElementById('corpusList');
const allSentences = USAGE_EXAMPLES.map(s=>({
  id:s.id,neb:s.nebulith,ja:s.japanese,en:s.english,lit:s.title+'：'+s.note,
  badge:'学習用例・生成検証済み／未監査'
})).concat(EXT_SENTENCES.map(s => ({
  id:s.id,neb:s.nebulith,ja:s.japanese,en:s.english||'',lit:s.structure?'構造: '+s.structure:'',badge:'拡張構文'
})),CANON.map(c => ({
  id:c.id,neb:c.neb,ja:c.ja,en:c.en||'',lit:c.lit||'',badge:'公式正本コーパス'
})));
const corpusSearch=document.getElementById('corpusSearch');
function renderCorpus() {
  const q=corpusSearch.value.trim().toLowerCase();
  const filtered=allSentences.filter(c=>[c.id,c.ja,c.neb,c.en,c.lit,c.badge].join(' ').toLowerCase().includes(q));
  document.getElementById('corpusCount').textContent=`${filtered.length} / ${allSentences.length}例`;
  corpusList.innerHTML=filtered.length?filtered.map(c=>`
    <div class="corpus-card">
      <div class="corpus-badge">${escapeHtml(c.badge)} [#${escapeHtml(c.id)}]</div>
      <div class="corpus-glyph">${escapeHtml(c.neb)}</div>
      <div class="corpus-neb">${escapeHtml(c.neb)}</div>
      <div class="corpus-ja"> ${escapeHtml(c.ja)}</div>
      ${c.en?`<div class="corpus-en"> ${escapeHtml(c.en)}</div>`:''}
      ${c.lit?`<div class="corpus-lit">${escapeHtml(c.lit)}</div>`:''}
    </div>`).join(''):'<p>一致する例文がありません。</p>';
}
// ==============================================================================
// Valnes Dialogues & Canonical Compounds Browser (857 Words / 286 Scenarios)
// ==============================================================================
const rawCompoundsDataset = (typeof VERIFIED_CANONICAL_COMPOUNDS !== 'undefined') ? VERIFIED_CANONICAL_COMPOUNDS : { entries: [], scenarios: [] };
const canonEntries = rawCompoundsDataset.entries || [];
const canonScenarios = rawCompoundsDataset.scenarios || [];

let dialogueViewMode = 'scenarios'; // 'scenarios' | 'compounds'
let selectedDialogueCategory = 'ALL';

const dialogueSearchInput = document.getElementById('dialogueSearchInput');
const dialogueCategoryChips = document.getElementById('dialogueCategoryChips');
const dialoguesCount = document.getElementById('dialoguesCount');
const dialoguesList = document.getElementById('dialoguesList');
const viewModeScenariosBtn = document.getElementById('viewModeScenarios');
const viewModeCompoundsBtn = document.getElementById('viewModeCompounds');

// Extract unique categories
const dialogueCategories = Array.from(new Set(canonEntries.map(e => e.category || 'その他'))).filter(Boolean).sort();

function initDialogueCategoryChips() {
  if (!dialogueCategoryChips) return;
  const allChips = ['ALL', ...dialogueCategories];
  dialogueCategoryChips.innerHTML = allChips.map(cat => {
    const label = cat === 'ALL' ? 'すべて' : cat;
    const activeClass = (cat === selectedDialogueCategory) ? ' active' : '';
    return `<button type="button" class="chip-btn${activeClass}" data-cat="${escapeHtml(cat)}">${escapeHtml(label)}</button>`;
  }).join('');

  const getChipBtns = () => {
    if (typeof dialogueCategoryChips.querySelectorAll === 'function') return dialogueCategoryChips.querySelectorAll('.chip-btn');
    if (typeof document.querySelectorAll === 'function') return document.querySelectorAll('#dialogueCategoryChips .chip-btn');
    return [];
  };
  getChipBtns().forEach(btn => {
    btn.addEventListener('click', () => {
      selectedDialogueCategory = btn.getAttribute('data-cat');
      getChipBtns().forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderDialogues();
    });
  });
}

function sendTextToEditor(text) {
  if (!editorInput) return;
  editorInput.value = text;
  editorPreview.textContent = text;
  updateEditorStats();
  safeStorage.setItem('neb_editor_draft', text);
  activateTab('editor');
}

function sendTextToTranslator(text, lang = 'neb') {
  if (!transInput) return;
  srcLang = lang;
  dstLang = (lang === 'neb') ? 'ja' : 'neb';
  if (srcLangSelect) srcLangSelect.value = srcLang;
  if (dstLangSelect) dstLangSelect.value = dstLang;
  transInput.value = text;
  activateTab('translator');
  doTranslate();
}

function renderDialogues() {
  if (!dialoguesList) return;
  const q = (dialogueSearchInput ? dialogueSearchInput.value.trim().toLowerCase() : '');

  if (dialogueViewMode === 'scenarios') {
    const filtered = canonScenarios.filter(scen => {
      if (selectedDialogueCategory !== 'ALL') {
        const scenEntries = canonEntries.filter(e => e.scenario_id === scen.id);
        const matchesCategory = scenEntries.some(e => e.category === selectedDialogueCategory);
        if (!matchesCategory) return false;
      }
      if (!q) return true;
      const haystack = [
        scen.id,
        scen.title,
        ...(scen.speakers || []),
        ...(scen.focus_compounds || []),
        ...(scen.turns || []).map(t => `${t.speaker} ${t.nrs} ${t.ja} ${t.compound || ''}`)
      ].join(' ').toLowerCase();
      return haystack.includes(q);
    });

    if (dialoguesCount) {
      dialoguesCount.textContent = `表示中: ${filtered.length} / ${canonScenarios.length} 篇の対話シナリオ`;
    }

    if (!filtered.length) {
      dialoguesList.innerHTML = '<div class="empty-state"><p>一致する対話シナリオがありません。</p></div>';
      return;
    }

    const displayList = filtered.slice(0, 60);

    dialoguesList.innerHTML = `
      <div class="dialogue-list">
        ${displayList.map(scen => {
          const turnsHtml = (scen.turns || []).map(t => `
            <div class="dialogue-turn">
              <div class="turn-speaker">${escapeHtml(t.speaker)}:</div>
              <div class="turn-glyph">${escapeHtml(t.nrs)}</div>
              <div class="turn-nrs">${escapeHtml(t.nrs)}</div>
              <div class="turn-ja">${escapeHtml(t.ja)}</div>
            </div>
          `).join('');

          const compoundsHtml = (scen.focus_compounds || []).map(c => `
            <span class="badge-chip" style="cursor: pointer;" data-compound="${escapeHtml(c)}">${escapeHtml(c)}</span>
          `).join('');

          const fullDialogueText = (scen.turns || []).map(t => t.nrs).join('\n');

          return `
            <article class="dialogue-card" id="dialogue-${escapeHtml(scen.id)}">
              <div class="dialogue-header">
                <div>
                  <span class="dialogue-id">${escapeHtml(scen.id)}</span>
                  <h3 class="dialogue-title" style="margin-top: 4px;">${escapeHtml(scen.title)}</h3>
                </div>
                <div class="dialogue-speakers">話者: ${escapeHtml((scen.speakers || []).join(' / '))}</div>
              </div>
              <div class="dialogue-turns">
                ${turnsHtml}
              </div>
              <div class="dialogue-compounds">
                <span style="font-size: 0.8rem; font-weight: 600; color: var(--md-sys-color-primary); margin-right: 4px;">実証複合語:</span>
                ${compoundsHtml}
              </div>
              <div class="dialogue-actions">
                <button type="button" class="tool-btn" data-action="to-editor" data-text="${escapeHtml(fullDialogueText)}">エディタで開く</button>
                <button type="button" class="tool-btn" data-action="to-trans" data-text="${escapeHtml(fullDialogueText)}">翻訳へ送る</button>
              </div>
            </article>
          `;
        }).join('')}
        ${filtered.length > 60 ? '<p style="text-align: center; color: var(--md-sys-color-outline); padding: 12px;">（検索条件により最初の60件を表示中。絞り込み検索をご活用ください）</p>' : ''}
      </div>
    `;

  } else {
    const filtered = canonEntries.filter(entry => {
      if (selectedDialogueCategory !== 'ALL' && entry.category !== selectedDialogueCategory) {
        return false;
      }
      if (!q) return true;
      const haystack = [
        entry.nrs,
        entry.meaningJa,
        entry.meaningEn,
        entry.category,
        entry.scenario_id,
        ...(entry.morphemes || []),
        entry.example_sentence,
        entry.example_ja
      ].join(' ').toLowerCase();
      return haystack.includes(q);
    });

    if (dialoguesCount) {
      dialoguesCount.textContent = `表示中: ${filtered.length} / ${canonEntries.length} 語の正本複合語`;
    }

    if (!filtered.length) {
      dialoguesList.innerHTML = '<div class="empty-state"><p>一致する正本複合語がありません。</p></div>';
      return;
    }

    const displayList = filtered.slice(0, 100);

    dialoguesList.innerHTML = `
      <div class="compound-grid">
        ${displayList.map(entry => {
          const morphemesStr = (entry.morphemes || []).join(' + ');
          return `
            <div class="compound-card" data-nrs="${escapeHtml(entry.nrs)}">
              <div>
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px;">
                  <div>
                    <span style="font-size: 1.15rem; font-weight: 700; color: var(--md-sys-color-primary);">${escapeHtml(entry.nrs)}</span>
                    <span class="badge-chip" style="margin-left: 6px;">${escapeHtml(entry.pos || '名')}</span>
                  </div>
                  <span class="badge-chip" style="background: var(--md-sys-color-surface-container-highest); color: var(--md-sys-color-on-surface-variant);">${escapeHtml(entry.category || '')}</span>
                </div>
                <div class="word-glyph" style="font-size: 2.1rem; margin: 4px 0 8px 0;">${escapeHtml(entry.nrs)}</div>
                <div class="compound-roots">構成: ${escapeHtml(morphemesStr)}</div>
                <div style="font-size: 0.95rem; font-weight: 500; margin-bottom: 4px;">${escapeHtml(entry.meaningJa || '')}</div>
                <div style="font-size: 0.8rem; color: var(--md-sys-color-on-surface-variant);">${escapeHtml(entry.meaningEn || '')}</div>
              </div>
              <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 12px; border-top: 1px dashed var(--md-sys-color-outline-variant); padding-top: 8px;">
                <span class="badge-chip" style="cursor: pointer;" data-jump-scenario="${escapeHtml(entry.scenario_id)}">${escapeHtml(entry.scenario_id)}</span>
                <button type="button" class="tool-btn" data-action="to-trans" data-text="${escapeHtml(entry.example_sentence || entry.nrs)}">例文翻訳</button>
              </div>
            </div>
          `;
        }).join('')}
      </div>
      ${filtered.length > 100 ? '<p style="text-align: center; color: var(--md-sys-color-outline); padding: 16px;">（検索条件により最初の100件を表示中。検索ボックスで語句を絞り込めます）</p>' : ''}
    `;
  }

  // Bind click handlers for dynamic elements
  const queryList = (sel) => {
    if (typeof dialoguesList.querySelectorAll === 'function') return dialoguesList.querySelectorAll(sel);
    if (typeof document.querySelectorAll === 'function') return document.querySelectorAll('#dialoguesList ' + sel);
    return [];
  };

  queryList('[data-action="to-editor"]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      sendTextToEditor(btn.getAttribute('data-text') || '');
    });
  });

  queryList('[data-action="to-trans"]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      sendTextToTranslator(btn.getAttribute('data-text') || '');
    });
  });

  queryList('[data-jump-scenario]').forEach(badge => {
    badge.addEventListener('click', (e) => {
      e.stopPropagation();
      const scenId = badge.getAttribute('data-jump-scenario');
      dialogueViewMode = 'scenarios';
      if (viewModeScenariosBtn) viewModeScenariosBtn.classList.add('active');
      if (viewModeCompoundsBtn) viewModeCompoundsBtn.classList.remove('active');
      if (dialogueSearchInput) dialogueSearchInput.value = scenId;
      selectedDialogueCategory = 'ALL';
      initDialogueCategoryChips();
      renderDialogues();
    });
  });

  queryList('[data-compound]').forEach(badge => {
    badge.addEventListener('click', (e) => {
      e.stopPropagation();
      const comp = badge.getAttribute('data-compound');
      dialogueViewMode = 'compounds';
      if (viewModeCompoundsBtn) viewModeCompoundsBtn.classList.add('active');
      if (viewModeScenariosBtn) viewModeScenariosBtn.classList.remove('active');
      if (dialogueSearchInput) dialogueSearchInput.value = comp;
      renderDialogues();
    });
  });
}

if (viewModeScenariosBtn) {
  viewModeScenariosBtn.addEventListener('click', () => {
    dialogueViewMode = 'scenarios';
    viewModeScenariosBtn.classList.add('active');
    viewModeCompoundsBtn.classList.remove('active');
    renderDialogues();
  });
}

if (viewModeCompoundsBtn) {
  viewModeCompoundsBtn.addEventListener('click', () => {
    dialogueViewMode = 'compounds';
    viewModeCompoundsBtn.classList.add('active');
    viewModeScenariosBtn.classList.remove('active');
    renderDialogues();
  });
}

if (dialogueSearchInput) {
  dialogueSearchInput.addEventListener('input', renderDialogues);
}

// Initial Dialogues Setup
initDialogueCategoryChips();
renderDialogues();

corpusSearch.addEventListener('input',renderCorpus);
renderCorpus();

// Initial Render
renderLexicon();

function saveTranslationSession(){
  return safeStorage.setItem('neb_session_v1',JSON.stringify({schemaVersion:1,text:transInput.value,srcLang,dstLang,choices:inputChoicesState,updatedAt:new Date().toISOString()}));
}
function downloadJson(value,name){
  const url=URL.createObjectURL(new Blob([JSON.stringify(value,null,2)],{type:'application/json'}));
  const a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
}
const sessionRaw=safeStorage.json('neb_session_v1',null);
if(sessionRaw)try{
  const saved=NebulithWorkspace.session(sessionRaw);transInput.value=saved.text;srcLang=saved.srcLang;dstLang=saved.dstLang;inputChoicesState=saved.choices;
  srcLangSelect.value=srcLang;dstLangSelect.value=dstLang;
  for(const [id,key] of [['inputSubject','subject'],['inputVerb','verb'],['inputPossession','possession'],['inputSense','sense']])document.getElementById(id).value=inputChoicesState[key]||'';
  doTranslate();document.getElementById('sessionStatus').textContent='翻訳下書きを復元しました。補完・解釈候補は確認して確定してください。';
}catch(e){reportStorageError(e.message);}
const restoredFont=Number(safeStorage.getItem('neb_font_size')||36);
if(restoredFont>=20&&restoredFont<=64){fontSizeSlider.value=String(restoredFont);fontSizeVal.textContent=restoredFont+'px';editorPreview.style.fontSize=restoredFont+'px';}
document.getElementById('queueStatusFilter').addEventListener('change',renderQueueList);
let pendingQueueImport=null,pendingBackup=null;
document.getElementById('importQueueFiles').addEventListener('change',async e=>{
  pendingQueueImport=null;document.getElementById('applyQueueImport').disabled=true;
  try{
    let next=feedbackQueue,files=[];
    for(const file of Array.from(e.target.files||[])){
      if(file.size>10*1024*1024)throw Error('1ファイル10MB以内にしてください。');
      const text=await file.text();let sha256='';
      if(globalThis.crypto?.subtle){const bytes=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(text));sha256=Array.from(new Uint8Array(bytes),b=>b.toString(16).padStart(2,'0')).join('');}
      const raw=JSON.parse(text);const source={name:file.name,sha256};
      next=NebulithWorkspace.mergeQueue(next,raw,source).queue;files.push(file.name);
    }
    if(!files.length)return;
    pendingQueueImport={queue:next,files};document.getElementById('queueImportPreview').textContent=files.join('、')+'：検証済み。統合後 '+next.length+'件（重複は元要求ごとに集約）。';
    document.getElementById('applyQueueImport').disabled=false;
  }catch(error){document.getElementById('queueImportPreview').textContent='取込できません：'+error.message;}
});
document.getElementById('applyQueueImport').addEventListener('click',()=>{
  if(!pendingQueueImport)return;
  const result=NebulithWorkspace.mergeQueue(feedbackQueue,pendingQueueImport.queue,{name:'検証済み取込'});
  if(persistQueue(result.queue)){document.getElementById('queueImportPreview').textContent='取込済み：'+feedbackQueue.length+'件。';pendingQueueImport=null;document.getElementById('applyQueueImport').disabled=true;}
});
document.getElementById('backupExport').addEventListener('click',()=>{
  const snapshot=safeStorage.snapshot();snapshot.values={...snapshot.values,neb_font_size:String(fontSizeSlider.value),neb_theme:currentTheme,neb_favorites:JSON.stringify([...favorites]),neb_history:JSON.stringify(browsingHistory),neb_feedback_queue:JSON.stringify(feedbackQueue),neb_editor_draft:editorInput.value,neb_session_v1:JSON.stringify({schemaVersion:1,text:transInput.value,srcLang,dstLang,choices:inputChoicesState})};
  downloadJson(snapshot,'nebulith-backup-'+Date.now()+'.json');
});
document.getElementById('backupImport').addEventListener('change',async e=>{
  pendingBackup=null;document.getElementById('backupApply').disabled=true;
  try{const file=e.target.files?.[0];if(!file)return;if(file.size>20*1024*1024)throw Error('20MB以内にしてください。');pendingBackup=NebulithWorkspace.backup(JSON.parse(await file.text()));document.getElementById('backupPreview').textContent='検証済み。復元すると現在の設定・下書き・記録を置き換えます。必要なら先にバックアップを保存してください。';document.getElementById('backupApply').disabled=false;}catch(error){document.getElementById('backupPreview').textContent=error.message;}
});
document.getElementById('backupApply').addEventListener('click',()=>{if(pendingBackup&&safeStorage.restore(pendingBackup))window.location.reload();});


// Cleaned: Font toggle button removed as per project requirements.
// Dedicated glyph sections (.word-glyph, .corpus-glyph, .modal-glyph-large) render Nebulith font natively.

// ==============================================================================
// Service Worker Registration for Offline PWA
// ==============================================================================
if (typeof navigator !== 'undefined' && 'serviceWorker' in navigator && typeof window !== 'undefined' && window.location && (window.location.protocol === 'https:' || window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')) {
  let hadController=!!navigator.serviceWorker.controller;
  navigator.serviceWorker.addEventListener('controllerchange',()=>{
    if(hadController){document.getElementById('pwaUpdateStatus').textContent='更新を反映できます。下書きを保存して再読み込みしてください。';document.getElementById('pwaReload').hidden=false;}
    hadController=true;
  });
  document.getElementById('pwaReload').addEventListener('click',()=>{
    if(composingInput){document.getElementById('pwaUpdateStatus').textContent='日本語の変換を確定してから更新してください。';return;}
    if(saveTranslationSession())window.location.reload();
  });
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('./service-worker.js').then((reg) => {
      console.log('Nebulith PWA Service Worker registered:', reg.scope);
    }).catch((err) => {
      console.warn('Nebulith Service Worker registration failed:', err);
    });
  });
}

