import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from model import Item

class MyTextEdit(QWidget):
    def __init__(self, item):
        QWidget.__init__(self)
        self.textbox = QTextEdit()
        s = '(%s) %s \n\n   %s' % (str(item.index), item.content, item.answer_list)
        self.textbox.setText(s)
        self.textbox.setStyleSheet("border: 0px;background-color: rgb(255, 255, 255, 60);")
        #self.textbox.setWordWrap(True)
        #self.textbox
        #self.setFixedHeight(100)
        self.textbox.setReadOnly(True)
        layout = QVBoxLayout(self)
        layout.addWidget(self.textbox)

class Window(QWidget):

    def __init__(self):

        QWidget.__init__(self)
        layout = QHBoxLayout(self)

        self.listWidget = QListWidget()
        #self.listWidget.setGridSize(QSize(500,500))
        self.listWidget.itemClicked.connect(self.clicked)
        self.load()
        layout.addWidget(self.listWidget)

    def load(self, items=None):
        if self.listWidget.item(0):
            self.listWidget.clear()
        if not items:
            items = Item.select().where(Item.paper=='001488853815484cd6e778becbd4d86a6841f4c6d2c766f000').order_by(Item.index).paginate(0, 100)
        for i in range(len(items)):
            item = items[i]
            widgetItem = QListWidgetItem()
            textEdit = MyTextEdit(item)
            widgetItem.setSizeHint(QSize(100,100))
            self.listWidget.addItem(widgetItem)
            self.listWidget.setItemWidget(widgetItem, textEdit)

    def clicked(self, widgetItem):
        print(widgetItem.text())

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())