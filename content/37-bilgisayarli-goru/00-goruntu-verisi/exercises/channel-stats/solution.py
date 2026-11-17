import torch


def channel_stats(batch):
    x = torch.tensor(batch)
    means = x.mean(dim=(0, 2, 3)).tolist()
    stds = x.std(dim=(0, 2, 3)).tolist()
    return [round(m, 3) for m in means], [round(s, 3) for s in stds]

batch = [[[[0.0, 1.0]], [[0.5, 0.5]]], [[[1.0, 1.0]], [[0.5, 0.5]]]]
means, stds = channel_stats(batch)
print(means)
print(stds)
