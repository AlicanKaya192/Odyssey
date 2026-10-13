def averaging(id_lists, V):
    rows = []
    for ids in id_lists:
        row = [0.0] * V
        for i in ids:
            row[i] += 1 / len(ids)
        rows.append([round(x, 3) for x in row])
    return rows

for row in averaging([[1, 2], [3, 3, 0]], 4):
    print(row)
