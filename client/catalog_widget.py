from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from model import Paper

class Catalog(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        formbox = QFormLayout()
        mygroupbox = QGroupBox('试卷列表')
        imgs = []
        names = []
        papers = Paper.select().paginate(0,50)
        for i in range(len(papers)):
            paper = papers[i]
            imglabel = QLabel('')
            imglabel.setPixmap(QPixmap('./icons/file.png'))
            imgs.append(imglabel)
            Tlabel = QLabel(paper.name)
            names.append(Tlabel)
            formbox.addRow(imgs[i], names[i])
            mygroupbox.setLayout(formbox)
        scroll = QScrollArea()
        scroll.setWidget(mygroupbox)
        scroll.setWidgetResizable(True)
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)
        '''
        for i in range(len(papers)):
            paper = papers[i]
            label = QLabel()
            pl = QAction(QIcon('./icons/file_32.png'), paper.name)
            label.addAction(pl)
            print(paper.name)
            layout.addWidget(label)
        '''


        self.setLayout(layout)
        self.setFixedWidth(200)
