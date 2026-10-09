import math


def all_pairs(n, edges):
    d = [[math.inf] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    for a, b, w in edges:
        d[a][b] = min(d[a][b], w)
        d[b][a] = min(d[b][a], w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return [[-1 if x == math.inf else x for x in row] for row in d]


for row in all_pairs(4, [[0, 1, 3], [1, 2, 1], [0, 2, 7]]):
    print(row)
