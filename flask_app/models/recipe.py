from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app.models import user

class Recipe:
  db_name = 'recipes_schema'

  def __init__(self, data):
    self.id = data['id']
    self.name = data['name']
    self.under_30_min = data['under_30_min']
    self.description = data['description']
    self.instructions = data['instructions']
    self.recipe_date = data['recipe_date']
    self.created_at = data['created_at']
    self.updated_at = data['updated_at']
    self.user = None

  @staticmethod
  def validate_recipe(data):
    is_valid = True
    if len(data['name'])<3:
      flash('Name must be at least 3 characters.')
      is_valid = False
    if len(data['description'])<3:
      flash('Description must be at least 3 characters.')
      is_valid = False
    if len(data['instructions'])<3:
      flash('Instructions must be at least 3 characters.')
      is_valid = False
    if len(data['recipe_date'])<3:
      flash('Select a valid recipe date.')
      is_valid = False
    if 'under_30_min' not in data:
      flash('Indicate cooking time.')
      is_valid = False
    return is_valid

  @classmethod
  def create(cls, data):
    query = 'INSERT INTO recipes (name, under_30_min, description, instructions, recipe_date, user_id) VALUES ( %(name)s , %(under_30_min)s , %(description)s , %(instructions)s , %(recipe_date)s , %(user_id)s );'
    return connectToMySQL(cls.db_name).query_db(query, data)

  @classmethod
  def update(cls, data):
      query = "UPDATE recipes SET name = %(name)s, under_30_min = %(under_30_min)s, description = %(description)s, instructions = %(instructions)s , recipe_date = %(recipe_date)s WHERE id = %(id)s ;"
      return connectToMySQL(cls.db_name).query_db(query, data)

  @classmethod
  def get_by_id(cls, data):
      query = "SELECT * FROM recipes WHERE id = %(id)s;"
      results = connectToMySQL(cls.db_name).query_db(query, data)
      if len(results) < 1:
          return False
      return cls(results[0])

  @classmethod
  def get_all(cls):
    query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id ;"
    results = connectToMySQL(cls.db_name).query_db(query)
    recipes = []
    for row in results:
      recipe = cls(row)
      user_data = {
        'id' : row['users.id'],
        'created_at' : row['users.created_at'],
        'updated_at' : row['users.updated_at'],
        'first_name' : row['first_name'],
        'last_name' : row['last_name'],
        'email' : row['email'],
        'password' : row['password']
      }
      one_user = user.User(user_data)
      recipe.user = one_user
      recipes.append(recipe)
    return recipes

  @classmethod
  def delete(cls, data):
      query = "DELETE FROM recipes WHERE id = %(id)s ;"
      return connectToMySQL(cls.db_name).query_db(query, data)