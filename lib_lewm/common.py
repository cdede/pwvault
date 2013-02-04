
import subprocess
import time
import os
import configparser
from getpass import getpass
from kppy import KPDB

def copy2clip(key,tip ,value):
    print (key,'  :  ', " | %s copied to clipboard "%tip)
    (subprocess.Popen(['xsel', '-pi'], stdin = subprocess.PIPE)
                         .communicate(value.encode()))
    (subprocess.Popen(['xsel', '-bi'], stdin = subprocess.PIPE)
                         .communicate(value.encode()))
    time.sleep(9)
    subprocess.Popen(['xsel', '-pc'])
    subprocess.Popen(['xsel', '-bc'])

def getfilename(file1):
    if file1 == '':
        file1 = None
    else:
        file1 = os.path.expanduser(file1)

    return file1

def opendb(filename):
    filename=os.path.expanduser(filename)
    cf1 = configparser.ConfigParser()
    cf1.read(filename)
    key1 = cf1.get("main", "key")
    key1 = getfilename(key1)
    keyfile = cf1.get("main", "keyfile")
    keyfile = getfilename(keyfile)
    ret_pass = getpass('input password :')
    db =KPDB(key1, ret_pass ,keyfile, True)
    return db

