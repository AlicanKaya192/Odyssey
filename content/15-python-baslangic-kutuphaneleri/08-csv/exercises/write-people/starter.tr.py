import csv


def write_people(path, people):
    with open(path, "w", encoding="utf-8") as f:
        for person in people:
            f.write(",".join(person.values()) + "\n")
    with open(path, encoding="utf-8") as f:
        return f.read().splitlines()

people = [{"name": "Ada", "city": "London, UK"}, {"name": "Alan", "city": "Wilmslow"}]
for line in write_people("out.csv", people):
    print(line)
