#!/usr/bin/python
from optparse import OptionParser
from kppy import *
import subprocess
import time

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
    parser.add_option("-f", "--file", dest="filename", help="keepass FILE", metavar="FILE")
    parser.add_option("-p", "--pass", dest="passcmd", help="pass CMD", metavar="pass")
    parser.add_option("-c", "--check", action="store_true", dest="check",
                      help="check mail", default=False)
    parser.add_option("-a", "--add", action="store_true", dest="add",
                      help="add mail conf", default=False)
    (options, args) = parser.parse_args()
    db = KPDB(options.filename, subprocess.getoutput(options.passcmd), True)
    len1=len(args)
    if len1 == 1:
        gid=''
        eid=args[0]
    elif len1==2:
        gid=args[0]
        eid=args[1]
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
        inp1=input('get username?')
        if inp1=='':
            copy2clip(tmp1[0].title+'.'+tmp1[1].title,'username',tmp1[1].username)
    else:
        for i in ret:
            print (i[0].title+'.'+i[1].title,i[1].username)

    db.close()

if __name__ == "__main__":
    main()
