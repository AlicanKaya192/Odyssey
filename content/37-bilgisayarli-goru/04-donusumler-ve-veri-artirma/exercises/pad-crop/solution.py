import torch
import torch.nn.functional as F


def pad_crop(img, padding, top, left):
    x = torch.tensor(img)
    h, w = x.shape
    padded = F.pad(x, (padding, padding, padding, padding))
    return padded[top:top + h, left:left + w].tolist()

img = [[1, 2], [3, 4]]
print(pad_crop(img, 1, 0, 0))
print(pad_crop(img, 1, 1, 1))
print(pad_crop(img, 1, 2, 2))
