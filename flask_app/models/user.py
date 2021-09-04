from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app import app
import re 

bcrypt = Bcrypt(app)

class User():
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_user(cls, data):

        hashed_pw = bcrypt.generate_password_hash(data['password'])
        
        data['hashed_pw'] = hashed_pw 

        connection = connectToMySQL('recipe_app')
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(hashed_pw)s)'
        new_user_id = connection.query_db(query, data)

        return new_user_id 
    
    @classmethod 
    def get_user_by_email(cls, data):
        connection = connectToMySQL('recipe_app')
        query = "SELECT * FROM users WHERE email = %(email)s"

        results = connection.query_db(query, data)

        if len(results) <= 0:
            return None
        else:
            return User(results[0])

    @staticmethod
    def validate_registration(data):
        is_valid = True

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(data['first_name']) < 3 or len(data['first_name']) > 30:
            is_valid = False
            flash('First name should be 3 to 30 characters')

        if len(data['last_name']) < 3 or len(data['last_name']) > 30:
            is_valid = False
            flash('Last name should be 3 to 30 characters')


        connection = connectToMySQL('recipe_app')
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connection.query_db(query, data)

        if len(results) != 0:
            is_valid = False
            flash('Email is already in use!!!')

        if not EMAIL_REGEX.match(data['email']):
            is_valid = False 
            flash('Please provide a valid email address!!!')

        if len(data['password']) < 8:
            is_valid = False 
            flash('Password should be at least eight characters long!')

        if data['password'] != data['confirm_password']:
            is_valid = False
            flash('Password and confirm password field should match!!!')
        
        return is_valid 
    