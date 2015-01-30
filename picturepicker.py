#! /usr/bin/env python

import sys
from PySide.QtCore import *
from PySide.QtGui import *

class Picture_Picker(QFileDialog):

    def __init__(self, parent=None):
        super(Picture_Picker, self).__init__(parent)

        self.setWindowTitle("Select an image file")
        self.l = QLabel()
        self.layout().addWidget(self.l, 1, 3, Qt.AlignCenter)
        self.layout().setColumnMinimumWidth(1, 400)
        self.layout().setColumnStretch(1, 1)
        self.setNameFilter("Images (*.png *.gif *.jpg *.jpeg *.bmp)")
        li = self.layout().itemAtPosition(1, 0)
        wid = li.widget()
        subwid = wid.widget(0)
        subwid.hide()
                
        # Connect to currentChanged signal
        self.currentChanged.connect(self.updateIcon)

    def updateIcon(self, path):
        img = QPixmap(path)
        self.l.setPixmap(img.scaled(300, 300, Qt.KeepAspectRatio))
