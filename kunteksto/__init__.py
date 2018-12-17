import os
import configparser

from flask import Flask


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

