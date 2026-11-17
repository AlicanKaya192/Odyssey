import time
import torch
from torch import nn


def timeit(fn, repeat=5):
    # fn'i repeat kez calistir, time.perf_counter ile olc, en kisasini dondur
    return 0.0

torch.manual_seed(0)
model = nn.Sequential(nn.Linear(64, 128), nn.ReLU(), nn.Linear(128, 10)).eval()
x = torch.randn(512, 64)
with torch.inference_mode():
    loop = timeit(lambda: [model(row) for row in x])
    batch = timeit(lambda: model(x))
print(batch < loop / 10)
