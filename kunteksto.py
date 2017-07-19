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
@click.option('--mode', '-m', type=click.Choice(['all', 'editdb', 'generate']),help="See the documentation. If you don't know then use: all", prompt=True)
@click.option('--infile', '-i', help='Full path and filename of the input CSV file.', prompt=True)
@click.option('--outdir', '-o', help='Full path to the output directory for writing the database and other files. Overrides the config file default value.')
@click.option('--delim', '-d', type=click.Choice([',', ';', ':', '|', '$']), help=' Overrides the config file default value.')
@click.option('--analyzelevel', '-a', type=click.Choice(['simple', 'full']), help=' Overrides the config file default value.')
def kunteksto(mode, infile, outdir, delim, analyzelevel):
    
    # Setup config info
    config = configparser.ConfigParser()
    config.read('kunteksto.conf')
    
    if not delim:
        delim = config['KUNTEKSTO']['delim']
    if not analyzelevel:
        analyzelevel = config['KUNTEKSTO']['analyzelevel']
    
    if outdir is None:
        if config['KUNTEKSTO']['outdir'].lower() in ['output', 'none']:
            outdir = os.getcwd() + os.path.sep + config['KUNTEKSTO']['outdir']
        else:
            print("You must supply a writable output directory.")
            exit(code=1)

    if not infile:
        print("You must supply a readable CSV input file.")
        exit(code=1)

    if not mode:
        click.echo("You must supply a mode.")
        exit(code=1)
        
    elif mode == 'all':
        outDB = analyze(infile, delim, analyzelevel, outdir)
        run([config['SQLITEBROWSER']['cmd'],  outDB])
        modelName = makeModel(outDB, outdir)
        datagen(modelName, outDB, infile, delim, outdir, config)

    elif mode == 'generate':
        print("This will generate a new model and data from an existing DB. Not yet implemented.")
        
    elif mode == 'editdb':
        dname, fname = os.path.split(infile)
        dbName = fname[:fname.index('.')] + '.db'
        db_file = outdir + os.path.sep + dbName
        run([config['SQLITEBROWSER']['cmd'],  db_file])
                
    exit(code=0)

def datagen(modelName, outDB, infile, delim, outdir, config):
    # open a connection to the RDF store if one is defined and RDF is to be generated.  
    if config['KUNTEKSTO']['rdf']:
        if config['ALLEGROGRAPH']['status'].upper() == "ACTIVE":
            try:
                from franz.openrdf.connect import ag_connect
                connRDF = ag_connect(config['ALLEGROGRAPH']['repo'], host=config['ALLEGROGRAPH']['host'], port=config['ALLEGROGRAPH']['port'],  user=config['ALLEGROGRAPH']['user'], password=config['ALLEGROGRAPH']['pw'])
            except:
                connRDF = None
                print('RDF Connection Error', 'Could not create connection to Allegrograph.')
        else:
            connRDF = None

    # open a connection to the XML DB if one is defined and XML is to be generated.
    if config['KUNTEKSTO']['xml']:
        if config['BASEX']['status'].upper() == "ACTIVE":
            try:
                import BaseXClient
                connXML = BaseXClient.Session(config['BASEX']['host'], int(config['BASEX']['port']), config['BASEX']['user'], config['BASEX']['pw'])
                connXML.execute("create db " + config['BASEX']['dbname'])
            except:
                connXML = None
                print('XML Connection Error', 'Could not create connection to BaseX.')
        else:
            connXML = None

    # open a connection to the JSON DB if one is defined and JSON is to be generated.      
    if config['KUNTEKSTO']['json']:
        if config['MONGODB']['status'].upper() == "ACTIVE":
            try:
                from pymongo import MongoClient
                # default MongoDB has no authentication requirements.
                client = MongoClient(config['MONGODB']['host'], int(config['MONGODB']['port']))
                connJSON = client[config['MONGODB']['dbname']]
            except:
                connJSON = None
                print('JSON Connection Error', 'Could not create connection to MongoDB.')
        else:
            connJSON = None

    # generate the data
    if modelName:
        makeData(modelName, outDB, infile,  delim, outdir, connRDF, connXML, connJSON)

        if connRDF:
            connRDF.close()
        if connXML:
            connXML.close()
        print('Data Generation', 'Completed.')

    else:
        print('Procedure Error', 'Missing model DB or no selected output directory.')

    return


if __name__ == '__main__':
    os.environ['XML_CATALOG_FILES'] = 'Kunteksto_catalog.xml'
    print('\n Kunteksto is running ...\n\n')
    kunteksto()
    