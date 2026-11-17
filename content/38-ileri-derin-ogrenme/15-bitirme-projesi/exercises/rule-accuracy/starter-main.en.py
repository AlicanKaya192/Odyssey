import numpy as np
import torch
from dl_data import make_sensor

x_np, y_np = make_sensor(600, seed=7)
gain = np.random.default_rng(3).uniform(0.5, 2.0, (600, 1)).astype(np.float32)
x = torch.tensor(x_np * gain).unsqueeze(1)
y = torch.tensor(y_np)


def rule_accuracy(threshold):
    # For the test set (500:600): fault if the largest |x| > threshold; accuracy, 2 places
    return 0.0

print(rule_accuracy(3.0))
