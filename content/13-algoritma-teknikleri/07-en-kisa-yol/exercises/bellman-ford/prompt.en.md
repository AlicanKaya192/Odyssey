Write the function `bellman_ford(n, edges, start)`: the nodes are `0`..`n − 1`,
the edges `[a, b, weight]` (directed, the weight can be negative). It returns
the distance of each node from `start` as a list; `None` for an unreachable
one. If there is a negative cycle (an update still happens in an extra
round), it returns `None`.

Relax every edge for `n − 1` rounds.

**Expected output:**

```
[0, 0, 4, 3]
None
```
