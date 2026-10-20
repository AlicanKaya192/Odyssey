def slice_accuracy(rows, predictions, column):
    groups = {}
    for row, predicted in zip(rows, predictions):
        groups.setdefault(row[column], []).append(predicted == row["churned"])
    return [[value, round(sum(hits) / len(hits), 3)] for value, hits in sorted(groups.items())]


rows = [
    {"plan": "pro", "churned": 1}, {"plan": "basic", "churned": 0},
    {"plan": "pro", "churned": 0}, {"plan": "basic", "churned": 1},
    {"plan": "pro", "churned": 1}, {"plan": "basic", "churned": 0},
]
predictions = [1, 0, 1, 0, 1, 0]
for value, accuracy in slice_accuracy(rows, predictions, "plan"):
    print(value, accuracy)
