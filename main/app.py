from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initiate Flask app
app = Flask(__name__)

# Initiate database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///the_bland_mirror.sqlite3'
db = SQLAlchemy(app)

from main import routes