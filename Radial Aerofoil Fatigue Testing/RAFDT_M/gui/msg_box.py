#coding=utf-8
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSvg import QSvgWidget

from .. import media
from .. import core

class WarningBox(QDialog):
    def __init__(self,parent,msg):
        super(WarningBox,self).__init__(parent)
        self.my_parent=parent
        self.img_path=media.img.ImgPath()
        self.setWindowIcon(self.img_path.main_icon)
        title=('Warning')
        self.setWindowTitle(core.common.trans(title))
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setMinimumSize(400,120)
        self.DefineUIElements()
        self.msg=msg
        self.Start()

    def Start(self):
        msg=core.common.trans(self.msg)

        top_right_layout=QVBoxLayout()
        if type(msg)==type('str'):
            label=QLabel(msg)
            label.setAlignment(Qt.AlignLeft)
            top_right_layout.addWidget(label)
        elif type(msg)==type([]) or type(msg)==type((0,)):
            labels=[]
            for n in msg:
                labels.append(QLabel('%s' %n))
                labels[-1].setAlignment(Qt.AlignLeft)
            for n in range(0,len(labels)):
                top_right_layout.addWidget(labels[n])
        top_right_layout.addStretch()

        label=QSvgWidget(self.img_path.warning_yellow)
        label.setFixedSize(100,100)
        
        top_layout=QHBoxLayout()
        top_layout.addWidget(label)
        top_layout.addLayout(top_right_layout)

        button_layout=QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        dia_layout=QVBoxLayout()
        dia_layout.addLayout(top_layout)
        dia_layout.addLayout(button_layout)

        self.setLayout(dia_layout)

    def DefineUIElements(self):
        text=('OK')
        self.ok_button=QPushButton(core.common.trans(text))
        self.ok_button.clicked.connect(self.OKButtonClicked)
        self.ok_button.setFixedWidth(100)

        text=('Cancel')
        self.cancel_button=QPushButton(core.common.trans(text))
        self.cancel_button.setFixedWidth(100)
        self.cancel_button.clicked.connect(self.close)

    def OKButtonClicked(self):
        self.my_parent.MsgBoxInterface(True)
        self.close()

class QuestionBox(QDialog):
    def __init__(self,parent,msg):
        super(QuestionBox,self).__init__(parent)
        self.my_parent=parent
        self.img_path=media.img.ImgPath()
        self.setWindowIcon(self.img_path.main_icon)
        title=('Question')
        self.setWindowTitle(core.common.trans(title))
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setMinimumSize(400,120)
        self.DefineUIElements()
        self.msg=msg
        self.Start()

    def Start(self):
        msg=core.common.trans(self.msg)

        top_right_layout=QVBoxLayout()
        if type(msg)==type('str'):
            label=QLabel(msg)
            label.setAlignment(Qt.AlignLeft)
            top_right_layout.addWidget(label)
        elif type(msg)==type([]) or type(msg)==type((0,)):
            labels=[]
            for n in msg:
                labels.append(QLabel('%s' %n))
                labels[-1].setAlignment(Qt.AlignLeft)
            for n in range(0,len(labels)):
                top_right_layout.addWidget(labels[n])
        top_right_layout.addStretch()

        label=QSvgWidget(self.img_path.question_blue)
        label.setFixedSize(100,100)
        
        top_layout=QHBoxLayout()
        top_layout.addWidget(label)
        top_layout.addLayout(top_right_layout)

        button_layout=QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.yes_button)
        button_layout.addWidget(self.no_button)

        dia_layout=QVBoxLayout()
        dia_layout.addLayout(top_layout)
        dia_layout.addLayout(button_layout)

        self.setLayout(dia_layout)

    def DefineUIElements(self):
        text=('Yes')
        self.yes_button=QPushButton(core.common.trans(text))
        self.yes_button.clicked.connect(self.YesButtonClicked)
        self.yes_button.setFixedWidth(100)

        text=('No')
        self.no_button=QPushButton(core.common.trans(text))
        self.no_button.setFixedWidth(100)
        self.no_button.clicked.connect(self.NoButtonClicked)

    def YesButtonClicked(self):
        self.my_parent.MsgBoxInterface(True)
        self.close()

    def NoButtonClicked(self):
        self.my_parent.MsgBoxInterface(False)
        self.close()