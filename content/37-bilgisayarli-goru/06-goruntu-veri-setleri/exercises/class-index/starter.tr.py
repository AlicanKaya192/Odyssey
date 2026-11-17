import tempfile
from pathlib import Path

import numpy as np
from PIL import Image
from torchvision import datasets


def class_index(names):
    return {}

print(class_index(["dog", "cat", "bird"]))
print(class_index(["7", "12", "3"]))
