PyTorch's built-in way to initialise all the layers of a model with the same
rule is `model.apply(function)`: the function is applied to every sub-module
of the model in turn.

```python
def init_weights(module):
    if isinstance(module, nn.Linear):
        nn.init.kaiming_normal_(module.weight, nonlinearity="relu")
        nn.init.zeros_(module.bias)


torch.manual_seed(0)
model = nn.Sequential(nn.Linear(256, 256), nn.ReLU(), nn.Linear(256, 10))
model.apply(init_weights)
print(model[0].bias.abs().sum().item())
print(round(model[0].weight.std().item(), 2), round(math.sqrt(2 / 256), 2))
```

```text
0.0
0.09 0.09
```

- `isinstance` picked only the `nn.Linear` layers; ReLU was left alone (it
  has no parameters anyway).
- The biases were zeroed; the standard deviation of the weights matches
  Kaiming's formula `sqrt(2 / 256)`.
- `apply` walks nested modules too: it reaches the layers of the
  `nn.Sequential`s inside your own class. Calling the initialisation with
  `self.apply(...)` at the end of the model's `__init__` is a common
  pattern.
