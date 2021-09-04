from flask_app import app
from flask import render_template, redirect, request, session, flash 
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.recipe import Recipe

@app.route('/recipes')
def all_recipes():
    if 'user_id' not in session:
        flash('Please log in to view the recipes!')
        return redirect('/')
    
    return render_template('recipes.html')


@app.route('/recipes/create', methods=['POST'])
def create_recipe():

    valid = Recipe.validate_message(request.form)

    if not valid:
        print('validation failed')
        return redirect('/recipes')
    
    print('validation success!')

    data = {
        'user_id': session['user_id'],
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions']
    }

    Recipe.create_recipe(data)

    return redirect('/recipes/all')

@app.route('/destroy/recipe/<int:recipe_id>')
def delete_recipe(recipe_id):

    data = {
        "id": recipe_id
    }
    Recipe.destroy(data)
    return redirect('/recipes/all')

@app.route('/recipes/all')
def all_of_recipes():

    connection = connectToMySQL('recipe_app')
    result = connection.query_db('SELECT * FROM recipes;')
    return render_template('all_recipes.html', recipes = result)


@app.route('/edit/recipe/<int:recipe_id>')
def edit_recipe(recipe_id):

    data = {
        "id": recipe_id
    }
    return render_template('edit.html', edit_recipe= Recipe.get_by_id(data))

@app.route('/update/recipe', methods=['POST'])
def update_recipe():
    
    
    data = {
        "id": request.form['id'],
        "name": request.form['name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
    }
    Recipe.update_recipe(data)
    return redirect('/recipes/all')