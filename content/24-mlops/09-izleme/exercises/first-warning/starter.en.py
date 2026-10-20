def first_warning(signals):
    # Go month by month; if any signal fired that month, return it with the names.
    pass


signals = {
    "accuracy": [False, False, False, False, True, True],
    "predicted_rate": [False, False, True, True, True, True],
    "usage_mean": [False, False, True, True, True, True],
}
print(first_warning(signals))
print(first_warning({"accuracy": [False, False]}))
