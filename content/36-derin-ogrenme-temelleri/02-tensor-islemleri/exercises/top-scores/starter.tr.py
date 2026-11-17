import torch


def top(scores):
    return [[], []]

scores = [[0.5, 2.0, 1.0], [3.0, 0.25, 0.75], [1.0, 1.5, 4.0]]
print(top(scores))
