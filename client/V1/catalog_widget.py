from PyQt5.QtWidgets import QWidget, QListWidgetItem, QVBoxLayout, QListWidget
from PyQt5.QtGui import QIcon, QFont
from model import Paper, Item, User
import json

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
        self.setFixedWidth(185)

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
        #widgetItem.setCheckState(Qt.Checked)
        self.item_view.items = items
        self.item_view.load(items)

    def showall(self):
        self.load()

    def star(self):
        users = User.select()
        tag = users[0].tag
        data = json.loads(tag)
        papersid = data.get('star')
        papers = [paper for paper in Paper.select().where(Paper.id<<papersid)]
        self.load(papers)

    def done(self):
        users = User.select()
        tag = users[0].tag
        data = json.loads(tag)
        papersid = data.get('done')
        papers = [paper for paper in Paper.select().where(Paper.id << papersid)]
        self.load(papers)

    def commited(self):
        pass