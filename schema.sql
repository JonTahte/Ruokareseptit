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
    rating INTEGER
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
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
    rating INTEGER,
    sent_at TEXT
);

CREATE INDEX idx_recipes_user_id ON recipes(user_id);
CREATE INDEX idx_reviews_recipe_id ON reviews(recipe_id);
