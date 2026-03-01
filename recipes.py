import db

def recipe_count():
    sql = "SELECT COUNT(id) FROM recipes"
    return db.query(sql)[0][0]

def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    result = db.query(sql)

    classes={}

    for title, value in result:
        classes[title].append(value)
    return classes

def add_recipe(title, prep_time, ingredients, cooking_steps, user_id):
    sql = """INSERT INTO recipes (title, prep_time, ingredients,
                                  cooking_steps, user_id, rating)
             VALUES (?, ?, ?, ?, ?, NULL)"""
    db.execute(sql, [title, prep_time, ingredients, cooking_steps, user_id])

def add_recipe_classes(recipe_id, classes):
    sql = "INSERT INTO recipe_classes (recipe_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [recipe_id, title, value])

def get_classes(recipe_id):
    sql = "SELECT title, value FROM recipe_classes WHERE recipe_id = ?"
    return db.query(sql, [recipe_id])

def get_recipes(page, page_size):
    sql = """SELECT recipes.id, recipes.title, recipes.rating, 
            users.id AS user_id, users.username, 
       (SELECT COUNT(*) FROM reviews WHERE recipe_id = recipes.id) review_count
        FROM (
            SELECT id, title, rating, user_id 
            FROM recipes 
            ORDER BY id DESC 
            LIMIT ? OFFSET ?
        ) recipes
        JOIN users ON recipes.user_id = users.id;"""
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [limit, offset])

def get_recipe(recipe_id):
    sql = """SELECT recipes.id,
                    recipes.title,
                    recipes.prep_time,
                    recipes.ingredients,
                    recipes.cooking_steps,
                    recipes.rating,
                    users.id user_id,
                    users.username
             FROM recipes, users
             WHERE recipes.user_id = users.id AND
                    recipes.id = ?"""
    result = db.query(sql, [recipe_id])
    return result[0] if result else None


def update_recipe(recipe_id, title, prep_time, ingredients, cooking_steps):
    sql = """UPDATE recipes SET title = ?, prep_time = ?,
                    ingredients = ?, cooking_steps = ?
            WHERE id = ?"""
    db.execute(sql, [title, prep_time, ingredients, cooking_steps, recipe_id])

def update_classes(recipe_id, classes):
    sql = "DELETE FROM recipe_classes WHERE recipe_id = ?"
    db.execute(sql, [recipe_id])

    sql = "INSERT INTO recipe_classes (recipe_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [recipe_id, title, value])


def remove_recipe(recipe_id):
    sql = """DELETE FROM recipes WHERE id = ?"""
    db.execute(sql, [recipe_id])

def search_recipes(query, page, page_size):
    sql = """SELECT recipes.id, recipes.title, recipes.rating,
                    recipes.user_id, users.username
             FROM recipes, users
             WHERE users.id = recipes.user_id AND
                (recipes.title LIKE ?
                 OR recipes.ingredients LIKE ?
                 OR recipes.cooking_steps LIKE ?)
             ORDER BY recipes.id DESC
             LIMIT ? OFFSET ?"""
    like = "%" + query + "%"
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [like, like, like, limit, offset])

def query_recipe_count(query):
    sql = """SELECT COUNT(id) FROM recipes
            WHERE (recipes.title LIKE ?
                OR recipes.ingredients LIKE ?
                OR recipes.cooking_steps LIKE ?)
            ORDER BY recipes.id DESC"""
    if not query:
        query = ""
    like = "%" + query + "%"
    return db.query(sql, [like, like, like])[0][0]
