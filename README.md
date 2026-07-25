# Student Management System

A database-driven web application built with **Flask**, **SQLAlchemy ORM**, **SQLite**, and **Jinja2** that provides complete CRUD functionality for managing student records and course enrollments.

## Features

- Create new student records
- Update existing student information
- Delete student records and associated enrollments
- View detailed student profiles
- Manage course enrollments
- Server-side rendering using Jinja2 templates
- SQLite database with SQLAlchemy ORM
- Relational database design with foreign key relationships

## Tech Stack

- Python 3
- Flask
- SQLAlchemy
- SQLite
- Jinja2
- HTML

## Project Structure

```
.
├── app.py
├── database.sqlite3
├── templates/
│   ├── index.html
│   ├── create.html
│   ├── update.html
│   ├── student.html
│   └── error.html
└── static/
```

## Database Schema

The application uses three relational tables:

- **Student**
  - Student ID
  - Roll Number
  - First Name
  - Last Name

- **Course**
  - Course ID
  - Course Code
  - Course Name
  - Course Description

- **Enrollment**
  - Enrollment ID
  - Student ID (Foreign Key)
  - Course ID (Foreign Key)

## Installation

Clone the repository:

```bash
git clone https://github.com/<username>/flask-student-management-system.git
```

Navigate to the project directory:

```bash
cd flask-student-management-system
```

Install the required dependencies:

```bash
pip install flask flask_sqlalchemy
```

Run the application:

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000/
```

## Functionality

- View all students from the home page
- Add new students with multiple course enrollments
- Update student information and enrolled courses
- Delete students and corresponding enrollment records
- View complete enrollment details for each student

## Concepts Demonstrated

- Flask Routing
- CRUD Operations
- SQLAlchemy ORM
- Relational Database Modeling
- Foreign Key Relationships
- Server-side Rendering
- Template Inheritance (Jinja2)
- Form Handling
- SQLite Integration

## License

This project is intended for educational and learning purposes.
