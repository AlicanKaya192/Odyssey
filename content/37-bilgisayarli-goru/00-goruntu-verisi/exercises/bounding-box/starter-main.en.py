import torch
from dl_data import make_shapes, SHAPES


def bounding_box(img, threshold):
    return []

images, labels = make_shapes(5)
for img, label in zip(images[:3], labels[:3]):
    print(SHAPES[label], bounding_box(img[0].tolist(), 0.5))
