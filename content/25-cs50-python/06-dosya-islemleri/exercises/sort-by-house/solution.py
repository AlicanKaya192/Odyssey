import csv

students = []

with open("students.csv") as file:
    for row in csv.DictReader(file):
        students.append(row)

for student in sorted(students, key=lambda student: student["house"]):
    print(f"{student['name']} is in {student['house']}")
