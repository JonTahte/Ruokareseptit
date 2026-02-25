import db

def get_review(user_id, recipe_id):
    sql = "SELECT recipe_id, comment, grade FROM reviews WHERE user_id = ? and recipe_id = ?"
    result = db.query(sql, [user_id, recipe_id])
    return result[0] if result else None

def get_reviews(recipe_id):
    sql = """SELECT reviews.user_id,
                    reviews.comment,
                    reviews.grade,
                    users.username
            FROM reviews, users
            WHERE reviews.user_id = users.id AND
                  recipe_id = ? ORDER BY reviews.id DESC"""
    return db.query(sql, [recipe_id])

def add_review(user_id, recipe_id, comment, grade):
    sql = """INSERT INTO reviews (user_id, recipe_id, comment, grade)
             VALUES (?, ?, ?, ?)"""
    db.execute(sql, [user_id, recipe_id, comment, grade])

    update_grade(recipe_id)
    

def remove_review(user_id, recipe_id):
    sql = """DELETE FROM reviews WHERE user_id = ? AND
            recipe_id = ?"""
    db.execute(sql, [user_id, recipe_id])

    update_grade(recipe_id)

def update_grade(recipe_id):
    sql = "SELECT ROUND(AVG(grade), 2) AS avg FROM reviews WHERE recipe_id = ?"
    result = db.query(sql, [recipe_id])

    grade = None
    if result:
        grade = result[0]["avg"] 
    print(grade)
    sql = "UPDATE recipes SET grade = ? WHERE id = ?"
    db.execute(sql, [grade, recipe_id])
