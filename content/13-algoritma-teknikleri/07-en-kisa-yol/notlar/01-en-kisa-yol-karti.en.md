## Which algorithm?

| Situation | Algorithm | Cost |
|---|---|---|
| Unweighted (every edge is 1) | BFS | `O(n + m)` |
| Weighted, no negatives, one start | Dijkstra (heap) | `O((n + m) log n)` |
| Negative edges possible | Bellman–Ford | `O(n · m)` |
| All pairs, a small graph | Floyd–Warshall | `O(n³)` |
| One goal, a good estimate | A* | usually fewer nodes than Dijkstra |
| Directed acyclic graph (DAG) | relax in topological order | `O(n + m)` (next section) |

## Relaxation

The common step of all of them:

```python
if dist[a] + w < dist[b]:
    dist[b] = dist[a] + w
    parent[b] = a
```

"Is going to `b` through `a` shorter than what we know so far?" The
algorithms differ only in **the order** in which they do this step.

## Common mistakes

- Dijkstra on a graph with negative edges: a silently wrong result.
- Putting `(node, distance)` in the heap instead of `(distance, node)`: the
  heap sorts by name.
- Not skipping old records popped from the heap (a `done` or
  `d > dist[node]` check): it still works but does needless work.
- An unreachable node: `dist.get(node, math.inf)`; it stays infinite in the
  result.
- Overestimating in A*: faster, but the shortest-path guarantee is gone.
