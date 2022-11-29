from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

#This application has a bunch of URLs defined here so that we can have our views defined in several files and not a single one
#This is what Blueprints allows us to do
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first() #This is for looking for a specific field in the SQL Table you sepcified
        if user:
            if check_password_hash(user.password, password): #Check if password is correct for the specified email in the User table
                flash('Logged in Successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect Password", category='error')
    else:
        flash("Email does not exist.", category='error')

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
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        admin = request.form.get('admin')

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists.", category='error')
        elif admin != "Yes" and admin != "No":
            flash("Type \"Yes\" for an Admin account or type \"No\" for a User account.")
        elif len(email) < 4:
            flash('Email must be longer than 4 characters.', category='error')
        elif len(firstName) < 2:
            flash('First Name must be longer than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            if admin == "Yes":
                admin = True
            elif admin == "No":
                admin = False
            new_user = User(email=email, first_Name=firstName, password=generate_password_hash(password1, method='sha256'), admin_access = admin) #hashes password so it is not stored in plain text
            db.session.add(new_user)
            db.session.commit()
            flash('Account Created', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)