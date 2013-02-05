#!/usr/bin/python
from cmd import Cmd
from kppy import *
from lib_lewm.common import copy2clip,  opendb
import getopt

class HelloWorld(Cmd):
    """Simple command processor example."""
    
    def __init__(self, db):
        super(HelloWorld, self).__init__()
        self.db=db
        self.cur_root=self.db._root_group
        self.paths=[]
        self.entries={}
        self.prompt = '>>' + ''.join(self.paths)+': '
        self.change_root()
        self.isuser=True

    def postcmd(self, stop, line):
        self.prompt = '>>' + ''.join(self.paths)+': '
        return super(HelloWorld,self).postcmd( stop, line)

    def change_root(self):    
        self.groups=self.cur_root.children
        self.comp_group = [ i.title
                  for i in self.groups 
                  ]
        tmp1=self.comp_group
        self.dict_groups=dict(zip(tmp1, range(len(tmp1))))

    def do_cd(self, person):
        if person:
            if person not in self.dict_groups:
                return
            tmp1 = self.groups[self.dict_groups[person]]
            self.cur_root = tmp1
            self.paths.append(tmp1.title+'/')
        else:
            if self.cur_root is self.db._root_group:
                return
            else:
                self.cur_root = self.cur_root.parent
                self.paths.pop()
        self.change_root()
        self.change_group()

    def do_ls(self, person):
        try:
            options, remainder = getopt.getopt(person.split(), 'l')
        except:
            return
        islist = False
        for opt, arg in options:
            if opt == '-l':
                islist = True
        for i,e in self.entries.items():
            if islist:
                print(i,e.username)
            else:
                print (i)
        for i in self.comp_group:
            print (i+'/')

    def do_isuser(self):
        self.isuser = not self.isuser 

    def change_group(self):
        entries={}
        for ent1 in self.cur_root.entries:
            entries[ent1.title]=ent1
        self.entries=entries

    def help_cd(self):
        print('\n'.join([ 'cd [person]',
                           'cd the dir',
                           ]))
    def complete_cd(self, text, line, begidx, endidx):
        comp1 = self.comp_group
        if not text:
            completions = comp1[:]
        else:
            completions = [ f
                            for f in comp1
                            if f.startswith(text)
                            ]
        return completions

    def do_cat(self, person):
        if person:
            if person not in self.entries:
                return
            tmp1 = self.entries[person]
            print('comment :  ',tmp1.comment)
            print('url :  ',tmp1.url)
            copy2clip(self.cur_root.title+'.'+tmp1.title,'password',tmp1.password)
            if self.isuser:
                copy2clip(self.cur_root.title+'.'+tmp1.title,'username',tmp1.username)
        else:
            print('hi')

    def help_cat(self):
        print('\n'.join([ 'cat [person]',
                           'cat the person',
                           ]))
    

    def complete_cat(self, text, line, begidx, endidx):
        comp1 = list(self.entries.keys())
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
    db=opendb(filename)
    HelloWorld(db).cmdloop()

if __name__ == '__main__':
    main()
