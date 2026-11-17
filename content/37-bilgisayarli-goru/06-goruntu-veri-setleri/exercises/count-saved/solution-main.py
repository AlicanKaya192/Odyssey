import tempfile
from pathlib import Path

import numpy as np
from PIL import Image
from dl_data import make_shapes, SHAPES


def count_saved(n, seed):
    images, labels = make_shapes(n, seed=seed)
    with tempfile.TemporaryDirectory() as root:
        for i, (img, label) in enumerate(zip(images, labels)):
            target = Path(root) / SHAPES[label]
            target.mkdir(exist_ok=True)
            pixels = (img[0] * 255).round().astype(np.uint8)
            Image.fromarray(pixels, mode="L").save(target / f"{i:03d}.png")
        return [len(list((Path(root) / name).glob("*.png"))) for name in SHAPES]

print(count_saved(30, 1))
print(count_saved(12, 5))
