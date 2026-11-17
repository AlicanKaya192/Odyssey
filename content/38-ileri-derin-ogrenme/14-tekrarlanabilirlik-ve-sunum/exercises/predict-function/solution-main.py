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
    if len(values) != 6:
        raise ValueError(f"expected 6 values, got {len(values)}")
    with torch.inference_mode():
        logits = model(torch.tensor([values], dtype=torch.float32))
        probs = torch.softmax(logits, dim=1)[0]
    best = int(probs.argmax())
    return {"label": CLASSES[best], "probability": round(probs[best].item(), 2)}

answer = predict([0.0, 2.0, 0.0, 1.5, 0.0, 0.0])
print(answer["label"], 0.5 < answer["probability"] <= 1.0)
try:
    predict([1.0])
except ValueError as e:
    print(e)
