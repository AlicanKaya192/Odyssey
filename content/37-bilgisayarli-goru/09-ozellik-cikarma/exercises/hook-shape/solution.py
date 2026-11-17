import torch
from torch import nn


def hook_shape(index, size):
    torch.manual_seed(0)
    model = nn.Sequential(
        nn.Conv2d(1, 8, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        nn.Conv2d(8, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        nn.Flatten(),
    )
    captured = []


    def save(module, inputs, output):
        captured.append(output.detach())

    handle = model[index].register_forward_hook(save)
    with torch.no_grad():
        model(torch.zeros(1, 1, size, size))
    handle.remove()
    with torch.no_grad():
        model(torch.zeros(1, 1, size, size))
    return [list(captured[0].shape), len(captured)]

print(hook_shape(2, 16))
print(hook_shape(5, 24))
