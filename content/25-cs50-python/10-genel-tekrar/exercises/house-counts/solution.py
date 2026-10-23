import csv
import sys


def main():
    if len(sys.argv) < 2:
        sys.exit("Too few command-line arguments")
    if len(sys.argv) > 2:
        sys.exit("Too many command-line arguments")
    if not sys.argv[1].endswith(".csv"):
        sys.exit("Not a CSV file")
    try:
        print_counts(sys.argv[1])
    except FileNotFoundError:
        sys.exit("File does not exist")


def print_counts(path):
    counts = {}
    with open(path) as file:
        for row in csv.DictReader(file):
            counts[row["house"]] = counts.get(row["house"], 0) + 1
    for house in sorted(counts):
        print(f"{house}: {counts[house]}")


if __name__ == "__main__":
    main()
