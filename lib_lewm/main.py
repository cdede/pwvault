#!/usr/bin/python
from cmd import Cmd
from kppy import *
from lib_lewm.common import   opendb
import getopt
import subprocess
import time

class CmdKeepass(Cmd):
    """Simple command processor example."""
    
    def __init__(self, db,sleep=0):
        super(CmdKeepass, self).__init__()
        self.sleep =sleep
        self.db=db
        self.cur_root=self.db._root_group
        self._hist    = []      ## No history yet
        self._loc_ls = []
        self._exp = {}
        self.paths = []
        self.entries={}
        self.isuser=True
        self.walk()
    def copy2clip(self,key,tip ,value):
        print (key,'  :  ', " | %s copied to clipboard "%tip)
        (subprocess.Popen(['xsel', '-pi'], stdin = subprocess.PIPE)
                         .communicate(value.encode()))
        (subprocess.Popen(['xsel', '-bi'], stdin = subprocess.PIPE)
                         .communicate(value.encode()))
        time.sleep(self.sleep)
        tmp1 = subprocess.Popen(['xsel', '-pc'])
        tmp1.wait()
        tmp1 = subprocess.Popen(['xsel', '-bc'])
        tmp1.wait()

    def precmd(self, line):
        """ history
        """
        tmp1 = line.strip() 
        if tmp1 not in self._hist:
            self._hist += [ tmp1 ]
        return line


    def postcmd(self, stop, line):
        self.prompt = '>>' + ''.join(self.paths)+': '
        return super(CmdKeepass,self).postcmd( stop, line)

    def do_hist(self, num):
        if num:
            try :
                num=int(num)
                tmp1 = self._hist[num]
                print(tmp1)
                self.onecmd(tmp1)
            except:
                return
        else:
            range1=0
            for i in self._hist:
                print (range1,i)
                range1+=1

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

    def do_isuser(self):
        self.isuser = not self.isuser 

    def change_group(self):
        entries={}
        for ent1 in self.cur_root.entries:
            if ent1.title != 'Meta-Info' and ent1.username != 'SYSTEM':
                entries[ent1.title]=ent1
        self.entries=entries

    def do_cat(self, person):
        if person:
            if person not in self._exp:
                return
            tmp1 = self._exp[person]
            print('comment :  ',tmp1['comment'])
            print('url :  ',tmp1['url'])
            self.copy2clip(person,'password',tmp1['password'])
            if self.isuser:
                self.copy2clip(person,'username',tmp1['username'])
        else:
            print('hi')

    def walk(self ):
          self.groups=self.cur_root.children

          for i,a1 in self.entries.items() :
              tmp1={}
              tmp1['comment']=a1.comment
              tmp1['url']=a1.url
              tmp1['username']=a1.username
              tmp1['password']=a1.password
              self._exp[self.path+a1.title]=tmp1 

          for i in self.groups :
              self.cur_root = i
              self.change_group()
              self.paths.append(i.title+'_')
              self.path=(''.join(self.paths))
              self.walk()
              self.cur_root = self.cur_root.parent
              self.paths.pop()
    
    def help_cat(self):
        print('\n'.join([ 'cat [person]',
                           'cat the person',
                           ]))
    

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
        self.db.close()
        return True

def main(filename):
    db,sleep1=opendb(filename)
    CmdKeepass(db,sleep1).cmdloop()

if __name__ == '__main__':
    main()
