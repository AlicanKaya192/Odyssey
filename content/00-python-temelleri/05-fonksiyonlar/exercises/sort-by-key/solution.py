people = [
    {"name": "Grace", "grade": 75},
    {"name": "Ada", "grade": 90},
    {"name": "Brian", "grade": 40},
]


def by_grade(person):
    return person["grade"]


best_first = sorted(people, key=by_grade, reverse=True)

names = []
for person in best_first:
    names.append(person["name"])

alphabetical = sorted(names)

print(names)
print(alphabetical)
