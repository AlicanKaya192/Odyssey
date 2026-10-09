def gini(labels):
    n = len(labels)
    return 1 - sum((labels.count(c) / n) ** 2 for c in set(labels))


def best_split(x, y):
    values = sorted(set(x))
    best = None
    # Midpoints, weighted gini
    return best

x = [1, 2, 3, 4, 5, 6]
y = [0, 0, 0, 1, 1, 1]
print(best_split(x, y))
print(best_split([1, 2, 3, 4], [0, 1, 0, 1]))
