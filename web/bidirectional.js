// Nebulith Bidirectional Translation Engine (v1.0)
// Supports:
//  - Nebulith (VSO) -> Japanese (SOV)
//  - Nebulith (VSO) -> English (SVO)
//  - English (SVO)  -> Nebulith (VSO)
//  - Japanese (SOV) -> Nebulith (VSO) fallback integration

(function (root, factory) {
  if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.NebulithBidirectionalEngine = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  // Standard case markers
  const CASE_MARKERS = {
    el: { roleJa: '主格 (は・が)', roleEn: 'Subject', prepEn: '' },
    ia: { roleJa: '対格 (を)', roleEn: 'Direct Object', prepEn: '' },
    uo: { roleJa: '処格 (で・において)', roleEn: 'Locative', prepEn: 'in / at' },
    de: { roleJa: '具格 (で・により)', roleEn: 'Instrumental', prepEn: 'with / by' },
    va: { roleJa: '比較・奪格 (より・から)', roleEn: 'Ablative / Comparison', prepEn: 'than / from' },
    en: { roleJa: '属格 (の)', roleEn: 'Genitive', prepEn: 'of' }
  };

  // Verb / Aspect affixes
  const TENSE_PREFIXES = {
    fe: { ja: '〜した (過去)', en: 'did / -ed' },
    di: { ja: '〜している (進行)', en: 'is ...-ing' },
    se: { ja: '〜だろう (推量)', en: 'will / would' },
    ne: { ja: '〜ない (否定)', en: 'do not / not' }
  };

  const ASPECT_SUFFIXES = [
    { suffix: 'far', ja: '〜し終えた (完了)', en: 'have ...-en / finished' },
    { suffix: 'liv', ja: '〜し続けている (継続維持)', en: 'keep ...-ing' },
    { suffix: 'ast', ja: '〜したい (希望)', en: 'want to ...' },
    { suffix: 'ar', ja: '〜できる (可能)', en: 'can ...' },
    { suffix: 'cor', ja: '何度も〜する (反復)', en: 'repeatedly ...' },
    { suffix: 'iin', ja: 'たち (複数)', en: '-s / plural' }
  ];

  function getVocabMap() {
    if (typeof VOCAB !== 'undefined' && Array.isArray(VOCAB)) {
      const map = new Map();
      for (const w of VOCAB) {
        if (w.r) map.set(w.r.toLowerCase(), w);
      }
      return map;
    }
    return new Map();
  }

  const BUILTIN_VOCAB = {
    mi: { m: '私', en: 'I / me' },
    ti: { m: 'あなた', en: 'you' },
    solan: { m: '私たち', en: 'we / us' },
    valin: { m: '彼ら', en: 'they / them' },
    vyr: { m: '星', en: 'star' },
    valar: { m: '夜', en: 'night' },
    zohar: { m: '太陽', en: 'sun' },
    daris: { m: '水', en: 'water' },
    fal: { m: '光', en: 'light' },
    cynel: { m: '愛する・好む', en: 'like / love' },
    poran: { m: '歩く・旅する', en: 'walk / travel' },
    falun: { m: '輝く・光る', en: 'shine / gleam' },
    vyrel: { m: '観測する・見る', en: 'observe / see' },
    seron: { m: '憩う・休む', en: 'rest / repose' },
    cylani: { m: '美しい', en: 'beautiful' },
    surani: { m: '温かい', en: 'warm' },
    valani: { m: '暗い', en: 'dark' }
  };

  function lookupWord(token) {
    const clean = token.toLowerCase().replace(/^[^\w]+|[^\w]+$/g, '');
    const vocab = getVocabMap();
    if (vocab.has(clean)) return vocab.get(clean);
    if (BUILTIN_VOCAB[clean]) return { r: clean, ...BUILTIN_VOCAB[clean] };

    // Try stripping suffixes
    for (const asp of ASPECT_SUFFIXES) {
      if (clean.length > asp.suffix.length + 3 && clean.endsWith(asp.suffix)) {
        const root = clean.slice(0, -asp.suffix.length);
        if (vocab.has(root)) {
          const base = vocab.get(root);
          return { ...base, strippedSuffix: asp };
        }
      }
    }
    return null;
  }

  // Parse a single Nebulith clause (VSO structure)
  function parseNebulithClause(clauseStr) {
    const tokens = clauseStr.trim().split(/\s+/).filter(Boolean);
    if (!tokens.length) return null;

    let idx = 0;
    let isNeg = false;
    let tensePrefix = null;

    // Check pre-verbal particles
    while (idx < tokens.length) {
      const low = tokens[idx].toLowerCase();
      if (low === 'ne') {
        isNeg = true;
        idx++;
      } else if (low === 'fe' || low === 'di' || low === 'se') {
        tensePrefix = low;
        idx++;
      } else {
        break;
      }
    }

    if (idx >= tokens.length) return null;

    // Verb / Predicate token
    const verbToken = tokens[idx++];
    const verbClean = verbToken.toLowerCase().replace(/[.,!?;:]/g, '');
    let verbInfo = lookupWord(verbClean);
    let aspectSuffix = null;

    if (verbInfo && verbInfo.strippedSuffix) {
      aspectSuffix = verbInfo.strippedSuffix;
    } else {
      for (const asp of ASPECT_SUFFIXES) {
        if (verbClean.length > asp.suffix.length + 3 && verbClean.endsWith(asp.suffix)) {
          aspectSuffix = asp;
          break;
        }
      }
    }

    // Parse Case Phrases: el S, ia O, uo Loc, de Inst, va Comp, en Gen
    const phrases = [];
    let currentMarker = null;
    let currentTokens = [];

    while (idx < tokens.length) {
      const tok = tokens[idx];
      const low = tok.toLowerCase().replace(/[.,!?;:]/g, '');
      if (CASE_MARKERS[low]) {
        if (currentMarker) {
          phrases.push({ marker: currentMarker, words: [...currentTokens] });
        }
        currentMarker = low;
        currentTokens = [];
      } else {
        if (currentMarker) {
          currentTokens.push(tok);
        } else {
          // Unmarked initial or modifier
          currentTokens.push(tok);
        }
      }
      idx++;
    }
    if (currentMarker && currentTokens.length) {
      phrases.push({ marker: currentMarker, words: currentTokens });
    }

    return {
      isNeg,
      tensePrefix,
      aspectSuffix,
      verbToken,
      verbInfo,
      phrases
    };
  }

  // Full Nebulith -> Target Language (Japanese / English)
  function translateNebulith(text, targetLang = 'ja') {
    if (!text || !text.trim()) {
      return { text: '', alignments: [], success: false };
    }

    const sentences = text.split(/(?<=[.!?])\s+/).filter(Boolean);
    const translatedSentences = [];
    const allAlignments = [];

    for (const sent of sentences) {
      const clean = sent.trim().replace(/[.!?]+$/, '');
      const punct = sent.trim().slice(clean.length) || (targetLang === 'ja' ? '。' : '.');

      // Check conditional Zen
      if (clean.startsWith('Zen ') || clean.startsWith('zen ')) {
        const parts = clean.slice(4).split(/,\s*/);
        if (parts.length >= 2) {
          const condRes = translateSingleClause(parts[0], targetLang, true);
          const consRes = translateSingleClause(parts.slice(1).join(', '), targetLang, false);
          if (condRes.success && consRes.success) {
            let combined = '';
            if (targetLang === 'ja') {
              combined = `${condRes.text}なら、${consRes.text}${punct === '.' ? '。' : punct}`;
            } else {
              combined = `If ${condRes.text}, ${consRes.text}${punct === '。' ? '.' : punct}`;
            }
            translatedSentences.push(combined);
            allAlignments.push(...condRes.alignments, ...consRes.alignments);
            continue;
          }
        }
      }

      const res = translateSingleClause(clean, targetLang, false);
      if (res.success) {
        translatedSentences.push(res.text + punct);
        allAlignments.push(...res.alignments);
      } else {
        return { text: null, error: `未対応構文: ${sent}`, success: false };
      }
    }

    return {
      text: translatedSentences.join(' '),
      alignments: allAlignments,
      success: true
    };
  }

  // Helper: Translate a single VSO clause
  function translateSingleClause(clauseStr, targetLang, isCondition = false) {
    const parsed = parseNebulithClause(clauseStr);
    if (!parsed) return { text: '', alignments: [], success: false };

    const alignments = [];
    const isJa = targetLang === 'ja';

    // 1. Resolve Verb / Predicate
    const verbClean = parsed.verbToken.toLowerCase().replace(/[.,!?;:]/g, '');
    const vInfo = parsed.verbInfo || lookupWord(verbClean);
    let vJa = vInfo ? (vInfo.m || vInfo.meaningJa || verbClean).split(/[、／/]/)[0].trim() : verbClean;
    let vEn = vInfo ? (vInfo.en || vInfo.meaningEn || verbClean).split(/[,;/]/)[0].trim() : verbClean;

    // Apply suffixes
    if (parsed.aspectSuffix) {
      if (isJa) {
        if (parsed.aspectSuffix.suffix === 'ast') vJa = vJa.replace(/る$/, 'たい').replace(/す$/, 'したい') + (vJa.endsWith('たい') ? '' : 'たい');
        else if (parsed.aspectSuffix.suffix === 'ar') vJa = vJa.replace(/る$/, 'られる') + (vJa.endsWith('れる') ? '' : 'できる');
        else if (parsed.aspectSuffix.suffix === 'far') vJa = vJa.replace(/る$/, 'し終えた') + (vJa.endsWith('終えた') ? '' : 'し終えた');
        else if (parsed.aspectSuffix.suffix === 'liv') vJa = vJa.replace(/る$/, 'し続けている') + (vJa.endsWith('続けている') ? '' : 'し続けている');
      } else {
        if (parsed.aspectSuffix.suffix === 'ast') vEn = `want to ${vEn}`;
        else if (parsed.aspectSuffix.suffix === 'ar') vEn = `can ${vEn}`;
        else if (parsed.aspectSuffix.suffix === 'far') vEn = `have finished ${vEn}-ing`;
        else if (parsed.aspectSuffix.suffix === 'liv') vEn = `keep ${vEn}-ing`;
      }
    }

    if (parsed.isNeg) {
      if (isJa) vJa = vJa.replace(/る$/, 'ない').replace(/す$/, 'さない') + (vJa.endsWith('ない') ? '' : 'ない');
      else vEn = `do not ${vEn}`;
    }

    if (parsed.tensePrefix === 'fe') {
      if (isJa) vJa = vJa.replace(/る$/, 'た').replace(/す$/, 'した') + (vJa.endsWith('た') ? '' : 'た');
      else vEn = vEn.endsWith('e') ? `${vEn}d` : `${vEn}ed`;
    } else if (parsed.tensePrefix === 'di') {
      if (isJa) vJa = vJa.replace(/る$/, 'ている') + (vJa.endsWith('ている') ? '' : 'ている');
      else vEn = `is ${vEn}-ing`;
    }

    // 2. Resolve Phrases
    let subjJa = '', subjEn = '', objJa = '', objEn = '', compJa = '', compEn = '', locJa = '', locEn = '', instJa = '', instEn = '';

    for (const ph of parsed.phrases) {
      const phraseText = ph.words.join(' ');
      const mainWord = ph.words[0].toLowerCase().replace(/[.,!?;:]/g, '');
      const postAdjWord = ph.words.length > 1 ? ph.words[1].toLowerCase().replace(/[.,!?;:]/g, '') : null;

      const wInfo = lookupWord(mainWord);
      let pJa = wInfo ? (wInfo.m || wInfo.meaningJa || mainWord).split(/[、／/]/)[0].trim() : mainWord;
      let pEn = wInfo ? (wInfo.en || wInfo.meaningEn || mainWord).split(/[,;/]/)[0].trim() : mainWord;

      if (postAdjWord) {
        const adjInfo = lookupWord(postAdjWord);
        if (adjInfo) {
          const adjJa = (adjInfo.m || adjInfo.meaningJa).split(/[、／/]/)[0].trim();
          const adjEn = (adjInfo.en || adjInfo.meaningEn).split(/[,;/]/)[0].trim();
          pJa = `${adjJa}${pJa}`;
          pEn = `${adjEn} ${pEn}`;
        }
      }

      const roleObj = CASE_MARKERS[ph.marker];
      const roleLabel = roleObj ? (isJa ? roleObj.roleJa : roleObj.roleEn) : '修飾句';

      alignments.push({
        src: phraseText,
        src_en: phraseText,
        dst: isJa ? pJa : pEn,
        role: roleLabel
      });

      if (ph.marker === 'el') {
        subjJa = `${pJa}は`;
        subjEn = pEn;
      } else if (ph.marker === 'ia') {
        objJa = `${pJa}を`;
        objEn = pEn;
      } else if (ph.marker === 'va') {
        compJa = `${pJa}より`;
        compEn = `than ${pEn}`;
      } else if (ph.marker === 'uo') {
        locJa = `${pJa}で`;
        locEn = `in ${pEn}`;
      } else if (ph.marker === 'de') {
        instJa = `${pJa}によって`;
        instEn = `with ${pEn}`;
      }
    }

    // Add predicate alignment
    alignments.push({
      src: parsed.verbToken,
      src_en: parsed.verbToken,
      dst: isJa ? vJa : vEn,
      role: isJa ? '述語 (動詞/形容詞)' : 'Predicate Verb'
    });

    let clauseOut = '';
    if (isJa) {
      // Natural Japanese SOV order: S + Comp + Loc + Inst + O + V
      const parts = [subjJa, compJa, locJa, instJa, objJa, vJa].filter(Boolean);
      clauseOut = parts.join(' ');
    } else {
      // Natural English SVO order: S + V + O + Loc + Inst + Comp
      const parts = [subjEn, vEn, objEn, locEn, instEn, compEn].filter(Boolean);
      clauseOut = parts.join(' ');
    }

    return {
      text: clauseOut,
      alignments,
      success: true
    };
  }

  // English -> Nebulith Translation (SVO -> VSO)
  function translateEnglishToNebulith(englishText) {
    if (!englishText || !englishText.trim()) {
      return { text: '', alignments: [], success: false };
    }

    const norm = englishText.trim().toLowerCase();
    const vocab = getVocabMap();

    // 1. Conditionals: if ... , ...
    if (norm.startsWith('if ')) {
      const parts = englishText.slice(3).split(/,\s*/);
      if (parts.length >= 2) {
        const c1 = translateSingleEnglishClause(parts[0]);
        const c2 = translateSingleEnglishClause(parts.slice(1).join(', '));
        if (c1.success && c2.success) {
          const res = `Zen ${c1.text}, ${c2.text}.`;
          return {
            text: res,
            neb: res,
            tag: 'Zen Clause1, Clause2 (Conditional SVO -> VSO)',
            alignment: [...c1.alignments, ...c2.alignments],
            success: true
          };
        }
      }
    }

    // 2. Single English Clause
    const single = translateSingleEnglishClause(englishText);
    if (single.success) {
      const res = single.text.endsWith('.') ? single.text : `${single.text}.`;
      return {
        text: res,
        neb: res,
        tag: single.tag || 'English SVO -> Nebulith VSO',
        alignment: single.alignments,
        success: true
      };
    }

    return { text: null, error: `未対応の英語構文: ${englishText}`, success: false };
  }

  function translateSingleEnglishClause(clause) {
    const norm = clause.trim().replace(/[.,!?]+$/, '').toLowerCase();
    const tokens = norm.split(/\s+/);
    if (!tokens.length) return { success: false };

    // Pronouns & Noun mappings
    const pronounMap = {
      i: 'mi', me: 'mi', my: 'mi',
      you: 'ti', your: 'ti',
      we: 'solan', us: 'solan', our: 'solan',
      they: 'valin', them: 'valin',
      star: 'vyr', stars: 'vyr',
      night: 'valar',
      sun: 'zohar',
      water: 'daris',
      light: 'fal'
    };

    const verbMap = {
      like: 'cynel', likes: 'cynel', love: 'cynel', loved: 'fe cynel',
      walk: 'poran', walks: 'poran', walked: 'fe poran',
      shine: 'falun', shines: 'falun', shone: 'fe falun',
      see: 'vyrel', sees: 'vyrel', saw: 'fe vyrel',
      rest: 'seron', rests: 'seron',
      know: 'belan', knows: 'belan'
    };

    const adjMap = {
      beautiful: 'cylani',
      bright: 'falani',
      dark: 'valani',
      warm: 'surani'
    };

    let isNeg = norm.includes('not') || norm.includes("don't") || norm.includes("doesn't") || norm.includes("didn't");
    let isPast = norm.includes('did ') || norm.includes('was ') || norm.includes('were ') || tokens.some(t => t.endsWith('ed'));

    // Comparison: S is more Adj than O
    if (norm.includes('more') && norm.includes('than')) {
      const m = norm.match(/(?:the\s+)?(\w+)\s+(?:is|are)\s+more\s+(\w+)\s+than\s+(?:the\s+)?(\w+)/);
      if (m) {
        const sWord = pronounMap[m[1]] || m[1];
        const adjWord = adjMap[m[2]] || m[2];
        const oWord = pronounMap[m[3]] || m[3];
        const capAdj = adjWord.charAt(0).toUpperCase() + adjWord.slice(1);
        const res = `${capAdj} el ${sWord} va ${oWord}`;
        return {
          text: res,
          tag: 'Adj el S va O (Comparative)',
          alignments: [
            { src: m[1], src_en: m[1], dst: `el ${sWord}`, role: '比較主格 (Subject)' },
            { src: m[2], src_en: m[2], dst: capAdj, role: '形容詞述語 (Predicate)' },
            { src: m[3], src_en: m[3], dst: `va ${oWord}`, role: '奪格比較 (Comparison)' }
          ],
          success: true
        };
      }
    }

    // Predicate Adjective: S is Adj (e.g. "The night is beautiful")
    if (norm.includes('is ') || norm.includes('are ')) {
      const m = norm.match(/(?:the\s+)?(\w+)\s+(?:is|are)\s+(\w+)/);
      if (m && adjMap[m[2]]) {
        const sWord = pronounMap[m[1]] || m[1];
        const adjWord = adjMap[m[2]];
        const capAdj = adjWord.charAt(0).toUpperCase() + adjWord.slice(1);
        const res = `${capAdj} el ${sWord}`;
        return {
          text: res,
          tag: 'Adj el S (Adjective Predicate)',
          alignments: [
            { src: m[1], src_en: m[1], dst: `el ${sWord}`, role: '主格 (Subject)' },
            { src: m[2], src_en: m[2], dst: capAdj, role: '形容詞述語 (Predicate)' }
          ],
          success: true
        };
      }
    }

    // Transitive / Intransitive SVO
    // Find subject
    let subj = 'mi';
    let subjSrc = 'I';
    if (tokens[0] in pronounMap) {
      subj = pronounMap[tokens[0]];
      subjSrc = tokens[0];
    } else if (tokens[0] === 'the' && tokens[1] in pronounMap) {
      subj = pronounMap[tokens[1]];
      subjSrc = `${tokens[0]} ${tokens[1]}`;
    }

    // Find verb
    let verb = null;
    let verbSrc = null;
    for (const t of tokens) {
      if (verbMap[t]) {
        verb = verbMap[t];
        verbSrc = t;
        break;
      }
    }

    if (!verb) return { success: false };

    // Find object
    let obj = null;
    let objSrc = null;
    let postAdj = null;
    let postAdjSrc = null;

    const remaining = tokens.slice(tokens.indexOf(verbSrc) + 1).filter(t => !['the', 'a', 'an'].includes(t));
    for (const r of remaining) {
      if (adjMap[r]) {
        postAdj = adjMap[r];
        postAdjSrc = r;
      } else if (pronounMap[r]) {
        obj = pronounMap[r];
        objSrc = r;
      }
    }

    let verbForm = verb;
    if (isNeg && !verbForm.startsWith('ne ')) verbForm = `ne ${verbForm}`;
    if (isPast && !verbForm.startsWith('fe ')) verbForm = `fe ${verbForm}`;
    const capVerb = verbForm.charAt(0).toUpperCase() + verbForm.slice(1);

    let res = `${capVerb} el ${subj}`;
    const alignments = [
      { src: subjSrc, src_en: subjSrc, dst: `el ${subj}`, role: '主格 (Subject)' },
      { src: verbSrc, src_en: verbSrc, dst: capVerb, role: '述語動詞 (Verb)' }
    ];

    if (obj) {
      res += ` ia ${obj}`;
      if (postAdj) {
        res += ` ${postAdj}`;
        alignments.push({ src: `${postAdjSrc} ${objSrc}`, src_en: `${postAdjSrc} ${objSrc}`, dst: `ia ${obj} ${postAdj}`, role: '対格・後置修飾 (Object + Adj)' });
      } else {
        alignments.push({ src: objSrc, src_en: objSrc, dst: `ia ${obj}`, role: '対格 (Object)' });
      }
    }

    return {
      text: res,
      tag: 'VSO (English SVO -> Nebulith VSO)',
      alignments,
      success: true
    };
  }

  return {
    parseNebulithClause,
    translateNebulith,
    translateEnglishToNebulith
  };
}));
