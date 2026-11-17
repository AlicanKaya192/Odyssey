from torch import nn


def gan_param_count(z_dim, hidden):
    # Uretici: z_dim -> hidden -> 1, ayirt edici: 1 -> hidden -> 1
    return [0, 0]

print(gan_param_count(4, 16))
print(gan_param_count(2, 8))
