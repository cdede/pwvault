import argparse
from lib_lewm.server import PassServer
from lib_lewm.daemon import Daemon

def arg_parse():
    "Parse the command line arguments"
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd', default=None,
                        help='Daemon command: start|stop|restart', type=str)
    parser.add_argument('-f','--filename', help='conf filename'
            , default='')
    return parser.parse_args()

def main():
    args = arg_parse()
    pidfile = '/tmp/server.pid'
    if args.filename == '':
        filename = '~/.config/lewm/config'
    else:
        filename = args.filename
    if args.cmd == 'start':
        server = PassServer(pidfile,filename)
        server.start()
    elif args.cmd == 'stop':
        daemon = Daemon(pidfile)
        daemon.stop()
    elif args.cmd == '1':
        server = PassServer(pidfile)
        a= server.start_key(['as',True])
        print (a)

