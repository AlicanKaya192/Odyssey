def confusion(preds, labels, k):
    matrix = [[0] * k for _ in range(k)]
    return matrix

for row in confusion([0, 1, 1, 2, 2, 0], [0, 1, 2, 2, 1, 0], 3):
    print(row)
