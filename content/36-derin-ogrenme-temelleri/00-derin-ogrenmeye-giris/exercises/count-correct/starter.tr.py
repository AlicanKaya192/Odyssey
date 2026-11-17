import torch


def count_correct(scores, labels):
    return 0

scores = [[0.1, 2.0, -1.0], [3.0, 0.5, 0.2], [0.0, 0.1, 0.9], [1.0, 1.5, 0.0]]
print(count_correct(scores, [1, 0, 0, 1]))
print(count_correct(scores, [2, 2, 2, 2]))
