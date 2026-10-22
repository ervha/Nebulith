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
  let _externalRules = null;

  function configure(vocab, verifiedCompounds, rules = null) {
    _externalVocab = vocab;
    _externalVerifiedCompounds = verifiedCompounds;
    _externalRules = rules;
  }

  function translationRules() {
    if (_externalRules) return _externalRules;
    const extensions = typeof TRANSLATION_EXTENSIONS !== 'undefined' ? TRANSLATION_EXTENSIONS : {};
    const frames = typeof GRAMMAR_FRAMES !== 'undefined' ? GRAMMAR_FRAMES : {};
    const verbs = [...(extensions.productive?.verbs||[]),...(extensions.compoundProductive?.verbs||[]),...(extensions.roadmapProductive?.verbs||[])];
    return {frames:{...Object.fromEntries(verbs.map(v=>[v.id,v.frame])),...(extensions.frames||{}),...frames},verbs,adjectives:extensions.roadmapProductive?.adjectives||[],held:extensions.roadmapProductive?.held||[]};
  }

  function englishForm(phrase,kind) {
    const [head,...tail]=phrase.split(' '),rest=tail.length?' '+tail.join(' '):'';
    const irregular={be:'was',have:'had',do:'did',go:'went',come:'came',drink:'drank',eat:'ate',write:'wrote',sing:'sang',say:'said',take:'took',give:'gave',see:'saw',think:'thought',know:'knew',make:'made',feel:'felt',leave:'left',run:'ran',stand:'stood',sleep:'slept',build:'built',teach:'taught',find:'found',speak:'spoke',tell:'told',understand:'understood',shine:'shone',bring:'brought'};
    let word=head;
    if(kind==='past')word=irregular[head]||(head.endsWith('e')?head+'d':/[^aeiou]y$/.test(head)?head.slice(0,-1)+'ied':head+'ed');
    if(kind==='third')word=head==='have'?'has':/[^aeiou]y$/.test(head)?head.slice(0,-1)+'ies':/(s|sh|ch|x|z|o)$/.test(head)?head+'es':head+'s';
    if(kind==='ing')word=head.endsWith('ie')?head.slice(0,-2)+'ying':head.endsWith('e')&&!/ee$/.test(head)?head.slice(0,-1)+'ing':['run','sit','swim','begin','stop','plan'].includes(head)?head+head.at(-1)+'ing':head+'ing';
    return word+rest;
  }

  function englishPredicate(base,parsed,subject) {
    const past=parsed.prefixes.includes('fe'),progress=parsed.prefixes.includes('di'),neg=parsed.isNeg;
    const plural=/^(you|we|they)$/i.test(subject)||/ and /.test(subject),first=/^i$/i.test(subject),third=!plural&&!first;
    const be=past?(plural?'were':'was'):(plural?'are':first?'am':'is');
    const aspect=parsed.aspectSuffix?.suffix;
    let verb=base,aux=past?'Did':third?'Does':'Do',main=base;
    if(aspect==='ar'){aux=past?'Could':'Can';main=base;verb=aux.toLowerCase()+(neg?' not ':' ')+base;}
    else if(progress){aux=be;main=englishForm(base,'ing');verb=be+(neg?' not ':' ')+main;}
    else {
      if(aspect==='ast')verb='want to '+base;
      if(aspect==='far')verb='finish '+englishForm(base,'ing');
      if(aspect==='liv')verb='keep '+englishForm(base,'ing');
      main=verb;
      verb=neg?(past?'did not ':'do'+(third?'es':'')+' not ')+verb:past?englishForm(verb,'past'):third?englishForm(verb,'third'):verb;
      if(aspect==='cor'){verb='repeatedly '+verb;main='repeatedly '+main;}
    }
    if(parsed.prefixes.includes('se'))verb='perhaps '+verb;
    return {verb,aux:aux[0].toUpperCase()+aux.slice(1),main:(neg?'not ':'')+main};
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
    ri: {m:'彼／彼女',en:'he / she'},
    miin: { m: '私たち', en: 'we / us' },
    riin: { m: '彼ら', en: 'they / them' },
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
    if (!vocab.size && BUILTIN_VOCAB[clean]) return { r: clean,p:['cylani','surani','valani'].includes(clean)?'形':['cynel','poran','falun','vyrel','seron'].includes(clean)?'動':'名', ...BUILTIN_VOCAB[clean] };

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
    const prefixes = [];

    // Check pre-verbal particles
    while (idx < tokens.length) {
      const low = tokens[idx].toLowerCase();
      if (low === 'ne') {
        prefixes.push(low);
        isNeg = true;
        idx++;
      } else if (low === 'fe' || low === 'di' || low === 'se') {
        prefixes.push(low);
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
    }

    // Check sentence-level question marker: trailing 'ro', 'ro?', or '?'
    let isQuestion = clauseStr.trim().endsWith('?');
    const rawTokens = tokens.slice(idx);
    if (rawTokens.length > 0) {
      const lastTok = rawTokens[rawTokens.length - 1].toLowerCase().replace(/[.,!?;:]/g, '');
      if (lastTok === 'ro' || lastTok === 'ka') {
        isQuestion = true;
      }
    }

    // Parse Case Phrases: el S, ia O, uo Loc, de Inst, va Comp, en Gen
    const phrases = [];
    const unmarkedTokens = [];
    let currentMarker = null;
    let currentTokens = [];

    while (idx < tokens.length) {
      const tok = tokens[idx];
      const low = tok.toLowerCase().replace(/[.,!?;:]/g, '');
      if ((low === 'ro' || low === 'ka') && idx===tokens.length-1) {
        // standalone question particle; stop parsing case phrase
        isQuestion = true;
        idx++;
        continue;
      }
      // If currentMarker is 'en' or 'ia' and it introduced a clause (starts with a verb or interrogative),
      // keep accumulating all internal tokens until sentence ends.
      const isInsideSubClause = (currentMarker === 'en' || currentMarker === 'ia') && currentTokens.length > 0 && (() => {
        const firstW = currentTokens[0].toLowerCase().replace(/[.,!?;:]/g, '');
        const isInterrogative = ['kauo', 'kate', 'kaas', 'kahav', 'kaku', 'kazen'].includes(firstW);
        if (isInterrogative) return true;
        const info = lookupWord(firstW);
        return info && (info.p === '動' || info.pos === '動' || info.pos === '動詞');
      })();

      if (CASE_MARKERS[low] && !isInsideSubClause) {
        if (currentMarker) {
          phrases.push({ marker: currentMarker, words: [...currentTokens] });
        }
        currentMarker = low;
        currentTokens = [];
      } else {
        if (currentMarker) {
          currentTokens.push(tok);
        } else {
          // Unmarked words cannot be silently discarded before a case phrase.
          unmarkedTokens.push(tok);
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
      prefixes,
      aspectSuffix,
      verbToken,
      verbInfo,
      incompleteCase: !!currentMarker && !currentTokens.length,
      unmarkedTokens,
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
              sen: { ja: 'なら、', en: 'If ' },
              zen: { ja: 'ので、', en: 'Because ' },
              tor: { ja: 'けれど、', en: 'Although ' },
              hav: { ja: 'とき、', en: 'When ' },
              den: { ja: '、そして', en: 'And ' },
              sol: { ja: 'ために、', en: 'So that ' }
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
        return { text: null, error: res.error || `未対応構文: ${sent}`, success: false };
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
    if(!vInfo)return {text:'',alignments:[],success:false,error:'未知の述語: '+verbClean};
    const position=vInfo.p||vInfo.pos||'';
    if(parsed.prefixes.length&&position&&!/動|形/.test(position))return {success:false,error:'名詞・機能語に動詞の活用を付けることはできません。'};
    if(parsed.phrases.length && position && !/動|形/.test(position))return {text:'',alignments:[],success:false,error:'名詞や機能語は動詞として確定できません。'};
    if(parsed.incompleteCase || parsed.unmarkedTokens.length)return {text:'',alignments:[],success:false,error:'未解析の語、または未完成の格句があります。'};
    if(parsed.phrases.length && !parsed.phrases.some(p=>p.marker==='el'))return {text:'',alignments:[],success:false,error:'主体のel句が必要です。'};
    if(new Set(parsed.phrases.map(p=>p.marker)).size!==parsed.phrases.length)return {text:'',alignments:[],success:false,error:'同じ格句が重複しています。'};
    if(new Set(parsed.prefixes).size!==parsed.prefixes.length)return {success:false,error:'時制・相の標識が重複しています。'};
    if(parsed.aspectSuffix?.suffix==='iin')return {success:false,error:'複数接尾辞を述語としては確定できません。'};
    if(parsed.isQuestion&&parsed.prefixes.includes('se'))return {success:false,error:'推量と疑問の組み合わせは未対応です。'};
    const rules=translationRules(),frame=rules.frames?.[vInfo.id];
    const fail=error=>({text:null,alignments:[],success:false,error,source:clauseStr});
    if(parsed.phrases.length && frame) {
      const markers=parsed.phrases.map(p=>p.marker);
      if(!frame.required.every(c=>markers.includes(c)))return fail('述語に必須の格句が不足しています。');
      if(markers.some(c=>c!=='en'&&!frame.allowed.includes(c)))return fail('述語の許容格に合わない格句があります。');
      const target=parsed.phrases.find(p=>p.marker==='ia');
      if(frame.recipientAmbiguity&&!markers.includes('al')&&target?.words.length===1&&frame.recipientAmbiguity.roots.includes(target.words[0]?.toLowerCase()))return fail(frame.recipientAmbiguity.reason);
      for(const [role,rule] of Object.entries(frame.literalArguments||{})) {
        const ph=parsed.phrases.find(p=>p.marker===role);
        if(ph&&!rule.roots.includes(ph.words[0]?.toLowerCase()))return fail(rule.reason);
      }
    }
    for(const ph of parsed.phrases) {
      if(!ph.words.length)return fail('空の格句があります。');
      for(const word of ph.words)if(!lookupWord(word)&&!['ul','en'].includes(word.toLowerCase()))return fail('未知の引数: '+word);
      const first=lookupWord(ph.words[0]);
      const nested=/動/.test(first?.p||first?.pos||'')||['kauo','kate','kaas','kahav','kaku','kazen'].includes(ph.words[0]?.toLowerCase());
      if(nested) {
        const words=/動/.test(first?.p||first?.pos||'')?ph.words:ph.words.slice(1);
        const result=translateSingleClause(words.join(' '),targetLang);
        if(!result.success)return fail(result.error||'従属節が未確定です。');
      } else {
        const groups=ph.words.join(' ').split(/\s+ul\s+/);
        for(const group of groups){const words=group.split(' ');if(words.length>2)return fail('未対応の複雑な名詞句です。語を省略せず保持します。');if(words.length===2&&!/形/.test(lookupWord(words[1])?.p||''))return fail('名詞句の修飾を確定できません。');}
      }
    }

    let vJa = vInfo ? (vInfo.m || vInfo.meaningJa || verbClean).split(/[、／/]/)[0].trim() : verbClean;
    let vEn = vInfo ? (vInfo.en || vInfo.meaningEn || verbClean).split(/[,;/]/)[0].trim() : verbClean;

    // Apply suffixes. Japanese uses the shared conjugation table so endings are not appended twice.
    const verbRule=rules.verbs?.find(v=>v.id===vInfo.id);
    const meaningJa = verbRule?.lemma || (vInfo.m || vInfo.meaningJa || verbClean);
    if(isJa&&verbRule)vJa=verbRule.lemma;
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
      if(parsed.prefixes.includes('fe')&&parsed.isNeg)vEn=vEn.replace(/^do not /,'did not ');
      else if (parsed.prefixes.includes('fe')) vEn = vEn.endsWith('e') ? `${vEn}d` : `${vEn}ed`;
      if(parsed.prefixes.includes('di')) {
        const base=(vInfo.en||vInfo.meaningEn||verbClean).split(/[,;/]/)[0].trim();
        const ing=base.endsWith('e')?base.slice(0,-1)+'ing':base+'ing';
        vEn=(parsed.prefixes.includes('fe')?'was ':'is ')+(parsed.isNeg?'not ':'')+ing;
      }
      if(parsed.prefixes.includes('se'))vEn='perhaps '+vEn.replace(/^perhaps /,'');
    } else {
      const conjugated = conjugateJapaneseVerb(meaningJa, parsed, verbRule?.conjugation);
      if (conjugated) vJa = conjugated;
      if(parsed.aspectSuffix?.suffix==='cor')vJa='繰り返し'+vJa;
      if(parsed.prefixes.includes('se'))vJa+='かもしれない';
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
      const pEn = ph.words.length===1&&ph.marker!=='el'?({mi:'me',miin:'us',riin:'them'}[ph.words[0].toLowerCase()]||resolved.en):resolved.en;

      const roleObj = CASE_MARKERS[ph.marker];
      const roleLabel = (roleObj ? (isJa ? roleObj.roleJa : roleObj.roleEn) : '修飾句') + (resolved.etym || '');

      const phraseAlignmentIndex=alignments.length;
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
        const firstWord = ph.words[0] ? ph.words[0].toLowerCase().replace(/[.,!?;:]/g, '') : '';
        const whMap = {
          kauo: { en: 'where', ja: 'どこへ' },
          kate: { en: 'what', ja: '何を' },
          kaas: { en: 'who', ja: '誰が' },
          kahav: { en: 'when', ja: 'いつ' },
          kaku: { en: 'how', ja: 'どのように' },
          kazen: { en: 'why', ja: 'なぜ' }
        };
        const isWh = Boolean(whMap[firstWord]);
        const firstInfo = lookupWord(firstWord);
        const isComplementClause = isWh || (ph.words.length >= 2 && firstInfo && (firstInfo.p === '動' || firstInfo.pos === '動' || firstInfo.pos === '動詞' || /el|ia|uo|to/.test(ph.words[1])));
        if (isComplementClause) {
          if (isWh) {
            const subWords = ph.words.slice(1);
            const compRes = translateSingleClause(subWords.join(' '), targetLang, false);
            if (compRes.success) {
              const whInfo = whMap[firstWord];
              let subTextJa = compRes.text.replace(/^(.+?)は/, '$1が');
              objJa = `${whInfo.ja} ${subTextJa}か`;
              objEn = `${whInfo.en} ${compRes.text}`;
              alignments[phraseAlignmentIndex].dst=isJa?objJa:objEn;
              alignments[phraseAlignmentIndex].role='従属節（文単位）';
              alignments.push(...compRes.alignments);
              continue;
            }
          } else {
            const compRes = translateSingleClause(ph.words.join(' '), targetLang, false);
            if (compRes.success) {
              const verbClean = (parsed.verbToken || '').toLowerCase();
              const isQuotationVerb = /fenor|minpan|cival|soras|belan/.test(verbClean);
              let subTextJa = compRes.text.replace(/^(.+?)は/, '$1が');
              objJa = isQuotationVerb ? `${subTextJa}と` : `${subTextJa}ことを`;
              objEn = `that ${compRes.text}`;
              alignments[phraseAlignmentIndex].dst=isJa?objJa:objEn;
              alignments[phraseAlignmentIndex].role='従属節（文単位）';
              alignments.push(...compRes.alignments);
              continue;
            }
          }
        }
        objJa = `${pJa}を`;
        objEn = pEn;
      } else if (ph.marker === 'to') {
        toJa = `${pJa}へ`;
        toEn = `to ${pEn}`;
      } else if (ph.marker === 'al') {
        alJa = `${pJa}に`;
        alEn = `to ${pEn}`;
      } else if (ph.marker === 'ku') {
        kuJa = `${pJa}と共に`;
        kuEn = `with ${pEn}`;
      } else if (ph.marker === 'va') {
        if(/動/.test(position)&&frame?.allowed.includes('va')){compJa=`${pJa}から`;compEn=`from ${pEn}`;}
        else if(/形/.test(position)){compJa=`${pJa}より`;compEn=`than ${pEn}`;}
        else return fail('起点と比較の区別を確定できません。');
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

    // Realize copular adjectives as predicates rather than noun objects.
    const copular=vInfo.r==='relen';
    let englishCopula=null;
    let adjectiveInfo=/形/.test(position)?vInfo:null;
    if(copular) {
      const object=parsed.phrases.find(p=>p.marker==='ia');
      if(object?.words.length===1)adjectiveInfo=lookupWord(object.words[0]);
      if(!adjectiveInfo)return fail('コピュラの補語を確定できません。');
      if(rules.held?.some(a=>a.id===adjectiveInfo.id))return fail('補語の語義・品詞は再整理待ちです。');
    }
    if(adjectiveInfo&&(/形/.test(adjectiveInfo.p||'')||copular)) {
      if(parsed.prefixes.includes('di')||parsed.aspectSuffix)return fail('この形容詞叙述の相・モダリティは未対応です。');
      const row=rules.adjectives?.find(a=>a.id===adjectiveInfo.id);
      if(row&&!row.predicative)return fail('この形容詞は修飾のみ対応し、叙述は保留しています。');
      let lemma=row?.predicateLemma||row?.lemma||(adjectiveInfo.m||'').split(/[、／]/)[0];
      const past=parsed.prefixes.includes('fe'),negative=parsed.isNeg;
      if((row?.kind==='i'||!row&&lemma.endsWith('い'))&&/形/.test(adjectiveInfo.p||'')) {
        const stem=lemma.endsWith('良い')?lemma.slice(0,-2)+'良':lemma.slice(0,-1);
        vJa=negative?stem+(past?'くなかった':'くない'):past?stem+'かった':lemma;
      } else {
        lemma=lemma.replace(/[なの]$/,'');vJa=lemma+(negative?(past?'ではなかった':'ではない'):(past?'だった':'だ'));
      }
      if(parsed.prefixes.includes('se'))vJa+='かもしれない';
      const plural=/^(you|we|they)$/i.test(subjEn),first=/^i$/i.test(subjEn);
      const be=past?(plural?'were':'was'):(plural?'are':first?'am':'is');
      const adjectiveEn=(adjectiveInfo.en||'').split(/[,;/]/)[0].trim();
      vEn=be+(negative?' not ':' ')+adjectiveEn;
      englishCopula={be,complement:(negative?'not ':'')+adjectiveEn};
      if(copular){objJa='';objEn='';}
    }

    const englishVerb=!englishCopula?englishPredicate((vInfo.en||vInfo.meaningEn||verbClean).split(/[,;/]/)[0].trim(),parsed,subjEn):null;
    if(!isJa&&englishVerb)vEn=englishVerb.verb;
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
        const s = subjEn || 'you';
        const aux=englishCopula?englishCopula.be[0].toUpperCase()+englishCopula.be.slice(1):englishVerb.aux;
        const mainV=englishCopula?englishCopula.complement:englishVerb.main;
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
    const result=translateEnglishUnchecked(englishText);
    if(!result.success)return result;
    const checked=translateNebulith(result.neb||result.text,'ja');
    return checked.success?result:{text:null,source:englishText,success:false,error:checked.error||'生成先の項構造を検証できません。'};
  }
  function translateEnglishUnchecked(englishText) {
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
    const conjMatch = englishText.trim().match(/^(if|because|although|even if|even though|when|while|so that|in order that)\s+(.+)$/i);
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
          const nebConj = { if: 'Sen', because: 'Zen', although: 'Tor', 'even if': 'Tor', 'even though': 'Tor', when: 'Hav', while: 'Hav', 'so that': 'Sol', 'in order that': 'Sol' }[conjWord];
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

    // Reported Speech / Thought: [Subject] [says/said/thinks/thought/knows/knew] that [Clause]
    const repMatch = englishText.trim().match(/^([a-z]+)\s+(says?|said|thinks?|thought|knows?|knew)\s+that\s+(.+)$/i);
    if (repMatch) {
      const [, sWord, vWord, subClause] = repMatch;
      const vMap = {
        say: 'Fenor', says: 'Fenor', said: 'Fe fenor',
        think: 'Minpan', thinks: 'Minpan', thought: 'Fe minpan',
        know: 'Velsen', knows: 'Velsen', knew: 'Fe velsen'
      };
      const nMap = {
        i: 'mi', you: 'ti', we: 'miin', they: 'riin',
        he: 'taas', she: 'taas', it: 'tate'
      };
      const vNeb = vMap[vWord.toLowerCase()];
      const sNeb = nMap[sWord.toLowerCase()] || sWord.toLowerCase();
      const subRes = translateSingleEnglishClause(subClause);
      if (vNeb && subRes.success) {
        const res = `${vNeb} el ${sNeb} ia ${subRes.text.replace(/\.$/, '')}.`;
        return {
          text: res,
          neb: res,
          tag: 'Reported Speech / Thought (SVO -> VSO that-clause)',
          alignment: [
            { src: sWord, dst: 'el ' + sNeb, role: 'Subject' },
            { src: vWord, dst: vNeb, role: 'Predicate Verb' },
            ...subRes.alignments
          ],
          success: true
        };
      }
    }

    // Indirect Question / Wh-clause: [Subject] [knows/sees/observes/asks/wonders] [who/what/where/when/why/how] [Clause]
    const whMatch = englishText.trim().match(/^([a-z]+)\s+(knows?|knew|sees?|saw|observes?|observed|asks?|asked|wonders?|wondered)\s+(who|what|where|when|why|how)\s+(.+)$/i);
    if (whMatch) {
      const [, sWord, vWord, whWord, subClause] = whMatch;
      const vMap = {
        know: 'Velsen', knows: 'Velsen', knew: 'Fe velsen',
        see: 'Vyrel', sees: 'Vyrel', saw: 'Fe vyrel',
        observe: 'Vyrel', observes: 'Vyrel', observed: 'Fe vyrel',
        ask: 'Fenor', asks: 'Fenor', asked: 'Fe fenor',
        wonder: 'Minpan', wonders: 'Minpan', wondered: 'Fe minpan'
      };
      const nMap = {
        i: 'mi', you: 'ti', we: 'miin', they: 'riin',
        he: 'taas', she: 'taas', it: 'tate'
      };
      const whNebMap = {
        who: 'kaas', what: 'kate', where: 'kauo', when: 'kahav', why: 'kazen', how: 'kaku'
      };
      const vNeb = vMap[vWord.toLowerCase()];
      const sNeb = nMap[sWord.toLowerCase()] || sWord.toLowerCase();
      const whNeb = whNebMap[whWord.toLowerCase()];
      const subRes = translateSingleEnglishClause(subClause);
      if (vNeb && whNeb && subRes.success) {
        const res = `${vNeb} el ${sNeb} ia ${whNeb} ${subRes.text.replace(/\.$/, '')}.`;
        return {
          text: res,
          neb: res,
          tag: 'Indirect Question / Wh-clause (SVO -> VSO wh-clause)',
          alignment: [
            { src: sWord, dst: 'el ' + sNeb, role: 'Subject' },
            { src: vWord, dst: vNeb, role: 'Predicate Verb' },
            { src: whWord, dst: 'ia ' + whNeb, role: 'Interrogative Complement' },
            ...subRes.alignments
          ],
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
        if(!/名/.test(c.pos||''))continue;
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
      know: 'belan', knows: 'belan', knew: 'fe belan',
      say: 'fenor', says: 'fenor', said: 'fe fenor',
      think: 'minpan', thinks: 'minpan', thought: 'fe minpan'
    };
    const adjectives = {
      beautiful: 'cylani', bright: 'faluni', dark: 'kyrin', warm: 'teirini',
      white: 'alin', pure: 'alin', silver: 'tyni', red: 'pyrin', astral: 'vyri',
      blue: 'kyrin', clear: 'kyrin', cyan: 'kyrin',
      green: 'zylin', verdant: 'zylin',
      flame: 'pyrin',
      gold: 'syvan', golden: 'syvan',
      emerald: 'eirin', fresh: 'eirin',
      silent: 'moran', calm: 'moran',
      deep: 'telin', profound: 'telin'
    };
    // Resolve adjective labels against the loaded dictionary. Historical fallback
    // tables contained color/size substitutions; ambiguity must not pick a root.
    const currentVocab=getVocabMap();
    if(currentVocab.size) {
      nouns.light='falun';
      for(const term of Object.keys(adjectives)) {
        const matches=[...currentVocab.values()].filter(w=>/形/.test(w.p||'')&&(w.en||'').toLowerCase().split(/[,;/]/).map(x=>x.trim()).includes(term));
        if(matches.length===1)adjectives[term]=matches[0].r;else delete adjectives[term];
      }
      Object.assign(verbs,{know:'velsen',knows:'velsen',knew:'fe velsen',write:'kiras',writes:'kiras',wrote:'fe kiras'});
      for(const term of ['think','thinks','thought','rest','rests','rested'])delete verbs[term];
    }
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
      from: 'va',
      than: 'va'
    };

    // Extract trailing prepositional phrases
    const prepPhrases = [];
    let currentRemainder = (objectText || '').trim();

    while (currentRemainder) {
      const ppMatch = currentRemainder.match(/(?:^|\s+)(more\s+than|than|to|with|in|at|for|from)\s+(?:(the|a|an)\s+)?(?:([a-z]+)\s+)?([a-z]+)$/i);
      if (ppMatch) {
        const [full, prep, art, mod, pNoun] = ppMatch;
        const nNeb = noun(pNoun);
        if (!nNeb) break;
        if (mod && !Object.hasOwn(adjectives, mod)) break;
        const adjNeb = mod ? adjectives[mod] : null;
        const normPrep = prep.toLowerCase().replace(/^more\s+/, '');
        const nebMarker = prepMap[normPrep];
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

  function conjugateJapaneseVerb(meaning, parsed, configuredKind) {
    const suffix = parsed.aspectSuffix && ['ast', 'ar', 'far', 'liv'].includes(parsed.aspectSuffix.suffix) ? parsed.aspectSuffix.suffix : '';
    const prefixes = [];
    prefixes.push(...parsed.prefixes.filter(p=>['fe','ne','di'].includes(p)));
    if (!suffix && !prefixes.length) return null;
    for (const lemma of glossList(meaning)) {
      const kind = configuredKind || dictionaryVerbKind(lemma);
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

