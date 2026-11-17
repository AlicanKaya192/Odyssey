import torch


def result_shape(shape_a, shape_b):
    try:
        total = torch.zeros(shape_a) + torch.zeros(shape_b)
    except RuntimeError:
        return "error"
    return list(total.shape)

print(result_shape([3, 2], [2]))
print(result_shape([3, 1], [1, 4]))
print(result_shape([3, 2], [3]))
