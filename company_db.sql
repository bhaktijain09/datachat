-- Create a new database
CREATE DATABASE company_db;

-- Select the database
USE company_db;

-- Create Departments table
CREATE TABLE Departments (
    dept_id INT PRIMARY KEY AUTO_INCREMENT,
    dept_name VARCHAR(50) NOT NULL
);

-- Create Employees table
CREATE TABLE Employees (
    emp_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    position VARCHAR(50),
    hire_date DATE,
    dept_id INT,
    FOREIGN KEY (dept_id) REFERENCES Departments(dept_id)
);

-- Create Projects table
CREATE TABLE Projects (
    proj_id INT PRIMARY KEY AUTO_INCREMENT,
    proj_name VARCHAR(100) NOT NULL,
    dept_id INT,
    start_date DATE,
    end_date DATE,
    FOREIGN KEY (dept_id) REFERENCES Departments(dept_id)
);

-- Create Salaries table
CREATE TABLE Salaries (
    salary_id INT PRIMARY KEY AUTO_INCREMENT,
    emp_id INT,
    salary DECIMAL(10,2) NOT NULL,
    effective_date DATE,
    FOREIGN KEY (emp_id) REFERENCES Employees(emp_id)
);

-- Insert sample Departments
INSERT INTO Departments (dept_name) VALUES
('HR'),
('Engineering'),
('Sales'),
('Finance');

-- Insert sample Employees
INSERT INTO Employees (name, position, hire_date, dept_id) VALUES
('Alice Johnson', 'HR Manager', '2020-03-15', 1),
('Bob Smith', 'Software Engineer', '2019-07-22', 2),
('Charlie Brown', 'Sales Executive', '2021-01-10', 3),
('Diana Miller', 'Accountant', '2018-11-05', 4),
('Ethan Lee', 'DevOps Engineer', '2022-02-19', 2);

-- Insert sample Projects
INSERT INTO Projects (proj_name, dept_id, start_date, end_date) VALUES
('Employee Onboarding System', 1, '2022-01-01', '2022-06-30'),
('E-commerce Platform', 2, '2021-05-15', '2023-12-31'),
('CRM Upgrade', 3, '2022-03-01', '2022-12-01'),
('Financial Audit System', 4, '2020-07-01', '2021-01-31');

-- Insert sample Salaries
INSERT INTO Salaries (emp_id, salary, effective_date) VALUES
(1, 65000, '2023-01-01'),
(2, 85000, '2023-01-02');
