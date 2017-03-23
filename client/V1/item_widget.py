import sys
from PyQt5.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QRadioButton
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont
from model import Item

class MyTextEdit(QWidget):
    def __init__(self, item):
        QWidget.__init__(self)

        self.textbox = QTextEdit()
        s = '(%s) %s' % (str(item.index), item.content)
        self.textbox.setText(s)
        self.textbox.setStyleSheet("border: 0px;background-color: rgb(255, 255, 255, 60);")
        self.textbox.setReadOnly(True)
        self.textbox.setFont(QFont("Arial",11))

        self.answerbox = QWidget()
        anlist = [QRadioButton(x) for x in item.answer_list.split(',')]
        answerlayout = QHBoxLayout(self.answerbox)
        for i in range(len(anlist)):
            answerlayout.addWidget(anlist[i])

        layout = QVBoxLayout(self)
        layout.addWidget(self.textbox)
        layout.addWidget(self.answerbox)



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
            items = []#Item.select().where(Item.paper=='001488853815593ed92d53418ed4aca9751a39b14e03d33000').order_by(Item.index).paginate(0, 100)
        for i in range(len(items)):
            item = items[i]
            widgetItem = QListWidgetItem()
            textEdit = MyTextEdit(item)
            widgetItem.setSizeHint(QSize(100,150))
            self.listWidget.addItem(widgetItem)
            self.listWidget.setItemWidget(widgetItem, textEdit)

    def clicked(self, widgetItem):
        pass