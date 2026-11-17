from sklearn.metrics import f1_score


def macro_f1(y_true, y_pred, k):
    return 0.0

y_true = [0, 0, 0, 0, 0, 0, 1, 1, 2, 2]
y_pred = [0, 0, 0, 0, 0, 1, 1, 0, 2, 1]
print(macro_f1(y_true, y_pred, 3))
print(round(f1_score(y_true, y_pred, average="macro"), 3))
