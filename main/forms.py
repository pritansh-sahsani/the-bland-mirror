from email import message
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import phonenumbers

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
    content = TextAreaField('content', validators=[DataRequired(), Length(max=100000)])
    submit = SubmitField('Post')
