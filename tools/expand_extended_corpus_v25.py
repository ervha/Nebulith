import json
import os

def expand_extended_corpus():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ext_path = os.path.join(base_dir, 'data', 'extended_corpus_v2.json')
    
    with open(ext_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    existing_sentences = data['sentences']
    new_sentences = [
        {
            "id": "EXT-13",
            "category": "conditional_action",
            "japanese": "星が輝くなら、私は歩く。",
            "japanese_variants": ["星が輝くなら、私は歩きます。", "星が光るなら、私は歩く。", "星が光るなら、私は歩きます。"],
            "nebulith": "Zen falun el vyr, poran el mi.",
            "literal": "もし 輝く [主格] 星, 歩く [主格] 私",
            "structure": "Zen Clause1, Clause2 (条件節)"
        },
        {
            "id": "EXT-14",
            "category": "conditional_emotion",
            "japanese": "あなたが私を好きなら、私は嬉しいです。",
            "japanese_variants": ["あなたが私を好きなら、私は嬉しい。", "あなたが私を愛するなら、私は嬉しいです。"],
            "nebulith": "Zen cynel el ti ia mi, relen el mi ia elir.",
            "literal": "もし 愛する [主格] あなた [対格] 私, ある [主格] 私 [対格] 喜び",
            "structure": "Zen VSO1, VSO2 (条件節 + コピュラ感情)"
        },
        {
            "id": "EXT-15",
            "category": "comparative_adj",
            "japanese": "星は夜よりも美しい。",
            "japanese_variants": ["星は夜より美しいです。", "星は夜より美しい。"],
            "nebulith": "Cylani el vyr va valar.",
            "literal": "美しい [主格] 星 [奪格:〜より] 夜",
            "structure": "Adj el S va O (奪格比較構文)"
        },
        {
            "id": "EXT-16",
            "category": "comparative_verb",
            "japanese": "太陽は星よりも光る。",
            "japanese_variants": ["太陽は星より光ります。", "太陽は星よりも輝く。"],
            "nebulith": "Falun el zohar va vyr.",
            "literal": "光る [主格] 太陽 [奪格:〜より] 星",
            "structure": "V el S va O (動詞奪格比較構文)"
        },
        {
            "id": "EXT-17",
            "category": "interrogative_who",
            "japanese": "あなたは誰ですか？",
            "japanese_variants": ["お前は誰だ？", "あなたは誰？", "あなたは誰ですか。"],
            "nebulith": "Relen el ti ia keli ka?",
            "literal": "ある [主格] あなた [対格] 誰 [疑問詞]",
            "structure": "Relen el ti ia keli ka? (疑問詞疑問文: 誰)"
        },
        {
            "id": "EXT-18",
            "category": "interrogative_what",
            "japanese": "これは何ですか？",
            "japanese_variants": ["これは何？", "これは何だ？", "これは何ですか。"],
            "nebulith": "Relen el celen ia kelen ka?",
            "literal": "ある [主格] これ [対格] 何 [疑問詞]",
            "structure": "Relen el celen ia kelen ka? (疑問詞疑問文: 何)"
        },
        {
            "id": "EXT-19",
            "category": "interrogative_where",
            "japanese": "あなたはどこへ歩きますか？",
            "japanese_variants": ["お前はどこへ歩くのか？", "どこへ歩きますか？"],
            "nebulith": "Poran el ti to kauo ka?",
            "literal": "歩く [主格] あなた [方向格] どこ [疑問詞]",
            "structure": "Poran el ti to kauo ka? (疑問詞疑問文: どこ)"
        },
        {
            "id": "EXT-20",
            "category": "imperative_command",
            "japanese": "家へ歩きなさい。",
            "japanese_variants": ["家へ歩け。", "家へ歩いてください。"],
            "nebulith": "Poran to govan lo!",
            "literal": "歩く [方向格] 家 [命令詞]",
            "structure": "V to Dir lo! (命令構文)"
        },
        {
            "id": "EXT-21",
            "category": "imperative_cohortative",
            "japanese": "星を観測しよう。",
            "japanese_variants": ["星を観測しましょう。"],
            "nebulith": "Vyrel el mia ia vyr lo!",
            "literal": "観測する [主格] 私たち [対格] 星 [勧誘詞]",
            "structure": "V el mia ia O lo! (勧誘構文)"
        },
        {
            "id": "EXT-22",
            "category": "long_passage_2sent",
            "japanese": "星が夜空で輝く。私はあなたが好きです。",
            "japanese_variants": ["星が夜空で輝く。私はあなたが好きだ。"],
            "nebulith": "Falun el vyr uo valar. Cynel el mi ia ti.",
            "literal": "光る [主格] 星 [処格] 夜. 愛する [主格] 私 [対格] あなた",
            "structure": "2-Sentence Paragraph (単文 + VSO感情)"
        },
        {
            "id": "EXT-23",
            "category": "long_passage_3sent",
            "japanese": "夜は美しい。星が輝くから、私は歩く。私はあなたを信じている。",
            "japanese_variants": ["夜は美しい。星が輝くから、私は歩きます。私はあなたを信じています。"],
            "nebulith": "Cylani el valar. Sen falun el vyr, poran el mi. Fevas el mi ia ti.",
            "literal": "美しい [主格] 夜. 〜だから 輝く 星, 歩く 私. 信じる 私 あなた",
            "structure": "3-Sentence Complex Passage (形容述語 + 理由複文 + VSO)"
        }
    ]

    all_sentences = existing_sentences + new_sentences
    data['sentences'] = all_sentences
    data['name'] = "Nebulith Advanced Target Corpus v2.5"
    data['description'] = "感情・認識・授受・条件節・比較級・疑問詞・命令法・長文段落を含む総合構文セット (23例文)"

    with open(ext_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Expanded extended corpus to {len(all_sentences)} sentences.")

if __name__ == '__main__':
    expand_extended_corpus()
