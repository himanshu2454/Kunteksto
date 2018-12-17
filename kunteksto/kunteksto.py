"""
Main entry point for the Kunteksto application.
"""
import sys
import os
import functools

import click
import configparser
from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from flask_admin import Admin, form
from flask_admin.form import rules
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import ModelView
from flask.cli import with_appcontext

from wtforms import fields, widgets
from sqlalchemy.event import listens_for
from jinja2 import Markup

from .analyze import analyze

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

# Create directory for file fields to use
file_path = os.path.join(os.path.dirname(__file__), 'csvfiles')
try:
    os.mkdir(file_path)
except OSError:
    pass


# Create models
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64))
    path = db.Column(db.Unicode(128))

    def __unicode__(self):
        return self.name


class Datamodel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'))
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


@click.command('genmodel')
@click.argument('model_id')
def genmodel(model_id):
    """
    Generate a model based on model_id from the commandline.
    """
    click.echo('Generate the model: ' + model_id)

@click.command('gendata')
@click.argument('model_id')
@click.option('--infile', '-i', help='Full path and filename of the input CSV file.', prompt="Enter a valid CSV file")
def gendata(model_id, infile):
    """
    Generate data from a CSV file (infile) based on a model (model_id) from the commandline.
    """
    click.echo('Generate data from ' + infile + ' based on the model: ' + model_id)


app.cli.add_command(genmodel)
app.cli.add_command(gendata)

# Routing
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_csv', methods=('GET', 'POST'))
def upload_csv():
    """
    Upload a new CSV file for analysis.
    """

    delim = config['KUNTEKSTO']['delim']
    analyzelevel = config['KUNTEKSTO']['analyzelevel']
    outdir = config['KUNTEKSTO']['outdir']
    
    if request.method == 'POST':
        infile = request.form['csvfile']
        db = get_db()
        error = None

        if not infile:
            error = 'A CSV file is required.'

        if error is None:
            analyze(infile, delim, analyzelevel, outdir)

        flash(error)

    return render_template('admin/index.html')



if __name__ == "__main__":
    app.run()
