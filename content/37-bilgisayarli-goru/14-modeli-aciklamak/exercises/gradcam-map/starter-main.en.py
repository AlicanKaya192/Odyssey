import torch


def gradcam_map(maps, grads):
    return []

maps = [[[1.0, 0.0], [0.0, 0.0]], [[0.0, 0.0], [0.0, 2.0]]]
grads = [[[1.0, 1.0], [1.0, 1.0]], [[-1.0, -1.0], [-1.0, -1.0]]]
print(gradcam_map(maps, grads))
print(gradcam_map(maps, [[[0.5, 0.5], [0.5, 0.5]], [[0.5, 0.5], [0.5, 0.5]]]))
