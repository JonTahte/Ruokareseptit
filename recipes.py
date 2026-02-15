import db

def get_all_class_names():
    sql = "SELECT DISTINCT title FROM classes"
    result = db.query(sql)
    class_names=[]
    for entry in result:
        class_names.append(entry["title"])
    return class_names

def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    result = db.query(sql)

    classes={}
    for title, value in result:
        classes[title] = []
    for title, value in result:
        classes[title].append(value)

    return classes

def add_recipe(title, prep_time, ingredients, cooking_steps, user_id, classes):
    sql = """INSERT INTO recipes (title, prep_time, ingredients, cooking_steps, user_id)
             VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [title, prep_time, ingredients, cooking_steps, user_id])

    recipe_id = db.last_insert_id()

    sql="INSERT INTO recipe_classes (recipe_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [recipe_id, title, value])

def get_classes(recipe_id):
    sql = "SELECT title, value FROM recipe_classes WHERE recipe_id = ?"
    return db.query(sql, [recipe_id])

def get_recipes():
    sql = "SELECT id, title FROM  recipes ORDER BY id DESC;"
    return db.query(sql)

def get_recipe(recipe_id):
    sql = """SELECT recipes.id,
                  recipes.title,
                  recipes.prep_time,
                  recipes.ingredients,
                  recipes.cooking_steps,
                  users.id user_id,
                  users.username
            FROM recipes, users
            WHERE recipes.user_id = users.id AND
                 recipes.id = ?"""
    result = db.query(sql, [recipe_id])
    return result[0] if result else None


def update_recipe(recipe_id, title, prep_time, ingredients, cooking_steps):
    sql = """UPDATE recipes SET title = ?,
                            prep_time = ?,
                            ingredients = ?,
                            cooking_steps = ?
                        WHERE id = ?"""
    db.execute(sql, [title, prep_time, ingredients, cooking_steps, recipe_id])

def remove_recipe(recipe_id):
    sql = """DELETE FROM recipes
        WHERE id = ?"""
    print(recipe_id)
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