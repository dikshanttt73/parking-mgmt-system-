-- Create database and table for Parking Management System
CREATE DATABASE IF NOT EXISTS parking_db;
USE parking_db;

CREATE TABLE IF NOT EXISTS parkings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_no VARCHAR(20) NOT NULL,
    slot_no INT NOT NULL,
    entry_time DATETIME NOT NULL,
    exit_time DATETIME NULL,
    fee DECIMAL(8,2) NULL
);
