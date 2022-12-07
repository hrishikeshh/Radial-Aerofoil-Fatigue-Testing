#coding=utf-8

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os

from .. import media
from .. import mdb
from .. import core
from . import msg_box

#Python version dependent packages
if mdb.python_version==3:
    import _thread as thread
else:
    import thread

class ImportStrainDataDialog(QDialog):
    def __init__(self,parent):
        super(ImportStrainDataDialog, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setMinimumSize(800,600)
        text=('Import Strain Data Wizard')
        self.setWindowTitle(core.common.trans(text))
        self.IniUIElements()
        self.DrawLayout()

    def IniUIElements(self):
        text=('Browse File')
        self.browse_button=QPushButton(core.common.trans(text))
        self.browse_button.setFixedWidth(150)
        self.browse_button.clicked.connect(self.BrowseButtonClicked)

        self.file_table=QTableWidget(2,2)
        header=(('File Names'),('Format Type'))
        self.file_table.setHorizontalHeaderLabels(core.common.trans(header))
        self.file_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.file_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.file_table.setColumnWidth(0,300)
        self.file_table.setColumnWidth(1,200)

        text=('Back')
        self.back_button=QPushButton(core.common.trans(text))
        self.back_button.setFixedWidth(100)
        self.back_button.setDisabled(True)

        text=('Next')
        self.next_button=QPushButton(core.common.trans(text))
        self.next_button.setFixedWidth(100)
        self.next_button.setDisabled(True)

        text=('Cancel')
        self.cancel_button=QPushButton(core.common.trans(text))
        self.cancel_button.setFixedWidth(100)
        self.cancel_button.clicked.connect(self.CancelButtonClicked)

        self.data_processing_table=QTableWidget(2,2)
        header=(('File Names'),('Status')
        self.data_processing_table.setHorizontalHeaderLabels(core.common.trans(header))
        self.data_processing_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.data_processing_table.setSelectionBehavior(QAbstractItemView.SelectRows)

    def IniDB(self):
        self.strain_files=[]
        self.msg_box_action=None

    def DrawLayout(self):
        tree_layout=QVBoxLayout()
        self.tree=WizardTree()
        for n in self.tree.items:
            tree_layout.addWidget(n)
        tree_layout.addStretch()

        self.stack=QStackedWidget()
        self.stack.addWidget(self.BrowseFileStackWidget())
        self.stack.addWidget(self.ProcessDataStackWidget())

        self.stack.setCurrentIndex(0)

        top_layout=QHBoxLayout()
        top_layout.addLayout(tree_layout)
        v_separator=QFrame()
        v_separator.setFrameShape(QFrame.VLine)
        v_separator.setFrameShadow(QFrame.Sunken)
        top_layout.addWidget(v_separator)
        top_layout.addWidget(self.stack)

        nav_layout=QHBoxLayout()
        nav_layout.addStretch()
        nav_layout.addWidget(self.back_button)
        nav_layout.addWidget(self.next_button)
        nav_layout.addWidget(self.cancel_button)

        dia_layout=QVBoxLayout()
        h_separator=QFrame()
        h_separator.setFrameShape(QFrame.HLine)
        h_separator.setFrameShadow(QFrame.Sunken)
        dia_layout.addLayout(top_layout)
        dia_layout.addWidget(h_separator)
        dia_layout.addLayout(nav_layout)

        self.setLayout(dia_layout)

    def BrowseFileStackWidget(self):
        button_layout=QVBoxLayout()
        #button_layout.addStretch()
        button_layout.addWidget(self.browse_button)

        lower_layout=QHBoxLayout()
        lower_layout.addStretch()
        lower_layout.addLayout(button_layout)

        tab_layout=QVBoxLayout()
        tab_layout.addWidget(self.file_table)
        tab_layout.addLayout(lower_layout)

        text=('Strain Data File Selection')
        tab_group=QGroupBox(core.common.trans(text))
        tab_group.setLayout(tab_layout)
        return tab_group

    def ProcessDataStackWidget(self):
        tab_layout=QVBoxLayout()
        tab_layout.addWidget(self.data_processing_table)

        tab_widget=QWidget()
        tab_widget.setLayout(tab_layout)
        return tab_widget

    def BrowseButtonClicked(self):
        text1=('Select a Strain Data File')
        text2=('Plain Text(*.txt)')
        path=QFileDialog.getOpenFileNames(self,core.common.trans(text1),\
        mdb.current_path,core.common.trans(text2))
        if not len(path[0])==0:
            self.StrainFileBrowsed(path)
            #thread.start_new_thread(core.parser.ParseStrainFile,(path[0][0],'a',self,))

    def StrainFileBrowsed(self,path):
        file_no=len(path[0])
        self.file_table.setRowCount(file_no)
        for n in range(0,file_no):
            file_name=path[0][n]
            file_name=file_name.split('/')[-1]
            cell_item=QTableWidgetItem('%s' %file_name)
            self.file_table.setItem(n,0,cell_item)
            cell_item=TypeComboGenerator()
            self.file_table.setCellWidget(n,1,cell_item)
            file_db={'path':file_name,'type':None}
            self.strain_files.append(file_db)

    def StrainParsingFinishedRedirector(self,result):
        pass

    def NextButtonAvailibility(self,page_index):
        availibility=True
        if page_index==0:
            #Number of strain files shall greater than 0.
            if len(self.strain_files)==0:
                availibility=False
            #All files shall be assigned with a format type.
            for n in self.strain_files:
                if n['type']==None:
                    availibility=False
        elif page_index==1:
            pass
        self.next_button.setDisabled(not availibility)

    def MsgBoxInterface(self,flag):
        if self.msg_box_action=='exit':
            if flag:
                self.close()

    def CancelButtonClicked(self):
        self.msg_box_action='exit'
        msg=(('Data importing has not finished.'),\
        ('Data will loss if exit.'))
        warning_box=msg_box.WarningBox(self,msg)
        warning_box.exec_()

class WizardTree():
    def __init__(self):
        self.items=[]
        text=('Browse Files')
        self.items.append(QLabel(core.common.trans(text)))
        text=('Data Processing')
        self.items.append(QLabel(core.common.trans(text)))
        self.SetCurrentStep(0)

    def SetCurrentStep(self,current_step):
        if current_step<0 or current_step>=len(self.items):
            return
        done_font=QFont("Times", 10, QFont.Normal)
        current_font=QFont("Times", 10, QFont.Bold)
        todo_font=QFont("Times", 10, QFont.Normal)
        for n in range(0,len(self.items)):
            if n<current_step:
                self.items[n].setFont(done_font)
            elif n==current_step:
                self.items[n].setFont(current_font)
            else:
                self.items[n].setFont(todo_font)

class TypeComboGenerator(QComboBox):
    def __init__(self):
        super(TypeComboGenerator,self).__init__()
        text=('Please select format type')
        self.addItem(core.common.trans(text))
        self.addItem('a')