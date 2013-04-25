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

    def __init__ ( self,channel,details):
        self.running = 1

        self.channel = channel
        self.details = details

        self.thread1 = threading.Thread( target= self.run )
        self.thread1.start()

    def run ( self ):

        while self.running:
            print ('Received connection:', self.details [ 0 ])
            self.channel.send ( pickledList )
            for x in range ( 10 ):
                a = self.channel.recv ( 1024 )
                print (a)
            self.channel.close()
            #if a == 'stop':
            #    self.running = 0
            print ('Closed connection:', self.details [ 0 ])

def main():
    server = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
    server.bind ( ( '', port ) )
    server.listen ( 5 )
    channel, details = server.accept()
    ClientThread(channel,details)
if __name__ == '__main__':
    main()
