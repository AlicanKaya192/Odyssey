import torch


def pairwise_sq_dist(a, b):
    # This loop is correct but slow; remove it, write it with broadcasting
    out = []
    for p in a:
        row = []
        for r in b:
            row.append(int(sum((x - y) ** 2 for x, y in zip(p, r))))
        out.append(row)
    return out

print(pairwise_sq_dist([[0.0, 0.0], [1.0, 2.0]], [[1.0, 0.0], [3.0, 2.0]]))
