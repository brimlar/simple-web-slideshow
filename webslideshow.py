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

import sys
from PySide.QtCore import *
from PySide.QtGui import *
from ui_webslideshow import Ui_WebSlideshow
from ui_picturesegment import Ui_PictureSegment
from htmlgenerator import HTML_Generator
from picturepicker import Picture_Picker

__version__ = '0.9'


class Projwindow(QMainWindow, Ui_WebSlideshow):

    ### CONSTANTS ###
    PPATH = QDir.homePath() + "/Simple Web Slideshow Projects"  # Saved projects
    DEF_DURATION = 20               # initial / default duration
    MIN_DURATION = 1                # min duration i.e. time between slides
    MAX_DURATION = 60               # max duration i.e. time between slides
    MAX_SLIDES = 100                 # max number of slides
    EFFECTS = ["Blur", "Abrupt", "HorizontalSlide", "VerticalSlide"]
    RESOLUTIONS = ["1024x768", "1280x720", "1366x768", "1600x1200", "1920x1080"]

    ### INIT
    def __init__(self, parent=None):
        # need to call super of Projwindow for QT init / inheritance
        super(Projwindow, self).__init__(parent)

        QCoreApplication.setOrganizationName("brerin.org")
        QCoreApplication.setOrganizationDomain("brerin.org")
        QCoreApplication.setApplicationName("HTML5 Web Slideshow Generator")

        # Set custom application icon
        self.setWindowIcon(QIcon('VideoFolder.ico'))

        settings = QSettings()
        settings.setValue("current_folder", QDir.homePath())

        # Make saved projects folder
        try:
            p = QDir()
            if not p.exists(self.PPATH):
                p.mkdir(self.PPATH)
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

        # Blank array to hold reference to picture segments
        # This is the de facto "holds pictures" object
        self.psegments = []

        # Custom widget to hold scroll content
        self.scr_stuff = QWidget()
        self.setMinimumWidth(700)
        self.scr_vlay = QVBoxLayout()
        # Add stretch object to push the items up from the bottom
        self.scr_vlay.addStretch(1)

        # Call setupUI from UI file
        self.setupUi(self)

        # More scroll area work, post-setupUi
        self.scr_stuff.setLayout(self.scr_vlay)
        self.scrollArea.setWidget(self.scr_stuff)

        # populate comboboxes etc with any customization outside of the UI file
        for effect in self.EFFECTS:
            self.cb_effects.addItem(effect)

        self.sb_duration.setRange(self.MIN_DURATION, self.MAX_DURATION)
        self.sb_duration.setValue(self.DEF_DURATION)
        self.lbl_numslides.setToolTip('Pick a value from 2 to {}.'.format(self.MAX_SLIDES))
        self.sli_numslides.setMaximum(self.MAX_SLIDES)

        # We already populated the default value of the slider in the UI
        self.grow_psegments()

        for res in self.RESOLUTIONS:
            self.cb_resolution.addItem(res)

        # Connect to buttons / signals
        self.sli_numslides.sliderMoved.connect(self.edit_sli_lbl)
        self.sli_numslides.valueChanged.connect(self.grow_psegments)
        self.cb_resolution.currentIndexChanged.connect(self.change_res)
        # Connect to menu items
        self.actionNew_Slideshow.triggered.connect(self.new_proj)
        self.actionSave.triggered.connect(self.save_proj)
        self.actionExit.triggered.connect(self.cancel_proj)
        self.actionAbout_Simple_Web_Slideshow.triggered.connect(self.about_dlg)
        # Connect buttons at bottom to actions
        self.buttonBox.accepted.connect(self.save_proj)
        self.buttonBox.rejected.connect(self.cancel_proj)


    # Reimplement closeEvent on QMainWindow to intercept x-ing out
    def closeEvent(self, event):
        self.cancel_proj()
        event.ignore()


    ### BUTTON ACTIONS
    def edit_sli_lbl(self):
        self.lbl_numslides.setText("Number of slides:   <b>(%d)</b>" %
                                   self.sli_numslides.sliderPosition())


    def grow_psegments(self):
        # First, update the slide label
        self.lbl_numslides.setText("Number of slides:    <b>(%d)</b>" %
                                   self.sli_numslides.value())

        # If this gets called and the resolution widget hasn't been
        # populated, give it the default value 1024x768
        if self.cb_resolution.currentText():
            res = self.cb_resolution.currentText()
        else:
            res = self.RESOLUTIONS[0]

        if self.sli_numslides.value() < len(self.psegments):
            # Remove extra segments
            for i, item in enumerate(self.psegments):
                if i >= self.sli_numslides.value():
                    # itemAt uses a weird index that is off by one
                    self.scr_vlay.removeWidget(item)
                    item.setParent(None)
                    item.deleteLater()
            # Need to slice to keep self.psegments accurate
            self.psegments = self.psegments[0:self.sli_numslides.value()]
        else:
            # Add new segments
            for i in xrange(self.sli_numslides.value()):
                if i >= len(self.psegments):
                    item = PictureSegment(i, res)
                    self.psegments.append(item)
                    # have to insert so the stretch object stays at bottom
                    self.scr_vlay.insertWidget(i, item)
                    item.show()


    def change_res(self):
        # Forces viewport to adapt when res is changed
        for vp in self.psegments:
            vp.vp_setter(self.cb_resolution.currentText())
            if not vp.upic.isNull():
                vp.graphicsView.fitInView(vp.scene.sceneRect(), Qt.KeepAspectRatio)
                if vp.cb_type.currentText() == "Full screen":
                    vp.get_newres()
                    vp.msg_maker(vp.cb_type.currentText())
                elif vp.cb_type.currentText() == "Letterboxed":
                    vp.letterbox_pic()
                    vp.msg_maker(vp.cb_type.currentText())


    def cancel_proj(self):
        # Cancels the project
        wbox = QMessageBox.warning(self, "Exit program?", 
                                   "Close the application without saving?",
                                   QMessageBox.Cancel | QMessageBox.Ok,
                                   QMessageBox.Cancel)
        if wbox == QMessageBox.Ok:
            sys.exit()


    def save_proj(self):
        val = 0
        progress = QProgressDialog("Saving current slideshow...", "Cancel", 0, 
                                   (len(self.psegments) + 3), self)
        progress.setWindowTitle("Saving Project")
        progress.setWindowModality(Qt.WindowModal)
        progress.setMinimumDuration(0)
        progress.setAutoReset(False)
        # 1) Resize the pics
        # 2) Put the captions into a list
        # 3) Generate the HTML file
        progress.setValue(0)
        progress.setLabelText("Resizing and saving pictures...")
        # Get title, if nothing, set it to "Slideshow"
        if self.le_title.text():
            tit = self.le_title.text()
        else:
            tit = "Slideshow"
        # Check if dest dir exists, mkdir new if not
        # We'll increment the title by a number each time
        i = 1
        newtit = tit
        for ch in [",", " ", "?", "!", ":", ";", "(", ")", "."]:
            if ch in tit:
                newtit = newtit.replace(ch, "-")
        newtit = newtit.replace("--", "-")
        newtit = newtit.lower()
        # Delete the last character if it's a "-"
        if newtit[-1] == "-":
            newtit = newtit[:-1]
        p = QDir()
        while(p.exists(self.PPATH + "/" + newtit)):
            newtit = newtit + "-" + str(i)
            i = i + 1
        curprojf = self.PPATH + "/" + newtit
        try:
            p.mkdir(curprojf)
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
        # First resize and save the pix in the proj folder
        self.resize_pics(curprojf)
        # First big bump in the progress bar
        val = len(self.psegments)
        progress.setValue(val)
        self.resolution = [int(n) for n in self.cb_resolution.currentText().split("x")]
        self.captions = []
        for seg in self.psegments:
           self.captions.append(seg.le_caption.text())
        obj = HTML_Generator(tit, self.cb_effects.currentText(),
                             self.sli_numslides.value(), self.resolution, 
                             self.sb_duration.value(), self.captions)
        # Create HTML, CSS and JS files in project folder
        obj.gen_html(curprojf)
        val = val + 1
        progress.setValue(val)
        obj.gen_css(curprojf)
        val = val + 1
        progress.setValue(val)
        obj.gen_js(curprojf)
        val = val + 1
        progress.setValue(val)
        progress.setWindowTitle("Slideshow creation completed")
        progress.setLabelText("Slideshow creation completed.  "
                              "Your finished project can be found in:<br />"
                              "{0}".format(curprojf))
        progress.setCancelButtonText("OK")


    ### CUSTOM ACTIONS
    def new_proj(self):
        # Cancels current project, blanks values, starts new project
        self.sli_numslides.setValue(2)
        self.sb_duration.setValue(20)
        self.cb_resolution.setCurrentIndex(0)
        for seg in self.psegments:
            seg.clean_prev()
            seg.le_caption.clear()
            seg.cb_type.setCurrentIndex(0)
            seg.lbl_warning.clear()


    def about_dlg(self):
        # Shows about info in a dialog
        dlg = QMessageBox()
        dlg.setIcon(QMessageBox.Information)
        dlg.setWindowTitle("About Simple Web Slideshow")
        text = ("<b>About Simple Web Slideshow</b>:<br /><br />\
                Simple Web Slideshow is open source software, licensed \
                under the GPL v 3.0, which guarantees your freedom to modify \
                the source code and redistribute the program.  <br /><br />\
                If you found Simple Web Slideshow useful and time-saving \
                in a for-profit business, a business license of $25 is asked.\
                <br /><br />For personal or non-profit usage Simple Web \
                Slideshow is <b>free</b>, but please consider supporting the \
                software by making a donation.<br /><br />\
                Methods to donate or pay (including cryptocurrencies) can be \
                found online at:<br /><br />\
                <a href='http://swss.m-thing.org#downloads'>\
                http://swss.m-thing.org#downloads</a>")
        dlg.setText(text)
        dlg.exec_()


    def resize_pics(self, dest):
        for seg in self.psegments:
            if seg.upic:
                # Then scale it properly if it's mean to be full-screened
                if seg.cb_type.currentText() == "Full screen":
                    seg.newpic = seg.upic.scaled(seg.newres[0], seg.newres[1])
                    print("Cropping to {0}".format(seg.cropdims))
                    # Crop the pic to the preset cropped dimensions
                    seg.newpic = seg.newpic.copy(*seg.cropdims)
                elif seg.cb_type.currentText() == "Letterboxed":
                    seg.newpic = seg.upic.scaled(seg.newres[0], seg.newres[1])
                    print("Scaling to {0}".format(seg.newres))
            else:
                if seg.cb_type.currentText() == "Blank white":
                    # Create a blank white slide
                    seg.newpic = QPixmap(seg.res[0], seg.res[1])
                    seg.newpic.fill(Qt.white)
                elif seg.cb_type.currentText() == "Blank black":
                    # Create a blank black slide
                    seg.newpic = QPixmap(seg.res[0], seg.res[1])
                    seg.newpic.fill(Qt.black)
            seg.newpic.save(dest + "/" + str(seg.num + 1) + ".jpg")


class PictureSegment(QWidget, Ui_PictureSegment):

    # CONSTANTS
    WIDE_BOX = QSize(192, 108)                  #16:9 ratio box
    STD_BOX = QSize(192, 144)                   #4:3 ratio box
    WHITE_TRANS = QColor(255, 255, 255, 200)    #Transparent white
    RED_TRANS = QColor(255, 0, 0, 120)          #Transparent red
    GRAY_BG = QColor(34, 34, 34, 255)           #Dark gray background
    SLIDE_TYPES = ["Full screen", "Letterboxed", "Blank white", "Blank black"]


    def __init__(self, num, res, parent=None):
        super(PictureSegment, self).__init__(parent)

        # Others
        self.num = num
        self.upic = QPixmap()

        # Get floats out of the resolution b/c we need arith later
        self.res = [int(n) for n in res.split("x")]

        # Custom widgets that aren't shown
        self.scene = QGraphicsScene()

        # Setup
        self.setupUi(self)

        # Call vp_setter once to initialize widget size
        self.vp_setter(res)
        # Add the scene to the graphicsView upon creation
        # otherwise, we can't draw in a GV
        self.graphicsView.setScene(self.scene)

        # Inject slide type strings into combobox
        for typ in self.SLIDE_TYPES:
            self.cb_type.addItem(typ)

        # Some post draw customizations
        self.lbl_bignum.setText(str(num + 1))
        self.lbl_warning.clear()
        self.lbl_warning.setWordWrap(True)

        # Signals and slots
        self.btn_rotate.clicked.connect(self.rotate_pic)
        self.btn_upload.clicked.connect(self.upload_pic)
        self.le_caption.editingFinished.connect(self.commit_desc)
        self.le_caption.selectionChanged.connect(self.commit_desc)
        self.le_caption.returnPressed.connect(self.commit_desc)
        self.cb_type.currentIndexChanged.connect(self.change_sltype)


    # cb_type slot
    def change_sltype(self):
        cur_mode = self.cb_type.currentText()

        if cur_mode == self.SLIDE_TYPES[0]:
            # Fullscreen it!
            if not self.upic.isNull():
                self.get_newres()
                # Calculate offsets to center the pixmap item
                self.pmi.setOffset(0, 0)
                # Enlarge scene to fit the picture
                self.scene.setSceneRect(0, 0, self.upic.width(), self.upic.height())
                self.graphicsView.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
            else:
                print("self.upic does not exist")
            # Re-enable upload button
            self.btn_upload.setEnabled(True)
        elif cur_mode == self.SLIDE_TYPES[1]:
            # Letterbox it if there is a picture present
            if not self.upic.isNull():
                self.letterbox_pic()
            # Re-enable upload button
            self.btn_upload.setEnabled(True)
        else:
            if cur_mode == self.SLIDE_TYPES[2]:
                # Blank white it!
                # Need to blank the previous picture and all derivations
                self.clean_prev()
                self.set_vp_bg(Qt.white)
            elif cur_mode == self.SLIDE_TYPES[3]:
                # Blank black it!
                # Need to blank the previous picture and all derivations
                self.clean_prev()
                self.set_vp_bg(Qt.black)
            # Disable upload button
            self.btn_upload.setDisabled(True)
        self.msg_maker(self.cb_type.currentText())


    def clean_prev(self):
        # This cleans up the previous picture and all its graphics
        try:
            for item in self.scene.items():
                self.scene.removeItem(item)
                del item
            self.upic = QPixmap()
            # Reset scene to a 0 size for housekeeping
            self.scene.setSceneRect(0, 0, 0, 0)
        except Exception as e:
            print("Line {0}: {1}".format(sys.exc_info()[-1].tb_lineno, e))


    def rotate_pic(self):
        # rotates the uploaded pixmap 90 degrees clockwise
        # and recalculates its dimensions
        # then redraws it in the QGraphicsView
        trans = QTransform()
        self.rpic = self.upic.transformed(trans.rotate(90))
        self.clean_prev()
        self.upic = self.rpic
        del self.rpic
        self.pmi = self.scene.addPixmap(self.upic)
        print("New res: {0} x {1}".format(self.upic.width(), self.upic.height()))
        self.change_sltype()
        self.res_tagger(self.upic, self.scene)


    # btn_upload slot
    def upload_pic(self):
        # Let's talk to our QSettings object
        settings = QSettings()
        p = Picture_Picker()
        fname = False
        if (p.exec_()):
            fname = p.selectedFiles()[0]

        if fname:
            # Clean up previous photo if it exists
            self.clean_prev()
            # we only want the image itself
            self.upic = QPixmap(fname)
            # We also want the file path info b/c we'll set last directory
            self.finfo = QDir(fname)
            # Set the current_folder QSettings from path
            settings.setValue("current_folder", self.finfo.path())
            settings.sync()
            self.pmi = self.scene.addPixmap(self.upic)
            # If someone selects Letterboxed, make sure the pic is
            # smaller than the desired resolution
            if self.cb_type.currentText() == "Letterboxed":
                self.letterbox_pic()
            else:
                self.resize_scene(self.cb_type.currentText())
                self.graphicsView.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
                self.get_newres()
            # Draw the resolution text and box
            self.res_tagger(self.upic, self.scene)
            # Finally, call our message maker
            self.msg_maker(self.cb_type.currentText())


    def commit_desc(self):
        # When called, commits caption to PictureSegment object variable
        self.caption = self.le_caption.text()


    def res_tagger(self, pic, scene):
        # Creates two new attributes, self.restag and self.resbox
        # and adds them to the QGraphicsScene
        self.restag = QGraphicsTextItem(str(pic.width()) + "x" + str(pic.height()))
        self.restag.setFlags(QGraphicsItem.ItemIgnoresTransformations)
        # We want the resolution (4) above the res box (3)
        # Which are both above the red overlay boxes (2)
        self.restag.setZValue(4)
        scene.addItem(self.restag)
        self.resbox = scene.addRect((self.restag.boundingRect()), Qt.NoPen, self.WHITE_TRANS)
        self.resbox.setFlags(QGraphicsItem.ItemIgnoresTransformations)
        self.resbox.setZValue(3)


    def vp_setter(self, res):
        # Get floats out of the resolution b/c we need arith later
        self.res = [int(n) for n in res.split("x")]

        # If the ratio is widescreen, set 16:9 ratio graphicsview in the widget
        # Otherwise, set standard ratio (4:3) widget
        if round(float(self.res[0]) / float(self.res[1]), 1) == 1.8:
            self.graphicsView.setMinimumSize(self.WIDE_BOX)
            self.graphicsView.setMaximumSize(self.WIDE_BOX)
        else:
            self.graphicsView.setMinimumSize(self.STD_BOX)
            self.graphicsView.setMaximumSize(self.STD_BOX)


    def msg_maker(self, mode):
        # Depending on image size and selected resolution,
        # give a message in the label
        # mode is typically cb_type.currentText()

        MSG1 = "<b>This image is a perfect fit.</b>"
        MSG2 = ("<b><font color='red'>Warning</font></b>: The height on this "
                "image is smaller than the target resolution.  The height of "
                "the image will be <b>stretched</b> to compensate, and the "
                "width cropped.")
        MSG3 = ("<b><font color='red'>Warning</font></b>: the width on this "
                "image is smaller than the target resolution.  The width of "
                "the image will be <b>stretched</b> to compensate, and the "
                "height cropped.")
        MSG4 = ("Part of this image falls outside the target "
                "resolution.  It will be cropped to compensate.")
        MSG5 = ("<b><font color='red'>Warning</font></b>: This image is "
                "smaller than the target resolution. Its width and height will "
                "both be <b>stretched</b>, and a small amount may be cropped.")
        MSG6 = ("You have selected 'Letterboxed' mode for this picture, which "
                "means that it will not be cropped and it will be centered "
                "in the slideshow.")
        MSG7 = ("This image is bigger than the target resolution. "
                "It will be cropped to compensate, but it will look OK.")
        MSG8 = ("You have chosen to Letterbox this picture, but it comes out "
                "to be the same resolution as if you had 'full-screened' it. "
                "It will look fine (but consider full-screening it.)")
        W_MSG = ("<font color='red'>The quality of this image might be "
                 "degraded as a result.</font>")

        if not self.upic.isNull():
            if mode == "Letterboxed":
                if (self.newres[0] == self.res[0] and self.newres[1] == self.res[1]):
                    # Rare case where it gets letterboxed but it is the same
                    # resolution as the 'optimized resolution', in which
                    # case they could full screen it (and we tell them this)
                    self.lbl_warning.setText(MSG8)
                else:
                    # Letterboxed means no data is lost and msg is the same
                    self.lbl_warning.setText(MSG6)
            elif self.upic.width() == self.res[0]:
                # If width is the same as target resolution
                if self.upic.height() < self.res[1]:
                # Width same, height is less
                    self.lbl_warning.setText(MSG2 + W_MSG)
                elif self.upic.height() > self.res[1]:
                # Width same, height is more
                    self.lbl_warning.setText(MSG4)
                else:
                # Both width and height match target res!
                    self.lbl_warning.setText(MSG1)
            elif self.upic.width() < self.res[0]:
                # If width is less than resolution
                if self.upic.height() <= self.res[1]:
                    # The image is smaller in both dimensions
                    self.lbl_warning.setText(MSG5 + W_MSG)
                else:
                    # Else height equals or is larger than target,
                    # in which case we're going to have to stretch width
                    self.lbl_warning.setText(MSG3 + W_MSG)
            else:
                # Else width must be more than resolution
                if self.upic.height() < self.res[1]:
                    # Width is more, but height is less
                    self.lbl_warning.setText(MSG2 + W_MSG)
                elif self.upic.height() > self.res[1]:
                    # Width is more, height is more
                    self.lbl_warning.setText(MSG7)
                else:
                    # Width is more, height is same
                    self.lbl_warning.setText(MSG4)
        else:
            # Else there's no picture, so blank the msg
            self.lbl_warning.setText("")


    def window_scale(self):
        try:
            self.boxgroup.scene().removeItem(self.boxgroup)
        except Exception as e:
            print("Line {0}: {1}".format(sys.exc_info()[-1].tb_lineno, e))
        # If Letterboxed mode is selected, scale the uploaded pic
        # in the viewport box to reflect this
        # First, setSceneRect for letterboxed mode
        self.resize_scene(self.cb_type.currentText())

        # Calculate offsets to center the pixmap item
        left_offset = (self.res[0] - self.upic.width()) / 2
        top_offset = (self.res[1] - self.upic.height()) / 2
        self.pmi.setOffset(left_offset, top_offset)

        # Set background for letterboxed mode to GRAY_BG
        # self.set_vp_bg(self.GRAY_BG)
        self.graphicsView.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)


    def set_vp_bg(self, color=None):
        # helper function to set viewport background color
        if color:
            brush = QBrush(color)
        else:
            brush = Qt.NoBrush
        self.graphicsView.setBackgroundBrush(brush)


    def resize_scene(self, mode):
        # helper function to set scene size based upon mode
        if mode == "Full screen":
            self.scene.setSceneRect(0, 0, self.upic.width(), self.upic.height())
        elif mode == "Letterboxed":
            self.scene.setSceneRect(0, 0, self.res[0], self.res[1])


    def letterbox_pic(self):
        # calculates future scaled resolution for use when saving pictures
        # inserts the values into self.newres
        dims = [self.upic.width(), self.upic.height()]

        # Set background for letterboxed mode to GRAY_BG
        self.set_vp_bg(self.GRAY_BG)

        # Remove red overlay cropboxes if present
        self.remove_cropboxes()

        width_coef = round(self.res[0] / float(dims[0]), 4)
        height_coef = round(self.res[1] / float(dims[1]), 4)

        # We only care if a picture is bigger than the resolution
        # If it's smaller, we'll just letterbox it as-is without scaling
        if (width_coef < 1) or (height_coef < 1):
            # we want the smaller number, the more severe ratio
            coef = min(width_coef, height_coef)
            self.newres = [int(coef * dims[0]), int(coef * dims[1])]
            # Resize the scene so it stretches to fit the larger pic
            self.scene.setSceneRect(0, 0, self.upic.width(), self.upic.height())
            # and draw the larger picture within the viewport
            self.graphicsView.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        else:
            # else we just accept the smaller picture's dimensions
            self.newres = [dims[0], dims[1]]
            # Resize the scene so it goes back to normal
            self.scene.setSceneRect(0, 0, self.res[0], self.res[1])
            # and scale the viewport to the the combobox resolution
            self.window_scale()
        print("{0}'s new res is {1}".format(dims, self.newres))


    def remove_cropboxes(self):
        # Remove the red overlay boxes if the item has them
        try:
            self.boxgroup.scene().removeItem(self.boxgroup)
            del self.boxgroup
        except Exception as e:
            print("Line {0}: {1}".format(sys.exc_info()[-1].tb_lineno, e))


    def get_newres(self):
        # calculates new resolution of a pic based on combobox selection
        # draws red box overlay on picture as well

        # boxes will become a QBoxGroup later here
        boxes = []
        dims = [self.upic.width(), self.upic.height()]

        # Reset the gray bg color on the viewport if it exists
        if self.cb_type.currentText() == "Full screen":
            self.set_vp_bg()

        # Remove overlay cropboxes
        self.remove_cropboxes()

        # Get the ratios in diff between actual h/w and target
        width_coef = self.res[0] / float(dims[0])
        height_coef = self.res[1] / float(dims[1])

        # Whether it's w or h, we want the side that is most different
        coef = max(width_coef, height_coef)

        self.newres = [int(coef * dims[0]), int(coef * dims[1])]
        # Resize the scene so it stretches to fit the larger pic
        self.scene.setSceneRect(0, 0, self.upic.width(), self.upic.height())
        # and draw the larger picture within the viewport
        self.graphicsView.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

        if coef == width_coef:
            # It means we need to crop height b/c we scaled width to fit
            leftover = int(coef * dims[1]) - self.res[1]
            self.bx1 = QRectF(0, 0, dims[0], (0.5 * leftover) / coef)
            self.bx2 = QRectF(0, (dims[1] - ((0.5 * leftover) / coef)),
                              dims[0], (0.5 * leftover) / coef)
            # Set self.cropdims for when we save the resized image
            self.cropdims = (0, int(0.5 * leftover), int(self.res[0]),
                             int(self.res[1]))
        else:
            # It means we need to crop width b/c we scaled height to fit
            leftover = int(coef * dims[0]) - self.res[0]
            # We need to divide by x so the rects show what will
            # really be cut from the original photo
            self.bx1 = QRectF(0, 0, (0.5 * leftover) / coef, dims[1])
            self.bx2 = QRectF((dims[0] - ((0.5 * leftover) / coef)), 0,
                              (0.5 * leftover) / coef, dims[1])
            # Set self.cropdims for when we save the resized image
            self.cropdims = (int(0.5 * leftover), 0, int(self.res[0]),
                             int(self.res[1]))

        print("{0}'s new res is {1}".format(dims, self.newres))
        boxes.append(self.scene.addRect(self.bx1, Qt.NoPen, self.RED_TRANS))
        boxes.append(self.scene.addRect(self.bx2, Qt.NoPen, self.RED_TRANS))
        # self.boxgroup is the team of two red overlay squares
        self.boxgroup = self.scene.createItemGroup(boxes)
        #Set ZValue to place it under the resolution box, but above picture
        self.boxgroup.setZValue(1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    project = Projwindow()
    project.show()

    app.exec_()
    sys.exit()
