import torch
from torch import nn


def graph_ops(activation):
    act = nn.ReLU() if activation == "relu" else nn.Tanh()
    model = nn.Sequential(nn.Linear(3, 4), act, nn.Linear(4, 1)).eval()
    ep = torch.export.export(model, (torch.ones(2, 3),))
    ops = [str(n.target) for n in ep.graph.nodes if n.op == "call_function"]
    return [op.removeprefix("aten.") for op in ops]

print(graph_ops("relu"))
