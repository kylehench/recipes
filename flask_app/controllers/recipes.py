from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import recipe

@app.route('/recipes/new')
def recepies_new():
  if 'user_id' not in session.keys():
    return redirect('/')
  return render_template('recipes-new.html')

@app.route('/recipes/create', methods=['POST'])
def recepies_create():
  print(request.form)
  if 'user_id' not in session.keys():
    return redirect('/')
  if not recipe.Recipe.validate_recipe(request.form):
    return redirect('/recipes/new')
  data = dict(request.form)
  data['user_id'] = session['user_id']
  recipe.Recipe.create(data)
  return redirect('/dashboard')

@app.route('/recipes/<int:id>')
def recipes_read(id):
  if 'user_id' not in session.keys():
    return redirect('/')
  return render_template('recipes-read.html', recipe=recipe.Recipe.get_by_id({'id':id}))

@app.route('/recipes/edit/<int:id>')
def recipes_edit(id):
  if 'user_id' not in session.keys():
    return redirect('/')
  return render_template('recipes-edit.html', recipe=recipe.Recipe.get_by_id({'id':id}))

@app.route('/recipes/update/<int:id>', methods=['POST'])
def recipes_update(id):
  if 'user_id' not in session.keys():
    return redirect('/')
  if not recipe.Recipe.validate_recipe(request.form):
    return redirect(f'/recipes/edit/{id}')
  data = dict(request.form)
  data['id'] = id
  recipe.Recipe.update(data)
  return redirect('/dashboard')

@app.route('/recipes/destroy/<int:id>')
def recipes_destroy(id):
  recipe.Recipe.delete({'id' : id})
  return redirect('/dashboard')