import torch
import torch.nn.functional as F


def global_pool(fmap):
    x = torch.tensor(fmap)[None]
    averages = F.adaptive_avg_pool2d(x, 1).flatten().tolist()
    maxima = F.adaptive_max_pool2d(x, 1).flatten().tolist()
    return [round(v, 3) for v in averages], [round(v, 3) for v in maxima]

fmap = [[[1.0, 2.0], [3.0, 4.0]], [[0.0, 0.0], [0.0, 8.0]]]
averages, maxima = global_pool(fmap)
print(averages)
print(maxima)
