import torch
from torch import nn


def graph_ops(activation):
    act = nn.ReLU() if activation == "relu" else nn.Tanh()
    model = nn.Sequential(nn.Linear(3, 4), act, nn.Linear(4, 1)).eval()
    # Disa aktar; call_function dugumlerinin hedeflerini "aten." oneki olmadan listele
    return []

print(graph_ops("relu"))
