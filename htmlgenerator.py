#! /usr/bin/env python
'''
Copyright 2013 Brian Mansberger

This file is part of Simple Web Slideshow.

Simple Web Slideshow is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Simple Web Slideshow is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Simple Web Slideshow.  If not, see <http://www.gnu.org/licenses/>.
'''

import html

class HTML_Generator(object):

    def __init__(self, title, effect, num_slides, resolution, interval, txtlist, typelist=None):
           # Populate self.vals dictionary to inject into web files later
        self.vals = {'title': title, 
                        'effect': effect,
                        # +1 for the title slide, which is frame 1
                        'numslides': num_slides + 1, 
                        'width': resolution[0], 
                        'height': resolution[1],
                        'interval': (interval * 1000),
                        }
        self.txtlist = txtlist
          # Per-slide types ("Full screen", "Letterboxed", "Blank white",
          # "Blank black"); used to pick the caption style. Default to None so
          # older callers still work.
        self.typelist = typelist

         # Map the effect name from the UI dropdown to the CSS class used in
         # template.css. Blur is the default (no extra class), so its class is
         # empty and we omit it from the frame's class list.
        effect_class_map = {
            'Blur': '',
            'Abrupt': 'abrupt',
            'HorizontalSlide': 'horizontal',
            'VerticalSlide': 'vertical',
        }
        effect_class = effect_class_map.get(effect, '')

        fr_css = []
        fr_html = []

          # Frame 1 is always a title slide showing the slideshow name, so the
          # first thing the viewer sees is the title before any pictures.
        title_text = html.escape(title) if title else ""
        fr_css.append('#frame1 {{ z-index: 1; background: #222; }}\n'.format())
        fr_html.append('\u003cdiv class="frames active {effect}" id="frame1"\u003e\u003cdiv class="titleoverlay"\u003e{title}\u003c/div\u003e\u003c/div\u003e\n'.format(
                                effect=effect_class, title=title_text))

        for i in range(num_slides):
                  # If there is an associated text field, create the HTML string
                  # for insertion later. Pick the caption style by slide type:
                  # blank white/black slides get a centered, colored caption
                  # (matching the title slide); other slides get the usual
                  # bottom overlay.
            stype = (self.typelist[i] if self.typelist and i < len(self.typelist)
                        else "Full screen")
            if self.txtlist[i]:
                    # Escape user-entered caption text so it can't break the HTML
                    # (e.g. a caption containing </div> or &amp;) or inject markup.
                cap = html.escape(self.txtlist[i])
                if stype == "Blank white":
                    t = '<div class="black_on_white">{0}</div>'.format(cap)
                elif stype == "Blank black":
                    t = '<div class="white_on_black">{0}</div>'.format(cap)
                else:
                    t = '<div class="textoverlay">{0}</div>'.format(cap)
            else:
                t = ""
                # The picture file is numbered 1..N (1.jpg, 2.jpg, ...). The
                # frame id is offset by +1 so frame 1 is the title slide and
                # pictures occupy frame 2..N+1.
            pic_num = i + 1
            frame_num = pic_num + 1
                # Pictures start at frame 2 (frame 1 is the title slide).
            fr_css.append('#frame{0} {{ z-index: {0}; background: #222 '
                              'url("{1}.jpg") center center no-repeat; }}\n'.format(frame_num, pic_num))
                # Append the chosen effect as a CSS class so the transition is
                 # defined in template.css (Blur/Abrupt/HorizontalSlide/VerticalSlide)
            frame_class = "frames " + effect_class
            fr_html.append('\u003cdiv class="{0}" id="frame{1}"\u003e{2}\u003c/div\u003e\n'.format(
                                frame_class, frame_num, t))

        self.vals['frame_css'] =  "".join(fr_css)
        self.vals['frame_html'] = "".join(fr_html)

    def gen_html(self, dest):
        f = open("template.html", 'r')
        data = f.read()
        f.close()

        data = data.format(**self.vals)
        f = open("{0}/index.html".format(dest), 'w')
        f.write(data)
        f.close()

    def gen_css(self, dest):
        f = open("template.css", 'r')
        data = f.read()
        f.close()

        data = data.format(**self.vals)
        f = open("{0}/style.css".format(dest), 'w')
        f.write(data)
        f.close()

    def gen_js(self, dest):
        f = open("template.js", 'r')
        data = f.read()
        f.close()

        data = data.format(**self.vals)
        f = open("{0}/script.js".format(dest), 'w')
        f.write(data)
        f.close()
