# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'webslideshow.ui'
#
# Created: Sat Nov  2 21:16:03 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_WebSlideshow(object):
    def setupUi(self, WebSlideshow):
        WebSlideshow.setObjectName("WebSlideshow")
        WebSlideshow.resize(680, 655)
        WebSlideshow.setMinimumSize(QtCore.QSize(680, 650))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../media/Ubuntu/home/brian/SpiderOak Hive/Projects/Web Slideshow/Version6/VideoFolder.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        WebSlideshow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(WebSlideshow)
        self.centralwidget.setMinimumSize(QtCore.QSize(670, 0))
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setHorizontalSpacing(12)
        self.gridLayout.setObjectName("gridLayout")
        self.lbl_title = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_title.sizePolicy().hasHeightForWidth())
        self.lbl_title.setSizePolicy(sizePolicy)
        self.lbl_title.setObjectName("lbl_title")
        self.gridLayout.addWidget(self.lbl_title, 0, 0, 1, 1)
        self.le_title = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_title.sizePolicy().hasHeightForWidth())
        self.le_title.setSizePolicy(sizePolicy)
        self.le_title.setObjectName("le_title")
        self.gridLayout.addWidget(self.le_title, 0, 1, 1, 3)
        self.sli_numslides = QtGui.QSlider(self.groupBox)
        self.sli_numslides.setMinimum(2)
        self.sli_numslides.setMaximum(100)
        self.sli_numslides.setPageStep(1)
        self.sli_numslides.setTracking(False)
        self.sli_numslides.setOrientation(QtCore.Qt.Horizontal)
        self.sli_numslides.setTickPosition(QtGui.QSlider.TicksBothSides)
        self.sli_numslides.setObjectName("sli_numslides")
        self.gridLayout.addWidget(self.sli_numslides, 3, 1, 1, 3)
        self.lbl_resolution = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_resolution.sizePolicy().hasHeightForWidth())
        self.lbl_resolution.setSizePolicy(sizePolicy)
        self.lbl_resolution.setObjectName("lbl_resolution")
        self.gridLayout.addWidget(self.lbl_resolution, 4, 0, 1, 1)
        self.cb_effects = QtGui.QComboBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_effects.sizePolicy().hasHeightForWidth())
        self.cb_effects.setSizePolicy(sizePolicy)
        self.cb_effects.setObjectName("cb_effects")
        self.gridLayout.addWidget(self.cb_effects, 1, 1, 1, 1)
        self.lbl_duration = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_duration.sizePolicy().hasHeightForWidth())
        self.lbl_duration.setSizePolicy(sizePolicy)
        self.lbl_duration.setIndent(36)
        self.lbl_duration.setObjectName("lbl_duration")
        self.gridLayout.addWidget(self.lbl_duration, 1, 2, 1, 1)
        self.lbl_numslides = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_numslides.sizePolicy().hasHeightForWidth())
        self.lbl_numslides.setSizePolicy(sizePolicy)
        self.lbl_numslides.setObjectName("lbl_numslides")
        self.gridLayout.addWidget(self.lbl_numslides, 3, 0, 1, 1)
        self.lbl_effect = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_effect.sizePolicy().hasHeightForWidth())
        self.lbl_effect.setSizePolicy(sizePolicy)
        self.lbl_effect.setObjectName("lbl_effect")
        self.gridLayout.addWidget(self.lbl_effect, 1, 0, 1, 1)
        self.cb_resolution = QtGui.QComboBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_resolution.sizePolicy().hasHeightForWidth())
        self.cb_resolution.setSizePolicy(sizePolicy)
        self.cb_resolution.setObjectName("cb_resolution")
        self.gridLayout.addWidget(self.cb_resolution, 4, 1, 1, 1)
        self.sb_duration = QtGui.QSpinBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sb_duration.sizePolicy().hasHeightForWidth())
        self.sb_duration.setSizePolicy(sizePolicy)
        self.sb_duration.setObjectName("sb_duration")
        self.gridLayout.addWidget(self.sb_duration, 1, 3, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addWidget(self.groupBox)
        self.scrollArea = QtGui.QScrollArea(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_2 = QtGui.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 660, 79))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout.addWidget(self.scrollArea)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(408, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(self.centralwidget)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        WebSlideshow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(WebSlideshow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 680, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        WebSlideshow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(WebSlideshow)
        self.statusbar.setObjectName("statusbar")
        WebSlideshow.setStatusBar(self.statusbar)
        self.actionNew_Slideshow = QtGui.QAction(WebSlideshow)
        self.actionNew_Slideshow.setObjectName("actionNew_Slideshow")
        self.actionExit = QtGui.QAction(WebSlideshow)
        self.actionExit.setObjectName("actionExit")
        self.actionSave = QtGui.QAction(WebSlideshow)
        self.actionSave.setObjectName("actionSave")
        self.menuFile.addAction(self.actionNew_Slideshow)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(WebSlideshow)
        QtCore.QMetaObject.connectSlotsByName(WebSlideshow)

    def retranslateUi(self, WebSlideshow):
        WebSlideshow.setWindowTitle(QtGui.QApplication.translate("WebSlideshow", "Simple Web Slideshow", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("WebSlideshow", "Web Slideshow Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_title.setText(QtGui.QApplication.translate("WebSlideshow", "Slideshow title:", None, QtGui.QApplication.UnicodeUTF8))
        self.le_title.setPlaceholderText(QtGui.QApplication.translate("WebSlideshow", "Enter a title for this slideshow", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_resolution.setText(QtGui.QApplication.translate("WebSlideshow", "Optimize for resolution:", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_duration.setText(QtGui.QApplication.translate("WebSlideshow", "Slide duration (seconds):", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_numslides.setText(QtGui.QApplication.translate("WebSlideshow", "Number of slides:", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_effect.setText(QtGui.QApplication.translate("WebSlideshow", "Slide transition effect:", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("WebSlideshow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew_Slideshow.setText(QtGui.QApplication.translate("WebSlideshow", "New Slideshow", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("WebSlideshow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("WebSlideshow", "Save", None, QtGui.QApplication.UnicodeUTF8))

