import torch


def peak_cell(cam):
    t = torch.tensor(cam, dtype=torch.float32)
    index = t.flatten().argmax().item()
    return list(divmod(index, t.shape[1]))

cam = [[0.0, 0.2, 0.1], [0.5, 0.9, 0.3], [0.0, 0.4, 0.9]]
print(peak_cell(cam))
print(peak_cell([[1, 1], [1, 1]]))
