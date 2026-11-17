import torch


def quantize_int8(values):
    # [list of the int8 values, the scale with 4 places]
    return [[], 0.0]

print(quantize_int8([0.5, -1.27, 0.01]))
