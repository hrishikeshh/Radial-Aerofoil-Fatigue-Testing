#coding=utf-8

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from .. import mdb
from .. import media
from .. import core
from . import data_tree
from . import wp_stack
from . import menu_bar

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle(core.common.WindowTitle())
        img_path=media.img.ImgPath()
        self.setWindowIcon(img_path.main_icon)
        self.IniLayoutElements()
        self.IniLayout()

    def IniLayoutElements(self):
        self.tree=data_tree.DataTree()
        self.statusBar()
        self.stack=wp_stack.WPStack()
        self.menu_bar=self.menuBar()
        menu_bar.MenuBar(self.menu_bar)

    def IniLayout(self):
        self.setMinimumSize(1200, 600)
        self.main_layout=QSplitter()
        self.main_layout.addWidget(self.tree)
        self.main_layout.addWidget(self.stack)
        self.main_layout.setOrientation(Qt.Horizontal)

        stack_index=self.stack.Flag2Index('project_overview')
        self.stack.setCurrentIndex(stack_index)

        self.setCentralWidget(self.main_layout)