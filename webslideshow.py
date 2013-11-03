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

__version__ = '0.0.1'


class Projwindow(QMainWindow, Ui_WebSlideshow):

    ### CONSTANTS ###
    PPATH = QDir.homePath() + "/WebSlideshow Projects"  # Saved projects
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

        # Blank array to hold picture filepaths
        self.f_paths = []

        # Blank array to hold picture segments
        self.psegments = []

        # Custom widget to hold scroll content
        self.scr_stuff = QWidget()
        self.setMinimumWidth(700)
        self.scr_vlay = QVBoxLayout()

        # Call setupUI from UI file
        self.setupUi(self)

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
        # Connect buttons at bottom to actions
        self.buttonBox.accepted.connect(self.save_proj)
        self.buttonBox.rejected.connect(self.cancel_proj)


    ### BUTTON ACTIONS
    def edit_sli_lbl(self):
        self.lbl_numslides.setText("Number of slides:   <b>(%d)</b>" %
                                   self.sli_numslides.sliderPosition())


    def grow_psegments(self):
        # First, update the slide label
        self.lbl_numslides.setText("Number of slides:    <b>(%d)</b>" %
                                   self.sli_numslides.value())
        # If the bottom spacer exists, delete it.  We'll recreate it. 
        try:
            self.scr_vlay.removeItem(self.bot_space)
            self.bot_space.setParent(None)
            del self.bot_space
            #self.deleteLater()
        except:
            pass
        # Either remove or add child widgets
        if self.sli_numslides.value() < len(self.psegments):
            for i, item in enumerate(self.psegments):
                if i >= self.sli_numslides.value():
                    self.scr_vlay.removeWidget(item)
                    item.setParent(None)
                    item.deleteLater()
            self.psegments = self.psegments[0:self.sli_numslides.value()]
        else:
            for i in xrange(self.sli_numslides.value()):
                if i >= len(self.psegments):
                    # if we create object before drawing, pull default res
                    if not self.cb_resolution.currentText():
                        self.psegments.append(PictureSegment(i, self.RESOLUTIONS[0]))
                    else:
                        # otherwise, create a picturesegment and pass res
                        # to it so it can calculate its new dimensions
                        self.psegments.append(PictureSegment(i, self.cb_resolution.currentText()))
        for item in self.psegments:
            self.scr_vlay.addWidget(item)
            item.show()
        # Need to put a spacer at the end to push up the segments
        self.bot_space = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.scr_vlay.addSpacerItem(self.bot_space)
        self.scr_stuff.setLayout(self.scr_vlay)
        self.scrollArea.setWidget(self.scr_stuff)


    def change_res(self):
        # Forces viewport to adapt when res is changed
        for vp in self.psegments:
            vp.vp_setter(self.cb_resolution.currentText())
            if not vp.upic.isNull():
                vp.graphicsView.fitInView(vp.scene.sceneRect(), Qt.KeepAspectRatio)
                if vp.cb_type.currentText() == "Full screen":
                    vp.get_newres()
                    vp.msg_maker()
                elif vp.cb_type.currentText() == "Letterboxed":
                    if vp.upic.width() > vp.res[0]:
                        vp.get_newres()
                        vp.msg_maker()
                        vp.cb_type.setCurrentIndex(0)
                    elif vp.upic.height() > vp.res[1]:
                        vp.get_newres()
                        vp.msg_maker()
                        vp.cb_type.setCurrentIndex(0)
                    else:
                        vp.window_scale()


    def cancel_proj(self):
        # Cancels the project
        wbox = QMessageBox.warning(self, "Exit program?", 
                                   "Close the application without saving?",
                                   QMessageBox.Cancel | QMessageBox.Ok,
                                   QMessageBox.Cancel)
        if wbox == QMessageBox.Ok:
            sys.exit()


    def save_proj(self):
        self.val = 0
        progress = QProgressDialog("Saving current slideshow...", "Cancel", 0, 
                                   (len(self.psegments) + 3), self)
        progress.setWindowTitle("Saving Project")
        progress.setWindowModality(Qt.WindowModal)
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
        p = QDir()
        while(p.exists(self.PPATH + "/" + newtit)):
            newtit = tit + "-" + str(i)
            i = i + 1
        curprojf = self.PPATH + "/" + newtit
        try:
            p.mkdir(curprojf)
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
        # First resize and save the pix in the proj folder
        self.resize_pics(curprojf)
        # First big bump in the progress bar
        self.val = len(self.psegments)
        progress.setValue(self.val)
        self.resolution = [int(n) for n in self.cb_resolution.currentText().split("x")]
        self.captions = []
        for seg in self.psegments:
           self.captions.append(seg.le_caption.text())
        obj = HTML_Generator(tit, self.cb_effects.currentText(),
                             self.sli_numslides.value(), self.resolution, 
                             self.sb_duration.value(), self.captions)
        # Create HTML, CSS and JS files in project folder
        obj.gen_html(curprojf)
        self.val = self.val + 1
        progress.setValue(self.val)
        obj.gen_css(curprojf)
        self.val = self.val + 1
        progress.setValue(self.val)
        obj.gen_js(curprojf)
        self.val = self.val + 1
        progress.setValue(self.val)
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


    def resize_pics(self, dest):
        for seg in self.psegments:
            if seg.upic:
                # Then scale it properly if it's mean to be full-screened
                # We'll do nothing to Letterboxed pictures and let the HTML
                # handle them.
                if seg.cb_type.currentText() == "Full screen":
                    seg.newpic = seg.upic.scaled(seg.newres[0], seg.newres[1])
                    print("Cropping to {0}".format(seg.cropdims))
                    # Crop the pic to the preset cropped dimensions
                    seg.newpic = seg.newpic.copy(*seg.cropdims)
                elif seg.cb_type.currentText() == "Letterboxed":
                    seg.newpic = seg.upic
                    print("Preserving this photo's size...")
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
        self.cur_mode = self.cb_type.currentText()

        if self.cur_mode == self.SLIDE_TYPES[0]:
            # Fullscreen it!
            if not self.upic.isNull():
                self.get_newres()
                # Calculate offsets to center the pixmap item
                self.pmi.setOffset(0, 0)
                self.resize_scene(self.cb_type.currentText())
                self.graphicsView.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
            else:
                print("self.upic does not exist")
            # Re-enable upload button
            self.btn_upload.setEnabled(True)
        elif self.cur_mode == self.SLIDE_TYPES[1]:
            # Letterbox it if there is a picture present
            if not self.upic.isNull():
                self.window_scale()
            # Re-enable upload button
            self.btn_upload.setEnabled(True)
        else:
            if self.cur_mode == self.SLIDE_TYPES[2]:
                # Blank white it!
                # Need to blank the previous picture and all derivations
                self.clean_prev()
                self.set_vp_bg(Qt.white)
            elif self.cur_mode == self.SLIDE_TYPES[3]:
                # Blank black it!
                # Need to blank the previous picture and all derivations
                self.clean_prev()
                self.set_vp_bg(Qt.black)
            # Disable upload button
            self.btn_upload.setDisabled(True)
        self.msg_maker()


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
            print("Line 370: {0}".format(e))


    def rotate_pic(self):
        # rotates the uploaded pixmap 90 degrees clockwise
        # and recalculates its dimensions
        # then redraws it in the QGraphicsView
        trans = QTransform()
        self.upic.transformed(trans.rotate(90))
        self.clean_prev()


    # btn_upload slot
    def upload_pic(self):
        # Let's talk to our QSettings object
        settings = QSettings()
        # f_tup is a tuple
        f_tup = QFileDialog.getOpenFileName(self, "Select Image",
                                                 settings.value("current_folder"),
                                                 "Image Files "
                                                 "( *.png *.jpg *.bmp)")

        if f_tup[0]:
            # Clean up previous photo if it exists
            self.clean_prev()
            # we only want the image itself
            self.upic = QPixmap(f_tup[0])
            # We also want the file path info b/c we'll set last directory
            self.finfo = QDir(f_tup[0])
            # Set the current_folder QSettings from path
            settings.setValue("current_folder", self.finfo.path())
            settings.sync()
            self.pmi = self.scene.addPixmap(self.upic)
            # If someone selects Letterboxed, make sure the pic is
            # smaller than the desired resolution
            if self.cb_type.currentText() == "Letterboxed":
                if self.upic.width() > self.res[0]:
                    self.cb_type.setCurrentIndex(0)
                    self.resize_scene("Full screen")
                elif self.upic.height() > self.res[1]:
                    self.cb_type.setCurrentIndex(0)
                    self.resize_scene("Full screen")
                else:
                    self.resize_scene(self.cb_type.currentText())
                    self.window_scale()
            else:
                self.resize_scene(self.cb_type.currentText())
                self.graphicsView.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
            self.get_newres()
            self.gitem = QGraphicsTextItem(str(self.upic.width()) + "x" + str(self.upic.height()))
            self.gitem.setFlags(QGraphicsItem.ItemIgnoresTransformations)
            self.gitem.setZValue(4)
            self.scene.addItem(self.gitem)
            self.rect = self.scene.addRect((self.gitem.boundingRect()), Qt.NoPen,
                                           self.WHITE_TRANS)
            self.rect.setFlags(QGraphicsItem.ItemIgnoresTransformations)
            # gitem (resolution) sits on top of rect (res background square)
            self.rect.setZValue(3)

            # Finally, call our message maker
            self.msg_maker()


    def commit_desc(self):
        # When called, commits caption to PictureSegment object variable
        self.caption = self.le_caption.text()


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


    def msg_maker(self):
        # Depending on image size and selected resolution,
        # give a message in the label

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
                "means that its size will be unmodified and it will be centered "
                "in the slideshow.")
        MSG7 = ("This image is bigger than the target resolution. "
                "It will be resized and/or cropped to compensate, but it will "
                "look OK.")
        W_MSG = ("<font color='red'>The quality of this image might be "
                 "degraded as a result.</font>")

        if not self.upic.isNull():
            if self.upic.width() == self.res[0]:
                if self.upic.height() < self.res[1]:
                    # TODO if letterbox or if full, etc
                    self.lbl_warning.setText(MSG2 + W_MSG)
                elif self.upic.height() > self.res[1]:
                    self.lbl_warning.setText(MSG4)
                else:
                    self.lbl_warning.setText(MSG1)
            elif self.upic.width() < self.res[0]:
                if self.upic.height() <= self.res[1]:
                    # The image is smaller in both dimensions
                    # Let's give two different messages based upon slide type
                    if self.cb_type.currentText() == "Letterboxed":
                        self.lbl_warning.setText(MSG6)
                    elif self.cb_type.currentText() == "Full screen":
                        self.lbl_warning.setText(MSG5 + W_MSG)
                elif self.upic.height() > self.res[1]:
                    self.lbl_warning.setText(MSG3 + W_MSG)
                else:
                    self.lbl_warning.setText(MSG3 + W_MSG)
            else:
                if self.upic.height() < self.res[1]:
                    self.lbl_warning.setText(MSG3 + W_MSG)
                elif self.upic.height() > self.res[1]:
                    self.lbl_warning.setText(MSG7)
                else:
                    self.lbl_warning.setText(MSG4)
        else:
            self.lbl_warning.setText("")


    def window_scale(self):
        try:
            self.boxgroup.scene().removeItem(self.boxgroup)
        except Exception as e:
            print("Line 512: {0}".format(e))
        # If Letterboxed mode is selected, scale the uploaded pic
        # in the viewport box to reflect this
        # First, setSceneRect for letterboxed mode
        self.resize_scene(self.cb_type.currentText())

        # Calculate offsets to center the pixmap item
        left_offset = (self.res[0] - self.upic.width()) / 2
        top_offset = (self.res[1] - self.upic.height()) / 2
        self.pmi.setOffset(left_offset, top_offset)

        # Set background for letterboxed mode to GRAY_BG
        self.set_vp_bg(self.GRAY_BG)
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


    def get_newres(self):
        # calculates new resolution of a pic based on combobox selection
        # draws red box overlay on picture as well

        boxes = []
        dims = [self.upic.width(), self.upic.height()]

        # Reset the gray bg color on the viewport if it exists
        if self.cb_type.currentText() == "Full screen":
            self.set_vp_bg()

        # remove the red overlay boxes if the item has them
        try:
            self.boxgroup.scene().removeItem(self.boxgroup)
            del self.boxgroup
        except Exception as e:
            print("Line 570: {0}".format(e))

        for i, dim in enumerate(dims):
            # other_ind will be 1 if i is 0, 0 if i is 1
            other_ind = 1 - i
            other = dims[other_ind]
            x = self.res[i] / float(dim)
            other_res = int(x * dims[other_ind])

            if other_res >= self.res[other_ind]:
            # only move forward if the other dimension
            # is equal or greater to its counterpart
                if i == 0:
                    # we scaled width and will crop height
                    self.newres = [self.res[0], other_res]
                    leftover = other_res - self.res[1]
                    # We need to divide by x so the rects show what will
                    # really be cut from the original photo
                    self.bx1 = QRectF(0, 0, dims[0], (0.5 * leftover) / x)
                    self.bx2 = QRectF(0, (other - ((0.5 * leftover) / x)),
                                      dims[0], (0.5 * leftover) / x)
                    # Set self.cropdims for when we save the resized image
                    self.cropdims = (0, int(0.5 * leftover), int(self.res[0]),
                                     int(self.res[1]))
                else:
                    # we scaled height and will crop width
                    self.newres = [other_res, self.res[1]]
                    leftover = other_res - self.res[0]
                    # We need to divide by x so the rects show what will
                    # really be cut from the original photo
                    self.bx1 = QRectF(0, 0, (0.5 * leftover) / x, dims[1])
                    self.bx2 = QRectF((other - ((0.5 * leftover) /x)), 0,
                                      (0.5 * leftover) / x, dims[1])
                    # Set self.cropdims for when we save the resized image
                    self.cropdims = (int(0.5 * leftover), 0,
                                     int(self.res[0]),
                                     int(self.res[1]))
            else:
                # let's move to the other one, it must be bigger
                continue

        print("{0}'s new res is {1}".format(dims, self.newres))
        # We only want these red overlay boxes on full screen pictures
        if self.cb_type.currentText() == "Full screen":
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
