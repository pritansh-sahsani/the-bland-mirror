from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from main.config import Config
from flask_mail import Mail
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
bcrypt = Bcrypt(app)

# Initiate database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///the_bland_mirror.sqlite3'
db = SQLAlchemy(app)
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from main.models import *

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated
        

admin = Admin(app, index_view=MyAdminIndexView())

admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Posts, db.session))
admin.add_view(MyModelView(Comment, db.session))
admin.add_view(MyModelView(Subscribers, db.session))
admin.add_view(MyModelView(Likes, db.session))
admin.add_view(MyModelView(Messages, db.session))
admin.add_view(MyModelView(MessageReply, db.session))

mail = Mail(app)

from main import routes