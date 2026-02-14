import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db
import recipes


app = Flask(__name__)
app.secret_key=config.secret_key

@app.route("/")
def index():
    all_recipes = recipes.get_recipes()
    return render_template("index.html", recipes=all_recipes)

@app.route("/search_recipe")
def search_recipe():
    query = request.args.get("query")
    if query:
        results = recipes.search_items(query)
    else:
        query = ""
        results = []
    return render_template("search_recipe.html",
                           query=query,
                           results=results)

@app.route("/recipe/<int:recipe_id>")
def show_recipe(recipe_id):
    recipe = recipes.get_recipe(recipe_id)
    if not recipe:
        abort(404)
    return render_template("show_recipe.html", recipe=recipe)

@app.route("/new_recipe", methods = ["GET", "POST"])
def new_recipe():
    title = ""
    cooking_steps = ""
    ingredients=[""]

    if request.method == "POST":
        title = request.form["title"]
        cooking_steps = request.form["cooking_steps"]
        ingredients = request.form.getlist("ingredients")

        if "add" in request.form:
            ingredients.append("")
        elif "remove" in request.form:
            index_to_remove = int(request.form["remove"])
            if len(ingredients) > 1:
                ingredients.pop(index_to_remove)

    return render_template("new_recipe.html",
                            ingredients=ingredients,
                            title=title,
                            cooking_steps=cooking_steps)

@app.route("/create_recipe", methods=["POST"])
def create_recipe():
    title=request.form["title"]
    ingredients_list = request.form.getlist("ingredients")
    cooking_steps = request.form["cooking_steps"]
    ingredients = ";".join(ingredients_list)
    user_id = session["user_id"]

    recipes.add_recipe(title, ingredients, cooking_steps, user_id)

    return redirect("/")

@app.route("/edit_recipe/<int:recipe_id>", methods = ["GET", "POST"])
def edit_recipe(recipe_id):
    recipe = recipes.get_recipe(recipe_id)
    if not recipe:
        abort(404)
    if recipe["user_id"] != session["user_id"]:
        abort(403)

    recipe_id = recipe[0]
    title = recipe[1]
    cooking_steps = recipe[3]
    ingredients=recipe[2].split(";")

    if request.method == "POST":
        title = request.form["title"]
        cooking_steps = request.form["cooking_steps"]
        ingredients = request.form.getlist("ingredients")
        if "add" in request.form:
            ingredients.append("")
        elif "remove" in request.form:
            index_to_remove = int(request.form["remove"])
            if len(ingredients) > 1:
                ingredients.pop(index_to_remove)

    return render_template("edit_recipe.html",
                            recipe_id=recipe_id,
                            ingredients=ingredients,
                            title=title,
                            cooking_steps=cooking_steps)

@app.route("/update_recipe", methods=["POST"])
def update_recipe():
    recipe_id = request.form["recipe_id"]
    recipe = recipes.get_recipe(recipe_id)
    if not recipe:
        abort(404)
    if recipe["user_id"] != session["user_id"]:
        abort(403)

    title = request.form["title"]
    cooking_steps = request.form["cooking_steps"]
    ingredients_list = request.form.getlist("ingredients")
    ingredients = ";".join(ingredients_list)

    recipes.update_recipe(recipe_id, title, ingredients, cooking_steps)

    return redirect("/recipe/" + str(recipe_id))

@app.route("/remove_recipe/<int:recipe_id>", methods = ["GET", "POST"])
def remove_recipe(recipe_id):
    recipe = recipes.get_recipe(recipe_id)
    if not recipe:
        abort(404)
    if recipe["user_id"] != session["user_id"]:
        abort(403)

    if request.method=="GET":
        return render_template("remove_recipe.html", recipe=recipe)

    elif request.method=="POST":
        if "remove" in request.form:
            recipes.remove_recipe(recipe_id)
            return redirect("/")
        else:
            return redirect("/recipe/"+str(recipe_id))

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])[0]
        user_id = result["id"]
        password_hash = result["password_hash"]

        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create_account", methods = ["POST"])
def create_account():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])

    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")