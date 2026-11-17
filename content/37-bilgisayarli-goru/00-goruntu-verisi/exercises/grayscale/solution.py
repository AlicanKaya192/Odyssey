import torch


def grayscale(rgb):
    x = torch.tensor(rgb)
    gray = 0.299 * x[0] + 0.587 * x[1] + 0.114 * x[2]
    return [[round(v, 3) for v in row] for row in gray.tolist()]

pixel_rows = [[[1.0, 0.0]], [[0.0, 1.0]], [[0.0, 0.0]]]
print(grayscale(pixel_rows))
print(grayscale([[[0.5]], [[0.5]], [[0.5]]]))
