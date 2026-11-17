import numpy as np
import torch
from dl_data import make_sensor

x_np, y_np = make_sensor(600, seed=7)
gain = np.random.default_rng(3).uniform(0.5, 2.0, (600, 1)).astype(np.float32)
x = torch.tensor(x_np * gain).unsqueeze(1)
y = torch.tensor(y_np)


def best_threshold(candidates):
    def val_accuracy(t):
        pred = (x[400:500].abs().amax(dim=(1, 2)) > t).long()
        return (pred == y[400:500]).float().mean().item()

    return max(candidates, key=val_accuracy)

print(best_threshold([1.5, 2.0, 2.5, 3.0]))
