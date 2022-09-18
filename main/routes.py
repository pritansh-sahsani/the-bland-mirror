from flask import render_template, url_for, flash, redirect, request
from .app import app, db, bcrypt, login_manager
from .forms import RegistrationForm, LoginForm, CForm, CForm2
from .models import User
from flask_login import login_required, login_user, current_user, logout_user

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    """ Register user. """

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=hashed_password)

        db.session.add(user)
        db.session.commit()

        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """ Login user. """

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
    
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/chart", methods=['GET', 'POST'])
@login_required
def chart():
    form = CForm()
    if form.validate_on_submit():
        flash("a", 'danger')
        return redirect(url_for('index'))
    return render_template('chart.html', title='Chart', form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404