import json
from pathlib import Path
import subprocess
import unittest
import zipfile

ROOT=Path(__file__).resolve().parents[1]


class OfflineTranslationChecks(unittest.TestCase):
    def test_packaged_frames_match_canonical_argument_rules(self):
        rules=json.loads((ROOT/'data/corpus_rules.json').read_text(encoding='utf-8'))['frames']
        with zipfile.ZipFile(ROOT/'studio/build/NebulithStudio.jar') as archive:
            records={}
            for line in archive.read('translation-frames.tsv').decode().splitlines():
                id_,required,allowed,passive=line.split('\t')
                records[id_]={'required':set(required.split(',')),'allowed':set(allowed.split(',')),
                              'passiveAllowed':set(filter(None,passive.split(',')))}
        self.assertEqual(set(rules),set(records))
        for id_,frame in rules.items():
            for key in ['required','allowed','passiveAllowed']:
                self.assertEqual(set(frame.get(key,[])),records[id_][key])

    def test_bidirectional_grammar_examples_and_safe_rejection_in_real_jvm(self):
        java=Path('C:/Program Files/Android/Android Studio/jbr/bin/java.exe')
        if not java.exists():self.skipTest('Local JDK not installed')
        result=subprocess.run([str(java),'-Dfile.encoding=UTF-8','-Djava.awt.headless=true','-jar',
            str(ROOT/'studio/build/NebulithStudio.jar'),'--translation-self-test'],
            cwd=ROOT,capture_output=True,text=True,encoding='utf-8',timeout=30)
        self.assertEqual(0,result.returncode,result.stdout+result.stderr)
        self.assertIn('PASS: offline translation 92 checks',result.stdout)


if __name__=='__main__':unittest.main()
