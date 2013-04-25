from lib_lewm.copy_clip import   CopyClip
from lib_lewm.export_db import   ExportDb
class Keepass(CopyClip):
    def __init__(self, db,sleep=0,islist = False):
        super(Keepass, self).__init__(sleep)
        self.islist = islist
        assert type(db) == type({})
        self._exp = db

    def _ls_to_cat(self, key):
        self._loc_cat=[]
        for i in self._loc_ls :
            if key in i :
                self._loc_cat.append(i)

    def fill_ls(self):
        self._loc_ls=[]
        for i,e in self._exp.items():
            self._loc_ls.append( i)
        self._loc_ls.sort()

    def cat(self):
        if len(self._loc_cat) == 1:
            person = self._loc_cat[0]
            tmp1 = self._exp[person]
            print('comment :  ',tmp1['comment'])
            print('url :  ',tmp1['url'])
            self.copy2clip(person,'password',tmp1['password'])
            self.copy2clip(person,'username',tmp1['username'])
        elif len(self._loc_cat) > 1:
            for i in self._loc_cat:
                if self.islist:
                    tmp1 = self._exp[i]
                    print(i,tmp1['username'])
                else:
                    print(i)
        else:
            print('no term')


    def start(self,key):
        self.fill_ls()
        self._ls_to_cat(key)
        self.cat()


