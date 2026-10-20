def slice_accuracy(rows, predictions, column):
    # Walk rows and predictions together, group them, compute each group's accuracy.
    pass


rows = [
    {"plan": "pro", "churned": 1}, {"plan": "basic", "churned": 0},
    {"plan": "pro", "churned": 0}, {"plan": "basic", "churned": 1},
    {"plan": "pro", "churned": 1}, {"plan": "basic", "churned": 0},
]
predictions = [1, 0, 1, 0, 1, 0]
for value, accuracy in slice_accuracy(rows, predictions, "plan"):
    print(value, accuracy)
