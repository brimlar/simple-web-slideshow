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
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from ui_webslideshow import Ui_WebSlideshow
from ui_picturesegment import Ui_PictureSegment
from htmlgenerator import HTML_Generator
from picturepicker import Picture_Picker

__version__ = '0.9'


class Projwindow(QMainWindow, Ui_WebSlideshow):

    ### CONSTANTS ###
    PPATH = QDir.homePath() + "/Simple Web Slideshow Projects"  # Saved projects
    DEF_DURATION = 20               # initial / default duration
    MIN_DURATION = 1                  # min duration i.e. time between slides
    MAX_DURATION = 60                 # max duration i.e. time between slides
    MAX_SLIDES = 100                  # max number of slides
    EFFECTS = ["Blur", "Abrupt", "HorizontalSlide", "VerticalSlide"]
       # Each entry is (friendly_label, "WxH"). The label is shown in the
       # dropdown; the "WxH" is stored as item data and is what the code reads.
       # Ordered small/fast to large; 1080p is the default (index 3).
    RESOLUTIONS = [
         ("360p (640x360)",      "640x360"),
         ("480p (854x480)",      "854x480"),
         ("720p (1280x720)",     "1280x720"),
         ("1080p (1920x1080)",   "1920x1080"),
         ("1440p (2560x1440)",   "2560x1440"),
         ("4K (3840x2160)",      "3840x2160"),
         ("640x480 (legacy 4:3)","640x480"),
         ("1024x768 (legacy 4:3)","1024x768"),
    ]
    DEF_RESOLUTION_INDEX = 3           # 1080p

    ### INIT
    def __init__(self, parent=None):
          # need to call super of Projwindow for QT init / inheritance
        super(Projwindow, self).__init__(parent)

        # Set custom application icon (shipped with the project as a PNG)
        self.setWindowIcon(QIcon('Video-Folder.png'))

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

        self.le_duration.setText(str(self.DEF_DURATION))
            # Allow free typing (no QIntValidator blocking input) but flag bad
            # values in red via a live check; get_duration() clamps at save time.
        self.le_duration.setToolTip(
              "Seconds between slides. Minimum {0}, maximum {1}.".format(
                self.MIN_DURATION, self.MAX_DURATION))
              # A small warning label that appears *next to* the field when the
              # value is invalid or out of range. We pull the field out of the
              # generated grid cell and re-add it alongside the warning in a
              # horizontal sub-layout so the warning sits right beside it rather
              # than drifting to the far right of the row.
        self.lbl_durwarn = QLabel(self.groupBox)
        self.lbl_durwarn.setObjectName(u"lbl_durwarn")
        self.lbl_durwarn.setStyleSheet("color: #c00; font-weight: bold;")
        self.lbl_durwarn.setVisible(False)
              # Pull the field out of its generated grid cell and re-add it
              # alongside the warning in a horizontal sub-layout so the warning
              # sits right beside the field instead of drifting far right.
        self.gridLayout.removeWidget(self.le_duration)
        dur_hbox = QHBoxLayout()
        dur_hbox.addWidget(self.le_duration)
        dur_hbox.addWidget(self.lbl_durwarn)
        dur_hbox.addStretch(1)
        self.gridLayout.addLayout(dur_hbox, 2, 1, 1, 2)
        self.le_duration.textChanged.connect(self.check_duration)
        self.lbl_numslides.setToolTip('Pick a value from 2 to {}.'.format(self.MAX_SLIDES))
        self.sli_numslides.setMaximum(self.MAX_SLIDES)

          # Populate the resolution dropdown (friendly label + WxH data) and set
          # the default *before* creating the initial slide segments, so they
          # start at the default resolution.
        for label, wxh in self.RESOLUTIONS:
              # Show the friendly label, store the "WxH" as item data.
            self.cb_resolution.addItem(label, wxh)
        self.cb_resolution.setCurrentIndex(self.DEF_RESOLUTION_INDEX)

          # We already populated the default value of the slider in the UI
        self.grow_psegments()

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
        self.buttonBox.rejected.connect(self.close)


     # Reimplement closeEvent on QMainWindow so that x-ing out asks
     # whether to exit without saving, and only closes if the user confirms.
    def closeEvent(self, event):
        wbox = QMessageBox.warning(self, "Exit program?",
                                    "Close the application without saving?",
                                   QMessageBox.Cancel | QMessageBox.Ok,
                                   QMessageBox.Cancel)
        if wbox == QMessageBox.Ok:
            event.accept()
        else:
            event.ignore()


      ### BUTTON ACTIONS
    def get_duration(self):
          # Read the duration from the text field, validate it's a number in
          # range, and fall back to the default if the field is empty/bad.
        txt = self.le_duration.text().strip()
        if txt == "":
            return self.DEF_DURATION
        try:
            val = int(txt)
        except ValueError:
            QMessageBox.warning(self, "Invalid duration",
                "Slide duration must be a whole number of seconds "
                "({0} to {1}). Using the default ({2}).".format(
                    self.MIN_DURATION, self.MAX_DURATION, self.DEF_DURATION))
            return self.DEF_DURATION
        if val < self.MIN_DURATION or val > self.MAX_DURATION:
            val = max(self.MIN_DURATION, min(val, self.MAX_DURATION))
            QMessageBox.warning(self, "Duration out of range",
                "Slide duration must be between {0} and {1} seconds. "
                "Using {2} instead.".format(self.MIN_DURATION, self.MAX_DURATION, val))
        return val

    def check_duration(self, text):
            # Live feedback: turn the field + warning red when the value is
            # invalid or out of range, and clear it when valid.
        txt = text.strip()
        valid = True
        msg = ""
        if txt == "":
            valid = False
        else:
            try:
                val = int(txt)
                if val < self.MIN_DURATION or val > self.MAX_DURATION:
                    valid = False
            except ValueError:
                valid = False
        if valid:
            self.le_duration.setStyleSheet("")
            self.lbl_durwarn.setVisible(False)
        else:
            self.le_duration.setStyleSheet(
                "QLineEdit {{ border: 1px solid #c00; color: #c00; }}")
            self.lbl_durwarn.setVisible(True)
            self.lbl_durwarn.setText("Enter a number from {0} to {1}".format(
                self.MIN_DURATION, self.MAX_DURATION))

    def edit_sli_lbl(self):
        self.lbl_numslides.setText("Number of slides:   <b>(%d)</b>" %
                                   self.sli_numslides.sliderPosition())


    def grow_psegments(self):
        # First, update the slide label
        self.lbl_numslides.setText("Number of slides:    <b>(%d)</b>" %
                                   self.sli_numslides.value())

           # If this gets called and the resolution widget hasn't been
           # populated, give it the default value
        data = self.cb_resolution.currentData()
        if data:
            res = data
        else:
            res = self.RESOLUTIONS[0][1]        # WxH of the first entry

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
            for i in range(self.sli_numslides.value()):
                if i >= len(self.psegments):
                    item = PictureSegment(i, res)
                    self.psegments.append(item)
                    # have to insert so the stretch object stays at bottom
                    self.scr_vlay.insertWidget(i, item)
                    item.show()


    def change_res(self):
          # Forces viewport to adapt when res is changed
        res = self.cb_resolution.currentData() or self.RESOLUTIONS[0][1]
        for vp in self.psegments:
            vp.vp_setter(res)
            if not vp.upic.isNull():
                vp.graphicsView.fitInView(vp.scene.sceneRect(), Qt.KeepAspectRatio)
                if vp.cb_type.currentText() == "Full screen":
                    vp.get_newres()
                    vp.msg_maker(vp.cb_type.currentText())
                elif vp.cb_type.currentText() == "Letterboxed":
                    vp.letterbox_pic()
                    vp.msg_maker(vp.cb_type.currentText())


    def cancel_proj(self):
         # "Exit" menu item: ask to quit without saving, then close properly
         # (accept() runs closeEvent, which asks the same question).
        wbox = QMessageBox.warning(self, "Exit program?",
                                    "Close the application without saving?",
                                   QMessageBox.Cancel | QMessageBox.Ok,
                                   QMessageBox.Cancel)
        if wbox == QMessageBox.Ok:
            self.close()


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
        self.resolution = [int(n) for n in (self.cb_resolution.currentData()
                                     or self.RESOLUTIONS[0][1]).split("x")]
        self.captions = []
        self.slidetypes = []
        for seg in self.psegments:
           self.captions.append(seg.le_caption.text())
           self.slidetypes.append(seg.cb_type.currentText())
        obj = HTML_Generator(tit, self.cb_effects.currentText(),
                             self.sli_numslides.value(), self.resolution, 
                             self.get_duration(), self.captions, self.slidetypes)
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
        progress.setLabelText("Slideshow creation completed.<br /><br />"
                               "Your finished project can be found in:<br />"
                               "{0}<br /><br />"
                               "To launch your slideshow, open the index.html "
                               "file in a modern web browser and the slideshow "
                               "will automatically play.".format(curprojf))
        progress.setCancelButtonText("OK")


    ### CUSTOM ACTIONS
    def new_proj(self):
          # Cancels current project, blanks values, starts new project
        self.sli_numslides.setValue(2)
        self.le_duration.setText(str(self.DEF_DURATION))
        self.cb_resolution.setCurrentIndex(self.DEF_RESOLUTION_INDEX)
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
                <a href='http://sws.ideaprojects.me'>\
                http://sws.ideaprojects.me</a>")
        dlg.setText(text)
        dlg.exec_()


    def resize_pics(self, dest):
        for seg in self.psegments:
            if seg.upic:
                  # Then scale it properly if it's meant to be full-screened
                if seg.cb_type.currentText() == "Full screen":
                    seg.newpic = seg.upic.scaled(seg.newres[0], seg.newres[1])
                       # Crop the pic to the preset cropped dimensions
                    seg.newpic = seg.newpic.copy(*seg.cropdims)
                elif seg.cb_type.currentText() == "Letterboxed":
                    seg.newpic = seg.upic.scaled(seg.newres[0], seg.newres[1])
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
               # Fullscreen it! (only if a picture has been uploaded)
            if not self.upic.isNull():
                self.get_newres()
                  # Calculate offsets to center the pixmap item
                self.pmi.setOffset(0, 0)
                  # Enlarge scene to fit the picture
                self.scene.setSceneRect(0, 0, self.upic.width(), self.upic.height())
                self.graphicsView.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
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
             # This cleans up the previous picture and all its graphics.
             # Best-effort: if the scene is in an odd state we don't want to
             # crash, so a failure here is swallowed.
        try:
            for item in self.scene.items():
                self.scene.removeItem(item)
            self.upic = QPixmap()
                # Reset scene to a 0 size for housekeeping
            self.scene.setSceneRect(0, 0, 0, 0)
        except Exception:
            pass


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
        self.change_sltype()
        self.res_tagger(self.upic, self.scene)


    # btn_upload slot
    def upload_pic(self):
        # Let's talk to our QSettings object
        settings = QSettings()
        p = Picture_Picker()
        fname = False
        if p.exec():
            selected = p.selectedFiles()
            if selected:
                fname = selected[0]

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
          # Remove the red overlay crop boxes if present (best-effort).
        if hasattr(self, "boxgroup"):
            try:
                self.boxgroup.scene().removeItem(self.boxgroup)
            except Exception:
                pass
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

           # We only care if a picture is bigger than the resolution.
           # If it's smaller, we'll just letterbox it as-is without scaling.
        if (width_coef < 1) or (height_coef < 1):
               # we want the smaller number, the more severe ratio
            coef = min(width_coef, height_coef)
            self.newres = [int(coef * dims[0]), int(coef * dims[1])]
               # The picture is larger than the target, so scale the scene down to
               # the target resolution and center the (scaled) picture within it.
               # This also resets any stale offset left over from a previous call,
               # which was the cause of the picture drifting off-center when the
               # resolution was changed while in Letterboxed mode.
            self.scene.setSceneRect(0, 0, self.res[0], self.res[1])
            left_offset = (self.res[0] - self.upic.width()) * coef / 2
            top_offset = (self.res[1] - self.upic.height()) * coef / 2
            self.pmi.setOffset(left_offset, top_offset)
               # and draw the picture centered within the viewport
            self.graphicsView.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        else:
               # else we just accept the smaller picture's dimensions
            self.newres = [dims[0], dims[1]]
               # Resize the scene so it goes back to normal
            self.scene.setSceneRect(0, 0, self.res[0], self.res[1])
               # and scale the viewport to the combobox resolution
            self.window_scale()


    def remove_cropboxes(self):
              # Remove the red overlay boxes if the item has them. Use hasattr so
              # the first call (before any boxgroup exists) is a no-op.
        if hasattr(self, "boxgroup"):
            try:
                self.boxgroup.scene().removeItem(self.boxgroup)
                del self.boxgroup
            except Exception:
                pass


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

        boxes.append(self.scene.addRect(self.bx1, Qt.NoPen, self.RED_TRANS))
        boxes.append(self.scene.addRect(self.bx2, Qt.NoPen, self.RED_TRANS))
        # self.boxgroup is the team of two red overlay squares
        self.boxgroup = self.scene.createItemGroup(boxes)
        #Set ZValue to place it under the resolution box, but above picture
        self.boxgroup.setZValue(1)

if __name__ == '__main__':
     # Configure the settings/application identity *before* creating the
     # QApplication, so QSettings has the right org/app name from the start.
    QCoreApplication.setOrganizationName("brerin.org")
    QCoreApplication.setOrganizationDomain("brerin.org")
    QCoreApplication.setApplicationName("HTML5 Web Slideshow Generator")

    app = QApplication(sys.argv)
    project = Projwindow()
    project.show()

    sys.exit(app.exec())
