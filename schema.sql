CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE recipes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    prep_time INTEGER,
    ingredients TEXT,
    cooking_steps TEXT,
    user_id INTEGER REFERENCES users,
    grade INTEGER
);

CREATE TABLE classes (
    id INTGER PRIMARY KEY,
    title TEXT,
    value TEXT
    );

CREATE TABLE recipe_classes (
    id INTEGER PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes ON DELETE CASCADE,
    title TEXT,
    value TEXT
);

CREATE TABLE reviews (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    recipe_id INTEGER REFERENCES recipes ON DELETE CASCADE,
    comment TEXT,
    grade INTEGER
);