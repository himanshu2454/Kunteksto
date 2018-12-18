import configparser

import click

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, form
from flask_admin.contrib.sqla import ModelView

# Setup config info based on the current working directory
config = configparser.ConfigParser()
config.read('../kunteksto.conf')
print("\n\nKunteksto version: " + config['SYSTEM']['version'] + " using S3Model RM: " + config['SYSTEM']['rmversion'] + "\n\n")


app = Flask(__name__)

# set optional bootswatch theme https://bootswatch.com/3/yeti/
app.config['FLASK_ADMIN_SWATCH'] = config['KUNTEKSTO']['theme']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kunteksto.db'

db = SQLAlchemy(app)

# Create models
class Datamodel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project = db.Column('Project', db.String(50), unique=True, nullable=False)
    title = db.Column('Title', db.String(250), unique=True, nullable=False)
    description = db.Column('Description', db.Text, unique=False, nullable=False)
    copyright = db.Column('Copyright', db.String(250), unique=False, nullable=True)
    author = db.Column('Author', db.String(250), unique=False, nullable=False)
    definition_url = db.Column('Defining URL', db.String(500), unique=False, nullable=False)
    dmid = db.Column('Data Model ID', db.String(40), unique=True, nullable=False)
    dataid = db.Column('Data Cluster ID', db.String(40), unique=True, nullable=False)
    components = db.relationship('Component', backref='datamodel', lazy=True)

    def __repr__(self):
        return '<Data Model: %r>' % self.title
    

class Component(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('datamodel.id'))
    model = db.relationship("Datamodel", back_populates="components")
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
    def_text = db.Column('Default Text', db.Text, unique=False, nullable=True)
    def_num = db.Column('Default Number', db.String(100), unique=False, nullable=True)
    units = db.Column('Units', db.String(50), unique=False, nullable=True)
    mcid = db.Column('Component ID', db.String(40), unique=True, nullable=False)
    adid = db.Column('Adapter ID', db.String(40), unique=True, nullable=False)

    def __repr__(self):
        return '<Component: %r>' % self.label


admin = Admin(app, name='Kunteksto', template_mode='bootstrap3')

# Add administrative views here

admin.add_view(ModelView(Datamodel, db.session))
admin.add_view(ModelView(Component, db.session))

# Create DB
db.create_all()


# Commandline options


@click.command('analyze')
@click.argument('project')
@click.option('--infile', '-i', help='Full path and filename of the input CSV file.', prompt="Enter a valid CSV file")
def analyze(project, infile):
    """
    Analyze a CSV file (infile) to create a model from the commandline.
    You must include a unique PROJECT.
    """
    click.echo('Analyze ' + infile + ' for the project: ' + project)
    
    process(project, infile, config['KUNTEKSTO']['delim'], config['KUNTEKSTO']['analyzelevel'], config['KUNTEKSTO']['outdir'])

@click.command('genmodel')
@click.argument('project')
def genmodel(project):
    """
    Generate a model based on PROJECT from the commandline. Note that this creates a new model. 
    You should remove any previous models based on this PROJECT. 
    """
    click.echo('Generate a model for: ' + project)

@click.command('gendata')
@click.argument('project')
@click.option('--infile', '-i', help='Full path and filename of the input CSV file.', prompt="Enter a valid CSV file")
def gendata(project, infile):
    """
    Generate data from a CSV file (infile) based on a model (project) from the commandline.
    """
    click.echo('Generate data from ' + infile + ' based on the model: ' + project)


app.cli.add_command(analyze)
app.cli.add_command(genmodel)
app.cli.add_command(gendata)

# Routing
@app.route('/')
def index():
    return render_template('index.html')

