from pathlib import Path


def csv_rows(folder):
    base = Path(folder)
    rows = {}
    for path in base.rglob("*.csv"):
        lines = path.read_text(encoding="utf-8").splitlines()
        rows[path.relative_to(base).as_posix()] = len(lines) - 1
    return rows

rows = csv_rows("shop")
for name in sorted(rows):
    print(name, rows[name])
