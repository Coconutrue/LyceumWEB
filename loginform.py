from data import db_session
from flask import Flask, request, render_template, redirect, abort, url_for
from classes import LoginForm, NewsForm, homeForm, ProfileForm
from data.users import User
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from data.News import News

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

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
        elif form.profile.data:
            return redirect(url_for('profile'))
        elif form.log_in.data:
            return redirect(url_for('login'))
    return render_template('home.html', title='Home', form=form)

@app.route('/about_project', methods=['GET', 'POST'])
def about_project():
    return render_template('about_project.html')

@app.route('/interior_payments', methods=['GET', 'POST'])
def interior_payments():
    return render_template('interior_payments.html')

@app.route('/map', methods=['GET', 'POST'])
def map():
    return render_template('map.html')

@app.route('/rules', methods=['GET', 'POST'])
def rules():
    return render_template('rules.html')

@app.route('/locations', methods=['GET', 'POST'])
def locations():
    return render_template('locations.html')

@app.route('/What_is_this', methods=['GET', 'POST'])
def Monsters():
    return render_template('Monsters.html')


"""профиль и его изменение(на подобии новостей)"""

@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    db_sess = db_session.create_session()
    if form.validate_on_submit():
        if form.submit.data:
            user = db_sess.query(User).filter(User.id == current_user.id).first()
            if form.username.data != user.name:
                existing_user = db_sess.query(User).filter(User.name == form.username.data).first()
                if existing_user and existing_user.id != user.id:
                    return render_template('profile.html',
                                           form=form,
                                           message="Это имя пользователя уже занято")
                user.name = form.username.data
            if form.email.data != user.email:
                existing_user = db_sess.query(User).filter(User.email == form.email.data).first()
                if existing_user and existing_user.id != user.id:
                    return render_template('profile.html',
                                           form=form,
                                           message="Этот email уже используется")
                user.email = form.email.data
            if form.new_password.data:
                if not user.check_password(form.old_password.data):
                    return render_template('profile.html',
                                           form=form,
                                           message="Неверный старый пароль")
                if form.new_password.data != form.confirm_password.data:
                    return render_template('profile.html',
                                           form=form,
                                           message="Новые пароли не совпадают")
                user.set_password(form.new_password.data)
            db_sess.commit()
            return render_template('profile.html',
                                   form=form,
                                   message="Профиль успешно обновлен!")
    else:
        form.username.data = current_user.name
        form.email.data = current_user.email

    return render_template('profile.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


"""news"""

@app.route("/news")
def news():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        news = db_sess.query(News).filter(
            (News.user == current_user) | (News.is_private == True)
        ).all()
    else:
        news = db_sess.query(News).filter(News.is_private == False).all()
    return render_template("news.html", news=news)

@app.route('/add_news', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/news')
    return render_template('add_news.html', title='Добавление новости', form=form)


@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/news')
        else:
            abort(404)
    return render_template('add_news.html',
                           title='Редактирование новости',
                           form=form
                           )

@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    return redirect('/news')


"""логин регистрация, вся фигня"""
@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


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
            login_user(user) #??? правильно ли оно тут стоит?
            return redirect(url_for('home'))
        else:
            return render_template('login.html', title='Authorization',
                                   form=form,
                                   message="Invalid email or password")

    return render_template('login.html', title='Authorization', form=form)

if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    app.run(port=2010, host='127.0.0.1')