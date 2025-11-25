-- Quick Database Setup for TeleMedicine
-- Run this in MySQL Workbench or any MySQL client

CREATE DATABASE IF NOT EXISTS telemedicine;
USE telemedicine;

-- Users table - Main authentication and role management
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  role ENUM('patient','doctor','healthworker') NOT NULL,
  phone VARCHAR(15) NOT NULL,
  email VARCHAR(255) NULL,
  password_hash VARCHAR(255) NULL,
  employee_id VARCHAR(50) NULL,
  is_verified BOOLEAN DEFAULT TRUE,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  UNIQUE KEY uk_phone_role (phone, role),
  UNIQUE KEY uk_email_role (email, role),
  UNIQUE KEY uk_employee_id (employee_id)
);

-- Patients table
CREATE TABLE IF NOT EXISTS patients (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  name VARCHAR(100) NOT NULL,
  age INT NOT NULL,
  gender ENUM('male','female','other') NOT NULL,
  village VARCHAR(100) NOT NULL,
  registration_date DATE DEFAULT (CURRENT_DATE),
  medical_record_number VARCHAR(20) UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Doctors table
CREATE TABLE IF NOT EXISTS doctors (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  name VARCHAR(100) NOT NULL,
  phone VARCHAR(15) NOT NULL,
  email VARCHAR(255) NOT NULL,
  employee_id VARCHAR(50) NOT NULL,
  specialization VARCHAR(100) DEFAULT 'General Medicine',
  qualification VARCHAR(200) DEFAULT 'MBBS',
  years_of_experience INT DEFAULT 0,
  consultation_fee DECIMAL(10,2) DEFAULT 0.00,
  is_available BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Health Workers table
CREATE TABLE IF NOT EXISTS healthworkers (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  name VARCHAR(100) NOT NULL,
  assigned_village VARCHAR(100) NOT NULL,
  phone VARCHAR(15) NOT NULL,
  email VARCHAR(255) NOT NULL,
  employee_id VARCHAR(50) NOT NULL,
  qualification VARCHAR(200) DEFAULT 'ANM/GNM',
  shift_timing VARCHAR(50) DEFAULT 'Day Shift',
  is_on_duty BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Show tables created
SHOW TABLES;