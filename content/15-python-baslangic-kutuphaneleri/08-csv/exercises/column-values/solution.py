import csv


def column_values(path, column):
    with open(path, newline="", encoding="utf-8") as f:
        return [row[column] for row in csv.DictReader(f)]

for city in column_values("sales.csv", "city"):
    print(city)
