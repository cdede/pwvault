#!/usr/bin/python
import pickle
import socket
import threading
from common import port
# We'll pickle a list of numbers:
someList = [ 1, 2, 7, 9, 0 ]
pickledList = pickle.dumps ( someList )

# Our thread class:
class ClientThread ( threading.Thread ):

    def __init__ ( self):
        self.running = 1
        server = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
        server.bind ( ( '', port ) )
        server.listen ( 5 )
        self.server = server
        self.restart()
        self.thread1 = threading.Thread( target= self.run )
        self.thread1.start()

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
            #if a == 'stop':
            #    self.running = 0

    def restart(self):
        self.channel, self.details = self.server.accept()

def main():
    ClientThread()
if __name__ == '__main__':
    main()
