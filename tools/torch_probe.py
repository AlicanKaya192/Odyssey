"""PyTorch sonuçları makineler arasında ne kadar aynı? (Derin Öğrenme patikası ölçümü.)

Patikadaki alıştırmalara benzeyen küçük eğitimler sabit tohumla çalıştırılır;
kayıplar, doğruluk, tahminler ve ağırlık toplamı tam hâliyle JSON'a yazılır.
Dökümler Windows'ta `compare` ile karşılaştırılır: her değer için iki makinede
kaç ondalığa kadar aynı çıktığı ve tahminlerin birebir tutup tutmadığı.

Kullanım:
  python tools/torch_probe.py run <çıktı.json>
  python tools/torch_probe.py compare <a.json> <b.json> ...
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import sys
from pathlib import Path


def _summary(losses, logits, labels, model):
    import torch

    preds = logits.argmax(1).tolist()
    weight_sum = sum(float(p.double().sum()) for p in model.parameters())
    return {
        "loss_first": losses[0],
        "loss_mid": losses[len(losses) // 2],
        "loss_last": losses[-1],
        "acc": sum(int(p == t) for p, t in zip(preds, labels.tolist())) / len(preds),
        "preds_sha": hashlib.sha1(json.dumps(preds).encode()).hexdigest()[:12],
        "weight_sum": weight_sum,
        "logit_0": float(logits[0, 0]),
        "dtype": str(torch.get_default_dtype()),
    }


def mlp():
    import torch

    torch.manual_seed(0)
    x = torch.randn(512, 20)
    y = (x @ torch.randn(20, 1) > 0).long().squeeze(1)
    model = torch.nn.Sequential(torch.nn.Linear(20, 32), torch.nn.ReLU(), torch.nn.Linear(32, 2))
    opt = torch.optim.Adam(model.parameters(), lr=0.01)
    losses = []
    for _ in range(200):
        opt.zero_grad()
        loss = torch.nn.functional.cross_entropy(model(x), y)
        loss.backward()
        opt.step()
        losses.append(loss.item())
    with torch.no_grad():
        return _summary(losses, model(x), y, model)


def cnn_digits():
    import torch
    from sklearn.datasets import load_digits

    digits = load_digits()
    x = torch.tensor(digits.images, dtype=torch.float32).unsqueeze(1) / 16.0
    y = torch.tensor(digits.target)
    torch.manual_seed(0)
    model = torch.nn.Sequential(
        torch.nn.Conv2d(1, 8, 3, padding=1), torch.nn.ReLU(), torch.nn.MaxPool2d(2),
        torch.nn.Conv2d(8, 16, 3, padding=1), torch.nn.ReLU(), torch.nn.MaxPool2d(2),
        torch.nn.Flatten(), torch.nn.Linear(16 * 2 * 2, 10),
    )
    opt = torch.optim.SGD(model.parameters(), lr=0.1, momentum=0.9)
    loader = torch.utils.data.DataLoader(
        torch.utils.data.TensorDataset(x, y), batch_size=64, shuffle=True,
        generator=torch.Generator().manual_seed(0),
    )
    losses = []
    for _ in range(10):
        for xb, yb in loader:
            opt.zero_grad()
            loss = torch.nn.functional.cross_entropy(model(xb), yb)
            loss.backward()
            opt.step()
        losses.append(loss.item())
    model.eval()
    with torch.no_grad():
        return _summary(losses, model(x), y, model)


def lstm_seq():
    import torch

    torch.manual_seed(0)
    x = torch.randn(256, 15, 4)
    y = (x[:, :, 0].sum(1) > 0).long()

    class Net(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.lstm = torch.nn.LSTM(4, 16, batch_first=True)
            self.head = torch.nn.Linear(16, 2)

        def forward(self, seq):
            out, _ = self.lstm(seq)
            return self.head(out[:, -1])

    model = Net()
    opt = torch.optim.Adam(model.parameters(), lr=0.01)
    losses = []
    for _ in range(60):
        opt.zero_grad()
        loss = torch.nn.functional.cross_entropy(model(x), y)
        loss.backward()
        opt.step()
        losses.append(loss.item())
    with torch.no_grad():
        return _summary(losses, model(x), y, model)


def transformer():
    import torch

    torch.manual_seed(0)
    x = torch.randn(128, 10, 16)
    y = (x[:, :, :3].mean((1, 2)) > 0).long()
    layer = torch.nn.TransformerEncoderLayer(16, 4, dim_feedforward=32, dropout=0.0, batch_first=True)
    encoder = torch.nn.TransformerEncoder(layer, 2, enable_nested_tensor=False)
    head = torch.nn.Linear(16, 2)
    model = torch.nn.ModuleList([encoder, head])
    opt = torch.optim.AdamW(model.parameters(), lr=0.005)
    losses = []
    for _ in range(40):
        opt.zero_grad()
        loss = torch.nn.functional.cross_entropy(head(encoder(x).mean(1)), y)
        loss.backward()
        opt.step()
        losses.append(loss.item())
    model.eval()
    with torch.no_grad():
        return _summary(losses, head(encoder(x).mean(1)), y, model)


def autoencoder():
    import torch
    from sklearn.datasets import load_digits

    x = torch.tensor(load_digits().data, dtype=torch.float32) / 16.0
    torch.manual_seed(0)
    model = torch.nn.Sequential(
        torch.nn.Linear(64, 16), torch.nn.ReLU(), torch.nn.Linear(16, 4),
        torch.nn.Linear(4, 16), torch.nn.ReLU(), torch.nn.Linear(16, 64), torch.nn.Sigmoid(),
    )
    opt = torch.optim.Adam(model.parameters(), lr=0.01)
    losses = []
    for _ in range(100):
        opt.zero_grad()
        loss = torch.nn.functional.mse_loss(model(x), x)
        loss.backward()
        opt.step()
        losses.append(loss.item())
    with torch.no_grad():
        out = model(x)
        return {
            "loss_first": losses[0], "loss_mid": losses[50], "loss_last": losses[-1],
            "weight_sum": sum(float(p.double().sum()) for p in model.parameters()),
            "out_0": float(out[0, 10]),
        }


SCENARIOS = {"mlp": mlp, "cnn_digits": cnn_digits, "lstm_seq": lstm_seq,
             "transformer": transformer, "autoencoder": autoencoder}


def run(target: Path) -> int:
    import torch

    torch.set_num_threads(1)
    result = {
        "machine": f"{platform.system()} {platform.machine()}",
        "torch": torch.__version__,
        "capability": torch.backends.cpu.get_cpu_capability(),
        "env": {k: os.environ.get(k, "") for k in ("ATEN_CPU_CAPABILITY", "MKL_CBWR", "OMP_NUM_THREADS")},
        "scenarios": {name: fn() for name, fn in SCENARIOS.items()},
    }
    target.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


def _digits(a: float, b: float) -> int:
    """İki sayı kaç ondalığa yuvarlanınca aynı çıkıyor (0–12, eşitse 99)."""
    if a == b:
        return 99
    for d in range(12, -1, -1):
        if round(a, d) == round(b, d):
            return d
    return -1


def compare(paths: list[str]) -> int:
    dumps = [json.loads(Path(p).read_text(encoding="utf-8")) for p in paths]
    base = dumps[0]
    print("taban:", base["machine"], base["capability"], base["env"])
    for other in dumps[1:]:
        print(f"\n== {other['machine']} {other['capability']} {other['env']}")
        for name, values in base["scenarios"].items():
            other_values = other["scenarios"].get(name, {})
            parts = []
            for key, value in values.items():
                if key not in other_values:
                    continue
                if isinstance(value, float):
                    parts.append(f"{key}={_digits(value, other_values[key])}")
                else:
                    parts.append(f"{key}={'aynı' if value == other_values[key] else 'FARKLI'}")
            print(f"  {name:12} " + " ".join(parts))
    return 0


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "run":
        raise SystemExit(run(Path(sys.argv[2])))
    if len(sys.argv) >= 4 and sys.argv[1] == "compare":
        raise SystemExit(compare(sys.argv[2:]))
    print(__doc__)
    raise SystemExit(2)
