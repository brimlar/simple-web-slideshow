"""Tests for slidelayout.compute_layout (no Qt needed).  Run:  python3 -m unittest -v test_slidelayout"""
import random
import unittest

from slidelayout import (BLANK_WHITE, ENLARGE, FULL_SCREEN, LETTERBOXED, compute_layout)

FRAMES = [(1920, 1080), (1280, 720), (854, 480), (640, 360), (2560, 1440), (3840, 2160),
          (640, 480), (1024, 768)]


class KnownCases(unittest.TestCase):
    def test_small_image_letterboxed_stays_small_and_centred(self):
        lay = compute_layout(LETTERBOXED, 500, 300, 1920, 1080)
        self.assertEqual(lay.scaled, (500, 300))
        self.assertEqual(lay.place, (710, 390))
        self.assertIsNone(lay.crop)

    def test_small_image_full_screen_covers_and_crops(self):
        lay = compute_layout(FULL_SCREEN, 500, 300, 1920, 1080)
        self.assertEqual(lay.scaled, (1920, 1152))
        self.assertEqual(lay.crop, (0, 36, 1920, 1080))

    def test_small_image_enlarge_touches_first_border(self):
        lay = compute_layout(ENLARGE, 500, 300, 1920, 1080)
        self.assertEqual(lay.scaled, (1800, 1080))
        self.assertEqual(lay.place, (60, 0))

    def test_big_image_letterboxed_shrinks_to_fit(self):
        lay = compute_layout(LETTERBOXED, 3000, 2250, 1920, 1080)
        self.assertEqual(lay.scaled, (1440, 1080))
        self.assertEqual(lay.place, (240, 0))

    def test_perfect_fit(self):
        for mode in (FULL_SCREEN, LETTERBOXED, ENLARGE):
            lay = compute_layout(mode, 1920, 1080, 1920, 1080)
            self.assertEqual(lay.scaled, (1920, 1080))

    def test_blank_slides_have_no_layout(self):
        with self.assertRaises(ValueError):
            compute_layout(BLANK_WHITE, 10, 10, 1920, 1080)

    def test_bad_sizes(self):
        with self.assertRaises(ValueError):
            compute_layout(FULL_SCREEN, 0, 10, 1920, 1080)


class Properties(unittest.TestCase):
    def setUp(self):
        rnd = random.Random(1234)
        self.cases = [(rnd.randint(1, 8000), rnd.randint(1, 8000), *rnd.choice(FRAMES))
                      for _ in range(4000)]
        # include the awkward sizes where float division lands a hair under the frame
        self.cases += [(w, rnd.randint(1, 4000), 1920, 1080) for w in range(1, 4000, 7)]

    def test_full_screen(self):
        for iw, ih, rw, rh in self.cases:
            lay = compute_layout(FULL_SCREEN, iw, ih, rw, rh)
            sw, sh = lay.scaled
            x, y, cw, ch = lay.crop
            self.assertEqual((cw, ch), (rw, rh))
            self.assertGreaterEqual(sw, rw); self.assertGreaterEqual(sh, rh)
            # the crop rectangle always lies inside the scaled picture
            self.assertTrue(x >= 0 and y >= 0 and x + cw <= sw and y + ch <= sh, (iw, ih, rw, rh, lay))
            # one dimension fits the frame exactly (the picture is "covering", not stretched)
            self.assertTrue(sw == rw or sh == rh, (iw, ih, rw, rh, lay))
            # scaled size is the exact cover size, to within one pixel of truncation
            coef = max(rw / iw, rh / ih)
            self.assertLess(abs(sw - iw * coef), 1.0 + 1e-6); self.assertLess(abs(sh - ih * coef), 1.0 + 1e-6)

    def test_letterboxed(self):
        for iw, ih, rw, rh in self.cases:
            lay = compute_layout(LETTERBOXED, iw, ih, rw, rh)
            sw, sh = lay.scaled
            self.assertTrue(1 <= sw <= rw and 1 <= sh <= rh)
            self.assertLessEqual(sw, max(iw, 1) + 1); self.assertLessEqual(sh, max(ih, 1) + 1)   # never enlarged
            if iw > rw or ih > rh:
                self.assertTrue(sw == rw or sh == rh, (iw, ih, rw, rh, lay))
            x, y = lay.place
            self.assertAlmostEqual(x * 2 + sw, rw); self.assertAlmostEqual(y * 2 + sh, rh)

    def test_enlarge(self):
        for iw, ih, rw, rh in self.cases:
            lay = compute_layout(ENLARGE, iw, ih, rw, rh)
            sw, sh = lay.scaled
            self.assertTrue(1 <= sw <= rw and 1 <= sh <= rh)
            self.assertTrue(sw == rw or sh == rh, (iw, ih, rw, rh, lay))


class OldTruncationBug(unittest.TestCase):
    def test_old_int_truncation_could_leave_scaled_picture_a_pixel_short(self):
        # the previous code did int(coef * dim) with coef = res / dim
        short = [w for w in range(1, 6000) if int((1920 / w) * w) < 1920]
        self.assertTrue(short, "expected to find float-truncation cases")
        for w in short[:200]:
            lay = compute_layout(FULL_SCREEN, w, 1, 1920, 1080)
            self.assertGreaterEqual(lay.scaled[0], 1920)
        print("\n  old formula came up short for %d of 5999 picture widths (e.g. %s)" % (len(short), short[:6]))


if __name__ == "__main__":
    unittest.main()
