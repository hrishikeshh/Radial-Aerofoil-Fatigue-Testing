from .. import mdb

#Python version dependent packages
if mdb.python_version==3:
    import pickle
else:
    import cPickle as pickle

class Strain():
    def __init__(self):
        self.file_name=''
        self.header=None
        self.freq=None

def StartMDB():
    mdb.project_path=''
    mdb.project_name=''
    mdb.project_saved=True
    mdb.strain=[]
    mdb.sc=[]

def SaveProject2File(path):
    pass