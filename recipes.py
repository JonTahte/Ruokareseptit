import db

def add_recipe(title, ingredients, cooking_steps, user_id):
    sql = """INSERT INTO recipes (title, ingredients, cooking_steps, user_id)
            VALUES (?, ?, ?, ?)"""
    db.execute(sql, [title, ingredients, cooking_steps, user_id])