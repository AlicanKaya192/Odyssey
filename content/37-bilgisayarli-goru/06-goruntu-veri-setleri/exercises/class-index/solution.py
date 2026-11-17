import tempfile
from pathlib import Path

import numpy as np
from PIL import Image
from torchvision import datasets


def class_index(names):
    blank = Image.fromarray(np.zeros((4, 4), dtype=np.uint8))
    with tempfile.TemporaryDirectory() as root:
        for name in names:
            (Path(root) / name).mkdir()
            blank.save(Path(root) / name / "a.png")
        return datasets.ImageFolder(root).class_to_idx

print(class_index(["dog", "cat", "bird"]))
print(class_index(["7", "12", "3"]))
