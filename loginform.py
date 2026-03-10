from flask import Flask, request, url_for, render_template, redirect
from classes import LoginForm, homeForm, PerehodnikForm, lyceum_form


menu = [{"name": "Lyceum", "url": "perehodnik_lyceum"},
        ]

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

@app.route('/')
@app.route('/', methods=['GET', 'POST'])
def home():
    form = homeForm()
    if form.validate_on_submit():
        if form.Lyceum.data:
            return redirect(url_for('perehodnik_lyceum'))
        elif form.register.data:
            return redirect(url_for('login'))
    return render_template('home.html', title='Home', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('home'))
    return render_template('login.html', title='Authorization', form=form)

@app.route('/perehodnik_lyceum', methods=['GET', 'POST'])
def perehodnik_lyceum():
    form = PerehodnikForm()
    if form.validate_on_submit():
        if form.Next.data:
            return redirect(url_for('lyceum_home'))
        elif form.Comeback.data:
            return redirect(url_for('home'))
    return render_template('perehodnik_lyceum.html', title='COMEBACK', form=form)

@app.route('/lyceum_home', methods=['GET', 'POST'])
def lyceum_home():
    form = lyceum_form()
    if form.validate_on_submit():
        if form.TrueHome.data:
            return redirect(url_for('home'))
    return render_template('lyceum_home.html', form=form)
if __name__ == '__main__':
    app.run(port=2010, host='127.0.0.1', debug=True)