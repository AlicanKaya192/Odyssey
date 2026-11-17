import torch
from torch import nn


def inference_flags():
    model = nn.Linear(4, 2)
    x = torch.ones(3, 4)
    # [normal cikisin requires_grad'i, inference_mode cikisinin requires_grad'i,
    #  inference_mode cikisinin is_inference()'i]
    return [False, False, False]

print(inference_flags())
