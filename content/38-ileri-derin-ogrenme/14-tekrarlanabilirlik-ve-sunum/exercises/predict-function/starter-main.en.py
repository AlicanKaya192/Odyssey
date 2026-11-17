import torch
import torch.nn.functional as F
from torch import nn
from dl_data import make_table

x, y = map(torch.tensor, make_table(600, seed=7))
torch.manual_seed(0)
model = nn.Sequential(nn.Linear(6, 32), nn.ReLU(), nn.Linear(32, 3))
opt = torch.optim.Adam(model.parameters(), lr=0.01)
for _ in range(100):
    opt.zero_grad()
    F.cross_entropy(model(x[:500]), y[:500]).backward()
    opt.step()
model.eval()
CLASSES = ["low", "mid", "high"]


def predict(values):
    # If not 6 values: ValueError("expected 6 values, got N")
    # softmax inside inference_mode; {"label": ..., "probability": 2 places}
    return {}

answer = predict([0.0, 2.0, 0.0, 1.5, 0.0, 0.0])
print(answer["label"], 0.5 < answer["probability"] <= 1.0)
try:
    predict([1.0])
except ValueError as e:
    print(e)
