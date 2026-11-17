from torch import nn


def ae_param_count(code):
    # Kodlayıcı: 64 -> 32 -> code, kod çözücü: code -> 32 -> 64
    return 0

print(ae_param_count(4))
print(ae_param_count(2))
