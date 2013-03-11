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

KEY= 'vqydwa'

class ExportDbTest(unittest.TestCase):

    def setUp(self):
         db,sleep1=opendb('config','a')
         self.exp1 = ExportDb(db)

    def tearDown(self):
        pass

    def test_export(self):
        self.exp1.start('vqydwa')

class KeepassTest(unittest.TestCase):
    def setUp(self):
        db,sleep1=opendb('config1','a')
        self.cmd = Keepass(db)
    def test_start(self):
        self.cmd.start('')
        self.assertTrue(len(self.cmd._loc_cat)==2)
        self.cmd.start('a')
        self.assertTrue(len(self.cmd._loc_cat)==1)
        self.cmd.start('as')
        self.assertTrue(len(self.cmd._loc_cat)==0)


if __name__ == '__main__':
    unittest.main()
