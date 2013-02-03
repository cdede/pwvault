
import subprocess
import time
import os

def copy2clip(key,tip ,value):
    print (key,'  :  ', " | %s copied to clipboard "%tip)
    (subprocess.Popen(['xsel', '-pi'], stdin = subprocess.PIPE)
                         .communicate(value.encode()))
    (subprocess.Popen(['xsel', '-bi'], stdin = subprocess.PIPE)
                         .communicate(value.encode()))
    time.sleep(9)
    subprocess.Popen(['xsel', '-pc'])
    subprocess.Popen(['xsel', '-bc'])

def get_entries(db,geid):
    gid,eid=geid
    ret=[]
    for gr1 in db.groups:
        if gid in gr1.title:
            for ent1 in gr1.entries:
                if eid in ent1.title:
                    ret.append( [gr1,ent1])
    return ret

def getegid(lst1):
    len1=len(lst1)
    if len1 == 1:
        gid=''
        eid=lst1[0]
    elif len1==2:
        gid=lst1[0]
        eid=lst1[1]
    else:
        gid=''
        eid=''
    return [gid,eid]

def getfilename(file1):
    if file1 == '':
        file1 = None
    else:
        file1 = os.path.expanduser(file1)

    return file1

