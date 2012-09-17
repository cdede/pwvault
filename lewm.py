#!/usr/bin/python
from optparse import OptionParser
from kppy import *
import subprocess
import time
import os
import sys
import configparser

def copy2clip(key,tip ,value):
    print (key,'  :  ', " | %s copied to clipboard "%tip)
    (subprocess.Popen(['xsel', '-pi'], stdin = subprocess.PIPE)
                         .communicate(value.encode()))
    (subprocess.Popen(['xsel', '-bi'], stdin = subprocess.PIPE)
                         .communicate(value.encode()))
    time.sleep(9)
    subprocess.Popen(['xsel', '-pc'])
    subprocess.Popen(['xsel', '-bc'])
def main():
    parser = OptionParser()

    parser.add_option("-c", "--conf-file", dest="filename", help="conf FILE", metavar="FILE" ,default= os.path.expanduser('~/.config/lewm/config'))
    (options, args) = parser.parse_args()
    cf1 = configparser.ConfigParser()
    cf1.read(options.filename)
    key1 = cf1.get("main", "key")
    pass1 = cf1.get("main", "pass")
    db = KPDB(os.path.expanduser(key1), subprocess.getoutput(pass1), True)
    len1=len(args)
    if len1 == 1:
        gid=''
        eid=args[0]
    elif len1==2:
        gid=args[0]
        eid=args[1]
    else:
        gid=''
        eid=''
    ret=[]
    for gr1 in db.groups:
        if gid in gr1.title:
            for ent1 in gr1.entries:
                if eid in ent1.title:
                    ret.append( [gr1,ent1])
    len3=len(ret)
    if len3 == 0:
        print ('no record found ')
    elif len3==1:
        tmp1=ret[0]
        copy2clip(tmp1[0].title+'.'+tmp1[1].title,'password',tmp1[1].password)
        try:
            inp1=input('get username?')
        except KeyboardInterrupt:
            db.close()
            sys.exit()
        if inp1=='':
            copy2clip(tmp1[0].title+'.'+tmp1[1].title,'username',tmp1[1].username)
    else:
        for i in ret:
            print (i[0].title+'.'+i[1].title,i[1].username)

    db.close()

if __name__ == "__main__":
    main()
