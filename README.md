# GradeVault — Student Grade Management System

A comprehensive, modern web application for managing student records, grades, enrollments, attendance, and academic reporting. Built with **Streamlit** and **MySQL**, featuring a dark grey glass-morphism UI with animated gradient backgrounds and full CRUD functionality across all schema tables.

---

## Features

### Dashboard
- Real-time system statistics — student, teacher, course, enrollment, and grade counts displayed in glass-morphism stat cards
- Recent enrollments feed showing the 6 most recent enrollments with student name, course code, status, and date
- Recent grades feed showing the 6 most recent grade entries with student name, course code, letter grade, percentage, and date

### Student Management
- Full CRUD (Create, Read, Update, Delete) for student records
- Fields: User ID, First Name, Last Name, Email, Phone, Date of Birth
- Input validation matching database constraints (ID range 110000–199999, DOB 1956–2010)
- Search by ID, name, email, or phone

### Teacher Management
- Full CRUD for teacher records
- Fields: User ID, First Name, Last Name, Email, Phone, Hire Date
- ID range validation (310000–399999), hire date ≥ 1970-01-01
- Search by ID, name, email, or phone

### Course Management
- Full CRUD for course records
- Fields: Course Code, Course Name, Units (1–6), Teacher (select from existing), Semester (1st/2nd/3rd)
- Dynamic teacher dropdown populated from the teachers table
- Search by ID, code, name, or semester

### Enrollment Management
- Full CRUD for student-course enrollments
- Fields: Student (select from existing), Course (select from existing), Enrollment Date, Status (Enrolled/Completed/Dropped/On hold)
- Dynamic student and course dropdowns
- Search by ID, student ID, course ID, or status

### Grade Management
- Full CRUD for grade records linked to enrollments
- Fields: Enrollment (select from existing), Letter Grade (A/B/C/D/F), Percentage (50.0–99.9), Grade Date
- Dynamic enrollment dropdown showing student name and course code
- Search by ID, enrollment ID, or letter grade

### Attendance Tracking
- Full CRUD for attendance records linked to enrollments
- Fields: Enrollment (select from existing), Attendance Date, Status (Present/Absent/Late/Excused)
- Dynamic enrollment dropdown
- Search by ID, enrollment ID, or status

### User Management
- Dedicated management page for system user accounts
- Fields: Username, Password, Role (Student/Teacher/Admin)
- Auto-incrementing User ID (210000–299999)
- Search by ID, username, or role
- Inline add/edit form

### Report Cards
- Two-tab view: **Report Card Details** and **Summary**
- Powered by MySQL views (`final_report_card_summary`, `report_card_summary`) from the SQL schema
- Filterable by individual student or view all
- Detail view: per-course grades, letter grading, passed/failed remarks, units, semester
- Summary view: total units enrolled/passed, GWA, attendance counts

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | Streamlit (Python web framework) |
| Backend | Python 3.x |
| Database | MySQL 5.7+ / 8.0+ |
| Database Driver | mysql-connector-python |
| Data Processing | Pandas |
| Styling | Custom CSS — glass-morphism dark theme |

---

## Database Schema

### Core Tables

| Table | Purpose | Key Constraints |
|-------|---------|----------------|
| `users` | System user accounts | ID: 210000–299999, roles: Student/Teacher/Admin |
| `students` | Student profiles | ID: 110000–199999, FK→users, DOB: 1956–2010 |
| `teachers` | Teacher profiles | ID: 310000–399999, FK→users, hire ≥ 1970 |
| `courses` | Course catalog | ID: 410000–499999, FK→teachers, units: 1–6, semester: 1st/2nd/3rd |
| `enrollments` | Student-course links | ID: 510000–599999, FK→students & courses, status: Enrolled/Completed/Dropped/On hold |
| `grades` | Grade records | ID: 610000–699999, FK→enrollments, letter: A–F, percentage: 50.0–99.9 |
| `attendance` | Attendance logs | ID: 710000–799999, FK→enrollments, status: Present/Absent/Late/Excused |

### Views (Report Cards)

| View | Description |
|------|-------------|
| `report_card_details` | Per-student, per-course breakdown with grade, letter, and passed/failed remarks |
| `report_card_summary` | Aggregated per-student/semester totals: units enrolled/passed, GWA, attendance counts |
| `final_report_card_summary` | Combined detail + summary — the primary view used in the Report Cards page |

---

## Project Structure

```
Student Grade Management System/
├─ .gitignore
├─ .streamlit/
│  └─ secrets.toml
├─ attendance.py
├─ components.py
├─ courses.py
├─ Data Dictionary/
│  ├─ Data Dictionary (PDF ver.).pdf
│  └─ Data Dictionary (Sheet ver.).xlsx
├─ Database & ERD/
│  ├─ ERD_student_db.mwb
│  ├─ ERD_student_db.pdf
│  ├─ student_grade_management_sys (updated).sql
│  └─ student_grade_report_cards (updated).sql
├─ database.py
├─ enrollments.py
├─ grades.py
├─ main.py
├─ README.md
├─ requirements.txt
├─ students.py
├─ teachers.py
└─ users.py
```

---

## Getting Started

### 1. Prerequisites

- Python 3.7+
- MySQL Server 5.7+ or 8.0+
- pip (Python package manager)

### 2. Database Setup

Create the database and import the SQL schema files in order:

```bash
mysql -u root -p -e "CREATE DATABASE student_db;"
mysql -u root -p student_db < "Database & ERD/student_grade_management_sys (updated).sql"
mysql -u root -p student_db < "Database & ERD/student_grade_report_cards (updated).sql"
```

### 3. Configuration

Create `.streamlit/secrets.toml` in the project root:

```toml
db_host = "localhost"
db_user = "root"
db_password = "your_mysql_password"
db_name = "student_db"
```

> **Note:** The `.gitignore` already excludes `.streamlit/secrets.toml` to prevent credential leaks.

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Application

```bash
streamlit run main.py
```

Opens in your default browser at `http://localhost:8501`.

---

## User Interface

### Design Theme

- **Dark grey color scheme** — neutral #121212–#222222 backgrounds with subtle dark blue radial gradient glows
- **Animated background** — background gradients slowly drift diagonally (30s ease-in-out loop) for a living, motion-like feel
- **Glass-morphism** — frosted-glass panels (`backdrop-filter: blur`) on sidebar, stat cards, buttons, and form fields
- **Custom styling** — rounded inputs (10px), styled scrollbars, soft glow hover effects, hidden Streamlit chrome (menu, footer)
- **Responsive layout** — `wide` mode with two-column forms and adaptive components
- **Inter font** — clean, modern sans-serif typography via Google Fonts

### Navigation

Sidebar radio menu with the following pages:
| Page | Description |
|------|-------------|
| Dashboard | System overview with KPI cards and recent activity |
| Students | Manage student records |
| Teachers | Manage teacher records |
| Courses | Manage course catalog |
| Enrollments | Manage student-course enrollments |
| Grades | Record and manage grades |
| Attendance | Track student attendance |
| Users | Manage system user accounts |
| Report Cards | View detailed and summary report cards |

---

## CRUD Operations

Each management page follows a consistent workflow:

1. **Search** — Type in the search bar to filter records in real time
2. **Add New** — Click "Add New" to open the creation form in an expander
3. **Edit** — Select a record from the dropdown, click "Edit" to populate the form
4. **Delete** — Select a record, click "Delete", then confirm or cancel
5. **Save/Cancel** — Submit changes or discard them

### Generic CRUD Engine

The `crud()` function in `components.py` handles all standard tables (students, teachers, courses, enrollments, grades, attendance). It accepts:
- Table name, columns, headers — for display and query construction
- Primary key and range — for auto-incrementing new IDs within CHECK constraints
- Field definitions — each field specifies type (text/number/decimal/select/date), label, validation bounds, and defaults
- Search columns — for the LIKE-based filter query
- Select label function — for customizing the record selector display

The users page uses a dedicated implementation with custom password field handling.

---

## Security

- **SQL Injection Prevention** — All queries use parameterized statements (`%s` placeholders) via `mysql.connector`
- **Credential Protection** — Database credentials stored in `.streamlit/secrets.toml` (in `.gitignore`)
- **Input Validation** — Field types, ranges, and constraints enforced at the UI level before any query is executed
- **Error Handling** — Connection and query errors are caught and displayed without exposing system internals
- **Role-Based Structure** — User roles (Student/Teacher/Admin) are stored in the schema for future access control implementation

---

## Requirements

```
streamlit
mysql-connector-python
pandas
```

Install with: `pip install -r requirements.txt`

---

## License

This project is part of the MySQL-Based-Projects collection.
