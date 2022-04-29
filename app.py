import sys
import time

from PySide2.QtWidgets import QApplication, QMainWindow
from ui_headlineAPP import Ui_APP as Ui_MainWindow
import sqlite3
import wbSpider

tableList = []


def connect2DB():
    conn = sqlite3.connect("wbTopRank.db")
    cur = conn.cursor()
    executeResult = cur.execute("select name from sqlite_master where type = 'table' order by name").fetchall()
    for i, tab in enumerate(executeResult, start=0):
        tableList.append(tab[0])


def getHeadLineFromDB():
    wbSpider.main()
    conn = sqlite3.connect("wbTopRank.db")
    cur = conn.cursor()
    try:
        sql4 = f'select * from {tableList[-2]}'
        queryResult = cur.execute(sql4)
        return queryResult
    except IndexError:
        QApplication.processEvents()


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.button.clicked.connect(self.show2List)
        self.ui.comboBox.addItems(tableList[0:-1])
        self.ui.comboBox.currentIndexChanged.connect(self.comboxChanged)
        self.ui.freshBtn.clicked.connect(self.freshAll)

    def show2List(self):
        try:
            self.ui.listWidget.clear()
            self.ui.comboBox.showNormal()
            lastQuery = getHeadLineFromDB()
            for row in lastQuery:
                self.ui.listWidget.addItem(row[1])
            self.ui.listWidget.showNormal()
        except TypeError:
            QApplication.processEvents()

    def comboxChanged(self):
        self.ui.listWidget.clear()
        self.ui.comboBox.showNormal()
        conn = sqlite3.connect("wbTopRank.db")
        cur = conn.cursor()
        sql4 = f'select * from {tableList[self.ui.comboBox.currentIndex()]}'
        queryResult = cur.execute(sql4)
        for row in queryResult:
            self.ui.listWidget.addItem(row[1])

    def freshAll(self):
        # 实时刷新界面
        self.ui.listWidget.clear()
        QApplication.processEvents()
        self.ui.comboBox.repaint()
        # 睡眠一秒
        time.sleep(0.5)


connect2DB()
app = QApplication(sys.argv)
mainWindow = MainWindow()
mainWindow.show()
app.exec_()
