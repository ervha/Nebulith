import contextlib
import hashlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

from fontTools.pens.recordingPen import RecordingPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from build_font import build_font
from font_symbols import SYMBOLS


class FontSymbolChecks(unittest.TestCase):
    def setUp(self):
        self.font = TTFont(ROOT / 'fonts/Nebulith-Regular.ttf')
        self.cmap = self.font.getBestCmap()

    def test_every_symbol_and_alias_is_mapped_to_a_drawn_glyph(self):
        for name, chars, _, advance in SYMBOLS:
            for char in chars:
                self.assertEqual(name, self.cmap[ord(char)], char)
            self.assertGreater(self.font['glyf'][name].numberOfContours, 0, name)
            self.assertEqual(advance, self.font['hmtx'][name][0])

    def test_existing_glyph_outlines_and_spacing_are_preserved(self):
        old = TTFont(ROOT / 'audit/runs/2026-10-15-glyphs-v2.5/before/Nebulith-Regular-v2.4.ttf')
        prior = json.loads((ROOT / 'audit/runs/2026-10-15-glyphs-v2.5/before/glyph_reviews.json').read_text(encoding='utf-8'))
        expected_changes = {r['glyph'] for r in prior['entries'] if r['decision']=='pending'}-{'space'}
        old_set, new_set = old.getGlyphSet(), self.font.getGlyphSet()
        for name in old.getGlyphOrder():
            a, b = RecordingPen(), RecordingPen()
            old_set[name].draw(a)
            new_set[name].draw(b)
            if name in expected_changes:
                self.assertNotEqual(a.value, b.value, name)
            else:
                self.assertEqual(a.value, b.value, name)
            self.assertEqual(old['hmtx'][name], self.font['hmtx'][name], name)
        for code, name in old.getBestCmap().items():
            self.assertEqual(name, self.cmap[code])

    def test_current_corpus_has_no_missing_punctuation(self):
        corpus = json.loads((ROOT / 'data/canon_corpus.json').read_text(encoding='utf-8'))
        for unit in corpus['units']:
            self.assertEqual([], [c for c in unit['nrs'] if ord(c) not in self.cmap])

    def test_phonemic_apostrophe_and_quotes_remain_distinct(self):
        self.assertEqual('quotesingle', self.cmap[ord("'")])
        self.assertNotEqual(self.cmap[ord("'")], self.cmap[ord('’')])
        self.assertNotEqual(self.cmap[ord('‘')], self.cmap[ord('’')])

    def test_versioned_inventory_and_metric_bounds(self):
        inventory = json.loads((ROOT / 'fonts/inventory.json').read_text(encoding='utf-8'))
        self.assertEqual('Version 2.5', self.font['name'].getDebugName(5))
        self.assertEqual(87, len(self.font.getGlyphOrder()))
        self.assertEqual(112, len(self.cmap))
        self.assertEqual(inventory['glyphCount'], len(self.font.getGlyphOrder()))
        self.assertEqual(inventory['characters'], ''.join(chr(c) for c in sorted(self.cmap)))
        self.assertGreaterEqual(self.font['hhea'].advanceWidthMax, max(w for w, _ in self.font['hmtx'].metrics.values()))
        self.assertEqual(max(self.cmap), self.font['OS/2'].fsLastCharIndex)

    def test_rebuild_is_byte_reproducible(self):
        with tempfile.TemporaryDirectory(dir=ROOT / 'audit/runs') as directory:
            self.assertIn(ROOT / 'audit/runs', Path(directory).resolve().parents)
            with contextlib.redirect_stdout(io.StringIO()):
                build_font(directory)
                first = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(directory).iterdir()}
                build_font(directory)
                second = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(directory).iterdir()}
            self.assertEqual(first, second)

    def test_critical_counters_remain_open_and_outlines_fit_metrics(self):
        from fontTools.pens.boundsPen import BoundsPen
        gs = self.font.getGlyphSet()
        for name in self.font.getGlyphOrder():
            pen = BoundsPen(gs)
            gs[name].draw(pen)
            if pen.bounds:
                x0,y0,x1,y1 = pen.bounds
                self.assertGreaterEqual(x0, 0, name)
                self.assertLessEqual(x1, self.font['hmtx'][name][0], name)
                self.assertGreaterEqual(y0, self.font['hhea'].descent, name)
                self.assertLessEqual(y1, self.font['hhea'].ascent, name)
        for name in ['i', 'I', 't', 'T', 'one']:
            glyph = self.font['glyf'][name]
            areas=[]
            start=0
            for end in glyph.endPtsOfContours:
                points=list(glyph.coordinates[start:end+1])
                areas.append(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(points,points[1:]+points[:1])))
                start=end+1
            self.assertTrue(any(a>0 for a in areas) and any(a<0 for a in areas), name)


if __name__ == '__main__':
    unittest.main()
