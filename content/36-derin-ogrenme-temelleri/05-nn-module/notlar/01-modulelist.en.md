When writing a network with a variable number of layers, putting the layers
in a list comes to mind. A plain Python list **seems to work** but is
silently broken:

```python
class ListNet(nn.Module):
    def __init__(self, sizes, use_module_list):
        super().__init__()
        layers = [nn.Linear(a, b) for a, b in zip(sizes, sizes[1:])]
        self.layers = nn.ModuleList(layers) if use_module_list else layers

    def forward(self, x):
        for layer in self.layers:
            x = torch.relu(layer(x))
        return x


plain = ListNet([6, 8, 8, 3], use_module_list=False)
proper = ListNet([6, 8, 8, 3], use_module_list=True)
print(plain(x).shape, len(list(plain.parameters())))
print(proper(x).shape, len(list(proper.parameters())))
```

```text
torch.Size([600, 3]) 0
torch.Size([600, 3]) 6
```

- Both models give an output of the same shape. But the layers in the plain
  list were not registered with the model: `parameters()` is **empty**.
- When you try to train this model, no parameter reaches the optimizer.
  PyTorch notices and raises `optimizer got an empty parameter list`; but in
  a model where some layers are in a list and some are assigned with
  `self.`, there is not even an error: the ones in the list never learn.
- The fix is `nn.ModuleList` (`nn.ModuleDict` for a dictionary): used like a
  Python list, it registers its contents with the model.
