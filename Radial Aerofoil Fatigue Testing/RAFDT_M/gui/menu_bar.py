#coding=utf-8

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from .. import core

class MenuBar():
    def __init__(self,bar_obj):
        self.RootLevel(bar_obj)

    def RootLevel(self,bar_obj):
        text=('File')
        self.file=bar_obj.addMenu(core.common.trans(text))
        text=('Import')
        self.import_data=bar_obj.addMenu(core.common.trans(text))
        text=('Help')
        self.help=bar_obj.addMenu(core.common.trans(text))