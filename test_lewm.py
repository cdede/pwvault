#!/usr/bin/python
import os
from kppy import KPDB
try:
    from lib_lewm.main import main1
except ImportError:
    os.sys.path.append(os.curdir)
    from lib_lewm.keepass import Keepass
    from lib_lewm.export_db import ExportDb
    from lib_lewm.common import   opendb

import unittest

FLAG=0

class AppTest(unittest.TestCase):

    def setUp(self):
        if FLAG == 1:
            db,sleep1=opendb('config','a')
            self.exp1 = ExportDb(db)
            db,sleep1=opendb('config','a')
        else:
            db,sleep1=opendb('config1','a')
        self.cmd = Keepass(db)

    def tearDown(self):
        pass

    def test_start(self):
        self.cmd.start('')
        self.assertTrue(len(self.cmd._loc_cat)==2)
        self.cmd.start('a')
        self.assertTrue(len(self.cmd._loc_cat)==1)
        self.cmd.start('as')
        self.assertTrue(len(self.cmd._loc_cat)==0)

    def test_export(self):
        if FLAG == 1:
            self.exp1.start('vqydwa')

if __name__ == '__main__':
    unittest.main()
