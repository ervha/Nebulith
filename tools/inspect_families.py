# tools/inspect_families.py
import json

with open('data/lexicon.json', 'r', encoding='utf-8') as f:
    vocab = json.load(f)['vocabulary']

targets = ['tal', 'vel', 'ner', 'dom', 'fal', 'dar', 'val', 'ser', 'cel', 'fer']
with open('temp_inspect.txt', 'w', encoding='utf-8') as out:
    for t in targets:
        words = [w for w in vocab if w['nrs'].startswith(t)]
        out.write(f"\n=======================================================\n")
        out.write(f"=== Family: {t}* (Total: {len(words)}) ===\n")
        out.write(f"=======================================================\n")
        for w in words:
            out.write(f"  {w['nrs']:<14} | {w['pos']:<10} | {w['meaningJa']:<25} | {w['meaningEn']}\n")
