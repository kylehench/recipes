from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user
from flask_app.models import recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

def session_set_user(id):
  current_user = user.User.get_by_id({'id': id})
  session['user_id'] = current_user.id
  session['first_name'] = current_user.first_name
  session['full_name'] = current_user.full_name()

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/users/create', methods=['POST'])
def users_create():
  data = dict(request.form)
  if user.User.validate_user(data)==False or user.User.validate_email(data)==False:
    return redirect('/')
  data['password'] = bcrypt.generate_password_hash(data['password'])
  user_id = user.User.create(data)
  session_set_user(user_id)
  return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
  # see if the username provided exists in the database
  data = { "email" : request.form["email"] }
  user_in_db = user.User.get_by_email(data)
  # user is not registered in the db
  if not user_in_db:
    flash("Invalid Email/Password")
    return redirect("/")
  if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
    # if we get False after checking the password
    flash("Invalid Email/Password")
    return redirect('/')
  # if the passwords matched, we set the user_id into session
  session_set_user(user_in_db.id)
  return redirect('/dashboard')

@app.route('/dashboard')
def login_success():
  if 'user_id' not in session.keys():
    return redirect('/')
  return render_template('dashboard.html', recipes=recipe.Recipe.get_all())

@app.route('/logout')
def logout():
  session.clear()
  return redirect('/')