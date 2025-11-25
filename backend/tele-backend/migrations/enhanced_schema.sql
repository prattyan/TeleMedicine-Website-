-- Enhanced Database Schema for Permanent Data Storage
-- TeleMedicine Platform - Nabha District, Punjab

CREATE DATABASE IF NOT EXISTS telemedicine;
USE telemedicine;

-- Users table - Main authentication and role management
CREATE TABLE users (
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
  
  -- Constraints for data integrity
  CONSTRAINT chk_phone_format CHECK (phone REGEXP '^[0-9]{10,15}$'),
  CONSTRAINT chk_email_format CHECK (email IS NULL OR email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
  
  -- Unique constraints to prevent duplicates
  UNIQUE KEY uk_phone_role (phone, role),
  UNIQUE KEY uk_email_role (email, role),
  UNIQUE KEY uk_employee_id (employee_id)
);

-- Patients table - Comprehensive patient information
CREATE TABLE patients (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  name VARCHAR(100) NOT NULL,
  age INT NOT NULL,
  gender ENUM('male','female','other') NOT NULL,
  village VARCHAR(100) NOT NULL,
  registration_date DATE DEFAULT (CURRENT_DATE),
  medical_record_number VARCHAR(20) UNIQUE,
  emergency_contact VARCHAR(15),
  blood_group VARCHAR(5),
  allergies TEXT,
  chronic_conditions TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  -- Data validation constraints
  CONSTRAINT chk_age_valid CHECK (age > 0 AND age <= 150),
  CONSTRAINT chk_village_not_empty CHECK (LENGTH(TRIM(village)) > 0),
  CONSTRAINT chk_name_not_empty CHECK (LENGTH(TRIM(name)) > 0),
  
  -- Foreign key with proper cascading
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Doctors table - Complete doctor profile information
CREATE TABLE doctors (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  name VARCHAR(100) NOT NULL,
  phone VARCHAR(15) NOT NULL,
  email VARCHAR(255) NOT NULL,
  employee_id VARCHAR(50) NOT NULL,
  specialization VARCHAR(100),
  qualification VARCHAR(200),
  license_number VARCHAR(50),
  years_of_experience INT DEFAULT 0,
  consultation_fee DECIMAL(10,2) DEFAULT 0.00,
  available_from TIME DEFAULT '09:00:00',
  available_to TIME DEFAULT '17:00:00',
  is_available BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  -- Data validation constraints
  CONSTRAINT chk_doctor_name_not_empty CHECK (LENGTH(TRIM(name)) > 0),
  CONSTRAINT chk_doctor_phone_format CHECK (phone REGEXP '^[0-9]{10,15}$'),
  CONSTRAINT chk_consultation_fee_positive CHECK (consultation_fee >= 0),
  CONSTRAINT chk_experience_valid CHECK (years_of_experience >= 0 AND years_of_experience <= 60),
  
  -- Foreign key with proper cascading
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Health Workers table - Complete health worker information
CREATE TABLE healthworkers (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  name VARCHAR(100) NOT NULL,
  assigned_village VARCHAR(100) NOT NULL,
  phone VARCHAR(15) NOT NULL,
  email VARCHAR(255) NOT NULL,
  employee_id VARCHAR(50) NOT NULL,
  qualification VARCHAR(200),
  supervisor_name VARCHAR(100),
  work_area TEXT,
  shift_timing VARCHAR(50) DEFAULT 'Day Shift',
  is_on_duty BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  -- Data validation constraints
  CONSTRAINT chk_healthworker_name_not_empty CHECK (LENGTH(TRIM(name)) > 0),
  CONSTRAINT chk_healthworker_phone_format CHECK (phone REGEXP '^[0-9]{10,15}$'),
  CONSTRAINT chk_assigned_village_not_empty CHECK (LENGTH(TRIM(assigned_village)) > 0),
  
  -- Foreign key with proper cascading
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Villages reference table for data consistency
CREATE TABLE villages (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE,
  district VARCHAR(50) DEFAULT 'Nabha',
  state VARCHAR(50) DEFAULT 'Punjab',
  pincode VARCHAR(10),
  population INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert Nabha district villages
INSERT INTO villages (name, pincode, population) VALUES
('Nabha', '147201', 75000),
('Amloh', '147203', 12000),
('Bhadson', '147204', 8000),
('Buchhoki', '147205', 5500),
('Dalel Singh Wala', '147206', 4200),
('Dhanola', '147207', 6800),
('Ghanaur', '147208', 9500),
('Jandali', '147209', 3800),
('Khanpur', '147210', 7200),
('Kukranwala', '147211', 4500),
('Lehragaga', '147212', 11000),
('Madhopur', '147213', 6200),
('Mandvi', '147214', 5800),
('Mehal Kalan', '147215', 4900),
('Milkpur', '147216', 5200),
('Nabha Rural', '147217', 8500),
('Phirni', '147218', 4100),
('Raikot', '147219', 9800),
('Sahnewal', '147220', 7500),
('Samaspur', '147221', 5900),
('Sangatpur', '147222', 6400),
('Sheron', '147223', 4700),
('Sirhind', '147224', 13500),
('Tapa Mandi', '147225', 8200),
('Uchana', '147226', 5600);

-- Appointments table for permanent medical records
CREATE TABLE appointments (
  id INT AUTO_INCREMENT PRIMARY KEY,
  patient_id INT NOT NULL,
  doctor_id INT,
  healthworker_id INT,
  appointment_date DATE NOT NULL,
  appointment_time TIME NOT NULL,
  appointment_type ENUM('consultation', 'checkup', 'emergency', 'followup') NOT NULL,
  status ENUM('scheduled', 'confirmed', 'completed', 'cancelled', 'no_show') DEFAULT 'scheduled',
  symptoms TEXT,
  diagnosis TEXT,
  treatment_plan TEXT,
  prescription TEXT,
  consultation_fee DECIMAL(10,2) DEFAULT 0.00,
  payment_status ENUM('pending', 'paid', 'failed') DEFAULT 'pending',
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  -- Foreign keys
  FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE SET NULL ON UPDATE CASCADE,
  FOREIGN KEY (healthworker_id) REFERENCES healthworkers(id) ON DELETE SET NULL ON UPDATE CASCADE
);

-- Medical records for permanent health history
CREATE TABLE medical_records (
  id INT AUTO_INCREMENT PRIMARY KEY,
  patient_id INT NOT NULL,
  appointment_id INT,
  record_date DATE DEFAULT (CURRENT_DATE),
  vital_signs JSON,
  symptoms TEXT,
  diagnosis TEXT,
  treatment TEXT,
  medications TEXT,
  follow_up_required BOOLEAN DEFAULT FALSE,
  follow_up_date DATE,
  created_by INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (appointment_id) REFERENCES appointments(id) ON DELETE SET NULL ON UPDATE CASCADE,
  FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL ON UPDATE CASCADE
);

-- System audit log for data integrity
CREATE TABLE audit_log (
  id INT AUTO_INCREMENT PRIMARY KEY,
  table_name VARCHAR(50) NOT NULL,
  operation ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
  record_id INT NOT NULL,
  old_values JSON,
  new_values JSON,
  changed_by INT,
  ip_address VARCHAR(45),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY (changed_by) REFERENCES users(id) ON DELETE SET NULL ON UPDATE CASCADE
);

-- Indexes for better performance and data retrieval
CREATE INDEX idx_users_phone ON users(phone);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_employee_id ON users(employee_id);

CREATE INDEX idx_patients_name ON patients(name);
CREATE INDEX idx_patients_village ON patients(village);
CREATE INDEX idx_patients_registration_date ON patients(registration_date);
CREATE INDEX idx_patients_medical_record_number ON patients(medical_record_number);

CREATE INDEX idx_doctors_name ON doctors(name);
CREATE INDEX idx_doctors_specialization ON doctors(specialization);
CREATE INDEX idx_doctors_employee_id ON doctors(employee_id);

CREATE INDEX idx_healthworkers_name ON healthworkers(name);
CREATE INDEX idx_healthworkers_village ON healthworkers(assigned_village);
CREATE INDEX idx_healthworkers_employee_id ON healthworkers(employee_id);

CREATE INDEX idx_appointments_date ON appointments(appointment_date);
CREATE INDEX idx_appointments_status ON appointments(status);
CREATE INDEX idx_appointments_patient_id ON appointments(patient_id);

CREATE INDEX idx_medical_records_patient_id ON medical_records(patient_id);
CREATE INDEX idx_medical_records_date ON medical_records(record_date);

-- Views for easy data access
CREATE VIEW patient_summary AS
SELECT 
  u.id as user_id,
  u.phone,
  p.name,
  p.age,
  p.gender,
  p.village,
  p.registration_date,
  p.medical_record_number,
  u.is_active,
  u.created_at as registered_at
FROM users u
JOIN patients p ON u.id = p.user_id
WHERE u.role = 'patient';

CREATE VIEW doctor_summary AS
SELECT 
  u.id as user_id,
  u.phone,
  u.email,
  d.name,
  d.employee_id,
  d.specialization,
  d.qualification,
  d.years_of_experience,
  d.consultation_fee,
  d.is_available,
  u.is_active,
  u.created_at as registered_at
FROM users u
JOIN doctors d ON u.id = d.user_id
WHERE u.role = 'doctor';

CREATE VIEW healthworker_summary AS
SELECT 
  u.id as user_id,
  u.phone,
  u.email,
  h.name,
  h.employee_id,
  h.assigned_village,
  h.qualification,
  h.shift_timing,
  h.is_on_duty,
  u.is_active,
  u.created_at as registered_at
FROM users u
JOIN healthworkers h ON u.id = h.user_id
WHERE u.role = 'healthworker';

-- Stored procedures for data integrity
DELIMITER //

CREATE PROCEDURE generate_medical_record_number(IN patient_id INT)
BEGIN
    DECLARE record_number VARCHAR(20);
    SET record_number = CONCAT('MRN', LPAD(patient_id, 6, '0'));
    UPDATE patients SET medical_record_number = record_number WHERE id = patient_id;
END //

CREATE PROCEDURE archive_old_appointments()
BEGIN
    -- Archive appointments older than 2 years
    INSERT INTO appointments_archive 
    SELECT * FROM appointments 
    WHERE appointment_date < DATE_SUB(CURDATE(), INTERVAL 2 YEAR);
    
    DELETE FROM appointments 
    WHERE appointment_date < DATE_SUB(CURDATE(), INTERVAL 2 YEAR);
END //

DELIMITER ;

-- Backup and recovery procedures
-- Create backup tables structure
CREATE TABLE users_backup LIKE users;
CREATE TABLE patients_backup LIKE patients;
CREATE TABLE doctors_backup LIKE doctors;
CREATE TABLE healthworkers_backup LIKE healthworkers;

-- Data validation triggers
DELIMITER //

CREATE TRIGGER validate_patient_data 
BEFORE INSERT ON patients
FOR EACH ROW
BEGIN
    IF NEW.age <= 0 OR NEW.age > 150 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid age: must be between 1 and 150';
    END IF;
    
    IF LENGTH(TRIM(NEW.name)) = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Patient name cannot be empty';
    END IF;
    
    IF LENGTH(TRIM(NEW.village)) = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Village name cannot be empty';
    END IF;
END //

CREATE TRIGGER audit_user_changes
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (table_name, operation, record_id, old_values, new_values, changed_by)
    VALUES ('users', 'UPDATE', NEW.id, 
            JSON_OBJECT('phone', OLD.phone, 'email', OLD.email, 'is_active', OLD.is_active),
            JSON_OBJECT('phone', NEW.phone, 'email', NEW.email, 'is_active', NEW.is_active),
            NEW.id);
END //

DELIMITER ;

-- Grant appropriate permissions
-- Note: Adjust these based on your actual database user configuration
-- GRANT SELECT, INSERT, UPDATE ON telemedicine.* TO 'telemed_app'@'localhost';
-- GRANT DELETE ON telemedicine.otps TO 'telemed_app'@'localhost';

-- Initialize system data
INSERT INTO users (role, phone, email, password_hash, employee_id, is_verified) VALUES
('doctor', '9999999999', 'admin@nabha-telemed.in', '$2b$10$dummy.hash.for.admin', 'ADMIN001', TRUE);

INSERT INTO doctors (user_id, name, phone, email, employee_id, specialization, qualification) VALUES
(1, 'Dr. System Administrator', '9999999999', 'admin@nabha-telemed.in', 'ADMIN001', 'General Medicine', 'MBBS');

-- Show tables created
SHOW TABLES;