"""
Main entry point for the Kunteksto application.
"""
import sys
import os
from subprocess import run
import click
import configparser

from analyze import analyze
from generate import makeModel, makeData

@click.command()
@click.option('--mode', type=click.Choice(['analyze', 'genmodel', 'gendata', 'editdb', 'all']))
@click.option('--infile', help='Full path and filename of the input CSV file.')
@click.option('--outdir', help='Full path to the output directory for writing the database and other files.')
def kunteksto(mode, infile, outdir):
    
    # Setup config info
    config = configparser.ConfigParser()
    config.read('kunteksto.conf')
    sqlbrow = config['SQLITEBROWSER']['path']
    # get the RDF Store parameters.
    agraphStatus = config['ALLEGROGRAPH']['status']
    agraphHost = config['ALLEGROGRAPH']['host']
    agraphPort = config['ALLEGROGRAPH']['port']
    agraphRepo = config['ALLEGROGRAPH']['repo']
    agraphUser = config['ALLEGROGRAPH']['user']
    agraphPW = config['ALLEGROGRAPH']['pw']

    stardogStatus = config['STARDOG']['status']

    blazegraphStatus = config['BLAZEGRAPH']['status']

    graphdbStatus = config['GRAPHDB']['status']

    # get the XML DB parameters.
    basexStatus = config['BASEX']['status']
    basexHost = config['BASEX']['host']
    basexPort = config['BASEX']['port']
    basexDBName = config['BASEX']['dbname']
    basexUser = config['BASEX']['user']
    basexPW = config['BASEX']['pw']

    exisdbStatus = config['EXISTDB']['status']

    # get the JSON DB parameters.
    mongoStatus = config['MONGODB']['status']
    mongoHost = config['MONGODB']['host']
    mongoPort = config['MONGODB']['port']
    mongoDBName = config['MONGODB']['dbname']
    mongoUser = config['MONGODB']['user']
    mongoPW = config['MONGODB']['pw']

    couchStatus = config['COUCHDB']['status']

    genXML = config['KUNTEKSTO']['xml']
    genRDF = config['KUNTEKSTO']['rdf']
    genJSON = config['KUNTEKSTO']['json']

    analyzeLevel = config['KUNTEKSTO']['analyzeLevel']
    outdir = os.getcwd() + '/output/'
    sep_type = config['KUNTEKSTO']['sepType']
    version = config['KUNTEKSTO']['version']

    if not infile:
        print("You must supply a readable CSV input file.")
        exit(code=1)

    if not outdir:
        print("You must supply a writable output directory.")
        exit(code=1)

    if not mode:
        print("You must supply a mode.")
        exit(code=1)
    elif mode == 'analyze':
        doanalyze(infile, outdir, config)
        
    return

def doanalyze(infile, outdir, config):
    if infile:
        outDB = analyze(infile, config['KUNTEKSTO']['sepType'], config['KUNTEKSTO']['analyzeLevel'], outdir)
        if outDB:
            print('Created: ' + outDB)
            run([config['SQLITEBROWSER']['path'],  outDB])
        else:
            print("There was an error creating a database in " + outdir)
    return

def modelgen():
    # generate the model
    if outDB and not outdir == '(none selected)':
        modelName = makeModel(outDB, outdir)
        if modelName:
            model = modelName
    else:
        print("Missing model or directory.")
    
    return

def datagen():
    # open a connection to the RDF store if one is defined.
    if genRDF:
        if agraphStatus == "ACTIVE":
            try:
                from franz.openrdf.connect import ag_connect
                connRDF = ag_connect(agraphRepo, host=agraphHost,
                                     port=agraphPort,  user=agraphUser, password=agraphPW)
            except:
                connRDF = None
                print(
                    'RDF Connection Error', 'Could not create connection to Allegrograph.')

        else:
            connRDF = None

    # open a connection to the XML DB if one is defined.
    if genXML:
        if basexStatus == "ACTIVE":
            try:
                import BaseXClient
                connXML = BaseXClient.Session(basexHost, int(
                    basexPort), basexUser, basexPW)
                connXML.execute("create db " + basexDBName)
            except:
                connXML = None
                print(
                    'XML Connection Error', 'Could not create connection to BaseX.')

        else:
            connXML = None

    # open a connection to the JSON DB if one is defined.
    if genJSON:
        if mongoStatus == "ACTIVE":
            try:
                from pymongo import MongoClient
                # default MongoDB has no authentication requirements.
                client = MongoClient(mongoHost, int(mongoPort))
                connJSON = client[mongoDBName]
            except:
                connJSON = None
                print(
                    'JSON Connection Error', 'Could not create connection to MongoDB.')

        else:
            connJSON = None

    # generate the data
    if model and not outdir == '(none selected)':
        makeData(model, outDB, infile,
                 sep_type, outdir, connRDF, connXML, connJSON)

        if connRDF:
            connRDF.close()
        if connXML:
            connXML.close()
        print('Data Generation', 'Completed.')

    else:
        print(
            'Procedure Error', 'Missing model DB or no selected output directory.')

    return


if __name__ == '__main__':
    os.environ['XML_CATALOG_FILES'] = 'Kunteksto_catalog.xml'
    print('\n Kunteksto is running ...\n\n')
    kunteksto()
    
    print('\n Kunteksto exiting ...\n\n')
    exit()
