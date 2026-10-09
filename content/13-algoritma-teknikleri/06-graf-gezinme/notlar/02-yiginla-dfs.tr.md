Özyineli DFS'te çağrı yığınını Python tutuyor ve derinliği yaklaşık 1000 ile
sınırlı. Aynı işi kendi yığınımızla yaparsak sınır yok:

```python
def dfs_stack(graph, start):
    order, seen, stack = [], set(), [start]
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        order.append(node)
        for neighbour in sorted(graph[node], reverse=True):
            if neighbour not in seen:
                stack.append(neighbour)     # ters sırayla: küçük ad önce çıksın
    return order

chain = {i: set() for i in range(5000)}     # 0 - 1 - 2 - ... - 4999
for i in range(4999):
    chain[i].add(i + 1)
    chain[i + 1].add(i)

order = dfs_stack(chain, 0)
print(len(order), order[:5], order[-1])

small = {"a": {"b", "c"}, "b": {"a", "d"}, "c": {"a"}, "d": {"b"}}
print(dfs_stack(small, "a"))
```

```text
5000 [0, 1, 2, 3, 4] 4999
['a', 'b', 'd', 'c']
```

Komşular **ters sırayla** yığına konuyor; yığından son giren ilk çıktığı için
böylece özyineli DFS ile aynı sırada (alfabetik) geziliyor. Bir düğüm yığına
birden çok kez girebilir; çıkarken `seen` denetimi onu ikinci kez işlemez.
