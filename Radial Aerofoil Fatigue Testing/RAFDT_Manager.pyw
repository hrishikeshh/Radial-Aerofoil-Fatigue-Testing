from PyQt5.QtWidgets import *
import sys
import configparser
import os

import bftm

#Read initialization parameters
ini_para=configparser.ConfigParser()
ini_path=bftm.mdb.package_path+'\\env.ini'
if os.path.isfile(ini_path):
    try:
        ini_para.read(ini_path)
        bftm.mdb.language=ini_para['DEFAULT']['language']
    except:
        pass

#Start the mdb
bftm.core.db.StartMDB()

#Start the GUI
app=QApplication(sys.argv)
bftm.mdb.window=bftm.gui.main_window.MainWindow()
bftm.mdb.window.show()
app.exec_()