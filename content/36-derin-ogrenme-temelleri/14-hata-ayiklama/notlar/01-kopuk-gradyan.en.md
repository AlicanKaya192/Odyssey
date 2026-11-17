If part of the model does not learn at all, the first place to look is
whether every parameter's gradient is filled after `backward()`. A stray
`.detach()` (or `.item()`, a trip through NumPy) breaks the chain of
derivatives:

```python
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.first = nn.Linear(4, 4)
        self.second = nn.Linear(4, 1)

    def forward(self, x):
        h = torch.relu(self.first(x)).detach()
        return self.second(h)


net = Net()
net(torch.randn(3, 4)).sum().backward()
for name, p in net.named_parameters():
    print(name, None if p.grad is None else tuple(p.grad.shape))
```

```text
first.weight None
first.bias None
second.weight (1, 4)
second.bias (1,)
```

- The `second` layer has a gradient, `first` does not (`None`): the loss
  cannot see behind the `detach` point. The program raises no error; the
  first layer stays in its random starting state throughout training.
- The same printout also finds frozen layers (`requires_grad=False`); they
  show `None` too.
- The rule: `.detach()`, `.item()` and `.numpy()` appear in a model's
  `forward` only on purpose.
