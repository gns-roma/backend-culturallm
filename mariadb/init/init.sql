CREATE DATABASE IF NOT EXISTS culturallm_db;
USE culturallm_db;

DROP TABLE IF EXISTS users;

DROP USER IF EXISTS 'user'@'%';

CREATE USER 'user'@'%' IDENTIFIED BY 'userpassword';
GRANT ALL PRIVILEGES ON culturallm_db.* TO 'user'@'%' IDENTIFIED BY 'userpassword';
FLUSH PRIVILEGES;

CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    salt VARCHAR(255) NOT NULL,
    signup_date DATETIME NOT NULL,
    last_login DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255), -- può essere null per LLM
    type ENUM('human', 'llm') NOT NULL DEFAULT 'human',
    question TEXT NOT NULL,
    topic VARCHAR(255) NOT NULL,
    cultural_specificity INT NOT NULL DEFAULT 0 CHECK (cultural_specificity BETWEEN 0 AND 10),
    cultural_specificity_notes TEXT,
    tag TEXT,
    FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS answers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_id INT NOT NULL,
    username VARCHAR(255), -- può essere null se per LLM
    type ENUM('human', 'llm') NOT NULL DEFAULT 'human',
    answer TEXT NOT NULL,
    timestamp DATETIME NOT NULL,
    UNIQUE (question_id, username),
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
    FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ratings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    answer_id INT NOT NULL,
    question_id INT NOT NULL,
    username VARCHAR(255) NOT NULL, -- utente che ha dato il rating, per questo non può essere null
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    flag_ia BOOLEAN NOT NULL,
    UNIQUE (question_id, username, answer_id),
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
    FOREIGN KEY (answer_id) REFERENCES answers(id) ON DELETE CASCADE,
    FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    action_type VARCHAR(255) CHECK (action_type IN ('question', 'answer', 'rating')),
    score INT NOT NULL DEFAULT 0,
    timestamp DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS leaderboard (
    username VARCHAR(255) NOT NULL,
    score INT NOT NULL DEFAULT 0,
    num_ratings INT DEFAULT 0,
    num_questions INT DEFAULT 0,
    num_answers INT DEFAULT 0,
    UNIQUE (username),
    FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
);