import torch
from dl_data import make_scenes


def class_weights(n, seed):
    images, boxes, masks = make_scenes(n, size=32, seed=seed)
    counts = torch.bincount(torch.tensor(masks).flatten(), minlength=4).float()
    weight = counts.sum() / (4 * counts)
    return [round(v, 2) for v in weight.tolist()]

print(class_weights(100, 7))
print(class_weights(50, 3))
