from PyQt5.QtGui import *
import configparser

from .. import mdb

class ImgPath():
    def __init__(self):
        self.folder_path=mdb.package_path+'\\media\\'
        self.path_parser=configparser.ConfigParser()
        self.path_parser.read(self.folder_path+'path.inf')
        self.svgs()
        self.icons()

    def svgs(self):
        self.background=self.folder_path+self.path_parser['svg']['background']
        self.warning_yellow=self.folder_path+self.path_parser['svg']['warning_yellow']
        self.question_blue=self.folder_path+self.path_parser['svg']['question_blue']

    def icons(self):
        main_icon_path=self.folder_path+self.path_parser['icon']['icon']
        self.main_icon=QIcon(main_icon_path)