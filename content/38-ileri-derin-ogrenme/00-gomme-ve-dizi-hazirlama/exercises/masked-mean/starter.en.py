import torch


def masked_mean(vectors, mask):
    # Write your code here
    return []

vectors = [[[1.0, 2.0], [3.0, 4.0], [0.0, 0.0]],
           [[2.0, 2.0], [0.0, 0.0], [0.0, 0.0]]]
mask = [[1, 1, 0], [1, 0, 0]]
print(masked_mean(vectors, mask))
