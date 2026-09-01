class Student:
    def __init__(self, name, grade, city):
        self.name = name
        self.grade = grade
        self.city = city

    def is_passing(self):
        return self.grade >= 50


def load_students(path: str) -> list[Student]:
    people = []
    with open(path, encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            name, grade, city = line.split(",")
            people.append(Student(name, int(grade), city))
    return people


students = load_students("students.txt")

by_city = {}
for student in students:
    if not student.is_passing():
        continue
    if student.city not in by_city:
        by_city[student.city] = []
    by_city[student.city].append(student.name)

best = ""
best_grade = 0
for student in students:
    if student.grade > best_grade:
        best_grade = student.grade
        best = student.name


print(len(students))
print(by_city)
print(best)
