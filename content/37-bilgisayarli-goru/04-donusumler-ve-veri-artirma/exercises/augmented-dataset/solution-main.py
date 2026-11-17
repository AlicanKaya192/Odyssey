import torch
from torch.utils.data import Dataset
from torchvision.transforms import v2
from dl_data import make_shapes


class Shapes(Dataset):
    def __init__(self, x, y, transform=None):
        self.x = torch.from_numpy(x)
        self.y = torch.from_numpy(y)
        self.transform = transform

    def __len__(self):
        return len(self.y)

    def __getitem__(self, i):
        image = self.x[i]
        if self.transform is not None:
            image = self.transform(image)
        return image, self.y[i]

x, y = make_shapes(20, seed=3)
augment = v2.Compose([v2.RandomHorizontalFlip(), v2.RandomCrop(16, padding=3)])
torch.manual_seed(0)
plain = Shapes(x, y)
augmented = Shapes(x, y, augment)
print(len(plain), len(augmented))
image, label = augmented[0]
print(tuple(image.shape), label.item() == y[0])
print(torch.equal(plain[5][0], plain[5][0]), torch.equal(augmented[5][0], augmented[5][0]))
