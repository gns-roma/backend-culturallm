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
    username VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    salt VARCHAR(255) NOT NULL,
    signup_date DATETIME NOT NULL,
    last_login DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255), /* può essere null per indicare una domanda di un LLM */
    type ENUM('human', 'llm') NOT NULL DEFAULT 'human',
    question TEXT NOT NULL,
    topic VARCHAR(255) NOT NULL,
    cultural_specificity INT /*NOT NULL*/,
    cultural_specificity_notes TEXT /*NOT NULL*/,
    tag TEXT,
    FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS answers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_id INT NOT NULL,
    username VARCHAR(255),
    type ENUM('human', 'llm') NOT NULL DEFAULT 'human',
    answer TEXT NOT NULL,
    timestamp DATETIME NOT NULL,
    UNIQUE (question_id, username), /* Un utente può rispondere una sola volta alla stessa domanda */
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
    FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ratings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    answer_id INT NOT NULL UNIQUE,
    question_id INT NOT NULL,
    username VARCHAR(255) UNIQUE,
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    flag_ia BOOLEAN NOT NULL,
    UNIQUE (question_id, username, answer_id), /* Un utente può valutare una sola volta la stessa risposta a una certa domanda */
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
    FOREIGN KEY (answer_id) REFERENCES answers(id) ON DELETE CASCADE,
    FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    action_type VARCHAR(255) NOT NULL,
    score INT NOT NULL,
    timestamp DATETIME NOT NULL
);
