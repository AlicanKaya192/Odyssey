def precision_recall(matrix, c):
    return [0.0, 0.0]

matrix = [[5, 1, 0], [1, 1, 0], [0, 1, 1]]
for c in range(3):
    print(c, precision_recall(matrix, c))
print(precision_recall([[2, 0], [3, 0]], 1))
