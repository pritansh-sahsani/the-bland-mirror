from flask import render_template, url_for, redirect, request
from .app import app, db, bcrypt
from flask_login import login_required, login_user, current_user

@app.route("/")
@login_required
def index():
    if  request.method == "GET":
        return render_template("index.html")
    else:
        return render_template("result.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)

        db.session.add(user)
        db.session.commit()

        flash('Your account is successfully created, now you can log in!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

