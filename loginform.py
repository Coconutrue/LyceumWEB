from data import db_session
from flask import Flask, request, url_for, render_template, redirect, flash
from classes import LoginForm, homeForm, PerehodnikForm, lyceum_form
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'



@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.submit_reg.data:
        if form.password_reg.data != form.confirm_password_reg.data:
            return render_template('login.html', title='Authorization',
                                   form=form,
                                   message="Passwords don't match")
        if not form.username_reg.data or not form.email_reg.data or not form.password_reg.data:
            return render_template('login.html', title='Authorization',
                                   form=form,
                                   message="All registration fields must be filled in")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email_reg.data).first():
            return render_template('login.html', title='Authorization',
                                   form=form,
                                   message="The user with this email already exists")
        if db_sess.query(User).filter(User.name == form.username_reg.data).first():
            return render_template('login.html', title='Authorization',
                                   form=form,
                                   message="A user with that name already exists")
        user = User(
            name=form.username_reg.data,
            email=form.email_reg.data,
        )
        user.set_password(form.password_reg.data)
        db_sess.add(user)
        db_sess.commit()
        return render_template('login.html', title='Authorization',
                               form=form,
                               message="Successful registration, log in")
    elif form.submit_log.data:
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email_log.data).first()
        if user and user.check_password(form.password_log.data):
            return redirect(url_for('home'))
        else:
            return render_template('login.html', title='Authorization',
                                   form=form,
                                   message="Invalid email or password")

    return render_template('login.html', title='Authorization', form=form)

@app.route('/', methods=['GET', 'POST'])
def home():
    form = homeForm()
    if form.validate_on_submit():
        if form.Lyceum.data:
            return redirect(url_for('lyceum_home'))
        elif form.register.data:
            return redirect(url_for('login'))
    return render_template('home.html', title='Home', form=form)

@app.route('/lyceum_home', methods=['GET', 'POST'])
def lyceum_home():
    form = lyceum_form()
    if form.validate_on_submit():
        if form.TrueHome.data:
            return redirect(url_for('home'))
    return render_template('lyceum_home.html', form=form)


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    app.run(port=2010, host='127.0.0.1')