def houses(students):
    names = set()
    for student in students:
        names.add(student["house"])
    return sorted(names)
