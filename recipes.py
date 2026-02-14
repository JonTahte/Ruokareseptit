import db

def add_recipe(title, ingredients, cooking_steps, user_id):
    sql = """INSERT INTO recipes (title, ingredients, cooking_steps, user_id)
             VALUES (?, ?, ?, ?)"""
    db.execute(sql, [title, ingredients, cooking_steps, user_id])

def get_recipes():
    sql = "SELECT id, title FROM  recipes ORDER BY id DESC;"
    return db.query(sql)

def get_recipe(recipe_id):
    sql = """SELECT recipes.id,
                  recipes.title,
                  recipes.ingredients,
                  recipes.cooking_steps,
                  users.id user_id,
                  users.username
           FROM recipes, users
           WHERE recipes.user_id = users.id AND
                 recipes.id = ?"""
    result = db.query(sql, [recipe_id])
    return result[0] if result else None


def update_recipe(recipe_id, title, ingredients, cooking_steps):
    sql = """UPDATE recipes SET title = ?,
                            ingredients = ?,
                            cooking_steps = ?
                        WHERE id = ?"""
    db.execute(sql, [title, ingredients, cooking_steps, recipe_id])

def remove_recipe(recipe_id):
    sql = """DELETE FROM recipes
        WHERE id = ?"""
    db.execute(sql, [recipe_id])

def search_items(query):
    sql = """SELECT id, title
             FROM recipes
             WHERE title LIKE ?
             OR ingredients LIKE ?
             OR cooking_steps LIKE ?
             ORDER BY id DESC"""
    like="%" + query + "%"
    return db.query(sql, [like, like, like])