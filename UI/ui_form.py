# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QTabWidget,
    QTextEdit, QVBoxLayout, QWidget)

from pyqtgraph import PlotWidget

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(1366, 768)
        self.groupBox = QGroupBox(Widget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(50, 10, 681, 80))
        self.layoutWidget = QWidget(self.groupBox)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 40, 661, 26))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.lineEditInputFileLocation = QLineEdit(self.layoutWidget)
        self.lineEditInputFileLocation.setObjectName(u"lineEditInputFileLocation")

        self.horizontalLayout.addWidget(self.lineEditInputFileLocation)

        self.pushButtonFindInputFile = QPushButton(self.layoutWidget)
        self.pushButtonFindInputFile.setObjectName(u"pushButtonFindInputFile")

        self.horizontalLayout.addWidget(self.pushButtonFindInputFile)

        self.tabWidget = QTabWidget(Widget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(50, 120, 1291, 631))
        self.tabNormal = QWidget()
        self.tabNormal.setObjectName(u"tabNormal")
        self.groupBox_2 = QGroupBox(self.tabNormal)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(840, 10, 431, 571))
        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 20, 401, 61))
        self.label.setWordWrap(False)
        self.lineEdit = QLineEdit(self.groupBox_2)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(10, 70, 71, 20))
        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(90, 50, 101, 61))
        self.label_2.setWordWrap(False)
        self.widget = QWidget(self.groupBox_2)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(10, 110, 401, 451))
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.textEditNormalX = QTextEdit(self.widget)
        self.textEditNormalX.setObjectName(u"textEditNormalX")

        self.verticalLayout_2.addWidget(self.textEditNormalX)

        self.textEditNormalY = QTextEdit(self.widget)
        self.textEditNormalY.setObjectName(u"textEditNormalY")

        self.verticalLayout_2.addWidget(self.textEditNormalY)

        self.widget1 = QWidget(self.tabNormal)
        self.widget1.setObjectName(u"widget1")
        self.widget1.setGeometry(QRect(16, 13, 811, 561))
        self.verticalLayout = QVBoxLayout(self.widget1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.gvSmallNormalX = PlotWidget(self.widget1)
        self.gvSmallNormalX.setObjectName(u"gvSmallNormalX")

        self.horizontalLayout_2.addWidget(self.gvSmallNormalX)

        self.gvBigNormalX = PlotWidget(self.widget1)
        self.gvBigNormalX.setObjectName(u"gvBigNormalX")

        self.horizontalLayout_2.addWidget(self.gvBigNormalX)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.gvSmallNormalY = PlotWidget(self.widget1)
        self.gvSmallNormalY.setObjectName(u"gvSmallNormalY")

        self.horizontalLayout_3.addWidget(self.gvSmallNormalY)

        self.gvBigNormalY = PlotWidget(self.widget1)
        self.gvBigNormalY.setObjectName(u"gvBigNormalY")

        self.horizontalLayout_3.addWidget(self.gvBigNormalY)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.tabWidget.addTab(self.tabNormal, "")
        self.tabFastest = QWidget()
        self.tabFastest.setObjectName(u"tabFastest")
        self.tabWidget.addTab(self.tabFastest, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.tabWidget.addTab(self.tab_3, "")
        self.pushButtonShowResults = QPushButton(Widget)
        self.pushButtonShowResults.setObjectName(u"pushButtonShowResults")
        self.pushButtonShowResults.setGeometry(QRect(750, 30, 151, 81))
        self.pushButtonSavePlots = QPushButton(Widget)
        self.pushButtonSavePlots.setObjectName(u"pushButtonSavePlots")
        self.pushButtonSavePlots.setGeometry(QRect(920, 30, 171, 81))

        self.retranslateUi(Widget)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
        self.groupBox.setTitle(QCoreApplication.translate("Widget", u"Input the settling result file (.txt)", None))
        self.pushButtonFindInputFile.setText(QCoreApplication.translate("Widget", u"...", None))
#if QT_CONFIG(tooltip)
        self.tabWidget.setToolTip(QCoreApplication.translate("Widget", u"<html><head/><body><p>Normal</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_2.setTitle(QCoreApplication.translate("Widget", u"Analysis", None))
        self.label.setText(QCoreApplication.translate("Widget", u"Report movement history when the setting time is larger or equal to", None))
        self.label_2.setText(QCoreApplication.translate("Widget", u"seconds.", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabNormal), QCoreApplication.translate("Widget", u"Normal X and Y", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabFastest), QCoreApplication.translate("Widget", u"Fastest X and Y", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("Widget", u"Z", None))
        self.pushButtonShowResults.setText(QCoreApplication.translate("Widget", u"Show results!", None))
        self.pushButtonSavePlots.setText(QCoreApplication.translate("Widget", u"Save plots!", None))
    # retranslateUi

