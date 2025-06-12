CREATE DATABASE IF NOT EXISTS culturallm_db;

USE culturallm_db;


-- user management
DROP TABLE IF EXISTS users;

DROP USER IF EXISTS 'user'@'%';

CREATE USER 'user'@'%' IDENTIFIED BY 'userpassword';

GRANT ALL PRIVILEGES ON culturallm_db.* to 'user'@'%' IDENTIFIED BY 'userpassword';
FLUSH PRIVILEGES;

-- table creation
CREATE TABLE IF NOT EXISTS users (
    user VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    salt VARCHAR(255) NOT NULL,
    date DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user VARCHAR(255),
    question TEXT NOT NULL,
    topic VARCHAR(255) NOT NULL,
    score INT NOT NULL,
    score_notes TEXT NOT NULL,
    FOREIGN KEY (user) REFERENCES users(user) ON DELETE CASCADE
)
