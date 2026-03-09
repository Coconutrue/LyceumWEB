from flask import Flask, request, url_for, render_template, redirect
from classes import LoginForm, homeForm, PerehodnikForm


menu = [{"name": "Lyceum", "url": "perehodnik_lyceum"},
        ]

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('home'))
    return render_template('login.html', title='Authorization', form=form)

@app.route('/', methods=['GET', 'POST'])
def home():
    form = homeForm()
    if form.validate_on_submit():
        if form.Lyceum.data:
            return redirect(url_for('perehodnik_lyceum'))
    return render_template('home.html', title='Home', form=form)


@app.route('/', methods=['GET', 'POST'])
def perehodnik_lyceum():
    form = PerehodnikForm()
    if form.validate_on_submit():
        if form.Next.data:
            print("Нажата кнопка Next")
            return "Выполняется действие для Next"
        elif form.Comeback.data:
            print("Нажата кнопка Comeback")
            return "Выполняется действие для Comeback"
    return render_template('perehodnik_lyceum.html', title='COMEBACK', form=form)



if __name__ == '__main__':
    app.run(port=2010, host='127.0.0.1')












































