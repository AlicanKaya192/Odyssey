def class_metrics(y_true, y_pred):
    pairs = list(zip(y_true, y_pred))
    tp = sum(1 for t, p in pairs if t == 1 and p == 1)
    # fp, fn; then the three measures
    return 0.0, 0.0, 0.0

print(class_metrics([1, 0, 1, 1, 0, 0, 1], [1, 0, 0, 1, 1, 0, 1]))
print(class_metrics([0, 0, 1], [0, 0, 0]))
