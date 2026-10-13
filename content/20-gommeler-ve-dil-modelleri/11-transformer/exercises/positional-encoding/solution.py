import math


def positional_encoding(n, d):
    rows = []
    for pos in range(n):
        row = []
        for i in range(0, d, 2):
            angle = pos / 10000 ** (i / d)
            row += [round(math.sin(angle), 3), round(math.cos(angle), 3)]
        rows.append(row)
    return rows

for row in positional_encoding(3, 4):
    print(row)
