def gini(labels):
    n = len(labels)
    return 1 - sum((labels.count(c) / n) ** 2 for c in set(labels))


def best_split(x, y):
    values = sorted(set(x))
    best = None
    for a, b in zip(values, values[1:]):
        t = (a + b) / 2
        left = [c for v, c in zip(x, y) if v <= t]
        right = [c for v, c in zip(x, y) if v > t]
        score = (len(left) * gini(left) + len(right) * gini(right)) / len(y)
        if best is None or score < best[1] - 1e-12:
            best = (t, score)
    return best[0], round(best[1], 3)

x = [1, 2, 3, 4, 5, 6]
y = [0, 0, 0, 1, 1, 1]
print(best_split(x, y))
print(best_split([1, 2, 3, 4], [0, 1, 0, 1]))
