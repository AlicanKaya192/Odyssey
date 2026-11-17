import torch
import torch.nn.functional as F


def pad_crop(img, padding, top, left):
    return []

img = [[1, 2], [3, 4]]
print(pad_crop(img, 1, 0, 0))
print(pad_crop(img, 1, 1, 1))
print(pad_crop(img, 1, 2, 2))
