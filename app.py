import re
import secrets
import math

import sqlite3
from flask import Flask
from flask import abort, flash, redirect, render_template, request, session
import markupsafe

import config
import db
import recipes
import reviews
import users

app = Flask(__name__)
app.secret_key=config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

@app.route("/")
@app.route("/<int:page>")
def index(page=1):
    page_size = 10
    recipe_count = recipes.recipe_count()
    page_count = math.ceil(recipe_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/1")
    if page > page_count:
        return redirect("/" + str(page_count))

    all_recipes = recipes.get_recipes(page, page_size)
    return render_template("index.html", page=page, page_count=page_count,
                            recipes=all_recipes)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    user_recipes = users.get_recipes(user_id)
    return render_template("show_user.html", user=user, recipes=user_recipes)

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

@app.route("/create_review", methods=["POST"])
def post_review():
    require_login()
    check_csrf()

    user_id = session["user_id"]
    recipe_id = request.form.get("recipe_id")
    recipe = recipes.get_recipe(recipe_id)
    if not recipe:
        abort(404)
    if recipe["user_id"] == user_id:
        abort(403)

    comment = request.form["comment"]
    if comment and len(comment) > 1000:
        abort(403)
    rating = request.form.get("star")
    if not rating:
        abort(403)

    reviews.add_review(user_id, recipe_id, comment, rating)
    return redirect("/recipe/" + str(recipe_id))

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

    if request.method=="POST":
        check_csrf()
        if "remove" in request.form:
            reviews.remove_review(user_id, recipe_id)
        return redirect("/recipe/" + str(recipe_id))

@app.route("/reviews/<int:recipe_id>")
@app.route("/reviews/<int:recipe_id>/<int:page>")
def show_reviews(recipe_id, page=1):
    page_size = 10
    review_count = reviews.review_count(recipe_id)
    page_count = math.ceil(review_count / page_size)
    page_count = max(page_count, 1)
    if page < 1:
        return redirect("/reviews/" + str(recipe_id) + "/1")
    if page > page_count:
        return redirect("/reviews/" + str(recipe_id) + "/" + str(page_count))

    recipe = recipes.get_recipe(recipe_id)
    recipe_reviews = reviews.get_reviews(recipe_id, page, page_size)
    return render_template("show_reviews.html", page=page,
                           page_count=page_count, recipe=recipe,
                           reviews=recipe_reviews, review_count=review_count)

@app.route("/new_recipe", methods = ["GET", "POST"])
def new_recipe():
    require_login()

    classes = recipes.get_all_classes()
    ingredients = [""]
    if request.method == "GET":
        remove_names_from_session()

    if request.method == "POST":
        ingredients = request.form.getlist("ingredients")
        for name, value in request.form.items():
            if name != "ingredients":
                session[name] = value
        ingredients = add_remove_ingredient(ingredients)
    return render_template("new_recipe.html", ingredients=ingredients,
                           classes=classes)

@app.route("/create_recipe", methods=["POST"])
def create_recipe():
    require_login()
    check_csrf()
    remove_names_from_session()

    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    prep_time = request.form["prep_time"]
    if not re.search("^[1-9][0-9]{0,2}$", prep_time):
        abort(403)
    ingredients_list = request.form.getlist("ingredients")
    if len(ingredients_list) > 15:
        abort(403)
    for ingredient in ingredients_list:
        if not ingredient or len(ingredient) > 50:
            abort(403)
    ingredients = ";".join(ingredients_list)
    cooking_steps = request.form["cooking_steps"]
    if not cooking_steps or len(cooking_steps) > 1000:
        abort(403)
    user_id = session["user_id"]

    classes = recipes.get_all_classes()
    my_classes=[]
    for class_name, class_values in classes.items():
        class_value = request.form[class_name]
        if class_value:
            if class_name not in classes:
                abort(403)
            if class_value not in class_values:
                abort(403)
            my_classes.append((class_name, class_value))

    recipes.add_recipe(title, prep_time, ingredients, cooking_steps, user_id)
    recipe_id = db.last_insert_id()
    recipes.add_recipe_classes(recipe_id, my_classes)
    return redirect("/recipe/" + str(recipe_id))

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

    if request.method == "POST":
        ingredients = request.form.getlist("ingredients")
        for name, value in request.form.items():
            if name != "ingredients":
                session[name] = value
        ingredients = add_remove_ingredient(ingredients)
    return render_template("edit_recipe.html", recipe=recipe,
                           ingredients=ingredients, all_classes=all_classes)

@app.route("/update_recipe", methods=["POST"])
def update_recipe():
    require_login()
    check_csrf()
    remove_names_from_session()

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
    if len(ingredients_list) > 15:
        abort(403)
    for ingredient in ingredients_list:
        if not ingredient or len(ingredient) > 50:
            abort(403)
    ingredients = ";".join(ingredients_list)

    cooking_steps = request.form["cooking_steps"]
    if not cooking_steps or len(cooking_steps) > 1000:
        abort(403)

    classes = recipes.get_all_classes()
    my_classes=[]
    for class_name, class_values in classes.items():
        class_value = request.form[class_name]
        if class_value:
            if class_name not in classes:
                abort(403)
            if class_value not in class_values:
                abort(403)
            my_classes.append((class_name, class_value))

    recipes.update_recipe(recipe_id, title, prep_time, ingredients,
                          cooking_steps)
    recipes.update_classes(recipe_id, my_classes)

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

    if request.method=="POST":
        check_csrf()
        if "remove" in request.form:
            recipes.remove_recipe(recipe_id)
            return redirect("/")
        else:
            return redirect("/recipe/"+str(recipe_id))

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)

        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            flash("VIRHE: väärä tunnus tai salasana")
            return redirect("/login")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create_account", methods = ["POST"])
def create_account():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        flash("VIRHE: salasanat eivät ole samat")
        return redirect("/register")

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        flash("VIRHE: tunnus on jo varattu")
        return redirect("/register")

    flash("Tunnus luotu")
    return redirect("/")

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")

def add_remove_ingredient(ingredients):
    if "add" in request.form:
        if len(ingredients) < 15:
            ingredients.append("")
        else:
            flash("VIRHE: Liian monta ainesosaa")
    elif "remove" in request.form:
        index_to_remove = int(request.form["remove"])
        if len(ingredients) > 1:
            ingredients.pop(index_to_remove)
        else:
            flash("VIRHE: Reseptillä on oltava vähintään 1 ainesosa")
    else:
        remove_names_from_session()
    return ingredients

def remove_names_from_session():
    keys = list(session.keys())
    keep_in_session = ["user_id", "username", "csrf_token"]
    for key in keys:
        if key not in keep_in_session:
            session.pop(key)
