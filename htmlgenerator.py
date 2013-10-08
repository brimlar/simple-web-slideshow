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

class HTML_Generator(object):

    def __init__(self, title, effect, num_slides, resolution, interval, txtlist):
        # Populate self.vals dictionary to inject into web files later
        self.vals = {'title': title, 
                     'effect': effect,
                     'numslides': num_slides, 
                     'width': resolution[0], 
                     'height': resolution[1],
                     'interval': (interval * 1000),
                     }
        self.txtlist = txtlist

        fr_css = []
        fr_html = []
        for i in range(num_slides):
            # If there is an associated text field, create the HTML string
            # for insertion later
            if self.txtlist[i]:
                t = '<div class="textoverlay">{0}</div>'.format(self.txtlist[i])
            else:
                t = ""
            # We bump i by 1 because we use that value to write HTML and CSS code
            i = i + 1
            if i == 1:
                # The first layer is always fully opaque
                fr_css.append('#frame{0} {{ z-index: {0}; background: #222 '
                              'url("{0}.jpg") center center no-repeat; }}\n'.format(i))
            else:
                # ...but the others change
                fr_css.append('#frame{0} {{ z-index: {0}; background: #222 ' 
                              'url("{0}.jpg") center center no-repeat; opacity: 0; }}\n'.format(i))
            fr_html.append('<div class="frames" id="frame{0}">{1}</div>\n'.format(i, t))

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
