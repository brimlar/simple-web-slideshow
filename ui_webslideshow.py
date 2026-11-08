# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'webslideshow.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialogButtonBox,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLayout, QLineEdit, QMainWindow, QMenu,
    QMenuBar, QScrollArea, QSizePolicy, QSlider,
    QSpacerItem, QStatusBar, QVBoxLayout, QWidget)

class Ui_WebSlideshow(object):
    def setupUi(self, WebSlideshow):
        if not WebSlideshow.objectName():
            WebSlideshow.setObjectName(u"WebSlideshow")
        WebSlideshow.resize(680, 655)
        WebSlideshow.setMinimumSize(QSize(680, 650))
        icon = QIcon()
        icon.addFile(u"Video-Folder.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        WebSlideshow.setWindowIcon(icon)
        self.actionNew_Slideshow = QAction(WebSlideshow)
        self.actionNew_Slideshow.setObjectName(u"actionNew_Slideshow")
        self.actionExit = QAction(WebSlideshow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionSave = QAction(WebSlideshow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionAbout_Simple_Web_Slideshow = QAction(WebSlideshow)
        self.actionAbout_Simple_Web_Slideshow.setObjectName(u"actionAbout_Simple_Web_Slideshow")
        self.centralwidget = QWidget(WebSlideshow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setMinimumSize(QSize(670, 0))
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QSize(662, 0))
        self.groupBox.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.groupBox.setFlat(False)
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout.setHorizontalSpacing(12)
        self.gridLayout.setVerticalSpacing(8)
        self.lbl_title = QLabel(self.groupBox)
        self.lbl_title.setObjectName(u"lbl_title")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lbl_title.sizePolicy().hasHeightForWidth())
        self.lbl_title.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.lbl_title, 0, 0, 1, 1)

        self.le_title = QLineEdit(self.groupBox)
        self.le_title.setObjectName(u"le_title")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.le_title.sizePolicy().hasHeightForWidth())
        self.le_title.setSizePolicy(sizePolicy2)
        self.le_title.setFocusPolicy(Qt.ClickFocus)

        self.gridLayout.addWidget(self.le_title, 0, 1, 1, 1)

        self.lbl_effect = QLabel(self.groupBox)
        self.lbl_effect.setObjectName(u"lbl_effect")
        sizePolicy1.setHeightForWidth(self.lbl_effect.sizePolicy().hasHeightForWidth())
        self.lbl_effect.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.lbl_effect, 1, 0, 1, 1)

        self.cb_effects = QComboBox(self.groupBox)
        self.cb_effects.setObjectName(u"cb_effects")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.cb_effects.sizePolicy().hasHeightForWidth())
        self.cb_effects.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.cb_effects, 1, 1, 1, 1)

        self.lbl_duration = QLabel(self.groupBox)
        self.lbl_duration.setObjectName(u"lbl_duration")
        sizePolicy1.setHeightForWidth(self.lbl_duration.sizePolicy().hasHeightForWidth())
        self.lbl_duration.setSizePolicy(sizePolicy1)
        self.lbl_duration.setIndent(0)

        self.gridLayout.addWidget(self.lbl_duration, 2, 0, 1, 1)

        self.le_duration = QLineEdit(self.groupBox)
        self.le_duration.setObjectName(u"le_duration")
        sizePolicy3.setHeightForWidth(self.le_duration.sizePolicy().hasHeightForWidth())
        self.le_duration.setSizePolicy(sizePolicy3)
        self.le_duration.setMaxLength(4)

        self.gridLayout.addWidget(self.le_duration, 2, 1, 1, 1)

        self.lbl_numslides = QLabel(self.groupBox)
        self.lbl_numslides.setObjectName(u"lbl_numslides")
        sizePolicy1.setHeightForWidth(self.lbl_numslides.sizePolicy().hasHeightForWidth())
        self.lbl_numslides.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.lbl_numslides, 3, 0, 1, 1)

        self.sli_numslides = QSlider(self.groupBox)
        self.sli_numslides.setObjectName(u"sli_numslides")
        self.sli_numslides.setMinimum(2)
        self.sli_numslides.setMaximum(100)
        self.sli_numslides.setPageStep(1)
        self.sli_numslides.setTracking(False)
        self.sli_numslides.setOrientation(Qt.Horizontal)
        self.sli_numslides.setTickPosition(QSlider.TicksBothSides)

        self.gridLayout.addWidget(self.sli_numslides, 3, 1, 1, 1)

        self.lbl_resolution = QLabel(self.groupBox)
        self.lbl_resolution.setObjectName(u"lbl_resolution")
        sizePolicy1.setHeightForWidth(self.lbl_resolution.sizePolicy().hasHeightForWidth())
        self.lbl_resolution.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.lbl_resolution, 4, 0, 1, 1)

        self.cb_resolution = QComboBox(self.groupBox)
        self.cb_resolution.setObjectName(u"cb_resolution")
        sizePolicy3.setHeightForWidth(self.cb_resolution.sizePolicy().hasHeightForWidth())
        self.cb_resolution.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.cb_resolution, 4, 1, 1, 1)


        self.horizontalLayout_2.addLayout(self.gridLayout)


        self.verticalLayout.addWidget(self.groupBox)

        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy4)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 660, 335))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.groupBox.raise_()

        self.verticalLayout.addWidget(self.scrollArea)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_11 = QSpacerItem(408, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_11)

        self.buttonBox = QDialogButtonBox(self.centralwidget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)

        self.horizontalLayout.addWidget(self.buttonBox)


        self.verticalLayout.addLayout(self.horizontalLayout)

        WebSlideshow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(WebSlideshow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 680, 24))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuAbout = QMenu(self.menubar)
        self.menuAbout.setObjectName(u"menuAbout")
        WebSlideshow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(WebSlideshow)
        self.statusbar.setObjectName(u"statusbar")
        WebSlideshow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        self.menuFile.addAction(self.actionNew_Slideshow)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuAbout.addAction(self.actionAbout_Simple_Web_Slideshow)

        self.retranslateUi(WebSlideshow)

        QMetaObject.connectSlotsByName(WebSlideshow)
    # setupUi

    def retranslateUi(self, WebSlideshow):
        WebSlideshow.setWindowTitle(QCoreApplication.translate("WebSlideshow", u"Simple Web Slideshow", None))
        self.actionNew_Slideshow.setText(QCoreApplication.translate("WebSlideshow", u"New Slideshow", None))
        self.actionExit.setText(QCoreApplication.translate("WebSlideshow", u"Exit", None))
        self.actionSave.setText(QCoreApplication.translate("WebSlideshow", u"Save", None))
        self.actionAbout_Simple_Web_Slideshow.setText(QCoreApplication.translate("WebSlideshow", u"About Simple Web Slideshow", None))
        self.groupBox.setTitle(QCoreApplication.translate("WebSlideshow", u"Web Slideshow Settings", None))
        self.lbl_title.setText(QCoreApplication.translate("WebSlideshow", u"Slideshow title:", None))
        self.le_title.setPlaceholderText(QCoreApplication.translate("WebSlideshow", u"Enter a title for this slideshow", None))
        self.lbl_effect.setText(QCoreApplication.translate("WebSlideshow", u"Slide transition effect:", None))
        self.lbl_duration.setText(QCoreApplication.translate("WebSlideshow", u"Slide duration (seconds):", None))
        self.lbl_numslides.setText(QCoreApplication.translate("WebSlideshow", u"Number of slides:", None))
        self.lbl_resolution.setText(QCoreApplication.translate("WebSlideshow", u"Optimize for resolution:", None))
        self.menuFile.setTitle(QCoreApplication.translate("WebSlideshow", u"File", None))
        self.menuAbout.setTitle(QCoreApplication.translate("WebSlideshow", u"About", None))
    # retranslateUi

