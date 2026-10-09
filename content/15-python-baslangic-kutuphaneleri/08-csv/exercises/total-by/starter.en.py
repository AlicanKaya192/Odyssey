import csv


def total_by(path, key, value):
    totals = {}
    # read with DictReader, convert to float, add up
    return totals

totals = total_by("sales.csv", "customer", "amount")
for name in sorted(totals):
    print(name, totals[name])
