"""
An example of connecting to a Neo4j server directly.
Another option to explore is to use the  TinkerPop project to connect to multiple DBs (graph and/or RDF).
Also, Stardog is a combination Graph and RDF store option. 
"""
import configparser

from pprint import pprint

from py2neo import Graph, Node, Relationship, authenticate


# Setup config info
config = configparser.ConfigParser()
config.read('kunteksto.conf')

authenticate(config['NEO4J']['host'] + ':' + config['NEO4J']['port'],config['NEO4J']['user'], config['NEO4J']['pw'] )

url = 'http://'+ config['NEO4J']['host'] + ':' + config['NEO4J']['port'] + config['NEO4J']['dbpath']
graph_db = Graph(url)


def insert_data():
    die_hard = graph_db.create(
        Node("Person",name = "Bruce Willis"),
        Node("Person",name = "John McClane"),
        Node("Person",name = "Alan Rickman"),
        Node("Person",name = "Hans Gruber"),
        Node("Person",name = "Nakatomi Plaza"),)
    pprint(die_hard)

insert_data()
