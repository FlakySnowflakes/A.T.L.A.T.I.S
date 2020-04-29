# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'admin_window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSignal
from codes.url_parser import *
from codes.Filter_Reviews import *
from data_Conversion import *
import time
import socket


class QThread2(QtCore.QThread):
    sig2 = pyqtSignal(str)

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

    def run(self):
        self.hostname = socket.gethostname()
        self.IPAddr = socket.gethostbyname(self.hostname)
        try:
            self.sig2.emit('\nIP Address: {}::{}\n' . format(str(self.IPAddr), str(self.hostname)))
            time.sleep(1)
            self.sig2.emit('Log:')
            time.sleep(1)
        except Exception as err:
            self.sig2.emit(str(err))


class QThread1(QtCore.QThread):

    sig1 = pyqtSignal(str)

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

    def on_source(self, lineftxt, city):
        self.source_txt = lineftxt
        self.city = city.title()

    def run(self):
        global results
        pta = ParseTripAdvisor(35, self.city) #(35) <--- number of reviews to parse
        self.running = True
        while self.running:
            try:
                time.sleep(2)
                self.sig1.emit('Collecting soup...')
                time.sleep(2)
                pta.get_soup(self.source_txt)
                self.sig1.emit('Parsing soup...')
                time.sleep(2)
                pta.parse(self.source_txt)
                self.sig1.emit('Hotel name: ' + pta.hotelName)
                time.sleep(1.5)
                if pta.HotelExist() == True:
                    self.sig1.emit(str(pta.hotelName) + ' database already exists')
                else:
                    self.sig1.emit(str('Creating new file...'))
                    self.sig1.emit(str('Converting to dataframe...'))
                    time.sleep(1)
                    df = to_DataFrame(results)
                    del results[:]
                    time.sleep(3)
                    df = filter_review(df, pta.hotelName, pta.city)
                    self.sig1.emit(str('Filtering each sentences...'))
                    time.sleep(1)
                    SetSave(df, pta.hotelName, pta.city, pta.address)
                    self.sig1.emit(str(pta.hotelName) + ' saved in database and csv')
                    time.sleep(1)
            except Exception as err:
                self.sig1.emit(str(err))
            break


class Admin_Window(QMainWindow):

    sig = pyqtSignal(str, str)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(480, 367)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 1, 0, 1, 1)

        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_2.addWidget(self.lineEdit_2, 0, 1, 1, 1)

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_2.addWidget(self.lineEdit, 1, 1, 1, 1)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setAccessibleName("")
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAlignment(QtCore.Qt.AlignRight |
                                QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.verticalLayout_6.addLayout(self.gridLayout_2)

        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setPlaceholderText("")
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout_6.addWidget(self.plainTextEdit)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.pushButton.clicked.connect(self.on_but1)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Admin Window"))
        self.pushButton.setText(_translate("MainWindow", "Add to database"))
        self.label.setText(_translate("MainWindow", "City:"))

    def on_but1(self):
        self.thread2 = QThread2(parent=self)
        self.thread2.start()
        self.thread2.sig2.connect(self.on_info)
        self.thread2.requestInterruption()
        city = self.lineEdit_2.text()
        lineURL = self.lineEdit.text()
        self.thread1 = QThread1()
        self.sig.connect(self.thread1.on_source)
        self.sig.emit(lineURL, city)
        self.thread1.start()
        self.thread1.sig1.connect(self.on_info)
        self.thread1.requestInterruption()

    def on_info(self, info):
        self.plainTextEdit.appendPlainText(str(info))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Admin_Window()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
