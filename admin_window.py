# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'admin_window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import codes.url_parser 
from codes.url_parser import *
from codes.Filter_Reviews import *
from data_Conversion import *

class Ui_MainWindow(object):

    def start(self):
        global results
        url = self.lineEdit.text()
        pt = ParseTripAdvisor(20)
        pt.get_soup(url)
        pt.parse(url)
        self.plainTextEdit.insertPlainText(pt.hotel_name + '\n')
        self.QtCore.QTimer.singleShot(0, self.start)
        # if check == True:
        #     self.plainTextEdit.insertPlainText("File "+ p.hotel_name +" already exists and is readable\n")
        #     pass
        # else:
        #     self.plainTextEdit.insertPlainText("The file does not exist...\n"+ "Creating new file...\n")
        #     df = to_DataFrame(results)  # Convert list to DataFrame
        #     del results[:]
        #     df = filter_review(df, p.hotel_name)  # Divide the review sentences from the DataFrame
        #     self.plainTextEdit.insertPlainText(df + '\n')
        #     saveto_sql(df, p.hotel_name)  # <---- save pandas to sql
        #     self.plainTextEdit.insertPlainText(p.hotel_name + ' added to sql\n')
        #     saveto_csv(df, p.hotel_name)  # <---- save pandas to sql
        #     self.plainTextEdit.insertPlainText(p.hotel_name + ' added to csv\n')

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
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
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
        
        self.pushButton.clicked.connect(self.start)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Add to database"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "Enter a URL of hotel (from TripAdvisor only)"))
        self.label.setText(_translate("MainWindow", "City:"))

    class worker(QRunnable):
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

