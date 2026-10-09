import math


def all_pairs(n, edges):
    d = [[math.inf] * n for _ in range(n)]
    # Diagonal 0, edges both ways; then three loops.
    return [[-1 if x == math.inf else x for x in row] for row in d]


for row in all_pairs(4, [[0, 1, 3], [1, 2, 1], [0, 2, 7]]):
    print(row)
