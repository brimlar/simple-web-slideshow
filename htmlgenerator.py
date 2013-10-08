#! /usr/bin/env python

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
