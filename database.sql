CREATE DATABASE client_query_management;
USE client_query_management;
CREATE TABLE users (id INT PRIMARY KEY AUTO_INCREMENT, username VARCHAR(50), email VARCHAR(50) NOT NULL, mobile_number VARCHAR(50) NOT NULL, hashed_password VARCHAR(255), role VARCHAR(10));
CREATE TABLE queries (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, email VARCHAR(100), mobile VARCHAR(15),category VARCHAR(50), heading VARCHAR(200), description TEXT, status VARCHAR(10) DEFAULT 'open', query_created_time DATETIME, query_closed_time DATETIME ,FOREIGN KEY (user_id) REFERENCES users(id) );

INSERT INTO users (username, email, mobile_number, hashed_password, role)
VALUES (
    'client1',
    'client1@example.com',
    '5454564645',
    '$2b$12$MwJ1sginlEGhM3xDuC5D1.OgyrgcEPannkuOerLso7wYpaLUkgQd6',
    'client'
);


INSERT INTO users (username, email, mobile_number, hashed_password, role)
VALUES (
    'support123',
    'support123@example.com',
    '4545878745',
    '$2b$12$b2O4SAiz9rdGU7Oq32neJuoySk7N4GO5pG.l.arsUF64ONu2dq9ZW',
    'support'
);

