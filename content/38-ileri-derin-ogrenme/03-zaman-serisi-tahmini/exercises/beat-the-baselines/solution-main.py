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
for epoch in range(15):
    for xb, yb in loader:
        opt.zero_grad()
        nn.functional.mse_loss(model(xb), yb).backward()
        opt.step()

model.eval()
actual = series[split:]

with torch.no_grad():
    pred = model(x_test).numpy() * std + mean
mae_lstm = np.abs(pred - actual).mean()
mae_naive = np.abs(series[split - 1:-1] - actual).mean()
mae_week = np.abs(series[split - 7:-7] - actual).mean()

print(mae_lstm < mae_naive, mae_lstm < mae_week)
