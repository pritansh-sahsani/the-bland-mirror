from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from main.config import Config


app = Flask(__name__, instance_relative_config=False)
app.config.from_object(Config)

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
