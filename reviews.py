import db

def get_review(user_id, recipe_id):
    sql = """SELECT reviews.recipe_id, reviews.comment, reviews.rating,
            reviews.sent_at, reviews.user_id, users.username
            FROM reviews, users
            WHERE users.id = reviews.user_id AND
            reviews.user_id = ? AND reviews.recipe_id = ?"""
    result = db.query(sql, [user_id, recipe_id])
    return result[0] if result else None

def get_reviews(recipe_id):
    sql = """SELECT reviews.user_id,
                    reviews.comment,
                    reviews.rating,
                    reviews.sent_at,
                    users.username
            FROM reviews, users
            WHERE reviews.user_id = users.id AND
                  recipe_id = ? ORDER BY reviews.id DESC"""
    return db.query(sql, [recipe_id])

def add_review(user_id, recipe_id, comment, rating):
    sql = """INSERT INTO reviews (user_id, recipe_id, comment, rating, sent_at)
             VALUES (?, ?, ?, ?, datetime('now'))"""
    db.execute(sql, [user_id, recipe_id, comment, rating])

    update_rating(recipe_id)
    

def remove_review(user_id, recipe_id):
    sql = """DELETE FROM reviews WHERE user_id = ? AND
            recipe_id = ?"""
    db.execute(sql, [user_id, recipe_id])

    update_rating(recipe_id)

def update_rating(recipe_id):
    sql = "SELECT ROUND(AVG(rating), 2) AS avg FROM reviews WHERE recipe_id = ?"
    result = db.query(sql, [recipe_id])

    rating = None
    if result:
        rating = result[0]["avg"]
    print(rating)
    sql = "UPDATE recipes SET rating = ? WHERE id = ?"
    db.execute(sql, [rating, recipe_id])
