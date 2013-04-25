#!/usr/bin/python
import logging
import pickle
import argparse
import socket
import threading
from common import port
from daemon import Daemon
# We'll pickle a list of numbers:
someList = [ 1, 2, 7, 9, 0 ]
pickledList = pickle.dumps ( someList )

def arg_parse():
    "Parse the command line arguments"
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd', default=None,
                        help='Daemon command: start|stop|restart', type=str)
    return parser.parse_args()
           #if a == 'stop':
            #    self.running = 0

class Server( Daemon):
    def __init__(self, pidfile):
        logfile = '/tmp/lewm.log'
        loglevel = logging.DEBUG
        logging.basicConfig(format='[%(levelname)s] in %(filename)s:'
                                   '%(funcName)s at %(asctime)s\n%(message)s',
                            level=loglevel, 
                            filename=logfile, 
                            filemode='a')
      
        Daemon.__init__(self, pidfile)
        self.running = 1
        server = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
        server.bind ( ( '', port ) )
        server.listen ( 5 )
        self.server = server

    def run ( self ):

        while self.running:
            self.channel, self.details = self.server.accept()
            logging.info ('Received connection:', self.details [ 0 ])
            self.channel.settimeout(5)
            a = self.channel.recv ( 1024 )
            logging.info (a)
            if a == b'':
                self.channel.close()
                logging.info ('Closed connection:', self.details [ 0 ])
            else:
                m = int(a) *2
                msg = pickle.dumps(m) 
                logging.info('Send a message %d'%m)
                self.channel.send ( msg)
 
def main():
    args = arg_parse()
    pidfile = '/tmp/server.pid'
    if args.cmd == 'start':
        server = Server(pidfile)
        logging.info ('start')
        server.start()
    elif args.cmd == 'stop':
        daemon = Daemon(pidfile)
        daemon.stop()
if __name__ == '__main__':
    main()
