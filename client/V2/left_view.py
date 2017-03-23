# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from model import Paper, Item, User
import json
class MyListWidgetItem(QListWidgetItem):
    def __init__(self, paper=None):
        QListWidgetItem.__init__(self)
        self.paper = paper
        self.setIcon(QIcon('../icons/file_1.png'))
        self.setFont(QFont("Arial", 13))

class LeftView(QFrame):
    def __init__(self):
        QFrame.__init__(self)
        self.setFrameStyle(QFrame.Panel)
        self.setFixedWidth(150)

        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)
        self.tree_widget = QTreeWidget()
        self.load()
        layout.addWidget(self.tree_widget)

    def load(self):
        papers = Paper.select().group_by(Paper.tag).paginate(0, 100)
        l = []
        for i in range(len(papers)):
            paper = papers[i]
            leve0_item = QTreeWidgetItem(self.tree_widget)
            leve0_item.setText(0,paper.tag)
            self.tree_widget.addTopLevelItem(leve0_item)