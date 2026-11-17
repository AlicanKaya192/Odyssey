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
    return 0.0, 0.0

plain_train, plain_test = fit(None)
aug_train, aug_test = fit(augment)
print(plain_train - plain_test > 0.1)
print(aug_train - aug_test < 0.1)
print(aug_test > plain_test)
