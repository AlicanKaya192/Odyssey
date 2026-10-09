import math
from collections import deque


def dag_shortest(n, edges, start):
    out = {i: [] for i in range(n)}
    waiting = [0] * n
    for a, b, w in edges:
        out[a].append((b, w))
        waiting[b] += 1
    queue = deque(i for i in range(n) if waiting[i] == 0)
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for b, _ in out[node]:
            waiting[b] -= 1
            if waiting[b] == 0:
                queue.append(b)
    dist = [math.inf] * n
    dist[start] = 0
    for node in order:
        if dist[node] == math.inf:
            continue
        for b, w in out[node]:
            if dist[node] + w < dist[b]:
                dist[b] = dist[node] + w
    return [None if d == math.inf else d for d in dist]


print(dag_shortest(5, [[0, 1, 2], [0, 2, 6], [1, 2, -3], [2, 3, 1], [1, 3, 5], [3, 4, -2]], 0))
