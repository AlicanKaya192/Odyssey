import torch


def brightness_difference(a, b):
    x = torch.tensor(a, dtype=torch.uint8).to(torch.int16)
    y = torch.tensor(b, dtype=torch.uint8).to(torch.int16)
    return (x - y).abs().tolist()

print(brightness_difference([10, 200, 50], [30, 100, 50]))
print(brightness_difference([0, 255], [255, 0]))
