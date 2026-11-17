# 1D Convolution

In the Computer Vision module a convolution was a small kernel sliding over an
image: at every position it looks for a local pattern with the same weights.
The same idea works in one dimension: the kernel slides along a **time
sequence**. A sensor signal, audio, a heart rhythm recording or a sequence of
word embeddings can be read this way.

A 1D convolution has two big differences from an LSTM: all positions are
computed **at the same time** (an LSTM waits step by step), and the network
recognises a pattern **wherever it is**. In this section we train a small 1D
convolutional network that catches a sudden fault in a sensor recording.

## `nn.Conv1d`: shapes

```python
import torch
from torch import nn

torch.manual_seed(0)
conv = nn.Conv1d(in_channels=1, out_channels=4, kernel_size=5)
x = torch.randn(2, 1, 64)
print(conv(x).shape)
print(nn.Conv1d(1, 4, 5, padding=2)(x).shape)
print(nn.Conv1d(1, 4, 5, stride=2)(x).shape)
print(conv.weight.shape, sum(p.numel() for p in conv.parameters()))
```

```text
torch.Size([2, 4, 60])
torch.Size([2, 4, 64])
torch.Size([2, 4, 30])
torch.Size([4, 1, 5]) 24
```

- The input is `(B, C, T)`: batch, **channel**, time. The channel is the
  number of values per step (1 for one sensor, 3 for a three-axis
  accelerometer). Careful: the LSTM wanted `(B, T, D)`; `Conv1d` wants the
  channel **first**.
- Without padding and with stride 1 the output length is `64 − 5 + 1 = 60`.
  `padding=2` adds two zeros to each end and the length stays 64. `stride=2`
  moves the kernel two at a time and halves the length: `(64 − 5) // 2 + 1 =
  30`.
- The weight is `(output channels, input channels, kernel)` = `(4, 1, 5)`;
  20 weights + 4 biases = 24 parameters. The sequence length does not affect
  the parameter count at all.

## A kernel by hand

Let us give the kernel ourselves: `[-1, 1]` computes "next value minus this
value" at every position, that is, it finds the **change**.

```python
diff = nn.Conv1d(1, 1, kernel_size=2, bias=False)
with torch.no_grad():
    diff.weight[:] = torch.tensor([[[-1.0, 1.0]]])
signal = torch.tensor([[[0.0, 0.0, 1.0, 3.0, 3.0, 1.0, 0.0]]])
print(diff(signal).tolist())
```

```text
[[[0.0, 1.0, 2.0, 0.0, -2.0, -1.0]]]
```

While the signal rises the output is positive, while it falls negative, and
zero where it is flat. PyTorch's convolution slides the kernel without
flipping it (mathematics calls this cross-correlation); for a learned kernel
the difference does not matter. In training the network finds its own kernels
like this: one becomes sensitive to jumps, another to vibration.

## Data: sensor windows

`make_sensor` produces sensor windows of 64 steps: a healthy window is a wave
plus noise; a faulty window has a short, sharp jump and vibration **at a
random place**.

```python
from dl_data import make_sensor

xs, ys = make_sensor(400, length=64, seed=7)
x = torch.from_numpy(xs).unsqueeze(1)
y = torch.from_numpy(ys)
x_train, y_train, x_test, y_test = x[:300], y[:300], x[300:], y[300:]
print(x.shape, y.sum().item(), len(y))
```

```text
torch.Size([400, 1, 64]) 119 400
```

`unsqueeze(1)` adds the channel dimension: `(400, 64)` → `(400, 1, 64)`.
119 of the windows are faulty.

## The model: convolution, ReLU, taking the largest

```python
class FaultNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv1d(1, 8, kernel_size=5, padding=2), nn.ReLU(),
            nn.Conv1d(8, 8, kernel_size=5, padding=2), nn.ReLU(),
            nn.AdaptiveMaxPool1d(1))
        self.head = nn.Linear(8, 2)

    def forward(self, x):
        return self.head(self.features(x).squeeze(-1))


def fit(model, epochs=15):
    loader = torch.utils.data.DataLoader(
        torch.utils.data.TensorDataset(x_train, y_train), batch_size=32, shuffle=True,
        generator=torch.Generator().manual_seed(0))
    opt = torch.optim.Adam(model.parameters(), lr=0.01)
    for epoch in range(epochs):
        model.train()
        for xb, yb in loader:
            opt.zero_grad()
            nn.functional.cross_entropy(model(xb), yb).backward()
            opt.step()
    model.eval()
    with torch.no_grad():
        return (model(x_test).argmax(dim=1) == y_test).float().mean().item()


torch.manual_seed(0)
cnn_acc = fit(FaultNet())
print(round(cnn_acc, 2), cnn_acc > 0.9)
```

```text
0.99 True
```

- `nn.AdaptiveMaxPool1d(1)` takes the **largest** value of each channel over
  the whole time axis: `(B, 8, 64)` → `(B, 8, 1)`. The answer to "did the
  jump detector go off anywhere in this window?" The position of the fault
  stops mattering.
- The network is 99% right on the test set. On this computer
  training took a few seconds.

## Knowing the position but not the pattern

For comparison let us train a linear model that takes the 64 values
directly:

```python
class Flat(nn.Module):
    def __init__(self):
        super().__init__()
        self.head = nn.Linear(64, 2)

    def forward(self, x):
        return self.head(x.squeeze(1))


torch.manual_seed(0)
flat_acc = fit(Flat())
print(round(flat_acc, 1), flat_acc < cnn_acc)
```

```text
0.7 True
```

The linear model learns a separate weight for every position; since the jump
is somewhere else in every window it finds no consistent weight and stays
around 70%. A convolution uses the same kernel at every
position, so it learns the pattern once and recognises it everywhere.

## Summary

- The input of `nn.Conv1d` is `(B, C, T)`: channel first. Turn an LSTM-style
  `(B, T, D)` around with `x.transpose(1, 2)`.
- The output length is `(T + 2·padding − kernel) // stride + 1`; the
  parameter count does not depend on the sequence length.
- The kernel is the same at every position: a pattern is recognised wherever
  it is. `AdaptiveMaxPool1d(1)` asks "is it anywhere?"
- All positions are computed at once; on long sequences this is much faster
  than an LSTM.
