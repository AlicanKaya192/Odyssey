import torch
from torch import nn
from sklearn.datasets import load_digits

torch.manual_seed(0)
digits = load_digits()
X = torch.tensor(digits.data, dtype=torch.float32) / 16
y = torch.tensor(digits.target)
model = nn.Sequential(nn.Linear(64, 16), nn.ReLU(), nn.Linear(16, 10))
optimizer = torch.optim.SGD(model.parameters(), lr=0.5)
loss_fn = nn.CrossEntropyLoss()

first = loss_fn(model(X[:1200]), y[:1200]).item()
for epoch in range(100):
    optimizer.zero_grad()
    loss = loss_fn(model(X[:1200]), y[:1200])
    loss.backward()
    optimizer.step()

last = loss_fn(model(X[:1200]), y[:1200]).item()
correct = (model(X[1200:]).argmax(dim=1) == y[1200:]).sum().item()
print(last < first / 4)
print(correct > 500)
