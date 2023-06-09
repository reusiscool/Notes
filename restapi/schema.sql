-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS telegram;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE telegram(
  tg_id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  deleted TIMESTAMP DEFAULT NULL,
  notify TIMESTAMP DEFAULT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);
