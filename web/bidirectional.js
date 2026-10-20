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
    to: { roleJa: '向格 (へ・に)', roleEn: 'Allative', prepEn: 'to' },
    al: { roleJa: '与格 (に・へ)', roleEn: 'Dative', prepEn: 'for / to' },
    ku: { roleJa: '共格 (と・と共に)', roleEn: 'Comitative', prepEn: 'with' },
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

  let _externalVocab = null;
  let _externalVerifiedCompounds = null;

  function configure(vocab, verifiedCompounds) {
    _externalVocab = vocab;
    _externalVerifiedCompounds = verifiedCompounds;
  }

  function getVocabMap() {
    const map = new Map();
    const vocabList = _externalVocab || (typeof VOCAB !== 'undefined' ? VOCAB : (typeof globalThis !== 'undefined' ? globalThis.VOCAB : null));
    if (Array.isArray(vocabList)) {
      for (const w of vocabList) {
        if (w.r) map.set(w.r.toLowerCase(), w);
      }
    }
    const compObj = _externalVerifiedCompounds || (typeof VERIFIED_CANONICAL_COMPOUNDS !== 'undefined' ? VERIFIED_CANONICAL_COMPOUNDS : (typeof globalThis !== 'undefined' ? globalThis.VERIFIED_CANONICAL_COMPOUNDS : null));
    if (compObj && Array.isArray(compObj.entries)) {
      for (const c of compObj.entries) {
        if (c.nrs && !map.has(c.nrs.toLowerCase())) {
          map.set(c.nrs.toLowerCase(), {
            id: c.id,
            r: c.nrs,
            p: c.pos,
            m: c.meaningJa,
            en: c.meaningEn,
            et: c.etymology,
            morphemes: c.morphemes,
            o: 'verified_compound'
          });
        }
      }
    }
    return map;
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

    // Check sentence-level question marker: trailing 'ro', 'ro?', or '?'
    let isQuestion = clauseStr.trim().endsWith('?');
    const rawTokens = tokens.slice(idx);
    if (rawTokens.length > 0) {
      const lastTok = rawTokens[rawTokens.length - 1].toLowerCase().replace(/[.,!?;:]/g, '');
      if (lastTok === 'ro') {
        isQuestion = true;
      }
    }

    // Parse Case Phrases: el S, ia O, uo Loc, de Inst, va Comp, en Gen
    const phrases = [];
    let currentMarker = null;
    let currentTokens = [];

    while (idx < tokens.length) {
      const tok = tokens[idx];
      const low = tok.toLowerCase().replace(/[.,!?;:]/g, '');
      if (low === 'ro') {
        // standalone question particle; stop parsing case phrase
        isQuestion = true;
        idx++;
        continue;
      }
      // If currentMarker is 'en' and it introduced a clause (starts with a verb),
      // keep accumulating all internal tokens until sentence ends.
      const isInsideRelativeClause = currentMarker === 'en' && currentTokens.length > 0 && (() => {
        const firstW = currentTokens[0].toLowerCase().replace(/[.,!?;:]/g, '');
        const info = lookupWord(firstW);
        return info && (info.p === '動' || info.pos === '動' || info.pos === '動詞');
      })();

      if (CASE_MARKERS[low] && !isInsideRelativeClause) {
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
      isQuestion,
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

      // Check compound & coordinating conjunctions: Zen / Sen / Tor / Hav / Den / Sol
      const conjMatch = clean.match(/^(Zen|Sen|Tor|Hav|Den|Sol)\s+(.+)$/i);
      if (conjMatch) {
        const conjKey = conjMatch[1].toLowerCase();
        const parts = conjMatch[2].split(/,\s*/);
        if (parts.length >= 2) {
          const condRes = translateSingleClause(parts[0], targetLang, true);
          const consRes = translateSingleClause(parts.slice(1).join(', '), targetLang, false);
          if (condRes.success && consRes.success) {
            const conjMap = {
              zen: { ja: 'なら、', en: 'If ' },
              sen: { ja: 'ので、', en: 'Because ' },
              tor: { ja: 'けれど、', en: 'Although ' },
              hav: { ja: 'とき、', en: 'When ' },
              den: { ja: '、そして', en: 'And ' },
              sol: { ja: '、したがって', en: 'Therefore ' }
            }[conjKey];
            let combined = '';
            if (targetLang === 'ja') {
              combined = `${condRes.text}${conjMap.ja}${consRes.text}${punct === '.' ? '。' : punct}`;
            } else {
              combined = `${conjMap.en}${condRes.text}, ${consRes.text}${punct === '。' ? '.' : punct}`;
            }
            translatedSentences.push(combined);
            allAlignments.push(...condRes.alignments, ...consRes.alignments);
            continue;
          }
        } else if (conjKey === 'den' || conjKey === 'sol') {
          const singleRes = translateSingleClause(conjMatch[2], targetLang, false);
          if (singleRes.success) {
            const prefix = {
              den: { ja: 'そして、', en: 'And ' },
              sol: { ja: 'だから、', en: 'So ' }
            }[conjKey];
            const combined = targetLang === 'ja'
              ? `${prefix.ja}${singleRes.text}${punct === '.' ? '。' : punct}`
              : `${prefix.en}${singleRes.text}${punct === '。' ? '.' : punct}`;
            translatedSentences.push(combined);
            allAlignments.push(...singleRes.alignments);
            continue;
          }
        }
      }

      // Check mid-sentence coordinating conjunctions: Clause1, den Clause2 / Clause1, sol Clause2
      const midCoordMatch = clean.match(/^(.+?),\s+(den|sol)\s+(.+)$/i);
      if (midCoordMatch) {
        const c1Str = midCoordMatch[1];
        const coordKey = midCoordMatch[2].toLowerCase();
        const c2Str = midCoordMatch[3];
        const r1 = translateSingleClause(c1Str, targetLang, false);
        const r2 = translateSingleClause(c2Str, targetLang, false);
        if (r1.success && r2.success) {
          const coordMap = {
            den: { ja: '、そして', en: ', and ' },
            sol: { ja: '、だから', en: ', so ' }
          }[coordKey];
          let combined = '';
          if (targetLang === 'ja') {
            combined = `${r1.text}${coordMap.ja}${r2.text}${punct === '.' ? '。' : punct}`;
          } else {
            combined = `${r1.text}${coordMap.en}${r2.text}${punct === '。' ? '.' : punct}`;
          }
          translatedSentences.push(combined);
          allAlignments.push(...r1.alignments, ...r2.alignments);
          continue;
        }
      }

      const res = translateSingleClause(clean, targetLang, false);
      if (res.success) {
        const trailingPunct = /[?？!！.。]$/.test(res.text) ? '' : punct;
        translatedSentences.push(res.text + trailingPunct);
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

    // Apply suffixes. Japanese uses the shared conjugation table so endings are not appended twice.
    const meaningJa = vInfo ? (vInfo.m || vInfo.meaningJa || verbClean) : verbClean;
    if (parsed.aspectSuffix) {
      if (!isJa) {
        if (parsed.aspectSuffix.suffix === 'ast') vEn = `want to ${vEn}`;
        else if (parsed.aspectSuffix.suffix === 'ar') vEn = `can ${vEn}`;
        else if (parsed.aspectSuffix.suffix === 'far') vEn = `have finished ${vEn}-ing`;
        else if (parsed.aspectSuffix.suffix === 'liv') vEn = `keep ${vEn}-ing`;
      }
    }

    if (parsed.isNeg && !isJa) vEn = `do not ${vEn}`;

    if (!isJa) {
      if (parsed.tensePrefix === 'fe') vEn = vEn.endsWith('e') ? `${vEn}d` : `${vEn}ed`;
      else if (parsed.tensePrefix === 'di') vEn = `is ${vEn}-ing`;
    } else {
      const conjugated = conjugateJapaneseVerb(meaningJa, parsed);
      if (conjugated) vJa = conjugated;
    }

    // 2. Resolve Phrases (including coordinated 'ul' and genitive 'en')
    let subjJa = '', subjEn = '', objJa = '', objEn = '', compJa = '', compEn = '', locJa = '', locEn = '', instJa = '', instEn = '', toJa = '', toEn = '', alJa = '', alEn = '', kuJa = '', kuEn = '';

    function resolveTokenJaEn(tok) {
      const clean = tok.toLowerCase().replace(/[.,!?;:]/g, '');
      const wInfo = lookupWord(clean);
      const ja = wInfo ? (wInfo.m || wInfo.meaningJa || clean).split(/[、／/]/)[0].trim() : clean;
      const en = wInfo ? (wInfo.en || wInfo.meaningEn || clean).split(/[,;/]/)[0].trim() : clean;
      const etym = wInfo && wInfo.morphemes ? ` [${wInfo.morphemes.join('+')}]` : '';
      return { ja, en, etym };
    }

    function resolvePhraseTokens(words) {
      // Handle 'ul' coordination inside a case phrase
      const ulIdx = words.findIndex(w => w.toLowerCase() === 'ul');
      if (ulIdx > 0 && ulIdx < words.length - 1) {
        const left = resolvePhraseTokens(words.slice(0, ulIdx));
        const right = resolvePhraseTokens(words.slice(ulIdx + 1));
        return {
          ja: `${left.ja}と${right.ja}`,
          en: `${left.en} and ${right.en}`,
          etym: left.etym || right.etym
        };
      }
      const main = resolveTokenJaEn(words[0]);
      if (words.length > 1) {
        const second = words[1].toLowerCase().replace(/[.,!?;:]/g, '');
        if (second !== 'ka') {
          const adj = resolveTokenJaEn(second);
          return { ja: `${adj.ja}${main.ja}`, en: `${adj.en} ${main.en}`, etym: main.etym };
        }
      }
      return main;
    }

    for (const ph of parsed.phrases) {
      const phraseText = ph.words.join(' ');
      const resolved = resolvePhraseTokens(ph.words);
      const pJa = resolved.ja;
      const pEn = resolved.en;

      const roleObj = CASE_MARKERS[ph.marker];
      const roleLabel = (roleObj ? (isJa ? roleObj.roleJa : roleObj.roleEn) : '修飾句') + (resolved.etym || '');

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
      } else if (ph.marker === 'to') {
        toJa = `${pJa}へ`;
        toEn = `to ${pEn}`;
      } else if (ph.marker === 'al') {
        alJa = `${pJa}に`;
        alEn = `for ${pEn}`;
      } else if (ph.marker === 'ku') {
        kuJa = `${pJa}と共に`;
        kuEn = `with ${pEn}`;
      } else if (ph.marker === 'va') {
        compJa = `${pJa}より`;
        compEn = `than ${pEn}`;
      } else if (ph.marker === 'uo') {
        locJa = `${pJa}で`;
        locEn = `in ${pEn}`;
      } else if (ph.marker === 'de') {
        instJa = `${pJa}によって`;
        instEn = `with ${pEn}`;
      } else if (ph.marker === 'en') {
        // Check if en introduces a relative clause (e.g. en [Verb] el [Subject]...)
        const firstWord = ph.words[0] ? ph.words[0].toLowerCase().replace(/[.,!?;:]/g, '') : '';
        const firstInfo = lookupWord(firstWord);
        const isRelativeClause = ph.words.length >= 2 && firstInfo && (firstInfo.p === '動' || firstInfo.pos === '動' || firstInfo.pos === '動詞' || /el|ia|uo|to/.test(ph.words[1]));
        if (isRelativeClause) {
          const relRes = translateSingleClause(ph.words.join(' '), targetLang, false);
          if (relRes.success) {
            if (objJa) {
              objJa = `${relRes.text} ` + objJa;
              objEn = `${objEn} that ${relRes.text}`;
            } else if (subjJa) {
              subjJa = `${relRes.text} ` + subjJa;
              subjEn = `${subjEn} that ${relRes.text}`;
            } else if (locJa) {
              locJa = `${relRes.text} ` + locJa;
              locEn = `${locEn} where ${relRes.text}`;
            }
            continue;
          }
        }
        if (objJa) {
          objJa = `${pJa}の` + objJa;
          objEn = `${objEn} of ${pEn}`;
        } else if (locJa) {
          locJa = `${pJa}の` + locJa;
          locEn = `${locEn} of ${pEn}`;
        } else if (subjJa) {
          subjJa = `${pJa}の` + subjJa;
          subjEn = `${subjEn} of ${pEn}`;
        }
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
      // Natural Japanese SOV order: S + Comp + Loc + To + Al + Ku + Inst + O + V
      let finalVJa = vJa;
      if (parsed.isQuestion) {
        finalVJa = finalVJa.endsWith('か') ? `${finalVJa}？` : `${finalVJa}か？`;
      }
      const parts = [subjJa, compJa, locJa, toJa, alJa, kuJa, instJa, objJa, finalVJa].filter(Boolean);
      clauseOut = parts.join(' ');
    } else {
      // Natural English SVO order: S + V + O + To + Al + Loc + Ku + Inst + Comp
      if (parsed.isQuestion) {
        const isPast = parsed.tensePrefix === 'fe' || (parsed.verbInfo && parsed.verbInfo.tense === 'past');
        const canModal = parsed.aspectSuffix && parsed.aspectSuffix.suffix === 'ar';
        const wantModal = parsed.aspectSuffix && parsed.aspectSuffix.suffix === 'ast';
        const aux = canModal ? 'Can' : (isPast ? 'Did' : 'Do');
        const s = subjEn || 'you';
        let mainV = vEn;
        if (canModal) mainV = mainV.replace(/^can\s+/, '');
        if (wantModal) mainV = `want to ${mainV}`;
        const parts = [aux, s, mainV, objEn, toEn, alEn, locEn, kuEn, instEn, compEn].filter(Boolean);
        clauseOut = parts.join(' ') + '?';
      } else {
        const parts = [subjEn, vEn, objEn, toEn, alEn, locEn, kuEn, instEn, compEn].filter(Boolean);
        clauseOut = parts.join(' ');
      }
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

    // 0. Interrogative SVO: Do/Does/Did/Can/Could [Subject] [Verb] ... ?
    const qMatch = englishText.trim().match(/^(do|does|did|can|could)\s+([a-z]+)\s+([a-z]+(?:\s+to\s+[a-z]+)?)(?:\s+(.+?))?\??$/i);
    if (qMatch) {
      const [, aux, subj, verbPart, objPart] = qMatch;
      const auxLow = aux.toLowerCase();
      const isPast = auxLow === 'did' || auxLow === 'could';
      const isCan = auxLow === 'can' || auxLow === 'could';

      // Reconstruct declarative clause
      let declEnglish = `${subj} `;
      if (isCan) {
        declEnglish += `can ${verbPart}`;
      } else if (isPast) {
        declEnglish += `did ${verbPart}`;
      } else {
        declEnglish += `${verbPart}`;
      }
      if (objPart) {
        declEnglish += ` ${objPart}`;
      }

      const declRes = translateSingleEnglishClause(declEnglish);
      if (declRes.success) {
        const cleanNeb = declRes.text.replace(/\.$/, '');
        const qNeb = `${cleanNeb} ro?`;
        return {
          text: qNeb,
          neb: qNeb,
          tag: 'English Interrogative -> Nebulith VSO (ro?)',
          alignment: [
            ...declRes.alignments,
            { src: englishText.trim(), dst: 'ro?', role: 'Interrogative Particle (ro)' }
          ],
          success: true
        };
      }
    }

    const norm = englishText.trim().toLowerCase();
    const vocab = getVocabMap();

    // 1. Compound Conjunctions: if / because / although / when ... , ...
    const conjMatch = englishText.trim().match(/^(if|because|although|even if|even though|when)\s+(.+)$/i);
    if (conjMatch) {
      const conjWord = conjMatch[1].toLowerCase();
      const parts = conjMatch[2].split(/,\s*/);
      if (parts.length >= 2) {
        const c1 = translateSingleEnglishClause(parts[0]);
        let secondPart = parts.slice(1).join(', ').trim();
        if (conjWord === 'if' && /^then\s+/i.test(secondPart)) {
          secondPart = secondPart.replace(/^then\s+/i, '');
        }
        const c2 = translateSingleEnglishClause(secondPart);
        if (c1.success && c2.success) {
          const nebConj = { if: 'Zen', because: 'Sen', although: 'Tor', 'even if': 'Tor', 'even though': 'Tor', when: 'Hav' }[conjWord];
          const res = `${nebConj} ${c1.text}, ${c2.text}.`;
          return {
            text: res,
            neb: res,
            tag: `${nebConj} Clause1, Clause2 (Compound SVO -> VSO)`,
            alignment: [...c1.alignments, ...c2.alignments],
            success: true
          };
        }
      }
    }

    // 2. Coordinated clauses: Clause1, and Clause2 / Clause1, so Clause2
    const coordMatch = englishText.trim().match(/^(.+?),\s+(and|so)\s+(.+)$/i);
    if (coordMatch) {
      const c1 = translateSingleEnglishClause(coordMatch[1]);
      const c2 = translateSingleEnglishClause(coordMatch[3]);
      if (c1.success && c2.success) {
        const conjWord = coordMatch[2].toLowerCase();
        const nebCoord = conjWord === 'and' ? 'den' : 'sol';
        const res = `${c1.text.replace(/\.$/, '')}, ${nebCoord} ${c2.text.replace(/\.$/, '')}.`;
        return {
          text: res,
          neb: res,
          tag: `Clause1, ${nebCoord} Clause2 (Coordinated SVO -> VSO)`,
          alignment: [...c1.alignments, ...c2.alignments],
          success: true
        };
      }
    }

    // 3. Initial And / So: And Clause / So Clause
    const initCoordMatch = englishText.trim().match(/^(and|so)\s+(.+)$/i);
    if (initCoordMatch) {
      const conjWord = initCoordMatch[1].toLowerCase();
      const c = translateSingleEnglishClause(initCoordMatch[2]);
      if (c.success) {
        const nebCoord = conjWord === 'and' ? 'Den' : 'Sol';
        const res = `${nebCoord} ${c.text.endsWith('.') ? c.text : c.text + '.'}`;
        return {
          text: res,
          neb: res,
          tag: `${nebCoord} Clause (Initial Coordination)`,
          alignment: c.alignments,
          success: true
        };
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
    // Accept only complete supported clauses. Unconsumed words must never disappear.
    if (/[!?]/.test(clause)) return { success: false };
    const norm = clause.trim().replace(/[.]+$/, '').toLowerCase();
    const nouns = {
      i: 'mi', me: 'mi', you: 'ti', we: 'miin', us: 'miin',
      they: 'riin', them: 'riin', star: 'vyr', stars: 'vyr',
      night: 'valar', sun: 'zohar', water: 'daris', light: 'fal',
      house: 'govan', room: 'vorn', garden: 'velar', city: 'domom',
      lake: 'daron', forest: 'velom', book: 'pamel', market: 'renar'
    };
    const compObj = _externalVerifiedCompounds || (typeof VERIFIED_CANONICAL_COMPOUNDS !== 'undefined' ? VERIFIED_CANONICAL_COMPOUNDS : (typeof globalThis !== 'undefined' ? globalThis.VERIFIED_CANONICAL_COMPOUNDS : null));
    if (compObj && Array.isArray(compObj.entries)) {
      for (const c of compObj.entries) {
        if (c.nrs && !Object.hasOwn(nouns, c.nrs.toLowerCase())) {
          nouns[c.nrs.toLowerCase()] = c.nrs.toLowerCase();
        }
        for (const g of String(c.meaningEn || '').split(/[,;/]/)) {
          const cleanG = g.trim().toLowerCase().replace(/^(?:the|a|an)\s+/, '');
          if (cleanG && /^[a-z]+$/.test(cleanG) && !Object.hasOwn(nouns, cleanG)) {
            nouns[cleanG] = c.nrs.toLowerCase();
          }
        }
      }
    }
    const verbs = {
      like: 'cynel', likes: 'cynel', liked: 'fe cynel',
      love: 'cynel', loves: 'cynel', loved: 'fe cynel',
      walk: 'poran', walks: 'poran', walked: 'fe poran',
      shine: 'falun', shines: 'falun', shone: 'fe falun',
      see: 'vyrel', sees: 'vyrel', saw: 'fe vyrel',
      observe: 'vyrel', observes: 'vyrel', observed: 'fe vyrel',
      drink: 'bion', drinks: 'bion', drank: 'fe bion',
      eat: 'neran', eats: 'neran', ate: 'fe neran',
      write: 'soran', writes: 'soran', wrote: 'fe soran',
      record: 'soran', records: 'soran', recorded: 'fe soran',
      protect: 'vymin', protects: 'vymin', protected: 'fe vymin',
      rest: 'seron', rests: 'seron', rested: 'fe seron',
      know: 'belan', knows: 'belan', knew: 'fe belan'
    };
    const adjectives = {
      beautiful: 'cylani', bright: 'falani', dark: 'valani', warm: 'surani',
      white: 'alin', pure: 'alin', silver: 'tyni', red: 'pyrin', astral: 'vyri',
      blue: 'kyrin', clear: 'kyrin', cyan: 'kyrin',
      green: 'zylin', verdant: 'zylin',
      flame: 'pyrin',
      gold: 'syvan', golden: 'syvan',
      emerald: 'eirin', fresh: 'eirin',
      silent: 'moran', calm: 'moran',
      deep: 'telin', profound: 'telin'
    };
    const nounPattern = '(?:(?:the|a|an)\\s+)?([a-z]+)';
    const fail = () => ({ success: false });
    const cap = s => s.charAt(0).toUpperCase() + s.slice(1);
    const noun = text => {
      const match = text.match(new RegExp('^' + nounPattern + '$'));
      return match && Object.hasOwn(nouns, match[1]) ? nouns[match[1]] : null;
    };

    const copula = norm.match(new RegExp('^' + nounPattern + '\\s+(is|are)\\s+(not\\s+)?(more\\s+)?([a-z]+)(?:\\s+than\\s+' + nounPattern + ')?$'));
    if (copula) {
      const [, subject, , negation, more, adjective, comparison] = copula;
      if (!Object.hasOwn(nouns, subject) || !Object.hasOwn(adjectives, adjective) ||
          !!more !== !!comparison || comparison && !Object.hasOwn(nouns, comparison)) return fail();
      const predicate = (negation ? 'ne ' : '') + adjectives[adjective];
      return {
        text: cap(predicate) + ' el ' + nouns[subject] + (comparison ? ' va ' + nouns[comparison] : ''),
        tag: comparison ? 'Comparative' : 'Adjective Predicate',
        alignments: [
          { src: subject, dst: 'el ' + nouns[subject], role: 'Subject' },
          { src: (negation || '') + adjective, dst: cap(predicate), role: 'Predicate' },
          ...(comparison ? [{ src: comparison, dst: 'va ' + nouns[comparison], role: 'Comparison' }] : [])
        ], success: true
      };
    }

    const match = norm.match(new RegExp('^' + nounPattern + "\\s+(?:(do not|does not|did not|don't|doesn't|didn't)\\s+)?(?:(want to|wanted to|can|could|finish|finished|keep|kept)\\s+)?([a-z]+)(?:\\s+(.+))?$"));
    if (!match) return fail();
    const [, subject, auxiliary, aspectModal, rawVerb, objectText] = match;
    const verb = rawVerb.endsWith('ing') && (aspectModal === 'finish' || aspectModal === 'finished' || aspectModal === 'keep' || aspectModal === 'kept')
      ? (Object.hasOwn(verbs, rawVerb.slice(0, -3)) ? rawVerb.slice(0, -3) : (Object.hasOwn(verbs, rawVerb.slice(0, -3) + 'e') ? rawVerb.slice(0, -3) + 'e' : rawVerb))
      : rawVerb;
    if (!Object.hasOwn(nouns, subject) || !Object.hasOwn(verbs, verb)) return fail();
    const prepMap = {
      to: 'to',
      with: 'ku',
      in: 'uo',
      at: 'uo',
      for: 'al',
      from: 'va'
    };

    // Extract trailing prepositional phrases
    const prepPhrases = [];
    let currentRemainder = (objectText || '').trim();

    while (currentRemainder) {
      const ppMatch = currentRemainder.match(/(?:^|\s+)(to|with|in|at|for|from)\s+(?:(the|a|an)\s+)?(?:([a-z]+)\s+)?([a-z]+)$/i);
      if (ppMatch) {
        const [full, prep, art, mod, pNoun] = ppMatch;
        const nNeb = noun(pNoun);
        if (!nNeb) break;
        if (mod && !Object.hasOwn(adjectives, mod)) break;
        const adjNeb = mod ? adjectives[mod] : null;
        const nebMarker = prepMap[prep.toLowerCase()];
        prepPhrases.unshift({
          prep: prep.toLowerCase(),
          nebMarker,
          noun: nNeb,
          adjective: adjNeb,
          rawText: full.trim()
        });
        currentRemainder = currentRemainder.slice(0, currentRemainder.length - full.length).trim();
      } else {
        break;
      }
    }

    let object = null;
    let adjective = null;
    if (currentRemainder) {
      const objectMatch = currentRemainder.match(/^(?:(?:the|a|an)\s+)?(?:([a-z]+)\s+)?([a-z]+)$/);
      if (!objectMatch) return fail();
      const [, modifier, objectNoun] = objectMatch;
      object = noun(objectNoun);
      if (!object || (modifier && !Object.hasOwn(adjectives, modifier))) return fail();
      adjective = modifier ? adjectives[modifier] : null;
    }

    // Only known transitive predicates may take a direct object; required direct objects stay required.
    const transitive = ['cynel', 'vyrel', 'belan', 'bion', 'neran', 'soran', 'vymin'].includes(verbs[verb].replace(/^fe /, ''));
    if (transitive !== !!object) return fail();

    if (auxiliary && verbs[verb].startsWith('fe ')) return fail();
    const modalPast = aspectModal === 'wanted to' || aspectModal === 'could' || aspectModal === 'finished' || aspectModal === 'kept';
    const aspectSuf = !aspectModal ? '' : (aspectModal.startsWith('want') ? 'ast' : (aspectModal === 'can' || aspectModal === 'could' ? 'ar' : (aspectModal.startsWith('finish') ? 'far' : 'liv')));
    const past = verbs[verb].startsWith('fe ') || (auxiliary && auxiliary.startsWith('did')) || modalPast;
    const baseVerb = verbs[verb].replace(/^fe /, '') + aspectSuf;
    const predicate = (past ? 'fe ' : '') + (auxiliary ? 'ne ' : '') + baseVerb;
    const objectPhrase = object ? ' ia ' + object + (adjective ? ' ' + adjective : '') : '';
    let ppNebStr = '';
    for (const pp of prepPhrases) {
      ppNebStr += ' ' + pp.nebMarker + ' ' + pp.noun + (pp.adjective ? ' ' + pp.adjective : '');
    }
    const fullNeb = cap(predicate) + ' el ' + nouns[subject] + objectPhrase + ppNebStr;
    return {
      text: fullNeb,
      tag: 'English SVO -> Nebulith VSO',
      alignments: [
        { src: subject, dst: 'el ' + nouns[subject], role: 'Subject' },
        { src: (auxiliary ? auxiliary + ' ' : '') + verb, dst: cap(predicate), role: 'Predicate' },
        ...(object ? [{ src: currentRemainder, dst: objectPhrase.trim(), role: 'Object' }] : []),
        ...prepPhrases.map(pp => ({
          src: pp.rawText,
          dst: (pp.nebMarker + ' ' + pp.noun + (pp.adjective ? ' ' + pp.adjective : '')).trim(),
          role: `Prepositional Phrase (${pp.prep})`
        }))
      ], success: true
    };
  }

  const GODAN_RU = new Set(['走る', '帰る', '入る', '切る', '知る', '要る', '減る', '焦る', '限る', '蹴る', '滑る', '照る', '練る', '参る', '喋る']);
  const ICHIDAN_VOWEL = 'いきしちにひみりぎじぢびぴえけせてねへめれげぜでべぺ';

  function glossList(meaning) {
    return String(meaning || '').split(/[、／/・]/).map(part => part.replace(/（[^）]*）|\([^)]*\)/g, '').trim()).filter(Boolean);
  }

  function dictionaryVerbKind(lemma) {
    if (!lemma || lemma.length < 2) return null;
    if (lemma === '来る' || lemma === 'くる') return 'kuru';
    if (lemma.endsWith('する')) return 'suru';
    if (lemma.endsWith('くる')) return 'kuru';
    if (lemma.endsWith('る')) {
      if (GODAN_RU.has(lemma)) return 'る';
      return ICHIDAN_VOWEL.includes(lemma[lemma.length - 2]) ? 'ichidan' : 'る';
    }
    const last = lemma.slice(-1);
    return 'うくぐすつぬぶむ'.includes(last) ? last : null;
  }

  function localJapaneseForms(lemma, kind) {
    let past, te, negative, polite, potStem;
    if (kind === 'kuru') {
      past = '来た'; te = '来て'; negative = '来ない'; polite = '来'; potStem = '来られ';
    } else if (kind === 'suru') {
      const stem = lemma.slice(0, -2);
      past = stem + 'した'; te = stem + 'して'; negative = stem + 'しない'; polite = stem + 'し'; potStem = stem + 'でき';
    } else if (kind === 'ichidan') {
      const stem = lemma.slice(0, -1);
      past = stem + 'た'; te = stem + 'て'; negative = stem + 'ない'; polite = stem; potStem = stem + 'られ';
    } else {
      const endings = { 'う': ['わ', 'い', 'った', 'って', 'え'], 'く': ['か', 'き', 'いた', 'いて', 'け'], 'ぐ': ['が', 'ぎ', 'いだ', 'いで', 'げ'], 'す': ['さ', 'し', 'した', 'して', 'せ'], 'つ': ['た', 'ち', 'った', 'って', 'て'], 'ぬ': ['な', 'に', 'んだ', 'んで', 'ね'], 'ぶ': ['ば', 'び', 'んだ', 'んで', 'べ'], 'む': ['ま', 'み', 'んだ', 'んで', 'め'], 'る': ['ら', 'り', 'った', 'って', 'れ'] };
      const table = endings[kind];
      if (!table || !lemma.endsWith(kind)) return [];
      const stem = lemma.slice(0, -1);
      negative = stem + table[0] + 'ない';
      polite = stem + table[1];
      past = stem + table[2];
      te = stem + table[3];
      potStem = stem + table[4];
    }
    const rows = [
      [lemma, []],
      [past, ['fe']],
      [negative, ['ne']],
      [negative.slice(0, -1) + 'かった', ['fe', 'ne']],
      [te + 'いる', ['di']],
      [te + 'いた', ['fe', 'di']],
      [te + 'いない', ['ne', 'di']],
      [te + 'いなかった', ['fe', 'ne', 'di']],
      [polite + 'たい', [], 'ast', '希望'],
      [polite + 'たかった', ['fe'], 'ast', '過去の希望'],
      [polite + 'たくない', ['ne'], 'ast', '希望の否定'],
      [polite + 'たくなかった', ['fe', 'ne'], 'ast', '過去の希望の否定'],
      [potStem + 'る', [], 'ar', '可能'],
      [potStem + 'た', ['fe'], 'ar', '過去の可能'],
      [potStem + 'ない', ['ne'], 'ar', '可能の否定'],
      [potStem + 'なかった', ['fe', 'ne'], 'ar', '過去の可能の否定'],
      [polite + '終える', [], 'far', '完了相'],
      [polite + '終えた', ['fe'], 'far', '過去の完了相'],
      [polite + '終えない', ['ne'], 'far', '完了相の否定'],
      [polite + '終えなかった', ['fe', 'ne'], 'far', '過去の完了相の否定'],
      [polite + '続ける', [], 'liv', '継続相'],
      [polite + '続けた', ['fe'], 'liv', '過去の継続相'],
      [polite + '続けない', ['ne'], 'liv', '継続相の否定'],
      [polite + '続けなかった', ['fe', 'ne'], 'liv', '過去の継続相の否定']
    ];
    return rows.map(([ending, prefixes, suffix = '', feature = '']) => ({ ending, prefixes, suffix, feature }));
  }

  function formsFor(lemma, kind) {
    const external = typeof globalThis !== 'undefined' ? globalThis.nebulithJapaneseForms : null;
    if (typeof external === 'function') {
      try { return external(lemma, kind); } catch (_) { /* use the local table */ }
    }
    return localJapaneseForms(lemma, kind);
  }

  function samePrefixes(actual, expected) {
    if (actual.length !== expected.length) return false;
    const got = new Set(actual);
    return expected.every(prefix => got.has(prefix));
  }

  function selectJapaneseForm(forms, prefixes, suffix) {
    let rows = forms.filter(form => (form.suffix || '') === suffix && samePrefixes(form.prefixes || [], prefixes));
    if (suffix === 'ast') rows = rows.filter(form => /たい/.test(form.ending) || (form.feature || '').includes('希望'));
    const plain = rows.filter(form => !/ます|です/.test(form.ending) && !/ことができる|ことができな/.test(form.ending));
    if (plain.length) rows = plain;
    rows.sort((a, b) => a.ending.length - b.ending.length);
    return rows[0] || null;
  }

  function conjugateJapaneseVerb(meaning, parsed) {
    const suffix = parsed.aspectSuffix && ['ast', 'ar', 'far', 'liv'].includes(parsed.aspectSuffix.suffix) ? parsed.aspectSuffix.suffix : '';
    const prefixes = [];
    if (parsed.isNeg) prefixes.push('ne');
    if (parsed.tensePrefix === 'fe' || parsed.tensePrefix === 'di') prefixes.push(parsed.tensePrefix);
    if (!suffix && !prefixes.length) return null;
    for (const lemma of glossList(meaning)) {
      const kind = dictionaryVerbKind(lemma);
      if (!kind) continue;
      const chosen = selectJapaneseForm(formsFor(lemma, kind), prefixes, suffix);
      if (chosen) return chosen.ending;
    }
    return null;
  }

  return {
    parseNebulithClause,
    configure,
    translateNebulith,
    translateEnglishToNebulith
  };
}));

