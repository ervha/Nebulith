"""Recheck and record the specific 30-unit review, bound to content and dependencies."""
import json
from nebulith_data import ROOT,dump,entry_hash,validate_corpus,corpus_markdown
from corpus_review import analyze_unit,dependency_hash


def main():
    corpus=json.loads((ROOT/'data/canon_corpus.json').read_text(encoding='utf-8'))
    vocab=json.loads((ROOT/'data/lexicon.json').read_text(encoding='utf-8'))['vocabulary']
    rules=json.loads((ROOT/'data/corpus_rules.json').read_text(encoding='utf-8'))
    batch=json.loads((ROOT/'data/audit/corpus_review_batch_30.json').read_text(encoding='utf-8'))
    assert len(corpus['units'])==30 and not validate_corpus(corpus,vocab)
    for unit in corpus['units']:
        analysis=analyze_unit(unit,vocab,rules)
        body={k:v for k,v in unit.items() if k not in ['review','syntaxReview']}
        if analysis['errors'] or batch['units'][unit['id']]!={'bodyHash':entry_hash(body),'dependencyHash':dependency_hash(unit,vocab,rules)}:
            raise ValueError('New semantic review required: '+unit['id'])
        unit['syntaxReview']=analysis
        unit['review'].update({'status':'approved','reviewer':'Codex','reviewType':'AI linguistic review',
           'criteriaVersion':rules['version'],'reviewedAgainstDependenciesHash':dependency_hash(unit,vocab,rules)})
        unit['review']['reviewedAgainstUnitHash']=entry_hash({k:v for k,v in unit.items() if k!='review'})
    dump(ROOT/'data/canon_corpus.json',corpus)
    path=ROOT/'docs/Project Requirements And Design.md';text=path.read_text(encoding='utf-8')
    path.write_text(text.split('<!-- BEGIN GENERATED CANON -->')[0]+corpus_markdown(corpus,vocab),encoding='utf-8')
    print('Reviewed 30 units; five supported predicates only, no general translation claim.')


if __name__=='__main__':main()
