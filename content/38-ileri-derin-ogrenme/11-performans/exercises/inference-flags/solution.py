import torch
from torch import nn


def inference_flags():
    model = nn.Linear(4, 2)
    x = torch.ones(3, 4)
    y = model(x)
    with torch.inference_mode():
        z = model(x)
    return [y.requires_grad, z.requires_grad, z.is_inference()]

print(inference_flags())
