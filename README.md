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
transmission time of the data via the web browser.
That is why I pursued this simplistic method.

## Version 1.0

Version 1.0 is a port from the original **Python 2 / PySide 1.x**
release to **Python 3 + PySide6**. The GUI is now built
programmatically (no Qt Designer `.ui` files or generated
`ui_*.py`), the slide-geometry math lives in a small,
GUI-free `slidelayout.py` module, and the transition effects
are pure CSS.

## Requirements (Python 3 / PySide6)

- **Python 3** (3.8+; developed and tested on 3.14).
- **PySide6** (see `requirements.txt`; tested on 6.12).

On macOS with Homebrew:

    brew install python

### Installing

1. Create a virtual environment and install the one
    dependency (PySide6, which bundles the Qt libraries):

    ```
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

### Running

```
source .venv/bin/activate      # if not already active
python3 webslideshow.py
```

The generated slideshow is written to a folder under your home
directory (`~/Simple Web Slideshow Projects/...`), and can be
opened in any modern web browser.

## How it works

For each picture you add a slide, you pick a **slide type**:

- **Full screen** — scale to cover the frame and crop the
  overflow (the default look).
- **Letterboxed** — scale down to fit if it's too big, never
  enlarge, and centre.
- **Enlarge to first border** — scale up or down until the
  picture touches the first border, then centre.
- **Blank white** / **Blank black** — a solid slide, useful as
  a divider; captions are centred and coloured to match.

Each frame can carry a caption and a **transition effect**
(Blur, Abrupt, HorizontalSlide, VerticalSlide). The output is
three files per slideshow:

- `index.html` — one frame per slide plus a leading title
  slide; the title frame is baked `.active` so the first paint
  shows the title with no JS-timing trick.
- `style.css` — frame styling and the transition effects.
- `script.js` — toggles the `.active` class on a timer; the
  effect itself lives entirely in CSS.

## Notes on the port

- **Caption text is HTML-escaped** before being injected into
  the generated pages, so a caption can no longer break the HTML
  or inject markup.
- **Transitions are CSS-native**: the four effect names map to
  CSS classes on each frame, and `script.js` only toggles an
  `.active` class on a timer. The same effects, fewer lines.
- **Slide geometry is factored out** into `slidelayout.py`
  (`compute_layout`), a pure function with no Qt dependency. The
  on-screen preview and the code that saves the final pictures
  both call it, so what you see is what is saved.
- **Image handling stays on Qt's `QPixmap`/`QImage`** (no extra
  dependencies); it is part of PySide6.

## Testing

The slide-layout math (the pure-logic core) is covered by a
test suite that needs no display and no PySide6:

```
python3 -m unittest -v test_slidelayout
```

It checks known cases, randomized property tests across many
frame sizes, and the float-truncation bug the old `int()` math
used to fall into.

## Business Use

We ask that if you find Simple Web Slideshow useful in a for-profit
business, that you consider sending $25 to the project.  You may
contact Brimlar here at this GitHub project.

## Project layout

| File | Purpose |
|------|---------|
| `webslideshow.py` | Main application + GUI logic |
| `htmlgenerator.py` | Builds the HTML/CSS/JS for a slideshow |
| `slidelayout.py` | Pure slide-geometry math (scaled / crop / place) |
| `template.*` | HTML/CSS/JS templates the generator fills in |
| `test_slidelayout.py` | Tests for `slidelayout.compute_layout` |
| `requirements.txt` | Dependencies (`PySide6`) |
| `Video-Folder.png` | App icon |

---

Original release: 2013 (Python 2 / PySide 1.x).
Version 1.0 ported to Python 3 / PySide6 in 2026.
