CREATE DATABASE university_system;
USE university_system;

CREATE TABLE Departments (
    dept_id INT PRIMARY KEY AUTO_INCREMENT,
    dept_name VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE Year (
    year_id INT PRIMARY KEY AUTO_INCREMENT,
    year_name VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    dept_id INT,
    year_id INT,
    CONSTRAINT fk_students_dept
        FOREIGN KEY (dept_id) REFERENCES Departments(dept_id),
    CONSTRAINT fk_students_year
        FOREIGN KEY (year_id) REFERENCES Year(year_id)
) ENGINE=InnoDB;

CREATE TABLE Courses (
    course_id INT PRIMARY KEY AUTO_INCREMENT,
    course_name VARCHAR(100) NOT NULL,
    dept_id INT,
    FOREIGN KEY (dept_id) REFERENCES Departments(dept_id)
) ENGINE=InnoDB;

CREATE TABLE Enrollments (
    enrollment_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    course_id INT,
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
) ENGINE=InnoDB;

INSERT INTO Departments (dept_name) VALUES
('COMPS'),
('IT'),
('EXTC'),
('MECH');

INSERT INTO Year (year_name) VALUES
('First Year'),
('Second Year'),
('Third Year'),
('Fourth Year');

INSERT INTO students (full_name, email, dept_id, year_id) VALUES
('Bhakti Jain', '223bhakti0079@dbit.in', 1, 1),
('Neha Verma', 'neha.verma@dbit.in', 2, 2),
('Rohan Mehta', 'rohan.mehta@dbit.in', 1, 3),
('Priya Nair', 'priya.nair@dbit.in', 3, 1),
('Kunal Patil', 'kunal.patil@dbit.in', 4, 4);




