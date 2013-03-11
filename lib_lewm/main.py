#!/usr/bin/python
from lib_lewm.common import   opendb
from lib_lewm.keepass import Keepass
from lib_lewm.export_db import ExportDb
from optparse import OptionParser
import sys
    
def main(filename):
    parser = OptionParser()
    parser.add_option("-e", "--export", action="store_true", dest="export",
                      help="export keyfile", default=False)
    parser.add_option("-l", "--list", action="store_true", dest="list",
                      help="list username", default=False)
    (options, args) = parser.parse_args()
    islist = False
    if options.export:
        if len(args) != 1 :
            print('no key')
            sys.exit()
        db,sleep1=opendb(filename)
        if type(db) == type({}):
            sys.exit()
        exp1 = ExportDb(db)
        exp1.start(args[0])
        sys.exit()
    elif options.list:
        islist = True
    if len(args) == 0 :
        tmp=''
    else:
        tmp=args[0]
    db,sleep1=opendb(filename)
    Keepass(db,sleep1,islist).start(tmp)

if __name__ == '__main__':
    main()
