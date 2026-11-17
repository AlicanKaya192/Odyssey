import torch


def channel_stats(batch):
    return [], []

batch = [[[[0.0, 1.0]], [[0.5, 0.5]]], [[[1.0, 1.0]], [[0.5, 0.5]]]]
means, stds = channel_stats(batch)
print(means)
print(stds)
