CREATE DATABASE IF NOT EXISTS culturallm_db;

USE culturallm-db;

CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT,
    user VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) not NULL,
    password_hash VARCHAR(255) not NULL.
    salt VARCHAR(255) not NULL,
    date DATETIME not NULL
);
