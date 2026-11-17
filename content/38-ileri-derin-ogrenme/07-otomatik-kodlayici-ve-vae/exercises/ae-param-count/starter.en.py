from torch import nn


def ae_param_count(code):
    # Encoder: 64 -> 32 -> code, decoder: code -> 32 -> 64
    return 0

print(ae_param_count(4))
print(ae_param_count(2))
