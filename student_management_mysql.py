import mysql.connector

# Database connection class
class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="naim1234",
            database="student_management"
        )
        self.cursor = self.conn.cursor()
    

    def execute_query(self, query, params=None):
        self.cursor.execute(query, params or ())
        self.conn.commit()

    def fetch_query(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()

# Person class
class Person:
    def __init__(self, db, name, age, address):
        self.db = db
        self.name = name
        self.age = age
        self.address = address

    def save(self):
        query = "INSERT INTO person (name, age, address) VALUES (%s, %s, %s)"
        self.db.execute_query(query, (self.name, self.age, self.address))
        return self.db.cursor.lastrowid

# Student class inherits from Person
class Student(Person):
    def __init__(self, db, name, age, address, student_id):
        super().__init__(db, name, age, address)
        self.student_id = student_id

    def save(self):
        person_id = super().save()
        query = "INSERT INTO student (student_id, person_id) VALUES (%s, %s)"
        self.db.execute_query(query, (self.student_id, person_id))

# Course class
class Course:
    def __init__(self, db, course_code, course_name, instructor):
        self.db = db
        self.course_code = course_code
        self.course_name = course_name
        self.instructor = instructor

    def save(self):
        query = "INSERT INTO course (course_code, course_name, instructor) VALUES (%s, %s, %s)"
        self.db.execute_query(query, (self.course_code, self.course_name, self.instructor))

# Enrollment class for managing enrollments and grades
class Enrollment:
    def __init__(self, db):
        self.db = db

    def enroll_student(self, student_id, course_code):
        query = "INSERT INTO enrollment (student_id, course_code) VALUES (%s, %s)"
        self.db.execute_query(query, (student_id, course_code))

    def add_grade(self, student_id, course_code, grade):
        # Check if the course exists
        course_check_query = "SELECT course_code FROM course WHERE course_code = %s"
        course_exists = self.db.fetch_query(course_check_query, (course_code,))
        if not course_exists:
            print(f"Error: Course code '{course_code}' does not exist.")
            return

        # Check if the student is enrolled in the course
        enrollment_check_query = "SELECT * FROM enrollment WHERE student_id = %s AND course_code = %s"
        enrollment_exists = self.db.fetch_query(enrollment_check_query, (student_id, course_code))
        if not enrollment_exists:
            print(f"Error: Student {student_id} is not enrolled in course {course_code}.")
            return

        # Add or update grade
        query = """
        INSERT INTO grades (student_id, course_code, grade)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE grade = %s
        """
        self.db.execute_query(query, (student_id, course_code, grade, grade))
        print(f"Grade {grade} added for {student_id} in {course_code}.")

# Main CLI for the Student Management System
def main_menu():
    db = Database()
    try:
        while True:
            print("\n==== Student Management System ====")
            print("1. Add New Student")
            print("2. Add New Course")
            print("3. Enroll Student in Course")
            print("4. Add Grade for Student")
            print("5. Display Student Details")
            print("6. Display Course Details")
            print("7. Exit")
            choice = input("Select Option: ")

            if choice == '1':
                name = input("Enter Name: ")
                age = int(input("Enter Age: "))
                address = input("Enter Address: ")
                student_id = input("Enter Student ID: ")
                student = Student(db, name, age, address, student_id)
                student.save()
                print(f"Student {name} (ID: {student_id}) added successfully.")
            
            elif choice == '2':
                course_name = input("Enter Course Name: ")
                course_code = input("Enter Course Code: ")
                instructor = input("Enter Instructor Name: ")
                course = Course(db, course_code, course_name, instructor)
                course.save()
                print(f"Course {course_name} (Code: {course_code}) created with instructor {instructor}.")
            
            elif choice == '3':
                student_id = input("Enter Student ID: ")
                course_code = input("Enter Course Code: ")
                enrollment = Enrollment(db)
                enrollment.enroll_student(student_id, course_code)
                print(f"Student {student_id} enrolled in course {course_code}.")
            
            elif choice == '4':
                student_id = input("Enter Student ID: ")
                course_code = input("Enter Course Code: ")
                grade = input("Enter Grade: ")
                enrollment = Enrollment(db)
                enrollment.add_grade(student_id, course_code, grade)
                print(f"Grade {grade} added for {student_id} in {course_code}.")
            
            elif choice == '5':
                student_id = input("Enter Student ID: ")
                query = """
                SELECT person.name, student.student_id, person.age, person.address
                FROM student
                JOIN person ON student.person_id = person.id
                WHERE student.student_id = %s
                """
                student_info = db.fetch_query(query, (student_id,))
                if student_info:
                    name, student_id, age, address = student_info[0]
                    print(f"\nStudent Information:\nName: {name}\nID: {student_id}\nAge: {age}\nAddress: {address}")
                    
                    # Display Enrolled Courses and Grades
                    query = """
                    SELECT course.course_name, grades.grade
                    FROM enrollment
                    LEFT JOIN course ON enrollment.course_code = course.course_code
                    LEFT JOIN grades ON enrollment.student_id = grades.student_id AND enrollment.course_code = grades.course_code
                    WHERE enrollment.student_id = %s
                    """
                    courses = db.fetch_query(query, (student_id,))
                    print("Enrolled Courses and Grades:")
                    for course_name, grade in courses:
                        print(f"Course: {course_name}, Grade: {grade or 'Not Assigned'}")
                else:
                    print("Student not found.")
            
            elif choice == '6':
                course_code = input("Enter Course Code: ")
                query = """
                SELECT course.course_name, course.instructor
                FROM course
                WHERE course.course_code = %s
                """
                course_info = db.fetch_query(query, (course_code,))
                if course_info:
                    course_name, instructor = course_info[0]
                    print(f"\nCourse Information:\nCourse Name: {course_name}\nCode: {course_code}\nInstructor: {instructor}")
                    
                    # Display Enrolled Students
                    query = """
                    SELECT person.name
                    FROM enrollment
                    JOIN student ON enrollment.student_id = student.student_id
                    JOIN person ON student.person_id = person.id
                    WHERE enrollment.course_code = %s
                    """
                    students = db.fetch_query(query, (course_code,))
                    print("Enrolled Students:")
                    for student in students:
                        print(f"Student: {student[0]}")
                else:
                    print("Course not found.")
            
            elif choice == '7':
                print("Exiting Student Management System. Goodbye!")
                break

            else:
                print("Invalid option. Please try again.")

    finally:
        db.close()

if __name__ == "__main__":
    main_menu()
