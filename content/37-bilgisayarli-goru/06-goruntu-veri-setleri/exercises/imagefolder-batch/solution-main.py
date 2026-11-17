import tempfile
from pathlib import Path

import numpy as np
import torch
from PIL import Image
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import v2
from dl_data import make_shapes, SHAPES

images, labels = make_shapes(40, seed=2)
with tempfile.TemporaryDirectory() as root:
    for i, (img, label) in enumerate(zip(images, labels)):
        target = Path(root) / SHAPES[label]
        target.mkdir(exist_ok=True)
        Image.fromarray((img[0] * 255).round().astype(np.uint8)).save(target / f"{i:02d}.png")
    gray = v2.Compose([v2.ToImage(), v2.Grayscale(), v2.ToDtype(torch.float32, scale=True)])
    data = datasets.ImageFolder(root, transform=gray)
    loader = DataLoader(data, batch_size=8, shuffle=True,
                        generator=torch.Generator().manual_seed(0))
    batch, batch_labels = next(iter(loader))
    print(len(data), len(loader))
    print(tuple(batch.shape), batch_labels.dtype)
    print(round(batch.max().item(), 2) <= 1.0)
