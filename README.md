# Student Management System

## Overview

This project is a CLI-based Student Management System implemented in Python using Object-Oriented Programming (OOP) principles. The system allows users to manage student records, course enrollments, and grade assignments. Additionally, it provides functionality to save and load data to/from a file.

## Features

- **Add New Student**: Create and add a new student to the system.
- **Add New Course**: Create and add a new course to the system.
- **Enroll Student in Course**: Enroll a student in a specified course.
- **Add Grade for Student**: Assign or update a grade for a student in a specified course.
- **Display Student Details**: Retrieve and display details of a student, including enrolled courses and grades.
- **Display Course Details**: Retrieve and display details of a course, including the list of enrolled students.
- **Save Data to File**: Save all student and course data to a file in JSON format.
- **Load Data from File**: Load data from a file, restoring student, course, and enrollment information.

## Class Design

### Class 1: Person

- **Attributes**:
  - `name` (str): Name of the person.
  - `age` (int): Age of the person.
  - `address` (str): Address of the person.

- **Method**:
  - `display_person_info()`: Print the details of the person (name, age, and address).

### Class 2: Student (inherits from Person)

- **Additional Attributes**:
  - `student_id` (str): Unique identifier for each student.
  - `grades` (dict): Dictionary containing subjects and their respective grades.
  - `courses` (list): List of courses the student is enrolled in.

- **Methods**:
  - `add_grade(subject, grade)`: Add or update the grade for a specified subject.
  - `enroll_course(course)`: Enroll the student in a specified course.
  - `display_student_info()`: Print all details of the student, including enrolled courses and grades.

### Class 3: Course

- **Attributes**:
  - `course_name` (str): Name of the course.
  - `course_code` (str): Unique course code.
  - `instructor` (str): Name of the instructor.
  - `students` (list): List to store students enrolled in this course.

- **Methods**:
  - `add_student(student)`: Add a student to the course.
  - `display_course_info()`: Display the course details and the list of enrolled students.

## System Functionalities

The system provides a menu-driven CLI for users to interact with the system. The main options and functionalities include:

1. **Add Student**
2. **Add New Course**
3. **Enroll Student in Course**
4. **Add Grade for Student**
5. **Display Student Details**
6. **Display Course Details**
7. **Save Data to File**
8. **Load Data from File**
9. **Exit**

## Error Handling

- Verify that `student_id` and `course_code` exist before processing any operations.
- Ensure grades are only assigned to students for courses in which they are enrolled.

## Bonus Challenge

- **Save and Load Data**: Implement functions to save and load data in JSON format.

## Getting Started

1. Clone the repository or download the ZIP file.
2. Navigate to the project directory.
3. Run the main Python script to start the CLI.

```bash
python main.py
```


License
This project is licensed under the MIT License - see the LICENSE file for details.

