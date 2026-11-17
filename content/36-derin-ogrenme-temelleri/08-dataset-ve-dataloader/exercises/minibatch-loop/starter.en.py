import torch
from torch import nn
from torch.utils.data import TensorDataset, DataLoader, random_split
from sklearn.datasets import load_digits

digits = load_digits()
X = torch.tensor(digits.data, dtype=torch.float32) / 16
y = torch.tensor(digits.target)
train_set, test_set = random_split(TensorDataset(X, y), [1500, 297],
                                   generator=torch.Generator().manual_seed(0))
torch.manual_seed(0)
train_loader = DataLoader(train_set, batch_size=32, shuffle=True,
                          generator=torch.Generator().manual_seed(0), num_workers=0)
model = nn.Sequential(nn.Linear(64, 32), nn.ReLU(), nn.Linear(32, 10))
optimizer = torch.optim.Adam(model.parameters(), lr=0.005)
loss_fn = nn.CrossEntropyLoss()
for epoch in range(5):
    # Walk over the batches; four steps for each batch.
    pass

x_test, y_test = test_set[:]
with torch.no_grad():
    correct = (model(x_test).argmax(dim=1) == y_test).sum().item()
print(correct > 270)
