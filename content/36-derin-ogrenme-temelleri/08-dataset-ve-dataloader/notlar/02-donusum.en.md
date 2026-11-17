Changing an example before it reaches the model (flattening, flipping,
scaling) is usually done in the Dataset's `__getitem__`. Taking the
transform as a parameter lets the same data class serve different jobs:

```python
class TransformedShapes(Dataset):
    def __init__(self, n, transform=None):
        self.images, self.labels = make_shapes(n, size=16)
        self.transform = transform

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, i):
        image = torch.from_numpy(self.images[i])
        if self.transform is not None:
            image = self.transform(image)
        return image, int(self.labels[i])


flat = TransformedShapes(100, transform=lambda t: t.flatten())
mirrored = TransformedShapes(100, transform=lambda t: t.flip(-1))
print(flat[0][0].shape, mirrored[0][0].shape)
print(torch.equal(mirrored[0][0], shapes[0][0].flip(-1)))
```

```text
torch.Size([256]) torch.Size([1, 16, 16])
True
```

- `flat` turns the image into the flat vector `nn.Linear` wants.
- `mirrored` mirrors the image horizontally (reverses the last dimension).
  Applied at random, this becomes data augmentation: the model sees slightly
  different images every epoch.
- The transform runs again on every `__getitem__` call; the original data
  does not change.

In the Computer Vision module, `torchvision.transforms` gives ready-made
versions of these transforms; the idea is the same.
