#!/usr/bin/python
import os
from kppy import KPDB
try:
    from lib_lewm.main import main1
except ImportError:
    os.sys.path.append(os.curdir)
    from lib_lewm.main import CmdKeepass

import unittest
class AppTest(unittest.TestCase):

      def setUp(self):
          self.db = KPDB('test.kdb', 'a' ,None, True)
          self.cmd = CmdKeepass(self.db)
          self.path = ''

      def tearDown(self):
          self.db.close()

      def test_export(self):
          self.cmd.do_export()
          self.assertTrue( self.cmd._exp== {'Internet/e': {'comment': '', 'username': 'e', 'password': 'e', 'url': 'e'}, 'Internet/a/c': {'comment': '', 'username': 'c', 'password': 'c', 'url': 'c'}}
                  )
if __name__ == '__main__':
    unittest.main()
