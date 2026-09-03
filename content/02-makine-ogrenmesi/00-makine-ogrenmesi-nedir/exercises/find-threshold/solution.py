scores = [35, 48, 52, 60, 66, 71, 78, 85, 90, 95]
passed = [0, 0, 0, 1, 0, 1, 1, 1, 1, 1]

best_t, best_acc = None, -1.0

for t in range(30, 101, 5):
    prediction = [1 if s >= t else 0 for s in scores]
    correct = sum(1 for a, b in zip(prediction, passed) if a == b)
    acc = correct / len(passed)
    if acc > best_acc:
        best_t, best_acc = t, acc

print(best_t, round(best_acc, 2))
