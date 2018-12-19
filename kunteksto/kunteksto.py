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

from . import app, config
from .analyze import process

from .models import Datamodel, Component, db



# Add Admin setup and administrative views here
admin = Admin(app, name='Kunteksto', template_mode='bootstrap3')

class DatamodelModelView(ModelView):
    can_create = False
    edit_modal = True
    can_export = True
    column_list = ('project', 'title', 'author', 'dmid', 'id')
    form_excluded_columns = ['dmid', 'dataid', 'components']
    def on_form_prefill(self, form, id):
        form.project.render_kw = {'readonly': True}  # make the project readonly
    
class ComponentModelView(ModelView):
    can_create = False
    edit_modal = True
    can_export = True
    column_list = ('header', 'label', 'datatype', 'mcid', 'model_id')
    form_excluded_columns = ['mcid', 'adid', 'model_id', 'model_link']

    def on_form_prefill(self, form, id):
        form.header.render_kw = {'readonly': True}  # make the header readonly

admin.add_view(DatamodelModelView(Datamodel, db.session))
admin.add_view(ComponentModelView(Component, db.session))



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


if __name__ == "__main__":
    app.run()
