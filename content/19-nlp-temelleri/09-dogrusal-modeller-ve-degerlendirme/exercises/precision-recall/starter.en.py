def prf(y_true, y_pred, label):
    return [0.0, 0.0, 0.0]

y_true = ["neg", "neg", "neg", "pos", "pos", "pos", "pos"]
y_pred = ["neg", "pos", "pos", "pos", "pos", "pos", "neg"]
print(prf(y_true, y_pred, "neg"))
print(prf(y_true, y_pred, "pos"))
