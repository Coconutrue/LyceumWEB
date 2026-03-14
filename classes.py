from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class homeForm(FlaskForm):
    Lyceum = SubmitField('Lyceum?')
    register = SubmitField('Authorization')


class PerehodnikForm(FlaskForm):
    Next = SubmitField('Next?')
    Comeback = SubmitField('Comeback')
class lyceum_form(FlaskForm):
    TrueHome = SubmitField('Home')

