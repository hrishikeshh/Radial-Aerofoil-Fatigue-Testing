#coding=utf-8

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class DataTree(QTreeWidget):
    def __init__(self):
        super(DataTree, self).__init__()
        self.setMinimumWidth(100)
        self.setMaximumWidth(400)
        self.setHeaderLabels(['________'])

    def IniMainStructure(self):
        self.model=QTreeWidgetItem(self)
        self.model.setText(0,'UnTitled Model')