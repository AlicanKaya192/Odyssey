from collections import Counter


def top_confusions(y_true, y_pred, k):
    return []

y_true = ["a", "a", "b", "b", "c", "c", "c"]
y_pred = ["a", "b", "a", "c", "b", "b", "c"]
print(top_confusions(y_true, y_pred, 2))
