#!/usr/bin/python3

import sys
import socket 
import argparse     
import sqlite3
import json
import csv
from enum import Enum

class Domain:
    """
    Domain Class
    """
    
    def __init__(self, id, name, unscoped):
        self.id = id
        self.name = name
        self.unscoped = unscoped
        self.subdomains = list()
        
    def addSubDomain(self, subdomain):
        self.subdomains.append(subdomain)
        
    def toJSON(self):
        return {"id": self.id, "name": self.name, "unscoped": self.unscoped, "subdomains": self.subdomains}
        
        
class Subdomain:
    """
    Subdomain Class
    """
    
    def __init__(self, id, name, unscoped, resolvable):
        self.id = id
        self.name = name
        self.unscoped = unscoped
        self.resolvable = resolvable
        
    def toJSON(self):
        return {"id": self.id, "name": self.name, "unscoped": self.unscoped, "resolvable": self.resolvable}
        

class Command(Enum):
    """
    Command Enum Class
    """
    
    PARSE_JSON = "JSON"
    PARSE_CSV = "CSV"

def execute(args, command):
    """
    Manage command passed from sn0int
    """
    
    print("[ * ] Executing command [ %s ]" % command.upper())
    c = connect(".data/sn0int/%s.db" % args.workspace.lower())
    dump = extract(c)
    export(command, dump)
        
    
def connect(db):
    """
    Connect to the sqlite database
    """
    
    print("[ * ] Connecting to database [ %s ]" % db)
    return sqlite3.connect(db).cursor()
    
    
def extract(conn):
    """
    Extract data from default.db sqlite file
    """
    
    print("[ * ] Extracting Information")
    
    results = dict()
    results['data'] = list()
    
    domains = conn.execute("SELECT * FROM domains")
    for domain in domains:
        d = Domain(domain[0], domain[1], domain[2])
        
        subdomains = conn.execute("SELECT * FROM subdomains WHERE domain_id = %d" % domain[0])
        
        for subdomain in subdomains:
            s = Subdomain(subdomain[0], subdomain[2], subdomain[3], subdomain[4])            
            d.addSubDomain(s.toJSON())
            
        results['data'].append(d.toJSON())    
        
    return results
    
    
def export(command, dump):
    """
    Export CSV or JSON file
    """
    
    print("[ * ] Exporting data to file")
        
    FILE_NAME = "output"
    
    if command.upper() == Command.PARSE_JSON.value:
        with open(FILE_NAME+".json", 'w') as f:
               json.dump(dump, f, indent=4, sort_keys=True)

    if command.upper() == Command.PARSE_CSV.value:
        with open(FILE_NAME+".csv", 'w') as f:
            output = csv.writer(f)
            output.writerow(dump['data'][0].keys())
            for domain in dump['data']:
                struct = dict()
                struct = domain.copy()
                struct['subdomains'] = list()
            
                for subdomain in domain['subdomains']:
                    struct['subdomains'].append(subdomain['name'])   
                
                output.writerow(struct.values())
       
  
def listen(args):
    """
    Initiate a socket and listen for incoming connections and commands
    """
    
    s = socket.socket()          
    print("[ * ] Creating Socket")
    s.bind(('', args.port))         
    print("[ * ] Binding Socket [ %s ]" % args.port)
    s.listen(5)  
    print("[ * ] Listening")              
    while True: 
       c, addr = s.accept()      
       print("[ + ] Connection [ %s:%s ]" % (str(addr[0]), str(addr[1])))
       
       data = c.recv(1024)
       if data.decode('ascii'):
           execute(args, data.decode('ascii'))
       
       # Close the connection with the client 
       # c.close()
   
   
if __name__ == '__main__':
    """
    Main run
    """
    
    parser = argparse.ArgumentParser()
    parser.add_argument("port", help="Port number to run the socket on", type=int)
    parser.add_argument("workspace", help="Name of workspace", type=str)
    args = parser.parse_args()
    
    if(args.port):
        listen(args)