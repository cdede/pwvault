#!/usr/bin/python
from optparse import OptionParser
from kppy import *
import subprocess
import time
import os
import sys
import configparser
from getpass import getpass

def copy2clip(key,tip ,value):
    print (key,'  :  ', " | %s copied to clipboard "%tip)
    (subprocess.Popen(['xsel', '-pi'], stdin = subprocess.PIPE)
                         .communicate(value.encode()))
    (subprocess.Popen(['xsel', '-bi'], stdin = subprocess.PIPE)
                         .communicate(value.encode()))
    time.sleep(9)
    subprocess.Popen(['xsel', '-pc'])
    subprocess.Popen(['xsel', '-bc'])

def get_entries(db,gid,eid):
    ret=[]
    for gr1 in db.groups:
        if gid in gr1.title:
            for ent1 in gr1.entries:
                if eid in ent1.title:
                    ret.append( [gr1,ent1])
    return ret

def main():
    parser = OptionParser()

    parser.add_option("-c", "--conf-file", dest="filename", help="conf FILE", metavar="FILE" ,default= os.path.expanduser('~/.config/lewm/config'))
    parser.add_option("-a", "--add", action="store_true", dest="add",
                      help="add password", default=False)
    parser.add_option("-s", "--show-all", action="store_true", dest="show_all",
                      help="show url and comment", default=False)
    (options, args) = parser.parse_args()
    cf1 = configparser.ConfigParser()
    cf1.read(options.filename)
    key1 = cf1.get("main", "key")
    pass1 = cf1.get("main", "pass")
    keyfile = cf1.get("main", "keyfile")
    
    key2 = cf1.get(pass1, "key")
    pass2 = None
    keyfile2 = cf1.get(pass1, "keyfile")

    key2=os.path.expanduser(key2)
    keyfile2=os.path.expanduser(keyfile2)
    group2=cf1.get(pass1, "group")
    title2=cf1.get(pass1, "title")
    if options.add:
        filebuffer = getpass('input password :')
        filebuffer1 = getpass('repeat input password :')
        if filebuffer1 == filebuffer :
            password2 = filebuffer
        else:
            print ('not match')
            sys.exit()

        db2 = KPDB(new = True)
        db2.keyfile = keyfile2
        db2.create_group(group2)
        for gr1 in db2.groups:
            if group2 == gr1.title:
                break
        gr1.create_entry(title2,1,'','',password2,'',2999,12,28)
        db2.save(key2+'.new')
        db2.close()
        sys.exit()

    db2 = KPDB(key2, pass2 ,keyfile2, True)
    ret=get_entries(db2, group2, title2)
    ret_pass=ret[0][1].password
    db2.close()
    if keyfile == '':
        keyfile = None
    else:
        keyfile = os.path.expanduser(keyfile)
    db = KPDB(os.path.expanduser(key1), ret_pass ,keyfile, True)
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
    ret=get_entries(db,gid,eid)
    len3=len(ret)
    if len3 == 0:
        print ('no record found ')
    elif len3==1:
        tmp1=ret[0]
        if options.show_all :
            print('comment :  ',tmp1[1].comment)
            print('url :  ',tmp1[1].url)
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
