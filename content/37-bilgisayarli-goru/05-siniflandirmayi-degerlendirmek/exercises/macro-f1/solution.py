from sklearn.metrics import f1_score


def macro_f1(y_true, y_pred, k):
    scores = []
    for c in range(k):
        tp = sum(1 for t, p in zip(y_true, y_pred) if t == c and p == c)
        predicted = sum(1 for p in y_pred if p == c)
        actual = sum(1 for t in y_true if t == c)
        precision = tp / predicted if predicted else 0.0
        recall = tp / actual if actual else 0.0
        both = precision + recall
        scores.append(2 * precision * recall / both if both else 0.0)
    return round(sum(scores) / k, 3)

y_true = [0, 0, 0, 0, 0, 0, 1, 1, 2, 2]
y_pred = [0, 0, 0, 0, 0, 1, 1, 0, 2, 1]
print(macro_f1(y_true, y_pred, 3))
print(round(f1_score(y_true, y_pred, average="macro"), 3))
