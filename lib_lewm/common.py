import os
import configparser
from getpass import getpass
from kppy import KPDB
import subprocess

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
    hash_pass = getfilename(hash_pass)
    if password1 == '':
        password1= subprocess.Popen(args='gpg --quiet  --batch --output - %s' % hash_pass, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()[0]
        ret_pass = password1.decode("utf-8")
    else:
        ret_pass = password1
    db =KPDB(key1, ret_pass ,keyfile, True)
    sleep = cf1.get("main", "sleep")
    return db,sleep

def gen_pass(key):
    ret_pass = getpass('input password :')
    ret_pass1 = getpass('reinput password :')
    if ret_pass == ret_pass1:
        p = subprocess.Popen([ 'gpg' ,'-er',   key,'--output', 'w.gpg'],stdout=subprocess.PIPE,stdin=subprocess.PIPE)
        p.stdin.write(bytes(ret_pass , "ascii"))
        assert(b''==p.communicate()[0])
        p.stdin.close()

