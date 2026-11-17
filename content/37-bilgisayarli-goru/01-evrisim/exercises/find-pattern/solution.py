import torch
import torch.nn.functional as F


def find_pattern(img, pattern):
    x = torch.tensor(img, dtype=torch.float32)[None, None]
    w = torch.tensor(pattern, dtype=torch.float32)[None, None]
    response = F.conv2d(x, w)[0, 0]
    index = response.argmax().item()
    return [index // response.shape[1], index % response.shape[1]]

img = [[0] * 7 for _ in range(6)]
img[3][4] = 1
img[2][4] = 1
img[4][4] = 1
img[3][3] = 1
img[3][5] = 1
cross = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
print(find_pattern(img, cross))
print(find_pattern(img, [[1, 1]]))
