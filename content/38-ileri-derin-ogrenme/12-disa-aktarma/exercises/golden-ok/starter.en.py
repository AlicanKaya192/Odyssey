import torch


def golden_ok(expected, actual, atol):
    # Write your code here
    return False

print(golden_ok([[1.0, 2.0]], [[1.0, 2.000001]], 1e-5))
print(golden_ok([[1.0, 2.0]], [[1.0, 2.1]], 1e-5))
