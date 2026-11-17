from torch import nn
from torchvision import models


def freeze_report(num_classes):
    return []

print(freeze_report(2))
print(freeze_report(10))
