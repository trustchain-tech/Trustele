# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 1000)
        MainWindow.setMinimumSize(QtCore.QSize(1000, 1000))
        MainWindow.setMaximumSize(QtCore.QSize(1000, 1000))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/resource/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setWindowOpacity(0.95)
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(1000, 1000))
        self.centralwidget.setMaximumSize(QtCore.QSize(1000, 1000))
        self.centralwidget.setObjectName("centralwidget")
        self.msg_area = QtWidgets.QTextEdit(self.centralwidget)
        self.msg_area.setGeometry(QtCore.QRect(510, 80, 391, 411))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        self.msg_area.setFont(font)
        self.msg_area.setObjectName("msg_area")
        self.user_area = QtWidgets.QTextEdit(self.centralwidget)
        self.user_area.setGeometry(QtCore.QRect(70, 80, 391, 411))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        self.user_area.setFont(font)
        self.user_area.setObjectName("user_area")
        self.user_label = QtWidgets.QLabel(self.centralwidget)
        self.user_label.setGeometry(QtCore.QRect(70, 30, 211, 41))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(16)
        self.user_label.setFont(font)
        self.user_label.setObjectName("user_label")
        self.msg_label = QtWidgets.QLabel(self.centralwidget)
        self.msg_label.setGeometry(QtCore.QRect(510, 30, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(16)
        self.msg_label.setFont(font)
        self.msg_label.setObjectName("msg_label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(750, 510, 151, 51))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(20)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.my_id = QtWidgets.QLineEdit(self.centralwidget)
        self.my_id.setGeometry(QtCore.QRect(250, 510, 431, 51))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(14)
        self.my_id.setFont(font)
        self.my_id.setMaxLength(64)
        self.my_id.setObjectName("my_id")
        self.id_label = QtWidgets.QLabel(self.centralwidget)
        self.id_label.setGeometry(QtCore.QRect(80, 510, 161, 51))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(16)
        self.id_label.setFont(font)
        self.id_label.setObjectName("id_label")
        self.info_area = QtWidgets.QTextBrowser(self.centralwidget)
        self.info_area.setGeometry(QtCore.QRect(70, 670, 831, 121))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.info_area.setFont(font)
        self.info_area.setObjectName("info_area")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(70, 590, 831, 41))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.power = QtWidgets.QLabel(self.centralwidget)
        self.power.setGeometry(QtCore.QRect(340, 920, 331, 41))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        self.power.setFont(font)
        self.power.setObjectName("power")
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(450, 840, 72, 71))
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap(":/resource/logo.png"))
        self.logo.setObjectName("logo")
        MainWindow.setCentralWidget(self.centralwidget)
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Trustele by trustchain-tech"))
        self.msg_area.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Smart Contracts are Everywhere</p></body></html>"))
        self.user_area.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">@blockchainaire</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.user_label.setText(_translate("MainWindow", "Users to Send"))
        self.msg_label.setText(_translate("MainWindow", "Message"))
        self.pushButton.setText(_translate("MainWindow", "Launch"))
        self.my_id.setText(_translate("MainWindow", "TrustChain"))
        self.id_label.setText(_translate("MainWindow", "My name is"))
        self.power.setText(_translate("MainWindow", "Powered by @blockchainaire"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))

import logo_rc
