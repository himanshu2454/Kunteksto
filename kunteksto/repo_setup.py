# Setup Marklogic, AllegroGraph and BaseX
import os
import sys
import requests
import configparser
from requests.auth import HTTPDigestAuth

from . import config
from .models import db, Session, RDFstore, XMLstore, JSONstore


RMVERSION = config['SYSTEM']['rmversion'].replace('.', '_')
parentdir = os.path.dirname(os.getcwd())
dmlib = os.path.join(parentdir, 'dmlib')
rmdir = os.path.join(parentdir, 's3model')

def ag_init(repo_name):
    """
    Initialize and connect to an Allegrograph database.
    https://franz.com/agraph/support/documentation/6.4.0/python/index.html
    """
    repo_name = repo_name.strip()
    
    try:
        from franz.openrdf.connect import ag_connect
    except:
        print("\nCould not find the AllegroGraph client.\n")
        exit(1)
        
    session = Session()
    rec = session.query(RDFstore).filter_by(name=repo_name).first()
    
    if rec == None:
        print("\nCould not find a RDF repository named: " + repo_name)
        exit(1)
        
    print('Checking AllegroGraph connections.\n')
    # Set environment variables for AllegroGraph
    os.environ['AGRAPH_HOST'] = rec.host
    os.environ['AGRAPH_PORT'] = rec.port
    os.environ['AGRAPH_USER'] = rec.user
    os.environ['AGRAPH_PASSWORD'] = rec.pw

    try:
        with ag_connect(rec.dbname, host=os.environ.get('AGRAPH_HOST'), port=os.environ.get('AGRAPH_PORT'), user=os.environ.get('AGRAPH_USER'), password=os.environ.get('AGRAPH_PASSWORD')) as conn:
            conn.clear(contexts='ALL_CONTEXTS')
            print('Initial Kunteksto RDF Repository Size: ', conn.size(), '\n')
            print("Loading RM OWL and RDF.")
            conn.addFile(os.path.join(rmdir, 's3model.owl'), serverSide=True)
            conn.addFile(os.path.join(rmdir, 's3model_' + RMVERSION + '.rdf'), serverSide=True)
            print('Current Kunteksto RDF Repository Size: ', conn.size(), '\n')
            print('AllegroGraph connections are okay.\n')
            print("Remember to upload the Data Model RDF file(s) after exporting them.\n\n")
    except:
        print("Could not establish a connection to AllegroGraph. Check to see that the server is running and the RDF repository values are correct.\n\n")



def bx_init(repo_name):
    """
    Initialize and connect to an BaseX database.
    """
    
    try:
        from BaseXClient import BaseXClient
    except:
        print("Could not find the BaseXClient")
        exit(1)
        
    session = Session()
    rec = session.query(XMLstore).filter_by(name=repo_name).first()

    if rec == None:
        print("\nCould not find a XML repository named: " + repo_name)
        exit(1)

    # Setup BaseX
    # create session
    print('Checking BaseX connections.\n')
    try:
        conn = BaseXClient.Session(rec.host, int(rec.port), rec.user, rec.pw)
        # create new database
        conn.create(rec.dbname, "")
        print(conn.info())

        # run query on database
        print(conn.execute("xquery doc(" + rec.dbname + ")"))
    except:
        conn = None
        print("Could not establish a BaseX connection. Check to see that the server is running and the database values are correct.\n\n")

    finally:
        # close session
        if conn is not None:
            conn.close()
            print('BaseX connections are okay.\n\n')

def ml_init(repo_name):
    """
    Initialize and connect to a Marklogic database.
    """
    dbinfo = None
    session = Session()
    dbinfo = session.query(XMLstore).filter_by(name=repo_name).first()

    # Found out what repo name this is
    if dbinfo is not None:
        print("\nFound a XML repository named: " + repo_name)
    else:
        dbinfo = session.query(RDFstore).filter_by(name=repo_name).first()
        if dbinfo is not None:
            print("\nFound a RDF repository named: " + repo_name)

    if dbinfo == None:
        dbinfo = session.query(JSONstore).filter_by(name=repo_name).first()
        if dbinfo is not None:
            print("\nFound a JSON repository named: " + repo_name)
        else:
            print("\nCould not find a repository named: " + repo_name)
            sys.exit(0)

    print("\nPreparing to setup MarkLogic 9.\n")

    dbname = dbinfo.dbname
    hostip = dbinfo.hostip
    port = dbinfo.port
    asport = dbinfo.asport
    user = dbinfo.user
    pw = dbinfo.pw

    # Check if dbname exists already, if it does then clear it and reload the RM RDF & ontology
    headers = {"Content-Type": "application/json", 'user-agent': 'Kunteksto'}
    payload = {"format": 'json'}
    url = 'http://' + hostip + ':' + '8002' + '/manage/v2/databases/' + dbname
    print("Checking for " + url)
    r = requests.get(url, auth=HTTPDigestAuth(user, pw), headers=headers, json=payload)
    if r.status_code == 200:
        print(dbname + " already exists. Clearing the database at " + url)
        payload = {"operation": 'clear-database'}
        url = 'http://' + hostip + ':' + '8002' + '/manage/v2/databases/' + dbname
        r = requests.post(url, auth=HTTPDigestAuth(user, pw), headers=headers, json=payload)
    else:
        # Attempt to create the DB
        headers = {"Content-Type": "application/json", 'user-agent': 'Kunteksto'}
        payload = {"database-name": dbname}
        url = 'http://' + hostip + ':8002/manage/v2/databases'
        print("Checking for " + url)
        r = requests.post(url, auth=HTTPDigestAuth(user, pw), headers=headers, json=payload)
        print(r.status_code)
        if r.status_code != 201:
            print("\nCannot create the database " + dbname + " on http://" + hostip + ":8002/manage/v2/databases")
            print("\nCheck your settings and your ML9 system. Process aborted!")
            sys.exit(-1)
        else:
            print("Created Database " + dbname)

    # Attempt to create the Forests
    numforests = int(dbinfo.forests)
    hostname = dbinfo.host
    print("Creating " + str(numforests) + " forests.")
    for fid in range(0, numforests):
        print("Creating forest: " + str(fid))
        payload = {"forest-name": dbname + '-' + str(fid), "host": hostname, "database": dbname}
        r = requests.post('http://' + hostip + ':8002/manage/v2/forests', auth=HTTPDigestAuth(user, pw), headers=headers, json=payload)
        if r.status_code != 201:
            print(r.status_code)
            print("Cannot create the forest " + dbname + '-' + str(fid) + " for database " + dbname + " on host " + hostname)
            print("\nCheck your settings and your ML9 system. Process aborted!")
            sys.exit(-1)
        else:
            print("Created Forest " + dbname + '-' + str(fid))

    # Set up REST API
    payload = {
      "rest-api": {
        "name": "kunteksto-app-server-" + asport,
        "database": dbname,
        "modules-database": "kunteksto-modules",
        "port": asport,
        "xdbc-enabled": "true",
        "forests-per-host": numforests,
        "error-format": "json"
      }
    }

    r = requests.post('http://' + hostip + ':8002/LATEST/rest-apis', auth=HTTPDigestAuth(user, pw), headers=headers, json=payload)
    if r.status_code != 201:
        print("\nCannot create the REST API for " + dbname + " on http://" + hostip + ":" + asport)
        print("\nCheck your settings and your ML9 system or maybe it already exists.")
    else:
        print("Created REST API for " + dbname + " at http://" + hostip + ":" + asport)

    # Write the RM RDF and ontology to ML9
    with open(os.path.join('../s3model', 's3model.owl'), 'r') as owlfile:
        owlStr = owlfile.read()
        headers = {"Content-Type": "application/xml", 'user-agent': 'Kunteksto'}
        url = 'http://' + hostip + ':' + port + '/v1/documents?uri=/s3model/s3model.owl'
        r = requests.put(url, auth=HTTPDigestAuth(user, pw), headers=headers, data=owlStr)

    with open(os.path.join('../s3model', 's3model_3_1_0.rdf'), 'r') as rdffile:
        rdfStr = rdffile.read()
        headers = {"Content-Type": "application/xml", 'user-agent': 'Kunteksto'}
        url = 'http://' + hostip + ':' + port + '/v1/documents?uri=/s3model/s3model_3_1_0.rdf'
        r = requests.put(url, auth=HTTPDigestAuth(user, pw), headers=headers, data=rdfStr)

    print("\nDatabase Setup is finished.\n\n")
