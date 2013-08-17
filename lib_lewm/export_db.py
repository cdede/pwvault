import json
import subprocess

class ExportDb():
    def __init__(self, db):
        self.entries={}
        self.db=db
        db.load()
        self.cur_root=self.db.root_group
        self.paths = []
        self._exp = {}
        self.walk()
        try:
            self.db.close()
        except:
            pass

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

    def change_group(self):
        entries={}
        for ent1 in self.cur_root.entries:
            if ent1.title != 'Meta-Info' and ent1.username != 'SYSTEM':
                entries[ent1.title]=ent1
        self.entries=entries

