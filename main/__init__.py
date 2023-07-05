from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from main.config import Config
from flask_mail import Mail

app = Flask(__name__, instance_relative_config=False)
app.config.from_object(Config)
bcrypt = Bcrypt(app)

# Initiate database
db = SQLAlchemy(app)

migrate = Migrate(app, db)

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
admin.add_view(MyModelView(Notification, db.session))

mail = Mail(app)

from main import routes