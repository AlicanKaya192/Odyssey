import math
from collections import deque


def dag_shortest(n, edges, start):
    out = {i: [] for i in range(n)}
    waiting = [0] * n
    for a, b, w in edges:
        out[a].append((b, w))
        waiting[b] += 1
    # 1. Kahn ile sira.  2. Sirayla gevset.
    dist = [math.inf] * n
    dist[start] = 0
    return [None if d == math.inf else d for d in dist]


print(dag_shortest(5, [[0, 1, 2], [0, 2, 6], [1, 2, -3], [2, 3, 1], [1, 3, 5], [3, 4, -2]], 0))
