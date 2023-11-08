DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS expense;

CREATE TABLE user (
    id TEXT PRIMARY KEY,
    email TEXT NOT NULL,
    given_name TEXT NOT NULL,
    family_name TEXT
);

CREATE TABLE expense (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    description TEXT NOT NULL,
    amount NUMERIC NOT NULL,
    created TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id)
);