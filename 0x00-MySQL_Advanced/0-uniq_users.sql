-- create users table
DROP TABLE IF EXISTS users;
CREATE table  users (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) NOT NULL UNIQUE,
        name  VARCHAR(255)
);
