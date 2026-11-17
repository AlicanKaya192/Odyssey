from torch import nn


def training_mode(model):
    pass

model = nn.Sequential(
    nn.Sequential(nn.Conv2d(1, 4, 3), nn.BatchNorm2d(4), nn.ReLU(), nn.AdaptiveAvgPool2d(1), nn.Flatten()),
    nn.Linear(4, 2),
)
model.eval()
training_mode(model)
print(model.training, model[0].training, model[1].training)
print(model[0][1].training)
