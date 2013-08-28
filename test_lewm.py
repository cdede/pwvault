#!/usr/bin/python
import os
try:
    from lib_lewm.main import main1
except ImportError:
    os.sys.path.append(os.curdir)
    from lib_lewm.keepass import PassServer
    from lib_lewm.common import   opendb,open_conf_1
    from lib_lewm.export_db import   ExportDb

import unittest
class KeepassTest(unittest.TestCase):
    def setUp(self):
        filename = 'example_export.conf'
        try:
            os.unlink('w.gpg')
        except :
            pass
        db ,key1= opendb(filename,'a')
        ed1 = ExportDb(db,key1)
        ed1.export()
        filename1 = 'example_config'
        file1,_=open_conf_1(filename1 )

        self.cmd = PassServer(file1)
    def test_start(self):
        a= self.cmd.start_key(['',True])
        self.assertTrue(('Internet_a_c   c\nInternet_e   e\n', {})==a)
        a= self.cmd.start_key(['a',True])
        self.assertTrue(('comment :  \nurl :  c\n', {'password': 'c', 'key': 'Internet_a_c', 'username': 'c'})==a)
        a= self.cmd.start_key(['as',True])
        self.assertTrue(('no term\n', {})==a)


if __name__ == '__main__':
    unittest.main()
