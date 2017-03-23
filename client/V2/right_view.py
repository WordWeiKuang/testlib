# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import json
from model import Paper, Item, User

class RightView(QFrame):
    def __init__(self):
        QFrame.__init__(self)
        self.setFrameStyle(QFrame.Panel)

        self.setFrameShape(QFrame.Panel)
        self.resize(QSize(100,100))