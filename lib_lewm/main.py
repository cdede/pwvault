#!/usr/bin/python
from cmd import Cmd
from kppy import *
from lib_lewm.common import copy2clip,  opendb
import getopt

class CmdKeepass(Cmd):
    """Simple command processor example."""
    
    def __init__(self, db):
        super(CmdKeepass, self).__init__()
        self.db=db
        self.cur_root=self.db._root_group
        self._hist    = []      ## No history yet
        self._loc_ls = []
        self._exp = {}
        self.entries={}
        self.onecmd('cd')
        self.isuser=True

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

    def change_root(self):    
        self.groups=self.cur_root.children
        self.comp_group = [ i.title
                  for i in self.groups 
                  ]
        tmp1=self.comp_group
        self.dict_groups=dict(zip(tmp1, range(len(tmp1))))

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

    def do_cd(self, person):
        if not person:
            self.cur_root = self.db._root_group
            self.paths=[]
            self.prompt = '>>' + ''.join(self.paths)+': '
        elif person !='..':
            if person not in self.dict_groups:
                return
            tmp1 = self.groups[self.dict_groups[person]]
            self.cur_root = tmp1
            self.paths.append(tmp1.title+'/')
        elif person =='..':
            if self.cur_root is self.db._root_group:
                return
            else:
                self.cur_root = self.cur_root.parent
                self.paths.pop()
        else:
            pass

        self.change_root()
        self.change_group()

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
        for i,e in self.entries.items():
            if islist:
                self._loc_ls.append( i+' ' +e.username)
            else:
                self._loc_ls.append( i)
        for i in self.comp_group:
            self._loc_ls.append(i+'/')
        self._print_ls(text)

    def do_isuser(self):
        self.isuser = not self.isuser 

    def change_group(self):
        entries={}
        for ent1 in self.cur_root.entries:
            if ent1.title != 'Meta-Info' and ent1.username != 'SYSTEM':
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

    def test_cat(self, person):
        if person:
            if person not in self.entries:
                return
            tmp1 = self.entries[person]
            return tmp1
        else:
            print('hi')

    def walk(self, list1):
          list2 = [ i   for i in list1
                  if i[-1]=='/'
                  ]
          list3 = [ i   for i in list1
                  if i[-1]!='/'
                  ]
          for j in list3:
              a1=self.test_cat(j)
              tmp1={}
              tmp1['comment']=a1.comment
              tmp1['url']=a1.url
              tmp1['username']=a1.username
              tmp1['password']=a1.password
              self._exp[self.path+a1.title]=tmp1 

          for i in list2:
              self.do_cd(i[:-1])
              self.do_ls('')
              list1 = self._loc_ls
              self.path=(''.join(self.paths))
              self.walk(list1)
              self.do_cd('..')
    
    def do_export(self):
        self.do_ls('')
        list1 = self._loc_ls
        self.walk(list1)


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
        self.db.close()
        return True

def main(filename):
    db=opendb(filename)
    CmdKeepass(db).cmdloop()

if __name__ == '__main__':
    main()
