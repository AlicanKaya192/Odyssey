Write the function `dag_shortest(n, edges, start)`: the nodes are
`0`..`n − 1`, the edges `[a, b, weight]` are directed and **acyclic**; the
weight can be negative. It returns the shortest distance from `start` to each
node as a list; `None` for an unreachable one.

First a topological order (Kahn), then relax the outgoing edges of each node
in that order: `O(n + m)`, negative edges are no problem.

**Expected output:**

```
[0, 2, -1, 0, -2]
```
