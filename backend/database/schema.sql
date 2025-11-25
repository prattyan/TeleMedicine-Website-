-- Patient Database Schema
-- This SQL script creates the patient table and related structures

CREATE DATABASE IF NOT EXISTS healthbridge_db;
USE healthbridge_db;

-- Patient table to store all patient registration details
CREATE TABLE patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender ENUM('male', 'female', 'other') NOT NULL,
    address TEXT NOT NULL,
    village VARCHAR(100) NOT NULL,
    emergency_contact_name VARCHAR(100) NOT NULL,
    emergency_contact_phone VARCHAR(20) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    email_verified BOOLEAN DEFAULT FALSE,
    phone_verified BOOLEAN DEFAULT FALSE,
    last_login TIMESTAMP NULL,
    profile_picture_url VARCHAR(500) NULL,
    medical_record_number VARCHAR(50) UNIQUE NULL,
    preferred_language ENUM('en', 'hi', 'pa') DEFAULT 'en'
);

-- Index for faster queries
CREATE INDEX idx_patients_email ON patients(email);
CREATE INDEX idx_patients_phone ON patients(phone);
CREATE INDEX idx_patients_village ON patients(village);
CREATE INDEX idx_patients_medical_record ON patients(medical_record_number);

-- Medical History table (for future use)
CREATE TABLE medical_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    condition_name VARCHAR(255) NOT NULL,
    diagnosed_date DATE NULL,
    description TEXT NULL,
    is_chronic BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
);

-- Appointments table (for future use)
CREATE TABLE appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NULL,
    appointment_date DATETIME NOT NULL,
    appointment_type ENUM('telemedicine', 'in_person', 'emergency') NOT NULL,
    status ENUM('scheduled', 'confirmed', 'completed', 'cancelled', 'no_show') DEFAULT 'scheduled',
    symptoms TEXT NULL,
    notes TEXT NULL,
    consultation_fee DECIMAL(10,2) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
);

-- Prescriptions table (for future use)
CREATE TABLE prescriptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    appointment_id INT NULL,
    doctor_id INT NULL,
    medication_name VARCHAR(255) NOT NULL,
    dosage VARCHAR(100) NOT NULL,
    frequency VARCHAR(100) NOT NULL,
    duration VARCHAR(100) NOT NULL,
    instructions TEXT NULL,
    prescribed_date DATE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
    FOREIGN KEY (appointment_id) REFERENCES appointments(id) ON DELETE SET NULL
);

-- Insert sample data for testing (optional)
-- INSERT INTO patients (
--     first_name, last_name, email, phone, date_of_birth, gender, 
--     address, village, emergency_contact_name, emergency_contact_phone, 
--     password_hash, preferred_language
-- ) VALUES (
--     'राम', 'सिंह', 'ram.singh@example.com', '+91-9876543210', '1985-06-15', 'male',
--     'H.No. 123, Main Street', 'Nabha', 'सीता सिंह', '+91-9876543211',
--     '$2b$10$hash_here', 'hi'
-- );