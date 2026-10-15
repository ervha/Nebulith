import json
import os
import re

def update_web_studio():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ext_path = os.path.join(base_dir, 'data', 'extended_corpus_v2.json')
    
    with open(ext_path, 'r', encoding='utf-8') as f:
        ext_data = json.load(f)

    # Enrich variants for all extended sentences
    for s in ext_data['sentences']:
        sid = s['id']
        variants = set(s.get('japanese_variants', []))
        variants.add(s['japanese'])
        
        if sid == 'EXT-01': # 好き
            variants.update(['私はあなたが好きだ。', '私はあなたが好きです。', '私はあなたが好き。', '私はあなたを愛する。', '私はあなたを愛しています。', '私はあなたを愛している。', '私はあなたを愛します。'])
        elif sid == 'EXT-02': # 美しい星が好き
            variants.update(['私は美しい星が好きだ。', '私は美しい星が好きです。', '私は美しい星が好き。', '私は美しい星を愛する。', '私は美しい星を愛している。'])
        elif sid == 'EXT-03': # 暗闇が好きではない
            variants.update(['私は暗闇が好きではない。', '私は暗闇が好きではありません。', '私は闇が好きではない。', '私は闇を愛さない。', '私は暗闇を好まない。'])
        elif sid == 'EXT-04': # 信じる
            variants.update(['私はあなたを信じている。', '私はあなたを信じています。', '私はあなたを信じる。', '私はあなたを信頼する。', '私はあなたを信頼している。', '私はあなたを信頼しています。'])
        elif sid == 'EXT-05': # 考える
            variants.update(['観測者は精神について深く考える。', '観測者は精神について深く思索する。', '観測者は精神を熟慮する。', '観測者は魂について思索する。'])
        elif sid == 'EXT-06': # 望む
            variants.update(['私たちは平和を望む。', '私たちは平和を望みます。', '私たちは平穏を望む。', '私たちは平穏を望みます。', '私たちは平和を願う。', '私たちは平和を願います。'])
        elif sid == 'EXT-07': # 送る
            variants.update(['私はあなたに通信を送る。', '私はあなたに通信を送ります。', '私はあなたへ通信を送る。', '私はあなたに通信を送信する。', '私はあなたに通信を送信します。'])
        elif sid == 'EXT-08': # 与える
            variants.update(['彼は私に光を与える。', '彼は私に光を与えます。', '彼は私に光を授ける。', '彼は私に光を授けます。', '彼女は私に光を与える。', '彼女は私に光を与えます。'])
        elif sid == 'EXT-09': # 逆接複文
            variants.update(['私は星を観測するが、あなたは家へ歩く。', '私は星を観測しますが、あなたは家へ歩きます。', '私は星を観測するが、あなたは家へ歩きます。'])
        elif sid == 'EXT-10': # 理由複文
            variants.update(['星が輝くから、夜は美しい。', '星が輝くので、夜は美しい。', '星が輝くから、夜は美しいです。', '星が輝くので、夜は美しいです。'])
        elif sid == 'EXT-11': # 副詞修飾
            variants.update(['星は常に輝く。', '星は常に輝きます。', '星は絶え間なく輝く。', '星はいつでも光る。', '星は常に光る。'])
        elif sid == 'EXT-12': # 所有
            variants.update(['私には親友がいる。', '私には親友がいます。', '私には友がいる。', '私には友がいます。', '私は親友を持つ。'])
        
        s['japanese_variants'] = sorted(list(variants))

    with open(ext_path, 'w', encoding='utf-8') as f:
        json.dump(ext_data, f, ensure_ascii=False, indent=2)
    print("Extended corpus variants enriched successfully.")

if __name__ == '__main__':
    update_web_studio()
