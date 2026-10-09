import math


def bellman_ford(n, edges, start):
    dist = [math.inf] * n
    dist[start] = 0
    for _ in range(n - 1):
        for a, b, w in edges:
            if dist[a] + w < dist[b]:
                dist[b] = dist[a] + w
    for a, b, w in edges:
        if dist[a] + w < dist[b]:
            return None
    return [None if d == math.inf else d for d in dist]


print(bellman_ford(4, [[0, 1, 1], [0, 2, 4], [2, 1, -4], [1, 3, 3]], 0))
print(bellman_ford(3, [[0, 1, 1], [1, 2, -2], [2, 1, 1]], 0))
