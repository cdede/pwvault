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
            a = pickle.loads(a)
            logging.info (a)
            if a == 'CLOSE':
                channel.close()
                logging.info ('Closed connection:', details [ 0 ])
            else:
                m = self.start_key(a)
                msg = pickle.dumps(m) 
                logging.info('Send a message %s'%str(m))
                channel.send ( msg)

    def start_key(self,key):
        return 's'

#class PassServer():
class PassServer(Server):
    def __init__(self, pidfile):
        super(PassServer, self).__init__(pidfile)
        self._exp = {'Internet_e': {'url': 'e', 'username': 'e', 'comment': '', 'password': 'e'}, 'Internet_a_c': {'url': 'c', 'username': 'c', 'comment': '', 'password': 'c'}}

    def fill_ls(self):
        self._loc_ls=[]
        for i,e in self._exp.items():
            self._loc_ls.append( i)
        self._loc_ls.sort()

    def ls_to_cat(self, key):
        self._loc_cat=[]
        for i in self._loc_ls :
            if key in i :
                self._loc_cat.append(i)

    def cat(self):
        str1 = ''
        dict1 = {}
        if len(self._loc_cat) == 1:
            person = self._loc_cat[0]
            tmp1 = self._exp[person]
            str1 += 'comment :  %s\n' % tmp1['comment'] 
            str1 += 'url :  %s\n' % tmp1['url']
            dict1['key']=person
            dict1['password']=tmp1['password']
            dict1['username']=tmp1['username']
        elif len(self._loc_cat) > 1:
            for i in self._loc_cat:
                if self.islist:
                    tmp1 = self._exp[i]
                    str1 += i+tmp1['username'] + "\n"
                else:
                    str1 += i + "\n"
        else:
            str1 += 'no term' + "\n"
        return str1,dict1


    def start_key(self,msg):
        key,islist = msg
        self.islist = islist
        logging.info ("key : %s" % key)
        self.fill_ls()
        self.ls_to_cat(key)
        asd = self.cat()
        return asd


def main():
    args = arg_parse()
    pidfile = '/tmp/server.pid'
    if args.cmd == 'start':
        server = PassServer(pidfile)
        server.start()
    elif args.cmd == 'stop':
        daemon = Daemon(pidfile)
        daemon.stop()
    elif args.cmd == '1':
        server = PassServer(pidfile)
        a= server.start_key(['a',True])
        print (a)
if __name__ == '__main__':
    main()
