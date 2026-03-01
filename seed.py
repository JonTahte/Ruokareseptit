import random
import sqlite3

db = sqlite3.connect("database.db")

db.execute("DELETE FROM users")
db.execute("DELETE FROM recipes")
db.execute("DELETE FROM reviews")

user_count = 1000
recipe_count = 10**6
review_count = 10**7

for i in range(1, user_count + 1):
    db.execute("INSERT INTO users (username) VALUES (?)",
               ["user" + str(i)])

for i in range(1, recipe_count + 1):
    user_id = random.randint(1, user_count)
    db.execute("INSERT INTO recipes (title, ingredients, user_id) VALUES (?, ?, ?)",
               ["recipe" + str(i), str(i),  user_id])

for i in range(1, review_count + 1):
    user_id = random.randint(1, user_count)
    recipe_id = random.randint(1, recipe_count)
    rating = random.randint(1, 5)
    db.execute("""INSERT INTO reviews (user_id, recipe_id, comment, rating, sent_at)
                  VALUES (?, ?, ?, ?, datetime('now'))""",
               [user_id, recipe_id, "comment" + str(i), rating])

db.commit()
db.close()
