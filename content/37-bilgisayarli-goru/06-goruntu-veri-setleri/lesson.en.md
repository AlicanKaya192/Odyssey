# ImageFolder and Image Datasets

Until now the pictures came ready in memory as a NumPy array. In real projects
pictures are **files**: hundreds or thousands of `.png` or `.jpg` files in a
folder. The most common layout gives each class its own subfolder:
`train/cat/...`, `train/dog/...`. torchvision's **`ImageFolder`** class reads
this layout and takes the labels from the folder names. In this section we
write our shape pictures to files, read them back with `ImageFolder` and do
the same job with our own `Dataset` class.

## Writing the pictures to files

With Pillow we save each picture as a greyscale (`"L"` mode) PNG file. We
first turn the pixels into `uint8`: whole numbers 0–255 in the file. We create
the folder inside the working folder, under the name `shapes_data`.

```python
from pathlib import Path

import numpy as np
from PIL import Image
from dl_data import make_shapes, SHAPES


def save_split(folder, n, seed):
    images, labels = make_shapes(n, seed=seed)
    for i, (img, label) in enumerate(zip(images, labels)):
        target = Path(folder) / SHAPES[label]
        target.mkdir(parents=True, exist_ok=True)
        pixels = (img[0] * 255).round().astype(np.uint8)
        Image.fromarray(pixels, mode="L").save(target / f"{i:03d}.png")


save_split("shapes_data/train", 60, seed=1)
save_split("shapes_data/test", 30, seed=2)
for folder in sorted(Path("shapes_data/train").iterdir()):
    print(folder.name, len(list(folder.glob("*.png"))))
```

```text
circle 24
square 15
triangle 21
```

There is now a real dataset on disk: files like
`shapes_data/train/circle/000.png`. The folder name is the label itself.

## ImageFolder

`ImageFolder` takes the root folder; each subfolder is a class, each picture
in it an example. `transform` is applied to each picture as it is read.

```python
import torch
from torchvision import datasets
from torchvision.transforms import v2

to_tensor = v2.Compose([v2.ToImage(), v2.ToDtype(torch.float32, scale=True)])
train_set = datasets.ImageFolder("shapes_data/train", transform=to_tensor)
print(train_set.classes)
print(train_set.class_to_idx)
print(len(train_set))
image, label = train_set[0]
print(image.shape, label)
```

```text
['circle', 'square', 'triangle']
{'circle': 0, 'square': 1, 'triangle': 2}
60
torch.Size([3, 16, 16]) 0
```

- `classes` and `class_to_idx` give the class names and their numbers; the
  numbers follow the **alphabetical** order of the names.
- Careful: the picture came out as `(3, 16, 16)`. By default `ImageFolder`
  opens files converted to **RGB**; a grey picture becomes three identical
  channels.
- `v2.ToImage()` turns the Pillow picture into a tensor; `ToDtype` scales it
  to [0, 1].

If we want a single channel we add `v2.Grayscale()` to the chain:

```python
gray = v2.Compose([v2.ToImage(), v2.Grayscale(), v2.ToDtype(torch.float32, scale=True)])
train_set = datasets.ImageFolder("shapes_data/train", transform=gray)
test_set = datasets.ImageFolder("shapes_data/test", transform=gray)
image, label = train_set[0]
print(image.shape, len(test_set))
path = Path(train_set.samples[0][0])
print(path.parent.name, path.name)
images, labels = make_shapes(60, seed=1)
original = torch.from_numpy(images[int(path.stem)])
print((image - original).abs().max().item() < 0.01)
```

```text
torch.Size([1, 16, 16]) 30
circle 004.png
True
```

- `train_set.samples` holds each example's file path and label. The first
  example is the first file in the `circle` folder: picture number 4 of
  `make_shapes` (the first four pictures are not circles).
- The picture read back from the file is almost the same as the one we saved.
  The difference comes from two small roundings: to `uint8` when saving (at
  most half a step) and when going from RGB back to grey (one step; a step is
  1 / 255 ≈ 0.004).

## DataLoader and holding out validation data

`ImageFolder` is an ordinary `Dataset`: it can be given to a `DataLoader`.
`random_split` is used to hold out a validation part of the training set;
with a seeded generator the split is repeatable.

```python
from torch.utils.data import DataLoader, random_split

part_train, part_val = random_split(train_set, [48, 12],
                                    generator=torch.Generator().manual_seed(0))
loader = DataLoader(part_train, batch_size=16, shuffle=True,
                    generator=torch.Generator().manual_seed(0))
batch, batch_labels = next(iter(loader))
print(len(part_train), len(part_val), len(loader))
print(batch.shape, batch_labels.dtype)
```

```text
48 12 3
torch.Size([16, 1, 16, 16]) torch.int64
```

The batch is `(16, 1, 16, 16)`: the CNNs of the earlier sections can be
trained on this data without any change. The labels are `int64`, as
`CrossEntropyLoss` wants.

## Our own Dataset class

What happens inside `ImageFolder` is surprisingly short. Let us write the same
thing ourselves: collect the file paths and labels in a list, open a file when
it is requested.

```python
from torch.utils.data import Dataset


class FolderImages(Dataset):
    def __init__(self, root, transform=None):
        self.classes = sorted(p.name for p in Path(root).iterdir() if p.is_dir())
        self.samples = []
        for index, name in enumerate(self.classes):
            for path in sorted((Path(root) / name).glob("*.png")):
                self.samples.append((path, index))
        self.transform = transform

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, i):
        path, label = self.samples[i]
        image = Image.open(path).convert("L")
        if self.transform is not None:
            image = self.transform(image)
        return image, label


mine = FolderImages("shapes_data/train", transform=to_tensor)
print(len(mine), mine.classes, mine[5][0].shape)
mine_files = [p.name for p, _ in mine.samples]
their_files = [Path(p).name for p, _ in train_set.samples]
print(mine_files == their_files, mine[5][1] == train_set[5][1])
print((mine[5][0] - train_set[5][0]).abs().max().item() < 0.005)
```

```text
60 ['circle', 'square', 'triangle'] torch.Size([1, 16, 16])
True True
True
```

- The files are in the same order, the labels the same. The pixels differ by
  at most one `uint8` step (1 / 255): `ImageFolder` first converts the picture
  to RGB and brings it back to grey with `Grayscale`; we open it as grey
  (`"L"`) directly.
- The picture is opened in `__getitem__`, not in `__init__`: thousands of
  pictures are not loaded into memory at once, only the requested one is read.
- Writing your own class is needed when the labels are not in folder names
  but in a CSV file; the notes have an example.

## Summary

- Folder layout: `root/class/picture.png`; `ImageFolder(root, transform=...)`.
- Class numbers follow the alphabetical order of the folder names; check
  `class_to_idx`.
- `ImageFolder` opens pictures as RGB; for a single channel use
  `v2.Grayscale()`.
- Holding out validation data: `random_split(..., generator=...)`.
- Your own `Dataset`: paths and labels in a list, open the file in
  `__getitem__`.
