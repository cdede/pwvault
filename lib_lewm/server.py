#!/usr/bin/python
import logging
import pickle
import argparse
import socket
import threading
from common import port
from daemon import Daemon
from export_db import ExportDb
from common import   opendb
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

    def run ( self ):
        server = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
        server.bind ( ( '', port ) )
        server.listen ( 5 )
        while self.running:
            channel, details = server.accept()
            logging.info ('Received connection:', details [ 0 ])
            channel.settimeout(5)
            a = channel.recv ( 1024 )
            logging.info (a)
            if a == b'':
                channel.close()
                logging.info ('Closed connection:', details [ 0 ])
            else:
                m = self.start_key(a)
                msg = pickle.dumps(m) 
                logging.info('Send a message %s'%m)
                channel.send ( msg)

    def start_key(self,key):
        return 'sssssss'

class PassServer(Server):
    def __init__(self, pidfile):
        super(PassServer, self).__init__(pidfile)
        db,sleep1=opendb('../config','a')
        exp1 = ExportDb(db)
        self._exp = exp1._exp

        # fill_ls
        self._loc_ls=[]
        for i,e in self._exp.items():
            self._loc_ls.append( i)
        self._loc_ls.sort()

    def _ls_to_cat(self, key):
        self._loc_cat=[]
        for i in self._loc_ls :
            if key in i :
                self._loc_cat.append(i)

    def cat(self):
        str1 = 'do cat'
        if len(self._loc_cat) == 1:
            person = self._loc_cat[0]
            tmp1 = self._exp[person]
            #print('comment :  ',tmp1['comment'])
            #print('url :  ',tmp1['url'])
            #self.copy2clip(person,'password',tmp1['password'])
            #self.copy2clip(person,'username',tmp1['username'])
        elif len(self._loc_cat) > 1:
            for i in self._loc_cat:
                if self.islist:
                    tmp1 = self._exp[i]
                    print(i,tmp1['username'])
                else:
                    print(i)
        else:
            print('no term')
        return str1


    def start_key(self,key):
        self._ls_to_cat(key)
        logging.info(self.cat())
        return self.cat()


def main():
    args = arg_parse()
    pidfile = '/tmp/server.pid'
    if args.cmd == 'start':
        server = PassServer(pidfile)
        server.start()
    elif args.cmd == 'stop':
        daemon = Daemon(pidfile)
        daemon.stop()
if __name__ == '__main__':
    main()
