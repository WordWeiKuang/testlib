from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from model import Paper, Item

class MyListWidgetItem(QListWidgetItem):
    def __init__(self, paper=None):
        QListWidgetItem.__init__(self)
        self.paper = paper

class Catalog(QWidget):

    def __init__(self, item_view=None):

        QWidget.__init__(self)
        layout = QVBoxLayout(self)

        self.item_view = item_view
        self.listWidget = QListWidget()
        self.listWidget.itemClicked.connect(self.clicked)
        self.load()
        layout.addWidget(self.listWidget)
        self.setFixedWidth(230)

    def load(self, papers=None):
        if self.listWidget.item(0):
            self.listWidget.clear()
        if not papers:
            papers = Paper.select().paginate(0, 100)
        for i in range(len(papers)):
            paper = papers[i]
            widgetItem = MyListWidgetItem(paper)
            widgetItem.setIcon(QIcon('./icons/file_1.png'))
            widgetItem.setText(paper.name)
            widgetItem.setFont(QFont("Arial",13))
            self.listWidget.addItem(widgetItem)

    def clicked(self, widgetItem):
        items = Item.select().where(Item.paper==widgetItem.paper.id).order_by(Item.index).paginate(0, 100)
        self.item_view.items = items
        self.item_view.load(items)