from data import db_session
from flask import Flask, request, url_for, render_template, redirect, flash
from classes import LoginForm, homeForm
from data.users import User
from flask_login import LoginManager


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
@app.route('/')
@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User,user_id)





















@app.route('/', methods=['GET', 'POST'])
def home():
    form = homeForm()
    if form.validate_on_submit():
        if form.register.data:
            return redirect(url_for('login'))
        elif form.map.data:
            return redirect(url_for('map'))
        elif form.news.data:
            return redirect(url_for('news'))
        elif form.rules.data:
            return redirect(url_for('rules'))
    return render_template('home.html', title='Home', form=form)





















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


















@app.route('/about_project', methods=['GET', 'POST'])
def about_project():
    return render_template('about_project.html')

@app.route('/interior_payments', methods=['GET', 'POST'])
def interior_payments():
    return render_template('interior_payments.html')

@app.route('/map', methods=['GET', 'POST'])
def map():
    return render_template('map.html')

@app.route('/news', methods=['GET', 'POST'])
def news():
    return render_template('news.html')

@app.route('/rules', methods=['GET', 'POST'])
def rules():
    return render_template('rules.html')

@app.route('/locations', methods=['GET', 'POST'])
def locations():
    return render_template('locations.html')

@app.route('/What_is_this', methods=['GET', 'POST'])
def Monsters():
    return render_template('Monsters.html')


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    app.run(port=2010, host='127.0.0.1')