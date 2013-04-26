#!/usr/bin/python
import os
from kppy import KPDB
try:
    from lib_lewm.main import main1
except ImportError:
    os.sys.path.append(os.curdir)
    from lib_lewm.server import PassServer
    from lib_lewm.common import   opendb

import unittest

class KeepassTest(unittest.TestCase):
    def setUp(self):
        filename = 'config'
        pidfile = '/tmp/server.pid'
        self.cmd = PassServer(pidfile,filename)
    def test_start(self):
        a= self.cmd.start_key(['',True])
        self.assertTrue(('Internet_a_c   c\nInternet_e   e\n', {})==a)
        a= self.cmd.start_key(['a',True])
        self.assertTrue(('comment :  \nurl :  c\n', {'password': 'c', 'key': 'Internet_a_c', 'username': 'c'})==a)
        a= self.cmd.start_key(['as',True])
        self.assertTrue(('no term\n', {})==a)


if __name__ == '__main__':
    unittest.main()
