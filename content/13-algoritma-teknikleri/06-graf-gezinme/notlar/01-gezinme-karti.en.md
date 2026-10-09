## Two templates

```python
from collections import deque

def bfs(graph, start):                     # a queue: level by level
    seen, queue = {start}, deque([start])
    while queue:
        node = queue.popleft()
        for nxt in graph[node]:
            if nxt not in seen:
                seen.add(nxt)              # mark when entering the queue
                queue.append(nxt)
    return seen

def dfs(graph, start):                     # a stack: all the way down
    seen, stack = set(), [start]
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        stack.extend(graph[node])
    return seen
```

## Which one?

| Question | Choose |
|---|---|
| The path with the fewest steps (unweighted) | BFS |
| Nodes at a given distance ("two steps away") | BFS |
| Is there a path? Connected components | either |
| Is there a cycle? Topological sorting | DFS |
| The shortest weighted path | neither → Dijkstra (next section) |

## Cost

Each node enters the queue/stack once and each edge is looked at once:
`O(n + m)`. Memory `O(n)`.

## Common mistakes

- Not keeping the visited nodes → an endless loop on a cycle.
- Marking a node in BFS when it **leaves** the queue: the same node enters the
  queue many times; the right way is to mark it when it **enters**.
- Using a list as the queue: `pop(0)` is `O(n)`; use `deque.popleft()`.
- Taking the path BFS gives as the shortest in a weighted graph: BFS minimises
  the **number** of edges, not the total weight.
- Recursive DFS on deep graphs → `RecursionError`.
