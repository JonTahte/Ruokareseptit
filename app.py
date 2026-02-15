import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
import config
import db
import recipes
import users
import re


app = Flask(__name__)
app.secret_key=config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    all_recipes = recipes.get_recipes()
    return render_template("index.html", recipes=all_recipes)


@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    recipes = users.get_recipes(user_id)
    return render_template("show_user.html", user=user, recipes=recipes)

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
    classes = recipes.get_classes(recipe_id)
    return render_template("show_recipe.html", recipe=recipe, classes=classes)

@app.route("/new_recipe", methods = ["GET", "POST"])
def new_recipe():
    require_login()
    classes = recipes.get_all_classes()
    ingredients = [""]
    if request.method == "POST":
        session.update(request.form.to_dict())
        ingredients = request.form.getlist("ingredients")

        if "add" in request.form:
            ingredients.append("")
        elif "remove" in request.form:
            index_to_remove = int(request.form["remove"])
            if len(ingredients) > 1:
                ingredients.pop(index_to_remove)
    else:
        remove_names_from_session()
    return render_template("new_recipe.html", ingredients=ingredients, state=session, classes=classes)

@app.route("/create_recipe", methods=["POST"])
def create_recipe():
    require_login()

    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    prep_time = request.form["prep_time"]
    if not re.search("^[1-9][0-9]{0,2}$", prep_time):
        abort(403)
    ingredients_list = request.form.getlist("ingredients")
    for ingredient in ingredients_list:
        if not ingredient or len(ingredient) > 50:
            abort(403)
    ingredients = ";".join(ingredients_list)
    cooking_steps = request.form["cooking_steps"]
    if not cooking_steps or len(cooking_steps) > 1000:
        abort(403)
    user_id = session["user_id"]

    class_names = recipes.get_all_class_names()
    classes=[]
    for name in class_names:
        value = request.form[name]
        if value:
            classes.append((name, value))

    recipes.add_recipe(title, prep_time, ingredients, cooking_steps, user_id, classes)

    return redirect("/")

@app.route("/edit_recipe/<int:recipe_id>", methods = ["GET", "POST"])
def edit_recipe(recipe_id):
    require_login()

    recipe = recipes.get_recipe(recipe_id)
    if not recipe:
        abort(404)
    if recipe["user_id"] != session["user_id"]:
        abort(403)

    ingredients = recipe["ingredients"].split(";")
    if request.method == "POST":
        session.update(request.form.to_dict())
        ingredients = request.form.getlist("ingredients")
        if "add" in request.form:
            ingredients.append("")
        elif "remove" in request.form:
            index_to_remove = int(request.form["remove"])
            if len(ingredients) > 1:
                ingredients.pop(index_to_remove)
    else:
        remove_names_from_session()
    return render_template("edit_recipe.html", recipe=recipe, ingredients=ingredients, state=session)

@app.route("/update_recipe", methods=["POST"])
def update_recipe():
    require_login()

    recipe_id = request.form["recipe_id"]
    recipe = recipes.get_recipe(recipe_id)
    if not recipe:
        abort(404)
    if recipe["user_id"] != session["user_id"]:
        abort(403)

    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)

    prep_time = request.form["prep_time"]
    if not re.search("^[1-9][0-9]{0,2}$", prep_time):
        abort(403)

    ingredients_list = request.form.getlist("ingredients")
    for ingredient in ingredients_list:
        if not ingredient or len(ingredient) > 50:
            abort(403)

    cooking_steps = request.form["cooking_steps"]
    if not cooking_steps or len(cooking_steps) > 1000:
        abort(403)
    ingredients = ";".join(ingredients_list)

    recipes.update_recipe(recipe_id, title, prep_time, ingredients, cooking_steps)

    return redirect("/recipe/" + str(recipe_id))

@app.route("/remove_recipe/<int:recipe_id>", methods = ["GET", "POST"])
def remove_recipe(recipe_id):
    require_login()

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

        user_id = users.check_login(username, password)

        if user_id:
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

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")

def remove_names_from_session():
    delete_from_session = [ "title", "prep_time", "ingredients", "cooking_steps"]
    classes=recipes.get_all_classes()
    for title in classes:
        delete_from_session.append(title)
    for name in delete_from_session:
        session.pop(name, None)