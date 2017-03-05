from PyQt5.QtWidgets import *
from model import Item

class ItemBox(QWidget):
    def __init__(self, item):
        QWidget.__init__(self)
        self.textbox = QTextEdit()
        s = '(%s) %s \n\n   %s' % (str(item.index), item.content, item.answer_list)
        self.textbox.setText(s)
        #self.setFixedHeight(85)
        self.textbox.setReadOnly(True)
        layout = QVBoxLayout(self)
        layout.addWidget(self.textbox)

class ItemView(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        mygroupbox = QGroupBox('试题列表')
        myform = QFormLayout()
        boxlist = []
        items = Item.select().order_by(Item.index).paginate(0, 100)
        for i in range(len(items)):
            item = items[i]
            boxlist.append(ItemBox(item))
            myform.addRow(boxlist[i])
        mygroupbox.setLayout(myform)
        scroll = QScrollArea()
        scroll.setWidget(mygroupbox)
        scroll.setWidgetResizable(True)
        #scroll.setFixedHeight(400)
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)



