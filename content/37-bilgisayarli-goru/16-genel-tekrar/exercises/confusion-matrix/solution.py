def confusion(predicted, truth, n):
    matrix = [[0] * n for _ in range(n)]
    for p, t in zip(predicted, truth):
        matrix[t][p] += 1
    return matrix

truth = [0, 0, 1, 1, 2, 2]
predicted = [0, 1, 1, 1, 2, 0]
for row in confusion(predicted, truth, 3):
    print(row)
