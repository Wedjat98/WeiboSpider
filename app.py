from PySide2.QtWidgets import QApplication, QMainWindow, QListWidget
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
    except sqlite3.Error as e:
        print(e)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.button.clicked.connect(self.show2List)
        self.ui.comboBox.addItems(tableList[0:-1])
        self.ui.comboBox.currentIndexChanged.connect(self.comboxChanged)

    def show2List(self):
        self.ui.listWidget.clear()
        self.ui.comboBox.showNormal()
        for row in getHeadLineFromDB():
            self.ui.listWidget.addItem(row[1])
        self.ui.listWidget.showNormal()

    def comboxChanged(self):
        self.ui.listWidget.clear()
        self.ui.comboBox.showNormal()
        conn = sqlite3.connect("wbTopRank.db")
        cur = conn.cursor()
        try:
            sql4 = f'select * from {tableList[self.ui.comboBox.currentIndex()]}'
            queryResult = cur.execute(sql4)
            for row in queryResult:
                self.ui.listWidget.addItem(row[1])
        except sqlite3.Error as e:
            print(e)


connect2DB()
app = QApplication([])
mainWindow = MainWindow()
mainWindow.show()
app.exec_()