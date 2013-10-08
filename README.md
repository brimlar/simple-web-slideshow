Simple Web Slideshow

This project will be licensed under the GPL Version 3.

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
