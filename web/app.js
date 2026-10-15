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

function escapeHtml(str) {
  if (!str) return '';
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
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
  const icon = document.getElementById('themeIcon');
  const label = document.getElementById('themeLabel');
  if (currentTheme === 'dark') {
    icon.textContent = '☀️';
    label.textContent = 'Light';
  } else {
    icon.textContent = '🌙';
    label.textContent = 'Dark';
  }
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

// Tab Navigation
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    btn.classList.add('active');
    const tabId = btn.getAttribute('data-tab');
    document.getElementById('tab-' + tabId).classList.add('active');
  });
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

function renderLexicon() {
  const query = searchInput.value.trim().toLowerCase();
  const rank = w => {
    if (!query) return 0;
    const labels = [w.r, ...(w.m+'、'+w.en).split(/[、／,;]/)].map(s=>s.trim().toLowerCase());
    return labels.includes(query) ? 0 : labels.some(s=>s.startsWith(query)) ? 1 : 2;
  };
  const filtered = VOCAB.filter(w => {
    if (currentFilterPos === 'FAV') {
      if (!favorites.has(w.r)) return false;
    } else if (currentFilterPos === 'HISTORY') {
      if(!browsingHistory.includes(w.r))return false;
    } else if (currentFilterPos !== 'ALL' && !w.p.includes(currentFilterPos)) {
      return false;
    }
    if (!query) return true;
    return (w.r && w.r.toLowerCase().includes(query)) ||
           (w.m && w.m.toLowerCase().includes(query)) ||
           (w.en && w.en.toLowerCase().includes(query)) ||
           (w.n && w.n.toLowerCase().includes(query));
  }).sort((a,b)=>rank(a)-rank(b));

  if (filtered.length === 0 && query) {
    resultCount.textContent = `表示中: 0 語 (一致なし)`;
    const alreadyInQueue = feedbackQueue.some(item => item.type === 'word' && item.text.toLowerCase() === query);
    wordGrid.innerHTML = `
      <div class="empty-state">
        <div style="font-size: 2.2rem;">🔍</div>
        <div style="font-size: 1.1rem; font-weight: 600;">「${escapeHtml(query)}」に一致する単語が見つかりませんでした</div>
        <p style="font-size: 0.85rem; color: var(--md-sys-color-on-surface-variant); max-width: 480px;">
          日本語・英語・星石文字での検索に対応していなかった語彙を内部キューに記録し、今後の辞書アップデートで回収・追加できます。
        </p>
        <button class="record-btn" id="recordMissingWordBtn" ${alreadyInQueue ? 'disabled style="opacity:0.7;"' : ''}>
          <span>${alreadyInQueue ? '✅ キューに記録済み' : '📥 この未対応語を記録する'}</span>
        </button>
      </div>
    `;
    const recBtn = document.getElementById('recordMissingWordBtn');
    if (recBtn && !alreadyInQueue) {
      recBtn.addEventListener('click', () => {
        if(!addFeedbackItem('word', 'search', query, '辞書検索0件ヒット'))return;
        recBtn.innerHTML = '<span>✅ キューに記録しました！</span>';
        recBtn.disabled = true;
        recBtn.style.opacity = '0.7';
      });
    }
    return;
  }

  resultCount.textContent = `表示中: ${filtered.length.toLocaleString()} 語 (全${VOCAB.length.toLocaleString()}語)`;
  if(currentFilterPos==='HISTORY')filtered.sort((a,b)=>browsingHistory.indexOf(a.r)-browsingHistory.indexOf(b.r));
  const displayList = filtered.slice(0, 150);
  wordGrid.innerHTML = displayList.map(w => {
    const isFav = favorites.has(w.r);
    return `
      <div class="word-card" onclick="openWordModal('${w.r}')">
        <button class="card-fav-btn ${isFav ? 'active' : ''}" onclick="toggleFav(event, '${w.r}')">★</button>
        <div>
          <div class="word-card-top">
            <span class="word-roman">${w.r}</span>
            <span class="word-pos">${w.p}</span>
          </div>
          <div class="word-glyph">${w.r}</div>
          <div class="word-meaning">${w.m}</div>
        </div>
        <div>
          ${w.en ? `<div style="font-size: 0.75rem; color: var(--md-sys-color-on-surface-variant); margin-top: 4px;">En: ${w.en}</div>` : ''}
          <div class="word-ipa">${w.i ? `/${w.i}/` : ''}</div>
        </div>
      </div>
    `;
  }).join('');
}

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

window.openWordModal = function(roman) {
  const word = VOCAB.find(w => w.r === roman);
  if (!word) return;
  activeModalWord = word;
  browsingHistory=[roman,...browsingHistory.filter(r=>r!==roman)].slice(0,100);
  safeStorage.setItem('neb_history',JSON.stringify(browsingHistory));
  document.getElementById('modalGlyph').textContent = word.r;
  document.getElementById('modalRoman').textContent = word.r;
  document.getElementById('modalPos').textContent = word.p;
  document.getElementById('modalId').textContent = '#' + word.id;
  document.getElementById('modalMeaningJa').textContent = word.m;
  document.getElementById('modalMeaningEn').textContent = word.en || '—';
  document.getElementById('modalIpa').textContent = word.i ? `/${word.i}/` : '—';
  document.getElementById('modalNotes').textContent = word.n || '基本星石語彙';
  updateModalFavButton();
  wordModal.classList.add('active');
};

function updateModalFavButton() {
  const btn = document.getElementById('modalFavToggle');
  if (activeModalWord && favorites.has(activeModalWord.r)) {
    btn.textContent = '★ お気に入り解除';
    btn.style.color = '#fbbc04';
  } else {
    btn.textContent = '☆ お気に入りに追加';
    btn.style.color = '';
  }
}

document.getElementById('modalFavToggle').addEventListener('click', () => {
  if (activeModalWord) {
    toggleFav({ stopPropagation: () => {} }, activeModalWord.r);
  }
});

document.getElementById('modalCloseBtn').addEventListener('click', () => {
  wordModal.classList.remove('active');
});
wordModal.addEventListener('click', (e) => {
  if (e.target === wordModal) wordModal.classList.remove('active');
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

  // Dynamic fallback rules for English -> Nebulith
  if (fromLang === 'en' && toLang === 'neb') {
    if (norm.includes('like') || norm.includes('love')) {
      if (norm.includes('you')) {
        const neg = norm.includes('not') || norm.includes("don't");
        const res = neg ? 'Ne cynel el mi ia ti.' : 'Cynel el mi ia ti.';
        return {
          neb: res,
          text: res,
          tag: 'VSO (English SVO -> Nebulith VSO)',
          alignment: [
            {"src": "私は", "src_en": "I", "dst": "el mi", "role": "主格 (Subject)"},
            {"src": "あなたを", "src_en": "you", "dst": "ia ti", "role": "対格 (Object)"},
            {"src": neg ? "好まない" : "好きだ", "src_en": neg ? "do not like" : "like / love", "dst": neg ? "Ne cynel" : "Cynel", "role": "述語動詞 (Verb)"}
          ],
          success: true
        };
      }
      if (norm.includes('star')) {
        const beautiful = norm.includes('beautiful');
        const res = beautiful ? 'Cynel el mi ia vyr cylani.' : 'Cynel el mi ia vyr.';
        return {
          neb: res,
          text: res,
          tag: 'VSO + Post-Adj',
          alignment: [
            {"src": "私は", "src_en": "I", "dst": "el mi", "role": "主格 (Subject)"},
            {"src": "星を", "src_en": "stars", "dst": "ia vyr", "role": "対格 (Object)"},
            ...(beautiful ? [{"src": "美しい", "src_en": "beautiful", "dst": "cylani", "role": "後置形容詞 (Post-Adj)"}] : []),
            {"src": "好きだ", "src_en": "like / love", "dst": "Cynel", "role": "述語動詞 (Verb)"}
          ],
          success: true
        };
      }
    }
    if (norm.includes('if') && norm.includes('star') && norm.includes('walk')) {
      return {
        neb: 'Zen falun el vyr, poran el mi.',
        text: 'Zen falun el vyr, poran el mi.',
        tag: 'Zen Clause1, Clause2 (Conditional)',
        alignment: [
          {"src": "星が輝くなら", "src_en": "if stars shine", "dst": "Zen falun el vyr", "role": "条件節 (Condition)"},
          {"src": "私は歩く", "src_en": "I walk", "dst": "poran el mi", "role": "帰結節 (Consequence)"}
        ],
        success: true
      };
    }
    if (norm.includes('more') && norm.includes('beautiful') && norm.includes('than')) {
      return {
        neb: 'Cylani el vyr va valar.',
        text: 'Cylani el vyr va valar.',
        tag: 'Adj el S va O (Ablative Comparison)',
        alignment: [
          {"src": "星は", "src_en": "the star", "dst": "el vyr", "role": "主格 (Subject)"},
          {"src": "夜よりも", "src_en": "than the night", "dst": "va valar", "role": "奪格比較 (Comparison)"},
          {"src": "美しい", "src_en": "is more beautiful", "dst": "Cylani", "role": "形容詞述語 (Predicate)"}
        ],
        success: true
      };
    }
    if (norm.includes('night') && norm.includes('beautiful')) {
      return {
        neb: 'Cylani el valar.',
        text: 'Cylani el valar.',
        tag: 'Adj Predicate',
        alignment: [
          {"src": "夜は", "src_en": "the night", "dst": "el valar", "role": "主格 (Subject)"},
          {"src": "美しい", "src_en": "is beautiful", "dst": "Cylani", "role": "形容詞述語 (Predicate)"}
        ],
        success: true
      };
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
    transNotice.innerHTML = '<span>ℹ️</span> 入力すると即座に文法解析・翻訳されます。';
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
      transNotice.innerHTML = '<span>✨</span> 長文段落・確定照合完了';
      return;
    }
  }

  // Split on punctuation or newlines
  const rawSentences = text.split(/(?<=[。！？!?\n])|(?<=\.\s+)/).map(s => s.trim()).filter(s => s.length > 0);

  const results = [];
  const tags = [];
  const combinedAlignments = [];
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
    transNotice.innerHTML = `<span>✨</span> 長文・構文解析完了 (${results.length}文 確定翻訳)`;
  } else {
    transOutputText.textContent = results.join(' ');
    transOutputGlyph.textContent = '';
    transTagsList.innerHTML = tags.map(t => `<span class="trans-structure-tag">${t}</span>`).join('');
    if (transAlignmentBox) transAlignmentBox.innerHTML = '';
    
    // Show Missing Box for unhandled sentences
    if (transMissingBox) {
      transMissingBox.style.display = 'flex';
      const already = feedbackQueue.some(i => i.type === 'sentence' && i.text.toLowerCase() === text.toLowerCase());
      if (recordMissingTransBtn) {
        recordMissingTransBtn.innerHTML = already ? '<span>✅ キューに記録済み</span>' : '<span>📥 未対応文章として記録する</span>';
        recordMissingTransBtn.disabled = already;
        recordMissingTransBtn.style.opacity = already ? '0.7' : '1';
        recordMissingTransBtn.onclick = () => {
          if(!addFeedbackItem('sentence', srcLang, text, '未確定構文・未対応文章'))return;
          recordMissingTransBtn.innerHTML = '<span>✅ キューに記録しました！</span>';
          recordMissingTransBtn.disabled = true;
          recordMissingTransBtn.style.opacity = '0.7';
        };
      }
    }
    transNotice.innerHTML = '<span>⚠️</span> 一部の文章が現在登録・検証済みの文型外です。下のボタンから未対応キューに記録できます。';
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
    return `
      <div class="align-chip">
        <span class="align-src">${escapeHtml(srcWord)}</span>
        <span class="align-arrow">➔</span>
        <span class="align-dst">${escapeHtml(a.dst)}</span>
        <span class="align-role">${escapeHtml(a.role)}</span>
      </div>
    `;
  }).join('');

  transAlignmentBox.innerHTML = `
    <div class="align-header">🔗 原文とNebulithの語句対応</div>
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
  document.getElementById('inputChoices').style.display=text.trim()&&(!result.complete||result.segments.length>1)?'flex':'none';
  document.getElementById('inputSentenceLabel').style.display=result.segments.length>1?'inline-block':'none';
  document.getElementById('inputSentence').innerHTML=result.segments.map((s,i)=>`<option value="${escapeHtml(s.key)}">${i+1}文目・${labels[s.state]}：${escapeHtml(s.source.slice(0,55))}</option>`).join('');
  document.getElementById('inputSentence').value=activeSentenceKey;
  document.getElementById('inputPossessionLabel').style.display=selected?.scopeAmbiguous?'inline-block':'none';
  const senseOptions=selected?.senseOptions||[];
  document.getElementById('inputSenseLabel').style.display=senseOptions.length?'inline-block':'none';
  document.getElementById('inputSense').innerHTML='<option value="">未選択</option>'+senseOptions.map(o=>`<option value="${escapeHtml(o.value)}">${escapeHtml(o.root+'：'+o.meaning)}</option>`).join('');
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
    const sources=(transInput.value.match(/[^。！？!?\n]+[。！？!?]*/g)||[]).map(s=>s.trim()).filter(Boolean);
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
    const typeLabel = item.type === 'word' ? '📖 単語検索' : '🔄 文章翻訳';
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
        <button class="tool-btn" style="color: var(--md-sys-color-error); padding: 4px 8px;" onclick="deleteQueueItem('${item.id}')">✕</button>
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
      <div class="corpus-ja">🇯🇵 ${escapeHtml(c.ja)}</div>
      ${c.en?`<div class="corpus-en">🇬🇧 ${escapeHtml(c.en)}</div>`:''}
      ${c.lit?`<div class="corpus-lit">${escapeHtml(c.lit)}</div>`:''}
    </div>`).join(''):'<p>一致する例文がありません。</p>';
}
corpusSearch.addEventListener('input',renderCorpus);
renderCorpus();

// Initial Render
renderLexicon();

function saveTranslationSession(){
  safeStorage.setItem('neb_session_v1',JSON.stringify({schemaVersion:1,text:transInput.value,srcLang,dstLang,choices:inputChoicesState,updatedAt:new Date().toISOString()}));
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
const splitSlider=document.getElementById('splitWidth');
function applySplit(value){document.documentElement.style.setProperty('--translation-columns',value+'fr '+(100-value)+'fr');document.getElementById('splitWidthValue').textContent=value+'%';}
const savedSplit=Number(safeStorage.getItem('neb_split')||50);splitSlider.value=String(savedSplit>=25&&savedSplit<=75?savedSplit:50);applySplit(Number(splitSlider.value));
splitSlider.addEventListener('input',e=>{const value=Number(e.target.value);if(value>=25&&value<=75){applySplit(value);safeStorage.setItem('neb_split',String(value));}});
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
  const snapshot=safeStorage.snapshot();snapshot.values={...snapshot.values,neb_font_size:String(fontSizeSlider.value),neb_split:String(splitSlider.value),neb_theme:currentTheme,neb_favorites:JSON.stringify([...favorites]),neb_history:JSON.stringify(browsingHistory),neb_feedback_queue:JSON.stringify(feedbackQueue),neb_editor_draft:editorInput.value,neb_session_v1:JSON.stringify({schemaVersion:1,text:transInput.value,srcLang,dstLang,choices:inputChoicesState})};
  downloadJson(snapshot,'nebulith-backup-'+Date.now()+'.json');
});
document.getElementById('backupImport').addEventListener('change',async e=>{
  pendingBackup=null;document.getElementById('backupApply').disabled=true;
  try{const file=e.target.files?.[0];if(!file)return;if(file.size>20*1024*1024)throw Error('20MB以内にしてください。');pendingBackup=NebulithWorkspace.backup(JSON.parse(await file.text()));document.getElementById('backupPreview').textContent='検証済み。復元すると現在の設定・下書き・記録を置き換えます。必要なら先にバックアップを保存してください。';document.getElementById('backupApply').disabled=false;}catch(error){document.getElementById('backupPreview').textContent=error.message;}
});
document.getElementById('backupApply').addEventListener('click',()=>{if(pendingBackup&&safeStorage.restore(pendingBackup))window.location.reload();});
