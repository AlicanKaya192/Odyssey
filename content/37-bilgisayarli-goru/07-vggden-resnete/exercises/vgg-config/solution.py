import torch
from torch import nn


def vgg_summary(config):
    layers = []
    channels = 1
    for item in config:
        if item == "M":
            layers.append(nn.MaxPool2d(2))
        else:
            layers += [nn.Conv2d(channels, item, 3, padding=1), nn.ReLU()]
            channels = item
    model = nn.Sequential(*layers)
    shape = list(model(torch.zeros(1, 1, 16, 16)).shape[1:])
    return [sum(p.numel() for p in model.parameters()), shape]

print(vgg_summary([16, 16, "M", 32, 32, "M"]))
print(vgg_summary([8, "M", 8, "M", 8, "M"]))
