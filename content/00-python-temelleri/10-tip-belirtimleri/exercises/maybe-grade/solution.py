def find_grade(name: str) -> int | None:
    grades = {"Ada": 90, "Alan": 70}
    if name in grades:
        return grades[name]
    return None


for person in ["Ada", "Grace"]:
    grade = find_grade(person)
    if grade is None:
        print(person, "not found")
    else:
        print(person, grade)
