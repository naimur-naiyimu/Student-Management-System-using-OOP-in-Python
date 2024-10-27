import json

class Person:
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address

    def display_person_info(self):
        print(f"Name: {self.name}, Age: {self.age}, Address: {self.address}")

class Student(Person):
    def __init__(self, name, age, address, student_id):
        super().__init__(name, age, address)
        self.student_id = student_id
        self.grades = {}
        self.courses = []

    def add_grade(self, subject, grade):
        self.grades[subject] = grade

    def enroll_course(self, course):
        if course not in self.courses:
            self.courses.append(course)

    def display_student_info(self):
        self.display_person_info()
        print(f"Student ID: {self.student_id}")
        print("Courses Enrolled:", ", ".join(self.courses))
        print("Grades:", self.grades)

class Course:
    def __init__(self, course_name, course_code, instructor):
        self.course_name = course_name
        self.course_code = course_code
        self.instructor = instructor
        self.students = []

    def add_student(self, student):
        if student not in self.students:
            self.students.append(student)

    def display_course_info(self):
        print(f"Course Name: {self.course_name}, Course Code: {self.course_code}, Instructor: {self.instructor}")
        print("Enrolled Students:", ", ".join([student.student_id for student in self.students]))

class System:
    def __init__(self):
        self.students = {}
        self.courses = {}

    def add_student(self, name, age, address, student_id):
        if student_id in self.students:
            print("Student ID already exists.")
            return
        student = Student(name, age, address, student_id)
        self.students[student_id] = student
        print("Student added successfully.")

    def enroll_in_course(self, student_id, course_code):
        if student_id not in self.students:
            print("Student ID does not exist.")
            return
        if course_code not in self.courses:
            print("Course code does not exist.")
            return
        student = self.students[student_id]
        course = self.courses[course_code]
        student.enroll_course(course_code)
        course.add_student(student)
        print("Student enrolled in course successfully.")

    def add_grade(self, student_id, course_code, grade):
        if student_id not in self.students:
            print("Student ID does not exist.")
            return
        if course_code not in self.courses:
            print("Course code does not exist.")
            return
        student = self.students[student_id]
        if course_code not in student.courses:
            print("Student is not enrolled in the course.")
            return
        student.add_grade(course_code, grade)
        print("Grade added successfully.")

    def display_student_details(self, student_id):
        if student_id not in self.students:
            print("Student ID does not exist.")
            return
        student = self.students[student_id]
        student.display_student_info()

    def display_course_details(self, course_code):
        if course_code not in self.courses:
            print("Course code does not exist.")
            return
        course = self.courses[course_code]
        course.display_course_info()

    def save_data(self, filename):
        data = {
            "students": {sid: vars(student) for sid, student in self.students.items()},
            "courses": {cc: vars(course) for cc, course in self.courses.items()}
        }
        with open(filename, 'w') as file:
            json.dump(data, file)
        print("Data saved successfully.")

    def load_data(self, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
            self.students = {sid: Student(**student) for sid, student in data["students"].items()}
            self.courses = {cc: Course(**course) for cc, course in data["courses"].items()}
            print("Data loaded successfully.")
        except FileNotFoundError:
            print("Data file not found.")

def main():
    system = System()
    while True:
        print("\nMenu:")
        print("1. Add Student")
        print("2. Enroll in Course")
        print("3. Add Grade")
        print("4. Display Student Details")
        print("5. Display Course Details")
        print("6. Save Data")
        print("7. Load Data")
        print("8. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter name: ")
            age = int(input("Enter age: "))
            address = input("Enter address: ")
            student_id = input("Enter student ID: ")
            system.add_student(name, age, address, student_id)
        elif choice == '2':
            student_id = input("Enter student ID: ")
            course_code = input("Enter course code: ")
            system.enroll_in_course(student_id, course_code)
        elif choice == '3':
            student_id = input("Enter student ID: ")
            course_code = input("Enter course code: ")
            grade = input("Enter grade: ")
            system.add_grade(student_id, course_code, grade)
        elif choice == '4':
            student_id = input("Enter student ID: ")
            system.display_student_details(student_id)
        elif choice == '5':
            course_code = input("Enter course code: ")
            system.display_course_details(course_code)
        elif choice == '6':
            filename = input("Enter filename to save data: ")
            system.save_data(filename)
        elif choice == '7':
            filename = input("Enter filename to load data: ")
            system.load_data(filename)
        elif choice == '8':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()