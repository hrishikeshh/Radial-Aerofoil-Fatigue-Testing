#coding=utf-8

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSvg import QSvgWidget

from .. import media

class BackgroundTab():
    def __init__(self):
        self.img_path=media.img.ImgPath()
        self.IniUIElements()
        self.DrawTab()

    def IniUIElements(self):
        self.DefinePicture()

    def DefinePicture(self):
        self.pic=QSvgWidget(self.img_path.background)
        self.pic.setFixedSize(400,400)

    def DrawTab(self):
        wp_layout=QHBoxLayout()
        wp_layout.addWidget(self.pic)
        self.tab_widget=QWidget()
        self.tab_widget.setLayout(wp_layout)