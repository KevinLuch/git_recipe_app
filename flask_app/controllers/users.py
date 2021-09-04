from flask_app import app
from flask import render_template, redirect, request, session, flash 
from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

from flask_app.models.user import User


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/users/register', methods=['POST'])
def register_user():

    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': request.form['password'],
        'confirm_password': request.form['confirm_password'],
    }

    valid = User.validate_registration(data)

    if valid:
        User.create_user(data)
        flash('Account created - log in son!')
    return redirect('/')

@app.route('/users/login', methods=['POST'])
def login_user():

    print(request.form)

    data = {
        'email': request.form['email']
    }

    user = User.get_user_by_email(data)

    if user == None:
        flash('Email is invalid!')
        return redirect('/')

    print(user)

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Password is incorrect!')
        return redirect('/')
    
    session['user_id'] = user.id 
    session['email'] = user.email 

    return redirect("/recipes/all")

@app.route('/destroy')
def destroy():
    session.clear()
    return redirect('/')