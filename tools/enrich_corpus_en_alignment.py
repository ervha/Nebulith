import json
import os

def enrich_corpus_with_en_and_alignment():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ext_path = os.path.join(base_dir, 'data', 'extended_corpus_v2.json')
    
    with open(ext_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Dictionary of alignments and english for each sentence ID
    enrichment = {
        "EXT-01": {
            "english": "I like you.",
            "english_variants": ["I love you.", "I really like you."],
            "alignment": [
                {"src": "私は", "src_en": "I", "dst": "el mi", "role": "主格 (Subject)", "meaning": "私 (I)"},
                {"src": "あなたが", "src_en": "you", "dst": "ia ti", "role": "対格 (Object)", "meaning": "あなた (you)"},
                {"src": "好きだ", "src_en": "like / love", "dst": "Cynel", "role": "述語動詞 (Verb)", "meaning": "愛する・好む (love/like)"}
            ]
        },
        "EXT-02": {
            "english": "I like the beautiful star.",
            "english_variants": ["I love the beautiful star."],
            "alignment": [
                {"src": "私は", "src_en": "I", "dst": "el mi", "role": "主格 (Subject)", "meaning": "私 (I)"},
                {"src": "好きだ", "src_en": "like", "dst": "Cynel", "role": "述語動詞 (Verb)", "meaning": "愛する・好む (love/like)"},
                {"src": "星を", "src_en": "the star", "dst": "ia vyr", "role": "対格名詞 (Object Noun)", "meaning": "星 (star)"},
                {"src": "美しい", "src_en": "beautiful", "dst": "cylani", "role": "後置形容詞 (Post-Adj)", "meaning": "美しい (beautiful)"}
            ]
        },
        "EXT-03": {
            "english": "I do not like darkness.",
            "english_variants": ["I don't like darkness.", "I do not love darkness."],
            "alignment": [
                {"src": "不 / ない", "src_en": "not", "dst": "Ne", "role": "否定辞 (Negative)", "meaning": "〜でない (not)"},
                {"src": "好きだ", "src_en": "like", "dst": "cynel", "role": "述語動詞 (Verb)", "meaning": "愛する・好む (love/like)"},
                {"src": "私は", "src_en": "I", "dst": "el mi", "role": "主格 (Subject)", "meaning": "私 (I)"},
                {"src": "暗闇が", "src_en": "darkness", "dst": "ia kym", "role": "対格 (Object)", "meaning": "闇・夜 (darkness)"}
            ]
        },
        "EXT-04": {
            "english": "I believe in you.",
            "english_variants": ["I trust you.", "I believe you."],
            "alignment": [
                {"src": "信じている", "src_en": "believe / trust", "dst": "Fevas", "role": "述語動詞 (Verb)", "meaning": "信託・信頼する (trust)"},
                {"src": "私は", "src_en": "I", "dst": "el mi", "role": "主格 (Subject)", "meaning": "私 (I)"},
                {"src": "あなたを", "src_en": "you", "dst": "ia ti", "role": "対格 (Object)", "meaning": "あなた (you)"}
            ]
        },
        "EXT-05": {
            "english": "The observer contemplates the spirit deeply.",
            "english_variants": ["The observer contemplates the soul.", "The observer meditates on the mind."],
            "alignment": [
                {"src": "深く考える", "src_en": "contemplates", "dst": "Memar", "role": "述語動詞 (Verb)", "meaning": "思索・熟慮する (contemplate)"},
                {"src": "観測者は", "src_en": "the observer", "dst": "el myren", "role": "主格 (Subject)", "meaning": "観測者・人間 (observer)"},
                {"src": "精神について", "src_en": "the spirit", "dst": "ia sylim", "role": "対格 (Object)", "meaning": "精神・心 (spirit)"}
            ]
        },
        "EXT-06": {
            "english": "We wish for peace.",
            "english_variants": ["We desire peace.", "We hope for peace."],
            "alignment": [
                {"src": "望む", "src_en": "wish / hope for", "dst": "Welin", "role": "述語動詞 (Verb)", "meaning": "希望する (hope)"},
                {"src": "私たちは", "src_en": "we", "dst": "el mia", "role": "主格複数 (Subject Plural)", "meaning": "私たち (we)"},
                {"src": "平和を", "src_en": "peace", "dst": "ia sirin", "role": "対格 (Object)", "meaning": "平穏・平和 (peace)"}
            ]
        },
        "EXT-07": {
            "english": "I send a message to you.",
            "english_variants": ["I transmit a signal to you.", "I send communication to you."],
            "alignment": [
                {"src": "送る", "src_en": "send / transmit", "dst": "Wesan", "role": "述語動詞 (Verb)", "meaning": "送信する (send)"},
                {"src": "私は", "src_en": "I", "dst": "el mi", "role": "主格 (Subject)", "meaning": "私 (I)"},
                {"src": "通信を", "src_en": "a message", "dst": "ia tolas", "role": "対格 (Object)", "meaning": "通信・メッセージ (message)"},
                {"src": "あなたに", "src_en": "to you", "dst": "to ti", "role": "方向格 (Direction)", "meaning": "あなたへ (to you)"}
            ]
        },
        "EXT-08": {
            "english": "He gives light to me.",
            "english_variants": ["She gives light to me."],
            "alignment": [
                {"src": "与える", "src_en": "gives", "dst": "Zelvan", "role": "述語動詞 (Verb)", "meaning": "授与する (give/bestow)"},
                {"src": "彼は", "src_en": "he / she", "dst": "el ri", "role": "主格 (Subject)", "meaning": "彼／彼女 (he/she)"},
                {"src": "光を", "src_en": "light", "dst": "ia falun", "role": "対格 (Object)", "meaning": "光 (light)"},
                {"src": "私に", "src_en": "to me", "dst": "to mi", "role": "方向格 (Direction)", "meaning": "私へ (to me)"}
            ]
        },
        "EXT-09": {
            "english": "I observe the star, but you walk to the house.",
            "english_variants": ["I watch the star, but you walk home."],
            "alignment": [
                {"src": "私は星を観測する", "src_en": "I observe the star", "dst": "Vyrel el mi ia vyr", "role": "第1節 (Clause 1)", "meaning": "私は星を観測する"},
                {"src": "が / しかし", "src_en": "but", "dst": "hav", "role": "逆接接続詞 (Conjunction)", "meaning": "しかし (but)"},
                {"src": "あなたは家へ歩く", "src_en": "you walk to the house", "dst": "poran el ti to govan", "role": "第2節 (Clause 2)", "meaning": "あなたは家へ歩く"}
            ]
        },
        "EXT-10": {
            "english": "Because the star shines, the night is beautiful.",
            "english_variants": ["The night is beautiful because the star shines."],
            "alignment": [
                {"src": "〜だから", "src_en": "because", "dst": "Sen", "role": "原因接続詞 (Because)", "meaning": "〜なので (because)"},
                {"src": "星が輝く", "src_en": "the star shines", "dst": "falun el vyr", "role": "原因節 (Reason Clause)", "meaning": "星が光る"},
                {"src": "夜は美しい", "src_en": "the night is beautiful", "dst": "cylani el valar", "role": "主節 (Main Clause)", "meaning": "夜は美しい"}
            ]
        },
        "EXT-11": {
            "english": "The star shines constantly.",
            "english_variants": ["The star always shines."],
            "alignment": [
                {"src": "輝く", "src_en": "shines", "dst": "Falun", "role": "述語動詞 (Verb)", "meaning": "光る・輝く (shine)"},
                {"src": "常に", "src_en": "constantly / always", "dst": "eirinu", "role": "様態副詞 (Adverb)", "meaning": "絶え間なく・常に (constantly)"},
                {"src": "星は", "src_en": "the star", "dst": "el vyr", "role": "主格 (Subject)", "meaning": "星 (star)"}
            ]
        },
        "EXT-12": {
            "english": "I have a close friend.",
            "english_variants": ["I have a confidant.", "There is a friend for me."],
            "alignment": [
                {"src": "いる / 持つ", "src_en": "have / there is", "dst": "Relen", "role": "所有存在コピュラ (Copula)", "meaning": "存在する・持つ (exist/have)"},
                {"src": "私には", "src_en": "I / for me", "dst": "el mi", "role": "主格 (Subject)", "meaning": "私 (I)"},
                {"src": "親友が", "src_en": "a close friend", "dst": "ia cynor", "role": "対格 (Object)", "meaning": "親友・盟友 (confidant)"}
            ]
        },
        "EXT-13": {
            "english": "If the star shines, I walk.",
            "english_variants": ["If the star shines, I will walk."],
            "alignment": [
                {"src": "もし〜なら", "src_en": "if", "dst": "Zen", "role": "条件接続詞 (If)", "meaning": "もし〜なら (if)"},
                {"src": "星が輝く", "src_en": "the star shines", "dst": "falun el vyr", "role": "条件節 (Condition Clause)", "meaning": "星が輝く"},
                {"src": "私は歩く", "src_en": "I walk", "dst": "poran el mi", "role": "帰結節 (Consequence Clause)", "meaning": "私は歩く"}
            ]
        },
        "EXT-14": {
            "english": "If you like me, I am happy.",
            "english_variants": ["If you love me, I am glad."],
            "alignment": [
                {"src": "もし〜なら", "src_en": "if", "dst": "Zen", "role": "条件接続詞 (If)", "meaning": "もし〜なら (if)"},
                {"src": "あなたが私を好き", "src_en": "you like me", "dst": "cynel el ti ia mi", "role": "条件節 (Condition Clause)", "meaning": "あなたが私を愛する"},
                {"src": "私は嬉しい", "src_en": "I am happy", "dst": "relen el mi ia elir", "role": "帰結節 (Consequence Clause)", "meaning": "私は喜びに満ちる"}
            ]
        },
        "EXT-15": {
            "english": "The star is more beautiful than the night.",
            "english_variants": ["Stars are more beautiful than night."],
            "alignment": [
                {"src": "美しい", "src_en": "beautiful", "dst": "Cylani", "role": "述語形容詞 (Adj Predicate)", "meaning": "美しい (beautiful)"},
                {"src": "星は", "src_en": "the star", "dst": "el vyr", "role": "主格 (Subject)", "meaning": "星 (star)"},
                {"src": "夜よりも", "src_en": "than the night", "dst": "va valar", "role": "奪格比較 (Ablative Comparison)", "meaning": "夜より (than night)"}
            ]
        },
        "EXT-16": {
            "english": "The sun shines more than the star.",
            "english_variants": ["The sun is brighter than the star."],
            "alignment": [
                {"src": "光る", "src_en": "shines", "dst": "Falun", "role": "述語動詞 (Verb)", "meaning": "光る (shine)"},
                {"src": "太陽は", "src_en": "the sun", "dst": "el zohar", "role": "主格 (Subject)", "meaning": "太陽 (sun)"},
                {"src": "星よりも", "src_en": "than the star", "dst": "va vyr", "role": "奪格比較 (Ablative Comparison)", "meaning": "星より (than star)"}
            ]
        },
        "EXT-17": {
            "english": "Who are you?",
            "english_variants": ["Who are you?"],
            "alignment": [
                {"src": "ある / です", "src_en": "are", "dst": "Relen", "role": "コピュラ (Copula)", "meaning": "〜である (be)"},
                {"src": "あなたは", "src_en": "you", "dst": "el ti", "role": "主格 (Subject)", "meaning": "あなた (you)"},
                {"src": "誰", "src_en": "who", "dst": "ia keli", "role": "疑問代名詞 (Interrogative)", "meaning": "誰 (who)"},
                {"src": "か？", "src_en": "?", "dst": "ka?", "role": "疑問小辞 (Question Particle)", "meaning": "疑問符 (?)"}
            ]
        },
        "EXT-18": {
            "english": "What is this?",
            "english_variants": ["What is this?"],
            "alignment": [
                {"src": "ある / です", "src_en": "is", "dst": "Relen", "role": "コピュラ (Copula)", "meaning": "〜である (be)"},
                {"src": "これは", "src_en": "this", "dst": "el celen", "role": "近称指示代名詞 (Pronoun)", "meaning": "これ (this)"},
                {"src": "何", "src_en": "what", "dst": "ia kelen", "role": "疑問代名詞 (Interrogative)", "meaning": "何 (what)"},
                {"src": "か？", "src_en": "?", "dst": "ka?", "role": "疑問小辞 (Question Particle)", "meaning": "疑問符 (?)"}
            ]
        },
        "EXT-19": {
            "english": "Where do you walk to?",
            "english_variants": ["Where are you walking?"],
            "alignment": [
                {"src": "歩く", "src_en": "walk", "dst": "Poran", "role": "述語動詞 (Verb)", "meaning": "歩く (walk)"},
                {"src": "あなたは", "src_en": "you", "dst": "el ti", "role": "主格 (Subject)", "meaning": "あなた (you)"},
                {"src": "どこへ", "src_en": "to where", "dst": "to kauo", "role": "方向疑問格 (Direction Where)", "meaning": "どこへ (where to)"},
                {"src": "か？", "src_en": "?", "dst": "ka?", "role": "疑問小辞 (Question Particle)", "meaning": "疑問符 (?)"}
            ]
        },
        "EXT-20": {
            "english": "Walk to the house!",
            "english_variants": ["Walk home!"],
            "alignment": [
                {"src": "歩け", "src_en": "Walk", "dst": "Poran", "role": "命令動詞 (Imperative Verb)", "meaning": "歩く (walk)"},
                {"src": "家へ", "src_en": "to the house", "dst": "to govan", "role": "方向格 (Direction)", "meaning": "家へ (to house)"},
                {"src": "なさい！", "src_en": "!", "dst": "lo!", "role": "命令小辞 (Imperative Particle)", "meaning": "〜せよ (!)"}
            ]
        },
        "EXT-21": {
            "english": "Let us observe the star!",
            "english_variants": ["Let's observe the star!"],
            "alignment": [
                {"src": "観測しよう", "src_en": "Let us observe", "dst": "Vyrel", "role": "動詞 (Verb)", "meaning": "観測する (observe)"},
                {"src": "私たちは", "src_en": "we", "dst": "el mia", "role": "主格複数 (Subject)", "meaning": "私たち (we)"},
                {"src": "星を", "src_en": "the star", "dst": "ia vyr", "role": "対格 (Object)", "meaning": "星 (star)"},
                {"src": "！", "src_en": "!", "dst": "lo!", "role": "勧誘小辞 (Cohortative)", "meaning": "〜しよう (!)"}
            ]
        },
        "EXT-22": {
            "english": "The star shines in the night sky. I like you.",
            "english_variants": ["The star shines in the night. I love you."],
            "alignment": [
                {"src": "星が夜空で輝く。", "src_en": "The star shines in the night sky.", "dst": "Falun el vyr uo valar.", "role": "第1文 (Sent 1)", "meaning": "星が夜空で輝く"},
                {"src": "私はあなたが好きです。", "src_en": "I like you.", "dst": "Cynel el mi ia ti.", "role": "第2文 (Sent 2)", "meaning": "私はあなたを好む"}
            ]
        },
        "EXT-23": {
            "english": "The night is beautiful. Because the star shines, I walk. I believe in you.",
            "english_variants": ["The night is beautiful. As the star shines, I walk. I trust you."],
            "alignment": [
                {"src": "夜は美しい。", "src_en": "The night is beautiful.", "dst": "Cylani el valar.", "role": "第1文 (Sent 1)", "meaning": "夜は美しい"},
                {"src": "星が輝くから、私は歩く。", "src_en": "Because the star shines, I walk.", "dst": "Sen falun el vyr, poran el mi.", "role": "第2文 (Sent 2)", "meaning": "星が輝くから私は歩く"},
                {"src": "私はあなたを信じている。", "src_en": "I believe in you.", "dst": "Fevas el mi ia ti.", "role": "第3文 (Sent 3)", "meaning": "私はあなたを信じている"}
            ]
        }
    }

    for s in data['sentences']:
        sid = s['id']
        if sid in enrichment:
            s['english'] = enrichment[sid]['english']
            s['english_variants'] = enrichment[sid]['english_variants']
            s['alignment'] = enrichment[sid]['alignment']

    with open(ext_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Enriched extended corpus with English and alignments.")

if __name__ == '__main__':
    enrich_corpus_with_en_and_alignment()
