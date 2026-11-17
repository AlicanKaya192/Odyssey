Not every dataset comes with class folders. Another common layout: all
pictures in a single folder, the labels in a CSV file (`file,label`).
`ImageFolder` cannot read it; you write your own `Dataset`.

```python
import csv
from pathlib import Path

import numpy as np
import torch
from PIL import Image
from torch.utils.data import Dataset
from torchvision.transforms import v2
from dl_data import make_shapes

folder = Path("flat_data")
folder.mkdir(exist_ok=True)
images, labels = make_shapes(6, seed=4)
with open(folder / "labels.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["file", "label"])
    for i, (img, label) in enumerate(zip(images, labels)):
        name = f"img{i}.png"
        Image.fromarray((img[0] * 255).round().astype(np.uint8)).save(folder / name)
        writer.writerow([name, int(label)])


class CsvImages(Dataset):
    def __init__(self, folder, transform=None):
        self.folder = Path(folder)
        with open(self.folder / "labels.csv", newline="") as f:
            self.rows = [(row["file"], int(row["label"])) for row in csv.DictReader(f)]
        self.transform = transform

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, i):
        name, label = self.rows[i]
        image = Image.open(self.folder / name).convert("L")
        if self.transform is not None:
            image = self.transform(image)
        return image, label


data = CsvImages(folder, v2.Compose([v2.ToImage(), v2.ToDtype(torch.float32, scale=True)]))
image, label = data[0]
print(len(data), tuple(image.shape), label == labels[0])
```

```text
6 (1, 16, 16) True
```

- `csv.DictReader` gives each row as a dictionary keyed by the header names.
- If a CSV file is opened on Windows without `newline=""`, empty lines can
  appear between rows; make `newline=""` a habit both when reading and when
  writing.
- Labels in a CSV are text; `int(...)` turns them into numbers. If the label
  is a name (`"cat"`), build a dictionary that maps names to numbers.
