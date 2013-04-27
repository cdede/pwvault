#!/usr/bin/python
from lib_lewm.export_db import ExportDb

class PassServer():
    def __init__(self, db):
        exp1 = ExportDb(db)
        self._exp = exp1._exp

    def fill_ls(self):
        self._loc_ls=[]
        for i,e in self._exp.items():
            self._loc_ls.append( i)
        self._loc_ls.sort()

    def ls_to_cat(self, key):
        self._loc_cat=[]
        for i in self._loc_ls :
            if key in i :
                self._loc_cat.append(i)

    def cat(self):
        str1 = ''
        dict1 = {}
        if len(self._loc_cat) == 1:
            person = self._loc_cat[0]
            tmp1 = self._exp[person]
            str1 += 'comment :  %s\n' % tmp1['comment'] 
            str1 += 'url :  %s\n' % tmp1['url']
            dict1['key']=person
            dict1['password']=tmp1['password']
            dict1['username']=tmp1['username']
        elif len(self._loc_cat) > 1:
            for i in self._loc_cat:
                if self.islist:
                    tmp1 = self._exp[i]
                    str1 += '%s   %s\n' % (i, tmp1['username'])
                else:
                    str1 += i + "\n"
        else:
            str1 += 'no term' + "\n"
        return str1,dict1


    def start_key(self,msg):
        key,islist = msg
        self.islist = islist
        self.fill_ls()
        self.ls_to_cat(key)
        asd = self.cat()
        return asd

