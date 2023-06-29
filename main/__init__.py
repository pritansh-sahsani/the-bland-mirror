from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from main.config import Config
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
mail = Mail(app)
bcrypt = Bcrypt(app)
admin = Admin(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from main.models import *

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Posts, db.session))
admin.add_view(ModelView(Comment, db.session))
admin.add_view(ModelView(Subscribers, db.session))
admin.add_view(ModelView(Likes, db.session))
admin.add_view(ModelView(Messages, db.session))
admin.add_view(ModelView(MessageReply, db.session))

from main import routes