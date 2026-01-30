CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

create table recipes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    cooking_steps TEXT,
    user_id INTEGER REFERENCES users
);

create table ingredients (
    id INTEGER PRIMARY KEY,
    ingredient TEXT,
    recipe_id INTEGER REFERENCES recipes
);