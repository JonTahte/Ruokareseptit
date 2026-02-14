import db

def add_recipe(title, ingredients, cooking_steps, user_id):
    sql = """INSERT INTO recipes (title, ingredients, cooking_steps, user_id)
             VALUES (?, ?, ?, ?)"""
    db.execute(sql, [title, ingredients, cooking_steps, user_id])

def get_recipes():
    sql="SELECT id, title FROM  recipes ORDER BY id DESC;"
    return db.query(sql)

def get_recipe(recipe_id):
    sql="""SELECT recipes.title,
                  recipes.ingredients,
                  recipes.cooking_steps,
                  users.username
           FROM recipes, users
           WHERE recipes.user_id = users.id AND
                 recipes.id = ?"""
    return db.query(sql, [recipe_id])[0]