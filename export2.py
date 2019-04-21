#!/usr/bin/python3

import socket 
import sqlite3


def execute():
    """
    Manage command passed from sn0int
    """
    
    print("[ * ] Executing command [ json ]")
    c = connect(".data/sn0int/test.db")
        
    
def connect(db):
    """
    Connect to the sqlite database
    """
    
    print("[ * ] Connecting to database [ %s ]" % db)
    return sqlite3.connect(db).cursor()
    
    
if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", 5555))
    
    sock.listen(5)
    
    connection = None
    while True:
        connection, address = sock.accept()
        received_message = connection.recv(300)
        if received_message.decode('ascii'):
            print(received_message.decode('ascii'))
            execute()
            
    connection.close()
    sock.close()
    
    
    