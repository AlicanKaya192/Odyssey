grades = {"Ada": "A", "Alan": "B", "Grace": "A", "Linus": "C", "Guido": "B", "Ken": "A"}

by_grade = {}
for name in grades:
    grade = grades[name]
    if grade not in by_grade:
        by_grade[grade] = []
    by_grade[grade].append(name)

for grade in sorted(by_grade):
    print(grade + ":", by_grade[grade])
