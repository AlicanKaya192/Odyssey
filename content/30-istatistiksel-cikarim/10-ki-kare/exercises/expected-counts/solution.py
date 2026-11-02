def expected_table(table):
    rows = [sum(row) for row in table]
    cols = [sum(col) for col in zip(*table)]
    total = sum(rows)
    return [[round(r * c / total, 1) for c in cols] for r in rows]


for row in expected_table([[782, 126], [1633, 157], [268, 34]]):
    print(row)
