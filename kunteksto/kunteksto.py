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

from .analyze import process



if __name__ == "__main__":
    app.run()
