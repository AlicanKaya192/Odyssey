def mean_by_param(runs, param, metric):
    # Degerleri grupla, her grubun ortalamasini al.
    pass


runs = [
    {"run": 1, "params": {"max_depth": 3, "seed": 0}, "metrics": {"val_accuracy": 0.78}},
    {"run": 2, "params": {"max_depth": 5, "seed": 0}, "metrics": {"val_accuracy": 0.81}},
    {"run": 3, "params": {"max_depth": 3, "seed": 1}, "metrics": {"val_accuracy": 0.79}},
    {"run": 4, "params": {"max_depth": 5, "seed": 1}, "metrics": {"val_accuracy": 0.82}},
    {"run": 5, "params": {"C": 1}, "metrics": {"val_accuracy": 0.83}},
]
for value, mean in mean_by_param(runs, "max_depth", "val_accuracy"):
    print("max_depth", value, mean)
