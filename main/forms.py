from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from flask_wtf.file import FileAllowed, FileField
from wtforms.validators import DataRequired, Length, Email

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
    related_1 = SelectField('Post 1', validators=[DataRequired()])
    related_2 = SelectField('Post 2', validators=[DataRequired()])
    related_3 = SelectField('Post 3', validators=[DataRequired()])
    submit = SubmitField('Post')
    
    def __init__(self, selection_choices):
        super(PostForm, self).__init__()
        self.related_1.choices = selection_choices
        self.related_2.choices = selection_choices
        self.related_3.choices = selection_choices
