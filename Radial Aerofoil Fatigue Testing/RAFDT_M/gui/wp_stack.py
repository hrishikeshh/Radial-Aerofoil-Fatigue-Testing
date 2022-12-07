from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from . import background_tab
from . import project_overview_tab

class WPStack(QStackedWidget):
    def __init__(self):
        super(WPStack, self).__init__()
        self.IniTabs()

    def IniTabs(self):
        #Index=0
        self.background=background_tab.BackgroundTab()
        self.addWidget(self.background.tab_widget)
        #Index=1
        self.overview=project_overview_tab.ProjectOverviewTab()
        self.addWidget(self.overview.tab_widget)

    def Flag2Index(self,flag):
        if flag=='background':
            return 0
        elif flag=='project_overview':
            return 1