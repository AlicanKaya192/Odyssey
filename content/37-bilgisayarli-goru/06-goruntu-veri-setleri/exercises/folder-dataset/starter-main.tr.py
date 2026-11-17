import tempfile
from pathlib import Path

import numpy as np
import torch
from PIL import Image
from torch.utils.data import Dataset
from torchvision.transforms import v2
from dl_data import make_shapes, SHAPES


class FolderImages(Dataset):
    def __init__(self, root, transform=None):
        self.classes = []
        self.samples = []
        self.transform = transform

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, i):
        path, label = self.samples[i]
        image = Image.open(path).convert("L")
        if self.transform is not None:
            image = self.transform(image)
        return image, label


images, labels = make_shapes(24, seed=3)
with tempfile.TemporaryDirectory() as root:
    for i, (img, label) in enumerate(zip(images, labels)):
        target = Path(root) / SHAPES[label]
        target.mkdir(exist_ok=True)
        Image.fromarray((img[0] * 255).round().astype(np.uint8)).save(target / f"{i:02d}.png")
    data = FolderImages(root, v2.Compose([v2.ToImage(), v2.ToDtype(torch.float32, scale=True)]))
    print(len(data), data.classes)
    image, label = data[0]
    print(tuple(image.shape), label)
    print([data[i][1] for i in range(0, 24, 6)])
