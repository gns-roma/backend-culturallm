CREATE DATABASE IF NOT EXISTS culturallm_db;
USE culturallm_db;

DROP TABLE IF EXISTS user;

DROP USER IF EXISTS 'user'@'%';
CREATE USER 'user'@'%' IDENTIFIED BY 'userpassword';
GRANT ALL PRIVILEGES ON culturallm_db.* to 'user'@'%' IDENTIFIED BY 'userpassword';
FLUSH PRIVILEGES;

CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user VARCHAR(255) not NULL,
    email VARCHAR(255) not NULL,
    password_hash VARCHAR(255) not NULL,
    salt VARCHAR(255) not NULL,
    date DATETIME not NULL
);
