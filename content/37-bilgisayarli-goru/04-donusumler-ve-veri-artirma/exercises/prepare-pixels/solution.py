import torch
from torchvision.transforms import v2


def prepare(pixels):
    pipeline = v2.Compose([
        v2.ToDtype(torch.float32, scale=True),
        v2.Normalize([0.5], [0.25]),
    ])
    x = torch.tensor(pixels, dtype=torch.uint8).reshape(1, 1, -1)
    return [round(v, 3) for v in pipeline(x).flatten().tolist()]

print(prepare([0, 64, 128, 255]))
