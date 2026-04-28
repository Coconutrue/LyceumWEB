from data import db_session
from classes import LoginForm, NewsForm, homeForm, ProfileForm
from data.users import User
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from data.News import News
from PIL import Image
import os
import uuid
from flask import Flask, request, render_template, redirect, abort, url_for


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads/avatars'
app.config['NEWS_UPLOAD_FOLDER'] = 'static/uploads/news_images'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['NEWS_UPLOAD_FOLDER'], exist_ok=True)


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
    return render_template('about_project.html', title='About Project')


@app.route('/interior_payments', methods=['GET', 'POST'])
def interior_payments():
    return render_template('interior_payments.html')


@app.route('/map', methods=['GET', 'POST'])
def map():
    # try:
    x = request.args.get('x')
    y = request.args.get('y', default=64)
    z = request.args.get('z')
    return render_template('map.html', x=x, y=y, z=z)
    # except:
    #     return render_template('map.html')


@app.route('/rules', methods=['GET', 'POST'])
def rules():
    return render_template('rules.html')


@app.route('/locations', methods=['GET', 'POST'])
def locations():
    return render_template('locations.html', title='Locations')


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
            if len(form.username.data) < 4 or len(form.username.data) > 14:
                return render_template('profile.html', title='Авторизация',
                                       form=form,
                                       message="Ошибка. Длина имени должна составлять от 3 до 14 символов")

            if form.email.data != user.email:
                existing_user = db_sess.query(User).filter(User.email == form.email.data).first()
                if existing_user and existing_user.id != user.id:
                    return render_template('profile.html',
                                           form=form,
                                           message="Этот email уже используется")
                user.email = form.email.data
            if not "@" in form.email.data:
                return render_template('profile.html', title='Авторизация',
                                       form=form,
                                       message="Ошибка. Укажите корректную почту")
            if form.new_password.data:
                if not user.check_password(form.old_password.data):
                    return render_template('profile.html',
                                           form=form,
                                           message="Неверный старый пароль")
                if form.new_password.data != form.confirm_password.data:
                    return render_template('profile.html',
                                           form=form,
                                           message="Новые пароли не совпадают")
                if len(form.new_password.data) < 4 or len(form.new_password.data) > 14:
                    return render_template('profile.html', title='Авторизация',
                                           form=form,
                                           message="Ошибка. Длина пароля должна составлять от 3 до 14 символов")
                user.set_password(form.new_password.data)
            db_sess.commit()
            return render_template('profile.html',
                                   form=form,
                                   message="Профиль успешно обновлен!")
    else:
        form.username.data = current_user.name
        form.email.data = current_user.email
    return render_template('profile.html', title='Profile', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


"""news"""
#мб имеет смысл сделать какую-то общую функцию которая будет проводить все проверки с изображением?
@app.route("/news")
def news():
    db_sess = db_session.create_session()
    news = db_sess.query(News).all()
    news.sort(key=lambda x: x.created_date, reverse=True)
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
        news.category = form.category.data
        news.user_id = current_user.id
        saved_filepath = None
        try:
            if form.image.data:
                file = form.image.data
                if file and file.filename:
                    allowed_ext = {'jpg', 'jpeg', 'png', 'gif'}
                    ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'jpg'
                    if ext not in allowed_ext:
                        form.image.errors.append("Не поддерживаемый формат")
                        return render_template('add_news.html', title='Добавление новости', form=form)

                    filename = f"{uuid.uuid4().hex}.{ext}"
                    filepath = os.path.join(app.config['NEWS_UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    saved_filepath = filepath
                    if not check_r(filepath):
                        os.remove(filepath)
                        form.image.errors.append("Файл слишком большой")
                        return render_template('add_news.html', title='Добавление новости', form=form)

                    if not check_img(filepath):
                        os.remove(filepath)
                        form.image.errors.append("Файл повреждён или не является изображением")
                        return render_template('add_news.html', title='Добавление новости', form=form)

                    news.image = f"/static/uploads/news_images/{filename}"
            db_sess.add(news)
            db_sess.commit()
            return redirect('/news')
        except:
            db_sess.rollback()
            if saved_filepath:
                os.remove(saved_filepath)
            form.image.errors.append("Ошибка сервера при сохранении")
            return render_template('add_news.html', title='Добавление новости', form=form)
    return render_template('add_news.html', title='Добавление новости', form=form)

def check_img(filename):
    try:
        with Image.open(f"{filename}") as im:
            im.verify()
        return True
    except:
        return False

def check_r(filename):
    image = Image.open(f"{filename}")
    width, height = image.size
    if width > 4000 or height > 4000:
        return False
    return True




@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id).first()
    if not news:
        abort(404)
    if not can_manage_news(news):
        abort(403)
    if request.method == "GET":
        form.title.data = news.title
        form.content.data = news.content
        form.category.data = news.category

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        news.title = form.title.data
        news.content = form.content.data
        news.category = form.category.data
        saved_filepath = None
        old_path = None
        try:
            if form.image.data and form.image.data.filename:
                file = form.image.data
                if news.image:
                    old_path = os.path.join(app.config['NEWS_UPLOAD_FOLDER'], news.image.split('/')[-1])
                if file and file.filename:
                    allowed_ext = {'jpg', 'jpeg', 'png', 'gif'}
                    ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'jpg'
                    if ext not in allowed_ext:
                        return render_template('add_news.html', title='Редактирование новости', form=form)
                    filename = f"{uuid.uuid4().hex}.{ext}"
                    filepath = os.path.join(app.config['NEWS_UPLOAD_FOLDER'], filename)
                    saved_filepath = filepath
                    file.save(filepath)
                    if not check_r(filepath):
                        os.remove(filepath)
                        form.image.errors.append("Файл слишком большой")
                        return render_template('add_news.html', title='Редактирование новости', form=form)
                    if not check_img(filepath):
                        os.remove(filepath)
                        form.image.errors.append("Файл повреждён или не является изображением")
                        return render_template('add_news.html', title='Редактирование новости', form=form)
                    news.image = f"/static/uploads/news_images/{filename}"
            db_sess.commit()
            if saved_filepath and old_path and os.path.exists(old_path):
                os.remove(old_path)
            return redirect('/news')
        except:
            db_sess.rollback()
            if saved_filepath:
                os.remove(saved_filepath)
            form.image.errors.append("Ошибка сервера при сохранении")
            return render_template('add_news.html', title='Редактирование новости', form=form)
    return render_template('add_news.html',
                           title='Редактирование новости',
                           form=form
                           )


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id).first()
    if not news:
        abort(404)
    if not can_manage_news(news):
        abort(403)
    if news.image:
        image_path = os.path.join(app.config['NEWS_UPLOAD_FOLDER'], news.image.split('/')[-1])
        if os.path.exists(image_path):
            os.remove(image_path)
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
            return render_template('login.html', title='Авторизация',
                                   form=form,
                                   message="Пароли не совпадают")
        if len(form.password_reg.data) >= 14 or len(form.password_reg.data) < 2:
            return render_template('login.html', title='Авторизация',
                                   form=form,
                                   message="Ошибка. Длина имени должна составлять от 3 до 14 символов")
        if not form.username_reg.data or not form.email_reg.data or not form.password_reg.data:
            return render_template('login.html', title='Авторизация',
                                   form=form,
                                   message="Все регистрационные поля должны быть заполнены")
        if len(form.username_reg.data) >= 14 or len(form.username_reg.data) < 3:
            return render_template('login.html', title='Авторизация',
                                   form=form,
                                   message="Ошибка. Длина имени должна составлять от 4 до 14 символов")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email_reg.data).first():
            return render_template('login.html', title='Авторизация',
                                   form=form,
                                   message="Пользователь с этим электронным письмом уже существует")
        if not "@" in form.email_reg.data or form.email_reg.data[-1] == "@":
            return render_template('login.html', title='Авторизация',
                                   form=form,
                                   message="Ошибка. Укажите корректную почту")
        if db_sess.query(User).filter(User.name == form.username_reg.data).first():
            return render_template('login.html', title='Авторизация',
                                   form=form,
                                   message="Пользователь с таким именем уже существует")
        user = User(
            name=form.username_reg.data,
            email=form.email_reg.data,
        )
        user.set_password(form.password_reg.data)
        db_sess.add(user)
        db_sess.commit()
        return render_template('login.html', title='Авторизация',
                               form=form,
                               message="Успешная регистрация")
    elif form.submit_log.data:
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email_log.data).first()
        if user and user.check_password(form.password_log.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            return render_template('login.html', title='Авторизация',
                                   form=form,
                                   message="Неверный адрес электронной почты или пароль")
    return render_template('login.html', title='Авторизация', form=form)

"""ажминка"""
@app.context_processor
def utility_processor():
    def is_admin():
        return current_user.is_authenticated and current_user.is_admin
    return dict(is_admin=is_admin)

def can_manage_news(news):
    if not current_user.is_authenticated:
        return False
    if news.user == current_user:
        return True
    if current_user.is_admin:
        return True
    return False



if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    app.run(port=2010, host='127.0.0.1', debug=True)



    #tuna http 2010