import torch


def normalize_cam(cam):
    t = torch.relu(torch.tensor(cam, dtype=torch.float32))
    peak = t.max().item()
    if peak > 0:
        t = t / peak
    return [[round(v, 2) for v in row] for row in t.tolist()]

print(normalize_cam([[0.0, -1.0], [2.0, 4.0]]))
print(normalize_cam([[-1.0, -2.0], [0.0, -3.0]]))
