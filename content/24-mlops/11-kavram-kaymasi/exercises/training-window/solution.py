def training_window(rows, current_month, size):
    return [r for r in rows if current_month - size < r["month"] <= current_month]


rows = [{"month": m, "id": i} for i, m in enumerate([0, 1, 2, 3, 4, 5, 5])]
print(len(training_window(rows, 5, 2)))
print([r["month"] for r in training_window(rows, 3, 2)])
print(training_window(rows, 5, 0))
