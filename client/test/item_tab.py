import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from model import Item

class MyTextEdit(QWidget):
    def __init__(self, item):
        QWidget.__init__(self)
        self.textbox = QTextEdit()
        #s = '(%s) %s \n\n   %s' % (str(item.index), item.content, item.answer_list)
        self.textbox.setText(item.content)
        self.textbox.setStyleSheet("border: 0px;background-color: rgb(255, 255, 255, 60);")
        #self.textbox.setWordWrap(True)
        #self.textbox
        #self.setFixedHeight(100)
        self.textbox.setReadOnly(True)
        self.textbox.setFont(QFont("Arial",11))
        layout = QVBoxLayout(self)
        layout.addWidget(self.textbox)

class ItemView(QWidget):
    def __init__(self, items=None):
        QWidget.__init__(self)

        self.items = items
        layout = QHBoxLayout(self)
        self.listWidget = QListWidget()
        #self.listWidget.setGridSize(QSize(500,500))
        self.listWidget.itemClicked.connect(self.clicked)
        self.load(self.items)
        layout.addWidget(self.listWidget)

    def load(self, items=None):
        if self.listWidget.item(0):
            self.listWidget.clear()
        if not items:
            items = Item.select().where(Item.paper=='001488853815593ed92d53418ed4aca9751a39b14e03d33000').order_by(Item.index).paginate(0, 100)
        for i in range(len(items)):
            item = items[i]
            widgetItem = QListWidgetItem()
            textEdit = MyTextEdit(item)
            widgetItem.setSizeHint(QSize(100,150))
            self.listWidget.addItem(widgetItem)
            self.listWidget.setItemWidget(widgetItem, textEdit)

    def clicked(self, widgetItem):
        pass

class Item_Tab_View(QWidget):
    def __init__(self):
        QWidget.__init__(self)