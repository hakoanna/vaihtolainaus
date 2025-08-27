CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    image BLOB
);

CREATE TABLE asks (
    id INTEGER PRIMARY KEY,
    title TEXT,
    content TEXT,
    sent_at TEXT,
    user_id INTEGER REFERENCES users,
    status INTEGER,
    type TEXT
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
);

CREATE TABLE ask_classes (
    id INTEGER PRIMARY KEY,
    ask_id INTEGER REFERENCES asks,
    title TEXT,
    value TEXT
);

CREATE TABLE replies (
    id INTEGER PRIMARY KEY,
    content TEXT,
    sent_at TEXT,
    user_id INTEGER REFERENCES users,
    ask_id INTEGER REFERENCES asks
);
