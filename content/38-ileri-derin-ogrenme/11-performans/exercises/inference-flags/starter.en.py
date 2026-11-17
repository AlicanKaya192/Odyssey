import torch
from torch import nn


def inference_flags():
    model = nn.Linear(4, 2)
    x = torch.ones(3, 4)
    # [requires_grad of the normal output, requires_grad of the inference_mode output,
    #  is_inference() of the inference_mode output]
    return [False, False, False]

print(inference_flags())
