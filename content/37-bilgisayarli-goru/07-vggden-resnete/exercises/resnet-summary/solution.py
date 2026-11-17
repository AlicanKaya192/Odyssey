from torch import nn
from torchvision import models


def resnet_summary(num_classes):
    model = models.resnet18(weights=None)
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    convs = sum(1 for m in model.modules() if isinstance(m, nn.Conv2d))
    params = sum(p.numel() for p in model.parameters())
    return [convs, params]

print(resnet_summary(3))
print(resnet_summary(10))
