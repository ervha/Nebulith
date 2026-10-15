import json
import sys

with open('data/lexicon.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

vocab = d.get('vocabulary', [])
keywords = ['好', '愛', '望', '思', '知', '求', '願', '信', '感', '友', '心', '与', '送', '美']
hits = [w for w in vocab if any(k in w.get('meaningJa', '') for k in keywords)]

# print safely to utf-8 stdout
for h in hits:
    sys.stdout.buffer.write(f"{h.get('nrs')} ({h.get('pos')}): {h.get('meaningJa')} [{h.get('meaningEn')}] - notes: {h.get('notes', '')}\n".encode('utf-8'))
