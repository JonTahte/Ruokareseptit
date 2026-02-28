# Pylint-raportti
Pylintin antama raportti sovelluksesta:

```
************* Module app
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:18:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:22:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:29:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:35:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:41:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:49:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:61:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:74:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:97:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:97:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:117:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:124:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:142:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:182:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:209:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:259:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:273:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
app.py:259:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:280:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:289:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
app.py:280:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:299:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:303:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:321:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:327:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:343:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module config
config.py:1:0: C0114: Missing module docstring (missing-module-docstring)
config.py:1:0: C0103: Constant name "secret_key" doesn't conform to UPPER_CASE naming style (invalid-name)      
************* Module db
db.py:1:0: C0114: Missing module docstring (missing-module-docstring)
db.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:10:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:10:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:19:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:22:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:22:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
************* Module recipes
recipes.py:1:0: C0114: Missing module docstring (missing-module-docstring)
recipes.py:3:0: C0116: Missing function or method docstring (missing-function-docstring)
recipes.py:14:0: C0116: Missing function or method docstring (missing-function-docstring)
recipes.py:20:0: C0116: Missing function or method docstring (missing-function-docstring)
recipes.py:25:0: C0116: Missing function or method docstring (missing-function-docstring)
recipes.py:29:0: C0116: Missing function or method docstring (missing-function-docstring)
recipes.py:37:0: C0116: Missing function or method docstring (missing-function-docstring)
recipes.py:53:0: C0116: Missing function or method docstring (missing-function-docstring)
recipes.py:59:0: C0116: Missing function or method docstring (missing-function-docstring)
recipes.py:68:0: C0116: Missing function or method docstring (missing-function-docstring)
recipes.py:72:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module reviews
reviews.py:1:0: C0114: Missing module docstring (missing-module-docstring)
reviews.py:3:0: C0116: Missing function or method docstring (missing-function-docstring)
reviews.py:12:0: C0116: Missing function or method docstring (missing-function-docstring)
reviews.py:23:0: C0116: Missing function or method docstring (missing-function-docstring)
reviews.py:30:0: C0116: Missing function or method docstring (missing-function-docstring)
reviews.py:38:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module users
users.py:1:0: C0114: Missing module docstring (missing-module-docstring)
users.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:9:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:15:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:20:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:28:4: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)

------------------------------------------------------------------
Your code has been rated at 8.42/10 (previous run: 8.42/10, +0.00)
```
Käydään tarkemmin läpi, miksi raportin huomautuksia ei olla korjattu.

## docstring-ilmoitukset

Suuri osa raportin ilmoituksista ovat seuraavanlaisia

```
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:18:0: C0116: Missing function or method docstring (missing-function-docstring)
```

Sovelluksen kehityksessä on tehty tietoisesti päätös, ettei käytetä docstring-kommentteja.

## Puuttuva palautusarvo

Raportissa on seuraavat ilmoitukset liittyen funktion puuttuvaan palautusarvoon

```
app.py:97:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:259:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:280:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
```

Esimerkiksi ensimmäinen ilmoitus koskee seuraavaa funktiota:

```python
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
```
Kyseinen funktio palauttaa arvon, kun `request.method` on `GET` tai `POST`. Jos request.method olisi siis jotai muuta, niin funktiolla ei olisi palautusarvoa. Kyseinen tilanne ei kuitenkaan ole mahdollinen, koska funktion dekoraattorissa on vaatimus, että metodin tulee olla `GET` tai `POST`.

## Tarpeeton else

Raportissa on seuraavat ilmoitukset liittyen `else`-haaroihin

```
app.py:273:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
app.py:289:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
users.py:28:4: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
```

Esimerkiksi ensimmäinen ilmoitus koskee seuraavaa koodia:
```python
if "remove" in request.form:
    recipes.remove_recipe(recipe_id)
    return redirect("/")
else:
    return redirect("/recipe/"+str(recipe_id))
```

Tämä koodi olisi mahdollista kirjoittaa seuraavasti tiiviimmin:

```python
if "remove" in request.form:
    recipes.remove_recipe(recipe_id)
    return redirect("/")
return redirect("/recipe/"+str(recipe_id))
```

Kuitenkin sovelluksen kehittäjän näkemyksen mukaan tällaisissa tapauksissa on selkeämpää kirjoittaa `else`-haara, koska se tuo esille kaksi vaihtoehtoa, miten koodi voi toimia eri tilanteissa.

## Vakion nimi

Raportissa on seuraava ilmoitus liittyen vakion nimeen

```
config.py:1:0: C0103: Constant name "secret_key" doesn't conform to UPPER_CASE naming style (invalid-name)
```

Tässä koodin päätasolla määritelty muuttuja tulkitaan vakioksi, jonka nimen tulisi olla kirjoitettu suurilla kirjaimilla. Muuttujaa käytetään koodissa näin:

```python
secret_key = "18fd24bf6a2ad4dac04a33963db1c42f"
```

Sovelluksen kehittäjän näkemyksen mukaan tässä tilanteessa näyttää paremmalta, että muuttujan nimi on pienillä kirjaimilla.

## Vaarallinen oletusarvo

Raportissa on seuraavat ilmoitukset liittyen vaaralliseen oletusarvoon:

```
db.py:10:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:22:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
```

Esimerkiksi ensimmäinen ilmoitus koskee seuraavaa funktiota:

```
def execute(sql, params=[]):
    con = get_connection()
    try:
        result = con.execute(sql, params)
        con.commit()
        g.last_insert_id = result.lastrowid
    finally:
        con.close()
```

Tässä parametrin oletusarvo `[]` on tyhjä lista. Tässä ongelmaksi voisi tulla, että sama oletusarvona oleva tyhjä listaolio on jaettu kaikkien funktion kutsujen kesken ja jos jossain kutsussa listan sisältöä muutettaisiin, tämä muutos näkyisi myös muihin kutsuihin. Tässä tapauksessa tämä ei haittaa, koska koodi ei muuta listaoliota.
