from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, RadioField
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
    profile = SubmitField('Personal account')
    map = SubmitField('map')
    news = SubmitField('news')
    rules = SubmitField('rules')
    donation = SubmitField('donation')
    log_in = SubmitField('Log In')

class NewsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Содержание")
    category = RadioField('Категория новости', choices=[
        ('bug', '🐛 Найден баг'),
        ('suggestion', '💡 Предложение изменений'),
        ('other', '📝 Другое'),
        ('advertisement', '📢 Реклама')
    ], validators=[DataRequired()], default='other')
    image = FileField('Изображение', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Только изображения!')])
    submit = SubmitField('Применить')

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    avatar = FileField('')
    old_password = PasswordField('Old password')
    new_password = PasswordField('New password')
    confirm_password = PasswordField('Password confirmation')
    submit = SubmitField('Save changes')