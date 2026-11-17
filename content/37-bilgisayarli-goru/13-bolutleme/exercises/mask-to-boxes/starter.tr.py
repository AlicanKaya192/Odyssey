import torch


def mask_boxes(mask):
    return []

mask = [[0, 0, 0, 0, 0],
        [0, 2, 2, 0, 0],
        [0, 2, 2, 0, 3],
        [1, 0, 0, 0, 3],
        [0, 0, 0, 0, 0]]
for box in mask_boxes(mask):
    print(box)
