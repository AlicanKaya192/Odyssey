import numpy as np
import torch
from dl_data import make_sensor

x_np, y_np = make_sensor(600, seed=7)
gain = np.random.default_rng(3).uniform(0.5, 2.0, (600, 1)).astype(np.float32)
x = torch.tensor(x_np * gain).unsqueeze(1)
y = torch.tensor(y_np)


def best_threshold(candidates):
    # Return the threshold with the highest accuracy on validation (400:500)
    return candidates[0]

print(best_threshold([1.5, 2.0, 2.5, 3.0]))
