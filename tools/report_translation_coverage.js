const fs=require('fs'),vm=require('vm'),path=require('path');
const root=path.resolve(__dirname,'..');
const ctx={};vm.createContext(ctx);
for(const f of ['web/data.js','web/incremental.js'])vm.runInContext(fs.readFileSync(path.join(root,f),'utf8'),ctx);
const coverage=vm.runInContext('createIncrementalTranslator(VOCAB,GRAMMAR_FRAMES,INPUT_RULES.aliases,[],TRANSLATION_EXTENSIONS).coverage()',ctx);
const lines=['# 日本語→Nebulithの変換範囲','','既存の正本文型を維持し、追加の項構造・活用・形容詞叙述をアプリ用の未監査案として実装しています。一般自由文翻訳の完成を意味しません。','',
`- 対応述語：${coverage.predicates}。生産的活用の日本語見出し：${coverage.productiveLemmas}。`,
`- 動詞の表層形：${coverage.verbForms}、形容詞の表層形：${coverage.adjectiveForms}、明示した場所語：${coverage.places}。`,
'- 主語・対象・所有・修飾・授受・起点・場所・道具・共同者を辞書から組み合わせます。',
'- 五段・一段・サ変・来るの現在／過去／否定／丁寧／進行／始動。希望・可能・推量などは対応する文型で候補を示し、利用者の確認後に確定します。必要性など未対応の意味は省略しません。',
'- 形容詞だけの叙述にNebulithのコピュラを補い、語義が複数なら選択後に確定します。',
'- 英語入力・Nebulithからの逆変換は登録対訳中心で、この対応数には含めません。','',
'## 生産的活用の見出し','','| 日本語 | NRS | 辞書ID |','| --- | --- | ---: |',
...coverage.verbs.map(v=>`| ${v.lemma} | ${v.root} | ${v.id} |`),
'','## 辞書にはあるが生成変換が未整備の動詞','','語義や活用を推測して自動採用せず、次の拡充対象として残します。','',
'| ID | NRS | 語義 | 未対応理由 |','| ---: | --- | --- | --- |',
...coverage.unsupportedVerbs.map(v=>`| ${v.id} | ${v.root} | ${v.meaning} | ${v.reason} |`),
'','## 複合形容詞の限定用法と保留','','| ID | 見出し | 対応範囲 |','| ---: | --- | --- |',
...(vm.runInContext('TRANSLATION_EXTENSIONS.roadmapProductive.adjectives',ctx)).map(a=>`| ${a.id} | ${a.lemma} | ${a.predicative?'修飾・叙述（否定・過去）':'修飾のみ。叙述は保留'} |`),
...vm.runInContext('TRANSLATION_EXTENSIONS.roadmapProductive.held',ctx).map(a=>`| ${a.id} | 語義・品詞の再整理待ち | ${a.reason} |`),
'','生成：`node tools/report_translation_coverage.js`。元データは `data/translation_patterns.json`、`data/compound_translation_patterns.json`、`data/roadmap_lexical_rules.json` とWeb翻訳エンジンです。追加文型は語義を限定したアプリ用案で、独立した言語審査の承認を意味しません。未整備動詞が0でも、各動詞の全語義・文型の網羅を意味しません。',''];
fs.writeFileSync(path.join(root,'docs/TRANSLATION_COVERAGE.md'),lines.join('\n'));
console.log(JSON.stringify({predicates:coverage.predicates,lemmas:coverage.productiveLemmas,verbForms:coverage.verbForms,adjectiveForms:coverage.adjectiveForms,places:coverage.places,unsupportedVerbs:coverage.unsupportedVerbs.length}));
