import torch


def temperature_probs(logits, temp):
    probs = torch.softmax(torch.tensor(logits) / temp, dim=0)
    return [round(p, 3) for p in probs.tolist()]

print(temperature_probs([2.0, 1.0, 0.1], 0.5))
print(temperature_probs([2.0, 1.0, 0.1], 2.0))
