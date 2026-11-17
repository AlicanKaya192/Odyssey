# nn.Module and Layers

So far we built models with `nn.Sequential`, lining the layers up one after
another. In most real PyTorch code, though, a model is a **class**: a class
that inherits from `nn.Module`, builds its layers in `__init__` and writes
the computation in `forward`. In this section we write such a class, see how
PyTorch finds the parameters and test with a short training that the class
works.

## The first model class

The data is `dl_data.make_table`: 600 rows, 6 features, 3 classes.

```python
import torch
from torch import nn
from dl_data import make_table


class TableNet(nn.Module):
    def __init__(self, n_features, n_hidden, n_classes):
        super().__init__()
        self.hidden = nn.Linear(n_features, n_hidden)
        self.act = nn.ReLU()
        self.out = nn.Linear(n_hidden, n_classes)

    def forward(self, x):
        h = self.act(self.hidden(x))
        return self.out(h)


torch.manual_seed(0)
model = TableNet(6, 16, 3)
x_np, y_np = make_table(600)
x, y = torch.from_numpy(x_np), torch.from_numpy(y_np)
print(x.shape, y.shape, model(x).shape)
```

```text
torch.Size([600, 6]) torch.Size([600]) torch.Size([600, 3])
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span><code>class TableNet(nn.Module)</code></span><span>The model inherits from PyTorch's <code>nn.Module</code> class.</span></div>
    <div class="anat-row"><span><code>super().__init__()</code></span><span>Prepares the base class; forget it and assigning a layer raises an error.</span></div>
    <div class="anat-row"><span><code>self.hidden = nn.Linear(...)</code></span><span>A layer assigned as an attribute becomes part of the model.</span></div>
    <div class="anat-row"><span><code>def forward(self, x)</code></span><span>The computation from input to output. We do not write the backward pass; autograd does.</span></div>
    <div class="anat-row"><span><code>model(x)</code></span><span>Calls <code>forward</code>. Do not write <code>model.forward(x)</code>.</span></div>
  </div>
  <figcaption>The parts of a PyTorch model.</figcaption>
</figure>

When you write `model(x)`, PyTorch calls `forward`, but it also does some
work of its own in between (such as the hooks we will see later). That is
why `forward` is never called directly.

## Parameters are found automatically

The moment we assign the layers with `self.`, `nn.Module` registers them and
the parameters inside them:

```python
print(model)
for name, p in model.named_parameters():
    print(name, tuple(p.shape), p.requires_grad)
print(sum(p.numel() for p in model.parameters()))
```

```text
TableNet(
  (hidden): Linear(in_features=6, out_features=16, bias=True)
  (act): ReLU()
  (out): Linear(in_features=16, out_features=3, bias=True)
)
hidden.weight (16, 6) True
hidden.bias (16,) True
out.weight (3, 16) True
out.bias (3,) True
163
```

- A parameter's name comes from the layer's attribute name: `hidden.weight`,
  `out.bias`.
- All of them are `requires_grad=True`: `nn.Linear` already builds its
  parameters as tensors that want gradients.
- `model.parameters()` is how this list reaches the optimizer:
  `torch.optim.SGD(model.parameters(), ...)`.
- `nn.ReLU` has no parameters; it is still in the list as a layer.

## Training the class

The model is written as a class, but the training loop does not change:

```python
x_train, y_train, x_test, y_test = x[:480], y[:480], x[480:], y[480:]
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
loss_fn = nn.CrossEntropyLoss()
for epoch in range(200):
    optimizer.zero_grad()
    loss = loss_fn(model(x_train), y_train)
    loss.backward()
    optimizer.step()
with torch.no_grad():
    accuracy = (model(x_test).argmax(dim=1) == y_test).float().mean().item()
print(round(loss.item(), 2), round(accuracy, 2))
```

```text
0.3 0.88
```

The test accuracy is 88%. The classes of `make_table` overlap on
purpose; it does not reach 100%. What matters is that our own class can be
trained just like `nn.Sequential`.

## Freedom in `forward`

`nn.Sequential` can only apply layers in order. In a class, `forward` is an
ordinary Python function: you can write additions, `if`, loops, several
inputs. For example a **residual connection**, which adds the input to the
output, is one of the building blocks of deep networks:

```python
class Residual(nn.Module):
    def __init__(self, size):
        super().__init__()
        self.layer = nn.Linear(size, size)

    def forward(self, x):
        return x + torch.relu(self.layer(x))


block = Residual(6)
nn.init.zeros_(block.layer.weight)
nn.init.zeros_(block.layer.bias)
print(block(x[:2]).shape, torch.equal(block(x[:2]), x[:2]))
```

```text
torch.Size([2, 6]) True
```

With the layer's weights at zero, `relu(0) = 0`; the block passes the input
through unchanged (`torch.equal` says two tensors are exactly the same). A
residual connection lets information flow without being lost even if the
layer learns nothing. ResNet in the Computer Vision module is built on this
idea.

## Training and evaluation mode

Every module has a `training` flag. Some layers (`Dropout` in the
Regularisation section, `BatchNorm` in the Normalisation section) behave
differently when training and when predicting; the flag tells them which one
we are in:

```python
print(model.training, model.hidden.training)
model.eval()
print(model.training, model.hidden.training)
model.train()
print(model.training)
```

```text
True True
False False
True
```

`model.eval()` sets the flag of the model and of **all its sub-layers** to
`False`; `model.train()` turns it back on. The habit: `model.eval()` and
`torch.no_grad()` before evaluating, `model.train()` when going back to
training.

## Summary

- A model is a class that inherits from `nn.Module`: layers in `__init__`,
  the computation in `forward`.
- The parameters of layers assigned with `self.` are registered
  automatically; `model.parameters()` goes to the optimizer.
- `forward` is free Python code; structures such as residual connections can
  be written.
- `model.eval()` and `model.train()` switch the mode.
