def confusion(y_true, y_pred, labels):
    pairs = list(zip(y_true, y_pred))
    return [[pairs.count((t, p)) for p in labels] for t in labels]

y_true = ["a", "a", "b", "b", "b", "c"]
y_pred = ["a", "b", "b", "b", "c", "c"]
for row in confusion(y_true, y_pred, ["a", "b", "c"]):
    print(row)
