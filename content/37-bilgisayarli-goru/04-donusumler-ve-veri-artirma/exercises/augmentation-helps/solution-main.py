import torch
import torch.nn.functional as F
from torch import nn
from torch.utils.data import DataLoader, Dataset
from torchvision.transforms import v2
from dl_data import make_shapes


class Shapes(Dataset):
    def __init__(self, x, y, transform=None):
        self.x, self.y, self.transform = torch.from_numpy(x), torch.from_numpy(y), transform

    def __len__(self):
        return len(self.y)

    def __getitem__(self, i):
        image = self.x[i] if self.transform is None else self.transform(self.x[i])
        return image, self.y[i]


x_small, y_small = make_shapes(90, seed=1)
x_test, y_test = make_shapes(300, seed=2)
x_test, y_test = torch.from_numpy(x_test), torch.from_numpy(y_test)
augment = v2.Compose([v2.RandomHorizontalFlip(), v2.RandomCrop(16, padding=3)])


def fit(transform):
    torch.manual_seed(0)
    model = nn.Sequential(
        nn.Conv2d(1, 8, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        nn.Conv2d(8, 16, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        nn.Flatten(), nn.Linear(256, 3),
    )
    optimizer = torch.optim.Adam(model.parameters(), lr=0.005)
    loader = DataLoader(Shapes(x_small, y_small, transform), batch_size=16, shuffle=True,
                        generator=torch.Generator().manual_seed(0))
    for epoch in range(25):
        model.train()
        for xb, yb in loader:
            optimizer.zero_grad()
            F.cross_entropy(model(xb), yb).backward()
            optimizer.step()
    model.eval()
    with torch.no_grad():
        train_x, train_y = torch.from_numpy(x_small), torch.from_numpy(y_small)
        train_acc = (model(train_x).argmax(1) == train_y).float().mean().item()
        test_acc = (model(x_test).argmax(1) == y_test).float().mean().item()
    return train_acc, test_acc

plain_train, plain_test = fit(None)
aug_train, aug_test = fit(augment)
print(plain_train - plain_test > 0.1)
print(aug_train - aug_test < 0.1)
print(aug_test > plain_test)
