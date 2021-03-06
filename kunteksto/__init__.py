import configparser

import click
import os

from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, form
from flask_admin.contrib.sqla import ModelView
from flask_babelex import Babel

from .catalogs import make_catalog

parentdir = os.path.dirname(os.getcwd())

# Setup config info 
config = configparser.ConfigParser()
config.read(parentdir + '/kunteksto.conf')
print("\n\nKunteksto version: " + config['SYSTEM']['version'] + " using S3Model RM: " + config['SYSTEM']['rmversion'] + "\n\n")

catdir = os.path.join(parentdir, 'catalogs')
# create XML catalog if it doesn't exist
if not os.path.exists(catdir + "/Kunteksto_catalog.xml"):
    make_catalog(config)

# env var used by lxml
os.environ['XML_CATALOG_FILES'] = catdir + '/Kunteksto_catalog.xml'

app = Flask(__name__)
babel = Babel(app)

# set optional bootswatch theme https://bootswatch.com/3/yeti/
app.config['FLASK_ADMIN_SWATCH'] = config['KUNTEKSTO']['theme']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kunteksto.db'
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

@babel.localeselector
def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'en')


db = SQLAlchemy(app)

