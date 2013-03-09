
import os
import configparser
from getpass import getpass
from kppy import KPDB

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
    sleep1 = int(cf1.get("main", "sleep"))
    keyfile = getfilename(keyfile)
    ret_pass = getpass('input password :')
    db =KPDB(key1, ret_pass ,keyfile, True)
    return db,sleep1

