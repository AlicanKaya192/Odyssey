import csv
import os

with open("data/sample.csv", encoding="utf-8") as handle:
    rows = list(csv.DictReader(handle))
print("rows:", len(rows))
print("data files:", sorted(os.listdir("data")))
