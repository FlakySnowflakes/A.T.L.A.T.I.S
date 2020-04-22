# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'admin_window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
import codes.url_parser
from codes.url_parser import *
from codes.Filter_Reviews import *
from data_Conversion import *
import time
import socket


class QThread2(QtCore.QThread):
    sig2 = pyqtSignal(str))

    def __init__(self, parent = None):
        QtCore.Qthread.__init__(self, parent)

    def get_ip(self):
        hostname=socket.gethostname()
        IPAddr=socket.gethostbyname(hostname)
        self.sig2.emit('Your Computer IP Address is: ' + IPAddr)



class QThread1(QtCore.QThread):

    sig1=pyqtSignal(str)

    def __init__(self, parent = None):
        QtCore.QThread.__init__(self, parent)

    def on_source(self, lineftxt):
        self.source_txt=lineftxt

    def run(self):
        global results
        pt=ParseTripAdvisor(20)
        self.running=True
        while self.running:
            try:
                pt.get_soup(self.source_txt)
                pt.parse(self.source_txt)
                self.sig1.emit(pt.hotelName)
                time.sleep(1)
                if pt.HotelExist == True:
                    self.sig1.emit(str(pt.hotelName) + 'already exists')
                else:
                    self.sig1.emit(str('Creating new file...'))
                    time.sleep(1)
                    df=to_DataFrame(results)
                    del results[:]
                    df=filter_review(df, pt.hotelName)
                    time.sleep(2)
                    self.sig1.emit(str(df))
                    time.sleep(1)
                    SetSave(df, pt.hotelName)
                    break
            except Exception as err:
                self.sig1.emit(str(err))


class Ui_MainWindow(QtWidgets.QMainWindow):

    sig=pyqtSignal(str)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(480, 367)
        self.centralwidget=QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_6=QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.gridLayout_2=QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.pushButton=QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 1, 0, 1, 1)

        self.lineEdit_2=QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_2.addWidget(self.lineEdit_2, 0, 1, 1, 1)

        self.lineEdit=QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_2.addWidget(self.lineEdit, 1, 1, 1, 1)

        self.label=QtWidgets.QLabel(self.centralwidget)
        self.label.setAccessibleName("")
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAlignment(QtCore.Qt.AlignRight |
                                QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.verticalLayout_6.addLayout(self.gridLayout_2)

        self.plainTextEdit=QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setPlaceholderText("")
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout_6.addWidget(self.plainTextEdit)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar=QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.pushButton.clicked.connect(self.on_but1)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate=QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Add to database"))
        self.lineEdit.setPlaceholderText(_translate(
            "MainWindow", "Enter a URL of hotel (from TripAdvisor only)"))
        self.label.setText(_translate("MainWindow", "City:"))

    def on_but1(self):
        try:
            self.thread2=QThread2()
            self.thread2.sig2.connect(self.on_info)
            self.thread2.start()
        except:
            self.plainTextEdit.clear()
            lineURL=self.lineEdit.text()
            self.thread1=QThread1()
            self.sig.connect(self.thread1.on_source)
            self.sig.emit(lineURL)
            self.thread1.start()
            self.thread1.sig1.connect(self.on_info)

    def on_info(self, info):
        self.plainTextEdit.appendPlainText(str(info))


if __name__ == "__main__":
    import sys
    app=QtWidgets.QApplication(sys.argv)
    MainWindow=QtWidgets.QMainWindow()
    ui=Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
