## Ready patterns

**BFS (fewest steps)**

```python
from collections import deque


def bfs(graph, start):
    dist = {start: 0}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for nxt in graph[node]:
            if nxt not in dist:
                dist[nxt] = dist[node] + 1
                queue.append(nxt)
    return dist
```

**Dijkstra (weighted, no negatives)**

```python
import heapq


def dijkstra(graph, start):
    dist = {start: 0}
    heap = [(0, start)]
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist[node]:
            continue                       # a stale entry
        for nxt, w in graph[node]:
            if d + w < dist.get(nxt, float("inf")):
                dist[nxt] = d + w
                heapq.heappush(heap, (d + w, nxt))
    return dist
```

**Union-find**

```python
def make_find(parent):
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    return find
```

**Dynamic programming (with memory)**

```python
from functools import cache


@cache
def ways(n):
    if n <= 1:
        return 1
    return ways(n - 1) + ways(n - 2)
```

## Python's ready tools

| Job | Tool |
|---|---|
| Heap | `heapq.heappush`, `heappop`, `nsmallest` |
| Queue | `collections.deque` |
| Counting | `collections.Counter` |
| Memory | `functools.cache` |
| Binary search | `bisect.bisect_left`, `bisect_right` |
| Topological order | `graphlib.TopologicalSorter` |
| Orders, combinations | `itertools.permutations`, `combinations` |
| GCD, integer square root | `math.gcd`, `math.isqrt` |
| Power with mod | `pow(a, e, m)` |
| Stable hash | `hashlib`, `zlib.crc32` |
