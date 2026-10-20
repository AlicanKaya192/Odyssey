def compare_runs(a, b):
    changed = []
    for key in ["config", "data", "library"]:
        if a[key] != b[key]:
            changed.append(key)
    if changed:
        return "changed: " + ", ".join(changed)
    if a["accuracy"] == b["accuracy"]:
        return "reproducible"
    return "not reproducible"


a = {"config": {"seed": 0}, "data": "d1", "library": "1.9.1", "accuracy": 0.77}
print(compare_runs(a, dict(a)))
print(compare_runs(a, {**a, "accuracy": 0.75}))
print(compare_runs(a, {**a, "data": "d2", "accuracy": 0.75}))
print(compare_runs(a, {**a, "config": {"seed": 1}, "library": "1.8.0"}))
