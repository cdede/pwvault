#!/usr/bin/python
import pickle
import socket
from common import port
from copy_clip import   CopyClip

# Connect to the server:
client = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
client.connect ( ( 'localhost', port ) )
client.settimeout(5)


# Send some messages:
str1 = ['a',True] 
client.send ( pickle.dumps(str1))
str2,dict1 = pickle.loads ( client.recv ( 1024 ) )
if dict1 != {}:
    cc1 = CopyClip(5)
    cc1.copy2clip(dict1['key'],'password',dict1['password'])
    cc1.copy2clip(dict1['key'],'username',dict1['username'])


# Retrieve and unpickle the list object:

# Close the connection
client.close()

