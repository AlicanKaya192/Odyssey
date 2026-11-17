import torch
from dl_data import make_shapes, SHAPES


def bounding_box(img, threshold):
    x = torch.tensor(img)
    rows, cols = torch.nonzero(x > threshold, as_tuple=True)
    if len(rows) == 0:
        return []
    return [cols.min().item(), rows.min().item(), cols.max().item() + 1, rows.max().item() + 1]

images, labels = make_shapes(5)
for img, label in zip(images[:3], labels[:3]):
    print(SHAPES[label], bounding_box(img[0].tolist(), 0.5))
