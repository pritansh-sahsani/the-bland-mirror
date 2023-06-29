from .app import db, app
from datetime import datetime

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
    related_1 = db.Column(db.Integer, nullable=False, default=1)
    related_2 = db.Column(db.Integer, nullable=False, default=2)
    related_3 = db.Column(db.Integer, nullable=False, default=3)

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

with app.app_context():
    db.create_all()
    db.session.commit()