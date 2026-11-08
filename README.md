Simple Web Slideshow

This project is licensed under the GPL Version 3.

The intended use for this program will be to take an
assortment of image files, resize them to a desired
"target" resolution, provide text overlay descriptions 
("captions") on the slides, and to put it into a native
HTML / CSS / JS web format so it is easily viewable in
any web browser.

A perfect use for this would be for kiosks where you know
the target resolution and want a slideshow to autoplay.
Just set up the kiosks to launch the browser upon bootup 
in fullscreen mode, pointing to the files on a web server,
and presto -- the autoplay slideshow will start.

This is far superior than creating PowerPoint presentations 
and using PowerPoint in slide mode on the kiosk machines, 
which requires the expensive and unnecessary use of 
Microsoft Office.

While it is possible using CSS and JS to dynamically draw 
image files according to the destination's viewport size,
this often means sending over the entire photo/image, which
could be many MBs in file size.  By resizing the photos to a
smaller resolution, you can dramatically decrease the
transmission time of the data via the web browser.  This is
why I pursued this simplistic method.

## Requirements (Python 3 / PySide6)

This version was ported from the original Python 2 / PySide 1.x
release to **Python 3 + PySide6**, and the slideshow transitions are
now implemented with CSS transitions instead of hand-rolled JS timers.

### Installing

1. Install **Python 3** (any 3.8+). On macOS with Homebrew:

   ```
   brew install python
   ```
2. Create a virtual environment and install the one dependency
   (PySide6, which bundles the Qt libraries):

   ```
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### Running

```
source venv/bin/activate     # if not already active
python3 webslideshow.py
```

The generated slideshow is written to a folder under your home
directory (`~/...`), and can be opened in any modern web browser.

## Notes on the port

- **Caption text is HTML-escaped** before being injected into the
  generated pages, so a caption can no longer break the HTML or
  inject markup.
- **Transitions are CSS-native**: the four effect names
  (Blur, Abrupt, HorizontalSlide, VerticalSlide) are now CSS
  classes on each frame, and `script.js` only toggles an
  `.active` class on a timer. The same effects, fewer lines.
- **Image handling stays on Qt's `QPixmap`** (no extra dependencies);
  it is part of PySide6.

## Testing

The pure-logic core (the HTML/CSS/JS generator) is covered by a small
smoke-test suite that needs no display or PySide6:

```
python3 test_htmlgenerator.py
```

It checks caption escaping (XSS), title-slide structure, per-slide-type
caption styling, effect-class mapping, and that the generated files are
well-formed.

## Project layout

| File | Purpose |
|------|---------|
| `webslideshow.py` | Main application + GUI logic |
| `htmlgenerator.py` | Builds the HTML/CSS/JS for a slideshow (tested) |
| `picturepicker.py` | Image-picker dialog with live preview |
| `ui_*.py` | Auto-generated Qt UI (regenerate from `*.ui` with `pyside6-uic`) |
| `*.ui` | Qt Designer source-of-truth for the UI |
| `template.*` | HTML/CSS/JS templates the generator fills in |
| `test_htmlgenerator.py` | Smoke tests for the generator |
| `requirements.txt` | Dependencies (`PySide6`) |

---

Original release: 2013 (Python 2 / PySide 1.x).  Ported to
Python 3 / PySide6 in 2026.
