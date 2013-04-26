import logging
import pickle
import socket
from lib_lewm.common import port,hash_str,hash_pass

from lib_lewm.daemon import Daemon

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

    def run ( self ):
        server = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
        server.bind ( ( '', port ) )
        server.listen ( 5 )
        while True:
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
                password_client  =a[0] 
                if hash_str(password_client) == hash_pass:
                    a = a[1:]
                    m = self.start_key(a)
                    msg = pickle.dumps(m) 
                    logging.info('Send a message %s'%str(m))
                    channel.send ( msg)

    def start_key(self,key):
        return 's'


