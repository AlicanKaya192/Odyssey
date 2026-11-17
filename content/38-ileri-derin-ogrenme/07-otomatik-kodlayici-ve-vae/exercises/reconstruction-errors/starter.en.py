import torch


def reconstruction_errors(original, rebuilt):
    # Write your code here
    return []

original = [[1.0, 0.0, 1.0, 0.0], [0.5, 0.5, 0.5, 0.5]]
rebuilt = [[1.0, 0.0, 0.0, 0.0], [0.5, 0.5, 0.5, 0.5]]
print(reconstruction_errors(original, rebuilt))
