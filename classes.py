from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Optional


class LoginForm(FlaskForm):
    username_log = StringField('Имя пользователя', validators=[DataRequired()])
    password_log = PasswordField('Пароль', validators=[DataRequired()])
    email_log = StringField('Почта', validators=[DataRequired()])
    username_reg = StringField('Имя пользователя', validators=[Optional()])
    email_reg = StringField('Почта', validators=[Optional()])
    password_reg = PasswordField('Пароль', validators=[Optional()])
    confirm_password_reg = PasswordField('Сохранить изменения', validators=[Optional()])
    submit_reg = SubmitField('Регистрация')
    submit_log= SubmitField('Вход')

class homeForm(FlaskForm):
    register = SubmitField('Авторизация')
    profile = SubmitField('Профиль')
    map = SubmitField('Карта')
    news = SubmitField('Новости')
    rules = SubmitField('Правила')
    donation = SubmitField('На сухарики')
    log_in = SubmitField('Вход')

class NewsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Содержание")
    category = RadioField('Категория новости', choices=[
        ('bug', 'Найден баг'),
        ('suggestion', ' Предложение изменений'),
        ('other', 'Другое'),
        ('advertisement', 'Реклама')
    ], validators=[DataRequired()], default='other')
    image = FileField('Изображение', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Только изображения!')])
    submit = SubmitField('Применить')

class ProfileForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('Почта', validators=[DataRequired()])
    avatar = FileField('')
    old_password = PasswordField('Прошлый пароль')
    new_password = PasswordField('Новый пароль')
    confirm_password = PasswordField('Повторите пароль')
    submit = SubmitField('Сохранить изменения')

