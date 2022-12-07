#coding=utf-8

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from .. import mdb
from .. import core
from . import import_strain_dia

class ProjectOverviewTab():
    def __init__(self):
        self.IniUIElements()
        self.DrawTab()

    def IniUIElements(self):
        text=('Import Strain')
        self.import_data_button=QPushButton(core.common.trans(text))
        self.import_data_button.setFixedWidth(200)
        self.import_data_button.clicked.connect(self.ImportStrainButtonClicked)

    def DrawTab(self):
        button_layout=QVBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.import_data_button)
        tab_layout=QHBoxLayout()
        tab_layout.addStretch()
        tab_layout.addLayout(button_layout)

        self.tab_widget=QWidget()
        self.tab_widget.setLayout(tab_layout)

    def ImportStrainButtonClicked(self):
        self.import_dia=import_strain_dia.ImportStrainDataDialog(mdb.window)
        self.import_dia.exec_()