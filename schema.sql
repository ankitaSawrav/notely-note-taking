DROP TABLE  IF EXISTS notes;
DROP TABLE  IF EXISTS users;


CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    user_name TEXT,
    user_email TEXT,
    password_hash TEXT
);

CREATE TABLE notes (
    notes_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    title varchar(50),
    notes_description TEXT,
    likes INTEGER,
    dislikes INTEGER
);