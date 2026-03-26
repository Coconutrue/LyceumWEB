from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional


class LoginForm(FlaskForm):
    username_log = StringField('Username', validators=[DataRequired()])
    password_log = PasswordField('Password', validators=[DataRequired()])
    email_log = StringField('Email', validators=[DataRequired()])
    username_reg = StringField('Username', validators=[Optional()])
    email_reg = StringField('Email', validators=[Optional()])
    password_reg = PasswordField('Password', validators=[Optional()])
    confirm_password_reg = PasswordField('Confirm Password', validators=[Optional()])
    submit_reg = SubmitField('Register')
    submit_log= SubmitField('Log In')

class homeForm(FlaskForm):
    Lyceum = SubmitField('Lyceum?')
    register = SubmitField('Authorization')
    profile = SubmitField('Личный кабинет')
    map = SubmitField('map')
    news = SubmitField('news')
    rules = SubmitField('rules')
    donation = SubmitField('donation')
    log_in = SubmitField('Log In')

class NewsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Содержание")
    is_private = BooleanField("Личное")
    submit = SubmitField('Применить')

class ProfileForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    old_password = PasswordField('Старый пароль')
    new_password = PasswordField('Новый пароль')
    confirm_password = PasswordField('Подтверждение пароля')
    submit = SubmitField('Сохранить изменения')
