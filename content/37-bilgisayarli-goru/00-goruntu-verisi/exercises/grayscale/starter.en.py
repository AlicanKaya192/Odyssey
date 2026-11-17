import torch


def grayscale(rgb):
    return []

pixel_rows = [[[1.0, 0.0]], [[0.0, 1.0]], [[0.0, 0.0]]]
print(grayscale(pixel_rows))
print(grayscale([[[0.5]], [[0.5]], [[0.5]]]))
