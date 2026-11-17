import numpy as np
import torch
from dl_data import make_sensor

x_np, y_np = make_sensor(600, seed=7)
gain = np.random.default_rng(3).uniform(0.5, 2.0, (600, 1)).astype(np.float32)
x = torch.tensor(x_np * gain).unsqueeze(1)
y = torch.tensor(y_np)


def rule_accuracy(threshold):
    pred = (x[500:].abs().amax(dim=(1, 2)) > threshold).long()
    return round((pred == y[500:]).float().mean().item(), 2)

print(rule_accuracy(3.0))
