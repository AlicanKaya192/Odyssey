import torch


def encode(boxes, S, size, C):
    return []

target = encode([[2, 4, 10, 12, 0], [8, 0, 16, 4, 1]], 2, 16, 2)
for row in target:
    for cell in row:
        print(cell)
