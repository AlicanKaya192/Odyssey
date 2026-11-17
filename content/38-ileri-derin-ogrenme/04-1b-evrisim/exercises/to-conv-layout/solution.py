import torch


def to_conv_layout(batch):
    return torch.tensor(batch).transpose(1, 2).tolist()

batch = [[[1, 2, 3], [4, 5, 6]]]
print(to_conv_layout(batch))
