create database placement_tracker;
use placement_tracker;
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
);
CREATE TABLE companies (
    company_id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    role VARCHAR(100) NOT NULL,
    package_lpa FLOAT NOT NULL,
    drive_date VARCHAR(20) NOT NULL,
    status VARCHAR(30) DEFAULT 'Applied',
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);