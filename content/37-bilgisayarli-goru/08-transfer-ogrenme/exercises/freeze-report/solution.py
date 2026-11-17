from torch import nn
from torchvision import models


def freeze_report(num_classes):
    model = models.resnet18(weights=None)
    for p in model.parameters():
        p.requires_grad = False
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    frozen = sum(p.numel() for p in model.parameters() if not p.requires_grad)
    return [trainable, frozen]

print(freeze_report(2))
print(freeze_report(10))
