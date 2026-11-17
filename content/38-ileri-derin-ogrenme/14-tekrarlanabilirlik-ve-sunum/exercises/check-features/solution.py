import math


def check_features(values, n=6):
    if not isinstance(values, list) or len(values) != n:
        return f"expected a list of {n} numbers"
    if not all(isinstance(v, (int, float)) and math.isfinite(v) for v in values):
        return "values must be finite numbers"
    return "ok"

print(check_features([1, 2, 3, 4, 5, 6]))
print(check_features([1, 2]))
print(check_features([1, 2, 3, 4, 5, float("inf")]))
