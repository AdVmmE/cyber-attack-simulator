-- Users table for SQL Injection simulation
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'user'
);

-- Reset data
DELETE FROM users;
INSERT INTO users (username, password, role) VALUES ('admin', 'admin123', 'admin');
INSERT INTO users (username, password, role) VALUES ('alice', 'alicePass', 'user');
INSERT INTO users (username, password, role) VALUES ('bob', 'bobPass', 'user');

-- Comments table for Stored XSS simulation
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    content TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

DELETE FROM comments;
INSERT INTO comments (user_id, content) VALUES (2, 'Hello world! This is a safe comment.');
INSERT INTO comments (user_id, content) VALUES (3, 'Great site, very secure.');

