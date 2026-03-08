from flask import Flask, request, url_for, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class PerehodnikForm(FlaskForm):
    Next = SubmitField('Next?')
    Comeback = SubmitField('Comeback')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('perehodnik_lyceum'))
    return render_template('login.html', title='Authorization', form=form)

@app.route('/', methods=['GET', 'POST'])
def perehodnik_lyceum():
    form = PerehodnikForm()
    if form.validate_on_submit():
        print("idi hahui")
    return render_template('perehodnik_lyceum.html', title='COMEBACK', form=form)


if __name__ == '__main__':
    app.run(port=2010, host='127.0.0.1')












































