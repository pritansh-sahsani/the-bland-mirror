from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, PasswordField, BooleanField
from flask_wtf.file import FileAllowed, FileField
from wtforms.validators import DataRequired, EqualTo, Email, Length, ValidationError, Optional

from main.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
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
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class CommentForm(FlaskForm):
    text=StringField('Comment', validators=[DataRequired(),Length(max=200)])
    name=StringField('Comment', validators=[DataRequired(),Length(max=50)])
    submit = SubmitField('Send')

class SubscribeForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Subscribe')

class ContactForm(FlaskForm):
    name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired(), Length(max=4000)])
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    content = TextAreaField('Content', validators=[Length(min=1, max=100000)])
    summary= StringField('Summary', validators=[DataRequired(), Length(max=140)])
    cover_img = FileField('Cover image', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Only .jpg, .png and .jpeg file formats are supported.')])
    related_1 = SelectField('Post 1', choices=[], validators=[Optional()])
    related_2 = SelectField('Post 2', choices=[], validators=[Optional()])
    related_3 = SelectField('Post 3', choices=[], validators=[Optional()])
    submit = SubmitField('Post')
    
    def __init__(self, selection_choices):
        super(PostForm, self).__init__()
        self.related_1.choices = selection_choices
        self.related_2.choices = selection_choices
        self.related_3.choices = selection_choices

class MessageReplyForm(FlaskForm):
    reply = TextAreaField('reply', validators=[DataRequired(), Length(max=4000)])
    submit = SubmitField('Reply')