# -*- coding: utf-8 -*-
'''

TODO：从sqlit导入数据，编写orm，建立数据模型

'''
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from peewee import *

import sys

from model import Paper
from catalog_widget import Catalog
from item_widget import ItemView

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 设置窗口标题
        self.setWindowTitle('专题测试')
        self.setGeometry(100,100,1000,700)
        self.setWindowIcon(QIcon('./test/icons/penguin.png'))
        # 设置布局
        main_window_layout = QHBoxLayout()
        # 添加按钮动作，并加载图标图像
        button_action = QAction(QIcon('./test/icons/penguin.png'), 'Menu button', self)
        # 设置状态栏提示
        button_action.setStatusTip('This is menu button')
        button_action.triggered.connect(self.onButtonClick)
        button_action.setCheckable(True)
        # 添加新的菜单选项
        button_action2 = QAction('C++', self)
        button_action3 = QAction('Python', self)
        button_action2.setCheckable(True)
        button_action3.setCheckable(True)
        button_action2.triggered.connect(self.onButtonClick)
        button_action3.triggered.connect(self.onButtonClick)
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fiel_menu = menubar.addMenu('&File')
        fiel_menu.addAction(button_action)
        # 为菜单选项添加分隔符
        fiel_menu.addSeparator()
        build_system_menu = fiel_menu.addMenu('&Build System')
        build_system_menu.addAction(button_action2)
        build_system_menu.addSeparator()
        build_system_menu.addAction(button_action3)

        cata_list = Catalog()
        item_list = ItemView()

        #添加到主视图布局
        main_window_layout.addWidget(cata_list)
        main_window_layout.addWidget(item_list)

        #在主视图中设置中心组件
        widget = QWidget()
        widget.setLayout(main_window_layout)
        self.setCentralWidget(widget)

    def onButtonClick(self, s):
        print(s)


# 创建应用实例，通过 sys.argv 传入命令行参数
app = QApplication(sys.argv)
# 创建窗口实例
window = MainWindow()
# 显示窗口
window.show()
# 执行应用，进入事件循环
app.exec_()