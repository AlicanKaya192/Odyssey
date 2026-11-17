def precision_recall(matrix, c):
    correct = matrix[c][c]
    column = sum(row[c] for row in matrix)
    row = sum(matrix[c])
    precision = correct / column if column else 0.0
    recall = correct / row if row else 0.0
    return [round(precision, 3), round(recall, 3)]

matrix = [[5, 1, 0], [1, 1, 0], [0, 1, 1]]
for c in range(3):
    print(c, precision_recall(matrix, c))
print(precision_recall([[2, 0], [3, 0]], 1))
