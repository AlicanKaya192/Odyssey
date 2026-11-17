import torch


def row_scales(weight):
    # For every row: that row's largest |w| / 127, with 4 places
    return []

print(row_scales([[0.127, -0.0635], [12.7, 1.0]]))
