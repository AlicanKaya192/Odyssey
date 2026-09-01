class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def is_passing(self):
        return self.grade >= 50


class Course:
    def __init__(self, title):
        self.title = title
        self.students = []

    def enrol(self, student):
        self.students.append(student)
        return len(self.students)

    def passing_names(self):
        names = []
        for student in self.students:
            if student.is_passing():
                names.append(student.name)
        return names


course = Course("Python")
course.enrol(Student("Ada", 90))
course.enrol(Student("Brian", 40))
total = course.enrol(Student("Grace", 75))

print(total)
print(course.passing_names())
