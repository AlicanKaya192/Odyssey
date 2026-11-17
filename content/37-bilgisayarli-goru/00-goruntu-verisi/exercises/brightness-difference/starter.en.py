import torch


def brightness_difference(a, b):
    # There is a bug here: uint8 subtraction wraps around.
    x = torch.tensor(a, dtype=torch.uint8)
    y = torch.tensor(b, dtype=torch.uint8)
    return (x - y).abs().tolist()

print(brightness_difference([10, 200, 50], [30, 100, 50]))
print(brightness_difference([0, 255], [255, 0]))
