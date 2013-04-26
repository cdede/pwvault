import hashlib 
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
    keyfile = cf1.get("main", "keyfile")
    keyfile = getfilename(keyfile)
    hash_pass = cf1.get("main", "hash_pass")
    if password1 == '':
        ret_pass = getpass('input password :')
    else:
        ret_pass = password1
    db =KPDB(key1, ret_pass ,keyfile, True)
    return db,hash_pass

def hash_str(str1):
    h1 = hashlib.new('sha512')
    h1.update(str1.encode())
    return h1.hexdigest()

