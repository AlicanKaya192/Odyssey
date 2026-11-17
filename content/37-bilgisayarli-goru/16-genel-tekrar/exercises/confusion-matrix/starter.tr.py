def confusion(predicted, truth, n):
    return []

truth = [0, 0, 1, 1, 2, 2]
predicted = [0, 1, 1, 1, 2, 0]
for row in confusion(predicted, truth, 3):
    print(row)
