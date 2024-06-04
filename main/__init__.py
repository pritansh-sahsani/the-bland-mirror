from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_admin import Admin, AdminIndexView
from flask_msearch import Search
from flask_admin.contrib.sqla import ModelView
from flask_mail import Mail
from flask_login import current_user
from main.setup import app, db

bcrypt = Bcrypt(app)


# Initiate database

search = Search(app, db=db)

migrate = Migrate(app, db)

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
admin.add_view(MyModelView(PageViews, db.session))

mail = Mail(app)

from main import routes