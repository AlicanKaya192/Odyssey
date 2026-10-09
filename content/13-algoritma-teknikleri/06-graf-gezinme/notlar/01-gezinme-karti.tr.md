## İki şablon

```python
from collections import deque

def bfs(graph, start):                     # kuyruk: kat kat
    seen, queue = {start}, deque([start])
    while queue:
        node = queue.popleft()
        for nxt in graph[node]:
            if nxt not in seen:
                seen.add(nxt)              # kuyruğa girerken işaretle
                queue.append(nxt)
    return seen

def dfs(graph, start):                     # yığın: dibine kadar
    seen, stack = set(), [start]
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        stack.extend(graph[node])
    return seen
```

## Hangisi?

| Soru | Seç |
|---|---|
| En az adımlı yol (ağırlıksız) | BFS |
| Belli bir uzaklıktaki düğümler ("2 adım ötedekiler") | BFS |
| Bir yol var mı? Bağlı bileşenler | ikisi de |
| Döngü var mı? Topolojik sıralama | DFS |
| Ağırlıklı en kısa yol | ikisi de değil → Dijkstra (sonraki bölüm) |

## Maliyet

Her düğüm bir kez kuyruğa/yığına girer, her kenara bir kez bakılır:
`O(n + m)`. Bellek `O(n)`.

## Sık hatalar

- Ziyaret edilenleri tutmamak → döngüde sonsuz döngü.
- BFS'te düğümü kuyruktan **çıkarken** işaretlemek: aynı düğüm kuyruğa
  birçok kez girer; doğru olan **girerken** işaretlemek.
- Kuyruk için liste kullanmak: `pop(0)` `O(n)`; `deque.popleft()` kullan.
- Ağırlıklı grafta BFS'in verdiği yolu en kısa sanmak: BFS kenar **sayısını**
  en aza indirir, toplam ağırlığı değil.
- Derin graflarda özyineli DFS → `RecursionError`.
