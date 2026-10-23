students = {
    "Hermione": "Gryffindor",
    "Harry": "Gryffindor",
    "Ron": "Gryffindor",
    "Draco": "Slytherin",
    "Luna": "Ravenclaw",
    "Cedric": "Hufflepuff",
    "Cho": "Ravenclaw",
}

house = input("House: ").strip().title()
count = 0
for student in students:
    if students[student] == house:
        print(student)
        count += 1
print(f"{count} students")
