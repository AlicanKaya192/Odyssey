def prf(y_true, y_pred, label):
    tp = sum(t == label and p == label for t, p in zip(y_true, y_pred))
    said = sum(p == label for p in y_pred)
    real = sum(t == label for t in y_true)
    precision = tp / said if said else 0.0
    recall = tp / real if real else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return [round(precision, 3), round(recall, 3), round(f1, 3)]


def macro_f1(y_true, y_pred):
    return 0.0

y_true = ["neg", "neg", "neu", "pos", "pos", "pos", "pos", "pos"]
y_pred = ["neg", "pos", "pos", "pos", "pos", "pos", "pos", "neg"]
print(macro_f1(y_true, y_pred))
