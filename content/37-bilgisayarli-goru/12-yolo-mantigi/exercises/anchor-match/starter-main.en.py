import torch


def anchor_match(objects, anchors):
    return []

anchors = [[8, 8], [8, 16], [16, 8]]
print(anchor_match([[6, 14], [15, 7], [10, 10], [4, 4]], anchors))
