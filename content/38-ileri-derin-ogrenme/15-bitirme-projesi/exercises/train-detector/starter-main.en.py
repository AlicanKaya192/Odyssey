import numpy as np
import torch
import torch.nn.functional as F
from torch import nn
from dl_data import make_sensor

x_np, y_np = make_sensor(600, seed=7)
gain = np.random.default_rng(3).uniform(0.5, 2.0, (600, 1)).astype(np.float32)
x = torch.tensor(x_np * gain).unsqueeze(1)
y = torch.tensor(y_np)
torch.manual_seed(0)
model = nn.Sequential(
    nn.Conv1d(1, 16, 5, padding=2), nn.ReLU(), nn.MaxPool1d(2),
    nn.Conv1d(16, 32, 5, padding=2), nn.ReLU(), nn.AdaptiveMaxPool1d(1),
    nn.Flatten(), nn.Linear(32, 2))
opt = torch.optim.Adam(model.parameters(), lr=0.003)
loader = torch.utils.data.DataLoader(
    torch.utils.data.TensorDataset(x[:400], y[:400]), batch_size=32, shuffle=True,
    generator=torch.Generator().manual_seed(1))
# 1) Train for 10 epochs (model.train(), zero_grad, cross_entropy, backward, step)
# 2) model.eval(); predict on test (500:600), compute acc and the fault class's recall
acc, recall = 0.0, 0.0

print(acc > 0.9, recall > 0.8)
