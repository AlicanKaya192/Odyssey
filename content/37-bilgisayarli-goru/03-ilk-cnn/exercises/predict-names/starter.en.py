import torch

NAMES = ["circle", "square", "triangle"]


def predict_names(logits):
    return []

print(predict_names([[0.1, 2.0, -1.0], [3.0, 0.0, 0.5], [0.0, 0.1, 0.2]]))
