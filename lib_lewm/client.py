import pickle
import socket
from lib_lewm.common import port
from lib_lewm.copy_clip import   CopyClip
import argparse

def arg_parse():
    "Parse the command line arguments"
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd', default=None,
                        help='...(cmd)...', type=str)
    parser.add_argument('-l','--list', action='store_true',default=False, dest='list',
                        help='list username' )
    return parser.parse_args()


def main(a):
    args = arg_parse()
    str1 = [args.cmd,args.list] 
    get_item(str1)

def get_item(str1):
    # Connect to the server:
    client = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
    client.connect ( ( 'localhost', port ) )
    client.settimeout(5)
    
    
    # Send some messages:
    client.send ( pickle.dumps(str1))
    str2,dict1 = pickle.loads ( client.recv ( 1024 ) )
    print (str2)
    if dict1 != {}:
        cc1 = CopyClip(5)
        cc1.copy2clip(dict1['key'],'password',dict1['password'])
        cc1.copy2clip(dict1['key'],'username',dict1['username'])
    
    
    # Retrieve and unpickle the list object:
    
    # Close the connection
    client.close()

