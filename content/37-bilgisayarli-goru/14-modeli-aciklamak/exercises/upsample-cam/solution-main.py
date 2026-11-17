import torch
import torch.nn.functional as F


def upsample_cam(cam, size):
    t = torch.tensor(cam, dtype=torch.float32)[None, None]
    big = F.interpolate(t, size=(size, size), mode="nearest")
    return big[0, 0].tolist()

for row in upsample_cam([[1.0, 0.0], [0.0, 2.0]], 4):
    print(row)
