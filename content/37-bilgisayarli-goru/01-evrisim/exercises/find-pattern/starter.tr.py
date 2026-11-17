import torch
import torch.nn.functional as F


def find_pattern(img, pattern):
    return []

img = [[0] * 7 for _ in range(6)]
img[3][4] = 1
img[2][4] = 1
img[4][4] = 1
img[3][3] = 1
img[3][5] = 1
cross = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
print(find_pattern(img, cross))
print(find_pattern(img, [[1, 1]]))
