from main import db, app, login_manager, bcrypt
from datetime import datetime
from flask_login import UserMixin
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    url_title = db.Column(db.String(100), nullable=False) 
    content = db.Column(db.String(1000000), nullable=False)
    summary= db.Column(db.String(140), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    cover_img = db.Column(db.String(9), nullable=False)
    views = db.Column(db.Integer, nullable=False, default=0)
    likes = db.Column(db.Integer, nullable=False, default=0)
    comments = db.Column(db.Integer, nullable=False, default=0)
    related_1 = db.Column(db.Integer, nullable=False, default=0)
    related_2 = db.Column(db.Integer, nullable=False, default=0)
    related_3 = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"Post('{self.id}', '{self.title}', '{self.created_at}', '{self.summary}', '{self.views}', '{self.likes}', '{self.comments}')"

class Comment(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    post_no = db.Column(db.Integer, nullable=False)
    comment_no = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    ip_address = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f"Comment('{self.id}', '{self.post_no}', '{self.comment_no}')"

class Subscribers(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    
    def __repr__(self):
        return f"Subscriber('{self.id}', ',{self.email}')"

class Likes(db.Model):
    id= db.Column(db.Integer, nullable=False, primary_key=True)
    post_no = db.Column(db.Integer, nullable=False)
    ip_address = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Subscriber('{self.id}')"

class Messages(db.Model):
    id= db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(4000), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    read = db.Column(db.Boolean, nullable = False, default=False)
    replied = db.Column(db.Boolean, nullable = False, default=False)

    
class MessageReply(db.Model):
    id= db.Column(db.Integer, nullable=False, primary_key=True)
    message_id = db.Column(db.Integer, nullable=False)
    reply = db.Column(db.String(4000), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255))
    is_read = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Notification {self.id}>"


with app.app_context():
    db.create_all()
    db.session.commit()