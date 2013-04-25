#!/usr/bin/python
import pickle
import socket
from common import port

# Connect to the server:
client = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
client.connect ( ( 'localhost', port ) )
client.settimeout(5)


# Send some messages:
str1 = 'a' 
client.send ( str1.encode('utf-8'))
print (pickle.loads ( client.recv ( 1024 ) ))

# Retrieve and unpickle the list object:

# Close the connection
client.close()

