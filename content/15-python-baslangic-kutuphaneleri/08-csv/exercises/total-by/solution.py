import csv


def total_by(path, key, value):
    totals = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            name = row[key]
            totals[name] = totals.get(name, 0) + float(row[value])
    return {name: round(total, 2) for name, total in totals.items()}

totals = total_by("sales.csv", "customer", "amount")
for name in sorted(totals):
    print(name, totals[name])
