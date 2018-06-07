"""
MarkLogic 9 REST connection setup.
Uses the information from the kunteksto.conf 
Creates the Forest, Database and REST API Port 
"""
import os
import sys
import configparser
import requests
from requests.auth import HTTPDigestAuth

dirpath = os.getcwd()
curdir = os.path.basename(dirpath)

print("\nThe current directory name is : " + curdir)

if curdir != 'kunteksto':
    print("ERROR: You are not in the kunteksto directory. Change to the 'kunteksto' directory and run 'utils/db_setup.py'\n")
    raise SystemExit
    
config = configparser.ConfigParser()
config.read('kunteksto.conf')
print("\nDatabase setup for Kunteksto version: " + config['SYSTEM']['version'] + " using S3Model RM: " + config['SYSTEM']['rmversion'] + "\n")

if not config['MARKLOGIC']['status'].upper() == "ACTIVE":
    print("\nThe MarkLogic option is INACTIVE. Nothing to do.\n\n")
    sys.exit(0)

xmloption = True if config['MARKLOGIC']['loadxml'].upper() == "TRUE" else False
rdfoption = True if config['MARKLOGIC']['loadrdf'].upper() == "TRUE" else False
jsonoption = True if config['MARKLOGIC']['loadjson'].upper() == "TRUE" else False

if not xmloption and not rdfoption and not jsonoption:
    print("\nNone of the MarkLogic options are active. Nothing to do.\n\n")
    sys.exit(0)

print("\nPreparing to setup MarkLogic 9.\n")

dbname = config['MARKLOGIC']['dbname']
host = config['MARKLOGIC']['host']
port = config['MARKLOGIC']['port']
user = config['MARKLOGIC']['user']
pw = config['MARKLOGIC']['password']

# Attempt to create the DB
"""
curl -X POST  --anyauth -u admin:admin --header "Content-Type:application/json" \

  -d '{"database-name":"MyNewDatabase"}' http://localhost:8002/manage/v2/databases

"""
r = requests.get('http://' + host + ':8002', auth=HTTPDigestAuth(user, pw))
print(r.url)
print("STATUS: ", r.status_code)

if r.status_code != 200:
    print("\nCannot contact ML9 management at " + host +':8002')
    print("\nCheck your settings and your ML9 system.")
    sys.exit(-1)
    
if xmloption:    
    pass
else:
    print("\nThe MarkLogic XML option is INACTIVE.\n")

if rdfoption:    
    pass
else:
    print("\nThe MarkLogic RDF option is INACTIVE.\n")

if jsonoption:    
    pass
else:
    print("\nThe MarkLogic JSON option is INACTIVE.\n")

    
    