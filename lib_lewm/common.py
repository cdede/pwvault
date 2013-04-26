
import os
import configparser
from getpass import getpass
from kppy import KPDB
import subprocess
import json

port = 50000

def getfilename(file1):
    if file1 == '':
        file1 = None
    else:
        file1 = os.path.expanduser(file1)

    return file1

def opendb(filename,password1=''):
    filename=os.path.expanduser(filename)
    cf1 = configparser.ConfigParser()
    cf1.read(filename)
    key1 = cf1.get("main", "key")
    key1 = getfilename(key1)
    sleep1 = int(cf1.get("main", "sleep"))
    if os.path.splitext(key1)[1] == '.gpg':
        ret= subprocess.Popen(args='gpg --output - %s' % key1, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()[0]
        db=json.loads(ret.decode("utf-8"))
    else:
        keyfile = cf1.get("main", "keyfile")
        keyfile = getfilename(keyfile)
        if password1 == '':
            ret_pass = getpass('input password :')
        else:
            ret_pass = password1
        db =KPDB(key1, ret_pass ,keyfile, True)
    return db,sleep1

