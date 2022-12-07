#coding=utf-8

from .. import mdb

def trans(text_list):
    if mdb.language=='ch':
        index=1
    else:
        index=0

    if type(text_list[0])==type('wtf'):
        return text_list[index]
    elif type(text_list[0])==type([]) or type(text_list[0])==type((0,0)):
        return [n[index] for n in text_list]

def ProgramVersionStr():
    version_str='%d.%d.%d' %(mdb.version[0],mdb.version[1],mdb.version[2])
    return version_str

def WindowTitle():
    text=('Blade Fatigue Test Data Manager','_____')
    title=trans(text)
    title=title+'-V%s' %ProgramVersionStr()
    return title