import csv
import sys

from tabulate import tabulate

if len(sys.argv) < 2:
    sys.exit("Too few command-line arguments")
if len(sys.argv) > 2:
    sys.exit("Too many command-line arguments")
if not sys.argv[1].endswith(".csv"):
    sys.exit("Not a CSV file")

try:
    with open(sys.argv[1]) as file:
        menu = list(csv.DictReader(file))
except FileNotFoundError:
    sys.exit("File does not exist")

print(tabulate(menu, headers="keys", tablefmt="grid"))
