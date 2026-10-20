def best_run(runs, metric):
    # Olcumu olmayanlari atla, en yuksegi bul, numarasini dondur.
    pass


RUNS = [
    {"run": 1, "params": {"model": "baseline"}, "metrics": {"val_accuracy": 0.75}},
    {"run": 2, "params": {"model": "logistic", "C": 1},
     "metrics": {"val_accuracy": 0.83, "val_f1": 0.61}},
    {"run": 3, "params": {"model": "forest", "max_depth": 5},
     "metrics": {"val_accuracy": 0.81, "val_f1": 0.64}},
    {"run": 4, "params": {"model": "logistic", "C": 10},
     "metrics": {"val_accuracy": 0.83, "val_f1": 0.6}},
    {"run": 5, "params": {"model": "forest", "max_depth": 8},
     "metrics": {"val_accuracy": 0.8, "val_f1": 0.62}},
]
print(best_run(RUNS, "val_accuracy"))
print(best_run(RUNS, "val_f1"))
print(best_run(RUNS, "test_accuracy"))
