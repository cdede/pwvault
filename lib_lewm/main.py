#!/usr/bin/python
from cmd import Cmd
from kppy import *
from lib_lewm.common import   opendb
from lib_lewm.export_db import   ExportDb
from lib_lewm.copy_clip import   CopyClip
import getopt
import subprocess
import json
    
def main(filename):
    db,sleep1=opendb(filename)
    CmdKeepass(db,sleep1).cmdloop()

if __name__ == '__main__':
    main()
