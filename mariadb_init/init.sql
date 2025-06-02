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
    id INT AUTO_INCREMENT PRIMARY KEY,
    user VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    salt VARCHAR(255) NOT NULL,
    date DATETIME NOT NULL
);
