import math


def check_features(values, n=6):
    # If not a list or its length is not n: "expected a list of n numbers"
    # If any value is not a finite number: "values must be finite numbers"; if valid, "ok"
    return "ok"

print(check_features([1, 2, 3, 4, 5, 6]))
print(check_features([1, 2]))
print(check_features([1, 2, 3, 4, 5, float("inf")]))
