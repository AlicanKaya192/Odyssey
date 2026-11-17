import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset
from dl_data import make_shapes

x_train, y_train = make_shapes(600, seed=1)
x_test, y_test = make_shapes(300, seed=2)
train_set = TensorDataset(torch.from_numpy(x_train), torch.from_numpy(y_train))
x_test, y_test = torch.from_numpy(x_test), torch.from_numpy(y_test)
loader = DataLoader(train_set, batch_size=32, shuffle=True,
                    generator=torch.Generator().manual_seed(0))

torch.manual_seed(0)
model = nn.Sequential(
    nn.Conv2d(1, 8, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.Conv2d(8, 16, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.Flatten(), nn.Linear(256, 3),
)
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.005)

for epoch in range(8):
    model.train()
    for images, labels in loader:
        # Write the missing lines: zero the gradients, backpropagate, step.
        loss = loss_fn(model(images), labels)

model.eval()
with torch.no_grad():
    acc = (model(x_test).argmax(dim=1) == y_test).float().mean().item()
print(len(loader))
print(acc > 0.85)
