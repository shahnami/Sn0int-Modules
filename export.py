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
    
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.subdomains = list()
    
    def setSubDomain(self, subdomains):
        self.subdomains = subdomains
        
    def addSubDomain(self, subdomain):
        self.subdomains.append(subdomain)
        
    def remove(self, subdomain):
        self.subdomains.remove(subdomain)
        
    def toJSON(self):
        return {"id": self.id, "name": self.name, "subdomains": self.subdomains}
        
        
class Subdomain:
    """
    Subdomain Class
    """
    
    def __init__(self, id, name, resolvable, asn):
        self.id = id
        self.name = name
        self.resolvable = resolvable
        self.ips = list()
        self.asn = asn
        
    def setIP(self, ips):
        self.ips = ips
        
    def addIP(self, ip):
        self.ips.append(ip)
        
    def toJSON(self):
        return {"id": self.id, "name": self.name, "resolvable": self.resolvable, "ips": self.ips, "asn": self.asn}
        

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
    
    # print("[ * ] Executing command [ %s ]" % command.upper())
    c = connect(".data/sn0int/%s.db" % args.workspace.lower())
    dump = extract(c)
    export(args, command, dump)
        
    
def connect(db):
    """
    Connect to the sqlite database
    """
    
    # print("[ * ] Connecting to database [ %s ]" % db)
    return sqlite3.connect(db).cursor()
    
    
def extract(conn):
    """
    Extract data from default.db sqlite file
    """
    
    # print("[ * ] Extracting Information")
    
    
    
    results = dict()
    results['data'] = list()
    
    all_in_one = conn.execute("SELECT domains.id, domains.value, subdomains.id, subdomains.value, subdomains.resolvable, ipaddrs.value, ipaddrs.asn, ipaddrs.as_org FROM domains LEFT JOIN subdomains ON domains.id = subdomains.domain_id  LEFT JOIN subdomain_ipaddrs ON subdomain_ipaddrs.subdomain_id = subdomains.id LEFT JOIN ipaddrs ON subdomain_ipaddrs.ip_addr_id = ipaddrs.id WHERE domains.unscoped = 0 AND subdomains.unscoped = 0 ORDER BY domains.id, subdomains.resolvable DESC")
    for row in all_in_one:
        domain = Domain(row[0], row[1])
        subdomain = Subdomain(row[2], row[3], row[4], {"id": row[6], "organisation": row[7]})
        
        for entry in results['data']:
            if entry['id'] == domain.id:
                domain.setSubDomain(entry['subdomains'])
                results['data'].remove(entry)
                
            for subentry in entry['subdomains']:
                if subentry['id'] == subdomain.id:
                    subdomain.setIP(subentry['ips'])
                    domain.remove(subentry)
                    
        subdomain.addIP(row[5])            
        domain.addSubDomain(subdomain.toJSON())
        results['data'].append(domain.toJSON())
        
    return results
    
    
def export(args, command, dump):
    """
    Export CSV or JSON file
    """
    
    # print("[ * ] Exporting data to file")
    
    if command.upper() == Command.PARSE_JSON.value:
        with open(args.filename+".json", 'w') as f:
               json.dump(dump, f, indent=4, sort_keys=True)

    if command.upper() == Command.PARSE_CSV.value:
        with open(args.filename+".csv", 'w') as f:
            output = csv.writer(f)
            output.writerow(dump['data'][0].keys())
            for domain in dump['data']:
                struct = dict()
                struct = domain.copy()
                struct['subdomains'] = list()
            
                for subdomain in domain['subdomains']:
                    struct['subdomains'].append(subdomain['name'])   
                
                output.writerow(struct.values())
       
def reconnect(args):
    """
    Due to bug in sn0int, we need to reinitialise the socket after every command
    """
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", args.port))
    
    sock.listen(5)
    return sock

def listen(args):
    """
    Listen for incoming commands
    """
    
    sock = reconnect(args)
    connection = None
    while True:
        connection, address = sock.accept()
        received_message = connection.recv(300)
        if received_message.decode('ascii'):
            execute(args, received_message.decode('ascii'))
            
    connection.close()
    sock.close()
   
if __name__ == '__main__':
    """
    Main run
    """
    
    parser = argparse.ArgumentParser()
    parser.add_argument("port", help="Port number to run the socket on", type=int)
    parser.add_argument("workspace", help="Name of workspace", type=str)
    parser.add_argument("filename", help="Name of outputfile", type=str)
    args = parser.parse_args()
    
    if(args.port):
        listen(args)
        