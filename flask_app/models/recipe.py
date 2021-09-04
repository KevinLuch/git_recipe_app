from flask.templating import render_template
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models.user import User



class Recipe():
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def recipe_name(self):
        return f" {self.id} {self.name} {self.description} {self.instructions} {self.updated_at}"

    @classmethod
    def get_all_recipes(cls):
        connection = connectToMySQL('recipe_app')
        results = connection.query_db('SELECT * FROM recipes;')

        recipes = []

        for item in results:
            recipes.append(cls(item))

        return recipes
    
    @classmethod
    def create_recipe(cls, data):
        connection = connectToMySQL('recipe_app')
        query = "INSERT INTO recipes (user_id, name, description, instructions) VALUES (%(user_id)s, %(name)s, %(description)s, %(instructions)s)"
        new_recipe_id = connection.query_db(query, data)

        return new_recipe_id

    @classmethod
    def destroy(cls, data):
        query = 'DELETE FROM recipes WHERE id = %(id)s;'
        return connectToMySQL('recipe_app').query_db(query, data)


    @staticmethod
    def validate_message(data):

        is_valid = True

        if len(data['name']) < 1:
            is_valid = False
            flash('Recipe name should be at least 2 characters!')
        if len(data['description']) < 5:
            is_valid = False
            flash('Description should be at least 5 characters!')
        if len(data['instructions']) < 5:
            is_valid = False
            flash('Instructions should be at least 5 characters!')

        return is_valid 

    @classmethod
    def get_by_id(cls, data):
        query = 'SELECT * FROM recipes WHERE recipes.id=%(id)s;'
        results = connectToMySQL('recipe_app').query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def update_recipe(cls, data):
        query = 'UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, updated_at = NOW() WHERE id = %(id)s;'
        return connectToMySQL('recipe_app').query_db(query, data)