def class_accuracy(matrix):
    result = []
    for i, row in enumerate(matrix):
        total = sum(row)
        result.append(round(100 * row[i] / total, 1) if total else 0.0)
    return result

print(class_accuracy([[3, 1], [0, 2]]))
