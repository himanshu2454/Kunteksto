"""
Models for Kunteksto.
"""
import os.path

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy_utils import ChoiceType

from . import app

db = SQLAlchemy(app)

# Create models
class XMLstore(db.Model):
    """
    Define XML data storage locations.
    """
    __tablename__ = 'xmlstore'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('Storage Name', db.String(250), unique=True, nullable=False)
    host = db.Column('Host Name', db.String(500), unique=True, nullable=False)
    port = db.Column('Port Number', db.String(10), unique=False, nullable=False)
    hostip = db.Column('Host IP', db.String(45), unique=False, nullable=True)
    forests = db.Column('Forests', db.Integer, unique=False, nullable=True)
    dbname = db.Column('Database Name', db.String(250), unique=False, nullable=False)
    user = db.Column('User Name', db.String(250), unique=False, nullable=True)
    pw = db.Column('User Password', db.String(250), unique=False, nullable=True)
    models = db.relationship('Datamodel', backref='xmlstore', lazy=True)
    
    def __repr__(self):
        return self.name.strip()

class JSONstore(db.Model):
    """
    Define JSON data storage locations.
    """
    __tablename__ = 'jsonstore'
   
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('Storage Name', db.String(250), unique=True, nullable=False)
    host = db.Column('Host Name', db.String(500), unique=True, nullable=False)
    port = db.Column('Port Number', db.String(10), unique=False, nullable=False)
    hostip = db.Column('Host IP', db.String(45), unique=False, nullable=True)
    forests = db.Column('Forests', db.Integer, unique=False, nullable=True)
    dbname = db.Column('Database Name', db.String(250), unique=False, nullable=False)
    user = db.Column('User Name', db.String(250), unique=False, nullable=True)
    pw = db.Column('User Password', db.String(250), unique=False, nullable=True)
    models = db.relationship('Datamodel', backref='jsonstore', lazy=True)
    
    def __repr__(self):
        return self.name.strip()

class RDFstore(db.Model):
    """
    Define RDF data storage locations.
    """
    __tablename__ = 'rdfstore'
   
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('Storage Name', db.String(250), unique=True, nullable=False)
    host = db.Column('Host Name', db.String(500), unique=True, nullable=False)
    port = db.Column('Port Number', db.String(10), unique=False, nullable=False)
    hostip = db.Column('Host IP', db.String(45), unique=False, nullable=True)
    forests = db.Column('Forests', db.Integer, unique=False, nullable=True)
    dbname = db.Column('Database Name', db.String(250), unique=False, nullable=False)
    user = db.Column('User Name', db.String(250), unique=False, nullable=True)
    pw = db.Column('User Password', db.String(250), unique=False, nullable=True)
    models = db.relationship('Datamodel', backref='rdfstore', lazy=True)
    
    def __repr__(self):
        return self.name.strip()

class Datamodel(db.Model):
    """
    The Datamodel model provides a location to store the model information and metadata about the model.
    
    
    [NAMESPACES]
    any additional namespaces must be defined with their abbreviations. 
    {abbrev}:{namespace URI}
    Example:  dul: http://www.ontologydesignpatterns.org/ont/dul/DUL.owl# 

    """
    __tablename__ = 'datamodel'
    
    id = db.Column(db.Integer, primary_key=True)
    project = db.Column('Project', db.String(50), unique=True, nullable=False)
    title = db.Column('Title', db.String(250), unique=True, nullable=False)
    description = db.Column('Description', db.Text, unique=False, nullable=False)
    copyright = db.Column('Copyright', db.String(250), unique=False, nullable=True)
    author = db.Column('Author', db.String(250), unique=False, nullable=False)
    definition_url = db.Column('Defining URL', db.String(500), unique=False, nullable=False)
    namespaces = db.Column('Additional Namespaces', db.Text, unique=False, nullable=True)
    xml_store = db.Column(db.Integer, db.ForeignKey('xmlstore.id'), nullable=True)
    rdf_store = db.Column(db.Integer, db.ForeignKey('rdfstore.id'), nullable=True)
    json_store = db.Column(db.Integer, db.ForeignKey('jsonstore.id'), nullable=True)
    dmid = db.Column('Data Model ID', db.String(40), unique=True, nullable=False)
    dataid = db.Column('Data Cluster ID', db.String(40), unique=True, nullable=False)
    schema = db.Column('XML Schema', db.Text, unique=False, nullable=True)
    rdf = db.Column('RDF', db.Text, unique=False, nullable=True)
    catalog = db.Column('XML Catalog', db.Text, unique=False, nullable=True)
    components = db.relationship('Component', backref='datamodel', lazy=True)

    def __repr__(self):
        return '<Data Model: %r>' % self.title.strip()


class Component(db.Model):
    """
    The Component model provides a location to store the datatype and metadata information about each column in the CSV.
    """
    __tablename__ = 'component'
    
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('datamodel.id'))
    header = db.Column('CSV Column Header', db.String(100), unique=False, nullable=False)
    label = db.Column('Label Value', db.String(250), unique=False, nullable=False)
    datatype = db.Column('Datatype', db.String(10), unique=False, nullable=False)
    min_len = db.Column('Minimum Length', db.Integer, nullable=True)
    max_len = db.Column('Maximum Length', db.Integer, nullable=True)
    choices = db.Column('String Enumerations', db.Text, unique=False, nullable=True)
    regex = db.Column('Regular Expression', db.String(100), unique=False, nullable=True)
    min_incl = db.Column('Minimum Value (Inclusive)', db.String(100), unique=False, nullable=True)
    max_incl = db.Column('Maximum Value (Inclusive)', db.String(100), unique=False, nullable=True)
    min_excl = db.Column('Minimum Value (Exclusive)', db.String(100), unique=False, nullable=True)
    max_excl = db.Column('Maximum Value (Exclusive)', db.String(100), unique=False, nullable=True)
    description = db.Column('Description', db.Text, unique=False, nullable=False)
    definition_url = db.Column('Defining URL', db.String(500), unique=False, nullable=False)
    pred_obj = db.Column('List of predicate/object pairs', db.Text, unique=False, nullable=True)
    def_text = db.Column('Default Text', db.String(500), unique=False, nullable=True)
    def_num = db.Column('Default Number', db.String(100), unique=False, nullable=True)
    units = db.Column('Units', db.String(50), unique=False, nullable=True)
    mcid = db.Column('Component ID', db.String(40), unique=True, nullable=False)
    adid = db.Column('Adapter ID', db.String(40), unique=True, nullable=False)
    model_link = db.relationship("Datamodel", back_populates="components")

    def __repr__(self):
        return '<Component: %r>' % self.label.strip()



# Create DB
db.create_all()
db.session.commit()
# Database connection
engine = create_engine('sqlite:///kunteksto.db', echo=False)
# Create a Session
Session = sessionmaker(bind=engine)
session = Session()

# Add default Datastore records (if they don't already exist) as an example 
try:
    outdir = os.path.abspath(os.path.join(os.getcwd(), os.pardir, 'output', 'xml'))
    ds = XMLstore(name='Filesystem (example)', host=outdir, port='N/A', dbname='XML')
    db.session.add(ds)
    db.session.commit()
except:
    pass

try:
    outdir = os.path.abspath(os.path.join(os.getcwd(), os.pardir, 'output', 'json'))
    ds = JSONstore(name='Filesystem (example)', host=outdir, port='N/A', dbname='JSON')
    db.session.add(ds)
    db.session.commit()
except:
    pass

try:
    outdir = os.path.abspath(os.path.join(os.getcwd(), os.pardir, 'output', 'rdf'))
    ds = RDFstore(name='Filesystem (example)', host=outdir, port='N/A', dbname='RDF')
    db.session.add(ds)
    db.session.commit()
except:
    pass

try:
    ds = RDFstore(name='ALLEGROGRAPH (example)', host='localhost', port='10035', dbname='Kunteksto', user='admin', pw='admin')
    db.session.add(ds)
    db.session.commit()
except:
    pass

try:
    ds = RDFstore(name='Marklogic (example)', host='localhost.localdomain', port='10035', dbname='Kunteksto', hostip='192.168.25.120', forests=2, user='admin', pw='admin')
    db.session.add(ds)
    db.session.commit()
except:
    pass

try:
    ds = XMLstore(name='Marklogic (example)', host='localhost.localdomain', port='10035', dbname='Kunteksto', hostip='192.168.25.120', forests=2, user='admin', pw='admin')
    db.session.add(ds)
    db.session.commit()
except:
    pass

try:
    ds = JSONstore(name='Marklogic (example)', host='localhost.localdomain', port='10035', dbname='Kunteksto', hostip='192.168.25.120', forests=2, user='admin', pw='admin')
    db.session.add(ds)
    db.session.commit()
except:
    pass


try:
    ds = XMLstore(name='BaseX (example)', host='localhost', port='1984', dbname='Kunteksto', user='admin', pw='admin')
    db.session.add(ds)
    db.session.commit()
except:
    pass
