import csv


def write_people(path, people):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(people[0]))
        writer.writeheader()
        writer.writerows(people)
    with open(path, encoding="utf-8") as f:
        return f.read().splitlines()

people = [{"name": "Ada", "city": "London, UK"}, {"name": "Alan", "city": "Wilmslow"}]
for line in write_people("out.csv", people):
    print(line)
