# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PictureSegment.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGraphicsView,
    QGridLayout, QLabel, QLayout, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_PictureSegment(object):
    def setupUi(self, PictureSegment):
        if not PictureSegment.objectName():
            PictureSegment.setObjectName(u"PictureSegment")
        PictureSegment.resize(630, 198)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PictureSegment.sizePolicy().hasHeightForWidth())
        PictureSegment.setSizePolicy(sizePolicy)
        PictureSegment.setMinimumSize(QSize(630, 198))
        PictureSegment.setMaximumSize(QSize(16777215, 198))
        self.verticalLayout = QVBoxLayout(PictureSegment)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 6, 0, 0)
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout_2.setContentsMargins(-1, -1, 6, -1)
        self.lbl_bignum = QLabel(PictureSegment)
        self.lbl_bignum.setObjectName(u"lbl_bignum")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Ignored)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lbl_bignum.sizePolicy().hasHeightForWidth())
        self.lbl_bignum.setSizePolicy(sizePolicy1)
        self.lbl_bignum.setMinimumSize(QSize(0, 0))
        font = QFont()
        font.setPointSize(24)
        font.setBold(False)
        font.setItalic(False)
        self.lbl_bignum.setFont(font)
        self.lbl_bignum.setAlignment(Qt.AlignCenter)
        self.lbl_bignum.setMargin(0)

        self.gridLayout_2.addWidget(self.lbl_bignum, 0, 0, 1, 1)

        self.graphicsView = QGraphicsView(PictureSegment)
        self.graphicsView.setObjectName(u"graphicsView")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy2)
        self.graphicsView.setMinimumSize(QSize(192, 108))
        self.graphicsView.setMaximumSize(QSize(192, 144))
        self.graphicsView.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.graphicsView, 0, 1, 1, 3)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(9, 6, -1, -1)
        self.lbl_caption = QLabel(PictureSegment)
        self.lbl_caption.setObjectName(u"lbl_caption")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.lbl_caption.sizePolicy().hasHeightForWidth())
        self.lbl_caption.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.lbl_caption, 0, 0, 1, 1)

        self.btn_rotate = QPushButton(PictureSegment)
        self.btn_rotate.setObjectName(u"btn_rotate")
        sizePolicy2.setHeightForWidth(self.btn_rotate.sizePolicy().hasHeightForWidth())
        self.btn_rotate.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.btn_rotate, 1, 2, 1, 1)

        self.cb_type = QComboBox(PictureSegment)
        self.cb_type.setObjectName(u"cb_type")
        sizePolicy2.setHeightForWidth(self.cb_type.sizePolicy().hasHeightForWidth())
        self.cb_type.setSizePolicy(sizePolicy2)
        self.cb_type.setFocusPolicy(Qt.StrongFocus)

        self.gridLayout.addWidget(self.cb_type, 1, 1, 1, 1)

        self.le_caption = QLineEdit(PictureSegment)
        self.le_caption.setObjectName(u"le_caption")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(1)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.le_caption.sizePolicy().hasHeightForWidth())
        self.le_caption.setSizePolicy(sizePolicy4)

        self.gridLayout.addWidget(self.le_caption, 0, 1, 1, 3)

        self.lbl_type = QLabel(PictureSegment)
        self.lbl_type.setObjectName(u"lbl_type")

        self.gridLayout.addWidget(self.lbl_type, 1, 0, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 1, 3, 1, 1)

        self.lbl_warning = QLabel(PictureSegment)
        self.lbl_warning.setObjectName(u"lbl_warning")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.lbl_warning.sizePolicy().hasHeightForWidth())
        self.lbl_warning.setSizePolicy(sizePolicy5)
        self.lbl_warning.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.gridLayout.addWidget(self.lbl_warning, 2, 0, 1, 4)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 4, 2, 1)

        self.horizontalSpacer = QSpacerItem(18, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 1, 1, 1, 1)

        self.btn_upload = QPushButton(PictureSegment)
        self.btn_upload.setObjectName(u"btn_upload")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.btn_upload.sizePolicy().hasHeightForWidth())
        self.btn_upload.setSizePolicy(sizePolicy6)

        self.gridLayout_2.addWidget(self.btn_upload, 1, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(13, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 1, 3, 1, 1)

        self.gridLayout_2.setColumnStretch(4, 1)

        self.verticalLayout.addLayout(self.gridLayout_2)

        self.line = QFrame(PictureSegment)
        self.line.setObjectName(u"line")
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)


        self.retranslateUi(PictureSegment)

        QMetaObject.connectSlotsByName(PictureSegment)
    # setupUi

    def retranslateUi(self, PictureSegment):
        PictureSegment.setWindowTitle(QCoreApplication.translate("PictureSegment", u"Form", None))
        self.lbl_bignum.setText(QCoreApplication.translate("PictureSegment", u"1", None))
        self.lbl_caption.setText(QCoreApplication.translate("PictureSegment", u"Slide caption:", None))
        self.btn_rotate.setText(QCoreApplication.translate("PictureSegment", u"Rotate clockwise", None))
        self.le_caption.setPlaceholderText(QCoreApplication.translate("PictureSegment", u"Enter a caption for this image, or leave blank", None))
        self.lbl_type.setText(QCoreApplication.translate("PictureSegment", u"Slide type:", None))
        self.lbl_warning.setText(QCoreApplication.translate("PictureSegment", u"TextLabel", None))
        self.btn_upload.setText(QCoreApplication.translate("PictureSegment", u"Upload New Image", None))
    # retranslateUi

