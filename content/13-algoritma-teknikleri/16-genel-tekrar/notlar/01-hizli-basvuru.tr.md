## Hazır kalıplar

**BFS (en az adım)**

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

**Dijkstra (ağırlıklı, negatif yok)**

```python
import heapq


def dijkstra(graph, start):
    dist = {start: 0}
    heap = [(0, start)]
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist[node]:
            continue                       # eski kayıt
        for nxt, w in graph[node]:
            if d + w < dist.get(nxt, float("inf")):
                dist[nxt] = d + w
                heapq.heappush(heap, (d + w, nxt))
    return dist
```

**Birleşim-bulma**

```python
def make_find(parent):
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    return find
```

**Dinamik programlama (bellekle)**

```python
from functools import cache


@cache
def ways(n):
    if n <= 1:
        return 1
    return ways(n - 1) + ways(n - 2)
```

## Python'un hazırları

| İş | Araç |
|---|---|
| Heap | `heapq.heappush`, `heappop`, `nsmallest` |
| Kuyruk | `collections.deque` |
| Sayma | `collections.Counter` |
| Bellek | `functools.cache` |
| İkili arama | `bisect.bisect_left`, `bisect_right` |
| Topolojik sıra | `graphlib.TopologicalSorter` |
| Sıralanış, kombinasyon | `itertools.permutations`, `combinations` |
| EBOB, tam karekök | `math.gcd`, `math.isqrt` |
| Mod ile üs | `pow(a, e, m)` |
| Kararlı hash | `hashlib`, `zlib.crc32` |
