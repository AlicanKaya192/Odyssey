def expected_table(table):
    return [[float(v) for v in row] for row in table]


for row in expected_table([[782, 126], [1633, 157], [268, 34]]):
    print(row)
