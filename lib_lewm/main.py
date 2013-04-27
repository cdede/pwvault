import argparse
from lib_lewm.common import gen_pass
from lib_lewm.copy_clip import   CopyClip
from lib_lewm.keepass import   PassServer
from lib_lewm.common import   opendb
import sys

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
    return parser.parse_args()

def main():
    args = arg_parse()
    if args.filename == '':
        filename = '~/.config/lewm/config'
    else:
        filename = args.filename
    if args.gpg:
        gen_pass(args.cmd)
        sys.exit()
    db,sleep=opendb(filename )
    sleep = int(sleep)
    server = PassServer(db)
    str1 = [args.cmd,args.list] 
    str2,dict1 =  server.start_key(str1)
    print (str2)
    if dict1 != {}:
        cc1 = CopyClip(5)
        cc1.copy2clip(dict1['key'],'password',dict1['password'])
        cc1.copy2clip(dict1['key'],'username',dict1['username'])
    

