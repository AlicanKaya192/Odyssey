from pathlib import Path


def csv_rows(folder):
    rows = {}
    # for path in Path(folder).rglob("*.csv"):
    return rows

rows = csv_rows("shop")
for name in sorted(rows):
    print(name, rows[name])
