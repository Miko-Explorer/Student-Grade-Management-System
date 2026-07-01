#Create a database:
CREATE DATABASE student_db;

#Set created database default schema:
USE student_db;

#Users table:
CREATE TABLE users(
	user_id INT PRIMARY KEY,
  CONSTRAINT chk_users_id CHECK(user_id BETWEEN 210000 AND 299999), 
  username VARCHAR(100) NOT NULL UNIQUE, 
  passwords VARCHAR(255) NOT NULL, 
  roles ENUM('Student', 'Teacher', 'Admin') NOT NULL
);

#Student's information table:
CREATE TABLE students(
	student_id INT PRIMARY KEY,
  CONSTRAINT chk_student_id CHECK(student_id BETWEEN 110000 AND 199999), 
  user_id INT NOT NULL, 
  FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
  first_name VARCHAR(100) NOT NULL, 
  last_name VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL UNIQUE, 
  phone VARCHAR(11) NOT NULL UNIQUE, 
  date_of_birth DATE NOT NULL, 
  CONSTRAINT chk_dob CHECK(date_of_birth BETWEEN '1956-01-01' AND '2010-12-31')
);

#Teacher's information table:
CREATE TABLE teachers(
	teacher_id INT PRIMARY KEY, 
  CONSTRAINT chk_teacher_id CHECK(teacher_id BETWEEN 310000 AND 399999), 
  user_id INT NOT NULL, 
  FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE, 
  first_name VARCHAR(100) NOT NULL, 
  last_name VARCHAR(100) NOT NULL, 
  email VARCHAR(100) NOT NULL UNIQUE, 
  phone VARCHAR(11) NOT NULL UNIQUE,
  hire_date DATE NOT NULL,
  CONSTRAINT chk_hire_date CHECK(hire_date >= '1970-01-01')
);

#Course table:
CREATE TABLE courses(
	course_id INT PRIMARY KEY, 
  CONSTRAINT chk_course_id CHECK(course_id BETWEEN 410000 AND 499999), 
  course_code VARCHAR(20) NOT NULL, 
  course_name VARCHAR(200) NOT NULL, 
  units INT NOT NULL,
  CONSTRAINT chk_units CHECK(units BETWEEN 1 AND 6),
  teacher_id INT NOT NULL, 
  FOREIGN KEY(teacher_id) REFERENCES teachers(teacher_id) ON DELETE CASCADE ON UPDATE CASCADE,
  semester ENUM('1st', '2nd', '3rd') NOT NULL
);

#Student's enrollment table:
CREATE TABLE enrollments(
	enrollment_id INT PRIMARY KEY, 
  CONSTRAINT chk_enrollment_id CHECK(enrollment_id BETWEEN 510000 AND 599999), 
  student_id INT NOT NULL, 
  FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE ON UPDATE CASCADE, 
  course_id INT NOT NULL, 
  FOREIGN KEY(course_id) REFERENCES courses(course_id) ON DELETE CASCADE ON UPDATE CASCADE, 
  enrollment_date DATE NOT NULL DEFAULT (CURRENT_DATE()), 
  CONSTRAINT chk_enroll_date CHECK(enrollment_date >= '2001-01-01'),
  enrollment_status ENUM('Enrolled', 'Completed', 'Dropped', 'On hold') NOT NULL DEFAULT 'Enrolled'
);

#Student's grade table:
CREATE TABLE grades(
	grade_id INT PRIMARY KEY, 
  CONSTRAINT chk_grade_id CHECK (grade_id BETWEEN 610000 AND 699999),
  enrollment_id INT NOT NULL, 
  FOREIGN KEY(enrollment_id) REFERENCES enrollments(enrollment_id) ON DELETE CASCADE ON UPDATE CASCADE,
  grade_letter ENUM('A', 'B', 'C', 'D', 'F') NOT NULL,
  grade_percentage DECIMAL(3,1) NOT NULL, 
  CONSTRAINT chk_grade_percentage CHECK(grade_percentage BETWEEN 50.0 AND 99.9), 
  grade_date DATE NOT NULL DEFAULT (CURRENT_DATE()),
  CONSTRAINT chk_grade_date CHECK(grade_date >= '2001-01-01')
);

#Student's attendance table:
CREATE TABLE attendance(
	attendance_id INT PRIMARY KEY, 
  CONSTRAINT chk_attendance_id CHECK(attendance_id BETWEEN 710000 AND 799999), 
  enrollment_id INT NOT NULL, 
  FOREIGN KEY(enrollment_id) REFERENCES enrollments(enrollment_id) ON DELETE CASCADE ON UPDATE CASCADE, 
  attendance_date DATE NOT NULL DEFAULT (CURRENT_DATE()), 
  CONSTRAINT chk_attendance_date CHECK(attendance_date >= '2001-01-01'),
  attendance_status ENUM('Absent', 'Present', 'Late', 'Excused') NOT NULL DEFAULT 'Present'
);

#Display records: 
SELECT * FROM users; 
SELECT * FROM students;
SELECT * FROM teachers; 
SELECT * FROM courses; 
SELECT * FROM enrollments; 
SELECT * FROM attendance; 
SELECT * FROM grades;