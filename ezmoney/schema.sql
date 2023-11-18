DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS transactions;

CREATE TABLE user (
    id TEXT PRIMARY KEY,
    email TEXT NOT NULL,
    given_name TEXT NOT NULL,
    family_name TEXT,
    currency TEXT DEFAULT 'USD'
);

CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    description TEXT NOT NULL,
    amount NUMERIC NOT NULL,
    created TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id)
);