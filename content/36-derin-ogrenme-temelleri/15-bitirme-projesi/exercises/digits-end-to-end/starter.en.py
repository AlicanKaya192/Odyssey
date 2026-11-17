import torch
from sklearn.datasets import load_digits
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

digits = load_digits()
X = torch.tensor(digits.data, dtype=torch.float32) / 16
Y = torch.tensor(digits.target)
order = torch.randperm(len(X), generator=torch.Generator().manual_seed(1))
train_idx, test_idx = order[:1400], order[1400:]


def train_and_test(epochs):
    torch.manual_seed(0)
    model = nn.Sequential(nn.Linear(64, 32), nn.ReLU(), nn.Linear(32, 10))
    loader = DataLoader(TensorDataset(X[train_idx], Y[train_idx]), batch_size=32,
                        shuffle=True, generator=torch.Generator().manual_seed(0))
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    loss_fn = nn.CrossEntropyLoss()
    # Write the training loop here: in every epoch, for every batch,
    # zero_grad, loss, backward, step.
    with torch.no_grad():
        pred = model(X[test_idx]).argmax(dim=1)
    return (pred == Y[test_idx]).float().mean().item()


print(train_and_test(10) > 0.9)
