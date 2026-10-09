import csv


def filter_rows(src, dst, column, minimum):
    count = 0
    with open(src, newline="", encoding="utf-8") as fin, \
            open(dst, "w", newline="", encoding="utf-8") as fout:
        reader = csv.DictReader(fin)
        writer = csv.DictWriter(fout, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in reader:
            if float(row[column]) >= minimum:
                writer.writerow(row)
                count += 1
    return count

print(filter_rows("sales.csv", "big.csv", "amount", 100))
print(open("big.csv", encoding="utf-8").read())
