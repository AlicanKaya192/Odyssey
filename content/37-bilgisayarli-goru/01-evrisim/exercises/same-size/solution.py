import torch
import torch.nn.functional as F


def same_size(img, kernel):
    x = torch.tensor(img, dtype=torch.float32)[None, None]
    w = torch.tensor(kernel, dtype=torch.float32)[None, None]
    out = F.conv2d(x, w, padding=len(kernel) // 2)
    return out[0, 0].int().tolist()

img = [[0, 0, 0, 0], [0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]]
for row in same_size(img, [[1, 1, 1], [1, 1, 1], [1, 1, 1]]):
    print(row)
