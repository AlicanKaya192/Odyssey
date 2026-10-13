from collections import Counter


def top_confusions(y_true, y_pred, k):
    errors = Counter((t, p) for t, p in zip(y_true, y_pred) if t != p)
    ranked = sorted(errors.items(), key=lambda item: (-item[1], item[0]))
    return [[t, p, n] for (t, p), n in ranked[:k]]

y_true = ["a", "a", "b", "b", "c", "c", "c"]
y_pred = ["a", "b", "a", "c", "b", "b", "c"]
print(top_confusions(y_true, y_pred, 2))
