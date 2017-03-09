import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Window(QWidget):

    def __init__(self):

        QWidget.__init__(self)
        layout = QVBoxLayout(self)

        self.listWidget = QListWidget()
        self.listWidget.itemClicked.connect(self.see)


        layout.addWidget(self.listWidget)

    def load(self, value):
        for i in range(10):
            item = QListWidgetItem()
            item.setIcon(QIcon('../icons/file_1.png'))
            item.setText("Item %i" % i)
            self.listWidget.addItem(item)

    def see(self, widgetItem):
        print(widgetItem.text())

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())