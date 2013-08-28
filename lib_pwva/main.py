import argparse
from .common import gen_pass
from .copy_clip import   CopyClip
from .keepass import   PassServer
from .common import   opendb, open_conf_1
from .export_db import ExportDb
import sys
import os

def arg_parse():
    "Parse the command line arguments"
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--filename', help='conf filename'
            , default='')
    parser.add_argument('cmd', default=None,
                        help='...(cmd)...', type=str)
    parser.add_argument('-l','--list', action='store_true',default=False, dest='list',
                        help='list username' )
    parser.add_argument('-g','--gpg-pass', action='store_true',default=False, dest='gpg',
                        help='gpg password' )
    parser.add_argument('-e','--export', action='store_true',default=False, 
                        help='export keepass file' )
    return parser.parse_args()

def main():
    args = arg_parse()
    if args.filename == '':
        if args.export:
            filename = '~/.config/pwvault/export.conf'
        else:
            filename = '~/.config/pwvault/config'
    else:
        filename = args.filename
    if args.gpg:
        gen_pass(args.cmd)
        sys.exit()
    elif args.export:
        db, key1=opendb(filename )
        ed1 = ExportDb(db,key1,os.path.basename(args.cmd))
        ed1.export()
        sys.exit()
    file1,sleep=open_conf_1(filename )
    sleep = int(sleep)
    server = PassServer(file1)
    str1 = [args.cmd,args.list] 
    str2,dict1 =  server.start_key(str1)
    print (str2)
    if dict1 != {}:
        cc1 = CopyClip(sleep)
        cc1.copy2clip(dict1['key'],'password',dict1['password'])
        cc1.copy2clip(dict1['key'],'username',dict1['username'])
    

