#!/usr/bin/python
from cmd import Cmd
from kppy import *
from lib_lewm.common import   opendb
from lib_lewm.export_db import   ExportDb
from lib_lewm.copy_clip import   CopyClip
import getopt
import subprocess
import json

class CmdKeepass(Cmd):
    """Simple command processor example."""
    
    def __init__(self, db,sleep=0):
        super(CmdKeepass, self).__init__()
        self.copy2clip=CopyClip(sleep).copy2clip
        if type(db) == type({}):
            self._exp = db
            self.isdb=False
        else:
            self.isdb=True
            self._exp = ExportDb(db)._exp

    def _print_ls(self, key):
        for i in self._loc_ls :
            if key in i :
                print(i)

    def do_ls(self, person):
        try:
            options, remainder = getopt.getopt(person.split(), 'l')
        except:
            return
        islist = False
        for opt, arg in options:
            if opt == '-l':
                islist = True
        text = ''
        if len(remainder)>=1:
            text = remainder[0]
        self._loc_ls=[]
        for i,e in self._exp.items():
            if islist:
                self._loc_ls.append( i+' ' +e['username'])
            else:
                self._loc_ls.append( i)
        self._loc_ls.sort()
        self._print_ls(text)

    def do_cat(self, person):
        if person:
            if person not in self._exp:
                return
            tmp1 = self._exp[person]
            print('comment :  ',tmp1['comment'])
            print('url :  ',tmp1['url'])
            self.copy2clip(person,'password',tmp1['password'])
            self.copy2clip(person,'username',tmp1['username'])

    def complete_cat(self, text, line, begidx, endidx):
        comp1 = list(self._exp.keys())
        if not text:
            completions = comp1[:]
        else:
            completions = [ f
                            for f in comp1
                            if f.startswith(text)
                            ]
        return completions

  
    def do_EOF(self, line):
        return True

def main(filename):
    db,sleep1=opendb(filename)
    CmdKeepass(db,sleep1).cmdloop()

if __name__ == '__main__':
    main()
