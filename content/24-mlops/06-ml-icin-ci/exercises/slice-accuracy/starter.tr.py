def slice_accuracy(rows, predictions, column):
    # Satir ve tahmini birlikte gez, gruplara ayir, her grubun dogrulugunu hesapla.
    pass


rows = [
    {"plan": "pro", "churned": 1}, {"plan": "basic", "churned": 0},
    {"plan": "pro", "churned": 0}, {"plan": "basic", "churned": 1},
    {"plan": "pro", "churned": 1}, {"plan": "basic", "churned": 0},
]
predictions = [1, 0, 1, 0, 1, 0]
for value, accuracy in slice_accuracy(rows, predictions, "plan"):
    print(value, accuracy)
