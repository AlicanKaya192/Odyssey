import torch
from torch import nn
from torch.utils.data import TensorDataset, DataLoader


def evaluate(model, loader, loss_fn):
    return 0.0, 0.0


model = nn.Linear(2, 2)
nn.init.eye_(model.weight)
nn.init.zeros_(model.bias)
xs = torch.tensor([[2.0, 0.0], [0.0, 2.0], [1.0, 0.0], [0.0, 1.0], [3.0, 0.0]])
ys = torch.tensor([0, 1, 1, 1, 0])
loader = DataLoader(TensorDataset(xs, ys), batch_size=2)
loss, accuracy = evaluate(model, loader, nn.CrossEntropyLoss())
print(round(loss, 4), accuracy)
