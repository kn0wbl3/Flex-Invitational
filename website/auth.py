from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, create_mail, validator   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        ghin = request.form.get('ghin')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif not validator.validate_ghin(ghin):
            flash('Your GHIN is incorrect', category='error')
        else:
            new_user = User(email=email, first_name=first_name, ghin=ghin, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)


@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            send_mail(user)
            flash('An email has been sent with instructions to reset your password', category='info')
            return redirect(url_for('auth.login'))
        else:
            flash('Email does not exist. Please create an account', category='error')
    return render_template('reset_password.html', user=current_user)


def send_mail(user):
    token = user.generate_token()
    mail = create_mail(current_app)
    msg = Message(
        'Password Reset Request', 
        sender="flexinvitational1@gmail.com", 
        recipients=[user.email],
    )
    msg.body = (
        f"Hi {user.first_name},\n\n"
        "Click the following link to reset your password:\n"
        f"http://localhost:5000/change_password/{token}"
    )
    mail.send(msg)
    

@auth.route('/change_password/<token>', methods=['GET', 'POST'])
def change_password(token):
    verified_user = User.verify_token(token)
    if not verified_user:
        flash("Password link has expired, please try again", category="error")
        return redirect(url_for('auth.reset_password'))
    if request.method == "POST":
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            verified_user.password = generate_password_hash(password1, method='sha256')
            db.session.commit()
            flash('Password Succesfully Changed!', category='success')
            return redirect(url_for('auth.login'))

    return render_template("change_password.html", user=current_user)