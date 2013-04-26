import hashlib 
import os
import configparser
from getpass import getpass
from kppy import KPDB
import subprocess
import json

port = 50000
hash_pass = 'ddaf35a193617abacc417349ae20413112e6fa4e89a97ea20a9eeee64b55d39a2192992a274fc1a836ba3c23a3feebbd454d4423643ce80e2a9ac94fa54ca49f'

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
    keyfile = cf1.get("main", "keyfile")
    keyfile = getfilename(keyfile)
    if password1 == '':
        ret_pass = getpass('input password :')
    else:
        ret_pass = password1
    db =KPDB(key1, ret_pass ,keyfile, True)
    return db,sleep1

def hash_str(str1):
    h1 = hashlib.new('sha512')
    h1.update(str1.encode())
    return h1.hexdigest()

