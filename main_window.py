# -*- coding: utf-8 -*-

from login import Login_Window
from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
from functools import partial


class Ui_MainWindow(object):

    def loadCity(self):
        cities = []
        conn = sqlite3.connect('dbFiles/CityHotels.db')
        c = conn.cursor()
        query = "SELECT name FROM sqlite_master where type='table'"
        c.execute(query)
        rows = c.fetchall()
        for row in rows:
            cities.append(row[0])
        self.listWidget_2.addItems(cities)
        self.listWidget_2.itemClicked.connect(self.loadDataHt)
        c.close()

    def loadDataHt(self, CITY):
        self.listWidget.clear()
        hotels = []
        conn = sqlite3.connect('dbFiles/CityHotels.db')
        c = conn.cursor()
        query = "SELECT hotel FROM '{}'"
        c.execute(query .format(CITY.text()))
        rows = c.fetchall()
        for row in rows:
            hotels.append(row[0])
        self.listWidget.addItems(hotels)
        self.listWidget.itemClicked.connect(self.loadData)
        self.listWidget.itemClicked.connect(lambda item, CITY=CITY: self.show_details(item, CITY))
        self.listWidget.itemClicked.connect(self.show_Aspects)
        c.close()

    def loadData(self, item):
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(2)
        self.tableWidget_2.clear()
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.setColumnCount(2)
        conn = sqlite3.connect('dbFiles/hotel-TA.db')
        c = conn.cursor()
        self.show_Positives(item, c)
        self.show_Negatives(item, c)
        c.close()

    def show_Positives(self, item, c):
        query = "SELECT review, reviewer FROM '{}' WHERE P_sentiment = 'Positive'"
        result = c.execute(query .format(item.text()))
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number,
                                         QtWidgets.QTableWidgetItem(str(data)))

    def show_Negatives(self, item, c):
        query = "SELECT review, reviewer FROM '{}' WHERE N_sentiment = 'Negative'"
        result = c.execute(query .format(item.text()))
        for row_number, row_data in enumerate(result):
            self.tableWidget_2.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget_2.setItem(row_number, column_number,
                                           QtWidgets.QTableWidgetItem(str(data)))

    def show_details(self, item, CITY):
        conn = sqlite3.connect('dbFiles/Cityhotels.db')
        c = conn.cursor()
        self.get_numrev(item, CITY, c)
        self.get_address(item, CITY, c)
        self.pos_per(item, CITY, c)
        self.neg_per(item, CITY, c)
        c.close()

    def pos_per(self, item, CITY, c):
        query = "SELECT pos_percent FROM '{}' WHERE hotel = '{}'"
        c.execute(query . format(CITY.text(), item.text()))
        per_pos = c.fetchone()
        while per_pos:
            self.label_5.setText(str("%.2f" % float(per_pos[0]*100)) + '%')
            self.progressBar.setProperty("value", int(per_pos[0]*100))
            per_pos = c.fetchone()

    def neg_per(self, item, CITY, c):
        query = "SELECT neg_percent FROM '{}' WHERE hotel = '{}'"
        c.execute(query . format(CITY.text(), item.text()))
        neg_pos = c.fetchone()
        while neg_pos:
            self.label_6.setText(str("%.2f" % float(neg_pos[0]*100)) + '%')
            self.progressBar_2.setProperty("value", int(neg_pos[0]*100))
            neg_pos = c.fetchone()

    def get_numrev(self, item, CITY, c):
        query = "SELECT reviews FROM '{}' WHERE hotel = '{}'"
        c.execute(query . format(CITY.text(), item.text()))
        num_rev = c.fetchone()
        while num_rev:
            self.label_9.setText(str(num_rev[0]))
            num_rev = c.fetchone()

    def get_address(self, item, CITY, c):
        query = "SELECT address FROM '{}' WHERE hotel = '{}'"
        c.execute(query . format(CITY.text(), item.text()))
        address = c.fetchone()
        while address:
            self.plainTextEdit.setPlainText(str(address[0]))
            address = c.fetchone()

    def show_Aspects(self, item):
        self.listWidget_3.clear()
        aspects = []
        conn = sqlite3.connect(
            'keywords/' + self.listWidget_2.currentItem().text() + '_keywords.db')
        c = conn.cursor()
        query = """SELECT  "index" FROM '{}' ORDER BY "0"  DESC LIMIT 0, 49999"""
        c.execute(query . format(item.text()))
        rows = c.fetchall()
        for row in rows:
            aspects.append(row[0])
        self.listWidget_3.addItems(aspects)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(686, 486)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 200, 101, 16))
        self.label.setObjectName("label")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(20, 220, 191, 161))
        self.listWidget.setObjectName("listWidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(479, 417, 191, 32))
        self.pushButton.setObjectName("pushButton")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(230, 34, 411, 151))
        self.tableWidget.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tableWidget.setLineWidth(1)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setObjectName("tableWidget")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(287, -11, 311, 60))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar.setObjectName("progressBar")
        self.listWidget_2 = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_2.setGeometry(QtCore.QRect(20, 33, 191, 160))
        self.listWidget_2.setObjectName("listWidget_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 12, 101, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(236, 9, 59, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(229, 196, 59, 16))
        self.label_4.setObjectName("label_4")
        self.progressBar_2 = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar_2.setGeometry(QtCore.QRect(287, 176, 311, 60))
        self.progressBar_2.setProperty("value", 0)
        self.progressBar_2.setTextVisible(False)
        self.progressBar_2.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar_2.setObjectName("progressBar_2")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(610, 10, 59, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(610, 197, 59, 16))
        self.label_6.setObjectName("label_6")
        self.listWidget_3 = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_3.setGeometry(QtCore.QRect(340, 380, 301, 21))
        self.listWidget_3.setFlow(QtWidgets.QListView.LeftToRight)
        self.listWidget_3.setObjectName("listWidget_3")
        self.tableWidget_2 = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_2.setGeometry(QtCore.QRect(230, 220, 411, 151))
        self.tableWidget_2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.setColumnCount(2)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(229, 380, 120, 20))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(20, 380, 91, 20))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(114, 383, 91, 16))
        self.label_9.setObjectName("label_9")
        self.location = QtWidgets.QLabel(self.centralwidget)
        self.location.setGeometry(QtCore.QRect(20, 400, 59, 16))
        self.location.setObjectName("location")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(20, 417, 451, 31))
        self.plainTextEdit.setInputMethodHints(QtCore.Qt.ImhNone)
        self.plainTextEdit.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setPlainText("")
        self.plainTextEdit.setObjectName("plainTextEdit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton.clicked.connect(self.show_login)

        self.loadCity()
        # Positive Table
        self.tableWidget.verticalHeader().setDefaultSectionSize(75)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        # Negative Table
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(2)
        self.tableWidget_2.resizeRowsToContents()
        self.tableWidget_2.verticalHeader().setDefaultSectionSize(80)
        header = self.tableWidget_2.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GoTellHotels"))
        self.label.setText(_translate("MainWindow", "List of Hotels:"))
        self.pushButton.setText(_translate("MainWindow", "Admin"))
        self.progressBar.setFormat(_translate("MainWindow", "%p%"))
        self.label_2.setText(_translate("MainWindow", "List of cities:"))
        self.label_3.setText(_translate("MainWindow", "Positive"))
        self.label_4.setText(_translate("MainWindow", "Negative"))
        self.progressBar_2.setFormat(_translate("MainWindow", "%p%"))
        self.label_5.setText(_translate("MainWindow", "0%"))
        self.label_6.setText(_translate("MainWindow", "0%"))
        self.label_7.setText(_translate("MainWindow", "Popular mentions:"))
        self.label_8.setText(_translate("MainWindow", "No. of reviews:"))
        self.label_9.setText(_translate("MainWindow", "0"))
        self.location.setText(_translate("MainWindow", "Location:"))

    def show_login(self):
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Login_Window()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
