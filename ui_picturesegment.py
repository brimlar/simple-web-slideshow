# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PictureSegment3.ui'
#
# Created: Tue Sep  3 16:36:02 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

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

from PySide import QtCore, QtGui

class Ui_PictureSegment(object):
    def setupUi(self, PictureSegment):
        PictureSegment.setObjectName("PictureSegment")
        PictureSegment.resize(630, 198)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PictureSegment.sizePolicy().hasHeightForWidth())
        PictureSegment.setSizePolicy(sizePolicy)
        PictureSegment.setMinimumSize(QtCore.QSize(630, 198))
        PictureSegment.setMaximumSize(QtCore.QSize(16777215, 198))
        self.verticalLayout = QtGui.QVBoxLayout(PictureSegment)
        self.verticalLayout.setContentsMargins(0, 6, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.gridLayout_2.setContentsMargins(-1, -1, 6, -1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lbl_bignum = QtGui.QLabel(PictureSegment)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_bignum.sizePolicy().hasHeightForWidth())
        self.lbl_bignum.setSizePolicy(sizePolicy)
        self.lbl_bignum.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setWeight(50)
        font.setItalic(False)
        font.setBold(False)
        self.lbl_bignum.setFont(font)
        self.lbl_bignum.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_bignum.setMargin(0)
        self.lbl_bignum.setObjectName("lbl_bignum")
        self.gridLayout_2.addWidget(self.lbl_bignum, 0, 0, 1, 1)
        self.graphicsView = QtGui.QGraphicsView(PictureSegment)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setMinimumSize(QtCore.QSize(192, 108))
        self.graphicsView.setMaximumSize(QtCore.QSize(192, 144))
        self.graphicsView.setAlignment(QtCore.Qt.AlignCenter)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout_2.addWidget(self.graphicsView, 0, 1, 1, 3)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(9, 6, -1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.lbl_caption = QtGui.QLabel(PictureSegment)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_caption.sizePolicy().hasHeightForWidth())
        self.lbl_caption.setSizePolicy(sizePolicy)
        self.lbl_caption.setObjectName("lbl_caption")
        self.gridLayout.addWidget(self.lbl_caption, 0, 0, 1, 1)
        self.le_caption = QtGui.QLineEdit(PictureSegment)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_caption.sizePolicy().hasHeightForWidth())
        self.le_caption.setSizePolicy(sizePolicy)
        self.le_caption.setObjectName("le_caption")
        self.gridLayout.addWidget(self.le_caption, 0, 1, 1, 1)
        self.lbl_type = QtGui.QLabel(PictureSegment)
        self.lbl_type.setObjectName("lbl_type")
        self.gridLayout.addWidget(self.lbl_type, 1, 0, 1, 1)
        self.cb_type = QtGui.QComboBox(PictureSegment)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_type.sizePolicy().hasHeightForWidth())
        self.cb_type.setSizePolicy(sizePolicy)
        self.cb_type.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.cb_type.setObjectName("cb_type")
        self.gridLayout.addWidget(self.cb_type, 1, 1, 1, 1)
        self.lbl_warning = QtGui.QLabel(PictureSegment)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_warning.sizePolicy().hasHeightForWidth())
        self.lbl_warning.setSizePolicy(sizePolicy)
        self.lbl_warning.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.lbl_warning.setObjectName("lbl_warning")
        self.gridLayout.addWidget(self.lbl_warning, 2, 0, 1, 2)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 4, 2, 1)
        spacerItem = QtGui.QSpacerItem(18, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 1, 1, 1)
        self.btn_upload = QtGui.QPushButton(PictureSegment)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_upload.sizePolicy().hasHeightForWidth())
        self.btn_upload.setSizePolicy(sizePolicy)
        self.btn_upload.setObjectName("btn_upload")
        self.gridLayout_2.addWidget(self.btn_upload, 1, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(13, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 1, 3, 1, 1)
        self.gridLayout_2.setColumnStretch(4, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.line = QtGui.QFrame(PictureSegment)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)

        self.retranslateUi(PictureSegment)
        QtCore.QMetaObject.connectSlotsByName(PictureSegment)

    def retranslateUi(self, PictureSegment):
        PictureSegment.setWindowTitle(QtGui.QApplication.translate("PictureSegment", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_bignum.setText(QtGui.QApplication.translate("PictureSegment", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_caption.setText(QtGui.QApplication.translate("PictureSegment", "Slide caption:", None, QtGui.QApplication.UnicodeUTF8))
        self.le_caption.setPlaceholderText(QtGui.QApplication.translate("PictureSegment", "Enter a caption for this image, or leave blank", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_type.setText(QtGui.QApplication.translate("PictureSegment", "Slide type:", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_warning.setText(QtGui.QApplication.translate("PictureSegment", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_upload.setText(QtGui.QApplication.translate("PictureSegment", "Upload New Image", None, QtGui.QApplication.UnicodeUTF8))

