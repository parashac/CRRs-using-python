class Student:
    def __init__(self, student_id, name, email, phone):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.phone = phone

    def display(self):
        print(self.student_id,
              self.name,
              self.email,
              self.phone
              )
    def update_info(self, email, phone):
        self.email = email
        self.phone = phone


class Course:
    def __init__(self, course_id, title, credit_points):
        self.course_id = course_id
        self.title = title
        self.credit_points = credit_points

    def display(self):
        print(self.course_id, self.title, self.credit_points)

class Enrollment:
    def __init__(self, enrollment_id, student_id, course_id):
        self.enrollment_id = enrollment_id
        self.student_id = student_id
        self.course_id = course_id

    def display(self):
        print(self.enrollment_id, self.student_id, self.course_id)

class Result:
    def __init__(self, result_id, enrollment_id, score):
        self.result_id = result_id
        self.enrollment_id = enrollment_id
        self.score = score
        self.grade = self.calculate_grade()
    def calculate_grade(self):

        if self.score >=80:
            return "HD"
        elif self.score >=70:
            return "D"
        elif self.score >=60:
            return "CD"
        elif self.score >=50:
            return "P"
        else:
            return "F"

class CRRS_manager: ###main class inheritence
    def __init__(self):
        self.student =[]
        self.course = []
        self.enrollment = []
        self.results = []
        self.load_files()

    def load_files(self):
        try:
            with open("students.txt", "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    std = line.split(",")
                    if len(std) == 4:
                        self.student.append(Student(*std))
        except FileNotFoundError:
            pass

        try:
            with open("courses.txt","r") as f:
                for line in f:
                    c = line.strip().split(",")

                    self.course.append(Course(c[0], c[1], int(c[2])))

        except FileNotFoundError:
            pass

        try:
            with open("enrollment.txt", "r") as f:
                for line in f:
                    enroll = line.strip().split(",")
                    self.enrollment.append(Enrollment(*enroll))
        except FileNotFoundError:
            pass

        try:
            with open("results.txt", "r") as f:
                for line in f:
                    r = line.strip().split(",")

                    self.results.append(Result(r[0], r[1], int(r[2])))
        except FileNotFoundError:
            pass

    def log(self, message):
        with open("system_log.txt", "a") as f:
            f.write(message + "\n")

    def add_student(self):
        sid = input("Enter student id: ")
        for s in self.student:
            if s.student_id == sid:
                print("Student ID already exists")
                return
        name = input("Enter Name: ")
        email = input("Enter email: ")
        phone = input("Enter phone: ")
        self.student.append(Student(sid, name, email, phone))

        with open("students.txt", "a") as f:
            f.write(f"student_id: {sid}, student_name: {name}, email: {email}, phone: {phone}\n")

        self.log("student added successfully")
        print("Student added successfully.")
        print("------------------------------------------------------------------------------------------------------------------------")

    def view_students(self):
        if not self.student:
            print("No students found.")
            return

        print("<<<<<<<<Student Details>>>>>>>>")
        for s in self.student:
            s.display()
            print("------------------------------------------------------------------------------------------------------------------------")

    def add_course(self):
        cid = input("Course ID: ")
        title = input("Title: ")
        credit = int(input("Credit Points: "))
        self.course.append(Course(cid, title, credit))

        with open("courses.txt", "a") as f:
            f.write(f"course_id: {cid},title: {title}, credit_hours: {credit}\n")


        self.log("Course added successfully")
        print("Course added successfully.")
        print("------------------------------------------------------------------------------------------------------------------------")

    def enroll_student(self):
        print("<<<<<<<Available Courses:>>>>>>>>")
        for c in self.course:
            c.display()
        eid = input("Enrollment ID: ")
        sid = input("Student ID: ")
        cid = input("Course ID: ")

        for e in self.enrollment:
            if e.student_id == sid and e.course_id == cid:
                print("Already enrolled in this course")
                return

        self.enrollment.append(Enrollment(eid, sid, cid))

        with open("enrollment.txt", "a") as f:
            f.write(f"enroll_id: {eid}, student_id: {sid}, course_id: {cid}\n")

        self.log("Student enrolled successfully")
        print("Student enrolled successfully.\n")
        print("------------------------------------------------------------------------------------------------------------------------")

    def add_result(self):
        rid = input("Result ID: ")
        eid = input("Enrollment ID: ")
        score = int(input("Score (0-100): "))

        if score < 0 or score > 100:
            print("Invalid score")
            return

        result = Result(rid, eid, score)
        self.results.append(result)

        with open("results.txt", "a") as f:
            f.write(f"result_id: {rid},enroll_id: {eid}, score: {score}, grade: {result.grade}\n")

        self.log("Result added successfully")
        print("Result added successfully.")
        print("------------------------------------------------------------------------------------------------------------------------")

    def update_student(self):
        sid = input("Enter Student ID to update: ")
        for s in self.student:
            if s.student_id == sid:
                email = input("New email: ")
                phone = input("New phone: ")
                s.update_info(email, phone)
                print("Student info updated")
                self.log(f"Student {sid} updated")
                return
        print("Student not found")

    def update_course(self):
        cid = input("Enter Course ID to update: ")
        for c in self.course:
            if c.course_id == cid:
                title = input("New title: ")
                credit = int(input("New credit points: "))
                c.title = title
                c.credit_points = credit
                print("Course info updated")
                self.log(f"Course {cid} updated")
                return
        print("Course not found")
    def view_transcript(self):
        sid = input("Student ID: ")
        print("Transcript:")
        for e in self.enrollment:
            if e.student_id == sid:
                for r in self.results:
                    if r.enrollment_id == e.enrollment_id:
                        print(f"Course_id: {e.course_id}, Score: {r.score}, Grade: {r.grade}")
                        print("------------------------------------------------------------------------------------------------------------------------")

    def menu(self):
        while True:
            print("<<<<<<<MENU>>>>>>>")
            print("\n1.Add Student\n2.Add Course\n3.Enroll Student\n4.Add Result")
            print("5.View Transcript\n6.View Courses\n7.View Students\n8.Update student\n9.Update course\n10.View Enrollments\n11.Exit")

            choice = input("Enter your Choice: ")

            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.add_course()
            elif choice == "3":
                self.enroll_student()
            elif choice == "4":
                self.add_result()
            elif choice == "5":
                self.view_transcript()
            elif choice == "6":
                for c in self.course:
                    c.display()
            elif choice == "7":
                self.view_students()
            elif choice == "8":
                self.update_student()
            elif choice == "9":
                self.update_course()
            elif choice == "10":
                for e in self.enrollment:
                    e.display()
            elif choice == "11":
                print("Exiting...")
                break
            else:
                print("Invalid choice")

system = CRRS_manager()
system.menu()







