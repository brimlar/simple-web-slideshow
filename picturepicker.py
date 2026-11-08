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

class Picture_Picker(QDialog):

    def __init__(self, parent=None):
        super(Picture_Picker, self).__init__(parent)

        self.setWindowTitle("Select an image file")

        # The original implementation subclassed QFileDialog and poked at its
        # internal layout to embed a live preview. That internal layout changed
        # in Qt6, so this was rewritten as a small purpose-made dialog that
        # gives the same UX: a button to browse for an image and a preview
        # label that updates as you pick files.
        layout = QVBoxLayout(self)

        self.l = QLabel()
           # Don't force the label to fill a square; let it size to the scaled
           # preview so aspect ratio is preserved. A generous max keeps the
           # dialog from getting huge on big images.
        self.l.setMinimumSize(300, 200)
        self.l.setAlignment(Qt.AlignCenter)
        self.l.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.l)

        self.browse = QPushButton("Browse...")
        layout.addWidget(self.browse)

          # Accept/Reject so exec_() returns the right value and the dialog
          # can be dismissed with a Cancel button.
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.finfo = None
        self.selected_file = None

        self.browse.clicked.connect(self.browse_file)

    def browse_file(self):
        # Qt6's getOpenFileName returns (files, filter); unpack the first.
        files, _ = QFileDialog.getOpenFileName(
            self, "Select an image file", "",
            "Images (*.png *.gif *.jpg *.jpeg *.bmp)")
        if files:
            self.selected_file = files
            self.finfo = QDir(files)
            self.updateIcon(files)
            self.setWindowTitle("Select an image file - {0}".format(QFileInfo(files).fileName()))

    def updateIcon(self, path):
        img = QPixmap(path)
        if not img.isNull():
             # Scale to fit within a preview box, preserving aspect ratio so the
             # image isn't smushed into a square.
            max_w, max_h = 400, 300
            self.l.setPixmap(img.scaled(max_w, max_h, Qt.KeepAspectRatio))

    def selectedFiles(self):
        # Preserve the interface the original Picture_Picker exposed so
        # callers (e.g. webslideshow.upload_pic) work unchanged.
        return [self.selected_file] if self.selected_file else []
