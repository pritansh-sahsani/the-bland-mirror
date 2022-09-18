from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import User


class RegistrationForm(FlaskForm):
    name = StringField('Name',
                           validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered!')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class CForm(FlaskForm):
    type_of_chart = SelectField('Type of chart', choices=[('bar','Bar Chart'), ('pie','Pie Chart'), ('line','Line Chart'), ('scater', 'Scater Plot')])
    submit = SubmitField('Continue')

class CForm2(FlaskForm):
    rows = IntegerField('Number Of rows', validators=[DataRequired(),  Length(min=1 , max=5)])
    columns = IntegerField('Number Of columns', validators=[DataRequired(),  Length(min=1, max=2)])
    submit = SubmitField('Continue')