# Time Series Forecasting with an LSTM

The Time Series track covered forecasting with statistical methods: the
seasonal naive forecast, exponential smoothing, ARIMA, and as the most
important lesson, **not trusting a model before it beats a baseline**. This
section does the same job with an LSTM: a network that reads the past 28 days
and forecasts the next day. The method is new, the rules are old: split by
time, learn the scaling from the past only, and compare the result with naive
forecasts.

The series comes from `make_series`: two years of daily values; a rising
trend, weekly and yearly seasons, and noise on top.

## Windows: from a series to examples

An LSTM is not given a "series", it is given **windows**: 28 consecutive
values as input, the value right after them as the target. Shifting the
window by one day gives a new example.

```python
import numpy as np
import torch
from torch import nn
from dl_data import make_series

series = make_series(730)
split = 630
mean, std = series[:split].mean(), series[:split].std()
scaled = (series - mean) / std


def windows(values, size):
    xs = [values[i:i + size] for i in range(len(values) - size)]
    ys = [values[i + size] for i in range(len(values) - size)]
    return torch.tensor(np.array(xs)).unsqueeze(-1), torch.tensor(np.array(ys))


x_train, y_train = windows(scaled[:split], 28)
x_test, y_test = windows(scaled[split - 28:], 28)
print(series.shape, x_train.shape, y_train.shape)
print(x_test.shape, y_test.shape)
```

```text
(730,) torch.Size([602, 28, 1]) torch.Size([602])
torch.Size([100, 28, 1]) torch.Size([100])
```

- **Split by time:** the first 630 days for training, the last 100 for
  testing. A shuffled split would leak the future into training.
- **Scaling from training only:** the mean and standard deviation come from
  the first 630 days. Computed from the whole series, the level of the test
  period would leak into training (because of the trend and the yearly
  season the test period sits at a different level; see the second note).
- The test windows start in the last 28 days of training, so that the first
  test day can be forecast too: 100 test days, 100 windows.
- The last dimension of the input is 1: there is one number per step.
  `unsqueeze(-1)` turns the shape `(N, 28)` into `(N, 28, 1)`; the LSTM wants
  `(B, T, D)`.

## Model and training

```python
class Forecaster(nn.Module):
    def __init__(self, hidden=32):
        super().__init__()
        self.lstm = nn.LSTM(1, hidden, batch_first=True)
        self.head = nn.Linear(hidden, 1)

    def forward(self, x):
        out, (h, c) = self.lstm(x)
        return self.head(h[-1]).squeeze(-1)


torch.manual_seed(0)
model = Forecaster()
loader = torch.utils.data.DataLoader(
    torch.utils.data.TensorDataset(x_train, y_train), batch_size=32, shuffle=True,
    generator=torch.Generator().manual_seed(0))
opt = torch.optim.Adam(model.parameters(), lr=0.005)
loss_fn = nn.MSELoss()
for epoch in range(20):
    model.train()
    for xb, yb in loader:
        opt.zero_grad()
        loss = loss_fn(model(xb), yb)
        loss.backward()
        opt.step()
print(model(x_test[:3]).shape)
```

```text
torch.Size([3])
```

- This is **regression**: the output is one number and the loss is the mean
  squared error (`MSELoss`). `squeeze(-1)` makes `(B, 1)` into `(B,)` so that
  it has the same shape as the target; otherwise broadcasting builds a wrong
  `(B, B)` matrix of differences and the loss is silently wrong.
- 20 epochs took a few seconds on this computer.

## Comparing with baselines

We scale the forecasts back and measure them in the original units with the
**mean absolute error** (MAE). Two baselines: yesterday's value (naive) and
the same day last week (seasonal naive).

```python
model.eval()
with torch.no_grad():
    pred = model(x_test).numpy() * std + mean
actual = series[split:]
mae_lstm = np.abs(pred - actual).mean()
mae_naive = np.abs(series[split - 1:-1] - actual).mean()
mae_week = np.abs(series[split - 7:-7] - actual).mean()
print(round(float(mae_naive), 1), round(float(mae_week), 1))
print(round(float(mae_lstm), 1))
print(mae_lstm < mae_naive, mae_lstm < mae_week)
```

```text
4.8 2.4
1.9
True True
```

- The naive forecast is off by 4.8 units, the seasonal naive by
  2.4. The weekly season is strong, so the same day last week is
  a better forecast than yesterday.
- At 1.9 the LSTM beats both: it uses the weekly pattern and the
  level of the last days together.
- The noise in the series has a standard deviation of 2; the mean absolute
  value of such noise is about 1.6. Noise cannot be forecast,
  so no model can go below that; the LSTM is close to this limit.

## When an LSTM?

What the Time Series track showed by measuring holds here too: the gain
usually comes not from the method but from **information** (calendar,
holidays, promotions). An LSTM stands out in these cases:

| Situation | LSTM | Statistical method |
|---|---|---|
| One short series | Hard to learn from little data | Often enough, and better |
| Hundreds of similar series | One model can learn them all | A separate model per series |
| Many outside variables, non-linear relations | Takes them naturally | Needs hand-made features |
| An uncertainty interval | Takes extra work | Ready in most methods |

## Summary

- A series is cut into windows: `(N, T, 1)` input, the next value as the
  target.
- Split by time; take the scaling statistics from the training period only.
- For regression use `MSELoss`; bring the output to the target's shape
  (`squeeze(-1)`), otherwise broadcasting silently computes a wrong loss.
- Always compare with the naive and the seasonal naive forecast; use the
  model only if it beats both.
