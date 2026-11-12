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
from htmlgenerator import HTML_Generator
from slidelayout import (compute_layout, FULL_SCREEN, LETTERBOXED, ENLARGE,
                         BLANK_WHITE, BLANK_BLACK, PICTURE_MODES)

__version__ = '1.0'


def read_image(path):
    """Read a picture file into a QImage (None if it can't be read).

    Used for both the preview thumbnail and the final save, so both see the picture
    the same way. EXIF rotation is not applied (as before); call
    reader.setAutoTransform(True) here if phone photos should be turned upright.
    """
    img = QImageReader(path).read()
    return None if img.isNull() else img


class Projwindow(QMainWindow):

    ### CONSTANTS ###
    PPATH = QDir.homePath() + "/Simple Web Slideshow Projects"  # Saved projects
    DEF_DURATION = 20               # initial / default duration
    MIN_DURATION = 1                  # min duration i.e. time between slides
    MAX_DURATION = 60                 # max duration i.e. time between slides
    MAX_SLIDES = 100                  # max number of slides
    EFFECTS = ["Blur", "Abrupt", "HorizontalSlide", "VerticalSlide"]
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
        super(Projwindow, self).__init__(parent)

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
        self.psegments = []

        # Custom widget to hold scroll content
        self.scr_stuff = QWidget()
        self.scr_vlay = QVBoxLayout()
        self.scr_vlay.addStretch(1)

        # Build UI programmatically (replaces ui_webslideshow.py)
        self._build_ui()

        # More scroll area work, post-UI construction
        self.scr_stuff.setLayout(self.scr_vlay)
        self.scrollArea.setWidget(self.scr_stuff)

        # populate comboboxes etc
        for effect in self.EFFECTS:
            self.cb_effects.addItem(effect)

        self.le_duration.setText(str(self.DEF_DURATION))
        
        # Tooltip and validation setup for duration field
        tooltip_msg = "Seconds between slides. Enter a number from {0} to {1}.".format(
            self.MIN_DURATION, self.MAX_DURATION)
        self.le_duration.setToolTip(tooltip_msg)

        # Make duration text field compact (approx. 4 digits wide)
        self.le_duration.setMaximumWidth(55)
        self.le_duration.setMaxLength(4)
        self.le_duration.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Replace warning label layout with total slideshow duration label (right justified)
        self.gridLayout.removeWidget(self.le_duration)
        dur_hbox = QHBoxLayout()
        dur_hbox.addWidget(self.le_duration)
        
        self.lbl_total_duration = QLabel(self.groupBox)
        self.lbl_total_duration.setStyleSheet("color: #444; font-weight: normal;")
        self.lbl_total_duration.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.lbl_total_duration.setToolTip("This is the current duration of the slideshow.\n"
            "This does *not* include the seconds for the title screen.")
        dur_hbox.addWidget(self.lbl_total_duration, 1)  # stretch factor 1 pushes it right
        
        self.gridLayout.addLayout(dur_hbox, 2, 1, 1, 2)
        
        self.le_duration.textChanged.connect(self.check_duration)
        self.lbl_numslides.setToolTip('Pick a value from 2 to {}.'.format(self.MAX_SLIDES))
        self.sli_numslides.setMaximum(self.MAX_SLIDES)

        for label, wxh in self.RESOLUTIONS:
            self.cb_resolution.addItem(label, wxh)
        self.cb_resolution.setCurrentIndex(self.DEF_RESOLUTION_INDEX)

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

        # Initial calculation for total duration display
        self.update_total_duration()

    def _build_ui(self):
        """Programmatically builds the main window UI with increased width for caption breathing room."""
        self.setObjectName("WebSlideshow")
        self.resize(720, 655)
        self.setMinimumSize(QSize(720, 650))
        self.setWindowIcon(QIcon('Video-Folder.png'))

        # Actions
        self.actionNew_Slideshow = QAction("New Slideshow", self)
        self.actionExit = QAction("Exit", self)
        self.actionSave = QAction("Save", self)
        self.actionAbout_Simple_Web_Slideshow = QAction("About Simple Web Slideshow", self)

        # Central Widget
        self.centralwidget = QWidget(self)
        self.centralwidget.setMinimumSize(QSize(710, 0))
        self.verticalLayout = QVBoxLayout(self.centralwidget)

        # Group Box: Web Slideshow Settings
        self.groupBox = QGroupBox("Web Slideshow Settings", self.centralwidget)
        self.groupBox.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed))
        self.groupBox.setMinimumSize(QSize(702, 0))
        self.groupBox.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)

        self.horizontalLayout_2 = QHBoxLayout(self.groupBox)
        self.gridLayout = QGridLayout()
        self.gridLayout.setHorizontalSpacing(12)
        self.gridLayout.setVerticalSpacing(8)
        self.gridLayout.setSizeConstraint(QLayout.SetDefaultConstraint)

        self.lbl_title = QLabel("Slideshow title:", self.groupBox)
        self.le_title = QLineEdit(self.groupBox)
        self.le_title.setPlaceholderText("Enter a title for this slideshow")
        self.le_title.setToolTip("Currently, you must pick a title.\n"
            "If you don't want one, just enter a blank space and the title screen\n"
            "will appear without text on it.\n"
            "If you enter nothing, the word 'Slideshow' will appear on the title screen.")
        self.le_title.setFocusPolicy(Qt.ClickFocus)

        self.lbl_effect = QLabel("Slide transition effect:", self.groupBox)
        self.cb_effects = QComboBox(self.groupBox)

        self.lbl_duration = QLabel("Slide duration (seconds):", self.groupBox)
        self.le_duration = QLineEdit(self.groupBox)
        self.le_duration.setMaxLength(4)

        self.lbl_numslides = QLabel("Number of slides:", self.groupBox)
        
        self.sli_numslides = QSlider(Qt.Horizontal, self.groupBox)
        self.sli_numslides.setMinimum(2)
        self.sli_numslides.setMaximum(100)
        self.sli_numslides.setPageStep(1)
        self.sli_numslides.setTracking(False)
        self.sli_numslides.setTickPosition(
            QSlider.TicksBelow if sys.platform == "darwin" else QSlider.TicksBothSides)

        self.lbl_resolution = QLabel("Optimize for resolution:", self.groupBox)
        self.cb_resolution = QComboBox(self.groupBox)

        # Add widgets to grid
        self.gridLayout.addWidget(self.lbl_title, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.le_title, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.lbl_effect, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.cb_effects, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.lbl_duration, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.le_duration, 2, 1, 1, 1)
        self.gridLayout.addWidget(self.lbl_numslides, 3, 0, 1, 1)
        self.gridLayout.addWidget(self.sli_numslides, 3, 1, 1, 1)
        self.gridLayout.addWidget(self.lbl_resolution, 4, 0, 1, 1)
        self.gridLayout.addWidget(self.cb_resolution, 4, 1, 1, 1)

        self.horizontalLayout_2.addLayout(self.gridLayout)
        self.verticalLayout.addWidget(self.groupBox)

        # Scroll Area
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.verticalLayout.addWidget(self.scrollArea)

        # Bottom Button Box Layout
        self.horizontalLayout = QHBoxLayout()
        self.horizontalSpacer_11 = QSpacerItem(408, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(self.horizontalSpacer_11)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Save, self.centralwidget)
        self.horizontalLayout.addWidget(self.buttonBox)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.setCentralWidget(self.centralwidget)

        # Menu Bar & Status Bar
        self.menubar = QMenuBar(self)
        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)

        self.menuFile = self.menubar.addMenu("File")
        self.menuAbout = self.menubar.addMenu("About")

        self.menuFile.addAction(self.actionNew_Slideshow)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)

        self.menuAbout.addAction(self.actionAbout_Simple_Web_Slideshow)

        # Set Window Title
        self.setWindowTitle("Simple Web Slideshow")

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
        txt = text.strip()
        valid = True
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
        else:
            self.le_duration.setStyleSheet(
                "QLineEdit {{ border: 1px solid #c00; color: #c00; }}")
        
        self.update_total_duration()

    def update_total_duration(self):
        dur_val = self.get_duration()
        num_slides = self.sli_numslides.value()
        total_seconds = dur_val * num_slides

        # Automatically clamp and update text field value after the warning popup shows
        txt = self.le_duration.text().strip()
        if txt != "":
            try:
                val = int(txt)
                if val < self.MIN_DURATION or val > self.MAX_DURATION:
                    clamped_val = max(self.MIN_DURATION, min(val, self.MAX_DURATION))
                    self.le_duration.blockSignals(True)
                    self.le_duration.setText(str(clamped_val))
                    self.le_duration.blockSignals(False)
            except ValueError:
                pass

        if total_seconds < 60:
            time_str = f"{total_seconds} seconds"
        else:
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            min_word = "minute" if minutes == 1 else "minutes"
            if seconds == 0:
                time_str = f"{minutes} {min_word}"
            else:
                time_str = f"{minutes} {min_word}, {seconds} seconds"

        self.lbl_total_duration.setText(
            f"Current slideshow duration:&nbsp;&nbsp;<span style='font-weight:bold;'>{time_str}</span>&nbsp;&nbsp;&nbsp;")

    def edit_sli_lbl(self):
        self.lbl_numslides.setText("Number of slides:   <b>(%d)</b>" %
                                   self.sli_numslides.sliderPosition())
        self.update_total_duration()

    def grow_psegments(self):
        self.lbl_numslides.setText("Number of slides:    <b>(%d)</b>" %
                                   self.sli_numslides.value())

        data = self.cb_resolution.currentData()
        if data:
            res = data
        else:
            res = self.RESOLUTIONS[0][1]

        if self.sli_numslides.value() < len(self.psegments):
            for i, item in enumerate(self.psegments):
                if i >= self.sli_numslides.value():
                    self.scr_vlay.removeWidget(item)
                    item.setParent(None)
                    item.deleteLater()
            self.psegments = self.psegments[0:self.sli_numslides.value()]
        else:
            for i in range(self.sli_numslides.value()):
                if i >= len(self.psegments):
                    item = PictureSegment(i, res)
                    self.psegments.append(item)
                    self.scr_vlay.insertWidget(i, item)
                    item.show()
        
        self.update_total_duration()

    def change_res(self):
        res = self.cb_resolution.currentData() or self.RESOLUTIONS[0][1]
        for vp in self.psegments:
            vp.vp_setter(res)
            vp.refresh_preview()

    def cancel_proj(self):
        wbox = QMessageBox.warning(self, "Exit program?",
                                   "Close the application without saving?",
                                   QMessageBox.Cancel | QMessageBox.Ok,
                                   QMessageBox.Cancel)
        if wbox == QMessageBox.Ok:
            self.close()

    def save_proj(self):
        # Check every slide up front, before anything is written to disk
        problems = [seg for seg in self.psegments
                    if seg.cb_type.currentText() in PICTURE_MODES
                    and not (seg.has_image and QFileInfo(seg.img_path).isFile())]
        if problems:
            QMessageBox.warning(
                self, "Missing pictures",
                "These slides have no picture (or the picture file has moved): {0}.\n\n"
                "Upload a picture for each, or change the slide type to a blank slide.".format(
                    ", ".join(str(seg.num + 1) for seg in problems)))
            return

        val = 0
        progress = QProgressDialog("Saving current slideshow...", "Cancel", 0, 
                                   (len(self.psegments) + 3), self)
        progress.setWindowTitle("Saving Project")
        progress.setWindowModality(Qt.WindowModal)
        progress.setMinimumDuration(0)
        progress.setAutoReset(False)
        progress.setValue(0)
        progress.setLabelText("Resizing and saving pictures...")
        if self.le_title.text():
            tit = self.le_title.text()
        else:
            tit = "Slideshow"
        i = 1
        newtit = tit
        for ch in [",", " ", "?", "!", ":", ";", "(", ")", "."]:
            if ch in tit:
                newtit = newtit.replace(ch, "-")
        newtit = newtit.replace("--", "-")
        newtit = newtit.lower()
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
        if not self.resize_pics(curprojf):
            progress.cancel()
            return
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
        self.sli_numslides.setValue(2)
        self.le_duration.setText(str(self.DEF_DURATION))
        self.cb_resolution.setCurrentIndex(self.DEF_RESOLUTION_INDEX)
        for seg in self.psegments:
            seg.clean_prev()
            seg.le_caption.clear()
            seg.cb_type.setCurrentIndex(0)
            seg.lbl_warning.clear()

    def about_dlg(self):
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
                arranged by contacting brimlar at its GitHub page:<br /><br />\
                <a href='https://github.com/brimlar/simple-web-slideshow'>\
                https://github.com/brimlar/simple-web-slideshow</a>")
        dlg.setText(text)
        dlg.exec()

    def resize_pics(self, dest):
        """Render and save every slide. Returns False (after telling the user) on failure."""
        for seg in self.psegments:
            pic = seg.render_output()
            if pic is None:
                QMessageBox.warning(self, "Error",
                                    "Could not read the picture for slide {0}:\n{1}".format(
                                        seg.num + 1, seg.img_path))
                return False
            path = dest + "/" + str(seg.num + 1) + ".jpg"
            if not pic.save(path):
                QMessageBox.warning(self, "Error",
                                    "Could not save slide {0}:\n{1}".format(seg.num + 1, path))
                return False
        return True


class PictureSegment(QWidget):

    # CONSTANTS
    WIDE_BOX = QSize(192, 108)                  # 16:9 ratio box (192x108)
    STD_BOX = QSize(144, 108)                   # 4:3 ratio box scaled to match 108 height
    WHITE_TRANS = QColor(255, 255, 255, 200)    # Transparent white
    RED_TRANS = QColor(255, 0, 0, 120)          # Transparent red
    GRAY_BG = QColor(34, 34, 34, 255)           # Dark gray background
    SLIDE_TYPES = [FULL_SCREEN, LETTERBOXED, ENLARGE, BLANK_WHITE, BLANK_BLACK]
    PREVIEW_MAX = 640                           # longest side (px) of the thumbnail kept for the preview
    SCALE_MODE = Qt.SmoothTransformation        # how saved pictures are scaled (Qt.FastTransformation = old look)
    WARNING_LINES = 4                           # lines of warning text each slide reserves room for

    def __init__(self, num, res, parent=None):
        super(PictureSegment, self).__init__(parent)

        # Others
        self.num = num

        # The full-size picture is NOT kept in memory: only its path, size and rotation,
        # plus a small thumbnail inside the preview scene. It is re-read from disk at save time.
        self.img_path = None        # source file, or None when the slide has no picture
        self.img_w = self.img_h = 0 # picture size after rotation
        self.rotation = 0           # degrees clockwise, in steps of 90
        self.pmi = None             # the thumbnail's item in the preview scene
        self.lay = None             # last SlideLayout shown in the preview
        self.boxgroup = None        # red crop-band overlay (Full screen only)

        # Get floats out of the resolution b/c we need arith later
        self.res = [int(n) for n in res.split("x")]

        # Custom widgets that aren't shown
        self.scene = QGraphicsScene()

        # Build the widgets and layout
        self._build_ui()

        # Call vp_setter once to initialize widget size
        self.vp_setter(res)
        # Add the scene to the graphicsView upon creation
        self.graphicsView.setScene(self.scene)

        # Inject slide type strings into combobox
        for typ in self.SLIDE_TYPES:
            self.cb_type.addItem(typ)

        # Some post draw customizations
        self.lbl_bignum.setText(str(num + 1))
        self.lbl_warning.clear()
        self.lbl_warning.setWordWrap(True)
        self.lbl_imgres.setText("")

        # Signals and slots
        self.btn_rotate.clicked.connect(self.rotate_pic)
        self.btn_upload.clicked.connect(self.upload_pic)
        self.le_caption.editingFinished.connect(self.commit_desc)
        self.le_caption.selectionChanged.connect(self.commit_desc)
        self.le_caption.returnPressed.connect(self.commit_desc)
        self.cb_type.currentIndexChanged.connect(self.change_sltype)

    def _build_ui(self):
        """Builds this slide's widgets and layout in code (replaces ui_picturesegment.py)."""
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
        self.setMinimumSize(QSize(670, 198))
        self.setMaximumHeight(198)

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 16, 0)  # Adds a 16px right buffer

        # Main grid. Columns: 0 = big number, 1-3 = preview column, 4 = right-hand controls
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setVerticalSpacing(1)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)

        # Big slide number
        self.lbl_bignum = QLabel(self)
        self.lbl_bignum.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored))
        font = QFont()
        font.setPointSize(24)
        font.setBold(False)
        font.setItalic(False)
        self.lbl_bignum.setFont(font)
        self.lbl_bignum.setAlignment(Qt.AlignCenter)
        self.lbl_bignum.setMargin(0)
        self.lbl_bignum.setText("1")

        # Image resolution label (above the preview)
        self.lbl_imgres = QLabel(self)
        self.lbl_imgres.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed))
        self.lbl_imgres.setAlignment(Qt.AlignCenter)
        self.lbl_imgres.setStyleSheet(
            "font-weight: bold; color: #666; "
            "margin: 0px; padding: 0px;"
        )

        # Calculate height dynamically based on the current font's line height plus a tiny margin
        font_metrics = self.lbl_imgres.fontMetrics()
        self.lbl_imgres.setFixedHeight(font_metrics.lineSpacing() + 4)

        # Preview (size is set by vp_setter() to match target aspect ratio, locked down with Fixed policy)
        self.graphicsView = QGraphicsView(self)
        self.graphicsView.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.graphicsView.setAlignment(Qt.AlignCenter)
        self.graphicsView.setRenderHint(QPainter.SmoothPixmapTransform)   # the preview shows a downscaled thumbnail

        # Upload button (below the preview)
        self.btn_upload = QPushButton("Upload New Image", self)
        self.btn_upload.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Right-hand controls: caption, slide type + rotate, warning text
        self.gridLayout = QGridLayout()
        self.gridLayout.setContentsMargins(9, 6, -1, -1)

        self.lbl_caption = QLabel("Slide caption:", self)
        self.lbl_caption.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred))

        self.le_caption = QLineEdit(self)
        caption_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        caption_policy.setHorizontalStretch(1)
        self.le_caption.setSizePolicy(caption_policy)
        self.le_caption.setPlaceholderText("Enter a caption for this image, or leave blank")

        self.lbl_type = QLabel("Slide type:", self)

        self.cb_type = QComboBox(self)
        self.cb_type.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.cb_type.setFocusPolicy(Qt.StrongFocus)

        self.btn_rotate = QPushButton("Rotate clockwise", self)
        self.btn_rotate.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

        self.lbl_warning = QLabel(self)
        self.lbl_warning.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))
        self.lbl_warning.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.lbl_warning.setFixedHeight(
            self.lbl_warning.fontMetrics().lineSpacing() * self.WARNING_LINES)

        self.gridLayout.addWidget(self.lbl_caption, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.le_caption, 0, 1, 1, 3)
        self.gridLayout.addWidget(self.lbl_type, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.cb_type, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.btn_rotate, 1, 2, 1, 1)
        self.gridLayout.addItem(
            QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum), 1, 3, 1, 1)
        self.gridLayout.addWidget(self.lbl_warning, 2, 0, 1, 4)

        # Place everything in the main grid
        self.gridLayout_2.addWidget(self.lbl_imgres, 0, 1, 1, 3, Qt.AlignCenter)
        self.gridLayout_2.addWidget(self.lbl_bignum, 1, 0, 1, 1, Qt.AlignCenter)
        self.gridLayout_2.addWidget(self.graphicsView, 1, 1, 1, 3, Qt.AlignCenter)
        self.gridLayout_2.addWidget(self.btn_upload, 2, 1, 1, 3, Qt.AlignCenter)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 4, 2, 1, Qt.AlignTop)
        self.gridLayout_2.addItem(
            QSpacerItem(18, 20, QSizePolicy.Minimum, QSizePolicy.Minimum), 1, 1, 1, 1)
        self.gridLayout_2.addItem(
            QSpacerItem(13, 20, QSizePolicy.Minimum, QSizePolicy.Minimum), 1, 3, 1, 1)
        self.gridLayout_2.setColumnStretch(4, 1)

        self.verticalLayout.addLayout(self.gridLayout_2)

        # Separator line under each segment
        self.line = QFrame(self)
        self.line.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line)

    @property
    def has_image(self):
        return self.img_path is not None

    def update_res_label(self):
        if not self.has_image:
            self.lbl_imgres.setText("")
        elif self.cb_type.currentText() in (LETTERBOXED, ENLARGE) and self.lay is not None:
            self.lbl_imgres.setText(f"{self.lay.scaled[0]}x{self.lay.scaled[1]}")
        else:
            self.lbl_imgres.setText(f"{self.img_w}x{self.img_h}")

    # cb_type slot
    def change_sltype(self):
        cur_mode = self.cb_type.currentText()

        if cur_mode in (BLANK_WHITE, BLANK_BLACK):
            self.clean_prev()
            self.set_vp_bg(Qt.white if cur_mode == BLANK_WHITE else Qt.black)
            self.btn_upload.setDisabled(True)
        else:
            self.set_vp_bg(None if cur_mode == FULL_SCREEN else self.GRAY_BG)
            self.btn_upload.setEnabled(True)
        self.refresh_preview()

    def clean_prev(self):
        self.remove_cropboxes()
        self.pmi = None
        self.scene.clear()
        self.scene.setSceneRect(0, 0, 0, 0)
        self.img_path = None
        self.img_w = self.img_h = 0
        self.rotation = 0
        self.lay = None
        self.lbl_imgres.setText("")

    def rotate_pic(self):
        if not self.has_image:
            return
        self.rotation = (self.rotation + 90) % 360
        self.img_w, self.img_h = self.img_h, self.img_w
        self.pmi.setPixmap(self.pmi.pixmap().transformed(QTransform().rotate(90)))
        self.refresh_preview()

    # btn_upload slot
    def upload_pic(self):
        settings = QSettings()
        dir_path = settings.value("current_folder", QDir.homePath())

        filter_str = (
            "Images (*.png *.jpg *.jpeg *.webp *.bmp *.tif *.tiff);"
            ";JPEG Images (*.jpg *.jpeg)"
            ";PNG Images (*.png)"
            ";WebP Images (*.webp)"
        )

        fname, _ = QFileDialog.getOpenFileName(
            self,
            "Select Picture for Slide",
            dir_path,
            filter_str
        )
        if not fname:
            return

        # Load first: if the file is bad, the slide keeps whatever it had before
        img = read_image(fname)
        if img is None:
            QMessageBox.warning(self, "Error", "Could not load this picture:\n" + fname)
            return

        settings.setValue("current_folder", QFileInfo(fname).absolutePath())
        settings.sync()

        self.clean_prev()
        self.img_path = fname
        self.img_w, self.img_h = img.width(), img.height()
        self.pmi = self.scene.addPixmap(self._make_thumb(img))
        self.refresh_preview()      # the full-size QImage is released when this method returns

    def _make_thumb(self, img):
        """Small stand-in for the preview. The scene still works in real picture pixels."""
        if max(img.width(), img.height()) > self.PREVIEW_MAX:
            img = img.scaled(self.PREVIEW_MAX, self.PREVIEW_MAX,
                             Qt.KeepAspectRatio, Qt.SmoothTransformation)
        return QPixmap.fromImage(img)

    def refresh_preview(self):
        """Lay the picture out in the preview exactly as it will be saved."""
        mode = self.cb_type.currentText()
        self.remove_cropboxes()
        self.lay = None
        if self.has_image and mode in PICTURE_MODES:
            lay = compute_layout(mode, self.img_w, self.img_h, self.res[0], self.res[1])
            self.lay = lay
            if lay.crop:
                # Full screen: show the whole picture; red bands mark what the crop removes
                self.scene.setSceneRect(0, 0, self.img_w, self.img_h)
                size, pos = (self.img_w, self.img_h), (0, 0)
            else:
                # Letterboxed / Enlarge: show the whole slide frame with the picture placed in it
                self.scene.setSceneRect(0, 0, self.res[0], self.res[1])
                size, pos = lay.scaled, lay.place
            thumb = self.pmi.pixmap()
            self.pmi.setTransform(QTransform.fromScale(size[0] / thumb.width(),
                                                       size[1] / thumb.height()))
            self.pmi.setPos(*pos)
            if lay.bands:
                boxes = [self.scene.addRect(QRectF(*b), Qt.NoPen, self.RED_TRANS)
                         for b in lay.bands]
                self.boxgroup = self.scene.createItemGroup(boxes)
                self.boxgroup.setZValue(1)
            self.graphicsView.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        self.update_res_label()
        self.msg_maker(mode)

    def render_output(self):
        """Build the final slide picture from scratch, as a QImage.

        Returns None if the source picture can't be read. Nothing here depends on what
        the preview is currently showing: the size and crop come straight from
        compute_layout(), and the picture is re-read from disk.
        """
        mode = self.cb_type.currentText()
        res_w, res_h = self.res
        if mode not in PICTURE_MODES:
            canvas = QImage(res_w, res_h, QImage.Format_RGB32)
            canvas.fill(Qt.white if mode == BLANK_WHITE else Qt.black)
            return canvas
        if not self.has_image:
            return None
        img = read_image(self.img_path)
        if img is None:
            return None
        if self.rotation:
            img = img.transformed(QTransform().rotate(self.rotation))
        lay = compute_layout(mode, img.width(), img.height(), res_w, res_h)
        out = img.scaled(lay.scaled[0], lay.scaled[1], Qt.IgnoreAspectRatio, self.SCALE_MODE)
        if lay.crop:
            out = out.copy(*lay.crop)
        return out

    def commit_desc(self):
        self.caption = self.le_caption.text()

    def vp_setter(self, res):
        self.res = [int(n) for n in res.split("x")]
        self.graphicsView.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        if round(float(self.res[0]) / float(self.res[1]), 1) == 1.8:
            self.graphicsView.setFixedSize(self.WIDE_BOX)
        else:
            self.graphicsView.setFixedSize(self.STD_BOX)

    def msg_maker(self, mode):
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
        MSG9 = ("<b><font color='red'>Warning</font></b>: This image is smaller "
                "than the target resolution, and enlarging it to fit the first "
                "border will <b>stretch the image</b>.")
        MSG10 = ("The image already meets or exceeds the first border without "
                 "needing to stretch the image.  It will look fine, centered "
                 "with letterboxes on the other side.")
        W_MSG = ("<font color='red'>The quality of this image might be "
                 "degraded as a result.</font>")

        if self.has_image:
            if mode == "Letterboxed":
                if self.lay.scaled == (self.res[0], self.res[1]):
                    self.lbl_warning.setText(MSG8)
                else:
                    self.lbl_warning.setText(MSG6)
            elif mode == "Enlarge to first border":
                if self.img_w >= self.res[0] or self.img_h >= self.res[1]:
                    self.lbl_warning.setText(MSG10)
                else:
                    self.lbl_warning.setText(MSG9 + " " + W_MSG)
            elif self.img_w == self.res[0]:
                if self.img_h < self.res[1]:
                    self.lbl_warning.setText(MSG2 + W_MSG)
                elif self.img_h > self.res[1]:
                    self.lbl_warning.setText(MSG4)
                else:
                    self.lbl_warning.setText(MSG1)
            elif self.img_w < self.res[0]:
                if self.img_h <= self.res[1]:
                    self.lbl_warning.setText(MSG5 + W_MSG)
                else:
                    self.lbl_warning.setText(MSG3 + W_MSG)
            else:
                if self.img_h < self.res[1]:
                    self.lbl_warning.setText(MSG2 + W_MSG)
                elif self.img_h > self.res[1]:
                    self.lbl_warning.setText(MSG7)
                else:
                    self.lbl_warning.setText(MSG4)
        else:
            self.lbl_warning.setText("")

    def set_vp_bg(self, color=None):
        if color:
            brush = QBrush(color)
        else:
            brush = Qt.NoBrush
        self.graphicsView.setBackgroundBrush(brush)

    def remove_cropboxes(self):
        grp = self.boxgroup
        self.boxgroup = None
        if grp is not None and grp.scene() is not None:
            grp.scene().removeItem(grp)


if __name__ == '__main__':
    QCoreApplication.setOrganizationName("brerin.org")
    QCoreApplication.setOrganizationDomain("brerin.org")
    QCoreApplication.setApplicationName("HTML5 Web Slideshow Generator")

    app = QApplication(sys.argv)
    project = Projwindow()
    project.show()

    sys.exit(app.exec())