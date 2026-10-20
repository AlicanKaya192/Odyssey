def compare_runs(a, b):
    # Once degisen girdileri bul, sonra dogruluga bak.
    pass


a = {"config": {"seed": 0}, "data": "d1", "library": "1.9.1", "accuracy": 0.77}
print(compare_runs(a, dict(a)))
print(compare_runs(a, {**a, "accuracy": 0.75}))
print(compare_runs(a, {**a, "data": "d2", "accuracy": 0.75}))
print(compare_runs(a, {**a, "config": {"seed": 1}, "library": "1.8.0"}))
