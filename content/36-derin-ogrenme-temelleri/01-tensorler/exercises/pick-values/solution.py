import torch


def pick(rows, limit):
    t = torch.tensor(rows)
    first_column = t[:, 0].tolist()
    big = t[t > limit].tolist()
    return [first_column, big]

table = [[1, 9, 3], [8, 2, 7], [5, 6, 4]]
print(pick(table, 6))
print(pick(table, 10))
