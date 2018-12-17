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
