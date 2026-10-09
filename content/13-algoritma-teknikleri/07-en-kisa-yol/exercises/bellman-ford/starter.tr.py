import math


def bellman_ford(n, edges, start):
    dist = [math.inf] * n
    dist[start] = 0
    # n - 1 tur, sonra bir tur daha (negatif dongu).
    return [None if d == math.inf else d for d in dist]


print(bellman_ford(4, [[0, 1, 1], [0, 2, 4], [2, 1, -4], [1, 3, 3]], 0))
print(bellman_ford(3, [[0, 1, 1], [1, 2, -2], [2, 1, 1]], 0))
