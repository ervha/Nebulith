import copy,json,re,sys,unittest
from pathlib import Path
from urllib.parse import unquote
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from earth_scope import coverage,senses
from nebulith_data import entry_hash,corpus_semantic_pending,validate_corpus
from earth_comparison import load_and_compare


class DevelopmentChecks(unittest.TestCase):
    def test_scope_requires_all_senses_languages_and_minimum_forms(self):
        entry={'id':1,'meaningEn':'star, light','meaningJa':'星、光'}
        languages=['en','la','fr','es','de','ja']
        rows=[{'conceptId':'a','language':l,'comparisonForm':'word'} for l in languages]
        link={'lexiconId':1,'conceptId':'a','decision':'approved','reviewedSenses':sorted(senses(entry))}
        review={'lexiconId':1,'decision':'approved','entryHash':entry_hash(entry),'reviewer':'fixture','reason':'fixture',
                'senses':[{'label':s,'conceptIds':['a']} for s in senses(entry)]}
        policy={'requiredLanguages':languages,'minimumComparisonForms':6}
        args=([entry],rows,{'entries':[link]},policy,{'entries':[review]})
        self.assertTrue(coverage(*args)['scopeComplete'])
        incomplete=copy.deepcopy(review);incomplete['senses'].pop()
        self.assertFalse(coverage([entry],rows,{'entries':[link]},policy,{'entries':[incomplete]})['scopeComplete'])
        self.assertFalse(coverage([entry],rows[:-1],{'entries':[link]},policy,{'entries':[review]})['scopeComplete'])
        self.assertFalse(coverage([entry],rows,{'entries':[link]},{**policy,'minimumComparisonForms':7},{'entries':[review]})['scopeComplete'])

    def test_research_batch_is_partial_and_bound_to_entries(self):
        vocab=json.loads((ROOT/'data/lexicon.json').read_text(encoding='utf-8'))['vocabulary']
        by_id={r['id']:r for r in vocab}
        batch=json.loads((ROOT/'data/audit/earth_research_batch_01.json').read_text(encoding='utf-8'))
        self.assertEqual(50,len(batch['entries']))
        for row in batch['entries']:self.assertEqual(entry_hash(by_id[row['lexiconId']]),row['entryHash'])
        result=load_and_compare(vocab)
        self.assertFalse(result['scope_complete'])
        self.assertEqual(116,result['partially_reviewed_entry_count'])
        self.assertEqual([],result['errors']);self.assertEqual([],result['pending'])
        self.assertEqual('kyrven',by_id[37]['nrs']);self.assertEqual('neburil',by_id[38]['nrs'])

    def test_thirty_reviewed_examples_are_unique_and_valid(self):
        corpus=json.loads((ROOT/'data/canon_corpus.json').read_text(encoding='utf-8'))
        vocab=json.loads((ROOT/'data/lexicon.json').read_text(encoding='utf-8'))['vocabulary']
        self.assertEqual(30,len(corpus['units']))
        self.assertEqual(30,len({u['nrs'] for u in corpus['units']}))
        self.assertEqual([],validate_corpus(corpus,vocab));self.assertEqual([],corpus_semantic_pending(corpus))
        self.assertTrue(any(c['question'] for u in corpus['units'] for c in u['syntaxReview']['clauses']))

    def test_current_document_links(self):
        for path in [ROOT/'README.md',*(ROOT/'docs').glob('*.md')]:
            for href in re.findall(r'\]\(([^)]+)\)',path.read_text(encoding='utf-8')):
                if '://' not in href and not href.startswith('#'):
                    self.assertTrue((path.parent/unquote(href).split('#')[0]).exists(),(path,href))

    def test_web_bundle_matches_current_sources(self):
        from verify_web_bundle import verify
        result=verify();self.assertEqual(1008,result['rootEntries']);self.assertGreater(result['entries'],1008);self.assertEqual(30,result['examples'])
