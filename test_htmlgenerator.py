#!/usr/bin/env python3
"""Smoke tests for HTML_Generator (the pure-logic core of Simple Web Slideshow).

These tests don't require PySide6 or a display, so they can run in CI or a
headless environment. Run with:  python3 test_htmlgenerator.py
"""

import os
import tempfile
import unittest

from htmlgenerator import HTML_Generator


class TestHTMLGenerator(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def _make(self, **kwargs):
        # Sensible defaults; override per test.
        kwargs.setdefault("title", "My Slideshow")
        kwargs.setdefault("effect", "Blur")
        kwargs.setdefault("num_slides", 3)
        kwargs.setdefault("resolution", [1920, 1080])
        kwargs.setdefault("interval", 5)
        kwargs.setdefault("txtlist", ["First", "", "Third"])
        kwargs.setdefault("typelist", ["Full screen", "Letterboxed", "Blank white"])
        return HTML_Generator(**kwargs)

    # --- structure -----------------------------------------------------

    def test_title_slide_is_frame1_and_active(self):
        g = self._make()
        self.assertIn("id=\"frame1\"", g.vals["frame_html"])
        self.assertIn("class=\"frames active", g.vals["frame_html"])
        # The title text should appear in the first frame.
        self.assertIn("titleoverlay", g.vals["frame_html"])
        self.assertIn("My Slideshow", g.vals["frame_html"])

    def test_numslides_includes_title_slide(self):
        g = self._make(num_slides=3)
        # 3 picture slides + 1 title slide = 4
        self.assertEqual(g.vals["numslides"], 4)

    def test_frame_ids_are_unique_and_sequential(self):
        g = self._make(num_slides=4,
                        txtlist=["a", "b", "c", "d"],
                        typelist=["Full screen"] * 4)
        ids = []
        for line in g.vals["frame_html"].splitlines():
            if "id=\"frame" in line:
                idx = line.find("id=\"frame") + len("id=\"")
                end = line.find("\"", idx)
                ids.append(line[idx:end])
        self.assertEqual(ids, ["frame1", "frame2", "frame3", "frame4", "frame5"])
        self.assertEqual(len(ids), len(set(ids)), "frame ids must be unique")

    # --- caption escaping (XSS) --------------------------------------

    def test_caption_is_html_escaped(self):
        g = self._make(txtlist=["A & <b>bold</b>", "", ""])
        html_out = g.vals["frame_html"]
        self.assertIn("A &amp; &lt;b&gt;bold&lt;/b&gt;", html_out)
        # The raw, unescaped form must NOT appear.
        self.assertNotIn("<b>bold</b>", html_out)

    def test_title_is_html_escaped(self):
        g = self._make(title="Big & Bold")
        self.assertIn("Big &amp; Bold", g.vals["frame_html"])

    # --- caption style per slide type --------------------------------

    def test_blank_white_uses_black_on_white(self):
        g = self._make(txtlist=["Section", "", ""],
                       typelist=["Blank white", "Full screen", "Full screen"])
        html_out = g.vals["frame_html"]
        self.assertIn("black_on_white", html_out)

    def test_blank_black_uses_white_on_black(self):
        g = self._make(txtlist=["Section", "", ""],
                       typelist=["Blank black", "Full screen", "Full screen"])
        html_out = g.vals["frame_html"]
        self.assertIn("white_on_black", html_out)

    def test_fullscreen_uses_textoverlay(self):
        g = self._make(txtlist=["Cap", "", ""],
                       typelist=["Full screen", "Full screen", "Full screen"])
        html_out = g.vals["frame_html"]
        self.assertIn("textoverlay", html_out)

    def test_no_caption_produces_no_overlay_div(self):
        # A blank slide with no caption should have no overlay div.
        g = self._make(txtlist=["", "", ""],
                       typelist=["Blank white", "Blank black", "Full screen"])
        html_out = g.vals["frame_html"]
        self.assertNotIn("textoverlay", html_out)
        self.assertNotIn("black_on_white", html_out)
        self.assertNotIn("white_on_black", html_out)

    # --- effect class mapping ----------------------------------------

    def test_effect_class_is_applied(self):
        for effect, cls in [("Blur", ""), ("Abrupt", "abrupt"),
                            ("HorizontalSlide", "horizontal"),
                            ("VerticalSlide", "vertical")]:
            g = self._make(effect=effect)
            html_out = g.vals["frame_html"]
            if cls:
                self.assertIn(cls, html_out,
                              "effect {0} should produce class {1}".format(effect, cls))
            # frame1 is always active
            self.assertIn("frames active", html_out)

    # --- interval conversion -----------------------------------------

    def test_interval_is_in_milliseconds(self):
        g = self._make(interval=5)
        self.assertEqual(g.vals["interval"], 5000)

    # --- generated files are well-formed -----------------------------

    def test_generates_three_files(self):
        g = self._make()
        g.gen_html(self.tmp)
        g.gen_css(self.tmp)
        g.gen_js(self.tmp)
        for name in ("index.html", "style.css", "script.js"):
            path = os.path.join(self.tmp, name)
            self.assertTrue(os.path.exists(path), "{0} should be written".format(name))
            self.assertGreater(os.path.getsize(path), 0,
                               "{0} should be non-empty".format(name))

    def test_css_has_no_unformatted_double_braces(self):
        # A regression test: frame CSS must be single-braced in the output.
        g = self._make()
        g.gen_css(self.tmp)
        with open(os.path.join(self.tmp, "style.css"), encoding="utf-8") as f:
            css = f.read()
        self.assertNotIn("{{", css, "unformatted {{ should not appear in CSS")
        self.assertNotIn("}}", css, "unformatted }} should not appear in CSS")

    def test_html_has_no_unformatted_double_braces(self):
        g = self._make()
        g.gen_html(self.tmp)
        with open(os.path.join(self.tmp, "index.html"), encoding="utf-8") as f:
            html_out = f.read()
        self.assertNotIn("{{", html_out)
        self.assertNotIn("}}", html_out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
