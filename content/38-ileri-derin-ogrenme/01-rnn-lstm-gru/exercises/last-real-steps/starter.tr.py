import torch


def last_real_steps(out, lengths):
    # Kodunu buraya yaz
    return []

out = [[[1, 1], [2, 2], [3, 3]],
       [[4, 4], [5, 5], [0, 0]]]
print(last_real_steps(out, [3, 2]))
print(last_real_steps(out, [1, 1]))
