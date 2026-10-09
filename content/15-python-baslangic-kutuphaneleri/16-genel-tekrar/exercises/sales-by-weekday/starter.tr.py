import csv
from collections import defaultdict
from datetime import date

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def sales_by_weekday(path):
    totals = defaultdict(float)
    # DictReader, weekday(), DAYS[...]
    return {}

totals = sales_by_weekday("sales.csv")
for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
    if day in totals:
        print(day, totals[day])
