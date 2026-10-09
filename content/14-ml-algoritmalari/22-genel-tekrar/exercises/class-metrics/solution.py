def class_metrics(y_true, y_pred):
    pairs = list(zip(y_true, y_pred))
    tp = sum(1 for t, p in pairs if t == 1 and p == 1)
    fp = sum(1 for t, p in pairs if t == 0 and p == 1)
    fn = sum(1 for t, p in pairs if t == 1 and p == 0)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    total = precision + recall
    f1 = 2 * precision * recall / total if total else 0.0
    return round(precision, 3), round(recall, 3), round(f1, 3)

print(class_metrics([1, 0, 1, 1, 0, 0, 1], [1, 0, 0, 1, 1, 0, 1]))
print(class_metrics([0, 0, 1], [0, 0, 0]))
