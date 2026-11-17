import torch
from torch import nn

torch.manual_seed(0)
model = nn.Sequential(
    nn.Conv2d(1, 4, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.Conv2d(4, 8, 3), nn.ReLU(), nn.Flatten(),
)


def layer_shapes(size):
    shapes = []
    handles = [layer.register_forward_hook(
        lambda module, inputs, output: shapes.append(list(output.shape)))
        for layer in model]
    try:
        model(torch.zeros(1, 1, size, size))
    finally:
        for handle in handles:
            handle.remove()
    return shapes

for shape in layer_shapes(8):
    print(shape)
print(layer_shapes(12)[-1])
print(len(layer_shapes(8)))
