"""Slide layout math for Simple Web Slideshow.

One pure function, compute_layout(), decides how a picture is scaled, cropped and
placed for a given slide type and target resolution. The preview widget and the
code that saves the final pictures both call it, so what you see is what is saved.

No Qt in here on purpose: it can be tested without a GUI.
"""
from dataclasses import dataclass

# Slide types. The strings are also what the HTML generator receives.
FULL_SCREEN = "Full screen"
LETTERBOXED = "Letterboxed"
ENLARGE = "Enlarge to first border"
BLANK_WHITE = "Blank white"
BLANK_BLACK = "Blank black"

PICTURE_MODES = (FULL_SCREEN, LETTERBOXED, ENLARGE)


@dataclass(frozen=True)
class SlideLayout:
    mode: str
    frame: tuple        # (w, h) target resolution
    scaled: tuple       # (w, h) the picture is scaled to before cropping / placing
    crop: tuple         # (x, y, w, h) in 'scaled' pixels (Full screen only), else None
    place: tuple        # (x, y) top-left of the scaled picture inside the frame
    bands: tuple        # source-pixel rects (x, y, w, h) that Full screen crops away


def _px(x):
    """Whole pixels, truncating as the app always has, but forgiving float noise
    (so 1919.9999999999998 counts as 1920, not 1919)."""
    return int(x + 1e-6)


def compute_layout(mode, img_w, img_h, res_w, res_h):
    """Return the SlideLayout for a picture of img_w x img_h on a res_w x res_h slide.

    Full screen              scale to cover the frame, crop what overflows.
    Letterboxed              scale down to fit if too big, never enlarge, centre.
    Enlarge to first border  scale up or down until the first border touches, centre.
    """
    if mode not in PICTURE_MODES:
        raise ValueError("not a picture slide type: %r" % (mode,))
    if min(img_w, img_h, res_w, res_h) <= 0:
        raise ValueError("sizes must be positive")

    width_coef = res_w / img_w
    height_coef = res_h / img_h

    if mode == FULL_SCREEN:
        coef = max(width_coef, height_coef)
        # Never smaller than the frame: float error must not leave the scaled picture
        # a pixel short of the area we crop from it.
        sw = max(res_w, _px(img_w * coef))
        sh = max(res_h, _px(img_h * coef))
        crop_x = (sw - res_w) // 2
        crop_y = (sh - res_h) // 2
        if width_coef >= height_coef:       # picture is wider than the frame: crop top/bottom
            band = 0.5 * (sh - res_h) / coef
            bands = ((0, 0, img_w, band), (0, img_h - band, img_w, band))
        else:                               # picture is taller than the frame: crop left/right
            band = 0.5 * (sw - res_w) / coef
            bands = ((0, 0, band, img_h), (img_w - band, 0, band, img_h))
        return SlideLayout(mode, (res_w, res_h), (sw, sh), (crop_x, crop_y, res_w, res_h),
                           (-crop_x, -crop_y), bands)

    coef = min(width_coef, height_coef)
    if mode == LETTERBOXED:
        coef = min(coef, 1.0)               # Letterboxed shrinks but never enlarges
    sw = min(res_w, max(1, _px(img_w * coef)))
    sh = min(res_h, max(1, _px(img_h * coef)))
    return SlideLayout(mode, (res_w, res_h), (sw, sh), None,
                       ((res_w - sw) / 2, (res_h - sh) / 2), ())
