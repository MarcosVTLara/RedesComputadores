# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'server.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
    QSizePolicy, QStatusBar, QTextEdit, QWidget)

class Ui_Server(object):
    def setupUi(self, Server):
        if not Server.objectName():
            Server.setObjectName(u"Server")
        Server.resize(439, 394)
        self.centralwidget = QWidget(Server)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 0, 191, 41))
        font = QFont()
        font.setFamilies([u"SimSun"])
        font.setPointSize(14)
        self.label.setFont(font)
        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(10, 40, 411, 121))
        self.textEdit_2 = QTextEdit(self.centralwidget)
        self.textEdit_2.setObjectName(u"textEdit_2")
        self.textEdit_2.setGeometry(QRect(10, 210, 411, 121))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(0, 170, 191, 41))
        self.label_2.setFont(font)
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 340, 241, 41))
        self.label_3.setFont(font)
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(240, 350, 81, 22))
        Server.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(Server)
        self.statusbar.setObjectName(u"statusbar")
        Server.setStatusBar(self.statusbar)

        self.retranslateUi(Server)

        QMetaObject.connectSlotsByName(Server)
    # setupUi

    def retranslateUi(self, Server):
        Server.setWindowTitle(QCoreApplication.translate("Server", u"Server", None))
        self.label.setText(QCoreApplication.translate("Server", u"Received Messages:", None))
        self.label_2.setText(QCoreApplication.translate("Server", u"Sent Messages:", None))
        self.label_3.setText(QCoreApplication.translate("Server", u"Time between messages:", None))
    # retranslateUi

