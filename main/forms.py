from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, PasswordField, BooleanField
from flask_wtf.file import FileAllowed, FileField
from wtforms.validators import DataRequired, EqualTo, Email, Length, ValidationError, Optional

from main.models import User

min_max_error_message = """{field} Length Must Be Between {min} and {max}!"""

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=1, max=20, message=min_max_error_message.format(field='User Name', min='%(min)d', max='%(max)d'))])
    email = StringField('Email', validators=[Length(min=1, max=120, message=min_max_error_message.format(field='Email', min='%(min)d', max='%(max)d')), Email()])
    password = PasswordField('Password', validators=[Length(min=1, max=60, message=min_max_error_message.format(field='Password', min='%(min)d', max='%(max)d'))])
    confirm_password = PasswordField('Confirm Password', validators=[Length(min=1, max=60, message=min_max_error_message.format(field='Confirm Password', min='%(min)d', max='%(max)d')), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError('That username is already taken. Please choose a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('That email is already registered. Please register using a different email address.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Length(min=1, max=120, message=min_max_error_message.format(field='Email', min='%(min)d', max='%(max)d')), Email()])
    password = PasswordField('Password', validators=[Length(min=1, max=60, message=min_max_error_message.format(field='Password', min='%(min)d', max='%(max)d'))])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class CommentForm(FlaskForm):
    text=StringField('Comment', validators=[Length(min=1, max=200, message=min_max_error_message.format(field='Comment', min='%(min)d', max='%(max)d'))])
    name=StringField('Name', validators=[Length(min=1, max=50, message=min_max_error_message.format(field='Name', min='%(min)d', max='%(max)d'))])
    submit = SubmitField('Send')

class SubscribeForm(FlaskForm):
    email = StringField('Email', validators=[Length(min=1, max=120, message=min_max_error_message.format(field='Message', min='%(min)d', max='%(max)d')), Email()])
    submit = SubmitField('Subscribe')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[Length(min=1, max=100, message=min_max_error_message.format(field='Name', min='%(min)d', max='%(max)d'))])
    email = StringField('Email', validators=[Length(min=1, max=120, message=min_max_error_message.format(field='Email', min='%(min)d', max='%(max)d')), Email()])
    message = TextAreaField('Message', validators=[Length(min=1, max=4000, message=min_max_error_message.format(field='Message', min='%(min)d', max='%(max)d'))])
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[Length(min=1, max=100, message=min_max_error_message.format(field='Title', min='%(min)d', max='%(max)d'))])
    content = TextAreaField('Content', validators=[Length(min=1, max=100000, message=min_max_error_message.format(field='Content', min='%(min)d', max='%(max)d'))])
    summary= StringField('Summary', validators=[Length(min=1, max=140, message=min_max_error_message.format(field='Summary', min='%(min)d', max='%(max)d'))])
    cover_img = FileField('Cover image', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Only .jpg, .png and .jpeg file formats are supported.')])
    related_1 = SelectField('Post 1', choices=[], validators=[DataRequired()])
    related_2 = SelectField('Post 2', choices=[], validators=[DataRequired()])
    related_3 = SelectField('Post 3', choices=[], validators=[DataRequired()])
    submit = SubmitField('Post')
    
    def __init__(self, s1, s2, s3):
        super(PostForm, self).__init__()
        self.related_1.choices = s1
        self.related_2.choices = s2
        self.related_3.choices = s3

class MessageReplyForm(FlaskForm):
    reply = TextAreaField('reply', validators=[Length(min=1, max=4000, message=min_max_error_message.format(field='Reply', min='%(min)d', max='%(max)d'))])
    submit = SubmitField('Reply')