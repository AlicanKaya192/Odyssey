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
    # data: a one-channel ImageFolder in [0, 1]; loader: batch 8.
    data = None
    loader = []
    batch, batch_labels = next(iter(loader))
    print(len(data), len(loader))
    print(tuple(batch.shape), batch_labels.dtype)
    print(round(batch.max().item(), 2) <= 1.0)
