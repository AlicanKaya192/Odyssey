import torch


def gradcam_map(maps, grads):
    a = torch.tensor(maps, dtype=torch.float32)
    g = torch.tensor(grads, dtype=torch.float32)
    weights = g.mean(dim=(1, 2), keepdim=True)
    cam = torch.relu((weights * a).sum(dim=0))
    return [[round(v, 3) for v in row] for row in cam.tolist()]

maps = [[[1.0, 0.0], [0.0, 0.0]], [[0.0, 0.0], [0.0, 2.0]]]
grads = [[[1.0, 1.0], [1.0, 1.0]], [[-1.0, -1.0], [-1.0, -1.0]]]
print(gradcam_map(maps, grads))
print(gradcam_map(maps, [[[0.5, 0.5], [0.5, 0.5]], [[0.5, 0.5], [0.5, 0.5]]]))
