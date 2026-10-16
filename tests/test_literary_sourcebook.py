import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import literary_sourcebook as literary


class LiterarySourcebookChecks(unittest.TestCase):
    def setUp(self):
        self.book=json.loads((ROOT/'data/literary_sourcebook.json').read_text(encoding='utf-8'))

    def test_all_current_words_have_unique_source_backed_prose(self):
        words={w['nrs']:w for w in literary.words()}
        self.assertEqual(set(words),{r['root'] for r in self.book['entries']})
        self.assertEqual(1463,len({r['id'] for r in self.book['entries']}))
        self.assertEqual(4,len(self.book['works']))
        for row in self.book['entries']:
            self.assertEqual(literary.source_hash(words[row['root']]),row['sourceHash'])
            self.assertIn(row['root'],row['quote'])
            self.assertEqual('not-an-NRS-translation',row['translationStatus'])

    def test_append_keeps_existing_loci_and_editorial_changes(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);(root/'data').mkdir()
            book=copy.deepcopy(self.book)
            book['entries'][0]['quote']+=' 編集者の追記。'
            (root/'data/literary_sourcebook.json').write_text(json.dumps(book,ensure_ascii=False),encoding='utf-8')
            words=literary.words();new=copy.deepcopy(words[0]);new.update(id=99998,nrs='fixtureonlyroot')
            with patch.object(literary,'ROOT',root),patch.object(literary,'words',return_value=words+[new]):
                updated=literary.build_sourcebook()
                again=literary.build_sourcebook()
            self.assertEqual(updated,again)
            by_root={r['root']:r for r in updated['entries']}
            for row in book['entries']:self.assertEqual(row,by_root[row['root']])
            self.assertEqual('VL-99998',by_root[new['nrs']]['id'])

    def test_changed_meaning_requires_usage_review(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);(root/'data').mkdir()
            (root/'data/literary_sourcebook.json').write_text(json.dumps(self.book,ensure_ascii=False),encoding='utf-8')
            words=literary.words();words[0]['meaningJa']='意味を変更した検証用の値'
            with patch.object(literary,'ROOT',root),patch.object(literary,'words',return_value=words):
                with self.assertRaisesRegex(ValueError,'meaning changed'):literary.build_sourcebook()

    def test_reader_contains_each_exact_quote_and_anchor(self):
        from html import escape
        html=(ROOT/'web/library.html').read_text(encoding='utf-8')
        for row in self.book['entries']:
            self.assertIn('id="'+row['anchor']+'"',html)
            self.assertIn(escape(row['quote']),html)

    def test_bound_editions_and_original_appendices_exist(self):
        manifest=json.loads((ROOT/'audit/maintenance/codex-build-20261016.json').read_text(encoding='utf-8'))
        self.assertEqual(1463,manifest['literaryUsages'])
        self.assertEqual(30,manifest['corpusUnits'])
        for name in ['Valnes_Ibun','Valnes_saltwind','Valnes_glasswell','Valnes_lamptable']:
            self.assertTrue((ROOT/('docs/'+name+'.pdf')).read_bytes().startswith(b'%PDF'))
        self.assertEqual((ROOT/'docs/Valnes_Ibun.pdf').read_bytes(),(ROOT/'docs/Codex_Astrolith_Canon_Scripture.pdf').read_bytes())


if __name__=='__main__':unittest.main()
