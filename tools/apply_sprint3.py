# -*- coding: utf-8 -*-
import re

with open('web/incremental.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Target part() after quote handling to add adverb handling
target = '''      // --- Superlative Prefix Handling (最も / 一番) ---
      let isSuperlative = false;
      if (/(最も|一番)/.test(cleanSource)) {
        cleanSource = cleanSource.replace(/(最も|一番)[\\s\\u3000]*/g, '');
        isSuperlative = true;
      }'''

replacement = '''      // --- Superlative Prefix Handling (最も / 一番) ---
      let isSuperlative = false;
      if (/(最も|一番)/.test(cleanSource)) {
        cleanSource = cleanSource.replace(/(最も|一番)[\\s\\u3000]*/g, '');
        isSuperlative = true;
      }

      // --- Adverb Modification Handling (時間・頻度・程度・様態) ---
      const adverbList = [
        { ja: 'いつも', neb: 'havon', role: '頻度副詞（恒常）' },
        { ja: '常に', neb: 'havon', role: '頻度副詞（恒常）' },
        { ja: '時々', neb: 'havtul', role: '頻度副詞（断続）' },
        { ja: 'たまに', neb: 'havtul', role: '頻度副詞（断続）' },
        { ja: 'すでに', neb: 'feval', role: '時間副詞（完了）' },
        { ja: 'もう', neb: 'feval', role: '時間副詞（完了）' },
        { ja: 'まだ', neb: 'divan', role: '時間副詞（継続）' },
        { ja: 'すぐに', neb: 'tasik', role: '時間副詞（即時）' },
        { ja: '直ちに', neb: 'tasik', role: '時間副詞（即時）' },
        { ja: 'とても', neb: 'solpar', role: '程度副詞（極大）' },
        { ja: '非常に', neb: 'solpar', role: '程度副詞（極大）' },
        { ja: 'たいへん', neb: 'solpar', role: '程度副詞（極大）' },
        { ja: '少し', neb: 'vyntul', role: '程度副詞（極小）' },
        { ja: 'わずかに', neb: 'vyntul', role: '程度副詞（極小）' },
        { ja: '全く', neb: 'narval', role: '程度副詞（全否定）' },
        { ja: 'かなり', neb: 'radon', role: '程度副詞（中庸）' },
        { ja: 'ゆっくり', neb: 'moril', role: '様態副詞（緩慢）' },
        { ja: '早く', neb: 'tasin', role: '様態副詞（迅速）' },
        { ja: '速く', neb: 'tasin', role: '様態副詞（迅速）' },
        { ja: '静かに', neb: 'sirik', role: '様態副詞（沈黙）' },
        { ja: '共に', neb: 'kulen', role: '様態副詞（協調）' },
        { ja: '一緒に', neb: 'kulen', role: '様態副詞（協調）' },
        { ja: '独りで', neb: 'minkir', role: '様態副詞（単独）' }
      ];

      let matchedAdverb = null;
      if (depth === 0) {
        for (const adv of adverbList) {
          if (cleanSource.includes(adv.ja)) {
            // Remove adverb from cleanSource
            cleanSource = cleanSource.replace(new RegExp(adv.ja + '[\\\\s\\\\u3000]*'), '');
            matchedAdverb = adv;
            break;
          }
        }
      }'''

if target in code:
    code = code.replace(target, replacement)
    print('1. Added adverb detection logic to part()')
else:
    print('1. Target not found for adverb detection!')

# Target the end of part() to wrap result with matchedAdverb
end_pattern = r'(\s+)(return \{source,text:candidate,state:choices\.confirmed\?\'complete\':\'candidate\',candidate,meaning,senseOptions,verbOptions,alignment,notes:\[\.\.\.notes,\'Nebulithの格・項構造を検証。解釈を確認して確定してください。\'(?:,\.\.\.extensionNotes\(form\))?\]\};)'

def repl_end(m):
    indent = m.group(1)
    original_return = m.group(2)
    return f'''{indent}if (matchedAdverb) {{
{indent}  const advPrefix = matchedAdverb.neb[0].toUpperCase() + matchedAdverb.neb.slice(1);
{indent}  const bareCandidate = candidate.replace(/^[A-Z]/, c => c.toLowerCase());
{indent}  const fullCandidate = advPrefix + ' ' + bareCandidate;
{indent}  alignment = [
{indent}    {{ src: matchedAdverb.ja, dst: matchedAdverb.neb, role: matchedAdverb.role }},
{indent}    ...alignment
{indent}  ];
{indent}  return {{
{indent}    source,
{indent}    text: fullCandidate,
{indent}    state: 'complete',
{indent}    candidate: fullCandidate,
{indent}    meaning: {{ ...meaning, adverb: matchedAdverb }},
{indent}    senseOptions,
{indent}    verbOptions,
{indent}    alignment,
{indent}    notes: [...notes, matchedAdverb.ja + '（' + matchedAdverb.role + '）の副詞修飾を適用。']
{indent}  }};
{indent}}}
{indent}{original_return}'''

code = re.sub(end_pattern, repl_end, code)

# Also handle direct = full(cleanSource) with adverb
direct_target = '''      const direct=full(cleanSource);if(direct) {
        let dText = direct.text;
        let dAlign = direct.alignment || [];
        if (isSuperlative) {
          dText = dText.replace(/^((?:(?:Fe|Se|Ne|Di)\\s+)*)([a-zA-Z]+)/i, (m, prefixes, verb) => {
            return prefixes + 'cel' + verb.toLowerCase();
          });
          dText = dText[0].toUpperCase() + dText.slice(1);
          dAlign = [{src: '最も', dst: 'cel-', role: '最上級'}, ...dAlign];
        }
        return {...direct, text: dText, candidate: dText, alignment: dAlign, source};
      }'''

direct_replacement = '''      const direct=full(cleanSource);if(direct) {
        let dText = direct.text;
        let dAlign = direct.alignment || [];
        if (isSuperlative) {
          dText = dText.replace(/^((?:(?:Fe|Se|Ne|Di)\\s+)*)([a-zA-Z]+)/i, (m, prefixes, verb) => {
            return prefixes + 'cel' + verb.toLowerCase();
          });
          dText = dText[0].toUpperCase() + dText.slice(1);
          dAlign = [{src: '最も', dst: 'cel-', role: '最上級'}, ...dAlign];
        }
        if (matchedAdverb) {
          const advPrefix = matchedAdverb.neb[0].toUpperCase() + matchedAdverb.neb.slice(1);
          dText = advPrefix + ' ' + dText.replace(/^[A-Z]/, c => c.toLowerCase());
          dAlign = [{src: matchedAdverb.ja, dst: matchedAdverb.neb, role: matchedAdverb.role}, ...dAlign];
        }
        return {...direct, text: dText, candidate: dText, alignment: dAlign, source};
      }'''

if direct_target in code:
    code = code.replace(direct_target, direct_replacement)
    print('2. Added adverb handling to direct = full(cleanSource)')
else:
    print('2. direct_target not found!')

with open('web/incremental.js', 'w', encoding='utf-8') as f:
    f.write(code)
print('SUCCESS: Updated web/incremental.js for Sprint 3 adverbs')
