import csv
from collections import defaultdict
from datetime import date

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def sales_by_weekday(path):
    totals = defaultdict(float)
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            day = DAYS[date.fromisoformat(row["date"]).weekday()]
            totals[day] += float(row["amount"])
    return {day: round(total, 2) for day, total in totals.items()}

totals = sales_by_weekday("sales.csv")
for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
    if day in totals:
        print(day, totals[day])
