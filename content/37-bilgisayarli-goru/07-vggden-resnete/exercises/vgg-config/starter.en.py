import torch
from torch import nn


def vgg_summary(config):
    return []

print(vgg_summary([16, 16, "M", 32, 32, "M"]))
print(vgg_summary([8, "M", 8, "M", 8, "M"]))
