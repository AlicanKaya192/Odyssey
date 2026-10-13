def dominant(weights, share):
    result = []
    for row in weights:
        total = sum(row)
        best = max(range(len(row)), key=lambda i: row[i])
        result.append(best if total and row[best] / total >= share else -1)
    return result

weights = [[0.8, 0.1, 0.1], [0.4, 0.35, 0.25], [0.0, 0.0, 0.0]]
print(dominant(weights, 0.5))
