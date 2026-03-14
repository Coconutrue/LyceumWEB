from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username_log = StringField('Username', validators=[DataRequired()])
    password_log = PasswordField('Password', validators=[DataRequired()])
    email_log = StringField('Email', validators=[DataRequired()])
    username_reg = StringField('Username', validators=[DataRequired()])
    email_reg = StringField('Email', validators=[DataRequired()])
    password_reg = PasswordField('Password', validators=[DataRequired()])
    confirm_password_reg = PasswordField('Confirm Password', validators=[DataRequired()])
    submit_reg = SubmitField('Register')
    submit_log= SubmitField('Log In')

class homeForm(FlaskForm):
    Lyceum = SubmitField('Lyceum?')
    register = SubmitField('Authorization')


class PerehodnikForm(FlaskForm):
    Next = SubmitField('Next?')
    Comeback = SubmitField('Comeback')
class lyceum_form(FlaskForm):
    TrueHome = SubmitField('Home')

