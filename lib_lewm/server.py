#!/usr/bin/python
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
        Daemon.__init__(self, pidfile)
        self.running = 1
        server = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
        server.bind ( ( '', port ) )
        server.listen ( 5 )
        self.server = server
        self.restart()

    def restart(self):
        self.channel, self.details = self.server.accept()

    def run ( self ):

        while self.running:
            print ('Received connection:', self.details [ 0 ])
            a = self.channel.recv ( 1024 )
            print (a)
            if a == b'':
                self.channel.close()
                print ('Closed connection:', self.details [ 0 ])
                self.restart()
            else:
                m = int(a) *2
                self.channel.send ( pickle.dumps(m) )
 
def main():
    args = arg_parse()
    pidfile = '/tmp/server.pid'
    if args.cmd == 'start':
        server = Server(pidfile)
        server.start()
    elif args.cmd == 'stop':
        daemon = Daemon(pidfile)
        daemon.stop()
if __name__ == '__main__':
    main()
