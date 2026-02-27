import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
import config
import db
import recipes
import reviews
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

    my_review = None
    if "user_id" in session:
        my_review = reviews.get_review(session["user_id"], recipe_id)
    return render_template("show_recipe.html", recipe=recipe,
                           classes=classes, my_review=my_review)

@app.route("/remove_review/<int:recipe_id>", methods = ["GET", "POST"])
def remove_review(recipe_id):
    require_login()
    recipe = recipes.get_recipe(recipe_id)
    user_id = session["user_id"]
    review = reviews.get_review(user_id, recipe_id)

    if not review:
        abort(404)

    if request.method=="GET":
        return render_template("remove_review.html", recipe=recipe)

    elif request.method=="POST":
        if "remove" in request.form:
            reviews.remove_review(user_id, recipe_id)
        return redirect("/recipe/" + str(recipe_id))

@app.route("/reviews/<int:recipe_id>")
def show_reviews(recipe_id):
    recipe = recipes.get_recipe(recipe_id)
    recipe_reviews = reviews.get_reviews(recipe_id)
    return render_template("show_reviews.html", recipe=recipe, reviews=recipe_reviews)

@app.route("/create_review", methods=["POST"])
def post_review():
    require_login()

    user_id = session["user_id"]
    recipe_id = request.form["recipe_id"]
    recipe = recipes.get_recipe(recipe_id)
    if not recipe:
        abort(404)
    if recipe["user_id"] == user_id:
        abort(403)

    comment = request.form["comment"]
    if comment and len(comment) > 1000:
        abort(403)
    grade = request.form["grade"]
    if not re.search("^[1-5]$", grade):
        abort(403)

    reviews.add_review(user_id, recipe_id, comment, grade)
    return redirect("/recipe/" + str(recipe_id))

@app.route("/new_recipe", methods = ["GET", "POST"])
def new_recipe():
    require_login()
    classes = recipes.get_all_classes()
    ingredients = [""]
    if request.method == "GET":
        remove_names_from_session()

    elif request.method == "POST":
        for name, value in request.form.items():
            if name == "ingredients":
                ingredients = request.form.getlist("ingredients")
            else:
                session[name] = value

        if "add" in request.form:
            ingredients.append("")
        elif "remove" in request.form:
            index_to_remove = int(request.form["remove"])
            if len(ingredients) > 1:
                ingredients.pop(index_to_remove)
        else:
            remove_names_from_session()
    return render_template("new_recipe.html", ingredients=ingredients, classes=classes)

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

    class_names = recipes.get_all_classes()
    my_classes=[]
    for class_name in class_names:
        class_value = request.form[class_name]
        if class_value:
            if class_name not in class_names:
                abort(403)
            if class_value not in class_names[class_name]:
                abort(403)
            my_classes.append((class_name, class_value))

    new_recipe_id = recipes.add_recipe(title, prep_time, ingredients,
                                   cooking_steps, user_id, my_classes)
    return redirect("/recipe/" + str(new_recipe_id))

@app.route("/edit_recipe/<int:recipe_id>", methods = ["GET", "POST"])
def edit_recipe(recipe_id):
    require_login()

    recipe = recipes.get_recipe(recipe_id)
    if not recipe:
        abort(404)
    if recipe["user_id"] != session["user_id"]:
        abort(403)

    ingredients = recipe["ingredients"].split(";")
    all_classes = recipes.get_all_classes()

    if request.method == "GET":
        remove_names_from_session()
        for entry in recipes.get_classes(recipe_id):
            session[entry["title"]] = entry["value"]

    elif request.method == "POST":
        for name, value in request.form.items():
            if name == "ingredients":
                ingredients = request.form.getlist("ingredients")
            else:
                session[name] = value

        if "add" in request.form:
            ingredients.append("")
        elif "remove" in request.form:
            index_to_remove = int(request.form["remove"])
            if len(ingredients) > 1:
                ingredients.pop(index_to_remove)
        else:
            remove_names_from_session()
    return render_template("edit_recipe.html", recipe=recipe, 
                           ingredients=ingredients, all_classes=all_classes)

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

    class_names = recipes.get_all_classes()
    my_classes=[]
    for class_name in class_names:
        class_value = request.form[class_name]
        if class_value:
            if class_name not in class_names:
                abort(403)
            if class_value not in class_names[class_name]:
                abort(403)
            my_classes.append((class_name, class_value))

    recipes.update_recipe(recipe_id, title, prep_time, ingredients, cooking_steps, my_classes)

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
    keys = list(session.keys())
    for key in keys:
        if key!="user_id" and key!="username":
            session.pop(key)