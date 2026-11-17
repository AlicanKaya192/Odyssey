import torch
import torch.nn.functional as F


def same_size(img, kernel):
    return []

img = [[0, 0, 0, 0], [0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]]
for row in same_size(img, [[1, 1, 1], [1, 1, 1], [1, 1, 1]]):
    print(row)
