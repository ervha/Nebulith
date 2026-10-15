import json

with open('data/lexicon.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

vocab = d.get('vocabulary', [])
if vocab:
    print("Keys of first entry:", list(vocab[0].keys()))
    print("Sample:", {k: vocab[0][k] for k in list(vocab[0].keys())[:6]})
