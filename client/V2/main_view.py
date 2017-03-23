# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
from left_view import LeftView
from right_view import RightView

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setGeometry(100,100,1000,600)
        self.tool_bar = QToolBar('toolbat')
        self.addToolBar(self.tool_bar)
        self.splitter = QSplitter(Qt.Horizontal)#Qt.Vertical


        cata_view = LeftView()
        item_view = RightView()


        self.splitter.addWidget(cata_view)
        self.splitter.addWidget(item_view)

        self.setCentralWidget(self.splitter)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
