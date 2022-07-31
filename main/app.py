from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import bcrypt

# Initiate Flask app
app = Flask(__name__)

# App configurations
app.config['SECRET_KEY'] = '96cdd36bb88ee75a099543e467d621c4' # Random secret key for protecting from CSRF attacks
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dataistics.db' # SQLite database

# Initiate database
db = SQLAlchemy(app)

# Initialize bcrypt for encryption
bcrypt = Bcrypt(app)

from main import routes