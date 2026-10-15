// Nebulith Studio Web - Complete Application Logic (v2.6)

// State & LocalStorage
let currentTheme = localStorage.getItem('neb_theme') || 'dark';
let currentFilterPos = 'ALL';
let srcLang = 'ja'; // 'ja' | 'en' | 'neb'
let dstLang = 'neb'; // 'neb' | 'ja' | 'en'
let favorites = new Set(JSON.parse(localStorage.getItem('neb_favorites') || '[]'));
let activeModalWord = null;

// Initialize Theme
document.documentElement.setAttribute('data-theme', currentTheme);
updateThemeUI();

document.getElementById('themeToggleBtn').addEventListener('click', () => {
  currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', currentTheme);
  localStorage.setItem('neb_theme', currentTheme);
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
  const filtered = VOCAB.filter(w => {
    if (currentFilterPos === 'FAV') {
      if (!favorites.has(w.r)) return false;
    } else if (currentFilterPos !== 'ALL' && !w.p.includes(currentFilterPos)) {
      return false;
    }
    if (!query) return true;
    return (w.r && w.r.toLowerCase().includes(query)) ||
           (w.m && w.m.toLowerCase().includes(query)) ||
           (w.en && w.en.toLowerCase().includes(query));
  });

  resultCount.textContent = `表示中: ${filtered.length.toLocaleString()} 語 (全${VOCAB.length.toLocaleString()}語)`;
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
  localStorage.setItem('neb_favorites', JSON.stringify([...favorites]));
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

const transInput = document.getElementById('transInput');
const transOutputText = document.getElementById('transOutputText');
const transOutputGlyph = document.getElementById('transOutputGlyph');
const transTagsList = document.getElementById('transTagsList');
const transAlignmentBox = document.getElementById('transAlignmentBox');
const transNotice = document.getElementById('transNotice');
const swapTransBtn = document.getElementById('swapTransBtn');
const srcLangSelect = document.getElementById('srcLangSelect');
const dstLangSelect = document.getElementById('dstLangSelect');
const sampleSelect = document.getElementById('sampleSelect');
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
  const text = transInput.value.trim();
  if (!text) {
    transOutputText.textContent = 'ここに訳文が表示されます';
    transOutputGlyph.textContent = '';
    transTagsList.innerHTML = '';
    if (transAlignmentBox) transAlignmentBox.innerHTML = '';
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
    const outJoined = results.join(' ');
    transOutputText.textContent = outJoined;
    transOutputGlyph.textContent = dstLang === 'neb' ? outJoined : '';
    transTagsList.innerHTML = tags.map(t => `<span class="trans-structure-tag">${t}</span>`).join('');
    renderAlignments(combinedAlignments);
    transNotice.innerHTML = `<span>✨</span> 長文・構文解析完了 (${results.length}文 確定翻訳)`;
  } else {
    transOutputText.textContent = results.join(' ');
    transOutputGlyph.textContent = '';
    transTagsList.innerHTML = tags.map(t => `<span class="trans-structure-tag">${t}</span>`).join('');
    if (transAlignmentBox) transAlignmentBox.innerHTML = '';
    transNotice.innerHTML = '<span>⚠️</span> 一部の文章が現在登録・検証済みの文型外です。';
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
        <span class="align-src">${srcWord}</span>
        <span class="align-arrow">➔</span>
        <span class="align-dst">${a.dst}</span>
        <span class="align-role">${a.role}</span>
      </div>
    `;
  }).join('');

  transAlignmentBox.innerHTML = `
    <div class="align-header">🔗 単語・構文アライメント (Word Alignment)</div>
    <div class="align-list">${chipsHtml}</div>
  `;
}

let transTimer = null;
transInput.addEventListener('input', () => {
  clearTimeout(transTimer);
  transTimer = setTimeout(doTranslate, 120);
});

srcLangSelect.addEventListener('change', () => {
  srcLang = srcLangSelect.value;
  doTranslate();
});

dstLangSelect.addEventListener('change', () => {
  dstLang = dstLangSelect.value;
  doTranslate();
});

sampleSelect.addEventListener('change', (e) => {
  if (e.target.value) {
    const val = e.target.value;
    transInput.value = val;
    // Auto-detect language of sample
    if (/^[A-Za-z\s,.'!?]+$/.test(val)) {
      srcLang = 'en';
      dstLang = 'neb';
      srcLangSelect.value = 'en';
      dstLangSelect.value = 'neb';
    } else {
      srcLang = 'ja';
      dstLang = 'neb';
      srcLangSelect.value = 'ja';
      dstLangSelect.value = 'neb';
    }
    doTranslate();
  }
});

swapTransBtn.addEventListener('click', () => {
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
  transInput.value = '';
  sampleSelect.value = '';
  doTranslate();
});

copyDstBtn.addEventListener('click', () => {
  navigator.clipboard.writeText(transOutputText.textContent).then(() => {
    alert('訳文をクリップボードにコピーしました！');
  });
});

// Editor Features
const editorInput = document.getElementById('editorInput');
const editorPreview = document.getElementById('editorPreview');
const editorStats = document.getElementById('editorStats');
const fontSizeSlider = document.getElementById('fontSizeSlider');
const fontSizeVal = document.getElementById('fontSizeVal');

const savedDraft = localStorage.getItem('neb_editor_draft') || '';
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
  fontSizeVal.textContent = size;
  editorPreview.style.fontSize = size;
});

editorInput.addEventListener('input', (e) => {
  const val = e.target.value;
  editorPreview.textContent = val || 'Cynel el mi ia ti. Zen falun el vyr, cylani el valar.';
  updateEditorStats();
  localStorage.setItem('neb_editor_draft', val);
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
  localStorage.removeItem('neb_editor_draft');
});

// Corpus Cards Rendering (3 Languages: Nebulith / Japanese / English)
const corpusList = document.getElementById('corpusList');
const allSentences = EXT_SENTENCES.map(s => ({
  id: s.id,
  neb: s.nebulith,
  ja: s.japanese,
  en: s.english || '',
  lit: s.structure ? `構造: ${s.structure}` : '',
  badge: '★ 拡張構文 v2.6'
})).concat(CANON.map(c => ({
  id: c.id,
  neb: c.neb,
  ja: c.ja,
  en: c.lit || '',
  lit: c.lit ? `英語/逐語: ${c.lit}` : '',
  badge: '公式正本コーパス'
})));

corpusList.innerHTML = allSentences.map(c => `
  <div class="corpus-card">
    <div class="corpus-badge">${c.badge} [#${c.id}]</div>
    <div class="corpus-glyph">${c.neb}</div>
    <div class="corpus-neb">${c.neb}</div>
    <div class="corpus-ja">🇯🇵 ${c.ja}</div>
    ${c.en ? `<div class="corpus-en" style="font-size: 0.9rem; color: var(--md-sys-color-primary); margin-top: 3px;">🇬🇧 ${c.en}</div>` : ''}
    ${c.lit ? `<div class="corpus-lit">${c.lit}</div>` : ''}
  </div>
`).join('');

// Initial Render
renderLexicon();
