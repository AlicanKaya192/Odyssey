import csv


def total_by(path, key, value):
    totals = {}
    # DictReader ile oku, float'a cevir, topla
    return totals

totals = total_by("sales.csv", "customer", "amount")
for name in sorted(totals):
    print(name, totals[name])
