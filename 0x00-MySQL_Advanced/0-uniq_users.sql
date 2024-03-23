-- create users table
CREATE table IF NOT EXISTS users(
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) NOT NULL,
        NAME  VARCHAR(255) NOT NULL UNIQUE
);
